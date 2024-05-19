#!/usr/bin/python3
"""Test file for <models.city.City>.
"""
import os
import json
import models
import unittest
from models.city import City
from models.user import User
from datetime import datetime
from time import sleep


class TestCityInstantiation(unittest.TestCase):
    """Testing instantiation of the <City> class."""

    def test_city_instance(self):
        ct = City()
        ct1 = User()
        self.assertIsInstance(ct, City)
        self.assertNotIsInstance(ct1, City)

    def test_city_instance_in_storage(self):
        ct = City()
        all_objs = models.storage.all()
        self.assertIn(ct, all_objs.values())

    def test_city_id_object_type(self):
        self.assertEqual(type(City().id), str)

    def test_city_created_at_object_type(self):
        self.assertEqual(type(City().created_at), datetime)

    def test_city_updated_at_object_type(self):
        self.assertEqual(type(City().updated_at), datetime)

    def test_city_str_return_value(self):
        ct = City()
        cls, id, dict = type(ct).__name__, str(ct.id), str(ct.__dict__)
        self.assertIn(cls, str(ct))
        self.assertIn(id, str(ct))
        self.assertIn(dict, str(ct))

    def test_city_id_in_dict(self):
        d = City().to_dict()
        self.assertTrue(type(d['id']), str)

    def test_city_created_at_in_dict(self):
        d = City().to_dict()
        self.assertTrue(type(d['created_at']), str)

    def test_city_updated_at_in_dict(self):
        d = City().to_dict()
        self.assertTrue(type(d['updated_at']), str)

    def test_city_name_in_dict(self):
        d = City().to_dict()
        self.assertTrue(type(d['__class__']), str)
        self.assertEqual(d['__class__'], 'City')


class TestCitySave(unittest.TestCase):
    """Test the <City.save().> functionality.
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

    def test_serialization(self):
        ct = City()
        ct.save()
        with open('file.json') as json_file:
            json_str = json_file.read()
        self.assertIn(ct.id, json_str)

    def test_json_file(self):
        City().save()
        self.assertTrue(os.path.isfile('file.json'))

    def test_deserialization(self):
        ct = City()
        id = ct.id
        ct.save()
        with open('file.json') as json_file:
            json_obj = json.load(json_file)
        ct_1 = City(**json_obj['City.' + id])
        self.assertEqual(ct.id, ct_1.id)

    def test_updated_at_after_save(self):
        ct = City()
        updated_at = ct.updated_at
        sleep(0.5)
        ct.save()
        self.assertLess(updated_at, ct.updated_at)


class TestCityAttributes(unittest.TestCase):
    """Test <City> attribute data type.
    """
    def test_city_state_id_attr(self):
        self.assertTrue(hasattr(City(), 'state_id'))

    def test_city_name_attr(self):
        self.assertTrue(hasattr(City(), 'name'))


class TestCityAttributeAccessibilityAndType(unittest.TestCase):
    """Tests the accessibility and type of a <City> object attributes.
    """
    def setUp(self):
        self.ct = City()

    def test_city_state_id(self):
        self.assertIsInstance(self.ct.state_id, str)

    def test_city_name(self):
        self.assertIsInstance(self.ct.name, str)


if __name__ == "__main__":
    unittest.main()
