"""Tests for spaced-repetition memory engine and session builder."""

import os
import tempfile
import time

from memory import (
    MemoryStore,
    PATTERN_CARDS,
    build_session,
    get_pattern_card,
    session_step_payload,
)
from questions import get_all_questions
from skills import METHODS


class TestMemoryStore:
    def setup_method(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp.close()
        self.store = MemoryStore(self.tmp.name)

    def teardown_method(self):
        for path in (self.tmp.name, self.tmp.name + ".tmp"):
            if os.path.exists(path):
                os.unlink(path)

    def test_new_card_due_immediately(self):
        card = self.store.get_card("method", "hash_map")
        assert card["repetitions"] == 0
        assert card["due_at"] == 0

    def test_sm2_good_increases_interval(self):
        c1 = self.store.review("method", "hash_map", "good")
        assert c1["repetitions"] == 1
        assert c1["interval_days"] >= 1
        assert c1["due_at"] > time.time()
        c2 = self.store.review("method", "hash_map", "easy")
        assert c2["repetitions"] == 2
        assert c2["interval_days"] >= c1["interval_days"]

    def test_again_resets_reps(self):
        self.store.review("method", "two_pointers", "good")
        self.store.review("method", "two_pointers", "good")
        failed = self.store.review("method", "two_pointers", "again")
        assert failed["repetitions"] == 0
        assert failed["lapses"] >= 1
        assert failed["interval_days"] < 1

    def test_elaboration_roundtrip(self):
        self.store.save_elaboration(
            "hash_map", "Store value→index; look up complement first"
        )
        entry = self.store.get_elaboration("hash_map")
        assert "complement" in entry["text"]
        assert entry["history"]

    def test_mastery_summary(self):
        self.store.review("method", "hash_map", "good")
        summary = self.store.mastery_summary()
        assert summary["total_methods"] == len(METHODS)
        assert summary["methods_touched"] >= 1
        assert summary["stats"]["reviews"] >= 1


class TestPatternCards:
    def test_every_method_has_card(self):
        for mid in METHODS:
            card = get_pattern_card(mid)
            assert card is not None
            assert card["retrieve_prompt"]
            assert card["retrieve_answer"]
            assert card["schema"]

    def test_pattern_cards_cover_core(self):
        for mid in ("hash_map", "two_pointers", "sliding_window", "dp_1d"):
            assert mid in PATTERN_CARDS


class TestSessionBuilder:
    def setup_method(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp.close()
        self.store = MemoryStore(self.tmp.name)
        self.questions = get_all_questions()

    def teardown_method(self):
        for path in (self.tmp.name, self.tmp.name + ".tmp"):
            if os.path.exists(path):
                os.unlink(path)

    def test_build_session_interleaves(self):
        session = build_session(self.questions, store=self.store, limit=6)
        assert session["step_count"] == 6
        assert session["science"]["retrieval"]
        skills = [s["skill_id"] for s in session["steps"]]
        # With a fresh store, encode roles dominate; skills should vary
        assert len(set(skills)) >= 2
        for step in session["steps"]:
            assert step["card"]["method"]["id"] == step["ref_id"]
            assert "encode" in step["phases"]

    def test_session_step_payload(self):
        payload = session_step_payload("hash_map", self.questions)
        assert payload["pattern"]["method"]["id"] == "hash_map"
        assert payload["related_problems"]
        assert payload["parents"]
