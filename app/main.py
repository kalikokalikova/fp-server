from fastapi import FastAPI, Depends, status, Body
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
import app.crud as crud, app.models as models, app.schemas as schemas
from app.database import SessionLocal, engine, Base

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

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()

@app.get("/test-cors")
async def test_cors():
    return {"message": "CORS works!"}

@app.get("/api/v1/events/", response_model=list[schemas.EventResponse], status_code=status.HTTP_200_OK)
def get_events(skip:int=0,limit:int=100,db:Session=Depends(get_db)):
    try:
        events = crud.get_events(db,skip=skip,limit=limit)
        if not events:
            return JSONResponse(
                status_code=status.HTTP_204_NO_CONTENT,
                content={
                    "status": 204,
                    "error": True,
                    "message": "No events found"
                }
            )
        return events

    except Exception as e:
        #do we want to log errors?
        print(f"Error fetching events: {e}")
        return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "status": 500,
                    "error": True,
                    "message": "An unexpected error occurred"
                }
            )

@app.get("/api/v1/events/{event_id}", response_model=schemas.EventResponse, status_code=status.HTTP_200_OK, name="Get event by ID")
@app.get("/api/v1/events/{event_id}/{event_name}", response_model=schemas.EventResponse, status_code=status.HTTP_200_OK, name="Get event by ID/slug")
def get_event(
            event_id: int,
            event_name: str = None,
            db: Session = Depends(get_db)
        ):
    try:
        #check if valid event_id
        if event_id <= 0:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status": 400,
                    "error": True,
                    "message": "Invalid event ID"
                }
            )

        event = crud.get_event_by_id(db=db, event_id=event_id)
        if event is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "status": 404,
                    "error": True,
                    "message": "Event not found"
                }
            )
        
        if event_name is None or event_name != event.event.slug:
            return RedirectResponse(url=f"/api/v1/events/{event.event.event_id}/{event.event.slug}", status_code=307)

        return event

    except Exception as e:
        import traceback
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.post("/api/v1/events/", status_code=status.HTTP_201_CREATED)
def post_event(event:schemas.EventCreate = Body(...), db: Session=Depends(get_db)):
    try:
        if not event.title or event.start_date_time is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status": 400,
                    "error": True,
                    "message": "Missing required event fields"
                }
            )

        created_event = crud.create_event(db=db, event=event)

        event_data = schemas.EventResponse.model_validate(created_event).model_dump()

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "status": 201,
                "error": False,
                "data": jsonable_encoder(event_data)
            }
        )

    except Exception as e:
        print(f"Error while creating event: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": 500,
                "error": True,
                "message": e
            }
        )