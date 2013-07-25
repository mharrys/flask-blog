import re

from app.api import InvalidUsage
from app.models import User


def validate_username(username):
    if len(username) < 3:
        message = (
            'Username is too short, needs to be at least 3 characters long.'
        )
        raise InvalidUsage(message)

    # not using \w since it allows for unlimited underscores
    is_name_pattern = r'^[a-zA-Z0-9]+([ \-\_][a-zA-Z0-9]+)*$'
    if not re.match(is_name_pattern, username):
        message = (
            'Name can only be letters and digits with one space, underscore '
            'or hyphen as separator.'
        )
        raise InvalidUsage(message)

    if User.query.filter_by(name=username).first():
        message = 'Username already exist.'
        raise InvalidUsage(message, 409)


def validate_password(password):
    # any password should be ok with one minimal requirement, do not force
    # password styles onto users
    if len(password) < 1:
        message = (
            'Password is too short, needs to be at least 1 character long.'
        )
        raise InvalidUsage(message)
