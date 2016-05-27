"""All logic of /api/tokens endpoint should be described here."""

import falcon

from makechat.models import Token
from makechat.api.utils import token_create
from makechat.api.hooks import max_body, login_required


class TokenResource:
    """Create user token for API access."""

    def __init__(self, items_per_page):
        """Standard python __init__ method."""
        self.default_limit = items_per_page

    @falcon.before(login_required())
    def on_get(self, req, resp):
        """Process GET requests for /api/tokens."""
        user = req.context['user']
        req.context['items'] = Token.objects.filter(user=user)
        resp.status = falcon.HTTP_200

    @falcon.before(login_required())
    @falcon.before(max_body(1024))
    def on_post(self, req, resp):
        """Process POST requests for /api/tokens."""
        user = req.context['user']
        try:
            payload = req.context['payload']
            name = payload['name']
        except KeyError as er:
            raise falcon.HTTPBadRequest('Missing parameter',
                                        'The %s parameter is required.' % er)

        token = token_create(name=name, user=user)
        req.context['result'] = token.to_mongo()
        resp.status = falcon.HTTP_201
