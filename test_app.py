import pytest
import json
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    """Test the home endpoint."""
    response = client.get('/')
    
    assert response.status_code == 200
    assert b'Python Technical Questions Practice Tool' in response.data
    assert b'html' in response.data


def test_api_info_endpoint(client):
    """Test the API info endpoint."""
    response = client.get('/api')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['name'] == 'Python Technical Questions Practice Tool'
    assert 'endpoints' in data


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'ok'
    assert 'questions_count' in data


def test_get_questions(client):
    """Test getting all questions."""
    response = client.get('/questions')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert 'questions' in data
    assert 'total' in data
    assert len(data['questions']) >= 2  # Should have at least 2 questions


def test_get_questions_with_filter(client):
    """Test getting questions with difficulty filter."""
    response = client.get('/questions?difficulty=Easy')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert 'questions' in data
    assert all(q['difficulty'] == 'Easy' for q in data['questions'])


def test_get_questions_with_limit(client):
    """Test getting questions with limit."""
    response = client.get('/questions?limit=1')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(data['questions']) == 1


def test_get_specific_question(client):
    """Test getting a specific question by ID."""
    response = client.get('/questions/1')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert 'question' in data
    assert data['question']['id'] == 1


def test_get_nonexistent_question(client):
    """Test getting a question that doesn't exist."""
    response = client.get('/questions/999')
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert 'error' in data


def test_get_questions_by_difficulty(client):
    """Test getting questions by difficulty."""
    response = client.get('/questions/difficulty/Easy')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert 'questions' in data
    assert data['difficulty'] == 'Easy'
    assert all(q['difficulty'] == 'Easy' for q in data['questions'])


def test_get_questions_by_nonexistent_difficulty(client):
    """Test getting questions by a difficulty that doesn't exist."""
    response = client.get('/questions/difficulty/Hard')
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert 'error' in data
    assert 'available_difficulties' in data


def test_add_question(client):
    """Test adding a new question."""
    new_question = {
        "title": "Test Question",
        "difficulty": "Medium",
        "description": "This is a test question",
        "example": "Input: test\nOutput: result"
    }
    
    response = client.post('/questions', 
                          data=json.dumps(new_question),
                          content_type='application/json')
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['message'] == 'Question added successfully'
    assert 'question' in data
    assert data['question']['title'] == 'Test Question'


def test_add_question_missing_fields(client):
    """Test adding a question with missing required fields."""
    incomplete_question = {
        "title": "Test Question"
        # Missing difficulty and description
    }
    
    response = client.post('/questions',
                          data=json.dumps(incomplete_question),
                          content_type='application/json')
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert 'error' in data


def test_update_question(client):
    """Test updating an existing question."""
    update_data = {
        "title": "Updated Question Title",
        "description": "Updated description"
    }
    
    response = client.put('/questions/1',
                         data=json.dumps(update_data),
                         content_type='application/json')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['message'] == 'Question updated successfully'
    assert data['question']['title'] == 'Updated Question Title'


def test_update_nonexistent_question(client):
    """Test updating a question that doesn't exist."""
    update_data = {"title": "Updated Title"}
    
    response = client.put('/questions/999',
                         data=json.dumps(update_data),
                         content_type='application/json')
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert 'error' in data


def test_delete_question(client):
    """Test deleting a question."""
    # First, add a question to delete
    new_question = {
        "title": "Question to Delete",
        "difficulty": "Easy",
        "description": "This question will be deleted"
    }
    
    add_response = client.post('/questions',
                              data=json.dumps(new_question),
                              content_type='application/json')
    add_data = json.loads(add_response.data)
    question_id = add_data['question']['id']
    
    # Now delete it
    delete_response = client.delete(f'/questions/{question_id}')
    delete_data = json.loads(delete_response.data)
    
    assert delete_response.status_code == 200
    assert delete_data['message'] == 'Question deleted successfully'


def test_delete_nonexistent_question(client):
    """Test deleting a question that doesn't exist."""
    response = client.delete('/questions/999')
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert 'error' in data


def test_get_random_question(client):
    """Test getting a random question."""
    response = client.get('/practice/random')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert 'question' in data
    assert data['practice_mode'] == True


def test_get_random_question_by_difficulty(client):
    """Test getting a random question by difficulty."""
    response = client.get('/practice/random?difficulty=Easy')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert 'question' in data
    assert data['question']['difficulty'] == 'Easy'


def test_submit_solution(client):
    """Test submitting a solution."""
    solution_data = {
        "question_id": 1,
        "solution": "def two_sum(nums, target):\n    return [0, 1]"
    }
    
    response = client.post('/practice/submit',
                          data=json.dumps(solution_data),
                          content_type='application/json')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['solution_submitted'] == True
    assert 'evaluation' in data


def test_submit_solution_missing_data(client):
    """Test submitting a solution with missing data."""
    incomplete_data = {
        "question_id": 1
        # Missing solution
    }
    
    response = client.post('/practice/submit',
                          data=json.dumps(incomplete_data),
                          content_type='application/json')
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert 'error' in data


def test_submit_solution_invalid_question(client):
    """Test submitting a solution for a non-existent question."""
    solution_data = {
        "question_id": 999,
        "solution": "def test(): pass"
    }
    
    response = client.post('/practice/submit',
                          data=json.dumps(solution_data),
                          content_type='application/json')
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert 'error' in data


def test_get_stats(client):
    """Test getting statistics."""
    response = client.get('/stats')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert 'total_questions' in data
    assert 'difficulty_distribution' in data
    assert 'question_ids' in data


def test_404_error_handler(client):
    """Test 404 error handling."""
    response = client.get('/nonexistent-endpoint')
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert 'error' in data
    assert 'message' in data


def test_invalid_json_request(client):
    """Test handling of invalid JSON requests."""
    response = client.post('/questions',
                          data='invalid json',
                          content_type='application/json')
    
    # Should handle invalid JSON gracefully
    assert response.status_code in [400, 500]


def test_get_solutions(client):
    """Test getting solutions for a question."""
    response = client.get('/questions/1/solutions')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert 'solutions' in data
    assert 'question_title' in data
    assert len(data['solutions']) >= 1


def test_get_solutions_nonexistent_question(client):
    """Test getting solutions for a non-existent question."""
    response = client.get('/questions/999/solutions')
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert 'error' in data


def test_get_specific_solution(client):
    """Test getting a specific solution."""
    response = client.get('/questions/1/solutions/1')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert 'solution' in data
    assert data['solution']['id'] == 1


def test_get_specific_solution_nonexistent(client):
    """Test getting a non-existent solution."""
    response = client.get('/questions/1/solutions/999')
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert 'error' in data


def test_add_solution(client):
    """Test adding a new solution."""
    new_solution = {
        "title": "Test Solution",
        "description": "A test solution",
        "code": "def test(): return True",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
        "approach": "Test"
    }
    
    response = client.post('/questions/1/solutions',
                          data=json.dumps(new_solution),
                          content_type='application/json')
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['message'] == 'Solution added successfully'
    assert 'solution' in data


def test_add_solution_missing_fields(client):
    """Test adding a solution with missing required fields."""
    incomplete_solution = {
        "title": "Test Solution"
        # Missing description and code
    }
    
    response = client.post('/questions/1/solutions',
                          data=json.dumps(incomplete_solution),
                          content_type='application/json')
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert 'error' in data
