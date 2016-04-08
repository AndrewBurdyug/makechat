##########
/api/rooms
##########

.. http:get:: /api/rooms

    Get all chat rooms.

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

    :statuscode 200: ok
    :statuscode 401: not valid token
    :statuscode 403: not have admin permissions
    :statuscode 405: not allowed method
    :statuscode 406: not acceptable content type

.. http:post:: /api/rooms

    Create a new chat room with given name.

    **Request:**

    .. sourcecode:: http

        POST /api/rooms HTTP/1.1
        Accept: application/json
        Accept-Encoding: gzip, deflate
        Connection: keep-alive
        Content-Length: 21
        Content-Type: application/json
        Host: makechat-web
        User-Agent: HTTPie/0.9.3
        X-Auth-Token: 4388c735cba9455cae341cbf17ed2198

        {
            "name": "test_room"
        }

    **Response:**

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Cache-Control: max-age=86400, must-revalidate, no-store
        Connection: keep-alive
        Content-Length: 154
        Content-Type: application/json; charset=utf-8
        Date: Thu, 07 Apr 2016 23:50:08 GMT
        Server: nginx/1.9.11
        Vary: Accept-Encoding

        {
            "_id": {
                "$oid": "5706f230d55cfe00010944af"
            },
            "is_open": true,
            "is_visible": true,
            "members": [
                {
                    "$oid": "5706dac4d55cfe00010944ac"
                }
            ],
            "name": "test_room"
        }

    :<json string name: the name of chat room
    :>json object _id: ``id`` of chat room
    :>json string name: ``name`` of chat room
    :>json array members: ``members`` of chat room
    :>json boolean is_open: ``true`` if chat room is open
    :>json boolean is_visible: ``true`` if chat room is visible
    :statuscode 201: ok
    :statuscode 400: not have required data
    :statuscode 401: not valid token
    :statuscode 403: not have admin permissions
    :statuscode 405: not allowed method
    :statuscode 406: not acceptable content type
