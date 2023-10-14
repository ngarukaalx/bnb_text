#!/usr/bin/python3
"""
This module defines a class BaseModel which will be inherited
by all BaseModelInstances.
"""
import uuid
from datetime import datetime
from models import storage


class BaseModel():
    """
    defines a base class BaseModel.
    """

    def __init__(self, *args, **kwargs):
        """initialises a BaseModel instance
        args(list): wont be used.
        kwargs: key name pairs of instance attributes.
        """
        if kwargs and len(kwargs):
            for key in kwargs:
                if key != '__class__':
                    if key in ["created_at", "updated_at"]:
                        setattr(self, key, datetime.strptime(
                            kwargs[key], "%Y-%m-%dT%H:%M:%S.%f"))
                    else:
                        setattr(self, key, kwargs[key])
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self.to_dict())

    def __str__(self):
        """"prints the string rep of a class"""
        return "[" + self.__class__.__name__ + "]" + \
            "(" + self.id + ") " + str(self.__dict__)

    def save(self):
        """method that saves the instance to json"""
        self.updated_at = datetime.now()
        storage.save()


    def to_dict(self):
        """
        method for creating a dict of instance __dict__ keys and values.
        Returns:
            updated_dict(dict): a copy of self.__dict__ .
        """
        updated_dict = {}
        for k, v in self.__dict__.items():
            if k in ["created_at", "updated_at"]:
                updated_dict[k] = datetime.isoformat(v)
            else:
                updated_dict[k] = v
        updated_dict["__class__"] = self.__class__.__name__
        return updated_dict
