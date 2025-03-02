from fastapi import FastAPI, Depends, status, Body, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
import app.crud as crud, app.models as models, app.schemas as schemas
from app.database import SessionLocal, engine, Base
import traceback

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
        from fastapi import HTTPException
        import traceback
        print("Error Traceback:", traceback.format_exc())  # Debugging
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

@app.post("/api/v1/events/{event_id}/qa/", response_model=schemas.QAResponse)
def create_qa(event_id: int, qa_data: schemas.QACreate, request: Request, db: Session = Depends(get_db)):
    try:
        event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if event is None:
            raise ValueError("Event not found.")

        if qa_data.question_text and qa_data.answer_text:
            raise ValueError("Cannot have both question_text and answer_text.")
        if not qa_data.question_text and not qa_data.answer_text:
            raise ValueError("Either question_text or answer_text must be provided.")

        if qa_data.question_text:
            db_post = models.Question(event_id=event_id, question_text=qa_data.question_text)
        
        elif qa_data.answer_text:
            if not qa_data.id:
                raise ValueError("question id is required to post answers.")
            question = db.query(models.Question).filter(models.Question.id == qa_data.id).first()
            if not question:
                raise ValueError("Question not found")

            db_post = models.Answer(id=qa_data.id, answer_text=qa_data.answer_text)

        else:
            raise ValueError("Either question_text or answer_text must be provided.")
        
        db.add(db_post)
        db.commit()
        db.refresh(db_post)

        return db_post

    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": 400,
                "error": True,
                "message": str(e),
                "payload": qa_data.model_dump()
            }
        )
    
    except Exception as e:
        error_response = {
            "status": 400,
            "error": True,
            "message": str(e),
            "payload": qa_data.model_dump(),
            "trace": traceback.format_exc()
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_response)