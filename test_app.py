import pytest
import json
import uuid
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    """Test the home endpoint."""
    response = client.get("/")

    assert response.status_code == 200
    assert b"Drill" in response.data
    assert b"html" in response.data


def test_api_info_endpoint(client):
    """Test the API info endpoint."""
    response = client.get("/api")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "Drill" in data["description"] or "Technical" in data["name"]
    assert "endpoints" in data
    assert data["version"] == "3.0.0"


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["status"] == "ok"
    assert "questions_count" in data


def test_get_questions(client):
    """Test getting all questions."""
    response = client.get("/questions")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "questions" in data
    assert "total" in data
    assert len(data["questions"]) >= 2  # Should have at least 2 questions


def test_get_questions_with_filter(client):
    """Test getting questions with difficulty filter."""
    response = client.get("/questions?difficulty=Easy")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "questions" in data
    assert all(q["difficulty"] == "Easy" for q in data["questions"])


def test_get_questions_with_limit(client):
    """Test getting questions with limit."""
    response = client.get("/questions?limit=1")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data["questions"]) == 1


def test_get_specific_question(client):
    """Test getting a specific question by ID."""
    response = client.get("/questions/1")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "question" in data
    assert data["question"]["id"] == 1


def test_get_nonexistent_question(client):
    """Test getting a question that doesn't exist."""
    response = client.get("/questions/999")
    data = json.loads(response.data)

    assert response.status_code == 404
    assert "error" in data


def test_get_questions_by_difficulty(client):
    """Test getting questions by difficulty."""
    response = client.get("/questions/difficulty/Easy")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "questions" in data
    assert data["difficulty"] == "Easy"
    assert all(q["difficulty"] == "Easy" for q in data["questions"])


def test_get_questions_by_nonexistent_difficulty(client):
    """Test getting questions by a difficulty that doesn't exist."""
    response = client.get("/questions/difficulty/Expert")
    data = json.loads(response.data)

    assert response.status_code == 404
    assert "error" in data
    assert "available_difficulties" in data


def test_add_question(client):
    """Test adding a new question."""
    new_question = {
        "title": "Test Question",
        "difficulty": "Medium",
        "description": "This is a test question",
        "example": "Input: test\nOutput: result",
    }

    response = client.post(
        "/questions", data=json.dumps(new_question), content_type="application/json"
    )
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data["message"] == "Question added successfully"
    assert "question" in data
    assert data["question"]["title"] == "Test Question"


def test_add_question_missing_fields(client):
    """Test adding a question with missing required fields."""
    incomplete_question = {
        "title": "Test Question"
        # Missing difficulty and description
    }

    response = client.post(
        "/questions",
        data=json.dumps(incomplete_question),
        content_type="application/json",
    )
    data = json.loads(response.data)

    assert response.status_code == 400
    assert "error" in data


def test_update_question(client):
    """Test updating an existing question."""
    update_data = {
        "title": "Updated Question Title",
        "description": "Updated description",
    }

    response = client.put(
        "/questions/1", data=json.dumps(update_data), content_type="application/json"
    )
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["message"] == "Question updated successfully"
    assert data["question"]["title"] == "Updated Question Title"


def test_update_nonexistent_question(client):
    """Test updating a question that doesn't exist."""
    update_data = {"title": "Updated Title"}

    response = client.put(
        "/questions/999", data=json.dumps(update_data), content_type="application/json"
    )
    data = json.loads(response.data)

    assert response.status_code == 404
    assert "error" in data


def test_delete_question(client):
    """Test deleting a question."""
    # First, add a question to delete
    new_question = {
        "title": "Question to Delete",
        "difficulty": "Easy",
        "description": "This question will be deleted",
    }

    add_response = client.post(
        "/questions", data=json.dumps(new_question), content_type="application/json"
    )
    add_data = json.loads(add_response.data)
    question_id = add_data["question"]["id"]

    # Now delete it
    delete_response = client.delete(f"/questions/{question_id}")
    delete_data = json.loads(delete_response.data)

    assert delete_response.status_code == 200
    assert delete_data["message"] == "Question deleted successfully"


