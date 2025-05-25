from sqlalchemy.orm import Session, joinedload
from slugify import slugify
from typing import List

import app.models as models, app.schemas as schemas

def get_events(db: Session, skip:int=0, limit: int=100) -> List[schemas.EventResponse]:
    events = (
        db.query(models.Event)
        .options(joinedload(models.Event.location))
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [schemas.EventResponse(
            event=schemas.EventData.model_validate(event, from_attributes=True),
            location=schemas.Location.model_validate(event.location, from_attributes=True) if event.location else None
        )
        for event in events
    ]

def get_event_by_id(db: Session, event_id: int) -> schemas.EventResponse:
    event = (
        db.query(models.Event)
        .options(
            joinedload(models.Event.location),
            joinedload(models.Event.questions).joinedload(models.Question.answers))
        .filter(models.Event.id == event_id)
        .first()
    )
    if not event:
        return None
    
    event_data = schemas.EventData.model_validate(event, from_attributes=True)
    location_data = schemas.Location.model_validate(event.location, from_attributes=True) if event.location else None
    
    questions_data = None
    if event.allow_qa:
        questions_data = [
            schemas.QuestionResponse(
                id=q.id,
                question_text=q.question_text,
                created_at=q.created_at,
                answers=[
                    schemas.AnswerResponse(
                        id=a.id,
                        answer_text=a.answer_text,
                        created_at=a.created_at
                    ) for a in sorted(q.answers, key=lambda x: x.created_at, reverse=True)
                ] if q.answers else None
            ) for q in sorted(event.questions, key=lambda x: x.created_at, reverse=True)
        ]

    response = schemas.EventResponse(
        event=event_data,
        location=location_data,
        questions=questions_data
    )

    return response

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
    
    new_location_data = location_data.model_dump(by_alias=False)

    #placeholders for missing fields
    #will need to return to this because this API is so damn inconsistent
    default_values = {
        "name": new_location_data.get("address_1", "Unnamed Location"),
        "city": "Unknown",
        "state": "Unknown",
        "zip": "00000"
    }
    for field, default in default_values.items():
        new_location_data[field] = new_location_data.get(field) or default

    new_location = models.Location(**new_location_data)

    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location.id