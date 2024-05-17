#!/usr/bin/python3
"""Defines a class <HBNBCommand>."""
import cmd
from models import storage
from models.base_model import BaseModel


def validateArgs(arg, all_objs, commands):
    """Validates that <arg> passed to the interpreter are valid commands.
    """
    obj_keys = list(all_objs)
    id_keys = [i.rsplit('.')[1] for i in obj_keys]

    arg_len = len(arg.split())
    if arg_len == 2:
        cls_name, id_key = arg.split(" ")
        if cls_name not in commands:
            print("** class doesn't exist **")
        elif id_key not in id_keys:
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
    commands = ['BaseModel']

    def emptyline(self):
        """Command to execute when an emptyline is read.
        """
        pass

    def do_quit(self, arg):
        """Quite command to exit the program.
        """
        return True

    def do_EOF(self, arg):
        """Handles the end-of-file signal.
        """
        print()
        return True

    def help_create(self):
        h_str = "".join(["Creates a new instance of <BaseModel>, ",
                         "saves it to a JSON file 'file.json' and ",
                         "prints the <id> of the instance.\n"
                         ])
        print(h_str)

    def complete_create(self, text, line, beidx, enidx):
        if text:
            complete = [c for c in self.commands if c.startswith(text)]
        else:
            complete = self.commands.copy()
        return complete

    def do_create(self, arg):
        if not arg:
            print("** class name missing **")
        elif arg not in self.commands:
            print("** class dosen't exist **")
        else:
            my_model = BaseModel()
            my_model.save()
            print(my_model.id)

    def help_show(self):
        h_str = "".join(["Prints the string presentation of an instance ",
                         "based on the class name and <id>.\n"
                         ])
        print(h_str)

    def complete_show(self, text, line, beidx, enidx):
        if text:
            complete = [c for c in self.commands if c.startswith(text)]
        else:
            complete = self.commands.copy()
        return complete

    def do_show(self, arg):
        all_objs = storage.all()
        if validateArgs(arg, all_objs, self.commands.copy()):
            key = ".".join(arg.split())
            print(all_objs[key])

    def help_destroy(self):
        h_str = "".join(["Deletes an instance based on the class name ",
                         "and id and also save the changes.\n"
                         ])
        print(h_str)

    def complete_destroy(self, text, line, beidx, enidx):
        if text:
            complete = [c for c in self.commands if c.startswith(text)]
        else:
            complete = self.commands.copy()
        return complete

    def do_destroy(self, arg):
        all_objs = storage.all()
        if validateArgs(arg, all_objs, self.commands.copy()):
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
            complete = [c for c in self.commands if c.startswith(text)]
        else:
            complete = self.commands.copy()
        return complete

    def do_all(self, arg):
        all_objs = storage.all()

        if not arg:
            [print(obj) for i, obj in all_objs.items()]
        else:
            if arg not in self.commands:
                print("** class dosen't exist **")
            else:
                for k, v in all_objs.items():
                    if k.rsplit(".")[0] == arg:
                        print(v)

    def help_update(self):
        h_str = "".join(["Updates an instance based on the class name ",
                         "and id by adding or updating attributes and ",
                         "also updates the JSON file <file.json>.\n"
                         ])
        print(h_str)

    def complete_update(self, text, line, beidx, enidx):
        if text:
            complete = [c for c in self.commands if c.startswith(text)]
        else:
            complete = self.commands.copy()
        return complete

    def do_update(self, arg):
        all_objs = storage.all()
        obj_keys = [i.split(".")[1] for i in list(all_objs)]

        if len(arg.split()) <= 1:
            if arg:
                if arg in self.commands:
                    print("** instance id missing **")
                else:
                    print("** class name doesn't exist **")
            else:
                print("** class name missing **")
        elif len(arg.split()) == 2:
            if arg.split()[0] not in self.commands:
                print("** class name doesn't exist **")
            else:
                if arg.split()[1] not in obj_keys:
                    print("** no instance found **")
                else:
                    print("** attribute name missing **")
        elif len(arg.split()) == 3:
            if arg.split()[0] not in self.commands:
                print("** class doesn't exist **")
            else:
                if arg.split()[1] not in obj_keys:
                    print("** no instance found **")
                else:
                    print("** value missing **")
        else:
            cls_name, id, key, value = arg.split(' ', 3)
            if cls_name not in self.commands:
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
