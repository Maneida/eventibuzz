#!/usr/bin/python3
"""
Holds Event class
"""
# import models
from app.models.base_model import BaseModel, Base
# import sqlalchemy
from sqlalchemy import Column, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship


class Event(BaseModel, Base):
    """Representation of an Event"""
    __tablename__ = 'events'

    title = Column(String(225), nullable=False)
    description = Column(Text, nullable=True)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)

    place_name = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    googleMapsUri = Column(String(2000))
    location_id = Column(String(512), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # #Possible Future implementation for multiple users per event

    # users = Column(String(255))
    # timezone = Column(String(50), nullable=False)
    # repeat_duration = Column(String(50))
    # created_by = Column(String(255))
    # updated_by = Column(String(255))

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    
    user = relationship('User', back_populates='_events')
    attachments = relationship('Attachment', back_populates='event',
                               lazy='joined', cascade='delete')
    notifications = relationship(
        'Notification', back_populates='event',
        lazy='joined', cascade='delete')

    def __init__(self, *args, **kwargs):
        """initializes Event"""
        super().__init__(*args, **kwargs)

        
