"""Makechat API core.

All routes or API endpoints should be described here. Also we create WSGI
application here.
"""

import falcon
from makechat.api.users import UserLogin, UserLogout, UserRegister, UserPing, \
    UserResource
from makechat.api.tokens import TokenCreate
from makechat.api.rooms import RoomResource
from makechat.api.middlewares import RequireJSON, JSONTranslator, \
    MongoengineObjectsPaginator


def setting_up_api():
    """Setting up API instance."""
    do_login = UserLogin()
    do_logout = UserLogout()
    do_register = UserRegister()
    ping = UserPing()
    token_create = TokenCreate()
    room_resource = RoomResource(items_per_page=25)
    user_resource = UserResource(items_per_page=25)

    api = falcon.API(middleware=[
        RequireJSON(), JSONTranslator(), MongoengineObjectsPaginator()])

    api.add_route('/api/login', do_login)
    api.add_route('/api/logout', do_logout)
    api.add_route('/api/register', do_register)
    api.add_route('/api/tokens', token_create)
    api.add_route('/api/rooms/', room_resource)
    api.add_route('/api/rooms/{room_id}', room_resource)
    api.add_route('/api/users', user_resource)
    api.add_route('/api/ping', ping)
    return api

application = setting_up_api()
