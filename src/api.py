"""Makechat API.

Currently we not doing anything, just run demo_app for tests.
"""
from wsgiref.simple_server import make_server, demo_app


def run_server():
    """Run server."""
    httpd = make_server('', 8000, demo_app)
    print("Serving HTTP on port 8000...")

    # Respond to requests until process is killed

    httpd.serve_forever()
