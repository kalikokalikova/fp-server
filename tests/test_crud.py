from app import crud, models, schemas
from datetime import datetime

def test_create_event(db):
    """Test creating an event in the database"""
    event_data = schemas.EventCreate(
        title="Test Event",
        start_date_time="2025-01-01T10:00:00"
    )

    event = crud.create_event(db, event_data)

    assert event.event.event_id is not None
    assert event.event.title == "Test Event"
    assert event.event.start_date_time == datetime.fromisoformat("2025-01-01T10:00:00")
    assert event.location is None