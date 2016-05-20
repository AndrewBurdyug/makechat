"""All logic of /api/dashboard endpoint should be described here."""
import falcon
from makechat.api.utils import login_required


class DashboardResource:
    """User dashboard API endpoint."""

    @falcon.before(login_required())
    def on_get(self, req, resp):
        """Process GET requests for /api/dashboard."""
        req.context['result'] = {
            'status': 'ok',
            'items': [
                {'_id': 1, 'name': 'home', 'title': 'Home',
                 'icon': 'large home'},
                {'_id': 2, 'name': 'messages', 'title': 'Messages',
                 'icon': 'comment layout'},
                {'_id': 3, 'name': 'rooms', 'title': 'Rooms',
                 'icon': 'cube layout'},
                {'_id': 5, 'name': 'settings', 'title': 'Settings',
                 'icon': 'setting'},
                {'_id': 6, 'name': 'logout', 'title': 'Sign out',
                 'icon': 'sign out'},
            ]
        }
        user = req.context['user']
        if user.is_superuser:
            req.context['result']['items'].insert(
                3, {'_id': 4, 'name': 'users', 'title': 'Users',
                    'icon': 'users'},
            )
        resp.status = falcon.HTTP_200
