#!/usr/bin/env python3
"""LeetCode Practice Tool - Flashcard Style Game
A full-fledged practice tool for common LeetCode questions in a flashcard-like game format."""

import sys
import os
from game import FlashcardGame
from questions import get_categories, get_difficulties


class LeetCodePracticeTool:
    def __init__(self):
        self.game = FlashcardGame()
        self.current_mode = "menu"

    def display_welcome(self):
        """Display welcome message and main menu."""
        print("\n" + "="*60)
        print("🚀 LEETCODE PRACTICE TOOL - FLASHCARD GAME")
        print("="*60)
        print("Welcome to your personal LeetCode practice companion!")
        print("Practice coding problems in a fun, flashcard-style format.")
        print("="*60)

    def display_main_menu(self):
        """Display the main menu options."""
        print("\n📋 MAIN MENU:")
        print("-" * 30)
        print("1. 🎯 Start Practice Session")
        print("2. 📊 View Statistics")
        print("3. 🎮 Practice Options")
        print("4. ❓ Help")
        print("5. 🚪 Exit")
        print("")

    def display_practice_menu(self):
        """Display practice session options."""
        print("\n🎯 PRACTICE SESSION OPTIONS:")
        print("-" * 40)
        print("1. 🎲 Random Questions (All)")
        print("2. 📂 Filter by Category")
        print("3. ⭐ Filter by Difficulty")
        print("4. 🎯 Specific Category + Difficulty")
        print("5. 📈 View Available Filters")
        print("6. 🔙 Back to Main Menu")
        print("")

    def get_user_choice(self, max_choice):
        """Get and validate user choice."""
        try:
            choice = input("👉 Enter your choice: ").strip()
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= max_choice:
                    return choice_num
            print("❌ Invalid choice. Please try again.")
            return None
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)
        except:
            print("❌ Invalid input. Please try again.")
            return None

    def setup_practice_session(self):
        """Set up a practice session based on user preferences."""
        while True:
            self.display_practice_menu()
            choice = self.get_user_choice(6)

            if choice == 1:
                # Random questions (all)
                count = self.game.set_question_pool()
                print(f"✅ Loaded {count} questions from all categories!")
                return True

            elif choice == 2:
                # Filter by category
                categories = get_categories()
                print("\n📂 Available Categories:")
                for i, category in enumerate(categories, 1):
                    print(f"{i}. {category.replace('_', ' ').title()}")
                print(f"{len(categories) + 1}. Back")

                cat_choice = self.get_user_choice(len(categories) + 1)
                if cat_choice and cat_choice <= len(categories):
                    selected_category = categories[cat_choice - 1]
                    count = self.game.set_question_pool(category=selected_category)
                    if count > 0:
                        print(f"✅ Loaded {count} questions from {selected_category.replace('_', ' ').title()}!")
                        return True
                    else:
                        print("❌ No questions found for this category.")

            elif choice == 3:
                # Filter by difficulty
                difficulties = get_difficulties()
                print("\n⭐ Available Difficulties:")
                for i, difficulty in enumerate(difficulties, 1):
                    print(f"{i}. {difficulty}")
                print(f"{len(difficulties) + 1}. Back")

                diff_choice = self.get_user_choice(len(difficulties) + 1)
                if diff_choice and diff_choice <= len(difficulties):
                    selected_difficulty = difficulties[diff_choice - 1]
                    count = self.game.set_question_pool(difficulty=selected_difficulty)
                    if count > 0:
                        print(f"✅ Loaded {count} questions with {selected_difficulty} difficulty!")
                        return True
                    else:
                        print("❌ No questions found for this difficulty.")

            elif choice == 4:
                # Specific category + difficulty
                categories = get_categories()
                print("\n📂 Select Category:")
                for i, category in enumerate(categories, 1):
                    print(f"{i}. {category.replace('_', ' ').title()}")

                cat_choice = self.get_user_choice(len(categories))
                if cat_choice:
                    selected_category = categories[cat_choice - 1]

                    difficulties = get_difficulties()
                    print("\n⭐ Select Difficulty:")
                    for i, difficulty in enumerate(difficulties, 1):
                        print(f"{i}. {difficulty}")

                    diff_choice = self.get_user_choice(len(difficulties))
                    if diff_choice:
                        selected_difficulty = difficulties[diff_choice - 1]
                        count = self.game.set_question_pool(
                            category=selected_category, 
                            difficulty=selected_difficulty
                        )
                        if count > 0:
                            print(f"✅ Loaded {count} questions: {selected_category.replace('_', ' ').title()} - {selected_difficulty}!")
                            return True
                        else:
                            print("❌ No questions found for this combination.")

            elif choice == 5:
                # View available filters
                print(self.game.get_available_filters())
                input("Press Enter to continue...")

            elif choice == 6:
                # Back to main menu
                return False

    def run_practice_session(self):
        """Run the main practice session."""
        print("\n" + "="*60)
        print("🎯 PRACTICE SESSION STARTED")
        print("="*60)
        print("Instructions:")
        print("• Read each question carefully")
        print("• Type 'hint' for hints, 'solution' to see the answer")
        print("• Type 'correct' if you got it right, 'wrong' if not")
        print("• Type 'skip' to skip a question, 'quit' to end session")
        print("="*60)

        while True:
            question = self.game.get_next_question()
            if not question:
                print("\n🎉 Congratulations! You've completed all questions in this set!")
                break

            # Show the question
            print("\n" + self.game.show_question())

            # Wait for user input
            while True:
                user_input = input("\n👉 Enter command (hint/solution/correct/wrong/skip/quit): ").strip().lower()

                if user_input == 'hint':
                    print(self.game.show_hints())

                elif user_input == 'solution':
                    print(self.game.show_solution())

                elif user_input == 'correct':
                    self.game.record_answer(True)
                    print("✅ Great job! Marked as correct.")
                    break

                elif user_input == 'wrong':
                    self.game.record_answer(False)
                    print("❌ No worries! Keep practicing.")
                    break

                elif user_input == 'skip':
                    print("⏭️ Question skipped.")
                    break

                elif user_input == 'quit':
                    print("\n📊 Ending practice session...")
                    print(self.game.get_session_summary())
                    return

                else:
                    print("❌ Invalid command. Try: hint, solution, correct, wrong, skip, or quit")

        # Show session summary
        print(self.game.get_session_summary())

    def show_statistics(self):
        """Display user statistics."""
        print("\n" + self.game.get_overall_stats())
        print("\nOptions:")
        print("1. 🔄 Reset Statistics")
        print("2. 🔙 Back to Main Menu")

        choice = self.get_user_choice(2)
        if choice == 1:
            confirm = input("⚠️ Are you sure you want to reset all statistics? (yes/no): ").strip().lower()
            if confirm in ['yes', 'y']:
                print(self.game.reset_stats())
            else:
                print("Statistics not reset.")

    def show_help(self):
        """Display help information."""
        help_text = """📚 LEETCODE PRACTICE TOOL - HELP

🎯 HOW TO USE:
1. Select 'Start Practice Session' from the main menu
2. Choose your practice preferences (category, difficulty, or all questions)
3. Read each question and think through the solution
4. Use commands during practice:
   • 'hint' - Get helpful hints for the current question
   • 'solution' - View the complete solution with explanation
   • 'correct' - Mark your answer as correct (if you solved it)
   • 'wrong' - Mark your answer as wrong (for honest practice)
   • 'skip' - Skip the current question
   • 'quit' - End the practice session

📊 STATISTICS:
The tool tracks your progress including:
• Total questions answered
• Accuracy percentage
• Performance by category and difficulty
• Current streak of correct answers

🎮 PRACTICE MODES:
• Random: Practice questions from all categories
• Category Filter: Focus on specific topics (arrays, strings, etc.)
• Difficulty Filter: Practice easy, medium, or hard questions
• Specific Filter: Combine category and difficulty

💡 TIPS:
• Be honest about your answers to track real progress
• Use hints before looking at solutions
• Review solutions even if you got the answer right
• Practice regularly to improve your streak

Press Enter to continue..."""
        print(help_text)
        input()

    def run(self):
        """Main application loop."""
        self.display_welcome()

        while True:
            self.display_main_menu()
            choice = self.get_user_choice(5)

            if choice == 1:
                # Start Practice Session
                if self.setup_practice_session():
                    self.run_practice_session()

            elif choice == 2:
                # View Statistics
                self.show_statistics()

            elif choice == 3:
                # Practice Options (same as start practice)
                self.setup_practice_session()

            elif choice == 4:
                # Help
                self.show_help()

            elif choice == 5:
                # Exit
                print("\n👋 Thanks for practicing! Keep coding!")
                sys.exit(0)


def main():
    """Entry point of the application."""
    try:
        app = LeetCodePracticeTool()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
