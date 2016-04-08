"""All logic of /api/rooms endpoint should be described here."""
import falcon

from mongoengine.errors import NotUniqueError, ValidationError

from makechat.models import Room, Member
from makechat.api.utils import max_body, admin_required


class RoomResource:
    """Chat room resource."""

    @falcon.before(admin_required())
    def on_get(self, req, resp):
        """Process GET requests for /api/rooms."""
        resp.body = Room.objects.to_json()
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
