"""Tesing API middlewares."""
import unittest
import falcon
from falcon import testing

from makechat.api import setting_up_api


class TestMiddlewares(testing.TestCase):
    """Testing API middlewares."""

    def setUp(self):
        """Standard setUp unittest method."""
        self.api = setting_up_api()
        self.path = '/api/login'

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

    def test_5_malformed_json(self):
        """Attempt to make a request with empty body (legacy html forms)."""
        resp = self.simulate_post(body='{a=b}', headers={
            'Content-Type': 'application/json', 'Content-Length': '100',
            'Accept': 'application/json'})
        # self.assertEqual(resp.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(resp.json, {
            'title': 'Malformed JSON',
            'description': 'Expecting property name enclosed in double quotes:'
                           ' line 1 column 2 (char 1)'})


if __name__ == '__main__':
    unittest.main()
