# Python Technical Questions Practice Tool

A comprehensive tool for practicing Python technical interview questions with **dual interfaces**: modern web API and interactive CLI flashcard game.

## Features

- **🌐 Modern Web Interface**: Beautiful, responsive web application with Tailwind CSS
- **🎮 Interactive CLI Game**: Flashcard-style practice with progress tracking
- **📊 Comprehensive Statistics**: Track performance across categories and difficulties
- **🔍 Multiple Practice Modes**: Random, category-based, and difficulty-based filtering
- **💡 Progressive Hints**: Get helpful hints before viewing solutions
- **📚 Rich Question Database**: 6+ LeetCode problems with detailed solutions
- **🚀 RESTful API**: Full CRUD operations for programmatic access
- **✅ Comprehensive Testing**: 30+ unit tests covering all functionality

## Project Structure

```
.
├── app.py              # Flask web application
├── flashcard_game.py   # CLI flashcard game interface
├── game.py             # Game logic and statistics
├── questions.py        # Question database (6+ LeetCode problems)
├── cli.py              # Simple CLI interface
├── main.py             # Core algorithmic functions
├── templates/          # Web interface templates
├── static/             # CSS and static files
├── test_app.py         # Web API tests
├── test_main.py        # Algorithm tests
├── test_cli.py         # CLI tests
└── README.md           # This file
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

### 1. 🎮 Interactive CLI Flashcard Game

The CLI flashcard game provides an engaging way to practice coding questions with progress tracking.

#### Start the flashcard game:
```bash
python3 flashcard_game.py
```

#### Features:
- **Interactive menus** with emoji indicators
- **Multiple practice modes**: Random, category-based, difficulty-based
- **Progressive hints** before viewing solutions
- **Progress tracking** with statistics and streaks
- **Session summaries** with accuracy and duration

#### Game Commands:
- `hint` - Get helpful hints
- `solution` - View complete solution
- `correct` - Mark answer as correct
- `wrong` - Mark answer as wrong
- `skip` - Skip current question
- `quit` - End practice session

### 2. 📋 Simple CLI Interface

The simple CLI provides basic question browsing.

#### List all available questions:
```bash
python3 cli.py --list
```

#### View a specific question by ID:
```bash
python3 cli.py --question 1
```

#### Get help:
```bash
python3 cli.py --help
```

### 3. 🌐 Web API & Interface

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

### 4. 🔧 Core Functions

Run the main algorithmic functions directly:

```bash
python3 main.py
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

The tool includes **6+ LeetCode problems** across multiple categories:

### Arrays
1. **Two Sum** (Easy) - Find two numbers that add up to target
2. **Best Time to Buy and Sell Stock** (Easy) - Maximize profit from stock prices
3. **3Sum** (Medium) - Find all unique triplets that sum to zero

### Strings
4. **Valid Palindrome** (Easy) - Check if string is palindrome after cleaning

### Linked Lists
5. **Reverse Linked List** (Easy) - Reverse a singly linked list

### Trees
6. **Maximum Depth of Binary Tree** (Easy) - Find the maximum depth of a binary tree

### Additional Questions
- **Fibonacci Sequence** (Easy) - Calculate nth Fibonacci number
- **Reverse String** (Easy) - Reverse a string in place

Each question includes:
- **Detailed problem statements** with examples
- **Multiple solution approaches** with complexity analysis
- **Progressive hints** for learning
- **Complete code implementations**

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

## Deployment

### 🚀 Deploy to Render (Recommended - Free)

1. **Fork/Clone this repository** to your GitHub account
2. **Sign up** at [render.com](https://render.com)
3. **Connect your GitHub account**
4. **Create New Web Service**
5. **Select your repository**
6. **Configure:**
   - **Name**: `python-technical-questions`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
7. **Deploy!** Your app will be live at `https://your-app-name.onrender.com`

### 🚀 Deploy to Railway (Alternative - Free)

1. **Sign up** at [railway.app](https://railway.app)
2. **Connect GitHub** and select this repository
3. **Railway auto-detects** Flask app
4. **Deploy automatically**
5. **Get your live URL**

### 🚀 Deploy to Heroku (Alternative - Limited Free)

1. **Install Heroku CLI**
2. **Login**: `heroku login`
3. **Create app**: `heroku create your-app-name`
4. **Deploy**: `git push heroku master`
5. **Open**: `heroku open`

### 📝 Environment Variables

For production, consider setting:
- `FLASK_ENV=production`
- `FLASK_DEBUG=false`

## License

This project is open source and available under the MIT License.
