from typing import List, Optional
from datetime import datetime as dt
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class LocationBase(BaseModel):
    name: Optional[str] = None
    full_address: Optional[str]
    address_1: str
    address_2: Optional[str] = None
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    place_id: Optional[str]

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    created_at: dt

    model_config = ConfigDict(from_attributes=True, extra="ignore")

class EventBase(BaseModel):
    title: str
    host: Optional[str] = None
    description: Optional[str] = None
    start_date_time: dt
    end_date_time: Optional[dt] = None
    location_id: Optional[int] = None
    allow_qa: bool = True
    image_url: Optional[str] = None

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "title": "a title",
            "host": "my name",
            "description": "A local picnic with games and food.",
            "start_date_time": datetime.now().isoformat(),
            "end_date_time": (datetime.now().replace(hour=23, minute=59)).isoformat(),
            "location_id": 1,
            "allow_qa": True,
            "image_url": "",
        }        
    })

class EventCreate(EventBase):
    location: Optional[LocationBase] = None

class EventData(BaseModel):
    event_id: int = Field(..., alias="id")
    title: str
    host: Optional[str] = None
    description: Optional[str] = None
    start_date_time: dt
    end_date_time: Optional[dt] = None
    allow_qa: bool
    slug: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, extra="ignore")

class QACreate(BaseModel):
    id: Optional[int] = None  # QUESTION id - Required for answers
    question_text: Optional[str] = None  # Present if creating a question
    answer_text: Optional[str] = None  # Present if creating an answer

class QAResponse(BaseModel):
    id: int
    event_id: Optional[int] = None
    question_id: Optional[int] = None
    question_text: Optional[str] = None
    answer_text: Optional[str] = None
    created_at: dt

    model_config = ConfigDict(from_attributes=True)

class AnswerResponse(BaseModel):
    id: int
    answer_text: str
    created_at: dt

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    created_at: dt
    answers: Optional[List[AnswerResponse]] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class EventResponse(BaseModel):
    event: EventData
    location: Optional[Location] = None
    questions: Optional[List[QuestionResponse]] = None

    model_config = ConfigDict(from_attributes = True, extra = "ignore")