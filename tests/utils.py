"""All tests utils should be described here."""

import json
import urllib.request
import urllib.error


def prepare_request(url, data, method='POST', is_json=True, session=None):
    """Prepare urllib.request.Request object."""
    headers = {}
    if is_json:
        headers.update({'Content-Type': 'application/json'})
        data = json.dumps(data).encode('ascii')
    else:
        data = data.encode('ascii')
    if session:
        headers.update({'Cookie': 'session=%s' % session})
    return urllib.request.Request(url, data, headers, method=method)


def get_content(res):
    """Decode JSON response data to dict."""
    data = res.read().decode('ascii')
    print(data)
    if data:
        return json.loads(data)
    return {}


def make_request(req):
    """Prepare prepared request."""
    try:
        res = urllib.request.urlopen(req)
    except (urllib.error.URLError, urllib.error.HTTPError) as er:
        res = er
    finally:
        res.content = get_content(res)
        return res
