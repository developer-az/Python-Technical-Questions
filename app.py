from flask import Flask, request, render_template
from cli import load_questions

from skills import (
    LANGUAGE_STARTERS,
    annotate_question,
    get_method_detail,
    get_skill_detail,
    get_skill_tree,
    get_methods_for_question,
    get_primary_method_id,
    starter_template,
)
from notes import notes_store

app = Flask(__name__)

# Load questions from CLI module
questions = load_questions()


def _annotated(question):
    """Attach method metadata for API/UI consumers."""
    return annotate_question(question)


def _find_question(question_id):
    return next((q for q in questions if q["id"] == question_id), None)


# Simple CORS headers
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response


@app.route("/")
def home():
    """Home endpoint with web interface."""
    return render_template("index.html")


@app.route("/api")
def api_info():
    """API information endpoint."""
    return {
        "name": "Drill",
        "version": "2.0.0",
        "description": "Drill — interview-style coding practice with skill methods, IDE, and technique notes",
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
            "GET /stats": "Get statistics",
            "GET /questions/<id>/solutions": "Get all solutions for a question",
            "GET /questions/<id>/solutions/<solution_id>": "Get specific solution",
            "POST /questions/<id>/solutions": "Add new solution to question",
            "GET /flashcard": "Flashcard game interface",
            "GET /flashcard/start": "Start flashcard session",
            "POST /flashcard/answer": "Submit flashcard answer",
            "GET /flashcard/stats": "Get flashcard statistics",
        },
    }


@app.route("/health")
def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Application is running",
        "questions_count": len(questions),
    }


@app.route("/questions", methods=["GET"])
def get_questions():
    """Get all questions with optional filtering."""
    difficulty = request.args.get("difficulty")
    limit = request.args.get("limit", type=int)

    filtered_questions = questions

    if difficulty:
        filtered_questions = [
            q for q in questions if q["difficulty"].lower() == difficulty.lower()
        ]

    if limit:
        filtered_questions = filtered_questions[:limit]

    annotated = [_annotated(q) for q in filtered_questions]
    return {
        "questions": annotated,
        "total": len(annotated),
        "filters": {"difficulty": difficulty, "limit": limit},
    }


@app.route("/questions/<int:question_id>", methods=["GET"])
def get_question(question_id):
    """Get a specific question by ID."""
    question = next((q for q in questions if q["id"] == question_id), None)

    if not question:
        return {"error": f"Question with ID {question_id} not found"}, 404

    return {"question": _annotated(question)}


@app.route("/questions/difficulty/<difficulty>", methods=["GET"])
def get_questions_by_difficulty(difficulty):
    """Get all questions of a specific difficulty level."""
    filtered_questions = [
        q for q in questions if q["difficulty"].lower() == difficulty.lower()
    ]

    if not filtered_questions:
        return {
            "error": f"No questions found with difficulty '{difficulty}'",
            "available_difficulties": list(set(q["difficulty"] for q in questions)),
        }, 404

    return {
        "questions": filtered_questions,
        "difficulty": difficulty,
        "count": len(filtered_questions),
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
            "example": data.get("example", ""),
        }

        questions.append(new_question)

        return {"message": "Question added successfully", "question": new_question}, 201

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

        return {"message": "Question updated successfully", "question": question}

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

    return {"message": "Question deleted successfully", "deleted_question": question}


@app.route("/practice/random", methods=["GET"])
def get_random_question():
    """Get a random question for practice."""
    import random

    if not questions:
        return {"error": "No questions available"}, 404

    difficulty = request.args.get("difficulty")

    if difficulty:
        available_questions = [
            q for q in questions if q["difficulty"].lower() == difficulty.lower()
        ]
        if not available_questions:
            return {
                "error": f"No questions available with difficulty '{difficulty}'",
                "available_difficulties": list(set(q["difficulty"] for q in questions)),
            }, 404
    else:
        available_questions = questions

    random_question = random.choice(available_questions)

    return {"question": _annotated(random_question), "practice_mode": True}


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
                "feedback": "This is a mock evaluation. In a real implementation, your code would be executed and tested against test cases.",
            },
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
        "question_ids": [q["id"] for q in questions],
    }


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return {
        "error": "Endpoint not found",
        "message": "Check the API documentation at /",
    }, 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return {"error": "Internal server error", "message": "Something went wrong"}, 500


