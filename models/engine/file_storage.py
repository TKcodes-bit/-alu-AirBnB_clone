#!/usr/bin/python3
"""Defines the FileStorage class."""
import json

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The file path used to store JSON data.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id."""
        ocname = obj.__class__.__name__
        key = "{}.{}".format(ocname, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        odict = FileStorage.__objects
        objdict = {k: v.to_dict() for k, v in odict.items()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objdict, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
            classes = {
                "BaseModel": BaseModel,
                "User": User,
                "State": State,
                "City": City,
                "Place": Place,
                "Amenity": Amenity,
                "Review": Review,
            }
            for o in objdict.values():
                cls_name = o.get("__class__")
                if not cls_name or cls_name not in classes:
                    continue
                data = dict(o)
                del data["__class__"]
                self.new(classes[cls_name](**data))
        except FileNotFoundError:
            pass
