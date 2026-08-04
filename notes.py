"""Notes system: extract technique notes from code comments + notepad store.

Comments written in the practice IDE become durable study notes tagged by
question and method — so form cues survive beyond a single session.
"""

from __future__ import annotations

import json
import os
import re
import threading
import time
import uuid
from typing import Dict, List, Optional

DEFAULT_STORE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "user_notes.json"
)

# Capture line comments and simple block comments.
_LINE_COMMENT_RE = re.compile(
    r"(?P<prefix>^[ \t]*)(?P<marker>#|//+)[ \t]?(?P<body>.*)$"
)
_BLOCK_COMMENT_RE = re.compile(r"/\*(.*?)\*/", re.DOTALL)

# Skip boilerplate / noise comments
_NOISE_PREFIXES = (
    "todo",
    "fix",
    "hack",
    "xxx",
    "---",
    "===",
    "include ",
    "coding:",
    "!/usr/bin",
    "pragma",
)

_META_PREFIXES = (
    "method:",
    "form cue:",
    "time complexity",
    "space complexity",
)


class CommentExtractor:
    """Pull concrete technique notes out of source comments."""

    def extract(
        self,
        code: str,
        *,
        question_id: Optional[int] = None,
        method_id: Optional[str] = None,
        language: str = "python",
    ) -> List[Dict]:
        if not code or not code.strip():
            return []

        notes: List[Dict] = []
        seen = set()

        for raw in self._iter_comment_bodies(code):
            cleaned = self._clean_body(raw)
            if not cleaned:
                continue
            key = cleaned.lower()
            if key in seen:
                continue
            seen.add(key)

            inferred_method = method_id
            note_kind = "technique"
            lower = cleaned.lower()

            if lower.startswith("method:"):
                note_kind = "method_tag"
                cleaned = cleaned.split(":", 1)[1].strip() or cleaned
            elif lower.startswith("form cue:"):
                note_kind = "form_cue"
                cleaned = cleaned.split(":", 1)[1].strip() or cleaned

            notes.append(
                {
                    "id": str(uuid.uuid4()),
                    "text": cleaned,
                    "kind": note_kind,
                    "question_id": question_id,
                    "method_id": inferred_method,
                    "language": language,
                    "source": "comment",
                    "created_at": time.time(),
                }
            )

        return notes

    def _iter_comment_bodies(self, code: str) -> List[str]:
        bodies: List[str] = []

        # Strip block comments first so their interiors are collected
        def _block_repl(match: re.Match) -> str:
            inner = match.group(1)
            for line in inner.splitlines():
                bodies.append(line.strip(" *\t"))
            return ""

        without_blocks = _BLOCK_COMMENT_RE.sub(_block_repl, code)

        for line in without_blocks.splitlines():
            # Ignore hash inside strings roughly by requiring comment-like start
            stripped = line.lstrip()
            if stripped.startswith("#") or stripped.startswith("//"):
                match = _LINE_COMMENT_RE.match(line)
                if match:
                    bodies.append(match.group("body").strip())

        return bodies

    def _clean_body(self, body: str) -> Optional[str]:
        text = body.strip()
        if not text:
            return None

        # Drop shebang / separators / pure punctuation
        if len(text) < 8:
            return None
        lower = text.lower()
        for noise in _NOISE_PREFIXES:
            if lower.startswith(noise):
                return None

        # Keep method/form cue lines even if short-ish after strip
        for meta in _META_PREFIXES:
            if lower.startswith(meta):
                return text

        # Prefer sentences that look like technique notes
        technique_signals = (
            "store",
            "track",
            "invariant",
            "pointer",
            "window",
            "hash",
            "map",
            "base case",
            "recurrence",
            "dp[",
            "queue",
            "stack",
            "because",
            "so that",
            "instead of",
            "o(",
            "look up",
            "lookup",
            "expand",
            "contract",
            "shrink",
            "prev",
            "curr",
            "dummy",
            "bound",
            "subtree",
            "level",
        )
        if any(sig in lower for sig in technique_signals):
            return text

        # Also keep imperative teaching comments of decent length
        if len(text) >= 24 and not text.endswith(")"):
            # Skip obvious code leftovers that leaked
            if ("=" in text and "(" in text) or text.startswith("return "):
                return None
            return text

        return None


