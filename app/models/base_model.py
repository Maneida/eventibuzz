#!/usr/bin/python3
"""Base Model for the Eventibuzz webserver"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
import uuid
import app.models

Base = declarative_base()
time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def update_modified_at(self):
        self.modified_at = datetime.utcnow()

    def bm_update(self, attr_dict=None):
        """
            updates the basemodel and sets the correct attributes
        """
        IGNORE = [
            'id', 'created_at', 'updated_at', 'email',
            'event_id', 'user_id', 'attachment_id', 'notification_id'
        ]
        if attr_dict:
            updated_dict = {
                k: v for k, v in attr_dict.items() if k not in IGNORE
            }
            for key, value in updated_dict.items():
                setattr(self, key, value)
            self.save()

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        app.models.storage.new(self)
        app.models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        attr = vars(self)
        new_dict = {
            k: v.to_dict() if k.startswith('_') else v
            for k, v in attr.items()
            if not k.startswith('_') and not k.startswith('__')
        }

        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        if "start_datetime" in new_dict:
            new_dict["start_datetime"] = new_dict["start_datetime"].strftime(
                time)
        if "end_datetime" in new_dict:
            new_dict["end_datetime"] = new_dict["end_datetime"].strftime(time)

        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        app.models.storage.delete(self)
