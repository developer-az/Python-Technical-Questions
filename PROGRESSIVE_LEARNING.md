# Progressive Learning Mode (Duolingo-Style)

## Overview

Progressive Learning Mode transforms the way users learn technical interview questions by breaking down solutions into manageable sections, similar to how Duolingo teaches languages. Instead of reviewing complete solutions at once, users build solutions step-by-step through multiple choice questions.

## Features

### 🎯 Section-by-Section Learning
- Solutions are automatically broken down into logical code sections
- Each section represents a distinct programming concept (function definition, loops, conditionals, etc.)
- Users progress through sections sequentially, building the complete solution

### 🔍 Multiple Choice Questions
- Each section presents 4 multiple choice options
- 1 correct answer and 3 carefully crafted distractors
- Distractors include common mistakes and alternative approaches
- Instant feedback on correct/incorrect choices

### 📊 Progress Tracking
- Visual progress indicator showing sections completed
- Real-time display of the solution being built
- Clear section numbering (e.g., "Section 2/5")
- Percentage completion shown at each step

### 💡 Educational Feedback
- Explanations provided for both correct and incorrect choices
- Key programming concepts highlighted for each section
- Section descriptions help understand the purpose of each code block

## How to Use

### CLI (Command Line Interface)

1. Run the flashcard game:
   ```bash
   python flashcard_game.py
   ```

2. Select "Start Practice Session" from the main menu

3. Choose your question filters (category, difficulty, or all questions)

4. When prompted, select "Progressive Learning (Duolingo-style)" mode

5. For each section:
   - Read the problem description
   - View the section description and key concepts
   - Choose the correct code from 4 options
   - Get instant feedback
   - See the solution build up as you progress

### Web Interface

1. Start the web server:
   ```bash
   python app.py
   ```

2. Navigate to: `http://localhost:5000/flashcard/progressive`

3. Select optional filters (category, difficulty)

4. Click "Start Progressive Learning"

5. Work through each section using the interactive web interface

## Example Session

```
📚 QUESTION: Two Sum
🏷️  Category: Arrays | Difficulty: Easy

🎯 You'll build the solution in 4 sections

📍 Section 1/4 - Function definition and parameters
💡 Key concepts: Hash Map/Dictionary

🔍 Choose the correct code for this section:

1. def twoSum(nums, target):    ← Correct!
2. def solution(arr, val):
3. def findPair(numbers, sum):
4. def searchArray(data, key):

✅ Correct! This function definition and parameters.

📦 Solution built so far:
def twoSum(nums, target):

📊 Progress: 25% complete (1/4 sections done)
```

## Benefits

### For Learners
- **Incremental Understanding**: Master one concept at a time
- **Active Learning**: Make choices instead of passive reading
- **Pattern Recognition**: Learn to identify common code patterns
- **Reduced Cognitive Load**: Focus on small sections instead of entire solutions
- **Immediate Feedback**: Know right away if you're on the right track

### For Interview Preparation
- **Component Mastery**: Understand each part of a solution
- **Common Mistakes**: Learn from distractor options
- **Code Structure**: See how solutions are organized
- **Concept Reinforcement**: Key concepts highlighted for each section

## Technical Implementation

### Code Section Parser
- Automatically analyzes solutions to identify logical sections
- Detects function definitions, loops, conditionals, assignments, etc.
- Preserves code structure and indentation
- Extracts complexity information separately

### Multiple Choice Generator
- Creates contextually relevant distractor options
- Uses common programming mistakes as wrong answers
- Adapts distractors based on section type
- Ensures exactly one correct answer per section

### Game Flow
1. Parse solution into sections
2. Present first section with choices
3. Validate user selection
4. If correct: add to built solution, move to next section
5. If incorrect: allow retry with feedback
6. Repeat until all sections complete
7. Show final complete solution

## API Endpoints

### Start Progressive Session
```
POST /flashcard/progressive/start
Body: { "category": "Arrays", "difficulty": "Easy" }
Response: { "progressive_data": {...}, "questions_loaded": 10 }
```

### Get Current Section
```
GET /flashcard/progressive/section
Response: { "section_data": { "choices": [...], "section": {...} } }
```

### Submit Choice
```
POST /flashcard/progressive/submit
Body: { "choice_index": 0 }
Response: { "result": { "correct": true, "feedback": "...", "next_section": {...} } }
```

### Get Progress
```
GET /flashcard/progressive/progress
Response: { "progress": { "current_section": 2, "total_sections": 5, ... } }
```

## Files Modified

- `flashcard_game.py`: Added CLI progressive learning mode
- `game.py`: Core progressive learning logic (already existed)
- `code_sections.py`: Parser and choice generator (already existed)
- `app.py`: API endpoints (already existed)
- `templates/progressive_flashcard.html`: Web interface (already existed)

## Testing

Run progressive learning tests:
```bash
python -m pytest test_progressive_learning.py -v
```

All tests pass, including:
- Section parsing
- Multiple choice generation
- Game flow integration
- Progress tracking
- Session management
