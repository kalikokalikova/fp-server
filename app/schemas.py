# This is for data validation
from typing import Union, Optional
from datetime import datetime as dt
from pydantic import BaseModel, EmailStr

class EventBase(BaseModel):
    #add: end time (optional - could it be a string? eg "we'll be there until the mosquitoes get too bad!"), 
    #   host name, slug?, should location name & location address be two different things?
    title : str
    description : Optional[str] = None
    startDateTime: dt
    endDateTime: Optional[dt]
    #validation: must be after start time
    location: Optional[str] = None
    isShareable: bool
    allowQA: bool
    image_url: Optional[str] = None
    email: Optional[EmailStr]
    phone: Optional[str]

    class Config: 
        json_schema_extra = {
            "example": {
                "title": "Community Picnic",
                "description": "A local picnic with games and food.",
                "startDateTime": "2024-09-25T10:00:00Z",
                "endDateTime": "2024-09-25T14:00:00Z",
                "location": "my house",
                "isShareable": True,
                "allowQA": True,
                "image_url": "",
                "email": "foo@example.com",
                "phone": ""
            }
        }

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    datetime: Optional[dt] = None 
    location_name: Optional[str] = None
    is_public: Optional[bool] = None
    image_url: Optional[str] = None    


class Event(EventBase):
    id : int

    class Config:
        from_attributes = True

