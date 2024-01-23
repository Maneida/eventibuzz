#!/usr/bin/env python3
"""
Holds Notification class
"""

# import models
from app.models.base_model import BaseModel, Base
# import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Notification(BaseModel, Base):
    """Representation of a notification"""
    __tablename__ = 'notifications'

    message = Column(String(255), nullable=False)

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    event_id = Column(String(60), ForeignKey('events.id'), nullable=False)
    
    user = relationship('User', back_populates='_notifications')
    event = relationship('Event', back_populates='notifications')

    def __init__(self, *args, **kwargs):
        """initializes notification"""
        super().__init__(*args, **kwargs)
