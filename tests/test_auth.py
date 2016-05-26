"""All test of auth should be described here."""

import json
import unittest
import falcon
from http import cookies
from utils import prepare_request, make_request
from makechat.models import User
from makechat.api.utils import encrypt_password
from falcon import testing
from makechat.api import setting_up_api


class TestAppLogin(testing.TestCase):
    """Test UserLogin application."""

    def setUp(self):
        """Standard setUp unittest method."""
        self.api = setting_up_api()
        self.path = '/api/login'

    def simulate_request(self, *args, **kwargs):
        """Redefined falcon simulate_request."""
        kwargs.update({'method': args[0], 'path': self.path})
        return super(TestAppLogin, self).simulate_request(**kwargs)

    def test_1_missing_username(self):
        """Attempt to login without username."""
        resp = self.simulate_post(
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(resp.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(resp.json, {
            "title": "Missing parameter",
            "description": "The 'username' parameter is required."})

    def test_2_missing_password(self):
        """Attempt to login with username but without password."""
        resp = self.simulate_post(
            body=json.dumps({'username': 'test'}),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(resp.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(resp.json, {
            "title": "Missing parameter",
            "description": "The 'password' parameter is required."})

    def test_3_bad_password_chars(self):
        """Attempt to login with non ascii chars in password."""
        resp = self.simulate_post(
            body='{"username": "пароль", "password": "пароль"}',
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(resp.status, falcon.HTTP_UNAUTHORIZED)
        self.assertEqual(resp.json, {
            "title": "Bad password symbols",
            "description": "Invalid password characters."})

    def test_4_not_existing_user(self):
        """Attempt to login with not existing user."""
        resp = self.simulate_post(
            body='{"username": "not-exist-user", "password": "pass"}',
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(resp.status, falcon.HTTP_UNAUTHORIZED)
        self.assertEqual(resp.json, {
            "title": "Bad login attempt",
            "description": "Invalid username or password."})


class TestAppPing(testing.TestCase):
    """Test UserPing application."""

    def setUp(self):
        """Standard setUp unittest method."""
        self.api = setting_up_api()

        User.objects.create(
            username='test', email='test@example.org',
            password=encrypt_password('test'))

        resp = self.simulate_post(
            '/api/login', body='{"username": "test", "password": "test"}',
            headers={'Content-Type': 'application/json',
                     'Accept': 'application/json'})
        self.session = cookies.SimpleCookie(
            resp.headers['set-cookie'])['session'].value

    def test_1_ping_on_get(self):
        """Attempt to ping API."""
        resp = self.simulate_get('/api/ping', headers={
            'Cookie': 'session=%s' % self.session,
            'Content-Type': 'application/json', 'Accept': 'application/json'})
        self.assertEqual(resp.json['username'], 'test')

    @classmethod
    def tearDownClass(cls):
        """Standart tearDownClass method of unittest.TestCase."""
        User.drop_collection()  # erase the users collection


class TestAppLogout(testing.TestCase):
    """Test UserLogout application."""

    def setUp(self):
        """Standard setUp unittest method."""
        self.api = setting_up_api()

        User.objects.create(
            username='test', email='test@example.org',
            password=encrypt_password('test'))

        resp = self.simulate_post(
            '/api/login', body='{"username": "test", "password": "test"}',
            headers={'Content-Type': 'application/json',
                     'Accept': 'application/json'})
        self.session = cookies.SimpleCookie(
            resp.headers['set-cookie'])['session'].value

    def test_1_logout_on_get(self):
        """Attempt to logout."""
        resp = self.simulate_get('/api/logout', headers={
            'Cookie': 'session=%s' % self.session,
            'Content-Type': 'application/json', 'Accept': 'application/json'})
        print (resp.headers)
        self.assertEqual(resp.status, falcon.HTTP_OK)

    @classmethod
    def tearDownClass(cls):
        """Standart tearDownClass method of unittest.TestCase."""
        User.drop_collection()  # erase the users collection


class TestLogin(unittest.TestCase):
    """Test /api/login endpoint."""

    @classmethod
    def setUpClass(cls):
        """Standart SetUpClass method of unittest.TestCase."""
        cls.api_url = 'http://makechat-web/api/login'
        User.drop_collection()  # erase the users collection
        User.objects.create(
            username='test', email='test@example.org',
            password=encrypt_password('test'))

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
        User.drop_collection()  # erase the users collection


class TestRegister(unittest.TestCase):
    """Test /api/register endpoint."""

    @classmethod
    def setUpClass(cls):
        """Standart SetUpClass method of unittest.TestCase."""
        cls.api_url = 'http://makechat-web/api/register'
        User.drop_collection()  # erase the users collection

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

        #  Bad username string which contains non ASCII chars
        res = make_request(prepare_request(
            self.api_url, {'username': '!!?&', 'email': 'test@ex.com',
                           'password1': 'test2', 'password2': 'test2'}))
        self.assertEqual(res.code, 400)
        self.assertEqual(res.content.get('description'),
                         "{'username': 'String value did not match "
                         "validation regex'}")

        #  Bad username string which contains non ASCII chars
        res = make_request(prepare_request(
            self.api_url, {'username': 'test211', 'email': 'test@a',
                           'password1': 'test2', 'password2': 'test2'}))
        self.assertEqual(res.code, 400)
        self.assertEqual(res.content.get('description'),
                         "{'email': 'Invalid Mail-address: test@a'}")

    @classmethod
    def tearDownClass(cls):
        """Standart tearDownClass method of unittest.TestCase."""
        User.drop_collection()  # erase the users collection


class TestPing(unittest.TestCase):
    """Test /api/ping endpoint."""

    @classmethod
    def setUpClass(cls):
        """Standart SetUpClass method of unittest.TestCase."""
        cls.api_ping_url = 'http://makechat-web/api/ping'
        cls.api_login_url = 'http://makechat-web/api/login'

        User.drop_collection()  # erase the users collection
        User.objects.create(
            username='test', email='test@example.org',
            password=encrypt_password('test'))

        res = make_request(prepare_request(
            cls.api_login_url, {'username': 'test', 'password': 'test'}))
        cls.user_session = res.headers['set-cookie'] \
            .split(';')[0].split('=')[1]

    def test_1_ping_api_user_is_authenticated(self):
        """Attempt to ping api with successful authorization."""
        res = make_request(prepare_request(
            self.api_ping_url, {}, method='GET', session=self.user_session))
        self.assertEqual(res.code, 200)

    @classmethod
    def tearDownClass(cls):
        """Standart tearDownClass method of unittest.TestCase."""
        User.drop_collection()  # erase the users collection

if __name__ == '__main__':
    unittest.main()
