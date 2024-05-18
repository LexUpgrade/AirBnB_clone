#!/usr/bin/python3
"""Defines a class <User."""
from models.base_model import BaseModel


class User(BaseModel):
    """A <User> class that inherits from <BaseModel>.

    Class Public Attributes:
        email (str): ...
        password (str): ...
        first_name (str): ...
        last_name (str): ...
    """

    email = str()
    password = str()
    first_name = str()
    last_name = str()
