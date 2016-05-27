"""All test of auth should be described here."""

import unittest
import falcon

from falcon import testing
from utils import prepare_request, make_request
from makechat.models import User, Token
from makechat.api import setting_up_api
from makechat.api.utils import encrypt_password, session_create


class TestToken(unittest.TestCase):
    """Test /api/tokens endpoint."""

    @classmethod
    def setUpClass(cls):
        """Standart SetUpClass method of unittest.TestCase."""
        cls.api_tokens_url = 'http://makechat-web/api/tokens'
        cls.api_login_url = 'http://makechat-web/api/login'

        User.drop_collection()  # erase the users collection
        Token.drop_collection()  # erase the tokens collection

        cls.user = User.objects.create(
            username='test', email='test@example.org',
            password=encrypt_password('test'))

        res = make_request(prepare_request(
            cls.api_login_url, {'username': 'test', 'password': 'test'}))
        cls.session = res.headers['set-cookie'].split(';')[0].split('=')[1]

    def test_1_create_token(self):
        """Attempt to create token."""
        res = make_request(prepare_request(
            self.api_tokens_url, {'name': 'token1'}, session=self.session))
        self.assertEqual(res.content.get('name'), 'token1')
        self.assertEqual(res.code, 201)

        res = make_request(prepare_request(
            self.api_tokens_url, {'name': 'token2'}, session=self.session))
        self.assertEqual(res.content.get('name'), 'token2')
        self.assertEqual(res.code, 201)

    def test_2_get_user_tokens(self):
        """Attempt to get user tokens."""
        res = make_request(prepare_request(
            self.api_tokens_url, {}, method='GET', session=self.session))
        self.assertEqual(res.code, 200)
        items = res.content['items']
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['name'], 'token1')
        self.assertEqual(items[0]['user']['$oid'], str(self.user.pk))
        self.assertEqual(items[1]['name'], 'token2')
        self.assertEqual(items[1]['user']['$oid'], str(self.user.pk))

    @classmethod
    def tearDownClass(cls):
        """Standart tearDownClass method of unittest.TestCase."""
        User.drop_collection()  # erase the users collection
        Token.drop_collection()  # erase the tokens collection


class TestAppTokenResource(testing.TestCase):
    """Testing UserRegister application."""

    @classmethod
    def setUpClass(cls):
        """Standart SetUpClass method of unittest.TestCase."""
        User.drop_collection()  # erase the users collection

        cls.user = User.objects.create(
            username='test', email='test@example.org',
            password=encrypt_password('test'))
        cls.session = session_create(cls.user)

    def setUp(self):
        """Standard setUp unittest method."""
        self.api = setting_up_api()
        self.path = '/api/tokens'

    def simulate_request(self, *args, **kwargs):
        """Redefined falcon simulate_request."""
        kwargs.update({'method': args[0], 'path': self.path})
        return super(TestAppTokenResource, self).simulate_request(**kwargs)

    def test_1_create_token_with_empty_request(self):
        """Attempt to create token without any data."""
        resp = self.simulate_post(headers={
            'Cookie': 'session=%s' % self.session,
            'Content-Type': 'application/json', 'Accept': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(resp.json, {
            'title': 'Missing parameter',
            'description': "The 'payload' parameter is required."})

    def test_2_create_token_without_name(self):
        """Attempt to create token without name of token."""
        resp = self.simulate_post(body='{}', headers={
            'Cookie': 'session=%s' % self.session,
            'Content-Type': 'application/json', 'Accept': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(resp.json, {
            'title': 'Missing parameter',
            'description': "The 'name' parameter is required."})

    def test_3_create_token_successfully(self):
        """Attempt to create token successfully."""
        resp = self.simulate_post(body='{"name": "test1"}', headers={
            'Cookie': 'session=%s' % self.session,
            'Content-Type': 'application/json', 'Accept': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_CREATED)
        self.assertEqual(resp.json['name'], 'test1')

        resp = self.simulate_post(body='{"name": "test2"}', headers={
            'Cookie': 'session=%s' % self.session,
            'Content-Type': 'application/json', 'Accept': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_CREATED)
        self.assertEqual(resp.json['name'], 'test2')

    def test_3_get_user_tokens(self):
        """Attempt to get all user tokens."""
        resp = self.simulate_get(headers={
            'Cookie': 'session=%s' % self.session})
        self.assertEqual(resp.status, falcon.HTTP_OK)
        items = resp.json['items']
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['name'], 'test1')
        self.assertEqual(items[1]['name'], 'test2')

    @classmethod
    def tearDownClass(cls):
        """Standart tearDownClass method of unittest.TestCase."""
        User.drop_collection()  # erase the users collection

if __name__ == '__main__':
    unittest.main()
