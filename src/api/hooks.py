"""All falcon hooks should be described here.

All hooks should have apropriate tests before going to production.
Tests:
    tests/test_hooks.py
Docs:
    http://falcon.readthedocs.io/en/stable/api/hooks.html
"""
import falcon
from makechat.models import Token, Session


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


def token_required():
    """Check token hook."""
    def hook(req, resp, resource, params):
        title = 'Auth token required'
        description = ('Please provide an auth token as part of the request.')
        docs_url = 'http://makechat.rtfd.org/api/index.html#read-this-first'
        token = req.get_header('X-Auth-Token')
        if token is None or Token.objects.with_id(token) is None:
            raise falcon.HTTPUnauthorized(
                title, description, 'token', href=docs_url)
    return hook


def login_required():
    """Check auth hook."""
    def hook(req, resp, resource, params):
        cookies = req.cookies
        token_header = req.get_header('X-Auth-Token')
        title = 'Not authentificated'
        description = 'Please provide an auth token or login.'

        if 'session' not in cookies and token_header is None:
            raise falcon.HTTPUnauthorized(title, description, 'token')

        session = Session.objects.with_id(cookies.get('session'))
        token = Token.objects.with_id(token_header)

        if session is None and token is None:
            raise falcon.HTTPUnauthorized(title, description, 'token')

        if session:
            req.context['user'] = session.user

        if token:
            req.context['user'] = token.user

    return hook


def admin_required():
    """Check token hook."""
    def hook(req, resp, resource, params):
        is_authentificated = login_required()
        is_authentificated(req, resp, resource, params)

        if not req.context['user'].is_superuser:
            raise falcon.HTTPForbidden('Permission Denied',
                                       'Admin required.')
    return hook
