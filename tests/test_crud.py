from app import crud, models, schemas
from datetime import datetime

def test_create_event(db):
    """Test creating an event in the database, minimum required data"""
    event_data = schemas.EventCreate(
        title="Test Event",
        start_date_time="2025-01-01T10:00:00"
    )

    event = crud.create_event(db, event_data)

    assert event.event.event_id is not None
    assert event.event.title == "Test Event"
    assert event.event.start_date_time == datetime.fromisoformat("2025-01-01T10:00:00")
    assert event.location is None

def test_create_event_with_existing_location(db):
    """Test creating an event using an existing location"""
    location_id = crud.get_or_create_location(db, schemas.LocationBase(
        place_id="existing-place-123",
        full_address="789 Old St, Existing City, TS 56789",
        address_1="789 Old St",
        city="Existing City",
        state="TS",
        zip="56789"
    ))

    event_data = schemas.EventCreate(
        title="Event with existing location",
        start_date_time="2025-01-01T10:00:00",
        location_id=location_id
    )

    event = crud.create_event(db, event_data)

    assert event.event.event_id is not None
    assert event.event.title == "Event with existing location"
    assert event.location.id == location_id
    assert event.location is not None

def test_create_event_with_new_location(db):
    """Test creating an event and a new location together"""
    event_data = schemas.EventCreate(
        title="Event with new location",
        start_date_time="2025-01-01T10:00:00",
        location=schemas.LocationBase(
            place_id="new-place-456",
            full_address="456 New St, New City, TS 67890",
            address_1="456 New St",
            city="New City",
            state="TS",
            zip="67890"
        )
    )

    event = crud.create_event(db, event_data)

    assert event.event.event_id is not None
    assert event.event.title == "Event with new location"

    assert event.location is not None
    assert event.location.full_address == "456 New St, New City, TS 67890"
    assert event.location.place_id == "new-place-456"

def test_get_event_by_id(db):
    """Test retrieving an event by its ID"""
    event_data = schemas.EventCreate(
        title="Test Event",
        start_date_time="2025-01-01T10:00:00",
        location=schemas.LocationBase(
            place_id="test-place-789",
            full_address="789 Test Ave, Sample City, TS 67890",
            address_1="789 Test Ave",
            city="Sample City",
            state="TS",
            zip="67890"
        )
    )

    created_event = crud.create_event(db, event_data)

    fetched_event = crud.get_event_by_id(db, created_event.event.event_id)

    assert fetched_event is not None
    assert fetched_event.event.event_id == created_event.event.event_id
    assert fetched_event.event.title == "Test Event"
    assert fetched_event.event.start_date_time == created_event.event.start_date_time

    assert fetched_event.location is not None
    assert fetched_event.location.full_address == "789 Test Ave, Sample City, TS 67890"

def test_get_non_existent_event_by_id(db):
    """Test retrieving an event that does not exist"""
    non_existent_event_id = 9999  # Assuming this doesn't exist

    fetched_event = crud.get_event_by_id(db, non_existent_event_id)

    assert fetched_event is None

def test_get_or_create_location_creates_new_location(db):
    """Test that get_or_create_location creates a new location when it doesn't exist"""
    location_data = schemas.LocationBase(
        place_id="new-place-123",
        full_address="123 Test St, Testville, TS 12345",
        address_1="123 Test St",
        city="Testville",
        state="TS",
        zip="12345"
    )

    location_id = crud.get_or_create_location(db, location_data)

    assert location_id is not None
    location = db.query(models.Location).filter(models.Location.id == location_id).first()
    assert location is not None
    assert location.full_address == "123 Test St, Testville, TS 12345"

def test_get_or_create_location_retrieves_existing_location(db):
    """Test that get_or_create_location retrieves an existing location instead of creating a new one"""
    existing_location = models.Location(
        place_id="existing-place-789",
        name="Existing Test Location",
        full_address="456 Old St, Sample City, TS 67890",
        address_1="456 Old St",
        city="Sample City",
        state="TS",
        zip="67890"
    )
    db.add(existing_location)
    db.commit()
    db.refresh(existing_location)

    location_data = schemas.LocationBase(
        place_id="existing-place-789",
        full_address="456 Old St, Sample City, TS 67890",
        address_1="456 Old St",
        city="Sample City",
        state="TS",
        zip="67890"
    )

    location_id = crud.get_or_create_location(db, location_data)

    assert location_id == existing_location.id

#test_create_event_with_invalid_location
#test_create_event_without_title
#test_get_event_with_invalid_location