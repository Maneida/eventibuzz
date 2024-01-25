#!/usr/bin/env python3
"""
Holds class User
"""

from app.models.base_model import BaseModel, Base
from app.models.notification import Notification
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship


user_event_association = Table('user_role_association', Base.metadata,
    Column('user_id', String(60),ForeignKey('users.id')),
    Column('event_id', String(60),ForeignKey('events.id'))
)

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

    # Events being tracked by user
    tracked_events = relationship(
        'Event', secondary=user_event_association, back_populates='observers')

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

    # #####################################################################
    
    def create_created_notification(self):
        """
        Method for creating a notification when a new user is created.
        """
        notification_data = {
            "message": f"New user account created for '{self.email}'"
        }

        notification = Notification(user_id=self.id, **notification_data)
        notification.save()

    def create_deleted_notification(self):
        """
        Method for creating a notification when a user is deleted.
        """
        notification_data = {
            "message": f"User account, '{self.email}' has been deleted"
        }

        notification = Notification(user_id=self.id, **notification_data)
        notification.save()

    def create_updated_notification(self):
        """
        Method for creating a notification when a user is updated.
        """
        notification_data = {
            "message": f"User {self.email} details updated"
        }

        notification = Notification(user_id=self.id, **notification_data)
        notification.save()
