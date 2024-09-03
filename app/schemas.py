# This is for data validation
from typing import Union, Optional
from datetime import datetime as dt
from pydantic import BaseModel

class EventBase(BaseModel):
    title : str
    description : str | None = None
    datetime: dt
    location_name: str | None = None
    is_public: bool
    image_url: str


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
        orm_mode = True

