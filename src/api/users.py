"""All logic of user login/registration is should be described here."""

import falcon

from mongoengine.errors import ValidationError

from makechat import config as settings
from makechat.models import User, Member, Room
from makechat.api.utils import encrypt_password, session_create
from makechat.api.hooks import max_body, login_required, admin_required

SESSION_TTL = settings.getint('DEFAULT', 'session_ttl')


class UserRegister:
    """User register API endpoint."""

    @falcon.before(max_body(1024))
    def on_post(self, req, resp):
        """Process POST request from /register.html form."""
        try:
            payload = req.context['payload']
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
        session_value = session_create(user)
        resp.set_cookie('session', session_value, path='/', secure=False,
                        max_age=SESSION_TTL)
        resp.status = falcon.HTTP_201


class UserLogin:
    """User login API endpoint."""

    @falcon.before(max_body(1024))
    def on_post(self, req, resp):
        """Process POST request from /login.html form."""
        payload = req.context.get('payload', {})
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
        session_value = session_create(user)
        resp.set_cookie('session', session_value, path='/', secure=False,
                        max_age=SESSION_TTL)
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
        user = req.context['user']
        membership = Member.objects.filter(profile=user)
        rooms = Room.objects.filter(members__in=membership)
        req.context['result'] = {
            'username': user.username,
            'is_superuser': user.is_superuser,
            'have_rooms': bool(rooms)
        }
        resp.status = falcon.HTTP_200


class UserResource:
    """User resource API endpoint."""

    def __init__(self, items_per_page):
        """Standard python __init__ method."""
        self.default_limit = items_per_page

    @falcon.before(admin_required())
    def on_get(self, req, resp):
        """Process GET requests for /api/users."""
        req.context['items'] = User.objects.all().exclude('password')
        resp.status = falcon.HTTP_200
