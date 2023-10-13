"""This module contains a class FileStorage that serializes instances to a JSON
file and deserializes JSON file to instances
"""


import json
import os


class FileStorage:
    """serializes instances to a JSON file and deserializes JSON file to instances"""

    def __init__(self, file_path='file.json'):
        """class constructor"""

        self.__file_path = file_path
        self.__objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""

        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj
    
    def save(self):
        """ serializes __objects to the JSON file (path: __file_path)"""
        serialized = {}
        for key, obj in self.__objects.items():
            serialized[key] = obj.to_dict()
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            json.dump(serialized, file, default=str)
    
    def reload(self):
        """deserializes the JSON file to __objects (only if the
        JSON file (__file_path) exists
        """
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r', encoding='utf-8') as file:
                data_str = file.read()
                data = json.loads(data_str)
                for key, obj_data in data.items():
                    class_name, obj_id = key.split('.')
                    class_ = globals().get(class_name)
                    if class_:
                        obj = class_(**obj_data)
                        self.__objects[key] = obj
        return self.__objects
