import pytest
from datetime import datetime, UTC
from app import schemas

now = datetime.now(UTC)

def test_location_base_required_fields():
    with pytest.raises(ValueError):
        schemas.LocationBase()

    location = schemas.LocationBase(
        address_1="123 Main St",
        full_address="123 Main St, Townsville, TX 12345",
        city="Townsville",
        state="TX",
        zip="12345",
        place_id="abc123"
    )
    assert location.address_1 == "123 Main St"
    assert location.city == "Townsville"

def test_location_model_from_attributes():
    loc = schemas.Location(
        id=1,
        address_1="456 Oak St",
        full_address="456 Oak St, Townsville, TX 12345",
        city="Townsville",
        state="TX",
        zip="12345",
        place_id="place456",
        created_at=now
    )
    assert loc.id == 1
    assert loc.city == "Townsville"
    assert loc.created_at == now

def test_event_base_defaults_and_required():
    event = schemas.EventBase(
        title="Sample Event",
        start_date_time=now
    )

    assert event.title == "Sample Event"
    assert event.allow_qa is True  # default
    assert event.end_date_time is None  # optional

    # title is required
    with pytest.raises(ValueError):
        schemas.EventBase(start_date_time=now)

def test_event_create_with_location():
    event = schemas.EventCreate(
        title="Picnic",
        start_date_time=now,
        location=schemas.LocationBase(
            address_1="Park Rd",
            full_address="Park Rd, Townsville, TX",
            city="Townsville",
            state="TX",
            zip="67890",
            place_id="park123"
        )
    )

    assert event.location.address_1 == "Park Rd"
    assert event.location.city == "Townsville"

def test_event_data_alias_and_validation():
    data = schemas.EventData(
        id=123,
        title="Slug Test",
        start_date_time=now,
        allow_qa=False,
        slug="slug-test"
    )
    assert data.event_id == 123
    assert data.slug == "slug-test"

def test_question_response_and_aliases():
    resp = schemas.QuestionResponse(
        question_id=5,
        question_text="What's up?",
        created_at=now,
        answers=[]
    )
    assert resp.id == 5
    assert isinstance(resp.answers, list)

def test_answer_response():
    answer = schemas.AnswerResponse(
        answer_id=1,
        answer_text="Not much!",
        created_at=now
    )
    assert answer.id == 1
    assert answer.answer_text == "Not much!"

def test_qa_create_invalid_both_or_neither():
    # Both present — should not raise here (actual logic is in route, not schema)
    qa = schemas.QACreate(question_text="Q", answer_text="A", question_id=1)
    assert qa.question_text == "Q"
    assert qa.answer_text == "A"
    assert qa.question_id == 1

    # Neither present — technically allowed by schema, but enforced in route
    qa_empty = schemas.QACreate()
    assert qa_empty.question_text is None
    assert qa_empty.answer_text is None

def test_event_response_full():
    event = schemas.EventResponse(
        event=schemas.EventData(
            id=42,
            title="Test Event",
            start_date_time=now,
            allow_qa=True,
            slug="test-event"
        ),
        location=None,
        questions=[]
    )

    assert event.event.title == "Test Event"
    assert isinstance(event.questions, list)
