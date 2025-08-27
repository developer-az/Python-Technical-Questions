from flask import Flask, jsonify, request, render_template
from cli import load_questions
import json

app = Flask(__name__)

# Load questions from CLI module
questions = load_questions()

# Simple CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route("/")
def home():
    """Home endpoint with web interface."""
    return render_template('index.html')


@app.route("/api")
def api_info():
    """API information endpoint."""
    return {
        "name": "Python Technical Questions Practice Tool",
        "version": "1.0.0",
        "description": "A comprehensive API for practicing Python technical interview questions",
        "endpoints": {
            "GET /": "Web interface",
            "GET /api": "API information",
            "GET /health": "Health check",
            "GET /questions": "List all questions",
            "GET /questions/<id>": "Get specific question by ID",
            "GET /questions/difficulty/<level>": "Get questions by difficulty",
            "POST /questions": "Add new question",
            "PUT /questions/<id>": "Update question",
            "DELETE /questions/<id>": "Delete question",
            "GET /practice/random": "Get random question for practice",
            "POST /practice/submit": "Submit solution for evaluation",
            "GET /stats": "Get statistics"
        }
    }


@app.route("/health")
def health():
    """Health check endpoint."""
    return {
        "status": "ok", 
        "message": "Application is running",
        "questions_count": len(questions)
    }


@app.route("/questions", methods=["GET"])
def get_questions():
    """Get all questions with optional filtering."""
    difficulty = request.args.get("difficulty")
    limit = request.args.get("limit", type=int)
    
    filtered_questions = questions
    
    if difficulty:
        filtered_questions = [q for q in questions if q["difficulty"].lower() == difficulty.lower()]
    
    if limit:
        filtered_questions = filtered_questions[:limit]
    
    return {
        "questions": filtered_questions,
        "total": len(filtered_questions),
        "filters": {
            "difficulty": difficulty,
            "limit": limit
        }
    }


@app.route("/questions/<int:question_id>", methods=["GET"])
def get_question(question_id):
    """Get a specific question by ID."""
    question = next((q for q in questions if q["id"] == question_id), None)
    
    if not question:
        return {"error": f"Question with ID {question_id} not found"}, 404
    
    return {"question": question}


@app.route("/questions/difficulty/<difficulty>", methods=["GET"])
def get_questions_by_difficulty(difficulty):
    """Get all questions of a specific difficulty level."""
    filtered_questions = [q for q in questions if q["difficulty"].lower() == difficulty.lower()]
    
    if not filtered_questions:
        return {
            "error": f"No questions found with difficulty '{difficulty}'",
            "available_difficulties": list(set(q["difficulty"] for q in questions))
        }, 404
    
    return {
        "questions": filtered_questions,
        "difficulty": difficulty,
        "count": len(filtered_questions)
    }


@app.route("/questions", methods=["POST"])
def add_question():
    """Add a new question."""
    try:
        data = request.get_json()
        
        if not data:
            return {"error": "No data provided"}, 400
        
        required_fields = ["title", "difficulty", "description"]
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing required field: {field}"}, 400
        
        # Generate new ID
        new_id = max(q["id"] for q in questions) + 1 if questions else 1
        
        new_question = {
            "id": new_id,
            "title": data["title"],
            "difficulty": data["difficulty"],
            "description": data["description"],
            "example": data.get("example", "")
        }
        
        questions.append(new_question)
        
        return {
            "message": "Question added successfully",
            "question": new_question
        }, 201
        
    except Exception as e:
        return {"error": f"Failed to add question: {str(e)}"}, 500


@app.route("/questions/<int:question_id>", methods=["PUT"])
def update_question(question_id):
    """Update an existing question."""
    try:
        question = next((q for q in questions if q["id"] == question_id), None)
        
        if not question:
            return {"error": f"Question with ID {question_id} not found"}, 404
        
        data = request.get_json()
        
        if not data:
            return {"error": "No data provided"}, 400
        
        # Update fields
        for field in ["title", "difficulty", "description", "example"]:
            if field in data:
                question[field] = data[field]
        
        return {
            "message": "Question updated successfully",
            "question": question
        }
        
    except Exception as e:
        return {"error": f"Failed to update question: {str(e)}"}, 500


@app.route("/questions/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    """Delete a question."""
    global questions
    
    question = next((q for q in questions if q["id"] == question_id), None)
    
    if not question:
        return {"error": f"Question with ID {question_id} not found"}, 404
    
    questions = [q for q in questions if q["id"] != question_id]
    
    return {
        "message": "Question deleted successfully",
        "deleted_question": question
    }


@app.route("/practice/random", methods=["GET"])
def get_random_question():
    """Get a random question for practice."""
    import random
    
    if not questions:
        return {"error": "No questions available"}, 404
    
    difficulty = request.args.get("difficulty")
    
    if difficulty:
        available_questions = [q for q in questions if q["difficulty"].lower() == difficulty.lower()]
        if not available_questions:
            return {
                "error": f"No questions available with difficulty '{difficulty}'",
                "available_difficulties": list(set(q["difficulty"] for q in questions))
            }, 404
    else:
        available_questions = questions
    
    random_question = random.choice(available_questions)
    
    return {
        "question": random_question,
        "practice_mode": True
    }


@app.route("/practice/submit", methods=["POST"])
def submit_solution():
    """Submit a solution for evaluation (mock implementation)."""
    try:
        data = request.get_json()
        
        if not data:
            return {"error": "No solution data provided"}, 400
        
        question_id = data.get("question_id")
        solution = data.get("solution")
        
        if not question_id or not solution:
            return {"error": "Missing question_id or solution"}, 400
        
        question = next((q for q in questions if q["id"] == question_id), None)
        
        if not question:
            return {"error": f"Question with ID {question_id} not found"}, 404
        
        # Mock evaluation - in a real app, this would run the code
        evaluation_result = {
            "question_id": question_id,
            "solution_submitted": True,
            "evaluation": {
                "status": "submitted",
                "message": "Solution submitted successfully (mock evaluation)",
                "feedback": "This is a mock evaluation. In a real implementation, your code would be executed and tested against test cases."
            }
        }
        
        return evaluation_result
        
    except Exception as e:
        return {"error": f"Failed to evaluate solution: {str(e)}"}, 500


@app.route("/stats", methods=["GET"])
def get_stats():
    """Get statistics about the questions."""
    if not questions:
        return {"error": "No questions available"}, 404
    
    difficulties = {}
    for question in questions:
        diff = question["difficulty"]
        difficulties[diff] = difficulties.get(diff, 0) + 1
    
    return {
        "total_questions": len(questions),
        "difficulty_distribution": difficulties,
        "question_ids": [q["id"] for q in questions]
    }


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return {"error": "Endpoint not found", "message": "Check the API documentation at /"}, 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return {"error": "Internal server error", "message": "Something went wrong"}, 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
