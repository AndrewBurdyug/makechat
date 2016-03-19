"""All test of auth should be described here."""

import hashlib
import unittest

from utils import prepare_request, make_request
from makechat.models import User


class TestLogin(unittest.TestCase):
    """Test /api/login endpoint."""

    @classmethod
    def setUpClass(cls):
        """Standart SetUpClass method of unittest.TestCase."""
        cls.api_url = 'http://makechat-web/api/login'
        User.objects.create(
            username='test', email='test@example.org',
            password=hashlib.sha256('test'.encode('ascii')).hexdigest())

    def test_1_valid_creds(self):
        """Attempt to login with correct credentials."""
        res = make_request(prepare_request(
            self.api_url, {'username': 'test', 'password': 'test'}))
        self.assertEqual(res.code, 200)

    def test_2_invalid_creds(self):
        """Attempt to login with incorrect credentials."""
        # invalid password
        res = make_request(prepare_request(
            self.api_url, {'username': 'test', 'password': 'test1'}))
        self.assertEqual(res.code, 401)

        # invalid username
        res = make_request(prepare_request(
            self.api_url, {'username': 'test1', 'password': 'test'}))
        self.assertEqual(res.code, 401)

        # invalid username and password
        res = make_request(prepare_request(
            self.api_url, {'username': 'test1', 'password': 'test1'}))
        self.assertEqual(res.code, 401)

    @classmethod
    def tearDownClass(cls):
        """Standart tearDownClass method of unittest.TestCase."""
        User.objects.delete()


class TestRegister(unittest.TestCase):
    """Test /api/register endpoint."""

    @classmethod
    def setUpClass(cls):
        """Standart SetUpClass method of unittest.TestCase."""
        cls.api_url = 'http://makechat-web/api/register'

    def test_1_valid_form_data(self):
        """Attempt to register with valid form data."""
        res = make_request(prepare_request(
            self.api_url, {'username': 'test2', 'email': 'test@example.com',
                           'password1': 'test2', 'password2': 'test2'}))
        self.assertEqual(res.code, 201)

    def test_2_valid_form_data_username_exist(self):
        """Attempt to register with valid form data and existing username."""
        res = make_request(prepare_request(
            self.api_url, {'username': 'test2', 'email': 'test@example.com',
                           'password1': 'test2', 'password2': 'test2'}))
        self.assertEqual(res.code, 400)
        self.assertEqual(res.content.get('description'),
                         'Username is already taken.')

    def test_3_valid_form_data_email_exist(self):
        """Attempt to register with valid form data and existing email."""
        res = make_request(prepare_request(
            self.api_url, {'username': 'test3', 'email': 'test@example.com',
                           'password1': 'test3', 'password2': 'test3'}))
        self.assertEqual(res.code, 400)
        self.assertEqual(res.content.get('description'),
                         'Email is already taken.')

    def test_4_invalid_form_data(self):
        """Attempt to register with invalid form data."""
        # username, email, password2 are misssing
        res = make_request(prepare_request(
            self.api_url, {'password1': 'test2'}))
        self.assertEqual(res.code, 400)
        self.assertEqual(res.content.get('title'), 'Missing parameter')

        # email, password2 are misssing
        res = make_request(prepare_request(
            self.api_url, {'username': 'test2', 'password1': 'test2'}))
        self.assertEqual(res.code, 400)
        self.assertEqual(res.content.get('title'), 'Missing parameter')

        # password2 is misssing
        res = make_request(prepare_request(
            self.api_url, {'username': 'test2', 'email': 'test@example.com',
                           'password1': 'test2'}))
        self.assertEqual(res.code, 400)
        self.assertEqual(res.content.get('title'), 'Missing parameter')

        #  Passwords do not match
        res = make_request(prepare_request(
            self.api_url, {'username': 'test2', 'email': 'test@example.com',
                           'password1': 'test2', 'password2': '2222'}))
        self.assertEqual(res.code, 400)
        self.assertEqual(res.content.get('description'),
                         'Passwords do not match.')

    @classmethod
    def tearDownClass(cls):
        """Standart tearDownClass method of unittest.TestCase."""
        User.objects.delete()


if __name__ == '__main__':
    unittest.main()
