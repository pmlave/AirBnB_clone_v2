#!/usr/bin/python3
"""This is the base model class for AirBnB"""
import uuid
import models
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import os

Base = declarative_base()

class BaseModel:
    """This class will defines all common attributes/methods
    for other classes
    """

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiation of base model class
        Args:
            args: it won't be used
            kwargs: arguments for the constructor of the BaseModel
        Attributes:
            id: unique id generated
            created_at: creation date
            updated_at: updated date
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            if 'id' not in kwargs.keys():
                self.id = str(uuid.uuid4())
                self.created_at = self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """returns a string
        Return:
            returns a string of class name, id, and dictionary
        """
        tmp = self.to_dict()
        if '__class__' in tmp:
            del tmp['__class__']
            tmp['created_at'] = self.__dict__['created_at']
            tmp['updated_at'] = self.__dict__['updated_at']
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, tmp)

    def __repr__(self):
        """return a string representaion
        """
        return self.__str__()

    def save(self):
        """updates the public instance attribute updated_at to current
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """creates dictionary of the class  and returns
        Return:
            returns a dictionary of all the key values in __dict__
        """
        my_dict = dict(self.__dict__)
        if os.getenv("HBNB_TYPE_STORAGE") != "db":
            my_dict["__class__"] = str(type(self).__name__)
            my_dict["created_at"] = self.created_at.isoformat()
            my_dict["updated_at"] = self.updated_at.isoformat()
        if '_sa_instance_state' in my_dict.keys():
            del my_dict['_sa_instance_state']

        return my_dict

    def delete(self):
        """Deletes the current instance from storage when calling delete
        """
        models.storage.delete(self)
