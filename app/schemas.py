from typing import Union, Optional
from datetime import datetime as dt
from pydantic import BaseModel, EmailStr

class LocationBase(BaseModel):
    name: Optional[str] = None
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: str
    postcode: str
    placeId: str

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
    hostName: Optional[str] = None
    description: Optional[str] = None
    startDateTime: dt
    endDateTime: Optional[dt] = None
    location_id: Optional[int] = None
    isShareable: bool
    allowQA: bool = True
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
                "location_id": 1,
                "isShareable": True,
                "allowQA": True,
                "image_url": "",
                "email": "example@foo.com",
                "phone": "9999999999"
            }
        }

class EventCreate(EventBase):
    location: Optional[LocationBase] = None

class EventUpdate(BaseModel):
    title: Optional[str] = None
    #does changing the title change the slug? 
    #if yes, do we maintain redirects?
    description: Optional[str] = None
    startDateTime: Optional[dt] = None 
    location_id: Optional[int] = None
    isShareable: Optional[bool] = None
    image_url: Optional[str] = None
    slug: Optional[str] = None

class Event(EventBase):
    id : int

    class Config:
        from_attributes = True
        extra = "ignore"