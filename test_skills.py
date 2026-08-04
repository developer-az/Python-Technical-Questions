"""Tests for skill/method taxonomy and aggregation."""

from skills import (
    METHODS,
    PILLARS,
    QUESTION_METHODS,
    SKILLS,
    annotate_question,
    get_method_detail,
    get_methods_for_question,
    get_primary_method_id,
    get_questions_for_method,
    get_skill_detail,
    get_skill_tree,
    starter_template,
)
from questions import get_all_questions


class TestTaxonomyIntegrity:
    def test_all_question_methods_exist(self):
        for qid, mids in QUESTION_METHODS.items():
            assert mids, f"Question {qid} has no methods"
            for mid in mids:
                assert mid in METHODS, f"Unknown method {mid} on question {qid}"

    def test_skill_methods_exist(self):
        for skill in SKILLS.values():
            assert skill["pillar_id"] in PILLARS
            for mid in skill["method_ids"]:
                assert mid in METHODS

    def test_method_parents_exist(self):
        for method in METHODS.values():
            for sid in method["parent_skill_ids"]:
                assert sid in SKILLS

    def test_every_question_mapped(self):
        questions = get_all_questions()
        for q in questions:
            assert q["id"] in QUESTION_METHODS


class TestAggregation:
    def setup_method(self):
        self.questions = get_all_questions()

    def test_skill_tree_counts(self):
        tree = get_skill_tree(self.questions)
        assert tree["pillar_count"] == len(PILLARS)
        assert tree["method_count"] == len(METHODS)
        assert tree["skill_count"] == len(SKILLS)
        assert len(tree["pillars"]) == len(PILLARS)
        # Two Sum should appear under hash_map somewhere
        found = False
        for pillar in tree["pillars"]:
            for skill in pillar["skills"]:
                for method in skill["methods"]:
                    if method["id"] == "hash_map":
                        ids = [q["id"] for q in method["questions"]]
                        assert 1 in ids
                        found = True
        assert found

    def test_method_detail_drill_up(self):
        detail = get_method_detail("hash_map", self.questions)
        assert detail is not None
        assert detail["method"]["name"] == "Hash Map Lookup"
        assert detail["question_count"] >= 1
        assert detail["parents"]
        assert detail["parents"][0]["pillar"]["id"] in PILLARS
        assert detail["parents"][0]["skill"]["id"] in SKILLS

    def test_skill_detail_aggregates_methods(self):
        detail = get_skill_detail("array_patterns", self.questions)
        assert detail is not None
        assert detail["pillar"]["id"] == "fundamentals"
        assert detail["question_count"] >= 1
        assert len(detail["methods"]) >= 1

    def test_annotate_question(self):
        q = next(x for x in self.questions if x["id"] == 1)
        annotated = annotate_question(q)
        assert annotated["primary_method"]["id"] == "hash_map"
        assert annotated["methods"][0]["primary"] is True

    def test_get_questions_for_method(self):
        qs = get_questions_for_method("sliding_window", self.questions)
        assert any(q["id"] == 11 for q in qs)

    def test_primary_method(self):
        assert get_primary_method_id(11) == "sliding_window"
        methods = get_methods_for_question(11)
        assert methods[0]["id"] == "sliding_window"

    def test_starter_templates(self):
        q = next(x for x in self.questions if x["id"] == 1)
        py = starter_template("python", q)
        assert "Two Sum" in py
        assert "Hash Map" in py
        assert py.strip().startswith("#")
        js = starter_template("javascript", q)
        assert "function solve" in js
        java = starter_template("java", q)
        assert "class Solution" in java
        cpp = starter_template("cpp", q)
        assert "#include" in cpp
