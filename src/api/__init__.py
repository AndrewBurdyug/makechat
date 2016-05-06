"""Makechat API core.

All routes or API endpoints should be described here. Also we create WSGI
application here.
"""

import falcon
from makechat.api.users import UserLogin, UserRegister
from makechat.api.tokens import TokenCreate
from makechat.api.rooms import RoomResource
from makechat.api.middlewares import RequireJSON, JSONTranslator
from wsgiref.simple_server import make_server


def run_server(port=8000):
    """Run server."""
    do_login = UserLogin()
    do_register = UserRegister()
    token_create = TokenCreate()
    room_resource = RoomResource(items_per_page=25)

    api = application = falcon.API(
        middleware=[RequireJSON(), JSONTranslator()])

    api.add_route('/api/login', do_login)
    api.add_route('/api/register', do_register)
    api.add_route('/api/tokens', token_create)
    api.add_route('/api/rooms', room_resource)

    httpd = make_server('', port, application)
    print("Serving HTTP on port 8000...")

    # Respond to requests until process is killed

    httpd.serve_forever()
