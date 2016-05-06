"""All logic of /api/rooms endpoint should be described here."""
import math
import falcon

from mongoengine.errors import NotUniqueError, ValidationError

from makechat.models import Room, Member
from makechat.api.utils import max_body, login_required, admin_required


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

        offset = req.get_param_as_int('offset') or 0
        limit = req.get_param_as_int('limit') or self.default_limit

        # set maximum of limit, prevent huge queries:
        if limit > 100:
            limit = 100

        total = rooms.count()
        items = [x.to_mongo() for x in rooms.skip(offset).limit(limit)]

        req.context['result'] = {
            'status': 'ok',
            'items': items,
            'next_page': '/api/rooms?offset=%d&limit=%d' % (
                offset + limit, limit) if offset + limit < total else None,
            'prev_page': '/api/rooms?offset=%d&limit=%d' % (
                offset - limit, limit) if offset else None,
            'total_pages': '%d' % math.ceil(total / float(limit)),
        }
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

        try:
            room = Room.objects.create(name=name, members=[member])
        except (NotUniqueError, ValidationError) as er:
            raise falcon.HTTPBadRequest('Error occurred', '%s' % er)

        resp.body = room.to_json()
        resp.status = falcon.HTTP_201
