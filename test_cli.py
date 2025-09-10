from cli import load_questions
import subprocess
import sys


def test_load_questions():
    """Test that questions load correctly from the expanded database."""
    questions = load_questions()
    assert len(questions) >= 6  # Now we have at least 6 questions
    assert questions[0]["id"] == 1
    assert questions[0]["title"] == "Two Sum"
    # Verify we have questions from multiple categories
    categories = set(q.get("category", "General") for q in questions)
    assert len(categories) >= 3  # Should have Arrays, Strings, Trees, etc.


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
    assert "Valid Palindrome" in result.stdout  # Check for another question we know exists
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
