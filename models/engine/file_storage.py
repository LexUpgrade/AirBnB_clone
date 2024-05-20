#!/usr/bin/python3
"""Define a class <FileStorage>."""
import json
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel


class FileStorage:
    """Serializes instances to JSON file and deserializes JSON file
    to instances.
    """

    __file_path = "file.json"
    __objects = dict()

    def all(self):
        """Returns the dictionary <__objects>."""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in <__objects> the <obj> with the <obj class name.id>."""
        key = obj.__class__.__name__ + "." + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes <__objects> to the JSON file <__file_path>."""
        objects = FileStorage.__objects
        json_dict = {key: value.to_dict() for key, value in objects.items()}
        with open(FileStorage.__file_path, "w") as json_file:
            json.dump(json_dict, json_file)

    def reload(self):
        """Deserializes the JSON file to <__objects>."""
        try:
            with open(FileStorage.__file_path) as json_file:
                json_dict = json.load(json_file)
        except FileNotFoundError:
            return
        else:
            for value in json_dict.values():
                cls = value["__class__"]
                del value["__class__"]
                self.new(eval(cls)(**value))
