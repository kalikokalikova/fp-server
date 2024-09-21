from sqlalchemy.orm import Session
from slugify import slugify

import app.models as models, app.schemas as schemas

def get_events(db: Session, skip:int=0, limit: int=100):
    return db.query(models.Event).offset(skip).limit(limit).all()

def get_event_by_id(db: Session, event_id: int):
    #permit get by slug? what if slug is changed?
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def create_event(db:Session, event:schemas.EventCreate):
    slug = slugify(event.title)

    #ensure uniqueness
    existing_event = db.query(models.Event).filter(models.Event.slug == slug).first()
    count = 1

    # If the slug already exists, append a number to make it unique
    while existing_event:
        slug = f"{slugify(event.title)}-{count}"
        existing_event = db.query(models.Event).filter(models.Event.slug == slug).first()
        count += 1

    db_event = models.Event(**event.model_dump(), slug=slug)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

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