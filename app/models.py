from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    host = Column(String(255))
    description = Column(String(500), index=True)
    start_date_time = Column(DateTime)
    end_date_time = Column(DateTime)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    location = relationship("Location", back_populates="events")
    image_url = Column(String(255))
    allow_qa = Column(Boolean, default=True)
    slug = Column(String(255), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    questions = relationship(
        "Question", 
        back_populates="event",
        cascade="all, delete-orphan")

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(String(255), nullable=True) #foreign key
    name = Column(String(255), nullable=False, index=True)
    full_address = Column(String(500), nullable=True)
    address_1 = Column(String(255), nullable=False)
    address_2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    zip = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    events = relationship("Event", back_populates="location")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    question_text = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    event = relationship("Event", back_populates="questions")
    answers = relationship(
        "Answer", 
        back_populates="question",
        cascade="all, delete-orphan")

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey ("questions.id"), nullable=False)
    answer_text = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    question = relationship("Question", back_populates="answers")