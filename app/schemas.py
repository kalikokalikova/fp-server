# This is for data validation
from typing import Union, Optional
from datetime import datetime
from pydantic import BaseModel

class EventBase(BaseModel):
    title : str
    description : str | None = None
    datetime: datetime
    location_name: str | None = None
    is_public: bool
    image_url: str


class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    #datetime: Optional[datetime] = None #variable not allowed in type expression?
    location_name: Optional[str] = None
    is_public: Optional[bool] = None
    image_url: Optional[str] = None    


class Event(EventBase):
    id : int

    class Config:
        orm_mode = True

