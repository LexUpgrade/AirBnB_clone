#!/usr/bin/python3
"""Defines a class <HBNBCommand>."""
import re
import cmd
from models import storage
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel


def validateArgs(arg, all_objs, commands):
    """Validates that <arg> passed to the interpreter are valid commands.
    """
    obj_keys = list(all_objs)

    arg_len = len(arg.split())
    if arg_len == 2:
        cls_name = arg.split()[0]
        arg_key = arg.split()[0] + '.' + arg.split()[1]
        if cls_name not in commands:
            print("** class doesn't exist **")
        elif arg_key not in obj_keys:
            print("** no instance found **")
        else:
            return True
    else:
        if arg_len > 2:
            if arg.split()[0] not in commands:
                print("** class doesn't exist **")
            else:
                print("** no instance found **")
        elif arg_len == 1:
            if arg.split()[0] in commands:
                print("** instance id missing **")
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")
    return False


def validateUpdateArgs(arg, ids, commands):
    """Validates <arg> from update.
    """
    if re.search(r"\{.+\}\)$", arg):
        return True

    if len(arg.split()) <= 1:
        if len(arg.split()) == 0:
            print("** class name missing **")
        elif len(arg.split()) == 1:
            if arg in commands:
                print("** instance id missing **")
            else:
                print("** class doesn't exist **")
    elif len(arg.split()) == 2:
        if arg.split()[0] in commands:
            if arg.split()[1] not in ids:
                print("** no instance found **")
            else:
                print("** attribute name missing **")
        else:
            print("** class doesn't exist **")
    elif len(arg.split()) == 3:
        if arg.split()[0] in commands:
            if arg.split()[1] not in ids:
                print("** no instance found **")
            else:
                print("** value missing **")
        else:
            print("** class doesn't exist **")
    else:
        cls, id, key, value = arg.split(' ', 3)
        if cls not in commands:
            print("** class name doesn't exist **")
        elif id not in ids:
            print("** no instance found **")
        else:
            return True
    return False


def argToDict(arg):
    """Returns a dictionary of key/word arguments.
    """
    dictionary, tmp_dict, cls, id = {}, {}, None, None
    dt = re.search(r"\{.+\}", arg)
    if dt:
        cls, id, dict = arg.split(' ', 2)
        dict = dict.strip("{}")
        dict = dict.replace(", \"", "*->>\"").replace(", '", "*->>'")
        dict = dict.split("*->>")
        for i in dict:
            k = re.search(r"[\"'].+[\"']:", i).group().rstrip(":")
            v = re.search(r": .+", i).group().lstrip(": ")
            tmp_dict[k] = v
    else:
        cls, id, karg = arg.split(' ', 2)
        key = re.search(r"\".+\" ", karg).group().rstrip()
        value = re.search(r" .+", karg[karg.index('"', 1):]).group().lstrip()
        if value.startswith('"') and value.endswith('"'):
            value = re.search("\".+?\"", value).group()
            tmp_dict[key] = value
        else:
            tmp_dict[key] = value.split()[0].strip(",")

    for k, v in tmp_dict.items():
        ky = k.strip("\"' ")
        if (v.startswith('"') and v.endswith('"')) or\
                (v.startswith("'") and v.endswith("'")):
            dictionary[ky] = str(v.strip("\"'"))
        elif v.isdigit():
            dictionary[ky] = int(v)
        elif len(v.split('.')) == 2 and\
                all([i.isdigit() for i in v.split('.')]):
            dictionary[ky] = float(v)
    return (cls, id, dictionary)


