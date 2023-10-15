#!/usr/bin/python3
"""This module defines a class FileStorage That will handle deserialization
    and deserialization of objects.
"""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.review import Review


class FileStorage():
    """This class initiates an instance of FileStorage
        Attributes:
            filepath(string): private variable for the file path.
            objects(dict): store all objects using id as key
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """function that returns a dict of ids of class members"""
        return FileStorage.__objects

    def new(self, obj):
        """function for adding new object to __object dict"""

        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """function to serialize obj to str and store in file"""
        all_objs = self.all()
        bjs = {bj: all_objs[bj].to_dict () for bj in all_objs.keys()}
        with open(FileStorage.__file_path, "w", encoding='utf-8') \
                as json_file1:
            json.dump(bjs, json_file1)

    def reload(self):
        """deserializes the JSON file to __objects"""

        class_mapping = {
                "BaseModel": BaseModel,
                }

        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for serialized_obj in objdict.values():
                    cls_name = serialized_obj.get("__class__")
                    if cls_name and cls_name in class_mapping:
                        obj_cls = class_mapping[cls_name]
                        del serialized_obj["__class__"]
                        instance = obj_cls(**serialized_obj)
                        self.new(instance)
        except FileNotFoundError:
            return
