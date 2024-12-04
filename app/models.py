from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer,primary_key=True,index=True)
#     name = Column(String(255),index=True)
#     email = Column(String(255), unique=True, index=True)
#     todos = relationship("Todo",back_populates="owner")
#     is_active = Column(Boolean,default=False)


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    hostName = Column(String(255))
    description = Column(String(500), index=True)
    startDateTime = Column(DateTime)
    endDateTime = Column(DateTime)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    location = relationship("Location", back_populates="events")
    isShareable = Column(Boolean, default=False)
    image_url = Column(String(255))
    owner_id = Column(Integer)
    email = Column(String(255), nullable=True)
    allowQA = Column(Boolean, default=True)
    phone = Column(String(15), nullable=True)
    slug = Column(String(255), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    placeId = Column(String(255), nullable=True) #foreign key
    name = Column(String(255), nullable=False, index=True)
    addressLine1 = Column(String(255), nullable=False)
    addressLine2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postcode = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    events = relationship("Event", back_populates="location")