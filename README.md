# Python Technical Questions Practice Tool

A comprehensive tool for practicing Python technical interview questions with multiple interfaces: CLI, web API, and algorithmic functions.

## Features

- **CLI Interface**: Interactive command-line tool for browsing and practicing questions
- **Web API**: Flask-based REST API for programmatic access
- **Algorithmic Functions**: Core implementations of common interview problems
- **Test Suite**: Comprehensive unit tests for all components

## Project Structure

```
.
├── app.py          # Flask web application
├── cli.py          # Command-line interface
├── main.py         # Core algorithmic functions
├── test_main.py    # Tests for algorithmic functions
├── test_cli.py     # Tests for CLI interface
└── README.md       # This file
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Dependencies

Install the required dependencies:

```bash
# For Ubuntu/Debian systems
sudo apt install python3-flask python3-pytest

# For other systems or to install flask-cors
pip3 install flask flask-cors pytest --user --break-system-packages
```

Or install from requirements.txt:

```bash
pip3 install -r requirements.txt --user --break-system-packages
```

## Usage

### 1. Command Line Interface (CLI)

The CLI provides an interactive way to browse and practice coding questions.

#### List all available questions:
```bash
python cli.py --list
```

#### View a specific question by ID:
```bash
python cli.py --question 1
```

#### Get help:
```bash
python cli.py --help
```

### 2. Web API

The Flask application provides a comprehensive REST API with a modern web interface.

#### Start the web server:
```bash
python3 app.py
```

The server will start on `http://localhost:5000`

#### Web Interface:
- **GET /** - Modern web interface for managing questions
- **GET /api** - API documentation and information

#### REST API Endpoints:

**Question Management:**
- **GET /questions** - List all questions (with optional filtering)
- **GET /questions/<id>** - Get specific question by ID
- **GET /questions/difficulty/<level>** - Get questions by difficulty
- **POST /questions** - Add new question
- **PUT /questions/<id>** - Update existing question
- **DELETE /questions/<id>** - Delete question

**Practice Features:**
- **GET /practice/random** - Get random question for practice
- **POST /practice/submit** - Submit solution for evaluation

**Utility:**
- **GET /health** - Health check endpoint
- **GET /stats** - Get statistics about questions

#### Example API calls:
```bash
# Health check
curl http://localhost:5000/health

# Get all questions
curl http://localhost:5000/questions

# Get questions by difficulty
curl http://localhost:5000/questions/difficulty/Easy

# Add new question
curl -X POST http://localhost:5000/questions \
  -H "Content-Type: application/json" \
  -d '{"title":"New Question","difficulty":"Medium","description":"Description"}'

# Get random question
curl http://localhost:5000/practice/random

# Get statistics
curl http://localhost:5000/stats
```

### 3. Core Functions

Run the main algorithmic functions directly:

```bash
python main.py
```

This will execute the Fibonacci sequence demonstration.

## Testing

### Run All Tests

Execute the test suite to verify all components work correctly:

```bash
# Test algorithmic functions
python -m pytest test_main.py -v

# Test CLI interface
python -m pytest test_cli.py -v

# Test web API
python -m pytest test_app.py -v

# Run all tests
python -m pytest test_*.py -v
```

### Manual Testing

#### Test CLI Commands:
```bash
# Test help
python cli.py --help

# Test listing questions
python cli.py --list

# Test specific question
python cli.py --question 1
```

#### Test Web API:
```bash
# Start the server
python3 app.py

# In another terminal, test endpoints
curl http://localhost:5000/health
curl http://localhost:5000/api
curl http://localhost:5000/questions
curl http://localhost:5000/stats

# Or open in browser
# http://localhost:5000/ (web interface)
```

#### Test Core Functions:
```bash
python main.py
```

## Available Questions

The tool currently includes these practice questions:

1. **Two Sum** (Easy)
   - Find two numbers in an array that add up to a target
   - Example: `nums = [2,7,11,15], target = 9` → `[0,1]`

2. **Fibonacci Sequence** (Easy)
   - Calculate the nth Fibonacci number
   - Example: `n = 5` → `5` (sequence: 0,1,1,2,3,5)

## Development

### Adding New Questions

To add new questions, modify the `load_questions()` function in `cli.py`:

```python
def load_questions():
    return [
        # ... existing questions ...
        {
            "id": 3,
            "title": "New Question",
            "difficulty": "Medium",
            "description": "Question description",
            "example": "Input: ...\nOutput: ...",
        },
    ]
```

### Adding New API Endpoints

To add new endpoints to the web API, modify `app.py`:

```python
@app.route("/questions")
def get_questions():
    # Implementation here
    pass
```

### Running in Development Mode

For development with auto-reload:

```bash
# Flask development server
export FLASK_ENV=development
python app.py
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running commands from the project root directory
2. **Port Already in Use**: Change the port in `app.py` or kill the existing process
3. **Missing Dependencies**: Install Flask with `pip install flask`

### Debug Mode

Enable debug mode for detailed error messages:

```bash
export FLASK_DEBUG=1
python app.py
```

## Contributing

1. Add new questions to the `load_questions()` function
2. Implement corresponding algorithmic solutions
3. Add comprehensive tests
4. Update this README with new features

## License

This project is open source and available under the MIT License.