def test_delete_nonexistent_question(client):
    """Test deleting a question that doesn't exist."""
    response = client.delete("/questions/999")
    data = json.loads(response.data)

    assert response.status_code == 404
    assert "error" in data


def test_get_random_question(client):
    """Test getting a random question."""
    response = client.get("/practice/random")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "question" in data
    assert data["practice_mode"] == True


def test_get_random_question_by_difficulty(client):
    """Test getting a random question by difficulty."""
    response = client.get("/practice/random?difficulty=Easy")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "question" in data
    assert data["question"]["difficulty"] == "Easy"


def test_submit_solution(client):
    """Test submitting a solution."""
    solution_data = {
        "question_id": 1,
        "solution": "def two_sum(nums, target):\n    return [0, 1]",
    }

    response = client.post(
        "/practice/submit",
        data=json.dumps(solution_data),
        content_type="application/json",
    )
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["solution_submitted"] == True
    assert "evaluation" in data


def test_submit_solution_missing_data(client):
    """Test submitting a solution with missing data."""
    incomplete_data = {
        "question_id": 1
        # Missing solution
    }

    response = client.post(
        "/practice/submit",
        data=json.dumps(incomplete_data),
        content_type="application/json",
    )
    data = json.loads(response.data)

    assert response.status_code == 400
    assert "error" in data


def test_submit_solution_invalid_question(client):
    """Test submitting a solution for a non-existent question."""
    solution_data = {"question_id": 999, "solution": "def test(): pass"}

    response = client.post(
        "/practice/submit",
        data=json.dumps(solution_data),
        content_type="application/json",
    )
    data = json.loads(response.data)

    assert response.status_code == 404
    assert "error" in data


def test_get_stats(client):
    """Test getting statistics."""
    response = client.get("/stats")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "total_questions" in data
    assert "difficulty_distribution" in data
    assert "question_ids" in data


def test_404_error_handler(client):
    """Test 404 error handling."""
    response = client.get("/nonexistent-endpoint")
    data = json.loads(response.data)

    assert response.status_code == 404
    assert "error" in data
    assert "message" in data


def test_invalid_json_request(client):
    """Test handling of invalid JSON requests."""
    response = client.post(
        "/questions", data="invalid json", content_type="application/json"
    )

    # Should handle invalid JSON gracefully
    assert response.status_code in [400, 500]


def test_get_solutions(client):
    """Test getting solutions for a question."""
    response = client.get("/questions/1/solutions")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "solutions" in data
    assert "question_title" in data
    assert len(data["solutions"]) >= 1


def test_get_solutions_nonexistent_question(client):
    """Test getting solutions for a non-existent question."""
    response = client.get("/questions/999/solutions")
    data = json.loads(response.data)

    assert response.status_code == 404
    assert "error" in data


def test_get_specific_solution(client):
    """Test getting a specific solution."""
    response = client.get("/questions/1/solutions/1")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "solution" in data
    assert data["solution"]["id"] == 1


def test_get_specific_solution_nonexistent(client):
    """Test getting a non-existent solution."""
    response = client.get("/questions/1/solutions/999")
    data = json.loads(response.data)

    assert response.status_code == 404
    assert "error" in data


def test_add_solution(client):
    """Test adding a new solution."""
    new_solution = {
        "title": "Test Solution",
        "description": "A test solution",
        "code": "def test(): return True",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
        "approach": "Test",
    }

    response = client.post(
        "/questions/1/solutions",
        data=json.dumps(new_solution),
        content_type="application/json",
    )
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data["message"] == "Solution added successfully"
    assert "solution" in data


def test_add_solution_missing_fields(client):
    """Test adding a solution with missing required fields."""
    incomplete_solution = {
        "title": "Test Solution"
        # Missing description and code
    }

    response = client.post(
        "/questions/1/solutions",
        data=json.dumps(incomplete_solution),
        content_type="application/json",
    )
    data = json.loads(response.data)

    assert response.status_code == 400
    assert "error" in data


