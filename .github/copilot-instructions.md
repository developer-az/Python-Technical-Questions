# Python Technical Questions Practice Tool

Python Technical Questions is a practice tool for common leetcode questions in a flashcard-like game. It's built as both a CLI application and a Flask web application using Python 3.12.3.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Environment Setup
- Python 3.12.3 is available via `python` and `python3` commands
- Pip 24.0 is available via `pip3` command
- DO NOT use virtual environments - pip install in venv fails due to network timeouts. Use global --user installs instead.
- Install dependencies: `pip3 install --user <package>` (takes 2-5 seconds per package)
- Network timeouts may occur with PyPI - use --timeout=30 flag if needed

### Build and Development Commands
- Run main application: `python main.py` (takes ~0.02 seconds)
- Run CLI tool: `python cli.py --help` / `python cli.py --list` / `python cli.py --question 1` (takes ~0.03 seconds)
- Run Flask web app: `python app.py` (starts in ~1 second, runs on http://0.0.0.0:5000)

### Testing
- Run all tests: `python -m pytest test_*.py` (takes ~0.3 seconds for full suite)
- Run specific test file: `python -m pytest test_main.py -v` (takes ~0.2 seconds)
- Run with short traceback: `python -m pytest --tb=short` (takes ~0.2 seconds)
- NEVER CANCEL: All test commands complete in under 1 second. No special timeouts needed.

### Code Quality and Linting
- Format code: `python -m black .` (takes ~0.2 seconds for all files)
- Check formatting: `python -m black --check .` (takes ~0.2 seconds)
- Format with line length: `python -m black --line-length 79 .` (takes ~0.2 seconds)
- Lint code: `python -m flake8 *.py` (takes ~0.1 seconds)
- Type check: `python -m mypy *.py` (takes ~5 seconds)
- NEVER CANCEL: All linting commands complete in under 5 seconds. No special timeouts needed.

### Required Dependencies (install with pip3 install --user)
- pytest (for testing) - installs in ~3 seconds
- black (for code formatting) - installs in ~5 seconds  
- flake8 (for linting) - installs in ~5 seconds
- mypy (for type checking) - installs in ~5 seconds
- flask (for web app) - installs in ~2 seconds

## Validation

### Always run before committing
```bash
python -m black .
python -m flake8 *.py
python -m pytest test_*.py
```
All three commands complete in under 5 seconds total.

### Manual Testing Scenarios
- **CLI Application**: Test `python cli.py --list` shows available questions, `python cli.py --question 1` displays question details
- **Web Application**: Start `python app.py`, verify it serves on http://0.0.0.0:5000 with health endpoint at /health
- **Core Functionality**: Run `python main.py` to test main program logic (currently Fibonacci example)

### Common Validation Patterns
- Always test both import and execution: `python -c "from module import function"` then `python module.py`
- Test CLI arguments: Use `subprocess.run()` in tests to validate command line interface
- Web app testing: Start Flask app and verify startup messages show correct host/port

## Repository Structure and Key Files

### Current Structure
```
/home/runner/work/Python-Technical-Questions/Python-Technical-Questions/
├── main.py           # Core algorithm implementations (currently Fibonacci example)
├── cli.py            # Command-line interface for practice tool
├── app.py            # Flask web application
├── test_main.py      # Tests for main.py functions
├── test_cli.py       # Tests for CLI functionality
└── .github/
    └── copilot-instructions.md  # This file
```

### Key Code Locations
- **Question Database**: `load_questions()` function in `cli.py` - contains sample leetcode questions
- **CLI Interface**: `main()` function in `cli.py` with argparse for --list and --question flags
- **Web Interface**: Flask routes in `app.py` for / and /health endpoints
- **Algorithm Examples**: `fibonacci()` function in `main.py` as example implementation

## Common Development Tasks

### Adding New Questions
1. Edit `load_questions()` in `cli.py`
2. Add new dictionary with id, title, difficulty, description, example fields
3. Test with `python cli.py --list` and `python cli.py --question <id>`
4. Add corresponding test in `test_cli.py`

### Adding New Algorithms
1. Implement function in `main.py` 
2. Add corresponding test in `test_main.py`
3. Update CLI to reference new function if needed
4. Run full validation: `python -m black . && python -m flake8 *.py && python -m pytest test_*.py`

### Web Development
- Flask app in `app.py` uses development server (not for production)
- Add new routes by defining functions with `@app.route()` decorator
- Test with `python app.py` then visit http://0.0.0.0:5000
- Web app automatically reloads on file changes (debug=True)

## Troubleshooting

### Known Issues
- **Virtual Environments**: `python -m venv .venv` works but `pip install` in venv fails due to network timeouts - use global --user installs
- **Network Timeouts**: If pip install fails, retry with `--timeout=30` flag
- **Import Errors**: Always use relative imports and test both import and execution

### Error Recovery
- If linting fails: Run `python -m black .` to auto-fix formatting issues
- If tests fail: Check import statements and file paths are correct
- If web app won't start: Check for port conflicts, try different port with `app.run(port=5001)`

## Performance Expectations
- **Code execution**: All Python scripts run in <0.1 seconds
- **Testing**: Full test suite completes in <0.5 seconds  
- **Linting**: All linting tools complete in <5 seconds total
- **Package installation**: Most packages install in 2-5 seconds
- **Web app startup**: Flask development server starts in ~1 second

No special timeout handling needed for any operations - all complete quickly.