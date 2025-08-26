from cli import load_questions
import subprocess
import sys


def test_load_questions():
    """Test that questions load correctly."""
    questions = load_questions()
    assert len(questions) == 2
    assert questions[0]["id"] == 1
    assert questions[0]["title"] == "Two Sum"


def test_cli_help():
    """Test CLI help command."""
    result = subprocess.run(
        [sys.executable, "cli.py", "--help"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Python Technical Questions Practice Tool" in result.stdout


def test_cli_list():
    """Test CLI list command."""
    result = subprocess.run(
        [sys.executable, "cli.py", "--list"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Two Sum" in result.stdout
    assert "Fibonacci" in result.stdout


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
