#!/usr/bin/python3
"""
Holds Event class
"""
from app.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Attachment(BaseModel, Base):
    """Representation of an Attachment"""
    __tablename__ = 'attachments'

    event_id = Column(String(60), ForeignKey('events.id'))
    file_path = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

    _event = relationship('Event', back_populates='_attachments')

    def __init__(self, *args, **kwargs):
        """initializes attachment"""
        super().__init__(*args, **kwargs)

    @property
    def event(self):
        return [event.to_dict() for event in self._event]
