#!/usr/bin/python3
"""Test file for <models.amenity.Amenity>.
"""
import os
import json
import models
import unittest
from models.place import Place
from models.amenity import Amenity
from datetime import datetime
from time import sleep


class TestAmenityInstantiation(unittest.TestCase):
    """Testing instantiation of the <Amenity> class."""

    def test_amenity_instance(self):
        a = Amenity()
        a1 = Place()
        self.assertIsInstance(a, Amenity)
        self.assertNotIsInstance(a1, Amenity)

    def test_amenity_instance_in_storage(self):
        a = Amenity()
        all_objs = models.storage.all()
        self.assertIn(a, all_objs.values())

    def test_amenity_id_object_type(self):
        self.assertEqual(type(Amenity().id), str)

    def test_amenity_created_at_object_type(self):
        self.assertEqual(type(Amenity().created_at), datetime)

    def test_amenity_updated_at_object_type(self):
        self.assertEqual(type(Amenity().updated_at), datetime)

    def test_amenity_str_return_value(self):
        a = Amenity()
        cls, id, dict = type(a).__name__, str(a.id), str(a.__dict__)
        self.assertIn(cls, str(a))
        self.assertIn(id, str(a))
        self.assertIn(dict, str(a))

    def test_amenity_id_in_dict(self):
        d = Amenity().to_dict()
        self.assertTrue(type(d['id']), str)

    def test_amenity_created_at_in_dict(self):
        d = Amenity().to_dict()
        self.assertTrue(type(d['created_at']), str)

    def test_amenity_updated_at_in_dict(self):
        d = Amenity().to_dict()
        self.assertTrue(type(d['updated_at']), str)

    def test_amenity_name_in_dict(self):
        d = Amenity().to_dict()
        self.assertTrue(type(d['__class__']), str)
        self.assertEqual(d['__class__'], 'Amenity')


class TestAmenitySave(unittest.TestCase):
    """Test the <Amenity.save()> functionality.
    """
    @classmethod
    def setUpClass(cls):
        if os.path.isfile('file.json'):
            os.rename('file.json', 'tmp.json')

    @classmethod
    def tearDownClass(cls):
        if os.path.isfile('file.json'):
            os.remove('file.json')
        if os.path.isfile('tmp.json'):
            os.rename('tmp.json', 'file.json')

    def test_amenity_serialization(self):
        a = Amenity()
        a.save()
        with open('file.json') as json_file:
            json_str = json_file.read()
        self.assertIn(a.id, json_str)

    def test_amenity_json_file(self):
        if os.path.isfile('file.json'):
            os.remove('file.json')
        Amenity().save()
        self.assertTrue(os.path.isfile('file.json'))

    def test_amenity_deserialization(self):
        a = Amenity()
        id = a.id
        a.save()
        with open('file.json') as json_file:
            json_obj = json.load(json_file)
        a1 = Amenity(**json_obj['Amenity.' + id])
        self.assertEqual(a.id, a1.id)

    def test_amenity_updated_at_after_save(self):
        a = Amenity()
        updated_at = a.updated_at
        sleep(0.5)
        a.save()
        self.assertLess(updated_at, a.updated_at)


class TestAmenityAttributes(unittest.TestCase):
    """Validates attributes of a <Amenity> object.
    """
    def test_amenity_name_attr(self):
        self.assertTrue(hasattr(Amenity(), 'name'))


class TestAmenityAttributeAccessibilityAndType(unittest.TestCase):
    """Test the accessibility and type of a <Amenity> object attributes.
    """
    def test_amenity_name(self):
        self.assertIsInstance(Amenity().name, str)


if __name__ == "__main__":
    unittest.main()
