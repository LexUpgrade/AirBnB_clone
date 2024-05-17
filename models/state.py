#!/usr/bin/python3
"""Defines a class <state>."""
from models.base_model import BaseModel


class State(BaseModel):
    """A class <State> that inherits from <BaseModel>

    Public class attributes:
        name (str): Name of the state
    """

    name = str()
