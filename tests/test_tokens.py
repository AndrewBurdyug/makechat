"""All test of auth should be described here."""

import unittest

from utils import prepare_request, make_request
from makechat.models import User, Token
from makechat.api.utils import encrypt_password


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

    def test_1_get_user_tokens(self):
        """Attempt to get user tokens."""
        res = make_request(prepare_request(
            self.api_tokens_url, {}, method='GET', session=self.session))
        self.assertEqual(res.code, 200)
        self.assertEqual(len(res.content), 2)
        self.assertEqual(res.content[0]['name'], 'token1')
        self.assertEqual(res.content[0]['user']['$oid'], str(self.user.id))
        self.assertEqual(res.content[1]['name'], 'token2')
        self.assertEqual(res.content[1]['user']['$oid'], str(self.user.id))

    @classmethod
    def tearDownClass(cls):
        """Standart tearDownClass method of unittest.TestCase."""
        User.drop_collection()  # erase the users collection
        Token.drop_collection()  # erase the tokens collection

if __name__ == '__main__':
    unittest.main()
