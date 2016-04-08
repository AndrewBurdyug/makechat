=================
API documentation
=================

###############
Read this first
###############

Foremost you need create ``token`` or use already created when you have
completed sign up process. Token is a random phrase with 32 chars(ascii lowercase + digits).
For testing of API access you can use `curl <https://curl.haxx.se/>`_ or `httpie <https://pypi.python.org/pypi/httpie#http-headers>`_
command line tools or anything else which can communicate with server over HTTP protocol.
You should specify your ``token`` in HTTP header ``X-Auth-Token``.

----------------
Playing with API
----------------

Example request with ``curl``::

    $ curl -v -H "X-Auth-Token:4388c735cba9455cae341cbf17ed2198" http://makechat-web/api/rooms
    * Hostname was NOT found in DNS cache
    *   Trying 172.30.1.3...
    * Connected to makechat-web (172.30.1.3) port 80 (#0)
    > GET /api/rooms HTTP/1.1
    > User-Agent: curl/7.35.0
    > Host: makechat-web
    > Accept: */*
    > X-Auth-Token:4388c735cba9455cae341cbf17ed2198
    >
    < HTTP/1.1 200 OK
    * Server nginx/1.9.11 is not blacklisted
    < Server: nginx/1.9.11
    < Date: Thu, 07 Apr 2016 22:13:14 GMT
    < Content-Type: application/json; charset=utf-8
    < Content-Length: 304
    < Connection: keep-alive
    < Cache-Control: max-age=86400, must-revalidate, no-store
    < Vary: Accept-Encoding
    <
    * Connection #0 to host makechat-web left intact
    [{"members": [{"$oid": "5706dac4d55cfe00010944ac"}], "is_open": true, "is_visible": true, "_id": {"$oid": "5706dac4d55cfe00010944ad"}, "name": "room1"}, {"members": [{"$oid": "5706dac4d55cfe00010944ac"}], "is_open": true, "is_visible": true, "_id": {"$oid": "5706dac4d55cfe00010944ae"}, "name": "room2"}]$

or less verbose and more readable::

    $ curl -s -H "X-Auth-Token:4388c735cba9455cae341cbf17ed2198" http://makechat-web/api/rooms| python -m json.tool
    [
        {
            "_id": {
                "$oid": "5706dac4d55cfe00010944ad"
            },
            "is_open": true,
            "is_visible": true,
            "members": [
                {
                    "$oid": "5706dac4d55cfe00010944ac"
                }
            ],
            "name": "room1"
        },
        {
            "_id": {
                "$oid": "5706dac4d55cfe00010944ae"
            },
            "is_open": true,
            "is_visible": true,
            "members": [
                {
                    "$oid": "5706dac4d55cfe00010944ac"
                }
            ],
            "name": "room2"
        }
    ]

or golden mean by using ``httpie``::

    http -v GET http://makechat-web/api/rooms X-Auth-Token:4388c735cba9455cae341cbf17ed2198

**Request:**

.. sourcecode:: http

    GET /api/rooms HTTP/1.1
    Accept: */*
    Accept-Encoding: gzip, deflate
    Connection: keep-alive
    Host: makechat-web
    User-Agent: HTTPie/0.9.3
    X-Auth-Token: 4388c735cba9455cae341cbf17ed2198

**Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Cache-Control: max-age=86400, must-revalidate, no-store
    Connection: keep-alive
    Content-Length: 304
    Content-Type: application/json; charset=utf-8
    Date: Thu, 07 Apr 2016 22:26:12 GMT
    Server: nginx/1.9.11
    Vary: Accept-Encoding

    [
        {
            "_id": {
                "$oid": "5706dac4d55cfe00010944ad"
            },
            "is_open": true,
            "is_visible": true,
            "members": [
                {
                    "$oid": "5706dac4d55cfe00010944ac"
                }
            ],
            "name": "room1"
        },
        {
            "_id": {
                "$oid": "5706dac4d55cfe00010944ae"
            },
            "is_open": true,
            "is_visible": true,
            "members": [
                {
                    "$oid": "5706dac4d55cfe00010944ac"
                }
            ],
            "name": "room2"
        }
    ]


.. note::

    In examples we will use `httpie <https://pypi.python.org/pypi/httpie#http-headers>`_ for interaction with API,
    because it produces beautiful output with indentation aligned of JSON data.

-------------------------
Examples of bad responses
-------------------------
There are many typical mistakes of interaction with API. Do not panic,
just inspect your code one more time and look the API responses more closely:
almost all (except 405 Method Not Allowed error) they have ``title`` and ``description``,
so you can guess what the problem is.

* Request with not valid token or wrong credentials:

    **Request:**

    .. sourcecode:: http

        GET /api/rooms HTTP/1.1
        Accept: */*
        Accept-Encoding: gzip, deflate
        Connection: keep-alive
        Host: makechat-web
        User-Agent: HTTPie/0.9.3
        X-Auth-Token: 4388c735cba9455cae341cbf17ed2191


    **Response:**

    .. sourcecode:: http

        HTTP/1.1 401 Unauthorized
        Connection: keep-alive
        Content-Length: 99
        Content-Type: application/json
        Date: Thu, 07 Apr 2016 22:59:44 GMT
        Server: nginx/1.9.11

        {
            "description": "Please provide an auth token or login.",
            "title": "Not authentificated"
        }

* Request with valid token but without admin permissions (for some actions, you need administrator rights):

    **Request:**

    .. sourcecode:: http

        GET /api/rooms HTTP/1.1
        Accept: */*
        Accept-Encoding: gzip, deflate
        Connection: keep-alive
        Host: makechat-web
        User-Agent: HTTPie/0.9.3
        X-Auth-Token: 52115268596140298df2a640f37eea57

    **Response:**

    .. sourcecode:: http

        HTTP/1.1 403 Forbidden
        Connection: keep-alive
        Content-Length: 74
        Content-Type: application/json
        Date: Thu, 07 Apr 2016 23:01:49 GMT
        Server: nginx/1.9.11

        {
            "description": "Admin required.",
            "title": "Permission Denied"
        }

* Request with not acceptable content type:

    **Request:**

    .. sourcecode:: http

        PUT /api/rooms HTTP/1.1
        Accept: */*
        Accept-Encoding: gzip, deflate
        Connection: keep-alive
        Content-Length: 0
        Host: makechat-web
        User-Agent: HTTPie/0.9.3
        X-Auth-Token: 52115268596140298df2a640f37eea57


    **Response:**

    .. sourcecode:: http

        HTTP/1.1 406 Not Acceptable
        Connection: keep-alive
        Content-Length: 267
        Content-Type: application/json
        Date: Thu, 07 Apr 2016 23:21:38 GMT
        Server: nginx/1.9.11

        {
            "description": "This API only supports responses encoded as JSON.",
            "link": {
                "href": "http://docs.examples.com/api/json",
                "rel": "help",
                "text": "Documentation related to this error"
            },
            "title": "Media type not acceptable"
        }

* Request with not allowed method:

    **Request:**

    .. sourcecode:: http

        PUT /api/rooms HTTP/1.1
        Accept: application/json
        Accept-Encoding: gzip, deflate
        Connection: keep-alive
        Content-Length: 18
        Content-Type: application/json
        Host: makechat-web
        User-Agent: HTTPie/0.9.3
        X-Auth-Token: 52115268596140298df2a640f37eea57

        {
            "data": "test"
        }

    **Response:**

    .. sourcecode:: http

        HTTP/1.1 405 Method Not Allowed
        Connection: keep-alive
        Content-Length: 0
        Date: Thu, 07 Apr 2016 23:22:09 GMT
        Server: nginx/1.9.11
        allow: GET, POST, OPTIONS


* Request without required data:

    **Request:**

    .. sourcecode:: http

        POST /api/rooms HTTP/1.1
        Accept: application/json
        Accept-Encoding: gzip, deflate
        Connection: keep-alive
        Content-Length: 18
        Content-Type: application/json
        Host: makechat-web
        User-Agent: HTTPie/0.9.3
        X-Auth-Token: 4388c735cba9455cae341cbf17ed2198

        {
            "trash": "trash"
        }

    **Response:**

    .. sourcecode:: http

        HTTP/1.1 400 Bad Request
        Connection: keep-alive
        Content-Length: 92
        Content-Type: application/json
        Date: Thu, 07 Apr 2016 23:24:52 GMT
        Server: nginx/1.9.11

        {
            "description": "The 'name' parameter is required.",
            "title": "Missing parameter"
        }



#############
API endpoints
#############

.. toctree::

    endpoints/rooms
    endpoints/members
    endpoints/messages

