"""All logic of /api/rooms endpoint should be described here."""

import falcon

from mongoengine.errors import NotUniqueError, ValidationError

from makechat.models import Room, Member
from makechat.api.utils import max_body, login_required, admin_required, \
    make_paginated_response


class RoomResource:
    """Chat room resource."""

    def __init__(self, items_per_page):
        """Standard python __init__ method."""
        self.default_limit = items_per_page

    @falcon.before(login_required())
    def on_get(self, req, resp):
        """Process GET requests for /api/rooms."""
        if req.context['user'].is_superuser:
            rooms = Room.objects.all()
        else:
            rooms = Room.objects.filter(is_visible=True)
        make_paginated_response(req, rooms, self.default_limit)
        resp.status = falcon.HTTP_200

    @falcon.before(admin_required())
    @falcon.before(max_body(1024))
    def on_post(self, req, resp):
        """Process POST requests for /api/rooms."""
        payload = req.context['payload']
        try:
            name = payload['name']
        except KeyError as er:
            raise falcon.HTTPBadRequest('Missing parameter',
                                        'The %s parameter is required.' % er)
        try:
            member = Member.objects.get(
                role='owner', profile=req.context['user'])
        except Member.DoesNotExist:
            member = Member.objects.create(
                role='owner', profile=req.context['user'])
        room_options = {
            'name': name,
            'members': [member]
        }
        # not required option
        is_open = payload.get('is_open')
        if is_open is not None:
            room_options['is_open'] = is_open

        # not required option
        is_visible = payload.get('is_visible')
        if is_visible is not None:
            room_options['is_visible'] = is_visible

        try:
            room = Room.objects.create(**room_options)
        except (NotUniqueError, ValidationError) as er:
            raise falcon.HTTPBadRequest('Error occurred', '%s' % er)

        resp.body = room.to_json()
        resp.status = falcon.HTTP_201

    @falcon.before(admin_required())
    def on_delete(self, req, resp, room_id):
        """Process POST requests for /api/rooms."""
        owner = Member.objects.filter(
            role='owner', profile=req.context['user'])
        Room.objects.filter(members__in=owner, id=room_id).delete()
        resp.status = falcon.HTTP_200
