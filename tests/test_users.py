"""Testing of UserResource."""
import falcon
import unittest

from http import cookies
from falcon import testing

from makechat.api import setting_up_api
from makechat.api.utils import encrypt_password
from makechat.models import User


class TestAppUserResource(testing.TestCase):
    """Test UserResource application."""

    @classmethod
    def setUpClass(cls):
        """Standart SetUpClass method of unittest.TestCase."""
        User.drop_collection()  # erase the users collection

        User.objects.create(
            username='test1', email='test1@example.org',
            password=encrypt_password('test1'))

        User.objects.create(
            username='test2', email='test2@example.org', is_disabled=True,
            password=encrypt_password('test2'))

        User.objects.create(
            username='admin', email='admin@example.org', is_superuser=True,
            password=encrypt_password('admin'))

    def setUp(self):
        """Standard setUp unittest method."""
        self.api = setting_up_api()
        self.maxDiff = None

    def test_1_users_get_with_admin_rights(self):
        """Attempt to get users data."""
        resp = self.simulate_post(
            '/api/login', body='{"username": "admin", "password": "admin"}',
            headers={'Content-Type': 'application/json',
                     'Accept': 'application/json'})
        admin_session = cookies.SimpleCookie(
            resp.headers['set-cookie'])['session'].value

        resp = self.simulate_get('/api/users', headers={
            'Cookie': 'session=%s' % admin_session})
        data = resp.json
        users = [x['username'] for x in data['items']]
        self.assertEqual(len(data['items']), 3)
        self.assertIn('test1', users)
        self.assertIn('test2', users)
        self.assertIn('admin', users)

    def test_2_users_get_without_admin_rights(self):
        """Attempt to get users data without admin rights."""
        resp = self.simulate_post(
            '/api/login', body='{"username": "test1", "password": "test1"}',
            headers={'Content-Type': 'application/json',
                     'Accept': 'application/json'})
        user_session = cookies.SimpleCookie(
            resp.headers['set-cookie'])['session'].value

        resp = self.simulate_get('/api/users', headers={
            'Cookie': 'session=%s' % user_session})
        self.assertEqual(resp.status, falcon.HTTP_FORBIDDEN)

    @classmethod
    def tearDownClass(cls):
        """Standart tearDownClass method of unittest.TestCase."""
        User.drop_collection()  # erase the users collection

if __name__ == '__main__':
    unittest.main()
