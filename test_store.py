"""Tests for unified SQLite store."""

import os
import tempfile

from store import UserStore


class TestUserStore:
    def setup_method(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.tmp.close()
        self.store = UserStore(self.tmp.name)

    def teardown_method(self):
        for path in (self.tmp.name, self.tmp.name + "-journal", self.tmp.name + "-wal"):
            if os.path.exists(path):
                os.unlink(path)

    def test_draft_and_notepad(self):
        self.store.save_draft(1, "python", "print(1)")
        assert self.store.get_draft(1, "python")["code"] == "print(1)"
        self.store.save_notepad(1, "use a map")
        assert "map" in self.store.get_notepad(1)["content"]

    def test_review_persists(self):
        card = self.store.review("method", "hash_map", "good")
        assert card["repetitions"] == 1
        again = UserStore(self.tmp.name).get_card("method", "hash_map")
        assert again["repetitions"] == 1

    def test_notes_dedupe(self):
        n1 = self.store.add_notes(
            [{"text": "Store complement for O(1) lookup path", "question_id": 1}]
        )
        n2 = self.store.add_notes(
            [{"text": "Store complement for O(1) lookup path", "question_id": 1}]
        )
        assert len(n1) == 1
        assert n2 == []
