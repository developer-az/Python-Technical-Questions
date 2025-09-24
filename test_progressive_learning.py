"""Tests for progressive learning functionality."""

import pytest
from code_sections import CodeSectionParser, MultipleChoiceGenerator
from game import FlashcardGame
from questions import get_all_questions


class TestCodeSectionParser:
    """Test code section parsing functionality."""

    def setup_method(self):
        self.parser = CodeSectionParser()
        self.questions = get_all_questions()

    def test_parse_solution_basic(self):
        """Test basic solution parsing."""
        # Get a simple question (Two Sum - ID 1)
        two_sum = next(q for q in self.questions if q["id"] == 1)

        parsed = self.parser.parse_solution(two_sum["solution"])

        assert "sections" in parsed
        assert "complexity_info" in parsed
        assert "total_sections" in parsed
        assert "complete_code" in parsed

        # Should have multiple sections
        assert len(parsed["sections"]) >= 2
        assert parsed["total_sections"] == len(parsed["sections"])

    def test_section_structure(self):
        """Test that each section has required fields."""
        question = self.questions[0]
        parsed = self.parser.parse_solution(question["solution"])

        for section in parsed["sections"]:
            assert "index" in section
            assert "type" in section
            assert "code" in section
            assert "lines" in section
            assert "description" in section
            assert "key_concepts" in section

            # Check types
            assert isinstance(section["index"], int)
            assert isinstance(section["type"], str)
            assert isinstance(section["code"], str)
            assert isinstance(section["lines"], list)
            assert isinstance(section["description"], str)
            assert isinstance(section["key_concepts"], list)

    def test_complexity_extraction(self):
        """Test that complexity information is extracted correctly."""
        question = self.questions[0]
        parsed = self.parser.parse_solution(question["solution"])

        complexity_info = parsed["complexity_info"]
        assert "Time Complexity" in complexity_info
        assert "Space Complexity" in complexity_info

    def test_function_detection(self):
        """Test that function definitions are detected correctly."""
        question = self.questions[0]
        parsed = self.parser.parse_solution(question["solution"])

        # First section should be function definition for most problems
        first_section = parsed["sections"][0]
        assert "def " in first_section["code"]
        assert first_section["type"] == "function_def"


class TestMultipleChoiceGenerator:
    """Test multiple choice generation functionality."""

    def setup_method(self):
        self.parser = CodeSectionParser()
        self.choice_generator = MultipleChoiceGenerator()
        self.questions = get_all_questions()

    def test_generate_choices_basic(self):
        """Test basic choice generation."""
        question = self.questions[0]
        parsed = self.parser.parse_solution(question["solution"])
        first_section = parsed["sections"][0]

        choices = self.choice_generator.generate_choices(
            first_section, parsed["sections"]
        )

        # Should have 4 choices (1 correct + 3 distractors)
        assert len(choices) == 4

        # Exactly one should be correct
        correct_choices = [c for c in choices if c["is_correct"]]
        assert len(correct_choices) == 1

        # All should have required fields
        for choice in choices:
            assert "text" in choice
            assert "is_correct" in choice
            assert "explanation" in choice
            assert isinstance(choice["is_correct"], bool)
            assert isinstance(choice["text"], str)
            assert isinstance(choice["explanation"], str)

    def test_correct_choice_content(self):
        """Test that the correct choice contains the right code."""
        question = self.questions[0]
        parsed = self.parser.parse_solution(question["solution"])
        first_section = parsed["sections"][0]

        choices = self.choice_generator.generate_choices(
            first_section, parsed["sections"]
        )
        correct_choice = next(c for c in choices if c["is_correct"])

        # The correct choice should contain the original section code
        assert correct_choice["text"] == first_section["code"]


