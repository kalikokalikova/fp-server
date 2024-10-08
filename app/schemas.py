# This is for data validation
from typing import Union, Optional
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
    #does changing the title change the slug? 
    #if yes, do we maintain redirects?
    description: Optional[str] = None
    startDateTime: Optional[dt] = None 
    location: Optional[str] = None
    isShareable: Optional[bool] = None
    image_url: Optional[str] = None
    slug: Optional[str] = None


class Event(EventBase):
    id : int

    class Config:
        from_attributes = True

