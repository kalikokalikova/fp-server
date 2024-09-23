from fastapi import FastAPI, Depends, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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

#Dependency
def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()

# GETS
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

@app.get("/api/v1/events/{event_id}/{event_slug}", status_code=status.HTTP_200_OK)
def get_event_by_id(event_id: int, event_slug: str, db: Session = Depends(get_db)):
    #eventually: 401 unauthorized?
    try: 
        #check if valid event_id
        if event_id <= 0:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status": 400,
                    "error": True,
                    "message": "Invalid event ID provided"
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
        
        if event.allowQA:
            # Fetch questions for the event
            questions = db.query(models.Question).filter(models.Question.event_id == event.id).all()

            # For each question, fetch answers
            question_responses = []
            for question in questions:
                answers = db.query(models.Answer).filter(models.Answer.question_id == question.id).all()

                answer_responses = [schemas.AnswerResponse(id=answer.id, answer=answer.answer) for answer in answers]

                question_responses.append(schemas.QuestionResponse(
                    question=question.question,
                    answers=answer_responses  # Use AnswerResponse objects directly
                ))
            event.questions = question_responses

            event_dict = event.__dict__.copy()
            event_dict['questions'] = question_responses
            
            return schemas.EventWithQAResponse.model_validate(event_dict)

        event_dict = event.__dict__.copy()
        return schemas.EventResponse.model_validate(event_dict)
    
    except Exception as e:
        #do we want to log errors?
        print(f"Error fetching event: {e}")
        return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "status": 500,
                    "error": True,
                    "message": "An unexpected error occurred"
                }
            )

# POSTS
@app.post("/api/v1/events/", response_model=schemas.Event, status_code=status.HTTP_201_CREATED)
def post_event(event:schemas.EventCreate = Body(...), db: Session=Depends(get_db)):
    try:
        #eventually: authentication check
        #if logged in then
        #if create new account then
        ##check if actually existing
        #else create w/o user_id

        if not event.title or event.startDateTime is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status": 400,
                    "error": True,
                    "message": "Missing required event fields"
                }
            )

        if isinstance(event.location, dict): #if API call successful and passed as dict
            location_name = event.location.get('location')
            location_address = event.location.get('address')
        else: 
            location_name = event.location
            location_address = None
        
        created_event = crud.create_event(db=db, event=event) #location_name=location_name, location_address=location_address

        return created_event
    
    except Exception as e:
        print(f"Error while creating event: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": 500,
                "error": True,
                "message": "An unexpected error occurred while creating the event"
            }
        )

# PATCHES
@app.patch("/api/v1/events/", response_model=schemas.Event, status_code=status.HTTP_200_OK)
def update_event(event_id: int, event_data: schemas.EventUpdate, db: Session = Depends(get_db)):
    try:
        #authentication placeholders
        #if not authorized_user():
        #    return JSONResponse(
        #        status_code=status.HTTP_401_UNAUTHORIZED,
        #        content={
        #            "status": 401,
        #            "error": True,
        #            "message": "Unauthorized access"
        #        }
        #    )
        #if not authorized_to_update(event_id): 
        #    return JSONResponse(
        #        status_code=status.HTTP_403_FORBIDDEN,
        #        content={
        #            "status": 403,
        #            "error": True,
        #            "message": "You do not have permission to update this event"
        #        }
        #    )

        if not event_data or not isinstance(event_data, schemas.EventUpdate):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status": 400,
                    "error": True,
                    "message": "Invalid event data"
                }
            )
        
        event = crud.update_event(db=db, event_id=event_id, event_data=event_data)

        if event is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "status": 404,
                    "error": True,
                    "message": "Event not found"
                }
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": 200,
                "error": False,
                "message": "Event successfully updated",
                "data": event
            }
        )        

    except Exception as e:
        # 500 Internal Server Error: Catch any unexpected server-side errors
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": 500,
                "error": True,
                "message": "An error occurred while updating the event"
            }
        )

# DELETES
@app.delete("/api/v1/events?", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    try: 
        #authentication placeholders
        #if not authorized_user():
        #    return JSONResponse(
        #        status_code=status.HTTP_401_UNAUTHORIZED,
        #        content={
        #            "status": 401,
        #            "error": True,
        #            "message": "Unauthorized access"
        #        }
        #    )
        #if not authorized_to_update(event_id): 
        #    return JSONResponse(
        #        status_code=status.HTTP_403_FORBIDDEN,
        #        content={
        #            "status": 403,
        #            "error": True,
        #            "message": "You do not have permission to update this event"
        #        }
        #    )
        if event_id <= 0:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status": 400,
                    "error": True,
                    "message": "Invalid event ID provided"
                }
            )

        event = crud.delete_event(db=db, event_id=event_id)

        if event is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "status": 404,
                    "error": True,
                    "message": "Event not found"
                }
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": 200,
                "error": False,
                "message": "Deleted event"
            }
        )
    
    except Exception as e:
        # 500 Internal Server Error: Catch any unexpected server-side errors
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": 500,
                "error": True,
                "message": "An error occurred while deleting the event"
            }
        )