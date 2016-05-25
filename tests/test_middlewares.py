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

    def test_1_not_supported_content_type(self):
        """Attempt to make a request with not supported content-type."""
        resp = self.simulate_post('/api/login')
        self.assertEqual(resp.status, falcon.HTTP_NOT_ACCEPTABLE)

if __name__ == '__main__':
    unittest.main()
