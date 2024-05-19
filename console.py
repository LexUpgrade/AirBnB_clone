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
        cls_name = re.search(r"\w+\.", arg)
        cmd_arg = re.search(r"\..+\)", arg)
        id_n = re.search(r"\"(.+-){4}[0-9a-z]+\"", arg)
        kwarg = re.search(r", \"[\x00-\x7f]+\)", arg)
        if cmd_arg:
            c_arg = re.search(r"[^.].+\(", cmd_arg.group()).group()[:-1]
            if c_arg in list(command_dict.keys()):
                c = cls_name.group()[:-1]
                if c in self.__commands:
                    args = c
                    if id_n:
                        args += ' ' + id_n.group()[1:-1]
                        if kwarg:
                            args += ' '\
                                    + kwarg.group()[3:].replace("\",", "")[:-1]
                return command_dict[c_arg](args)
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

        lst = list()
        if not arg:
            lst.extend([str(obj) for i, obj in all_objs.items()])
        else:
            if arg not in self.__commands:
                print("** class dosen't exist **")
                return False
            else:
                for k, v in all_objs.items():
                    if k.rsplit(".")[0] == arg:
                        lst.append(str(v))
        print(lst)

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
        obj_keys = [i.split(".")[1] for i in list(all_objs)]

        if len(arg.split()) <= 1:
            if arg:
                if arg in self.__commands:
                    print("** instance id missing **")
                else:
                    print("** class name doesn't exist **")
            else:
                print("** class name missing **")
        elif len(arg.split()) == 2:
            if arg.split()[0] not in self.__commands:
                print("** class name doesn't exist **")
            else:
                if arg.split()[1] not in obj_keys:
                    print("** no instance found **")
                else:
                    print("** attribute name missing **")
        elif len(arg.split()) == 3:
            if arg.split()[0] not in self.__commands:
                print("** class doesn't exist **")
            else:
                if arg.split()[1] not in obj_keys:
                    print("** no instance found **")
                else:
                    print("** value missing **")
        else:
            cls_name, id, key, value = arg.split(' ', 3)
            if cls_name not in self.__commands:
                print("** class name doesn't exist **")
            elif id not in obj_keys:
                print("** no instance found **")
            else:
                k = cls_name + "." + id
                obj = all_objs[k]

                if key not in ['id', 'created_at', 'updated_at']:
                    if value.isdigit():
                        value = int(value)
                    elif len(value.split('.')) == 2 and\
                            all([i.isdigit() for i in value.split('.')]):
                        value = float(value)
                    else:
                        if value[0] == '"' and value[len(value) - 1] == '"':
                            value = value.strip('"')
                        else:
                            value = str(value.split(' ', 1)[0])
                    setattr(obj, key, value)
                    storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
