"""Testing of makechat.api.utils."""
import unittest

from makechat.api.utils import encrypt_password, session_create, token_create
from makechat.models import User, Session, Token


class TestUtils(unittest.TestCase):
    """Testing API utils."""

    @classmethod
    def setUpClass(cls):
        """Standart SetUpClass method of unittest.TestCase."""
        User.drop_collection()  # erase the users collection
        Session.drop_collection()  # erase the sessions collection
        Token.drop_collection()  # erase the tokens collection

        cls.user = User.objects.create(
            username='test', email='test@example.org',
            password=encrypt_password('test'))

    def test_1_session_create(self):
        """Attempt to create session for test user."""
        session_value = session_create(self.user)
        self.assertEqual(session_value,
                         Session.objects.filter(user=self.user)[0].value)

    def test_2_token_create(self):
        """Attempt to create token for test user."""
        token = token_create(self.user, 'test')
        self.assertEqual(token,
                         Token.objects.filter(user=self.user, name='test')[0])

    @classmethod
    def tearDownClass(cls):
        """Standart tearDownClass method of unittest.TestCase."""
        User.drop_collection()  # erase the users collection
        Session.drop_collection()  # erase the sessions collection
        Token.drop_collection()  # erase the tokens collection
