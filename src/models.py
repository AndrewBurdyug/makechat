"""All mongoengine models are should be described here."""
from datetime import datetime
from makechat import config as settings
from mongoengine import connect, Document, StringField, ReferenceField, \
    BooleanField, EmailField, DateTimeField, ListField, CASCADE, PULL

connect(alias='makechat', host=settings.get('DEFAULT', 'mongo_uri'))
connect(alias='makechat_test', host=settings.get('DEFAULT', 'test_mongo_uri'))

TEST_MODE = settings.getboolean('DEFAULT', 'test_mode')
SESSION_TTL = settings.getint('DEFAULT', 'session_ttl')

USER_ROLES = (
    ('admin', 'Superuser'),  # can create chat rooms and manage chat members
    ('owner', 'Chat owner'),  # can read/write and manage chat members
    ('member', 'Chat member'),  # can read/write, but can't manage chat members
    ('guest', 'Chat guest'),  # can read, but can't write
)


class MetaData(Document):
    """Base class for all models.

    The goal is to have metadata for all objects and do not repeat itself.
    """

    created = DateTimeField(default=datetime.now)

    meta = {
        'abstract': True
    }


class User(MetaData):
    """Collection of users profiles."""

    email = EmailField(required=True, unique=True)
    username = StringField(regex=r'[a-zA-Z0-9_-]+$', max_length=120,
                           required=True, unique=True)
    password = StringField(max_length=64, required=True)
    is_superuser = BooleanField(default=False)
    is_disabled = BooleanField(default=False)

    meta = {
        'collection': 'users',
        'db_alias': 'makechat_test' if TEST_MODE else 'makechat',
        'indexes': ['email', 'username', 'password']
    }

    def __str__(self):
        """Standart python magic __str__ method."""
        return self.username


class Member(MetaData):
    """Collection of room members."""

    role = StringField(max_length=10, choices=USER_ROLES, required=True)
    profile = ReferenceField(User, reverse_delete_rule=CASCADE)

    meta = {
        'collection': 'members',
        'db_alias': 'makechat_test' if TEST_MODE else 'makechat',
    }


class Room(MetaData):
    """Collection of chat rooms."""

    name = StringField(max_length=120, required=True, unique=True)
    members = ListField(ReferenceField(Member, reverse_delete_rule=PULL))
    is_visible = BooleanField(default=True)
    is_open = BooleanField(default=True)

    meta = {
        'collection': 'rooms',
        'db_alias': 'makechat_test' if TEST_MODE else 'makechat',
        'indexes': ['name', 'is_visible']
    }


class Message(MetaData):
    """Collection of chat messages."""

    text = StringField()
    sender = ReferenceField(User, reverse_delete_rule=CASCADE)
    recipient = ReferenceField(User, reverse_delete_rule=CASCADE)
    rooms = ListField(ReferenceField(Room, reverse_delete_rule=PULL))

    meta = {
        'collection': 'messages',
        'db_alias': 'makechat_test' if TEST_MODE else 'makechat',
        'indexes': [
            'sender', 'recipient',
            {
                'fields': ['$text'],
                'default_language': 'russian',
            }
        ]
    }


class Session(MetaData):
    """Collection of users sessions.

    WARNING: reverse_delete_rule=CASCADE for user field will cause error,
    see https://github.com/MongoEngine/mongoengine/issues/1135#issuecomment-207
    099167
    """

    user = ReferenceField(User)
    value = StringField(max_length=64, primary_key=True)

    meta = {
        'collection': 'sessions',
        'db_alias': 'makechat_test' if TEST_MODE else 'makechat',
        'indexes': [
            {'fields': ['created'], 'expireAfterSeconds': SESSION_TTL}
        ]
    }


class Token(MetaData):
    """Collection of API tokens.

    WARNING: reverse_delete_rule=CASCADE for user field will cause error,
    see https://github.com/MongoEngine/mongoengine/issues/1135#issuecomment-207
    099167
    """

    user = ReferenceField(User)
    name = StringField(max_length=100, required=True)
    value = StringField(max_length=32, primary_key=True)

    meta = {
        'collection': 'tokens',
        'db_alias': 'makechat_test' if TEST_MODE else 'makechat',
    }
