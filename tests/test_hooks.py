"""Testing of makechat.api.hooks."""
import unittest
import falcon
from falcon import testing
from makechat.models import User
from makechat.api.utils import encrypt_password, session_create, token_create
from makechat.api.hooks import admin_required, login_required, max_body, \
    token_required


class ExampleResource:
    """Simple dummy resource for testing hooks."""

    @falcon.before(login_required())
    def on_get(self, req, resp):
        """Process GET requests."""
        resp.status = falcon.HTTP_200

    @falcon.before(admin_required())
    @falcon.before(max_body(1024))
    def on_post(self, req, resp):
        """Process POST requests."""
        resp.status = falcon.HTTP_200

    @falcon.before(token_required())
    def on_delete(self, req, resp):
        """Process DELETE requests."""
        resp.status = falcon.HTTP_200

api = falcon.API()
api.add_route('/api/test', ExampleResource())


class TestHooks(testing.TestCase):
    """Testing API hooks."""

    @classmethod
    def setUpClass(cls):
        """Standart SetUpClass method of unittest.TestCase."""
        User.drop_collection()  # erase the users collection

        cls.user = User.objects.create(
            username='test', email='test@example.org',
            password=encrypt_password('test'))

        cls.admin = User.objects.create(
            username='admin', email='admin@example.org', is_superuser=True,
            password=encrypt_password('admin'))

    def setUp(self):
        """Standard setUp unittest method."""
        self.api = api
        self.path = '/api/test'

    def simulate_request(self, *args, **kwargs):
        """Redefined falcon simulate_request."""
        kwargs.update({'method': args[0], 'path': self.path})
        return super(TestHooks, self).simulate_request(**kwargs)

    def test_1_login_required_unauthorized(self):
        """Attempt to make GET unauthorized request."""
        resp = self.simulate_get()
        self.assertEqual(resp.status, falcon.HTTP_UNAUTHORIZED)

    def test_2_login_required_bad_session(self):
        """Atempt to make GET request with bad session."""
        resp = self.simulate_get(headers={
            'Cookie': 'session=not-existing-or-expired-session'})
        self.assertEqual(resp.status, falcon.HTTP_UNAUTHORIZED)

    def test_3_login_required_session_authorized(self):
        """Attempt to make GET user session authorized request."""
        session = session_create(self.user)
        resp = self.simulate_get(headers={
            'Cookie': 'session=%s' % session})
        self.assertEqual(resp.status, falcon.HTTP_OK)

    def test_4_login_required_token_authorized(self):
        """Attempt to make GET user token authorized request."""
        token = token_create(self.user, 'test')
        resp = self.simulate_get(headers={
            'X-Auth-Token': token.value})
        self.assertEqual(resp.status, falcon.HTTP_OK)

    def test_5_admin_required_unauthorized(self):
        """Attempt to make POST unauthorized request."""
        resp = self.simulate_post(headers={
            'Content-Type': 'application/json', 'Accept': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_UNAUTHORIZED)

    def test_6_admin_required_user_authorized(self):
        """Attempt to make POST user authorized request."""
        user_session = session_create(self.user)
        resp = self.simulate_post(headers={
            'Cookie': 'session=%s' % user_session,
            'Content-Type': 'application/json', 'Accept': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_FORBIDDEN)
        self.assertEqual(resp.json, {'title': 'Permission Denied',
                                     'description': 'Admin required.'})

    def test_7_admin_required_admin_authorized(self):
        """Attempt to make POST admin authorized request."""
        admin_session = session_create(self.admin)
        resp = self.simulate_post(headers={
            'Cookie': 'session=%s' % admin_session,
            'Content-Type': 'application/json', 'Accept': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_OK)

    def test_8_admin_required_admin_authorized_huge_post_data(self):
        """Attempt to make POST admin authorized request with huge data."""
        admin_session = session_create(self.admin)
        resp = self.simulate_post(body=2048 * 'x', headers={
            'Cookie': 'session=%s' % admin_session,
            'Content-Type': 'application/json', 'Accept': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_REQUEST_ENTITY_TOO_LARGE)

    def test_9_token_required_unauthorized(self):
        """Attempt to make DELETE request without any token."""
        resp = self.simulate_delete()
        self.assertEqual(resp.status, falcon.HTTP_UNAUTHORIZED)

    def test_10_token_required_with_bad_token(self):
        """Attempt to make DELETE request with bad token."""
        resp = self.simulate_delete(headers={
            'X-Auth-Token': 'not-existing-or-disabled-token'})
        self.assertEqual(resp.status, falcon.HTTP_UNAUTHORIZED)

    def test_11_token_required_authorized(self):
        """Attempt to make DELETE token authorized request."""
        token = token_create(self.user, 'test')
        resp = self.simulate_delete(headers={
            'X-Auth-Token': token.value})
        self.assertEqual(resp.status, falcon.HTTP_OK)

    @classmethod
    def tearDownClass(cls):
        """Standart tearDownClass method of unittest.TestCase."""
        User.drop_collection()  # erase the users collection

if __name__ == '__main__':
    unittest.main()