class NotesStore:
    """JSON-backed notepad + harvested comment notes (thread-safe enough for Flask)."""

    def __init__(self, path: str = DEFAULT_STORE_PATH):
        self.path = path
        self._lock = threading.Lock()
        self._data = {"notepads": {}, "notes": [], "progress": {}}
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.path):
            return
        try:
            with open(self.path, "r", encoding="utf-8") as fh:
                loaded = json.load(fh)
            if isinstance(loaded, dict):
                self._data["notepads"] = loaded.get("notepads", {})
                self._data["notes"] = loaded.get("notes", [])
                self._data["progress"] = loaded.get("progress", {})
        except (json.JSONDecodeError, OSError):
            # Keep empty store if corrupt; caller can still write fresh data
            pass

    def _save(self) -> None:
        directory = os.path.dirname(self.path) or "."
        os.makedirs(directory, exist_ok=True)
        tmp = f"{self.path}.tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(self._data, fh, indent=2)
        os.replace(tmp, self.path)

    # --- Notepad (freeform scratch pad per question) ---

    def get_notepad(self, question_id: int) -> Dict:
        key = str(question_id)
        with self._lock:
            pad = self._data["notepads"].get(key)
            if not pad:
                return {
                    "question_id": question_id,
                    "content": "",
                    "updated_at": None,
                }
            return {
                "question_id": question_id,
                "content": pad.get("content", ""),
                "updated_at": pad.get("updated_at"),
            }

    def save_notepad(self, question_id: int, content: str) -> Dict:
        key = str(question_id)
        now = time.time()
        with self._lock:
            self._data["notepads"][key] = {
                "content": content or "",
                "updated_at": now,
            }
            self._save()
        return self.get_notepad(question_id)

    # --- Harvested technique notes ---

    def add_notes(self, notes: List[Dict], *, dedupe: bool = True) -> List[Dict]:
        if not notes:
            return []
        added = []
        with self._lock:
            existing_texts = {
                (n.get("question_id"), n.get("text", "").strip().lower())
                for n in self._data["notes"]
            }
            for note in notes:
                text = (note.get("text") or "").strip()
                if not text:
                    continue
                key = (note.get("question_id"), text.lower())
                if dedupe and key in existing_texts:
                    continue
                entry = {
                    "id": note.get("id") or str(uuid.uuid4()),
                    "text": text,
                    "kind": note.get("kind", "technique"),
                    "question_id": note.get("question_id"),
                    "method_id": note.get("method_id"),
                    "language": note.get("language", "python"),
                    "source": note.get("source", "comment"),
                    "created_at": note.get("created_at", time.time()),
                }
                self._data["notes"].append(entry)
                existing_texts.add(key)
                added.append(entry)
            if added:
                self._save()
        return added

    def list_notes(
        self,
        *,
        question_id: Optional[int] = None,
        method_id: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Dict]:
        with self._lock:
            notes = list(self._data["notes"])
        if question_id is not None:
            notes = [n for n in notes if n.get("question_id") == question_id]
        if method_id is not None:
            notes = [n for n in notes if n.get("method_id") == method_id]
        notes.sort(key=lambda n: n.get("created_at", 0), reverse=True)
        if limit is not None:
            notes = notes[:limit]
        return notes

    def delete_note(self, note_id: str) -> bool:
        with self._lock:
            before = len(self._data["notes"])
            self._data["notes"] = [
                n for n in self._data["notes"] if n.get("id") != note_id
            ]
            if len(self._data["notes"]) == before:
                return False
            self._save()
            return True

    def harvest_from_code(
        self,
        code: str,
        *,
        question_id: int,
        method_id: Optional[str] = None,
        language: str = "python",
    ) -> List[Dict]:
        extractor = CommentExtractor()
        notes = extractor.extract(
            code,
            question_id=question_id,
            method_id=method_id,
            language=language,
        )
        return self.add_notes(notes)

    # --- Lightweight progress (solved reps per question / method) ---

    def mark_solved(self, question_id: int, method_id: Optional[str] = None) -> Dict:
        key = str(question_id)
        now = time.time()
        with self._lock:
            entry = self._data["progress"].get(key, {"solves": 0})
            entry["solves"] = int(entry.get("solves", 0)) + 1
            entry["last_solved_at"] = now
            if method_id:
                entry["method_id"] = method_id
            self._data["progress"][key] = entry
            self._save()
            return dict(entry)

    def get_progress(self) -> Dict:
        with self._lock:
            return {
                "by_question": dict(self._data["progress"]),
                "solved_count": sum(
                    1
                    for v in self._data["progress"].values()
                    if int(v.get("solves", 0)) > 0
                ),
            }


# Module-level store for the web app
notes_store = NotesStore()
