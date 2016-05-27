"""Testing of makechat.api.middlewares."""
import falcon
import unittest

from falcon import testing
from makechat.api.middlewares import RequireJSON, JSONTranslator, \
    MongoengineObjectsPaginator


class ExampleResource:
    """Simple dummy resource for testing hooks."""

    def on_get(self, req, resp):
        """Process GET requests."""
        if req.query_string == 'set_result':
            req.context['result'] = {'created': 'Fri May 27, 2016'}
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """Process POST requests."""
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp):
        """Process DELETE requests."""
        resp.status = falcon.HTTP_200


class DummyMongoItem:
    """Dummy Mongo item of collection.

    There is one function:
        def to_mongo(self) - is mimic of mongoengine queryset to_mongo func
    """

    def __init__(self, dictionary):
        """Standard python __init__ class method."""
        self.x = dictionary

    def to_mongo(self):
        """Dummy to_mongo function."""
        return self.x


class DummyMongoCollection:
    """Dummy Mongo collection.

    There are functions:
        def skip(self, offset) - is mimic of mongoengine queryset skip func
        def limit(self, limit) - is mimic of mongoengine queryset limit func
        def count(self) - is mimic of mongoengine queryset count func
    """

    def __init__(self, items):
        """Standard python __init__ class method."""
        self.items = items

    def __iter__(self):
        """Magick python __iter__ class method."""
        return iter(self.items)

    def skip(self, offset):
        """Dummy skip function."""
        return DummyMongoCollection(self.items[offset:])

    def limit(self, limit):
        """Dummy limit function."""
        return DummyMongoCollection(self.items[:limit])

    def count(self):
        """Dummy count function."""
        return len(self.items)


class ExamplePaginatedResource:
    """Simple dummy resource for testing hooks."""

    def __init__(self, items_per_page):
        """Standard python __init__ method."""
        self.default_limit = items_per_page

    def on_get(self, req, resp):
        """Process GET requests."""
        items = []
        for x in range(311):
            items.append(DummyMongoItem({'item%d' % x: x}))
        req.context['items'] = DummyMongoCollection(items)
        resp.status = falcon.HTTP_200


api = falcon.API(middleware=[
    RequireJSON(), JSONTranslator(), MongoengineObjectsPaginator()])
api.add_route('/api/test', ExampleResource())
api.add_route('/api/test_pagination', ExamplePaginatedResource(30))


