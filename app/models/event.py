#!/usr/bin/python3
"""
Holds Event class
"""
from app.models.base_model import BaseModel, Base
from app.models.notification import Notification
from sqlalchemy import Column, String, Text, Table, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship


user_event_association = Table('user_event_association', Base.metadata,
                               Column('user_id', String(60),
                                      ForeignKey('users.id')),
                               Column('event_id', String(60),
                                      ForeignKey('events.id'))
                               )


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

    _user = relationship('User', back_populates='_events')
    _attachments = relationship('Attachment', back_populates='_event',
                               lazy='joined', cascade='delete')
    _notifications = relationship(
        'Notification', back_populates='_event',
        lazy='joined', cascade='delete')

    # Users tracking event future
    _observers = relationship(
        'User', secondary=user_event_association,
        back_populates='_tracked_events')

    def __init__(self, *args, **kwargs):
        """initializes Event"""
        super().__init__(*args, **kwargs)

    @property
    def user(self):
        return [user.to_dict() for user in self._user]

    @property
    def attachments(self):
        return [event.to_dict() for event in self._attachments]

    @property
    def notifications(self):
        return [notification.to_dict() for notification in self._notifications]

    @property
    def observers(self):
        return [observer.to_dict() for observer in self._observers]

    def to_dict(self):
        """Converts the User object to a dictionary"""
        user_dict = super().to_dict()
        user_dict['attachments'] = self.attachments
        user_dict['notifications'] = self.notifications
        user_dict['observers'] = self.observers
        return user_dict

    # #####################################################################

    def create_created_notification(self):
        """
        Method for creating a notification when a new user is created.
        """
        notification_data = {
            "message": f"New Event '{self.title}' created."
        }
        # if user is the author use the above else
        # if subscribed, or for i in self.user.observers, do bthe below
        # notif_obj = storage.get('Notification', notif_id)
        # "message": f"Event'{self.title}'
        # created by '{self.user.get("username")}'"

        notification = Notification(event_id=self.id, user_id=self.user_id, **notification_data)
        notification.save()

    def create_deleted_notification(self):
        """
        Method for creating a notification when a user is deleted.
        """
        notification_data = {
            "message": f"Event '{self.title}' has been deleted"
        }

        notification = Notification(
            event_id=self.id, user_id=self.user_id, **notification_data)
        notification.save()

    def create_updated_notification(self):
        """
        Method for creating a notification when a user is updated.
        """
        notification_data = {
            "message": f"Event '{self.title}' details updated"
        }

        notification = Notification(event_id=self.id, user_id=self.user_id, **notification_data)
        notification.save()
