# This is for data validation
from pydantic import BaseModel
from datetime import datetime

class EventBase(BaseModel):
    title : str
    description : str | None = None
    datetime: datetime
    location_name: str | None = None
    is_public: bool
    image_url: str


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id : int

    class Config:
        orm_mode = True

