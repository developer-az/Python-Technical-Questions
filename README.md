# LeetCode Practice Tool - Flashcard Game 🚀

A full-fledged practice tool for common LeetCode questions in an interactive flashcard-style game format. Perfect for practicing coding interview questions with immediate feedback and progress tracking.

## Features ✨

- **📚 Common LeetCode Questions**: Curated collection of popular interview questions
- **🎯 Flashcard-Style Learning**: Interactive question-answer format with hints
- **📊 Progress Tracking**: Detailed statistics and performance analytics
- **🎮 Multiple Practice Modes**: Filter by category, difficulty, or practice all questions
- **💡 Hint System**: Progressive hints to guide your thinking
- **🔄 Persistent Statistics**: Track your progress across sessions
- **🏆 Streak Tracking**: Monitor your consecutive correct answers

## Question Categories 📂

- **Arrays**: Two Sum, Best Time to Buy/Sell Stock, 3Sum
- **Strings**: Valid Palindrome
- **Linked Lists**: Reverse Linked List
- **Trees**: Maximum Depth of Binary Tree

## Difficulty Levels ⭐

- **Easy**: Perfect for beginners
- **Medium**: Intermediate challenges
- **Hard**: Advanced problems (more coming soon!)

## Installation & Usage 🚀

### Prerequisites
- Python 3.6 or higher
- No external dependencies required!

### Quick Start
```bash
# Clone the repository
git clone https://github.com/developer-az/Python-Technical-Questions.git
cd Python-Technical-Questions

# Run the application
python3 main.py
```

### Alternative Execution
```bash
# Make the script executable
chmod +x main.py

# Run directly
./main.py
```

## How to Use 🎯

1. **Start the Application**: Run `python3 main.py`
2. **Choose Practice Mode**: Select from various filtering options
3. **Read Questions**: Study each problem carefully
4. **Use Interactive Commands**:
   - `hint` - Get helpful hints
   - `solution` - View the complete solution
   - `correct` - Mark your answer as correct
   - `wrong` - Mark as incorrect (be honest for better tracking!)
   - `skip` - Skip current question
   - `quit` - End practice session

## Features in Detail 📋

### Practice Modes
- **🎲 Random Questions**: Practice from all categories
- **📂 Category Filter**: Focus on specific topics (Arrays, Strings, etc.)
- **⭐ Difficulty Filter**: Practice by difficulty level
- **🎯 Specific Filter**: Combine category and difficulty

### Statistics & Analytics
- Total questions answered
- Overall accuracy percentage
- Performance breakdown by category
- Performance breakdown by difficulty
- Current streak of correct answers
- Session summaries

### Question Format
Each question includes:
- **Problem Statement**: Clear description with examples
- **Multiple Hints**: Progressive guidance
- **Complete Solution**: Code with time/space complexity analysis
- **Explanations**: Understanding the approach

## Example Session 🎮

```
🚀 LEETCODE PRACTICE TOOL - FLASHCARD GAME
============================================================
Welcome to your personal LeetCode practice companion!
Practice coding problems in a fun, flashcard-style format.
============================================================

📋 MAIN MENU:
------------------------------
1. 🎯 Start Practice Session
2. 📊 View Statistics
3. 🎮 Practice Options
4. ❓ Help
5. 🚪 Exit

👉 Enter your choice: 1

🎯 PRACTICE SESSION OPTIONS:
----------------------------------------
1. 🎲 Random Questions (All)
2. 📂 Filter by Category
3. ⭐ Filter by Difficulty
4. 🎯 Specific Category + Difficulty
5. 📈 View Available Filters
6. 🔙 Back to Main Menu

👉 Enter your choice: 2

📂 Available Categories:
1. Arrays
2. Strings
3. Linked Lists
4. Trees
5. Back

👉 Enter your choice: 1
✅ Loaded 3 questions from Arrays!

🎯 PRACTICE SESSION STARTED
============================================================
Instructions:
• Read each question carefully
• Type 'hint' for hints, 'solution' to see the answer
• Type 'correct' if you got it right, 'wrong' if not
• Type 'skip' to skip a question, 'quit' to end session
============================================================

===============================================================================
📚 QUESTION 1: Two Sum
🏷️  Category: Arrays | Difficulty: Easy
===============================================================================

Given an array of integers nums and an integer target, return indices of the 
two numbers such that they add up to target...

👉 Enter command (hint/solution/correct/wrong/skip/quit): hint

💡 HINTS:
----------------------------------------
1. Think about using a hash map to store numbers you've seen
2. For each number, check if its complement (target - number) exists
3. The complement approach avoids nested loops
```

## File Structure 📁

```
Python-Technical-Questions/
│
├── main.py          # Main application and CLI interface
├── game.py          # Game logic and flashcard functionality
├── questions.py     # Question database and management
├── README.md        # This documentation
└── leetcode_stats.json  # Auto-generated statistics file
```

## Statistics Tracking 📈

The tool automatically tracks:
- **Session Statistics**: Questions answered, accuracy, duration
- **Overall Statistics**: Total progress across all sessions
- **Category Performance**: How well you do in each topic area
- **Difficulty Performance**: Success rate by difficulty level
- **Streak Tracking**: Consecutive correct answers

Statistics are saved automatically in `leetcode_stats.json`.

## Tips for Success 💡

1. **Be Honest**: Mark answers correctly to track real progress
2. **Use Hints**: Try hints before looking at solutions
3. **Study Solutions**: Review explanations even if you got it right
4. **Practice Regularly**: Consistency improves your streak
5. **Focus on Weak Areas**: Use category/difficulty filters to target improvement

## Future Enhancements 🔮

- More questions across all categories
- Timed practice sessions
- Export progress reports
- Custom question sets
- Difficulty progression recommendations
- Visual progress charts

## Contributing 🤝

Feel free to contribute by:
- Adding more LeetCode questions
- Improving the user interface
- Adding new features
- Fixing bugs
- Enhancing documentation

## License 📄

This project is open source. Feel free to use, modify, and distribute.

---

**Happy Coding! 🎉**

Made with ❤️ for the coding interview preparation community.