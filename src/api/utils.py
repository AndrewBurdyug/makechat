"""All utils are should be placed here.

This module contain helpers function.

.. py:module:: makechat.api.utils
"""

import uuid
import hashlib

from makechat import config as settings
from makechat.models import Session, Token

SECRET_KEY = settings.get('DEFAULT', 'secret_key')


def encrypt_password(password):
    """Encrypt plain passowrd."""
    return hashlib.sha256(
        password.encode('ascii') + SECRET_KEY.encode('ascii')
    ).hexdigest()


def session_create(user):
    """Create session."""
    session = Session()
    session.user = user
    session.value = hashlib.sha256(
        user.username.encode('ascii') +
        uuid.uuid4().hex.encode('ascii')
    ).hexdigest()
    session.save()
    return session.value


def token_create(user, name):
    """Cretae a token."""
    token = uuid.uuid4().hex
    return Token.objects.create(user=user, value=token, name=name)
