"""Comment extraction + notepad adapter over the unified SQLite store."""

from __future__ import annotations

import re
import time
import uuid
from typing import Dict, List, Optional

_LINE_COMMENT_RE = re.compile(
    r"(?P<prefix>^[ \t]*)(?P<marker>#|//+)[ \t]?(?P<body>.*)$"
)
_BLOCK_COMMENT_RE = re.compile(r"/\*(.*?)\*/", re.DOTALL)

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

        def _block_repl(match: re.Match) -> str:
            inner = match.group(1)
            for line in inner.splitlines():
                bodies.append(line.strip(" *\t"))
            return ""

        without_blocks = _BLOCK_COMMENT_RE.sub(_block_repl, code)

        for line in without_blocks.splitlines():
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
        if len(text) < 8:
            return None
        lower = text.lower()
        for noise in _NOISE_PREFIXES:
            if lower.startswith(noise):
                return None
        for meta in _META_PREFIXES:
            if lower.startswith(meta):
                return text
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
        if len(text) >= 24 and not text.endswith(")"):
            if ("=" in text and "(" in text) or text.startswith("return "):
                return None
            return text
        return None


class NotesStore:
    """Adapter over UserStore for notepad + harvested notes + progress."""

    def __init__(self, path: str = None):
        if path:
            from store import UserStore

            self._store = UserStore(path)
        else:
            from store import user_store

            self._store = user_store

    def get_notepad(self, question_id: int):
        return self._store.get_notepad(question_id)

    def save_notepad(self, question_id: int, content: str):
        return self._store.save_notepad(question_id, content)

    def add_notes(self, notes, *, dedupe: bool = True):
        return self._store.add_notes(notes, dedupe=dedupe)

    def list_notes(self, *, question_id=None, method_id=None, limit=None):
        return self._store.list_notes(
            question_id=question_id, method_id=method_id, limit=limit
        )

    def delete_note(self, note_id: str) -> bool:
        return self._store.delete_note(note_id)

    def harvest_from_code(self, code, *, question_id, method_id=None, language="python"):
        return self._store.harvest_from_code(
            code, question_id=question_id, method_id=method_id, language=language
        )

    def mark_solved(self, question_id: int, method_id=None):
        return self._store.mark_solved(question_id, method_id=method_id)

    def get_progress(self):
        return self._store.get_progress()


notes_store = NotesStore()
