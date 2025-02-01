from sqlalchemy.orm import Session, joinedload
from slugify import slugify
from typing import List

import app.models as models, app.schemas as schemas

def get_events(db: Session, skip:int=0, limit: int=100) -> List[schemas.EventResponse]:
    events = db.query(models.Event).offset(skip).limit(limit).all()
    return [schemas.EventResponse.model_validate(event) for event in events]

def get_event_by_id(db: Session, id: int) -> schemas.EventResponse:
    event = db.query(models.Event).options(joinedload(models.Event.location)).filter(models.Event.event_id == event_id).first()
    return schemas.EventResponse.model_validate(event)

def create_event(db:Session, event:schemas.EventCreate):
    location_id = get_or_create_location(db, event.location) if event.location else event.location_id

    event_data = event.model_dump(exclude={"location", "location_id"})
 
    db_event = models.Event(**event_data, location_id=location_id, slug=None)

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    slug = f"{slugify(event.title)}"

    db_event.slug = slug
    db.commit()

    return schemas.EventResponse(
        event_id=db_event.id,
        event=schemas.EventData.model_validate(db_event),
        location=schemas.Location.model_validate(db_event.location) if db_event.location else None
    )

def get_or_create_location(db: Session, location_data: schemas.LocationBase):
    if location_data.place_id:
        existing_location = db.query(models.Location).filter(models.Location.place_id == location_data.place_id).first()
        if existing_location:
            return existing_location.id

    existing_location = db.query(models.Location).filter(models.Location.address_1 == location_data.address_1).first()
    if existing_location:
        return existing_location.id

    new_location = models.Location(
        place_id=location_data.place_id,
        address_1=location_data.address_1,
        address_2=location_data.address_2,
        city=location_data.city,
        state=location_data.state,
        zip=location_data.zip
    )

    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location.id