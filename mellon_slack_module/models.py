__author__ = "Paul Schifferer <paul@schifferers.net>"


class _Base(object):
    object_id = ""
    _raw_object = {}

    def __init__(self, json: dict):
        self._raw_object = json


class Topic(object):
    value = ""
    creator = ""
    last_set = 0


class Purpose(object):
    value = ""
    creator = ""
    last_set = 0


class Channel(_Base):
    name = ""
    created = 0
    creator = ""
    is_archived = False
    is_general = False
    is_shared = False
    is_org_shared = False
    is_member = False
    is_private = False
    is_mpim = False
    last_read = 0
    latest = {}
    unread_count = 0
    unread_count_display = 0
    members = []
    topic = Topic()
    purpose = Purpose()
    previous_names = []


class Conversation(_Base):
    name = ""
    created = 0
    creator = ""
    is_channel = False
    is_group = False
    is_im = False
    is_archived = False
    is_general = False
    is_shared = False
    is_org_shared = False
    is_member = False
    is_private = False
    is_mpim = False
    last_read = 0
    latest = {}
    unread_count = 0
    unread_count_display = 0
    members = []
    topic = Topic()
    purpose = Purpose()
    previous_names = []
    unlinked = 0
    is_read_only = False
    is_ext_shared = False
    pending_shared = []
    is_pending_ext_shared = False
    num_members = 0
    locale = ""


class Event(_Base):
    token = ""
    team_id = ""
    api_app_id = ""
    event_details = EventDetails()  # 'event'
    event_type = ""  # 'type'
    authed_users = []
    event_time = 0


class File(object):
    # TODO
    pass


class Group(_Base):
    name = ""
    created = 0
    creator = ""
    is_archived = False
    is_mpim = False
    members = []
    topic = Topic()
    purpose = Purpose()
    last_read = ""
    latest = {}
    unread_count = 0
    unread_count_display = 0


class IM(_Base):
    is_im = False
    user = ""
    created = 0
    is_user_deleted = False


class MPIM(_Base):
    name = ""
    is_group = False
    created = 0
    creator = ""
    members = []
    last_read = ""
    latest = {}
    unread_count = 0
    unread_count_display = 0


class Profile(object):
    avatar_hash = ""
    status_text = ""
    status_emoji = ""
    status_expiration = 0
    real_name = ""
    display_name = ""
    email = ""
    image_original = ""
    team = ""


class User(_Base):
    team_id = ""
    name = ""
    deleted = False
    color = ""
    real_name = ""
    tz = ""
    tz_label = ""
    tz_offset = 0
    profile = Profile()
    is_admin = False
    is_owner = False
    is_primary_owner = False
    is_restricted = False
    is_ultra_restricted = False
    is_bot = False
    is_stranger = False
    updated = 0
    is_app_user = False
    has_2fa = False
    locale = ""


class UserGroup(_Base):
    team_id = ""
    name = ""
    description = ""
    handle = ""
    is_external = False
    date_create = 0
    date_update = 0
    date_delete = 0
    auto_type = ""
    created_by = ""
    updated_by = ""
    deleted_by = ""
    prefs = {}
    users = []
    user_count = 0


#     __tablename__ = 'slack_user'

#     # User Name
#     name     = db.Column(db.String(128),  nullable=False)

#     # Identification Data: email & password
#     email    = db.Column(db.String(128),  nullable=False, unique=True)

#     # Authorisation Data: role & status
#     role     = db.Column(db.SmallInteger, nullable=False)
#     status   = db.Column(db.SmallInteger, nullable=False)

#     # New instance instantiation procedure
#     def __init__(self, name, email, password):

#         self.name     = name
#         self.email    = email
#         self.password = password

#     def __repr__(self):
#         return '<User %r>' % (self.name)