class HBNBCommand(cmd.Cmd):
    """A command interpreter."""

    prompt = "(hbhb) "
    __commands = ['BaseModel', 'User', 'State', 'City', 'Amenity',
                  'Place', 'Review'
                  ]

    def do_quit(self, arg):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """Handles the end-of-file signal
        """
        print("")
        return True

    def emptyline(self):
        """Command to execute when an emptyline is read.
        """
        pass

    def default(self, arg):
        """Default behaviour for invalid commands.
        """
        command_dict = {
                'all': self.do_all,
                'count': self.do_count,
                'show': self.do_show,
                'destroy': self.do_destroy,
                'update': self.do_update
                }
        args = None
        cnd = re.search(r"\..+\(.*\)", arg)
        cls_name = re.search(r"\w+\.", arg)
        id_n = re.search(r"\(\".+\"", arg)
        kwarg = re.search(r"\".+\",? .+\)", arg)
        if cnd:
            cnd = re.search(r"\..+\(", arg)
            cnd = cnd.group()[1:-1]
            if cnd in list(command_dict.keys()):
                cls_name = cls_name.group()[:-1]
                if cls_name in self.__commands:
                    args = cls_name
                    if id_n:
                        idx = id_n.group().index('"', 2)
                        id = id_n.group()[2:idx]
                        args += ' ' + id
                        if kwarg:
                            kw = kwarg.group()[idx + 1:].strip("), ")
                            args += ' ' + kw
                return command_dict[cnd](args)
        print(f"*** Unknown syntax: {arg}")
        return False

    def help_create(self):
        h_str = "".join(["Creates a new instance of <BaseModel>, ",
                         "saves it to a JSON file 'file.json' and ",
                         "prints the <id> of the instance.\n"
                         ])
        print(h_str)

    def complete_create(self, text, line, beidx, enidx):
        if text:
            complete = [c for c in self.__commands if c.startswith(text)]
        else:
            complete = self.__commands.copy()
        return complete

    def do_create(self, arg):
        if not arg:
            print("** class name missing **")
        elif arg not in self.__commands:
            print("** class dosen't exist **")
        else:
            cls_name = arg + "()"
            my_model = eval(cls_name)
            my_model.save()
            print(my_model.id)

    def help_show(self):
        h_str = "".join(["Prints the string presentation of an instance ",
                         "based on the class name and <id>.\n"
                         ])
        print(h_str)

    def complete_show(self, text, line, beidx, enidx):
        if text:
            complete = [c for c in self.__commands if c.startswith(text)]
        else:
            complete = self.__commands.copy()
        return complete

    def do_show(self, arg):
        all_objs = storage.all()
        if validateArgs(arg, all_objs, self.__commands.copy()):
            key = ".".join(arg.split())
            print(all_objs[key])

    def help_destroy(self):
        h_str = "".join(["Deletes an instance based on the class name ",
                         "and id and also save the changes.\n"
                         ])
        print(h_str)

    def complete_destroy(self, text, line, beidx, enidx):
        if text:
            complete = [c for c in self.__commands if c.startswith(text)]
        else:
            complete = self.commands.copy()
        return complete

    def do_destroy(self, arg):
        all_objs = storage.all()
        if validateArgs(arg, all_objs, self.__commands.copy()):
            key = ".".join(arg.split())
            del all_objs[key]
            storage.save()
            storage.reload()

    def help_all(self):
        h_str = "".join(["Prints all string representation of all ",
                         "instances based or not on the class name.",
                         "\n(ex: '$ destroy BaseModel 121212' or '$ all'.\n"
                         ])
        print(h_str)

    def complete_all(self, text, line, beidx, enidx):
        if text:
            complete = [c for c in self.__commands if c.startswith(text)]
        else:
            complete = self.__commands.copy()
        return complete

    def do_all(self, arg):
        all_objs = storage.all()

        objects = list()
        if not arg:
            objects.extend([str(obj) for i, obj in all_objs.items()])
        else:
            arg = arg.split()[0]
            if arg not in self.__commands:
                print("** class dosen't exist **")
                return False
            else:
                for k, v in all_objs.items():
                    if k.rsplit(".")[0] == arg:
                        objects.append(str(v))
        print(objects)

    def help_count(self):
        h_str = "".join(["Prints the number of a specified object ",
                         "in memory."
                         ])
        print(h_str)

    def complete_count(self, text, line, beidx, enidx):
        if text:
            complete = [i for i in self.__commands if i.startswith(text)]
        else:
            complete = self.__commands.copy()
        return complete

    def do_count(self, arg):
        all_objs = storage.all()

        lst = list()
        if arg is None:
            print("** class name missing **")
        elif arg not in self.__commands:
            print("** class doesn't exist **")
        else:
            lst.extend([i for i in all_objs.keys() if i.startswith(arg)])
            print(len(lst))

    def help_update(self):
        h_str = "".join(["Updates an instance based on the class name ",
                         "and id by adding or updating attributes and ",
                         "also updates the JSON file <file.json>.\n"
                         ])
        print(h_str)

    def complete_update(self, text, line, beidx, enidx):
        if text:
            complete = [c for c in self.__commands if c.startswith(text)]
        else:
            complete = self.__commands.copy()
        return complete

    def do_update(self, arg):
        all_objs = storage.all()
        ids = [i.split(".")[1] for i in list(all_objs.keys())]
        cls, id, dictionary = None, None, None

        if validateUpdateArgs(arg, ids, self.__commands):
            cls, id, dictionary = argToDict(arg)
        else:
            return False

        obj = all_objs[cls + '.' + id]
        for key, value in dictionary.items():
            setattr(obj, str(key), value)
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
