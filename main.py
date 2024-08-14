from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
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


@app.get("/events/", response_model=list[schemas.Event])
def get_events(skip:int=0,limit:int=100,db:Session=Depends(get_db)):
    events = crud.get_events(db,skip=skip,limit=limit)
    return events

@app.post("/events/",response_model=schemas.Event)
def post_event(event:schemas.EventCreate, db:Session=Depends(get_db)):
    return crud.create_event(db=db, event=event)

