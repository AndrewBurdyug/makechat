"""All mongoengine models are should be described here."""

from mongoengine import connect, Document, StringField, ReferenceField, \
    BooleanField

connect(alias='makechat', host='mongodb://makechat-mongo/makechat')

USER_ROLES = (
    ('admin', 'Superuser'),  # can create chat rooms and manage chat members
    ('owner', 'Chat owner'),  # can read/write and manage chat members
    ('member', 'Chat member'),  # can read/write, but can't manage chat members
    ('guest', 'Chat guest'),  # can read, but can't write
)


class User(Document):
    """Collection of users profiles."""

    email = StringField(required=True, unique=True)
    username = StringField(max_length=120, required=True, unique=True)
    password = StringField(max_length=64, required=True)

    meta = {
        'collection': 'users',
        'db_alias': 'makechat',
        'indexes': ['email', 'username', 'password']
    }


class Room(Document):
    """Collection of chat rooms."""

    name = StringField(max_length=120, required=True, unique=True)
    is_visible = BooleanField(default=True)

    meta = {
        'collection': 'rooms',
        'db_alias': 'makechat',
        'indexes': ['name', 'is_visible']
    }


class Role(Document):
    """Collection of users roles."""

    name = StringField(max_length=10, choices=USER_ROLES, required=True)
    user = ReferenceField(User)
    room = ReferenceField(Room)

    meta = {
        'collection': 'roles',
        'db_alias': 'makechat',
        'indexes': ['name', 'user']
    }
