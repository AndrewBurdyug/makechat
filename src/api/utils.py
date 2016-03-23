"""All utils are should be placed here."""

import uuid
import hashlib
import falcon

from makechat import config as settings
from makechat.models import Session

SECRET_KEY = settings.get('DEFAULT', 'secret_key')
SESSION_TTL = settings.getint('DEFAULT', 'session_ttl')


def max_body(limit):
    """Max body size hook."""
    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = ('The size of the request is too large. The body must not '
                   'exceed ' + str(limit) + ' bytes in length.')

            raise falcon.HTTPRequestEntityTooLarge(
                'Request body is too large', msg)
    return hook


def encrypt_password(password):
    """Encrypt plain passowrd."""
    return hashlib.sha256(
        password.encode('ascii') + SECRET_KEY.encode('ascii')
    ).hexdigest()


def session_create(resp, user):
    """Create session."""
    session = Session()
    session.user = user
    session.value = hashlib.sha256(
        user.username.encode('ascii') +
        uuid.uuid4().hex.encode('ascii')
    ).hexdigest()
    session.save()
    resp.set_cookie('session', session.value, path='/', secure=False,
                    max_age=SESSION_TTL)
