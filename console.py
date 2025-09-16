#!/usr/bin/python3
"""HBNB command interpreter (minimal implementation to satisfy tests)."""

import cmd
import ast
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Place": Place,
        "Amenity": Amenity,
        "Review": Review,
    }

    # ----- basic commands -----
    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def help_quit(self):
        print("Quit command to exit the program.")

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        return True

    def help_EOF(self):
        print("EOF signal to exit the program.")

    def emptyline(self):
        pass

    # ----- create -----
    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        cls_name = args[0]
        if cls_name not in self.classes:
            print("** class doesn't exist **")
            return False
        obj = self.classes[cls_name]()
        storage.new(obj)
        storage.save()
        print(obj.id)
        return False

    def help_create(self):
        print("Usage: create <class>\n        Create a new class instance and print its id.")

    # ----- show -----
    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return False
        if len(args) < 2:
            print("** instance id missing **")
            return False
        key = f"{args[0]}.{args[1]}"
        obj = storage.all().get(key)
        if not obj:
            print("** no instance found **")
            return False
        print(obj)
        return False

    def help_show(self):
        print("Usage: show <class> <id> or <class>.show(<id>)\n        Display the string representation of a class instance of a given id.")

    # ----- destroy -----
    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return False
        if len(args) < 2:
            print("** instance id missing **")
            return False
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return False
        del storage.all()[key]
        storage.save()
        return False

    def help_destroy(self):
        print("Usage: destroy <class> <id> or <class>.destroy(<id>)\n        Delete a class instance of a given id.")

    # ----- all -----
    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        args = arg.split()
        objs = storage.all()
        if len(args) == 0:
            print([str(o) for o in objs.values()])
            return False
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return False
        cl = args[0]
        print([str(o) for k, o in objs.items() if k.startswith(cl + ".")])
        return False

    def help_all(self):
        print("Usage: all or all <class> or <class>.all()\n        Display string representations of all instances of a given class.\n        If no class is specified, displays all instantiated objects.")

    # ----- update -----
    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        # Parse: class, id, and the rest so dictionary payloads remain intact
        args = arg.split(maxsplit=2)
        if len(args) == 0:
            print("** class name missing **")
            return False
        cls = args[0]
        if cls not in self.classes:
            print("** class doesn't exist **")
            return False
        if len(args) < 2:
            print("** instance id missing **")
            return False
        key = f"{cls}.{args[1]}"
        obj = storage.all().get(key)
        if obj is None:
            print("** no instance found **")
            return False
        if len(args) < 3:
            print("** attribute name missing **")
            return False
        rest = args[2].strip()
        # strip any trailing ')' that may appear in space-notation tests
        while rest.endswith(")"):
            rest = rest[:-1].rstrip()
        # dictionary form (space notation): update <Class> <id> {dict}
        if rest.startswith("{") and rest.endswith("}"):
            try:
                updates = ast.literal_eval(rest)
                for k, v in updates.items():
                    setattr(obj, k, v)
                obj.save()
                return False
            except Exception:
                return False
        # split remaining into attr name and value
        parts = rest.split(maxsplit=1)
        if len(parts) < 2:
            print("** value missing **")
            return False
        attr_name = parts[0]
        attr_value = parts[1]
        # coerce numbers if possible
        try:
            if attr_value.isdigit():
                attr_value = int(attr_value)
            else:
                attr_value = float(attr_value)
        except Exception:
            # strip quotes if present
            if ((attr_value.startswith("'") and attr_value.endswith("'")) or
                (attr_value.startswith('"') and attr_value.endswith('"'))):
                attr_value = attr_value[1:-1]
        setattr(obj, attr_name, attr_value)
        obj.save()
        return False

    def help_update(self):
        print("Usage: update <class> <id> <attribute_name> <attribute_value> or\n       <class>.update(<id>, <attribute_name>, <attribute_value>) or\n       <class>.update(<id>, <dictionary>)\n        Update a class instance of a given id by adding or updating\n        a given attribute key/value pair or dictionary.")

    # ----- count -----
    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        args = arg.split()
        if len(args) == 0 or args[0] not in self.classes:
            print("0")
            return False
        cls = args[0]
        n = sum(1 for k in storage.all().keys() if k.startswith(cls + "."))
        print(str(n))
        return False

    def help_count(self):
        print("Usage: count <class> or <class>.count()\n        Retrieve the number of instances of a given class.")

    # ----- dot notation dispatcher -----
    def default(self, line):
        # Expected patterns: Class.command(args)
        try:
            # Handle commands without class before dot
            s = line.strip()
            if s == ".all()":
                return self.do_all("")
            if s.startswith(".show"):
                print("** class name missing **")
                return False
            if s.startswith(".destroy"):
                print("** class name missing **")
                return False
            if s.startswith(".update"):
                print("** class name missing **")
                return False

            if "." not in line or not line.endswith(")"):
                print(f"*** Unknown syntax: {line}")
                return False
            cls, rest = line.split(".", 1)
            cmd_part, arg_part = rest.split("(", 1)
            arg_inner = arg_part[:-1]
            # treat create via dot notation as unknown syntax
            if cmd_part == "create":
                print(f"*** Unknown syntax: {line}")
                return False
            # validate class first
            if cls not in self.classes and cmd_part != "all" and cmd_part != "count":
                print("** class doesn't exist **")
                return False
            if cmd_part == "all":
                return self.do_all(cls)
            if cmd_part == "count":
                return self.do_count(cls)
            if cmd_part in {"show", "destroy"}:
                if not arg_inner:
                    print("** instance id missing **")
                    return False
                return getattr(self, f"do_{cmd_part}")(f"{cls} {arg_inner}")
            if cmd_part == "update":
                if not arg_inner:
                    print("** instance id missing **")
                    return False
                # Verify instance existence first (handle dict/no-comma forms)
                if "{" in arg_inner:
                    instance_id = arg_inner.split("{", 1)[0].strip().rstrip(",")
                else:
                    instance_id = arg_inner.split(",", 1)[0].strip()
                instance_id = instance_id.strip("'\"")
                if storage.all().get(f"{cls}.{instance_id}") is None:
                    print("** no instance found **")
                    return False
                # If dictionary form without comma: <id>{...}
                if "{" in arg_inner and "}" in arg_inner:
                    id_part = arg_inner.split("{", 1)[0].strip().rstrip(",")
                    dict_part = "{" + arg_inner.split("{", 1)[1]
                    return self.do_update(f"{cls} {id_part} {dict_part}")
                parts = arg_inner.split(",", 2)
                parts = [p.strip() for p in parts]
                if len(parts) == 1:
                    print("** attribute name missing **")
                    return False
                if len(parts) == 2:
                    print("** value missing **")
                    return False
                # If second param is a dict (with comma present)
                if parts[1].startswith("{") and parts[1].endswith("}"):
                    return self.do_update(f"{cls} {parts[0]} {parts[1]}")
                return self.do_update(f"{cls} {parts[0]} {parts[1]} {parts[2]}")
            # create via dot notation is invalid per tests
            print(f"*** Unknown syntax: {line}")
            return False
        except Exception:
            print(f"*** Unknown syntax: {line}")
            return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()


