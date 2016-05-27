"""All middlewares should be described here."""
import math
import bson.json_util as json
import falcon


class RequireJSON:
    """Check incoming requests type."""

    error_msg = falcon.HTTPNotAcceptable(
        'This API only supports responses encoded as JSON.',
        href='http://docs.examples.com/api/json')

    def process_request(self, req, resp):
        """Process each request."""
        if not req.content_type:
            raise self.error_msg

        if not req.client_accepts_json:
            raise self.error_msg

        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise self.error_msg


class MongoengineObjectsPaginator:
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

    def process_response(self, req, resp, resource):
        """Process each response."""
        if 'items' not in req.context:
            return

        queryset = req.context['items']
        offset = req.get_param_as_int('offset') or 0
        limit = req.get_param_as_int('limit') or resource.default_limit

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


class JSONTranslator:
    """Process JSON of incoming requests."""

    def process_request(self, req, resp):
        """Process each request."""
        if req.content_length in (None, 0):
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')
        try:
            req.context['payload'] = json.loads(body.decode('utf-8'))
        except Exception as er:
            raise falcon.HTTPError(falcon.HTTP_753, 'Malformed JSON', str(er))

    def process_response(self, req, resp, resource):
        """Process each response."""
        if 'result' in req.context:
            resp.body = json.dumps(req.context['result'])

        if falcon.HTTP_300 >= resp.status >= falcon.HTTP_200:
            if not resp.body:
                resp.body = json.dumps({'status': 'ok'})
