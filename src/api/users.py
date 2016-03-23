"""All logic of user login/registration is should be described here."""

import hashlib
import falcon
from mongoengine.errors import ValidationError

from makechat.models import User
from makechat.api.utils import max_body


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
            password = hashlib.sha256(password1.encode('ascii')).hexdigest()
        except UnicodeEncodeError:
            raise falcon.HTTPBadRequest('Bad password symbols',
                                        'Invalid password characters.')
        try:
            User.objects.create(
                username=username, password=password, email=email)
        except ValidationError as er:
            raise falcon.HTTPBadRequest('Error of user creation',
                                        '%s' % er.to_dict())
        resp.status = falcon.HTTP_201


class UserLogin:
    """User login API endpoint."""

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
            password = hashlib.sha256(password.encode('ascii')).hexdigest()
        except UnicodeEncodeError:
            raise falcon.HTTPUnauthorized('Bad password symbols',
                                          'Invalid password characters.')

        if not User.objects.filter(username=username, password=password):
            raise falcon.HTTPUnauthorized('Bad login attempt',
                                          'Invalid username or password.')
        resp.status = falcon.HTTP_200
