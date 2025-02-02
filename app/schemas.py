from typing import Union, Optional
from datetime import datetime as dt
from pydantic import BaseModel, Field

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

    class Config:
        from_attributes = True
        extra = "ignore"

class EventBase(BaseModel):
    title: str
    host: Optional[str] = None
    description: Optional[str] = None
    start_date_time: dt
    end_date_time: Optional[dt] = None
    location_id: Optional[int] = None
    allow_qa: bool = True
    image_url: Optional[str] = None

    class Config: 
        json_schema_extra = {
            "example": {
                "title": "a title",
                "host": "my name",
                "description": "A local picnic with games and food.",
                "start_date_time": "2024-09-25T10:00:00Z",
                "end_date_time": "2024-09-25T14:00:00Z",
                "location_id": 1,
                "allow_qa": True,
                "image_url": "",
            }
        }

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

    class Config:
        from_attributes = True
        populate_by_name = True
        extra = "ignore"

class EventResponse(BaseModel):
    event: EventData
    location: Optional[Location] = None
    #questions: Optional[List[Question]] = None

    class Config:
        from_attributes = True
        extra = "ignore"

class QACreate(BaseModel):
    question_id: Optional[int] = None  # Required for answers
    question_text: Optional[str] = None  # Present if creating a question
    answer_text: Optional[str] = None  # Present if creating an answer

class QAResponse(BaseModel):
    id: int
    event_id: Optional[int] = None
    question_id: Optional[int] = None
    question_text: Optional[str] = None
    answer_text: Optional[str] = None
    created_at: dt

    class Config:
        from_attributes = True