@app.route("/questions/<int:question_id>/solutions", methods=["GET"])
def get_solutions(question_id):
    """Get all solutions for a specific question."""
    question = next((q for q in questions if q["id"] == question_id), None)

    if not question:
        return {"error": f"Question with ID {question_id} not found"}, 404

    solutions = question.get("solutions", [])

    return {
        "question_id": question_id,
        "question_title": question["title"],
        "solutions": solutions,
        "total_solutions": len(solutions),
    }


@app.route("/questions/<int:question_id>/solutions/<int:solution_id>", methods=["GET"])
def get_solution(question_id, solution_id):
    """Get a specific solution for a question."""
    question = next((q for q in questions if q["id"] == question_id), None)

    if not question:
        return {"error": f"Question with ID {question_id} not found"}, 404

    solutions = question.get("solutions", [])
    solution = next((s for s in solutions if s["id"] == solution_id), None)

    if not solution:
        return {
            "error": f"Solution with ID {solution_id} not found for question {question_id}"
        }, 404

    return {
        "question_id": question_id,
        "question_title": question["title"],
        "solution": solution,
    }


@app.route("/questions/<int:question_id>/solutions", methods=["POST"])
def add_solution(question_id):
    """Add a new solution to a question."""
    try:
        question = next((q for q in questions if q["id"] == question_id), None)

        if not question:
            return {"error": f"Question with ID {question_id} not found"}, 404

        data = request.get_json()

        if not data:
            return {"error": "No data provided"}, 400

        required_fields = ["title", "description", "code"]
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing required field: {field}"}, 400

        # Initialize solutions list if it doesn't exist
        if "solutions" not in question:
            question["solutions"] = []

        # Generate new solution ID
        new_id = (
            max(s["id"] for s in question["solutions"]) + 1
            if question["solutions"]
            else 1
        )

        new_solution = {
            "id": new_id,
            "title": data["title"],
            "description": data["description"],
            "code": data["code"],
            "time_complexity": data.get("time_complexity", "Not specified"),
            "space_complexity": data.get("space_complexity", "Not specified"),
            "approach": data.get("approach", "Not specified"),
        }

        question["solutions"].append(new_solution)

        return {"message": "Solution added successfully", "solution": new_solution}, 201

    except Exception as e:
        return {"error": f"Failed to add solution: {str(e)}"}, 500


# Flashcard Game Integration
from game import FlashcardGame

# Global flashcard game instance
flashcard_game = FlashcardGame()


@app.route("/flashcard")
def flashcard_interface():
    """Flashcard game web interface - Redirects to progressive learning."""
    return render_template("progressive_flashcard.html")


@app.route("/flashcard/progressive")
def progressive_flashcard_interface():
    """Progressive learning flashcard interface."""
    return render_template("progressive_flashcard.html")


@app.route("/flashcard/start", methods=["POST"])
def start_flashcard_session():
    """Start a new flashcard session."""
    try:
        data = request.get_json() or {}
        category = data.get("category")
        difficulty = data.get("difficulty")

        count = flashcard_game.set_question_pool(
            category=category, difficulty=difficulty
        )

        return {
            "message": "Flashcard session started",
            "questions_loaded": count,
            "filters": {"category": category, "difficulty": difficulty},
        }
    except Exception as e:
        return {"error": f"Failed to start session: {str(e)}"}, 500


@app.route("/flashcard/question", methods=["GET"])
def get_flashcard_question():
    """Get the next flashcard question."""
    question = flashcard_game.get_next_question()

    if not question:
        return {"message": "No more questions available"}, 404

    return {
        "question": {
            "id": question["id"],
            "title": question["title"],
            "category": question["category"],
            "difficulty": question["difficulty"],
            "problem": question["problem"],
        }
    }


