#!/usr/bin/python3
"""Defines a class <HBNBCommand>."""
import cmd
import sys


class HBNBCommand(cmd.Cmd):
    """A command interpreter."""

    prompt = "(hbhb) "

    def emptyline(self):
        """emptyline command to execute when an emptyline command is passed.
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


if __name__ == "__main__":
    HBNBCommand().cmdloop()
