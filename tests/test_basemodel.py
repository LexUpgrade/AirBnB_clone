#!/usr/bin/python3
"""Test module for <BaseModel> class
"""
import unittest
from models.base_model import BaseModel
from datetime import datetime


class TestBaseModelInstances(unittest.TestCase):
    """A Test case for validating all the instances of all attributes
    of an object <BaseModel."""

    def setUp(self):
        """Creates an instance of <BaseModel> for unittesting."""

        self.my_model = BaseModel()

    def tearDown(self):
        """TearDown mothed for clearing up memory used by <setUp>
        method.
        """

        del self.my_model

    def test_objectInstance(self):
        """Checks if an instance declared by <setUp> is a <BaseModel>
        object.
        """

        self.assertIsInstance(self.my_model, BaseModel)

    def test_idInstance(self):
        """Checks if the attribute <id> of an instance <BaseModel>
        is a string.
        """

        self.assertIsInstance(self.my_model.id, str)

    def test_created_atInstance(self):
        """Checks if the attribute <created_at> of instance
        <self.my_model> is type <datetime>.
        """

        self.assertIsInstance(self.my_model.created_at, datetime)

    def test_updated_atInstance(self):
        """Checks if the attribute <updated_at> of instnace <self.my_model> is
        type <datetime>.
        """

        self.assertIsInstance(self.my_model.updated_at, datetime)

    def test__str__Instance(self):
        """Checks if the return object of <str(self.my_model)> is type str."""

        self.assertIsInstance(str(self.my_model), str)

    def test_to_dictInstance(self):
        """Checks if the return object of <self.my_model.to_dict()> is type
        <dict>.
        """

        self.assertIsInstance(self.my_model.to_dict(), dict)

    def test_dictInstances(self):
        """Validates if all the items of <self.my_model.to_dict()> are type
        <str>.
        """

        obj_dict = self.my_model.to_dict()

        self.assertIsInstance(obj_dict['id'], str)
        self.assertIsInstance(obj_dict['created_at'], str)
        self.assertIsInstance(obj_dict['updated_at'], str)
        self.assertIsInstance(obj_dict['__class__'], str)


class TestDictContents(unittest.TestCase):
    """Test case on <self.my_model.to_dict()>."""

    def setUp(self):
        """Set up all neccessary protocols for <TestDictContents> unittesting.
        """

        self.my_model = BaseModel()
        self.obj_dict = self.my_model.to_dict()

    def tearDown(self):
        """Clean up the memory space used by <setUp> method."""

        del self.my_model

    def test_validation(self):
        """Validates contents of <self.my_model.to_dict()>."""

        self.assertIn('__class__', self.obj_dict)
        self.assertIn('id', self.obj_dict)
        self.assertIn('created_at', self.obj_dict)
        self.assertIn('updated_at', self.obj_dict)

    def test_className(self):
        """Validates if the '__class__' attribute was correctly inserted."""

        self.assertEqual(self.obj_dict['__class__'], 'BaseModel')

    def test_not_overridden_dict(self):
        """Makes sure that <self.my_model.to_dict()> do not overwrite
        <self.my_model.__dict__>.
        """

        self.assertNotEqual(self.obj_dict, self.my_model.__dict__)

        obj_dict2 = self.my_model.to_dict()
        self.assertEqual(self.obj_dict, obj_dict2)

        self.obj_dict['name'] = "Alexander"
        obj_dict2['name'] = "Marvelous"
        self.assertNotEqual(self.obj_dict['name'], obj_dict2['name'])


if __name__ == "__main__":
    unittest.main()
