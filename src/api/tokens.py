"""All logic of /api/tokens endpoint should be described here."""

import falcon

from makechat.models import Session, Token
from makechat.api.utils import max_body, token_create


class TokenCreate:
    """Create user token for API access."""

    def on_get(self, req, resp):
        """Process GET requests for /api/tokens."""
        cookies = req.cookies
        if 'session' not in cookies:
            raise falcon.HTTPUnauthorized('Not authentificated',
                                          'Please login.', 'token')
        session = Session.objects.with_id(cookies['session'])
        if session is None:
            raise falcon.HTTPUnauthorized('Not authentificated',
                                          'Please login.', 'token')
        resp.body = Token.objects.filter(user=session.user).to_json()
        resp.status = falcon.HTTP_200

    @falcon.before(max_body(1024))
    def on_post(self, req, resp):
        """Process POST requests for /api/tokens."""
        cookies = req.cookies
        if 'session' not in cookies:
            raise falcon.HTTPUnauthorized('Not authentificated',
                                          'Please login.', 'token')
        session = Session.objects.with_id(cookies['session'])
        if session is None:
            raise falcon.HTTPUnauthorized('Not authentificated',
                                          'Please login.', 'token')
        payload = req.context['payload']
        try:
            name = payload['name']
        except KeyError as er:
            raise falcon.HTTPBadRequest('Missing parameter',
                                        'The %s parameter is required.' % er)
        token = token_create(name=name, user=session.user)
        resp.body = token.to_json()
        resp.status = falcon.HTTP_201
