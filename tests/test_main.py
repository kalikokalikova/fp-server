from fastapi.testclient import TestClient
from app.main import app
from app import schemas, crud, models

client = TestClient(app)

def test_post_create_event():
    """Test creating an event via FastAPI route"""
    response = client.post("/api/v1/events/", json={
        "title": "API Test Event",
        "start_date_time": "2025-01-01T10:00:00"
    })

    assert response.status_code == 201
    data = response.json()

    assert "data" in data
    assert "event" in data["data"]
    assert "event_id" in data["data"]["event"]
    assert data["data"]["event"]["title"] == "API Test Event"

def test_get_event_by_id():
    """Test retrieving an event by ID, including questions and answers"""
    
    create_response = client.post("/api/v1/events/", json={
        "title": "Event with QA",
        "start_date_time": "2025-01-01T10:00:00",
        "allow_qa": True
    })

    assert create_response.status_code == 201
    data = create_response.json()

    assert "data" in data
    assert "event" in data["data"]
    event_id = data["data"]["event"]["event_id"]
    
    response = client.get(f"/api/v1/events/{event_id}")

    assert response.status_code == 200
    data = response.json()

    assert "event" in data
    assert data["event"]["title"] == "Event with QA"

    assert "questions" in data
    assert isinstance(data["questions"], list)

def test_get_event_by_id_and_slug():
    """Test retrieving an event by ID and slug"""
    
    create_response = client.post("/api/v1/events/", json={
        "title": "Slugged Event",
        "start_date_time": "2025-01-01T10:00:00",
        "allow_qa": True
    })

    assert create_response.status_code == 201
    data = create_response.json()

    event_id = data["data"]["event"]["event_id"]
    event_slug = data["data"]["event"]["slug"]

    response = client.get(f"/api/v1/events/{event_id}/{event_slug}")

    assert response.status_code == 200
    data = response.json()

    assert "event" in data
    assert data["event"]["id"] == event_id
    assert data["event"]["slug"] == event_slug

def test_post_question():
    """Test posting a question to an event"""

    create_response = client.post("/api/v1/events/", json={
        "title": "QA Event",
        "start_date_time": "2025-01-01T10:00:00",
        "allow_qa": True
    })
    assert create_response.status_code == 201
    event_id = create_response.json()["data"]["event"]["id"]

    question_response = client.post(f"/api/v1/events/{event_id}/qa", json={
        "question_text": "Can I bring my cat?"
    })

    assert question_response.status_code == 200
    data = question_response.json()

    assert "id" in data
    assert data["question_text"] == "Can I bring my cat?"

#test_post_answer
