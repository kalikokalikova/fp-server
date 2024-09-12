from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import app.crud as crud, app.models as models, app.schemas as schemas
from app.database import SessionLocal, engine, Base
import json

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://fp-client-107bc916594c.herokuapp.com/",
    "https://fp-client-107bc916594c.herokuapp.com"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Dependency
def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()

# GETS
@app.get("/events/", response_model=list[schemas.Event], status_code=status.HTTP_200_OK)
def get_events(skip:int=0,limit:int=100,db:Session=Depends(get_db)):
    events = crud.get_events(db,skip=skip,limit=limit)
    if not events:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No events found")
        #better to return an empty list or a "no events found"? what did we decide about remote events?
    return events

@app.get("/events/{event_id}", response_model=schemas.Event, status_code=status.HTTP_200_OK)
def get_event_by_id(event_id: int, db: Session = Depends(get_db)):
    event = crud.get_event_by_id(db=db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# POSTS
@app.post("/events/",response_model=schemas.Event, status_code=status.HTTP_201_CREATED)
def post_event(event:schemas.EventCreate, db:Session=Depends(get_db)):
    return crud.create_event(db=db, event=event)

# PATCHES
@app.patch("/events/{event_id}", response_model=schemas.Event, status_code=status.HTTP_200_OK)
def update_event(event_id: int, event_data: schemas.EventUpdate, db: Session = Depends(get_db)):
    event = crud.update_event(db=db, event_id=event_id, event_data=event_data)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# DELETES
@app.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = crud.delete_event(db=db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted successfully"}