@app.route("/flashcard/hint", methods=["GET"])
def get_flashcard_hint():
    """Get hints for current question."""
    if not flashcard_game.current_question:
        return {"error": "No active question"}, 404

    hints = flashcard_game.current_question.get("hints", [])
    return {"hints": hints}


@app.route("/flashcard/solution", methods=["GET"])
def get_flashcard_solution():
    """Get solution for current question."""
    if not flashcard_game.current_question:
        return {"error": "No active question"}, 404

    return {"solution": flashcard_game.current_question["solution"]}


@app.route("/flashcard/answer", methods=["POST"])
def submit_flashcard_answer():
    """Submit answer for current question."""
    try:
        data = request.get_json()
        is_correct = data.get("correct", False)

        flashcard_game.record_answer(is_correct)

        return {"message": "Answer recorded", "correct": is_correct}
    except Exception as e:
        return {"error": f"Failed to record answer: {str(e)}"}, 500


@app.route("/flashcard/stats", methods=["GET"])
def get_flashcard_stats():
    """Get flashcard statistics."""
    return {
        "overall_stats": flashcard_game.stats,
        "session_stats": flashcard_game.session_stats,
    }


@app.route("/flashcard/categories", methods=["GET"])
def get_flashcard_categories():
    """Get available categories for flashcard game."""
    from questions import get_categories, get_difficulties

    return {"categories": get_categories(), "difficulties": get_difficulties()}


# Progressive Learning Mode Routes
@app.route("/flashcard/progressive/start", methods=["POST"])
def start_progressive_flashcard():
    """Start a progressive learning session."""
    try:
        data = request.get_json() or {}
        category = data.get("category")
        difficulty = data.get("difficulty")

        # Set up question pool
        count = flashcard_game.set_question_pool(
            category=category, difficulty=difficulty
        )

        if count == 0:
            return {"error": "No questions found for the selected filters"}, 404

        # Enable progressive mode
        flashcard_game.enable_progressive_mode(True)

        # Get first question and start progressive session
        question = flashcard_game.get_next_question()
        if not question:
            return {"error": "No questions available"}, 404

        progressive_data = flashcard_game.start_progressive_question()
        if not progressive_data:
            return {"error": "Failed to start progressive session"}, 500

        return {
            "message": "Progressive flashcard session started",
            "questions_loaded": count,
            "filters": {"category": category, "difficulty": difficulty},
            "progressive_data": progressive_data,
        }
    except Exception as e:
        return {"error": f"Failed to start progressive session: {str(e)}"}, 500


@app.route("/flashcard/progressive/section", methods=["GET"])
def get_current_progressive_section():
    """Get the current section with multiple choice options."""
    try:
        if not flashcard_game.progressive_mode:
            return {"error": "Progressive mode not enabled"}, 400

        section_data = flashcard_game.get_current_section_with_choices()
        if not section_data:
            return {"error": "No current section available"}, 404

        return {"section_data": section_data}
    except Exception as e:
        return {"error": f"Failed to get current section: {str(e)}"}, 500


@app.route("/flashcard/progressive/submit", methods=["POST"])
def submit_progressive_choice():
    """Submit a choice for the current progressive section."""
    try:
        data = request.get_json()
        if not data or "choice_index" not in data:
            return {"error": "Missing choice_index in request"}, 400

        choice_index = data["choice_index"]
        result = flashcard_game.submit_section_choice(choice_index)

        return {"result": result}
    except Exception as e:
        return {"error": f"Failed to submit choice: {str(e)}"}, 500


@app.route("/flashcard/progressive/progress", methods=["GET"])
def get_progressive_progress():
    """Get current progress in progressive mode."""
    try:
        progress = flashcard_game.get_progressive_progress()
        if not progress:
            return {"error": "No progressive session active"}, 404

        return {"progress": progress}
    except Exception as e:
        return {"error": f"Failed to get progress: {str(e)}"}, 500


