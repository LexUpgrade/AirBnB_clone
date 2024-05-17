#!/usr/bin/python3
"""Defines a class <City>."""
from models.base_model import BaseModel


class City(BaseModel):
    """A class <City> that inherits from <BaseModel>.

    Public class attributes:
        state_id (str): The <id> of a state.
        name (str): Name of the city.
    """

    state_id = str()
    name = str()