class TestFlashcardGameProgressive:
    """Test progressive learning mode in FlashcardGame."""

    def setup_method(self):
        self.game = FlashcardGame()
        self.game.set_question_pool()  # Load all questions

    def test_enable_progressive_mode(self):
        """Test enabling progressive mode."""
        assert not self.game.progressive_mode

        self.game.enable_progressive_mode(True)
        assert self.game.progressive_mode

        self.game.enable_progressive_mode(False)
        assert not self.game.progressive_mode

    def test_start_progressive_question(self):
        """Test starting a progressive learning session."""
        self.game.enable_progressive_mode(True)
        question = self.game.get_next_question()

        progressive_data = self.game.start_progressive_question()

        assert progressive_data is not None
        assert "total_sections" in progressive_data
        assert "question" in progressive_data
        assert "first_section" in progressive_data

        assert progressive_data["total_sections"] > 0
        assert progressive_data["question"] == question

    def test_get_current_section_with_choices(self):
        """Test getting current section with multiple choices."""
        self.game.enable_progressive_mode(True)
        self.game.get_next_question()
        self.game.start_progressive_question()

        section_data = self.game.get_current_section_with_choices()

        assert section_data is not None
        assert "section_index" in section_data
        assert "total_sections" in section_data
        assert "section" in section_data
        assert "choices" in section_data
        assert "built_so_far" in section_data
        assert "progress_percentage" in section_data

        # Should have 4 choices
        assert len(section_data["choices"]) == 4

        # Progress should start at 0%
        assert section_data["progress_percentage"] == 0
        assert section_data["section_index"] == 0

    def test_submit_correct_choice(self):
        """Test submitting a correct choice."""
        self.game.enable_progressive_mode(True)
        self.game.get_next_question()
        self.game.start_progressive_question()

        section_data = self.game.get_current_section_with_choices()

        # Find the correct choice
        correct_index = None
        for i, choice in enumerate(section_data["choices"]):
            if choice["is_correct"]:
                correct_index = i
                break

        assert correct_index is not None

        result = self.game.submit_section_choice(correct_index)

        assert result["correct"] is True
        assert result["section_complete"] is True
        assert "feedback" in result

        # Should advance to next section (unless it was the last one)
        if result.get("question_complete"):
            assert "complete_solution" in result
        else:
            assert "next_section" in result

    def test_submit_incorrect_choice(self):
        """Test submitting an incorrect choice."""
        self.game.enable_progressive_mode(True)
        self.game.get_next_question()
        self.game.start_progressive_question()

        section_data = self.game.get_current_section_with_choices()

        # Find an incorrect choice
        incorrect_index = None
        for i, choice in enumerate(section_data["choices"]):
            if not choice["is_correct"]:
                incorrect_index = i
                break

        assert incorrect_index is not None

        result = self.game.submit_section_choice(incorrect_index)

        assert result["correct"] is False
        assert result["section_complete"] is False
        assert result["question_complete"] is False
        assert "feedback" in result
        assert "retry_section" in result

    def test_progressive_session_reset(self):
        """Test resetting progressive session."""
        self.game.enable_progressive_mode(True)
        self.game.get_next_question()
        self.game.start_progressive_question()

        # Verify session is active
        assert len(self.game.current_sections) > 0
        assert len(self.game.built_solution) == 0

        # Reset
        self.game.reset_progressive_session()

        # Verify reset
        assert len(self.game.current_sections) == 0
        assert len(self.game.built_solution) == 0
        assert self.game.current_section_index == 0

    def test_get_progressive_progress(self):
        """Test getting progressive progress."""
        self.game.enable_progressive_mode(True)
        self.game.get_next_question()
        self.game.start_progressive_question()

        progress = self.game.get_progressive_progress()

        assert progress is not None
        assert "current_section" in progress
        assert "total_sections" in progress
        assert "progress_percentage" in progress
        assert "sections_completed" in progress
        assert "built_solution" in progress

        # Initial progress should be 0
        assert progress["current_section"] == 0
        assert progress["sections_completed"] == 0
        assert progress["progress_percentage"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
