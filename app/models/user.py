#!/usr/bin/env python3
"""
Holds class User
"""

# import models
from app.models.base_model import BaseModel, Base
# import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    __tablename__ = 'users'

    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    

    _events = relationship('Event', back_populates="user",
                          lazy='joined', cascade='delete')
    _notifications = relationship('Notification', back_populates='user',
                                 lazy='joined', cascade='delete')

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    @property
    def events(self):
        return [event.to_dict() for event in self._events]

    @property
    def notifications(self):
        return [notification.to_dict() for notification in self._notifications]

    def to_dict(self):
        """Converts the User object to a dictionary"""
        user_dict = super().to_dict()
        user_dict['events'] = self.events
        user_dict['notifications'] = self.notifications
        return user_dict
