"""All utils are should be placed here.

This module contain helpers function.

.. py:module:: makechat.api.utils
"""

import uuid
import math
import hashlib

from makechat import config as settings
from makechat.models import Session, Token

SECRET_KEY = settings.get('DEFAULT', 'secret_key')
SESSION_TTL = settings.getint('DEFAULT', 'session_ttl')


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


def token_create(user, name):
    """Cretae a token."""
    token = uuid.uuid4().hex
    while Token.objects.with_id(token):
        token = uuid.uuid4().hex
    return Token.objects.create(user=user, value=token, name=name)


def make_paginated_response(req, queryset, default_items_per_page):
    """Make paginated response.

    Add paginated items into ``req.context['result']``. Under the hood
    a function will do:

    .. sourcecode:: python

        req.context['result'] = {
            'status': 'ok',
            'items': items,
            'next_page': req.uri + '/?offset=%d&limit=%d' % (
                offset + limit, limit) if offset + limit < total else None,
            'prev_page': req.uri + '/?offset=%d&limit=%d' % (
                offset - limit, limit) if offset else None,
            'total_pages': '%d' % math.ceil(total / float(limit)),
        }

    See examples usage in:

    :py:func:`makechat.api.rooms.RoomResource.on_get`

    :param req: Falcon req object
    :param queryset: Resource queryset
    :param int default_items_per_page: The default items per page
    """
    offset = req.get_param_as_int('offset') or 0
    limit = req.get_param_as_int('limit') or default_items_per_page

    # set maximum of limit, prevent huge queries:
    if limit > 100:
        limit = 100

    items = [x.to_mongo() for x in queryset.skip(offset).limit(limit)]
    total = queryset.count()

    req.context['result'] = {
        'status': 'ok',
        'items': items,
        'next_page': req.path + '?offset=%d&limit=%d' % (
            offset + limit, limit) if offset + limit < total else None,
        'prev_page': req.path + '?offset=%d&limit=%d' % (
            offset - limit, limit) if offset else None,
        'total_pages': '%d' % math.ceil(total / float(limit)),
    }
