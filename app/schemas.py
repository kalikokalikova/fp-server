# This is for data validation
from typing import Union, Optional, List
from datetime import datetime as dt
from pydantic import BaseModel, EmailStr

class EventBase(BaseModel):
    title : str
    hostname : Optional[str] = None
    description : Optional[str] = None
    startDateTime: dt
    endDateTime: Optional[dt] = None
    location: Optional[str] = None
    isShareable: bool
    allowQA: bool
    image_url: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    owner_id: Optional[str] = None

    class Config: 
        json_schema_extra = {
            "example": {
                "title": "a title",
                "hostname": "my name",
                "description": "A local picnic with games and food.",
                "startDateTime": "2024-09-25T10:00:00Z",
                "endDateTime": "2024-09-25T14:00:00Z",
                "location": "my house",
                "isShareable": True,
                "allowQA": True,
                "image_url": "",
                "email": "example@foo.com",
                "phone": "9999999999"
            }
        }

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    startDateTime: Optional[dt] = None
    location: Optional[str] = None
    isShareable: Optional[bool] = None
    image_url: Optional[str] = None
    slug: Optional[str] = None


class Event(EventBase):
    title : str
    hostname : Optional[str] = None
    description : Optional[str] = None
    startDateTime: dt
    endDateTime: Optional[dt] = None
    location: Optional[str] = None
    owner_id: Optional[str] = None

    class Config:
        orm_mode = True

class EventResponse(BaseModel):
    title : str
    hostname : Optional[str] = None
    description : Optional[str] = None
    startDateTime: dt
    endDateTime: Optional[dt] = None
    location: Optional[str] = None
    owner_id: Optional[str] = None

    class Config:
        orm_mode = True

class AnswerResponse(BaseModel):
    id: int
    content: str

    class Config: 
        orm_mode = True

class QuestionResponse(BaseModel):
    id: int
    content: str
    answers: List[AnswerResponse] = []

    class config:
        orm_mode = True

class EventWithQAResponse(EventResponse): 
    questions: List[QuestionResponse] = []

    class Config:
        orm_mode = True