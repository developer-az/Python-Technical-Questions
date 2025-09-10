from cli import load_questions
import subprocess
import sys


def test_load_questions():
    """Test that questions load correctly from the expanded database."""
    questions = load_questions()
    assert len(questions) >= 21  # Now we have at least 21 questions
    assert questions[0]["id"] == 1
    assert questions[0]["title"] == "Two Sum"
    # Verify we have questions from multiple categories
    categories = set(q.get("category", "General") for q in questions)
    assert len(categories) >= 5  # Should have Arrays, Strings, Trees, DP, Linked Lists
    # Verify we have multiple difficulty levels
    difficulties = set(q.get("difficulty", "Unknown") for q in questions)
    assert "Easy" in difficulties
    assert "Medium" in difficulties
    assert "Hard" in difficulties


def test_expanded_question_categories():
    """Test that we have the expected categories in our expanded database."""
    questions = load_questions()
    categories = set(q.get("category", "General") for q in questions)

    expected_categories = {
        "Arrays",
        "Strings",
        "Linked Lists",
        "Trees",
        "Dynamic Programming",
    }
    assert expected_categories.issubset(
        categories
    ), f"Missing categories: {expected_categories - categories}"


def test_dynamic_programming_questions():
    """Test that we have Dynamic Programming questions."""
    questions = load_questions()
    dp_questions = [q for q in questions if q.get("category") == "Dynamic Programming"]

    assert len(dp_questions) >= 4  # Should have at least 4 DP questions
    # Check for specific classic DP problems
    dp_titles = {q["title"] for q in dp_questions}
    assert "Climbing Stairs" in dp_titles
    assert "Coin Change" in dp_titles
    assert "House Robber" in dp_titles
    assert "Longest Common Subsequence" in dp_titles


def test_cli_help():
    """Test CLI help command."""
    result = subprocess.run(
        [sys.executable, "cli.py", "--help"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Python Technical Questions Practice Tool" in result.stdout


def test_cli_list():
    """Test CLI list command with expanded question set."""
    result = subprocess.run(
        [sys.executable, "cli.py", "--list"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Two Sum" in result.stdout
    assert (
        "Valid Palindrome" in result.stdout
    )  # Check for another question we know exists
    assert "Maximum Depth of Binary Tree" in result.stdout  # And another one


def test_cli_question():
    """Test CLI question command."""
    result = subprocess.run(
        [sys.executable, "cli.py", "--question", "1"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Two Sum" in result.stdout
    assert "Easy" in result.stdout