def test_practice_page(client):
    response = client.get("/practice")
    assert response.status_code == 200
    assert b"Practice IDE" in response.data or b"code-editor" in response.data


def test_practice_page_with_question(client):
    response = client.get("/practice/1")
    assert response.status_code == 200


def test_skills_page(client):
    response = client.get("/skills")
    assert response.status_code == 200
    assert b"Skills" in response.data


def test_skill_tree_api(client):
    response = client.get("/api/skills/tree")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "pillars" in data
    assert data["method_count"] > 0


def test_method_detail_api(client):
    response = client.get("/api/skills/methods/hash_map")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["method"]["id"] == "hash_map"
    assert data["question_count"] >= 1
    assert data["parents"]


def test_practice_question_api(client):
    response = client.get("/api/practice/1?language=python")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["question"]["id"] == 1
    assert data["methods"][0]["id"] == "hash_map"
    assert "starter" in data
    assert "notepad" in data


def test_practice_catalog_api(client):
    response = client.get("/api/practice/catalog")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["total"] >= 1
    assert data["questions"][0]["primary_method"]


def test_notepad_and_harvest_flow(client):
    response = client.put(
        "/api/notes/notepad/1",
        data=json.dumps({"content": "Use a hash map for complements"}),
        content_type="application/json",
    )
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "hash map" in data["content"].lower()

    unique_cue = (
        f"# Store the complement in the map for O(1) lookup "
        f"during harvest-flow-{uuid.uuid4().hex[:8]}\n"
        "def two_sum(nums, target):\n"
        "    pass\n"
    )
    harvest = client.post(
        "/api/notes/harvest",
        data=json.dumps(
            {
                "question_id": 1,
                "method_id": "hash_map",
                "language": "python",
                "code": unique_cue,
            }
        ),
        content_type="application/json",
    )
    harvested = json.loads(harvest.data)
    assert harvest.status_code == 200
    assert harvested["count"] >= 1

    submit = client.post(
        "/api/practice/submit",
        data=json.dumps(
            {
                "question_id": 1,
                "code": (
                    f"# Track indices in a hash map instead of nested loops "
                    f"{uuid.uuid4().hex[:8]}\n"
                    "def f():\n"
                    "    pass\n"
                ),
                "language": "python",
                "notepad": "complement lookup",
                "mark_solved": True,
            }
        ),
        content_type="application/json",
    )
    result = json.loads(submit.data)
    assert submit.status_code == 200
    assert result["status"] == "recorded"
    assert result["next_drill"]["method_id"] == "hash_map"


def test_questions_include_methods(client):
    response = client.get("/questions/1")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["question"]["primary_method"]["id"] == "hash_map"


def test_learn_page(client):
    response = client.get("/learn")
    assert response.status_code == 200
    assert b"Encode" in response.data
    assert b"Retrieve" in response.data


def test_learn_session_api(client):
    response = client.post(
        "/api/learn/session",
        data=json.dumps({"limit": 4}),
        content_type="application/json",
    )
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["step_count"] == 4
    assert data["steps"][0]["card"]["retrieve_prompt"]


def test_learn_review_flow(client):
    unique = f"hash_map_test_{uuid.uuid4().hex[:6]}"
    # use a real method id
    encode = client.post(
        "/api/learn/encode",
        data=json.dumps({"kind": "method", "ref_id": "greedy_scan"}),
        content_type="application/json",
    )
    assert encode.status_code == 200
    elab = client.post(
        "/api/learn/elaborate",
        data=json.dumps(
            {
                "method_id": "greedy_scan",
                "text": f"Keep one running extremum {unique}",
            }
        ),
        content_type="application/json",
    )
    assert elab.status_code == 200
    review = client.post(
        "/api/learn/review",
        data=json.dumps(
            {"kind": "method", "ref_id": "greedy_scan", "rating": "good"}
        ),
        content_type="application/json",
    )
    data = json.loads(review.data)
    assert review.status_code == 200
    assert data["card"]["repetitions"] >= 1


def test_learn_mastery_api(client):
    response = client.get("/api/learn/mastery")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "due_count" in data
    assert data["total_methods"] >= 1