@app.route("/flashcard/progressive/next", methods=["POST"])
def next_progressive_question():
    """Move to next question in progressive mode."""
    try:
        if not flashcard_game.progressive_mode:
            return {"error": "Progressive mode not enabled"}, 400

        # Reset current progressive session
        flashcard_game.reset_progressive_session()

        # Get next question
        question = flashcard_game.get_next_question()
        if not question:
            return {"message": "No more questions available"}, 404

        # Start progressive session for new question
        progressive_data = flashcard_game.start_progressive_question()
        if not progressive_data:
            return {"error": "Failed to start progressive session"}, 500

        return {"progressive_data": progressive_data}
    except Exception as e:
        return {"error": f"Failed to get next question: {str(e)}"}, 500


# ---------------------------------------------------------------------------
# Drill platform: skills, practice IDE, notes
# ---------------------------------------------------------------------------


@app.route("/practice")
@app.route("/practice/<int:question_id>")
def practice_interface(question_id=None):
    """Interview-style practice IDE with notepad and method chips."""
    return render_template("practice.html", question_id=question_id)


@app.route("/skills")
def skills_interface():
    """Skill tree / method aggregation UI."""
    return render_template("skills.html", focus_method=None, focus_skill=None)


@app.route("/skills/method/<method_id>")
def method_interface(method_id):
    """Deep-link into a method on the skills page."""
    return render_template("skills.html", focus_method=method_id, focus_skill=None)


@app.route("/skills/skill/<skill_id>")
def skill_interface(skill_id):
    """Deep-link into a skill on the skills page."""
    return render_template("skills.html", focus_method=None, focus_skill=skill_id)


@app.route("/api/skills/tree", methods=["GET"])
def api_skill_tree():
    """Full pillar → skill → method tree with question counts."""
    return get_skill_tree(questions)


@app.route("/api/skills/methods/<method_id>", methods=["GET"])
def api_method_detail(method_id):
    detail = get_method_detail(method_id, questions)
    if not detail:
        return {"error": f"Method '{method_id}' not found"}, 404
    # Attach harvested notes for this method
    detail["notes"] = notes_store.list_notes(method_id=method_id, limit=50)
    return detail


@app.route("/api/skills/skills/<skill_id>", methods=["GET"])
def api_skill_detail(skill_id):
    detail = get_skill_detail(skill_id, questions)
    if not detail:
        return {"error": f"Skill '{skill_id}' not found"}, 404
    return detail


@app.route("/api/languages", methods=["GET"])
def api_languages():
    return {"languages": LANGUAGE_STARTERS}


@app.route("/api/practice/<int:question_id>", methods=["GET"])
def api_practice_question(question_id):
    """Payload for the practice IDE: problem, methods, starter, notepad, notes."""
    question = _find_question(question_id)
    if not question:
        return {"error": f"Question with ID {question_id} not found"}, 404

    language = request.args.get("language", "python")
    if language not in LANGUAGE_STARTERS:
        language = "python"

    annotated = _annotated(question)
    primary = get_primary_method_id(question_id)

    return {
        "question": annotated,
        "methods": annotated.get("methods", []),
        "languages": LANGUAGE_STARTERS,
        "language": language,
        "starter": starter_template(language, question),
        "notepad": notes_store.get_notepad(question_id),
        "notes": notes_store.list_notes(question_id=question_id, limit=50),
        "primary_method_id": primary,
        "progress": notes_store.get_progress()
        .get("by_question", {})
        .get(str(question_id)),
    }


@app.route("/api/practice/catalog", methods=["GET"])
def api_practice_catalog():
    """Lightweight question catalog for the practice sidebar."""
    difficulty = request.args.get("difficulty")
    method_id = request.args.get("method")
    catalog = []
    for q in questions:
        annotated = _annotated(q)
        if difficulty and q["difficulty"].lower() != difficulty.lower():
            continue
        if method_id:
            ids = [m["id"] for m in annotated.get("methods", [])]
            if method_id not in ids:
                continue
        catalog.append(
            {
                "id": q["id"],
                "title": q["title"],
                "difficulty": q["difficulty"],
                "category": q.get("category"),
                "methods": annotated.get("methods", []),
                "primary_method": annotated.get("primary_method"),
            }
        )
    return {"questions": catalog, "total": len(catalog)}


