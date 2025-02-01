from sqlalchemy.orm import Session, joinedload
from slugify import slugify
import json

import app.models as models, app.schemas as schemas

def get_events(db: Session, skip:int=0, limit: int=100):
    return db.query(models.Event).offset(skip).limit(limit).all()

def get_event_by_id(db: Session, event_id: int):
    return db.query(models.Event).options(joinedload(models.Event.location)).filter(models.Event.id == event_id).first()

def create_event(db:Session, event:schemas.EventCreate):
    location_id = get_or_create_location(db, event.location) if event.location else event.location_id

    event_data = event.model_dump(exclude={"location", "location_id"})
 
    db_event = models.Event(**event_data, location_id=location_id, slug=None)

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    slug = f"{db_event.id}/{slugify(event.title)}"

    db_event.slug = slug
    db.commit()

    return db_event

def get_or_create_location(db: Session, location_data: schemas.LocationBase):
    # Check if the location already exists
    existing_location = db.query(models.Location).filter_by(placeId=location_data.placeId).first()
    if existing_location:
        return existing_location.id

    if not location_data.name:
        location_data.name = f"{location_data.addressLine1}, {location_data.city}, {location_data.state} {location_data.postcode}"
    
    # Create new location if not found
    new_location = models.Location(**location_data.model_dump())
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location.id

def update_event(db: Session, event_id: int, event_data: schemas.EventUpdate):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event is None:
        return None
    update_data = event_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(event, key, value)
    db.commit()
    db.refresh(event)
    return event

def delete_event(db: Session, event_id: int):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event is None:
        return None
    db.delete(event)
    db.commit()
    return event