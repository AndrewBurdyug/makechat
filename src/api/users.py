"""All logic of user login/registration is should be described here."""

import hashlib
import falcon

from makechat.models import User
from makechat.api.utils import max_body


class UserRegister:
    """User register API endpoint."""

    @falcon.before(max_body(1024))
    def on_post(self, req, resp):
        """Process POST request from /register.html form."""
        email = req.get_param('email', required=True)
        username = req.get_param('username', required=True)
        password1 = req.get_param('password1', required=True)
        password2 = req.get_param('password2', required=True)

        if password1 != password2:
            raise falcon.HTTPBadRequest('Bad pasword',
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

        User.objects.create(username=username, password=password, email=email)
        resp.status = falcon.HTTP_201


class UserLogin:
    """User login API endpoint."""

    @falcon.before(max_body(1024))
    def on_post(self, req, resp):
        """Process POST request from /login.html form."""
        username = req.get_param('username', required=True)
        password = req.get_param('password', required=True)

        try:
            password = hashlib.sha256(password.encode('ascii')).hexdigest()
        except UnicodeEncodeError:
            raise falcon.HTTPUnauthorized('Bad password symbols',
                                          'Invalid password characters.')

        if not User.objects.filter(username=username, password=password):
            raise falcon.HTTPUnauthorized('Bad login attempt',
                                          'Invalid username or password.')
        resp.status = falcon.HTTP_200
