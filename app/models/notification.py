#!/usr/bin/env python3
"""
Holds Notification class
"""

from app.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Notification(BaseModel, Base):
    """Representation of a notification"""
    __tablename__ = 'notifications'

    message = Column(String(255), nullable=False)

    user_id = Column(String(60), ForeignKey('users.id'), nullable=True)
    event_id = Column(String(60), ForeignKey('events.id'), nullable=True)

    # is_read = Column(Boolean, , nullable=False, default=False)

    user = relationship('User', back_populates='_notifications')
    event = relationship('Event', back_populates='notifications')

    def __init__(self, *args, **kwargs):
        """initializes notification"""
        super().__init__(*args, **kwargs)