class TestMiddlewares(testing.TestCase):
    """Testing API middlewares."""

    def setUp(self):
        """Standard setUp unittest method."""
        self.api = api
        self.path = '/api/test'
        self.maxDiff = None

    def simulate_request(self, *args, **kwargs):
        """Redefined falcon simulate_request."""
        kwargs.update({'method': args[0], 'path': self.path})
        return super(TestMiddlewares, self).simulate_request(**kwargs)

    def test_1_not_supported_content_type(self):
        """Attempt to make a request with not supported content-type."""
        resp = self.simulate_post()
        self.assertEqual(resp.status, falcon.HTTP_NOT_ACCEPTABLE)

    def test_2_not_accepts_json(self):
        """Attempt to make a request without Accept header."""
        resp = self.simulate_post(headers={'Content-Type': 'text/html'})
        self.assertEqual(resp.status, falcon.HTTP_NOT_ACCEPTABLE)

    def test_3_wrong_accept_header(self):
        """Attempt to make a request with wrong Accept header."""
        resp = self.simulate_post(headers={
            'Content-Type': 'application/json', 'Accept': 'text/html'})
        self.assertEqual(resp.status, falcon.HTTP_NOT_ACCEPTABLE)

    def test_4_empty_request_body(self):
        """Attempt to make a request with empty body (legacy html forms)."""
        resp = self.simulate_post(headers={
            'Content-Type': 'application/json', 'Content-Length': '100',
            'Accept': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(resp.json, {
            'title': 'Empty request body',
            'description': 'A valid JSON document is required.'})

    def test_5_empty_request(self):
        """Attempt to make an empty request."""
        resp = self.simulate_get(headers={
            'Content-Type': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_OK)

    def test_6_json_dumps_result(self):
        """Attempt to make request with req.context['result'], json.dumps ."""
        resp = self.simulate_get(query_string='set_result', headers={
            'Content-Type': 'application/json'})
        self.assertEqual(resp.status, falcon.HTTP_OK)
        self.assertEqual(resp.json, {'created': 'Fri May 27, 2016'})

    def test_7_malformed_json(self):
        """Attempt to make a request with empty body (legacy html forms)."""
        resp = self.simulate_post(body='{a=b}', headers={
            'Content-Type': 'application/json', 'Content-Length': '100',
            'Accept': 'application/json'})
        # self.assertEqual(resp.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(resp.json, {
            'title': 'Malformed JSON',
            'description': 'Expecting property name enclosed in double quotes:'
                           ' line 1 column 2 (char 1)'})

    def test_12_pagination_without_params(self):
        """Attempt to make GET paginated request, default offset and limit."""
        self.path = '/api/test_pagination'
        resp = self.simulate_get(headers={
            'Content-Type': 'application/json', 'Accept': 'application/json'
        })
        self.assertEqual(resp.json, {
            'items': [{'item%d' % x: x} for x in range(30)],
            'next_page': '/api/test_pagination?offset=30&limit=30',
            'prev_page': None,
            'total_pages': '11',
            'status': 'ok',
        })

    def test_12_pagination_with_custom_offset(self):
        """Attempt to make GET paginated request with custom offset."""
        self.path = '/api/test_pagination'
        resp = self.simulate_get(query_string="offset=300", headers={
            'Content-Type': 'application/json', 'Accept': 'application/json'
        })
        self.assertEqual(resp.json, {
            'items': [{'item%d' % x: x} for x in range(300, 311)],
            'next_page': None,
            'prev_page': '/api/test_pagination?offset=270&limit=30',
            'total_pages': '11',
            'status': 'ok',
        })

    def test_12_pagination_with_custom_limit(self):
        """Attempt to make GET paginated request with custom limit."""
        self.path = '/api/test_pagination'
        resp = self.simulate_get(query_string="limit=10", headers={
            'Content-Type': 'application/json', 'Accept': 'application/json'
        })
        self.assertEqual(resp.json, {
            'items': [{'item%d' % x: x} for x in range(10)],
            'next_page': '/api/test_pagination?offset=10&limit=10',
            'prev_page': None,
            'total_pages': '32',
            'status': 'ok',
        })

    def test_12_pagination_with_custom_limit_and_offset(self):
        """Attempt to make GET paginated request with custom limit, offset."""
        self.path = '/api/test_pagination'
        resp = self.simulate_get(query_string="limit=10&offset=42", headers={
            'Content-Type': 'application/json', 'Accept': 'application/json'
        })
        self.assertEqual(resp.json, {
            'items': [{'item%d' % x: x} for x in range(42, 52)],
            'next_page': '/api/test_pagination?offset=52&limit=10',
            'prev_page': '/api/test_pagination?offset=32&limit=10',
            'total_pages': '32',
            'status': 'ok',
        })

    def test_12_pagination_with_huge_limit(self):
        """Attempt to make GET paginated request with huge limit > 100."""
        self.path = '/api/test_pagination'
        resp = self.simulate_get(query_string="limit=10000", headers={
            'Content-Type': 'application/json', 'Accept': 'application/json'
        })
        self.assertEqual(resp.json, {
            'items': [{'item%d' % x: x} for x in range(100)],
            'next_page': '/api/test_pagination?offset=100&limit=100',
            'prev_page': None,
            'total_pages': '4',
            'status': 'ok',
        })

if __name__ == '__main__':
    unittest.main()
