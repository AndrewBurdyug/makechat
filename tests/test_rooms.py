"""All test of auth should be described here."""
import falcon
import unittest

from falcon import testing
from utils import prepare_request, make_request
from makechat.models import User, Room, Member
from makechat.api import setting_up_api
from makechat.api.utils import encrypt_password, session_create


class TestAppRoomResource(testing.TestCase):
    """Testing of RoomResource application."""

    @classmethod
    def setUpClass(cls):
        """Standart SetUpClass method of unittest.TestCase."""
        User.drop_collection()  # erase the users collection
        Room.drop_collection()  # erase the rooms collection

        cls.user = User.objects.create(
            username='test', email='test@example.org',
            password=encrypt_password('test'))
        cls.user_session = session_create(cls.user)

        cls.admin = User.objects.create(
            username='admin', email='admin@example.org', is_superuser=True,
            password=encrypt_password('admin'))
        cls.admin_session = session_create(cls.admin)

        cls.admin2 = User.objects.create(
            username='admin2', email='admin2@example.org', is_superuser=True,
            password=encrypt_password('admin2'))
        cls.admin2_session = session_create(cls.admin2)

        cls.admin3 = User.objects.create(
            username='admin3', email='admin3@example.org', is_superuser=True,
            password=encrypt_password('admin3'))
        cls.admin3_session = session_create(cls.admin3)

    def setUp(self):
        """Standard setUp unittest method."""
        self.api = setting_up_api()
        self.path = '/api/rooms/'
        self.maxDiff = None

    def simulate_request(self, *args, **kwargs):
        """Redefined falcon simulate_request."""
        kwargs.update({'method': args[0], 'path': self.path})
        return super(TestAppRoomResource, self).simulate_request(**kwargs)

    def test1_create_room_with_empty_request(self):
        """Attempt to create room without any data."""
        resp = self.simulate_post(headers={
            'Cookie': 'session=%s' % self.admin_session,
            'Content-Type': 'application/json', 'Accept': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(resp.json, {
            'title': 'Missing parameter',
            'description': "The 'payload' parameter is required."})

    def test_2_create_room_without_name(self):
        """Attempt to create room without name of room."""
        resp = self.simulate_post(body='{}', headers={
            'Cookie': 'session=%s' % self.admin_session,
            'Content-Type': 'application/json', 'Accept': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(resp.json, {
            'title': 'Missing parameter',
            'description': "The 'name' parameter is required."})

    def test_3_create_room_successfully(self):
        """Attempt to create room successfully."""
        resp = self.simulate_post(body='{"name": "test1"}', headers={
            'Cookie': 'session=%s' % self.admin_session,
            'Content-Type': 'application/json', 'Accept': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_CREATED)
        self.assertEqual(resp.json['name'], 'test1')

        resp = self.simulate_post(body='{"name": "test2"}', headers={
            'Cookie': 'session=%s' % self.admin_session,
            'Content-Type': 'application/json', 'Accept': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_CREATED)
        self.assertEqual(resp.json['name'], 'test2')

        resp = self.simulate_post(body='{"name": "admin2_room"}', headers={
            'Cookie': 'session=%s' % self.admin2_session,
            'Content-Type': 'application/json', 'Accept': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_CREATED)
        self.assertEqual(resp.json['name'], 'admin2_room')

    def test_4_create_room_with_is_open_param(self):
        """Attempt to create room with is_open param."""
        resp = self.simulate_post(
            body='{"is_open": false, "name": "test3"}',
            headers={
                'Cookie': 'session=%s' % self.admin_session,
                'Content-Type': 'application/json',
                'Accept': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_CREATED)
        self.assertEqual(resp.json['name'], 'test3')
        self.assertEqual(resp.json['is_open'], False)

    def test_5_create_room_with_is_visible_param(self):
        """Attempt to create room with is_visible param."""
        resp = self.simulate_post(
            body='{"is_visible": false, "name": "test4"}',
            headers={
                'Cookie': 'session=%s' % self.admin_session,
                'Content-Type': 'application/json',
                'Accept': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_CREATED)
        self.assertEqual(resp.json['name'], 'test4')
        self.assertEqual(resp.json['is_visible'], False)

    def test_6_create_room_with_mongo_validation_error(self):
        """Attempt to create room and get mongo validation error."""
        very_big_room_name = 300 * 'x'
        resp = self.simulate_post(
            body='{"is_visible": false, "name": "%s"}' % very_big_room_name,
            headers={
                'Cookie': 'session=%s' % self.admin_session,
                'Content-Type': 'application/json',
                'Accept': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(resp.json, {
            'title': 'Error occurred',
            'description': "ValidationError (Room:None) (String value is "
            "too long: ['name'])"})

    def test_7_get_rooms_admin(self):
        """Attempt to get rooms superuser account."""
        resp = self.simulate_get(headers={
            'Cookie': 'session=%s' % self.admin_session})
        self.assertEqual(resp.status, falcon.HTTP_OK)
        expected_room_names = [
            'test1', 'test2', 'admin2_room', 'test3', 'test4']
        self.assertEqual(
            [x['name'] for x in resp.json['items']], expected_room_names)

    def test_8_get_rooms_user(self):
        """Attempt to get rooms user account."""
        resp = self.simulate_get(headers={
            'Cookie': 'session=%s' % self.user_session})
        self.assertEqual(resp.status, falcon.HTTP_OK)
        expected_room_names = ['test1', 'test2', 'admin2_room', 'test3']
        self.assertEqual(
            [x['name'] for x in resp.json['items']], expected_room_names)

    def test_91_delete_room(self):
        """Attempt to delete room."""
        room = Room.objects.first()
        self.path = '/api/rooms/%s' % room.pk
        resp = self.simulate_delete(headers={
            'Cookie': 'session=%s' % self.admin_session})
        self.assertEqual(resp.status, falcon.HTTP_OK)
        expected_room_names = ['test2', 'admin2_room', 'test3', 'test4']
        self.assertEqual(
            [x.name for x in Room.objects.all()], expected_room_names)

    def test_9_update_room_with_put(self):
        """Attempt to update room with PUT request."""
        room = Room.objects.first()
        room.name = 'new_room_name'
        self.path = '/api/rooms/%s' % room.pk
        resp = self.simulate_put(
            body=room.to_json(),
            headers={'Content-Type': 'application/json',
                     'Cookie': 'session=%s' % self.admin_session})
        self.assertEqual(resp.status, falcon.HTTP_OK)
        self.assertEqual(resp.json['name'], 'new_room_name')

    def test_9_update_room_with_empty_put(self):
        """Attempt to update room with empty PUT request."""
        room = Room.objects.first()
        room.name = 'new_room_name'
        self.path = '/api/rooms/%s' % room.pk
        resp = self.simulate_put(
            body='{}',
            headers={'Content-Type': 'application/json',
                     'Cookie': 'session=%s' % self.admin_session})
        self.assertEqual(resp.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(resp.json, {
            'title': 'OperationError',
            'description': 'No update parameters, would remove data'})

        resp = self.simulate_put(
            headers={'Content-Type': 'application/json',
                     'Cookie': 'session=%s' % self.admin_session})
        self.assertEqual(resp.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(resp.json, {
            'title': 'Error occurred',
            'description': 'Not found room with id %s' % str(room.pk)})

    def test_9_update_room_with_patch(self):
        """Attempt to update room with PUT request."""
        room = Room.objects.first()
        self.path = '/api/rooms/%s' % room.pk
        resp = self.simulate_patch(
            body='{"name": "new_room"}',
            headers={'Content-Type': 'application/json',
                     'Cookie': 'session=%s' % self.admin_session})
        self.assertEqual(resp.status, falcon.HTTP_OK)
        self.assertEqual(resp.json['name'], 'new_room')

    def test_9_update_room_with_patch_user_not_owner(self):
        """Attempt to update room with PUT request, user is not an owner."""
        room = Room.objects.first()
        self.path = '/api/rooms/%s' % room.pk
        resp = self.simulate_patch(
            body='{"members": []}',
            headers={'Content-Type': 'application/json',
                     'Cookie': 'session=%s' % self.admin2_session})
        self.assertEqual(resp.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(resp.json, {
            'title': 'Error occurred',
            'description': 'You are not owner of this room.'})

        # admin try to update room of admin2
        room = Room.objects.get(name='admin2_room')
        self.path = '/api/rooms/%s' % room.pk
        resp = self.simulate_patch(
            body='{"members": []}',
            headers={'Content-Type': 'application/json',
                     'Cookie': 'session=%s' % self.admin_session})
        self.assertEqual(resp.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(resp.json, {
            'title': 'Error occurred',
            'description': 'You are not owner of this room.'})

        # admin3(not have any room) try to update room of admin2
        room = Room.objects.get(name='admin2_room')
        self.path = '/api/rooms/%s' % room.pk
        resp = self.simulate_patch(
            body='{"members": []}',
            headers={'Content-Type': 'application/json',
                     'Cookie': 'session=%s' % self.admin3_session})
        self.assertEqual(resp.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(resp.json, {
            'title': 'Error occurred',
            'description': 'You are not owner of this room.'})

    @classmethod
    def tearDownClass(cls):
        """Standart tearDownClass method of unittest.TestCase."""
        User.drop_collection()  # erase the users collection
        Room.drop_collection()  # erase the rooms collection


class TestRoomResource(unittest.TestCase):
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
