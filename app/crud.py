from sqlalchemy.orm import Session

import app.models as models, app.schemas as schemas

def get_events(db: Session, skip:int=0, limit: int=100):
    return db.query(models.Event).offset(skip).limit(limit).all()

def get_event_by_id(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def create_event(db:Session, event:schemas.EventCreate):
    db_event = models.Event(**event.model_dump())
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