@app.route("/api/notes/notepad/<int:question_id>", methods=["GET"])
def api_get_notepad(question_id):
    if not _find_question(question_id):
        return {"error": f"Question with ID {question_id} not found"}, 404
    return notes_store.get_notepad(question_id)


@app.route("/api/notes/notepad/<int:question_id>", methods=["PUT", "POST"])
def api_save_notepad(question_id):
    if not _find_question(question_id):
        return {"error": f"Question with ID {question_id} not found"}, 404
    data = request.get_json() or {}
    content = data.get("content", "")
    return notes_store.save_notepad(question_id, content)


@app.route("/api/notes", methods=["GET"])
def api_list_notes():
    question_id = request.args.get("question_id", type=int)
    method_id = request.args.get("method_id")
    limit = request.args.get("limit", default=100, type=int)
    return {
        "notes": notes_store.list_notes(
            question_id=question_id, method_id=method_id, limit=limit
        )
    }


@app.route("/api/notes/harvest", methods=["POST"])
def api_harvest_notes():
    """Extract technique notes from code comments and persist them."""
    data = request.get_json() or {}
    code = data.get("code", "")
    question_id = data.get("question_id")
    language = data.get("language", "python")
    method_id = data.get("method_id")

    if question_id is None:
        return {"error": "Missing question_id"}, 400
    if not _find_question(int(question_id)):
        return {"error": f"Question with ID {question_id} not found"}, 404

    if not method_id:
        method_id = get_primary_method_id(int(question_id))

    added = notes_store.harvest_from_code(
        code,
        question_id=int(question_id),
        method_id=method_id,
        language=language,
    )
    return {
        "added": added,
        "count": len(added),
        "notes": notes_store.list_notes(question_id=int(question_id), limit=50),
    }


@app.route("/api/notes/<note_id>", methods=["DELETE"])
def api_delete_note(note_id):
    ok = notes_store.delete_note(note_id)
    if not ok:
        return {"error": "Note not found"}, 404
    return {"message": "Note deleted", "id": note_id}


@app.route("/api/practice/submit", methods=["POST"])
def api_practice_submit():
    """Save code notes, mark progress, return mock interview feedback."""
    data = request.get_json() or {}
    question_id = data.get("question_id")
    code = data.get("code", "")
    language = data.get("language", "python")
    notepad = data.get("notepad")
    mark_solved = bool(data.get("mark_solved", True))

    if question_id is None:
        return {"error": "Missing question_id"}, 400

    question = _find_question(int(question_id))
    if not question:
        return {"error": f"Question with ID {question_id} not found"}, 404

    method_id = data.get("method_id") or get_primary_method_id(int(question_id))

    if notepad is not None:
        notes_store.save_notepad(int(question_id), notepad)

    harvested = notes_store.harvest_from_code(
        code,
        question_id=int(question_id),
        method_id=method_id,
        language=language,
    )

    progress = None
    if mark_solved:
        progress = notes_store.mark_solved(int(question_id), method_id=method_id)

    methods = get_methods_for_question(int(question_id))
    method_names = [m["name"] for m in methods]

    return {
        "status": "recorded",
        "message": (
            "Rep recorded. Comments were harvested into technique notes; "
            "open the method to see how this aggregates upward."
        ),
        "harvested_count": len(harvested),
        "harvested": harvested,
        "progress": progress,
        "methods": method_names,
        "next_drill": (
            {
                "method_id": method_id,
                "method_name": methods[0]["name"] if methods else None,
                "url": f"/skills/method/{method_id}" if method_id else "/skills",
            }
            if method_id
            else None
        ),
        "feedback": {
            "interview_tip": (
                methods[0]["form_cues"][0]
                if methods
                else "State your approach before writing code."
            ),
            "complexity_reminder": (
                "Be ready to state time and space complexity out loud."
            ),
        },
    }


@app.route("/api/progress", methods=["GET"])
def api_progress():
    return notes_store.get_progress()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
