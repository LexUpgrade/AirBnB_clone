#!/usr/bin/python3
"""Test file for <models.review.Review>.
"""
import os
import json
import models
import unittest
from models.user import User
from models.review import Review
from datetime import datetime
from time import sleep


class TestReviewInstantiation(unittest.TestCase):
    """Testing instantiation of the <Review> class."""

    def test_review_instance(self):
        rv = Review()
        rv1 = User()
        self.assertIsInstance(rv, Review)
        self.assertNotIsInstance(rv1, Review)

    def test_review_instance_in_storage(self):
        rv = Review()
        all_objs = models.storage.all()
        self.assertIn(rv, all_objs.values())

    def test_review_id_object_type(self):
        self.assertEqual(type(Review().id), str)

    def test_review_created_at_object_type(self):
        self.assertEqual(type(Review().created_at), datetime)

    def test_review_updated_at_object_type(self):
        self.assertEqual(type(Review().updated_at), datetime)

    def test_review_str_return_value(self):
        rv = Review()
        cls, id, dict = type(rv).__name__, str(rv.id), str(rv.__dict__)
        self.assertIn(cls, str(rv))
        self.assertIn(id, str(rv))
        self.assertIn(dict, str(rv))

    def test_review_id_in_dict(self):
        d = Review().to_dict()
        self.assertTrue(type(d['id']), str)

    def test_review_craeted_at_in_dict(self):
        d = Review().to_dict()
        self.assertTrue(type(d['created_at']), str)

    def test_review_updated_at_in_dict(self):
        d = Review().to_dict()
        self.assertTrue(type(d['updated_at']), str)

    def test_review_class_name_in_dict(self):
        d = Review().to_dict()
        self.assertTrue(type(d['__class__']), str)
        self.assertTrue(d['__class__'], 'Review')


class TestReviewSave(unittest.TestCase):
    """Testing the <Review.save()> functionality.
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

    def test_review_serialization(self):
        rv = Review()
        rv.save()
        with open('file.json') as json_file:
            json_str = json_file.read()
        self.assertIn(rv.id, json_str)

    def test_review_json_file(self):
        Review().save()
        self.assertTrue(os.path.isfile('file.json'))

    def test_review_deserialization(self):
        rv = Review()
        id = rv.id
        rv.save()
        with open('file.json') as json_file:
            json_obj = json.load(json_file)
        rv_1 = Review(**json_obj['Review.' + rv.id])
        self.assertEqual(rv_1.id, rv.id)

    def test_review_updated_at_after_save(self):
        rv = Review()
        updated_at = rv.updated_at
        sleep(0.5)
        rv.save()
        self.assertLess(updated_at, rv.updated_at)


class TestReviewAttributes(unittest.TestCase):
    """Testin the data type of all <Review> object attributes.
    """
    def test_review_place_id_attr(self):
        self.assertTrue(hasattr(Review(), 'place_id'))

    def test_review_user_id_attr(self):
        self.assertTrue(hasattr(Review(), 'user_id'))

    def test_review_text_attr(self):
        self.assertTrue(hasattr(Review(), 'text'))


class TestReviewAttributeAccessibilityAndType(unittest.TestCase):
    """Testing the accessibity and type of a <Review> object attribute.
    """
    def test_review_place_id(self):
        self.assertIsInstance(Review().place_id, str)

    def test_review_user_id(self):
        self.assertIsInstance(Review().user_id, str)

    def test_review_text(self):
        self.assertIsInstance(Review().text, str)


if __name__ == "__main__":
    unittest.main()
