"""This module contains class BaseModel that defines all common attributes/methods for other classes"""


import uuid
from datetime import datetime

class BaseModel:
    """defines all common attributes/methods for other classes"""

    def __init__(self, *argv, **kwargs):
        """The class constructor initializes the id, created_at, update_at"""

        if kwargs and '__class__' not in kwargs:
            for key, value in kwargs.items():
                if key in ['created_at', 'updated_at']:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
            setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())

            self.created_at = datetime.now()
            self.updated_at = self.created_at

    def save(self):
        """updates the public insatance attribute update_at with the current datetime"""

        self.updated_at = datetime.now()

    def to_dict(self):
        """returns the dictionary containing all key/values of __dict__ of the instance"""

        obj_dict = self.__dict__.copy()

        obj_dict['__class__'] = self.__class__.__name__

        if 'created_at' in obj_dict:
            obj_dict['created_at'] = obj_dict['created_at'].isoformat()

        if 'updated_at' in obj_dict:
            obj_dict['updated_at'] = obj_dict['updated_at'].isoformat()

        return obj_dict

    def __str__(self):
        """should print [<class name>] (<self.id>) <self.__dict__>"""
        return (f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}")
