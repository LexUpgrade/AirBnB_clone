#!/usr/bin/python3
"""Defines a class <Review>."""
from models.base_model import BaseModel


class Review(BaseModel):
    """A class <Review> that inherits from <BaseModel>.

    Public class attributes:
        place_id (str): ...
        user_id (str): ...
        text (str): ...
    """

    place_id = str()
    user_id = str()
    text = str()
