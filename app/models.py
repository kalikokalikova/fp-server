from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

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
    hostname = Column(String(255))
    description = Column(String(500), index=True)
    startDateTime = Column(DateTime)
    endDateTime = Column(DateTime)
    location = Column(String(255)) #str for now, object later
    isShareable = Column(Boolean)
    image_url = Column(String(255)) 
    owner_id = Column(Integer)
    email = Column(String(255), nullable=True)
    allowQA = Column(Boolean, default=True)
    phone = Column(String(15), nullable=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)