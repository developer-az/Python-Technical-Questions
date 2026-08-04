"""Tests for comment harvesting and notepad persistence."""

import os
import tempfile

from notes import CommentExtractor, NotesStore


class TestCommentExtractor:
    def setup_method(self):
        self.extractor = CommentExtractor()

    def test_extracts_python_technique_comments(self):
        code = """
# Method: Hash Map Lookup
# Store the complement in the map before checking the next value
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        # Look up need in O(1) instead of nested loops
        need = target - num
        if need in seen:
            return [seen[need], i]
        seen[num] = i
"""
        notes = self.extractor.extract(code, question_id=1, method_id="hash_map")
        texts = " ".join(n["text"].lower() for n in notes)
        assert "complement" in texts or "look up" in texts
        assert any(n["kind"] == "method_tag" for n in notes)

    def test_extracts_js_comments(self):
        code = """
// Expand the window with the right pointer while chars stay unique
function lengthOfLongestSubstring(s) {
  // Contract from the left when a duplicate appears
  return 0;
}
"""
        notes = self.extractor.extract(
            code, question_id=11, method_id="sliding_window", language="javascript"
        )
        assert len(notes) >= 1
        assert any(
            "window" in n["text"].lower() or "contract" in n["text"].lower()
            for n in notes
        )

    def test_skips_noise(self):
        code = """
# TODO: implement
# ===
def foo():
    pass
"""
        notes = self.extractor.extract(code, question_id=1)
        assert notes == []


class TestNotesStore:
    def setup_method(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp.close()
        self.store = NotesStore(self.tmp.name)

    def teardown_method(self):
        for path in (self.tmp.name, self.tmp.name + ".tmp"):
            if os.path.exists(path):
                os.unlink(path)

    def test_notepad_roundtrip(self):
        self.store.save_notepad(1, "Track min price then update profit")
        pad = self.store.get_notepad(1)
        assert pad["content"] == "Track min price then update profit"
        assert pad["updated_at"] is not None

    def test_harvest_and_list(self):
        code = """
# Keep a running minimum price as the only history you need
def max_profit(prices):
    pass
"""
        added = self.store.harvest_from_code(
            code, question_id=2, method_id="greedy_scan"
        )
        assert len(added) >= 1
        notes = self.store.list_notes(question_id=2)
        assert len(notes) >= 1
        by_method = self.store.list_notes(method_id="greedy_scan")
        assert any(n["question_id"] == 2 for n in by_method)

    def test_dedupe_harvest(self):
        code = "# Store complement in the hash map for O(1) lookup later\nx = 1\n"
        first = self.store.harvest_from_code(code, question_id=1, method_id="hash_map")
        second = self.store.harvest_from_code(code, question_id=1, method_id="hash_map")
        assert len(first) >= 1
        assert second == []

    def test_delete_note(self):
        code = (
            "# Move the pointer that repairs the invariant when the sum is too large\n"
        )
        added = self.store.harvest_from_code(
            code, question_id=3, method_id="two_pointers"
        )
        assert added
        assert self.store.delete_note(added[0]["id"]) is True
        assert self.store.list_notes(question_id=3) == []

    def test_progress(self):
        self.store.mark_solved(1, method_id="hash_map")
        progress = self.store.get_progress()
        assert progress["solved_count"] == 1
        assert progress["by_question"]["1"]["solves"] == 1
