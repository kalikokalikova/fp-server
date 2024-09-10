from sqlalchemy.orm import Session

import app.models as models, app.schemas as schemas

def get_events(db: Session, skip:int=0, limit: int=100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def create_event(db:Session, event:schemas.EventCreate):
    db_event = models.Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event