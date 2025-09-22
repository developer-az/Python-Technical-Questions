"""Game logic and flashcard functionality for LeetCode practice tool."""

import random
import json
import os
from datetime import datetime
from questions import (
    get_all_questions,
    get_questions_by_category,
    get_questions_by_difficulty,
    get_categories,
    get_difficulties,
)


class FlashcardGame:
    def __init__(self):
        self.current_question = None
        self.question_pool = []
        self.stats = self.load_stats()
        self.session_stats = {
            "questions_answered": 0,
            "correct_answers": 0,
            "start_time": datetime.now(),
        }

    def load_stats(self):
        """Load user statistics from file."""
        stats_file = "leetcode_stats.json"
        if os.path.exists(stats_file):
            try:
                with open(stats_file, "r") as f:
                    return json.load(f)
            except:
                return self.get_default_stats()
        return self.get_default_stats()

    def get_default_stats(self):
        """Get default statistics structure."""
        return {
            "total_questions": 0,
            "correct_answers": 0,
            "questions_by_category": {},
            "questions_by_difficulty": {},
            "last_session": None,
            "streak": 0,
        }

    def save_stats(self):
        """Save user statistics to file."""
        stats_file = "leetcode_stats.json"
        try:
            with open(stats_file, "w") as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save stats: {e}")

    def set_question_pool(self, category=None, difficulty=None):
        """Set the pool of questions to practice from."""
        if category and difficulty:
            # Get questions from specific category and difficulty
            from questions import QUESTIONS

            if category in QUESTIONS and difficulty in QUESTIONS[category]:
                self.question_pool = QUESTIONS[category][difficulty].copy()
            else:
                self.question_pool = []
        elif category:
            self.question_pool = get_questions_by_category(category)
        elif difficulty:
            self.question_pool = get_questions_by_difficulty(difficulty)
        else:
            self.question_pool = get_all_questions()

        # Shuffle the questions for variety
        random.shuffle(self.question_pool)
        return len(self.question_pool)

    def get_next_question(self):
        """Get the next question from the pool."""
        if not self.question_pool:
            return None

        # Remove and return a question from the pool
        self.current_question = self.question_pool.pop()
        return self.current_question

    def show_question(self):
        """Display the current question in flashcard format."""
        if not self.current_question:
            return "No question available"

        q = self.current_question
        output = []
        output.append("=" * 80)
        output.append(f"📚 QUESTION {q['id']}: {q['title']}")
        output.append(f"🏷️  Category: {q['category']} | Difficulty: {q['difficulty']}")
        output.append("=" * 80)
        output.append("")
        output.append(q["problem"])
        output.append("")
        output.append("=" * 80)
        return "\n".join(output)

    def show_hints(self):
        """Show hints for the current question."""
        if not self.current_question or "hints" not in self.current_question:
            return "No hints available for this question."

        output = []
        output.append("💡 HINTS:")
        output.append("-" * 40)
        for i, hint in enumerate(self.current_question["hints"], 1):
            output.append(f"{i}. {hint}")
        output.append("")
        return "\n".join(output)

    def show_solution(self):
        """Show the solution for the current question."""
        if not self.current_question:
            return "No solution available"

        output = []
        output.append("✅ SOLUTION:")
        output.append("-" * 40)
        output.append(self.current_question["solution"])
        output.append("")
        return "\n".join(output)

    def record_answer(self, is_correct):
        """Record whether the user got the answer correct."""
        if not self.current_question:
            return

        # Update session stats
        self.session_stats["questions_answered"] += 1
        if is_correct:
            self.session_stats["correct_answers"] += 1

        # Update overall stats
        self.stats["total_questions"] += 1
        if is_correct:
            self.stats["correct_answers"] += 1
            self.stats["streak"] += 1
        else:
            self.stats["streak"] = 0

        # Update category stats
        category = self.current_question["category"]
        if category not in self.stats["questions_by_category"]:
            self.stats["questions_by_category"][category] = {"total": 0, "correct": 0}
        self.stats["questions_by_category"][category]["total"] += 1
        if is_correct:
            self.stats["questions_by_category"][category]["correct"] += 1

        # Update difficulty stats
        difficulty = self.current_question["difficulty"]
        if difficulty not in self.stats["questions_by_difficulty"]:
            self.stats["questions_by_difficulty"][difficulty] = {
                "total": 0,
                "correct": 0,
            }
        self.stats["questions_by_difficulty"][difficulty]["total"] += 1
        if is_correct:
            self.stats["questions_by_difficulty"][difficulty]["correct"] += 1

        # Update last session
        self.stats["last_session"] = datetime.now().isoformat()

        # Save stats
        self.save_stats()

    def get_session_summary(self):
        """Get a summary of the current session."""
        if self.session_stats["questions_answered"] == 0:
            return "No questions answered in this session."

        accuracy = (
            self.session_stats["correct_answers"]
            / self.session_stats["questions_answered"]
        ) * 100
        duration = datetime.now() - self.session_stats["start_time"]

        output = []
        output.append("📊 SESSION SUMMARY")
        output.append("=" * 40)
        output.append(f"Questions Answered: {self.session_stats['questions_answered']}")
        output.append(f"Correct Answers: {self.session_stats['correct_answers']}")
        output.append(f"Accuracy: {accuracy:.1f}%")
        output.append(f"Duration: {str(duration).split('.')[0]}")
        output.append(f"Current Streak: {self.stats['streak']}")
        output.append("")
        return "\n".join(output)

    def get_overall_stats(self):
        """Get overall user statistics."""
        if self.stats["total_questions"] == 0:
            return "No questions answered yet. Start practicing to see your stats!"

        overall_accuracy = (
            self.stats["correct_answers"] / self.stats["total_questions"]
        ) * 100

        output = []
        output.append("📈 OVERALL STATISTICS")
        output.append("=" * 50)
        output.append(f"Total Questions: {self.stats['total_questions']}")
        output.append(f"Correct Answers: {self.stats['correct_answers']}")
        output.append(f"Overall Accuracy: {overall_accuracy:.1f}%")
        output.append(f"Current Streak: {self.stats['streak']}")
        output.append("")

        if self.stats["questions_by_category"]:
            output.append("📂 BY CATEGORY:")
            for category, stats in self.stats["questions_by_category"].items():
                if stats["total"] > 0:
                    acc = (stats["correct"] / stats["total"]) * 100
                    output.append(
                        f"  {category}: {stats['correct']}/{stats['total']} ({acc:.1f}%)"
                    )
            output.append("")

        if self.stats["questions_by_difficulty"]:
            output.append("⭐ BY DIFFICULTY:")
            for difficulty, stats in self.stats["questions_by_difficulty"].items():
                if stats["total"] > 0:
                    acc = (stats["correct"] / stats["total"]) * 100
                    output.append(
                        f"  {difficulty}: {stats['correct']}/{stats['total']} ({acc:.1f}%)"
                    )
        return "\n".join(output)

    def reset_stats(self):
        """Reset all user statistics."""
        self.stats = self.get_default_stats()
        self.session_stats = {
            "questions_answered": 0,
            "correct_answers": 0,
            "start_time": datetime.now(),
        }
        self.save_stats()
        return "Statistics have been reset!"

    def get_available_filters(self):
        """Get available categories and difficulties for filtering."""
        output = []
        output.append("🎯 AVAILABLE FILTERS:")
        output.append("-" * 30)
        output.append("Categories: " + ", ".join(get_categories()))
        output.append("Difficulties: " + ", ".join(get_difficulties()))
        output.append("")
        return "\n".join(output)
