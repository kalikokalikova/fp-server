from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_events():
    response = client.get("/api/v1/events/")
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) > 0

    first_event = data[0]
    assert "title" in first_event
    assert "startDateTime" in first_event
    assert "location" in first_event
    assert isinstance(first_event["location"], dict)

#CRUD tests
#Create
#Read list
#Read single item
#Update
#Delete

#Edge cases/validations

#Authentication/authorization

#Performance/load

#Error handling