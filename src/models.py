"""All mongoengine models are should be described here."""

from makechat import config as settings
from mongoengine import connect, Document, StringField, ReferenceField, \
    BooleanField, EmailField

connect(alias='makechat', host=settings.get('DEFAULT', 'mongo_uri'))
connect(alias='makechat_test', host=settings.get('DEFAULT', 'test_mongo_uri'))

TEST_MODE = settings.getboolean('DEFAULT', 'test_mode')

USER_ROLES = (
    ('admin', 'Superuser'),  # can create chat rooms and manage chat members
    ('owner', 'Chat owner'),  # can read/write and manage chat members
    ('member', 'Chat member'),  # can read/write, but can't manage chat members
    ('guest', 'Chat guest'),  # can read, but can't write
)


class User(Document):
    """Collection of users profiles."""

    email = EmailField(required=True, unique=True)
    username = StringField(regex=r'[a-zA-Z0-9_-]+$', max_length=120,
                           required=True, unique=True)
    password = StringField(max_length=64, required=True)

    meta = {
        'collection': 'users',
        'db_alias': 'makechat_test' if TEST_MODE else 'makechat',
        'indexes': ['email', 'username', 'password']
    }

    def __str__(self):
        """Standart python magic __str__ method."""
        return self.username


class Room(Document):
    """Collection of chat rooms."""

    name = StringField(max_length=120, required=True, unique=True)
    is_visible = BooleanField(default=True)

    meta = {
        'collection': 'rooms',
        'db_alias': 'makechat_test' if TEST_MODE else 'makechat',
        'indexes': ['name', 'is_visible']
    }


class Role(Document):
    """Collection of users roles."""

    name = StringField(max_length=10, choices=USER_ROLES, required=True)
    user = ReferenceField(User)
    room = ReferenceField(Room)

    meta = {
        'collection': 'roles',
        'db_alias': 'makechat_test' if TEST_MODE else 'makechat',
        'indexes': ['name', 'user']
    }
