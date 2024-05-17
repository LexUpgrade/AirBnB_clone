#!/usr/bin/python3
"""Defines a class <Amenity>."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """A class <Amenity> that inherits from <BaseModel>.

    Public class attribute:
        name (str): ...
    """

    name = str()
