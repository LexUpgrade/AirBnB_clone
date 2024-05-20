#!/usr/bin/python3
"""Test file for <models.place.Place>.
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.user import User
from models.place import Place
from time import sleep


class TestPlaceInstantiation(unittest.TestCase):
    """Testing instantiation of the <Place> class."""

    def test_place_instance(self):
        place = Place()
        place1 = User()
        self.assertIsInstance(place, Place)
        self.assertNotIsInstance(place1, Place)

    def test_instance_in_storage(self):
        place = Place()
        all_objs = models.storage.all()
        self.assertIn(place, all_objs.values())

    def test_id_object_type(self):
        self.assertEqual(type(Place().id), str)

    def test_created_at_object_type(self):
        self.assertEqual(type(Place().created_at), datetime)

    def test_updated_at_object_type(self):
        self.assertEqual(type(Place().updated_at), datetime)

    def test_str_return_value(self):
        plc = Place()
        cls, id, dict = type(plc).__name__, str(plc.id), str(plc.__dict__)
        self.assertIn(cls, str(plc))
        self.assertIn(id, str(plc))
        self.assertIn(dict, str(plc))

    def test_id_in_dict(self):
        d = Place().to_dict()
        self.assertTrue(type(d['id']), str)

    def test_created_at_in_dict(self):
        d = Place().to_dict()
        self.assertTrue(type(d['created_at']), str)

    def test_updated_at_in_dict(self):
        d = Place().to_dict()
        self.assertTrue(type(d['updated_at']), str)

    def test_class_name_in_dict(self):
        d = Place().to_dict()
        self.assertTrue(type(d['__class__']), str)
        self.assertEqual(d['__class__'], 'Place')


class TestPlaceSave(unittest.TestCase):
    """Test the <User.save()> functionality.
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
        plc = Place()
        plc.save()
        with open('file.json') as json_file:
            json_str = json_file.read()
        self.assertIn(plc.id, json_str)

    def test_json_file(self):
        Place().save()
        self.assertTrue(os.path.isfile('file.json'))

    def test_deserialization(self):
        plc = Place()
        id = plc.id
        plc.save()
        with open('file.json') as json_file:
            json_obj = json.load(json_file)
        plc_1 = Place(**json_obj['Place.' + id])
        self.assertEqual(plc.id, plc_1.id)

    def test_updated_at_after_save(self):
        plc = Place()
        updated_at = plc.updated_at
        sleep(0.5)
        plc.save()
        self.assertLess(updated_at, plc.updated_at)


class TestPlaceAttributes(unittest.TestCase):
    """Validates attributes of a <Place> object.
    """
    def test_place_city_id_attr(self):
        self.assertTrue(hasattr(Place(), 'city_id'))

    def test_place_user_id_attr(self):
        self.assertTrue(hasattr(Place(), 'user_id'))

    def test_place_name_attr(self):
        self.assertTrue(hasattr(Place(), 'name'))

    def test_place_description_attr(self):
        self.assertTrue(hasattr(Place(), 'description'))

    def test_place_number_of_rooms_attr(self):
        self.assertTrue(hasattr(Place(), 'number_of_rooms'))

    def test_place_number_bathrooms_attr(self):
        self.assertTrue(hasattr(Place(), 'number_bathrooms'))

    def test_place_max_guest_attr(self):
        self.assertTrue(hasattr(Place(), 'max_guest'))

    def test_place_latitude_attr(self):
        self.assertTrue(hasattr(Place(), 'latitude'))

    def test_place_longitude_attr(self):
        self.assertTrue(hasattr(Place(), 'longitude'))

    def test_place_amenity_ids_attr(self):
        self.assertTrue(hasattr(Place(), 'amenity_ids'))


class TestPlaceAttributeAccessibilityAndType(unittest.TestCase):
    """Test attribute accessibility and type.
    """
    def setUp(self):
        self.plc = Place()

    def test_place_city_id(self):
        self.assertIsInstance(self.plc.city_id, str)

    def test_place_user_id(self):
        self.assertIsInstance(self.plc.user_id, str)

    def test_place_name(self):
        self.assertIsInstance(self.plc.name, str)

    def test_place_description(self):
        self.assertIsInstance(self.plc.description, str)

    def test_place_number_of_rooms(self):
        self.assertIsInstance(self.plc.number_of_rooms, int)

    def test_place_number_bathrooms(self):
        self.assertIsInstance(self.plc.number_bathrooms, int)

    def test_place_max_guest(self):
        self.assertIsInstance(self.plc.max_guest, int)

    def test_place_latitude(self):
        self.assertIsInstance(self.plc.latitude, float)

    def test_place_longitude(self):
        self.assertIsInstance(self.plc.longitude, float)

    def test_place_amenity_ids(self):
        self.assertIsInstance(self.plc.amenity_ids, list)


if __name__ == "__main__":
    unittest.main()
