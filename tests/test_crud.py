from app.crud import create_event
from app.schemas import EventCreate

def test_create_event(db):
    event_data = EventCreate(
        title="Test Event",
        startDateTime="2025-01-01T10:00:00",
        endDateTime="2025-01-01T12:00:00",
        description="This is a test event.",
        isShareable=True,
        allowQA=True,
        location={"placeId": "12345", "name": "Test Location", "city": "Test City", "state": "TS", "postcode": "12345"}
    )

    event = create_event(db, event_data)

    assert event.id is not None
    assert event.title == "Test Event"
    assert event.slug.startswith(f"{event.id}/test-event")

from app.crud import get_events

def test_get_events(db):
    events = get_events(db)
    assert isinstance(events, list)

from app.crud import get_event_by_id

def test_get_event_by_id(db):
    event = get_event_by_id(db, 1)
    assert event is None  # No event should exist initially

"""from app.crud import update_event
from app.schemas import EventUpdate

def test_update_event(db):
    # Create an event first
    event_data = EventCreate(
        title="Original Title",
        startDateTime="2025-01-01T10:00:00",
        endDateTime="2025-01-01T12:00:00",
        description="Original Description",
        isShareable=True,
        allowQA=True,
        location={"placeId": "12345", "name": "Test Location", "city": "Test City", "state": "TS", "postcode": "12345"}
    )
    event = create_event(db, event_data)

    # Update the event title
    update_data = EventUpdate(title="Updated Title")
    updated_event = update_event(db, event.id, update_data)

    assert updated_event.title == "Updated Title"

from app.crud import delete_event

def test_delete_event(db):
    event_data = EventCreate(
        title="Event to Delete",
        startDateTime="2025-01-01T10:00:00",
        endDateTime="2025-01-01T12:00:00",
        description="This will be deleted.",
        isShareable=True,
        allowQA=True,
        location={"placeId": "12345", "name": "Test Location", "city": "Test City", "state": "TS", "postcode": "12345"}
    )
    event = create_event(db, event_data)

    deleted_event = delete_event(db, event.id)

    assert deleted_event is not None
    assert delete_event(db, event.id) is None  # Should return None after deletion

from app.crud import get_or_create_location
from app.schemas import LocationBase

def test_get_or_create_location(db):
    location_data = LocationBase(
        placeId="12345",
        name="Test Location",
        addressLine1="123 Test St",
        city="Test City",
        state="TS",
        postcode="12345"
    )

    location_id_1 = get_or_create_location(db, location_data)
    location_id_2 = get_or_create_location(db, location_data)

    assert location_id_1 == location_id_2  # It should return the same location ID

from app.crud import create_question
from app.schemas import QuestionCreate

def test_create_question(db):
    question_data = QuestionCreate(event_id=1, text="What is this event about?")
    question = create_question(db, question_data)

    assert question.id is not None
    assert question.text == "What is this event about?"

from app.crud import get_questions_by_event

def test_get_questions_by_event(db):
    questions = get_questions_by_event(db, 1)
    assert isinstance(questions, list)
"""