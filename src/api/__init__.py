"""Makechat API core.

All routes or API endpoints should be described here. Also we create WSGI
application here.
"""

import falcon
from makechat.api.users import UserLogin, UserRegister
from wsgiref.simple_server import make_server


def run_server():
    """Run server."""
    do_login = UserLogin()
    do_register = UserRegister()

    api = application = falcon.API(middleware=[])

    api.add_route('/login', do_login)
    api.add_route('/register', do_register)

    httpd = make_server('', 8000, application)
    print("Serving HTTP on port 8000...")

    # Respond to requests until process is killed

    httpd.serve_forever()