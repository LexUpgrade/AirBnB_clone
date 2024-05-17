#!/usr/bin/python3
"""Test module for <BaseModel> class
"""
import os
import json
import unittest
from time import sleep
from datetime import datetime
from models.base_model import BaseModel


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


class TestArgsKwargs(unittest.TestCase):

    def setUp(self):
        """Sets up all neccessary protocols for unittesting."""
        self.my_model = BaseModel()
        self.json_dict = self.my_model.to_dict()
        self.new_json = self.json_dict.copy()
        self.new_json['__class__'] = 'ABC_class'
        self.my_model2 = BaseModel(name="Alexander", **self.new_json)

    def tearDown(self):
        """Cleans up memory area used by <setUp> method."""
        del self.my_model
        del self.my_model2
        del self.json_dict
        del self.new_json
        if os.path.isfile("file.json"):
            os.remove("file.json")

    def test_InstanceFromJsonDict(self):
        """Checks if instances from a json document was instantiated
        properly.
        """
        new_model = BaseModel(**self.json_dict)
        self.assertIsInstance(new_model, BaseModel)

    def test_ClassKey(self):
        """Makes sure that <__class__> was never overwritten, even when
        provided.
        """
        json_dict2 = self.my_model2.to_dict()
        self.assertNotEqual(json_dict2['__class__'], 'ABC_class')

    def test_InstancesOfAttrFromJsonDict(self):
        """Checks if all deserialized attributes were instantiated correctly.
        """
        self.assertIsInstance(self.my_model2.id, str)
        self.assertIsInstance(self.my_model2.created_at, datetime)
        self.assertIsInstance(self.my_model2.updated_at, datetime)
        self.assertNotIn('__class__', self.my_model2.__dict__)

    def test_attributeValidations(self):
        """Validates that all attributes passed by <**kwargs> were set
        properly and do exist.
        """
        new_dict = self.my_model2.to_dict()
        for key in self.new_json.keys():
            with self.subTest(key=key):
                self.assertIn(key, self.new_json)


class TestJsonSerializationDeserialization(unittest.TestCase):

    def setUp(self):
        """Sets up all neccessary protocols for unittesting."""
        self.my_model = BaseModel()

    def tearDown(self):
        """Cleans up memory area and facilities used by <setUp> method."""
        del self.my_model
        if os.path.isfile("file.json"):
            os.system("rm file.json")

    def test_FileJsonValidation(self):
        """Checks if <file.json> file was created after ruing <*.save()>.
        """
        self.my_model.save()
        self.assertTrue(os.path.isfile('file.json'))


if __name__ == "__main__":
    unittest.main()
