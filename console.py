#!/usr/bin/python3
"""Defines a class <HBNBCommand>."""
import cmd
import sys


class HBNBCommand(cmd.Cmd):
    """A command interpreter."""

    prompt = "(hbhb) "

    def do_quit(self, arg):
        """Quite command to exit the program.
        """
        return True

    def do_EOF(self, arg):
        """Handles the end-of-file signal.
        """
        print()
        return True

    def emptyline(self):
        """Command to execute if an emptyline was passed."""
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
