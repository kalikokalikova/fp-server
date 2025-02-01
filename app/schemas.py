from typing import Union, Optional
from datetime import datetime as dt
from pydantic import BaseModel, Field

class LocationBase(BaseModel):
    name: Optional[str] = None
    full_address: Optional[str] = Field(None, alias="locationText")
    address_1: str = Field(..., alias="addressLine1")
    address_2: Optional[str] = Field(None, alias="addressLine2")
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str] = Field(..., alias="postcode")
    place_id: Optional[str] = Field(None, alias="placeId")
    
    class Config:
        populate_by_name = True

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
    host: Optional[str] = Field(None, alias="hostName")
    description: Optional[str] = None
    start_date_time: dt = Field(..., alias="startDateTime")
    end_date_time: Optional[dt] = Field(None, alias="endDateTime")
    location_id: Optional[int] = None
    allow_qa: bool = Field(..., alias="allowQA")
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
        populate_by_name = True

class EventCreate(EventBase):
    location: Optional[LocationBase] = None

class EventData(BaseModel):
    title: str
    host: Optional[str] = None
    description: Optional[str] = None
    start_date_time: dt
    end_date_time: Optional[dt] = None
    allow_qa: bool

    class Config:
        from_attributes = True
        extra = "ignore"

class EventResponse(BaseModel):
    event_id: int
    event: EventData
    location: Optional[Location] = None
    #questions: Optional[List[Question]] = None

    class Config:
        from_attributes = True
        extra = "ignore"