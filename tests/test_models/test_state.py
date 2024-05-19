#!/usr/bin/python3
"""Test file for <models.state.State>.
"""
import os
import json
import models
import unittest
from time import sleep
from datetime import datetime
from models.user import User
from models.state import State


class TestStateInstantiation(unittest.TestCase):
    def test_state_instance(self):
        state = State()
        state1 = User()
        self.assertIsInstance(state, State)
        self.assertNotIsInstance(state1, State)

    def test_instance_in_storage(self):
        state = State()
        all_objs = models.storage.all()
        self.assertIn(state, all_objs.values())

    def test_id_object_type(self):
        self.assertEqual(type(State().id), str)

    def test_created_at_object_type(self):
        self.assertEqual(type(State().created_at), datetime)

    def test_updated_at_object_type(self):
        self.assertEqual(type(State().updated_at), datetime)

    def test_str_return_value(self):
        state = State()
        cls, id, dict = type(state).__name__, str(state.id), \
            str(state.__dict__)
        self.assertIn(cls, str(state))
        self.assertIn(id, str(state))
        self.assertIn(dict, str(state))

    def test_created_at_in_dict(self):
        d = State().to_dict()
        self.assertTrue(type(d['created_at']), str)

    def test_updated_at_in_dict(self):
        d = State().to_dict()
        self.assertTrue(type(d['updated_at']), str)

    def test_class_name_in_dict(self):
        d = State().to_dict()
        self.assertTrue(type(d['__class__']), str)


class TestStateSave(unittest.TestCase):

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
        state = State()
        state.save()
        with open('file.json') as j_file:
            j_str = j_file.read()
        self.assertIn(state.id, j_str)

    def test_serialization_file(self):
        State().save()
        self.assertTrue(os.path.isfile('file.json'))

    def test_deserialization(self):
        state = State()
        id = state.id
        state.save()
        with open('file.json') as j_file:
            json_obj = json.load(j_file)
        state1_0 = State(**json_obj['State.' + id])
        self.assertEqual(state1_0.id, state.id)

    def test_created_at_after_save(self):
        state = State()
        updated_at = state.updated_at
        sleep(0.5)
        state.save()
        self.assertLess(updated_at, state.updated_at)


class TestStateAttributes(unittest.TestCase):

    def test_state_name(self):
        self.assertTrue(hasattr(State(), 'name'))


class TestStateAttributeAccessibilityAndType(unittest.TestCase):

    def test_state_name(self):
        self.assertIsInstance(State().name, str)


if __name__ == "__main__":
    unittest.main()
