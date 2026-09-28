from enum import Enum


class Relationship(str, Enum):
    SAME_USERNAME = "same_username"
    SAME_URL = "same_url"
    SAME_EMAIL = "same_email"
    RELATED_PROFILE = "related_profile"
