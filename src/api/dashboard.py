"""All logic of /api/dashboard endpoint should be described here."""
import falcon
from makechat.api.utils import login_required


class DashboardResource:
    """User dashboard API endpoint."""

    @falcon.before(login_required())
    def on_get(self, req, resp):
        """Process GET requests for /api/dashboard."""
        resp.status = falcon.HTTP_200
