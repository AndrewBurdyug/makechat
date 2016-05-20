"""All logic of user login/registration is should be described here."""

import falcon

from mongoengine.errors import ValidationError

from makechat.models import User, Session
from makechat.api.utils import max_body, encrypt_password, session_create, \
    login_required


class UserRegister:
    """User register API endpoint."""

    @falcon.before(max_body(1024))
    def on_post(self, req, resp):
        """Process POST request from /register.html form."""
        payload = req.context['payload']
        try:
            email = payload['email']
            username = payload['username']
            password1 = payload['password1']
            password2 = payload['password2']
        except KeyError as er:
            raise falcon.HTTPBadRequest('Missing parameter',
                                        'The %s parameter is required.' % er)
        if password1 != password2:
            raise falcon.HTTPBadRequest('Bad password',
                                        'Passwords do not match.')
        if User.objects.filter(username=username):
            raise falcon.HTTPBadRequest('Bad username',
                                        'Username is already taken.')
        if User.objects.filter(email=email):
            raise falcon.HTTPBadRequest('Bad email',
                                        'Email is already taken.')
        try:
            password = encrypt_password(password1)
        except UnicodeEncodeError:
            raise falcon.HTTPBadRequest('Bad password symbols',
                                        'Invalid password characters.')
        try:
            user = User.objects.create(
                username=username, password=password, email=email)
        except ValidationError as er:
            raise falcon.HTTPBadRequest('Error of user creation',
                                        '%s' % er.to_dict())
        session_create(resp, user)
        resp.status = falcon.HTTP_201


class UserLogin:
    """User login API endpoint."""

    def on_get(self, req, resp):
        """Process GET requests for /login.html."""
        cookies = req.cookies
        if 'session' not in cookies:
            raise falcon.HTTPUnauthorized('Not authentificated',
                                          'Please login.', 'token')
        if not Session.objects.with_id(cookies['session']):
            raise falcon.HTTPUnauthorized('Not authentificated',
                                          'Please login.', 'token')
        resp.status = falcon.HTTP_200

    @falcon.before(max_body(1024))
    def on_post(self, req, resp):
        """Process POST request from /login.html form."""
        payload = req.context['payload']
        try:
            username = payload['username']
            password = payload['password']
        except KeyError as er:
            raise falcon.HTTPBadRequest('Missing parameter',
                                        'The %s parameter is required.' % er)
        try:
            password = encrypt_password(password)
        except UnicodeEncodeError:
            raise falcon.HTTPUnauthorized('Bad password symbols',
                                          'Invalid password characters.',
                                          'token')
        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            raise falcon.HTTPUnauthorized('Bad login attempt',
                                          'Invalid username or password.',
                                          'token')
        session_create(resp, user)
        resp.status = falcon.HTTP_200


class UserLogout:
    """User logout API endpoint."""

    def on_get(self, req, resp):
        """Process GET /api/logout requests."""
        cookies = req.cookies
        if 'session' in cookies:
            resp.unset_cookie('session')
        resp.status = falcon.HTTP_200


class UserPing:
    """Simple check if user authenticated.

    This is dummy endpoint for periodic lightweight checks.
    """

    @falcon.before(login_required())
    def on_get(self, req, resp):
        """Process GET requests for /api/ping."""
        resp.status = falcon.HTTP_200
