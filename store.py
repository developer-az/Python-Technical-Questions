"""Unified durable store for Drill.

One SQLite database replaces scattered JSON files, localStorage drafts,
and query-param session hacks. Scales as curriculum and users grow —
stdlib only, no extra deps.
"""

from __future__ import annotations

import json
import math
import os
import sqlite3
import threading
import time
import uuid
from contextlib import contextmanager
from typing import Dict, List, Optional

DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "drill.db"
)

QUALITY = {"again": 1, "hard": 2, "good": 3, "easy": 4}


def _now() -> float:
    return time.time()


class UserStore:
    """Thread-safe SQLite persistence for cards, notes, drafts, progress."""

    def __init__(self, path: str = DEFAULT_DB_PATH):
        self.path = path
        self._lock = threading.RLock()
        directory = os.path.dirname(path) or "."
        os.makedirs(directory, exist_ok=True)
        self._init_schema()
        if os.path.abspath(path) == os.path.abspath(DEFAULT_DB_PATH):
            self._migrate_legacy_json()

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.path, timeout=30, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_schema(self) -> None:
        with self._lock, self._conn() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS cards (
                    id TEXT PRIMARY KEY,
                    kind TEXT NOT NULL,
                    ref_id TEXT NOT NULL,
                    ease REAL NOT NULL DEFAULT 2.5,
                    interval_days REAL NOT NULL DEFAULT 0,
                    repetitions INTEGER NOT NULL DEFAULT 0,
                    lapses INTEGER NOT NULL DEFAULT 0,
                    due_at REAL NOT NULL DEFAULT 0,
                    stability REAL NOT NULL DEFAULT 0,
                    seen_encode INTEGER NOT NULL DEFAULT 0,
                    last_quality TEXT,
                    last_review_at REAL,
                    created_at REAL NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_cards_due ON cards(due_at);
                CREATE INDEX IF NOT EXISTS idx_cards_kind_ref ON cards(kind, ref_id);

                CREATE TABLE IF NOT EXISTS elaborations (
                    method_id TEXT PRIMARY KEY,
                    text TEXT NOT NULL DEFAULT '',
                    updated_at REAL,
                    history_json TEXT NOT NULL DEFAULT '[]'
                );

                CREATE TABLE IF NOT EXISTS notepads (
                    question_id INTEGER PRIMARY KEY,
                    content TEXT NOT NULL DEFAULT '',
                    updated_at REAL
                );

                CREATE TABLE IF NOT EXISTS notes (
                    id TEXT PRIMARY KEY,
                    text TEXT NOT NULL,
                    kind TEXT NOT NULL DEFAULT 'technique',
                    question_id INTEGER,
                    method_id TEXT,
                    language TEXT DEFAULT 'python',
                    source TEXT DEFAULT 'comment',
                    created_at REAL NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_notes_q ON notes(question_id);
                CREATE INDEX IF NOT EXISTS idx_notes_m ON notes(method_id);

                CREATE TABLE IF NOT EXISTS drafts (
                    question_id INTEGER NOT NULL,
                    language TEXT NOT NULL,
                    code TEXT NOT NULL DEFAULT '',
                    updated_at REAL,
                    PRIMARY KEY (question_id, language)
                );

                CREATE TABLE IF NOT EXISTS progress (
                    question_id INTEGER PRIMARY KEY,
                    solves INTEGER NOT NULL DEFAULT 0,
                    method_id TEXT,
                    last_solved_at REAL
                );

                CREATE TABLE IF NOT EXISTS meta (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS stats (
                    key TEXT PRIMARY KEY,
                    value INTEGER NOT NULL DEFAULT 0
                );
                """
            )
            for key in ("reviews", "encodes", "retrieves"):
                conn.execute(
                    "INSERT OR IGNORE INTO stats(key, value) VALUES (?, 0)", (key,)
                )

    def _migrate_legacy_json(self) -> None:
        """One-time import from old user_memory.json / user_notes.json if present."""
        root = os.path.dirname(os.path.abspath(__file__))
        flag = "legacy_migrated_v1"
        with self._lock, self._conn() as conn:
            row = conn.execute(
                "SELECT value FROM meta WHERE key = ?", (flag,)
            ).fetchone()
            if row:
                return

        mem_path = os.path.join(root, "user_memory.json")
        notes_path = os.path.join(root, "user_notes.json")
        try:
            if os.path.exists(mem_path):
                with open(mem_path, "r", encoding="utf-8") as fh:
                    mem = json.load(fh)
                for card in (mem.get("cards") or {}).values():
                    self._upsert_card_dict(card)
                for mid, elab in (mem.get("elaborations") or {}).items():
                    self.save_elaboration(mid, elab.get("text", ""))
                for key, val in (mem.get("stats") or {}).items():
                    self._bump_stat(key, int(val), absolute=True)
            if os.path.exists(notes_path):
                with open(notes_path, "r", encoding="utf-8") as fh:
                    notes = json.load(fh)
                for qid, pad in (notes.get("notepads") or {}).items():
                    self.save_notepad(int(qid), pad.get("content", ""))
                for note in notes.get("notes") or []:
                    self.add_notes([note], dedupe=True)
                for qid, prog in (notes.get("progress") or {}).items():
                    self.mark_solved(
                        int(qid),
                        method_id=prog.get("method_id"),
                        set_solves=int(prog.get("solves", 1)),
                    )
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            pass

        with self._lock, self._conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO meta(key, value) VALUES (?, ?)",
                (flag, "1"),
            )

    # --- cards / SM-2 ---

    def _card_from_row(self, row: sqlite3.Row) -> Dict:
        return {
            "id": row["id"],
            "kind": row["kind"],
            "ref_id": row["ref_id"],
            "ease": row["ease"],
            "interval_days": row["interval_days"],
            "repetitions": row["repetitions"],
            "lapses": row["lapses"],
            "due_at": row["due_at"],
            "stability": row["stability"],
            "seen_encode": bool(row["seen_encode"]),
            "last_quality": row["last_quality"],
            "last_review_at": row["last_review_at"],
            "created_at": row["created_at"],
        }

    def _upsert_card_dict(self, card: Dict) -> None:
        with self._lock, self._conn() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO cards(
                    id, kind, ref_id, ease, interval_days, repetitions, lapses,
                    due_at, stability, seen_encode, last_quality, last_review_at, created_at
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    card["id"],
                    card["kind"],
                    str(card["ref_id"]),
                    float(card.get("ease", 2.5)),
                    float(card.get("interval_days", 0)),
                    int(card.get("repetitions", 0)),
                    int(card.get("lapses", 0)),
                    float(card.get("due_at", 0)),
                    float(card.get("stability", 0)),
                    1 if card.get("seen_encode") else 0,
                    card.get("last_quality"),
                    card.get("last_review_at"),
                    float(card.get("created_at", _now())),
                ),
            )

    def ensure_card(self, kind: str, ref_id: str) -> Dict:
        card_id = f"{kind}:{ref_id}"
        with self._lock, self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM cards WHERE id = ?", (card_id,)
            ).fetchone()
            if row:
                return self._card_from_row(row)
            now = _now()
            conn.execute(
                """
                INSERT INTO cards(
                    id, kind, ref_id, ease, interval_days, repetitions, lapses,
                    due_at, stability, seen_encode, last_quality, last_review_at, created_at
                ) VALUES (?,?,?,?,0,0,0,0,0,0,NULL,NULL,?)
                """,
                (card_id, kind, str(ref_id), 2.5, now),
            )
            row = conn.execute(
                "SELECT * FROM cards WHERE id = ?", (card_id,)
            ).fetchone()
            return self._card_from_row(row)

    def get_card(self, kind: str, ref_id: str) -> Dict:
        return self.ensure_card(kind, ref_id)

    def _bump_stat(self, key: str, amount: int = 1, absolute: bool = False) -> None:
        with self._lock, self._conn() as conn:
            if absolute:
                conn.execute(
                    "INSERT OR REPLACE INTO stats(key, value) VALUES (?, ?)",
                    (key, amount),
                )
            else:
                conn.execute(
                    "INSERT OR IGNORE INTO stats(key, value) VALUES (?, 0)", (key,)
                )
                conn.execute(
                    "UPDATE stats SET value = value + ? WHERE key = ?",
                    (amount, key),
                )

    def mark_encoded(self, kind: str, ref_id: str) -> Dict:
        card = self.ensure_card(kind, ref_id)
        card["seen_encode"] = True
        self._upsert_card_dict(card)
        self._bump_stat("encodes")
        return self.get_card(kind, ref_id)

    def review(self, kind: str, ref_id: str, rating: str) -> Dict:
        q = QUALITY.get(rating)
        if q is None:
            raise ValueError(f"Invalid rating '{rating}'")
        card = self.ensure_card(kind, ref_id)
        card = self._sm2(card, q)
        card["last_quality"] = rating
        card["last_review_at"] = _now()
        card["seen_encode"] = True
        self._upsert_card_dict(card)
        self._bump_stat("reviews")
        if rating in ("good", "easy", "hard"):
            self._bump_stat("retrieves")
        return self.get_card(kind, ref_id)

    def _sm2(self, card: Dict, q: int) -> Dict:
        ease = float(card.get("ease", 2.5))
        reps = int(card.get("repetitions", 0))
        interval = float(card.get("interval_days", 0))
        lapses = int(card.get("lapses", 0))
        ease = max(1.3, ease + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))
        if q < 3:
            if q == 1:
                lapses += 1
                reps = 0
                interval = 0.01
            else:
                interval = max(0.5, interval * 1.2)
                reps = max(1, reps)
        else:
            if reps == 0:
                interval = 1.0
            elif reps == 1:
                interval = 3.0 if q >= 4 else 2.0
            else:
                interval = max(1.0, interval * ease)
                if q >= 4:
                    interval *= 1.15
            reps += 1
        stability = 1.0 / (1.0 + math.exp(-(reps - lapses - 1.5)))
        card.update(
            {
                "ease": round(ease, 3),
                "interval_days": round(interval, 4),
                "repetitions": reps,
                "lapses": lapses,
                "due_at": _now() + interval * 86400.0,
                "stability": round(stability, 3),
            }
        )
        return card

    def save_elaboration(self, method_id: str, text: str) -> Dict:
        key = str(method_id)
        now = _now()
        cleaned = (text or "").strip()
        with self._lock, self._conn() as conn:
            row = conn.execute(
                "SELECT history_json FROM elaborations WHERE method_id = ?", (key,)
            ).fetchone()
            history = []
            if row:
                try:
                    history = json.loads(row["history_json"] or "[]")
                except json.JSONDecodeError:
                    history = []
            if cleaned:
                history.append({"text": cleaned, "at": now})
            history = history[-20:]
            conn.execute(
                """
                INSERT OR REPLACE INTO elaborations(method_id, text, updated_at, history_json)
                VALUES (?, ?, ?, ?)
                """,
                (key, cleaned, now, json.dumps(history)),
            )
        return self.get_elaboration(method_id)

    def get_elaboration(self, method_id: str) -> Dict:
        with self._lock, self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM elaborations WHERE method_id = ?",
                (str(method_id),),
            ).fetchone()
        if not row:
            return {"text": "", "updated_at": None, "history": []}
        try:
            history = json.loads(row["history_json"] or "[]")
        except json.JSONDecodeError:
            history = []
        return {
            "text": row["text"] or "",
            "updated_at": row["updated_at"],
            "history": history,
        }

    def mastery_summary(self) -> Dict:
        from skills import METHODS

        with self._lock, self._conn() as conn:
            stats = {
                r["key"]: r["value"]
                for r in conn.execute("SELECT key, value FROM stats")
            }
            method_rows = conn.execute(
                "SELECT * FROM cards WHERE kind = 'method'"
            ).fetchall()
            problem_count = conn.execute(
                "SELECT COUNT(*) AS c FROM cards WHERE kind = 'problem'"
            ).fetchone()["c"]
            now = _now()
            due_count = conn.execute(
                "SELECT COUNT(*) AS c FROM cards WHERE due_at <= ?", (now,)
            ).fetchone()["c"]

        learned = [r for r in method_rows if r["repetitions"] > 0]
        fluent = [r for r in method_rows if r["stability"] >= 0.7]
        return {
            "stats": {
                "reviews": int(stats.get("reviews", 0)),
                "encodes": int(stats.get("encodes", 0)),
                "retrieves": int(stats.get("retrieves", 0)),
            },
            "method_cards": len(method_rows),
            "problem_cards": int(problem_count),
            "due_count": int(due_count),
            "methods_touched": len(learned),
            "methods_fluent": len(fluent),
            "total_methods": len(METHODS),
            "curriculum_coverage": round(len(learned) / max(1, len(METHODS)), 3),
        }

    def method_states(self) -> Dict[str, Dict]:
        from skills import METHODS

        states = {}
        now = _now()
        for mid in METHODS:
            card = self.get_card("method", mid)
            states[mid] = {
                "stability": card.get("stability", 0),
                "repetitions": card.get("repetitions", 0),
                "due": float(card.get("due_at", 0)) <= now,
                "interval_days": card.get("interval_days", 0),
                "seen_encode": card.get("seen_encode", False),
                "last_quality": card.get("last_quality"),
            }
        return states

    # --- notes / notepad ---

    def get_notepad(self, question_id: int) -> Dict:
        with self._lock, self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM notepads WHERE question_id = ?", (question_id,)
            ).fetchone()
        if not row:
            return {"question_id": question_id, "content": "", "updated_at": None}
        return {
            "question_id": question_id,
            "content": row["content"] or "",
            "updated_at": row["updated_at"],
        }

    def save_notepad(self, question_id: int, content: str) -> Dict:
        now = _now()
        with self._lock, self._conn() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO notepads(question_id, content, updated_at)
                VALUES (?, ?, ?)
                """,
                (question_id, content or "", now),
            )
        return self.get_notepad(question_id)

    def add_notes(self, notes: List[Dict], *, dedupe: bool = True) -> List[Dict]:
        if not notes:
            return []
        added = []
        with self._lock, self._conn() as conn:
            for note in notes:
                text = (note.get("text") or "").strip()
                if not text:
                    continue
                qid = note.get("question_id")
                if dedupe:
                    existing = conn.execute(
                        """
                        SELECT id FROM notes
                        WHERE question_id IS ?
                          AND lower(text) = lower(?)
                        """,
                        (qid, text),
                    ).fetchone()
                    if existing:
                        continue
                entry_id = note.get("id") or str(uuid.uuid4())
                created = float(note.get("created_at", _now()))
                conn.execute(
                    """
                    INSERT OR REPLACE INTO notes(
                        id, text, kind, question_id, method_id, language, source, created_at
                    ) VALUES (?,?,?,?,?,?,?,?)
                    """,
                    (
                        entry_id,
                        text,
                        note.get("kind", "technique"),
                        qid,
                        note.get("method_id"),
                        note.get("language", "python"),
                        note.get("source", "comment"),
                        created,
                    ),
                )
                added.append(
                    {
                        "id": entry_id,
                        "text": text,
                        "kind": note.get("kind", "technique"),
                        "question_id": qid,
                        "method_id": note.get("method_id"),
                        "language": note.get("language", "python"),
                        "source": note.get("source", "comment"),
                        "created_at": created,
                    }
                )
        return added

    def list_notes(
        self,
        *,
        question_id: Optional[int] = None,
        method_id: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Dict]:
        sql = "SELECT * FROM notes WHERE 1=1"
        params: List = []
        if question_id is not None:
            sql += " AND question_id = ?"
            params.append(question_id)
        if method_id is not None:
            sql += " AND method_id = ?"
            params.append(method_id)
        sql += " ORDER BY created_at DESC"
        if limit is not None:
            sql += " LIMIT ?"
            params.append(int(limit))
        with self._lock, self._conn() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [
            {
                "id": r["id"],
                "text": r["text"],
                "kind": r["kind"],
                "question_id": r["question_id"],
                "method_id": r["method_id"],
                "language": r["language"],
                "source": r["source"],
                "created_at": r["created_at"],
            }
            for r in rows
        ]

    def delete_note(self, note_id: str) -> bool:
        with self._lock, self._conn() as conn:
            cur = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            return cur.rowcount > 0

    def harvest_from_code(
        self,
        code: str,
        *,
        question_id: int,
        method_id: Optional[str] = None,
        language: str = "python",
    ) -> List[Dict]:
        from notes import CommentExtractor

        notes = CommentExtractor().extract(
            code,
            question_id=question_id,
            method_id=method_id,
            language=language,
        )
        return self.add_notes(notes)

    def mark_solved(
        self,
        question_id: int,
        method_id: Optional[str] = None,
        set_solves: Optional[int] = None,
    ) -> Dict:
        now = _now()
        with self._lock, self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM progress WHERE question_id = ?", (question_id,)
            ).fetchone()
            solves = (
                int(set_solves)
                if set_solves is not None
                else int(row["solves"] if row else 0) + 1
            )
            conn.execute(
                """
                INSERT OR REPLACE INTO progress(question_id, solves, method_id, last_solved_at)
                VALUES (?, ?, ?, ?)
                """,
                (question_id, solves, method_id or (row["method_id"] if row else None), now),
            )
        return {
            "solves": solves,
            "method_id": method_id,
            "last_solved_at": now,
        }

    def get_progress(self) -> Dict:
        with self._lock, self._conn() as conn:
            rows = conn.execute("SELECT * FROM progress").fetchall()
        by_q = {
            str(r["question_id"]): {
                "solves": r["solves"],
                "method_id": r["method_id"],
                "last_solved_at": r["last_solved_at"],
            }
            for r in rows
        }
        return {
            "by_question": by_q,
            "solved_count": sum(1 for v in by_q.values() if int(v.get("solves", 0)) > 0),
        }

    # --- code drafts (server-side; replaces localStorage) ---

    def get_draft(self, question_id: int, language: str) -> Dict:
        with self._lock, self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM drafts WHERE question_id = ? AND language = ?",
                (question_id, language),
            ).fetchone()
        if not row:
            return {
                "question_id": question_id,
                "language": language,
                "code": "",
                "updated_at": None,
            }
        return {
            "question_id": question_id,
            "language": language,
            "code": row["code"] or "",
            "updated_at": row["updated_at"],
        }

    def save_draft(self, question_id: int, language: str, code: str) -> Dict:
        now = _now()
        with self._lock, self._conn() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO drafts(question_id, language, code, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (question_id, language, code or "", now),
            )
        return self.get_draft(question_id, language)


# Singleton used by the app
user_store = UserStore()
