#!/usr/bin/python3
"""Test file for <models.user.User>.
"""
import os
import json
import unittest
import models
from datetime import datetime
from models.user import User
from models.city import City
from time import sleep


class TestUserInstantiation(unittest.TestCase):
    """Testing instantiation of the User class."""

    def test_user_instance(self):
        user1 = User()
        user2 = City()
        self.assertIsInstance(user1, User)
        self.assertNotIsInstance(user2, User)

    def test_instance_in_storage(self):
        user1 = User()
        all_objs = models.storage.all()
        self.assertIn(user1, all_objs.values())

    def test_id_object_type(self):
        self.assertEqual(type(User().id), str)

    def test_created_at_object_type(self):
        self.assertEqual(type(User().created_at), datetime)

    def test_updated_at_object_type(self):
        self.assertEqual(type(User().updated_at), datetime)

    def test_str_return_value(self):
        usr1 = User()
        cls, id, dicts = type(usr1).__name__, str(usr1.id), str(usr1.__dict__)
        self.assertIn(cls, str(usr1))
        self.assertIn(id, str(usr1))
        self.assertIn(dicts, str(usr1))

    def test_id_in_dict(self):
        d = User().to_dict()
        self.assertTrue(type(d['id']), str)

    def test_created_at_in_dict(self):
        d = User().to_dict()
        self.assertTrue(type(d['created_at']), str)

    def test_updated_at_in_dict(self):
        d = User().to_dict()
        self.assertTrue(type(d['updated_at']), str)

    def test_class_name_in_dict(self):
        d = User().to_dict()
        self.assertTrue(type(d['__class__']), str)
        self.assertEqual(d['__class__'], 'User')


class TestUserSave(unittest.TestCase):
    """Test the save functionality of <save>."""

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
        user1 = User()
        user1.save()
        with open('file.json') as j_file:
            j_str = j_file.read()
        self.assertIn(user1.id, j_str)

    def test_json_file(self):
        User().save()
        self.assertTrue(os.path.isfile('file.json'))

    def test_deserialization(self):
        user1 = User()
        id = user1.id
        user1.save()
        with open('file.json') as j_file:
            json_obj = json.load(j_file)
        user1_0 = User(**json_obj['User.' + id])
        self.assertEqual(user1_0.id, user1.id)

    def test_updated_at_after_save(self):
        usr = User()
        updated_at = usr.updated_at
        sleep(0.5)
        usr.save()
        self.assertLess(updated_at, usr.updated_at)


class TestUserAttributes(unittest.TestCase):
    """Validates attributes of a <User> object.
    """
    def test_user_attr_email(self):
        self.assertTrue(hasattr(User(), 'email'))

    def test_user_attr_password(self):
        self.assertTrue(hasattr(User(), 'password'))

    def test_user_attr_first_name(self):
        self.assertTrue(hasattr(User(), 'first_name'))

    def test_user_attr_last_name(self):
        self.assertTrue(hasattr(User(), 'last_name'))


class TestUserAttributeAccessibilityAndType(unittest.TestCase):
    """Test the accessibility of attributes and their type.
    """
    def setUp(self):
        self.usr = User()

    def test_user_first_name(self):
        self.assertIsInstance(self.usr.first_name, str)

    def test_user_last_name(self):
        self.assertIsInstance(self.usr.last_name, str)

    def test_user_password(self):
        self.assertIsInstance(self.usr.password, str)

    def test_user_email(self):
        self.assertIsInstance(self.usr.email, str)


if __name__ == "__main__":
    unittest.main()
