"""All test of auth should be described here."""

import unittest

from utils import prepare_request, make_request
from makechat.models import User, Room, Member
from makechat.api.utils import encrypt_password


class TestToken(unittest.TestCase):
    """Test /api/rooms endpoint."""

    @classmethod
    def setUpClass(cls):
        """Standart SetUpClass method of unittest.TestCase."""
        cls.api_rooms_url = 'http://makechat-web/api/rooms'
        cls.api_login_url = 'http://makechat-web/api/login'

        User.drop_collection()  # erase the users collection
        Room.drop_collection()  # erase the rooms collection

        cls.user = User.objects.create(
            username='test', email='test@example.org',
            password=encrypt_password('test'))

        cls.admin = User.objects.create(
            username='admin', email='admin@example.org',
            password=encrypt_password('admin'), is_superuser=True)

        res = make_request(prepare_request(
            cls.api_login_url, {'username': 'test', 'password': 'test'}))
        cls.user_session = res.headers['set-cookie'] \
            .split(';')[0].split('=')[1]

        res = make_request(prepare_request(
            cls.api_login_url, {'username': 'admin', 'password': 'admin'}))
        cls.admin_session = res.headers['set-cookie'] \
            .split(';')[0].split('=')[1]

    def test_1_create_room_without_admin_permissions(self):
        """Attempt to create room without admin permissions."""
        res = make_request(prepare_request(
            self.api_rooms_url, {'name': 'room1'}, session=self.user_session))
        self.assertEqual(res.code, 403)

    def test_2_create_room_wit_admin_permissions(self):
        """Attempt to create room with admin permissions."""
        res = make_request(prepare_request(
            self.api_rooms_url, {'name': 'room1'}, session=self.admin_session))
        self.assertEqual(res.code, 201)
        self.assertEqual(res.content.get('name'), 'room1')
        self.assertEqual(res.content.get('members'), [
            {
                '$oid': str(
                    Member.objects.get(profile=self.admin, role='owner').id)
            }
        ])

        res = make_request(prepare_request(
            self.api_rooms_url, {'name': 'room2'}, session=self.admin_session))
        self.assertEqual(res.code, 201)
        self.assertEqual(res.content.get('name'), 'room2')
        self.assertEqual(res.content.get('members'), [
            {
                '$oid': str(
                    Member.objects.get(profile=self.admin, role='owner').id)
            }
        ])

    def test_3_get_all_rooms(self):
        """Attempt to get all rooms."""
        res = make_request(prepare_request(
            self.api_rooms_url, {}, method='GET', session=self.admin_session))
        self.assertEqual(res.code, 200)
        self.assertEqual([
            x['name'] for x in res.content['items']], ['room1', 'room2'])

    @classmethod
    def tearDownClass(cls):
        """Standart tearDownClass method of unittest.TestCase."""
        User.drop_collection()  # erase the users collection
        Room.drop_collection()  # erase the rooms collection


if __name__ == '__main__':
    unittest.main()
