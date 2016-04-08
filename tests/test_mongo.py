"""Tests of all mongoengine models should be described here."""

import unittest

from bson.objectid import ObjectId
from makechat.models import User


class TestMongo(unittest.TestCase):
    """Test mongoengine models which described in mackechat.models."""

    def test_1_user_create(self):
        """Attempt to create user."""
        User.drop_collection()  # erase the users collection
        user = User.objects.create(
            username='test', email='test@example.org', password='test')
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.password, 'test')
        self.assertEqual(user.email, 'test@example.org')
        self.assertEqual(isinstance(user.id, ObjectId), True)

    @classmethod
    def tearDownClass(cls):
        """Standart tearDown method of unittest.TestCase."""
        User.drop_collection()

if __name__ == '__main__':
    unittest.main()
