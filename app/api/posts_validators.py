from datetime import datetime

from app.api import InvalidUsage
from app.helpers import slugify
from app.models import Post, User


def validate_title(title):
    if len(title) < 1:
        message = (
            'Title is too short, needs to be at least 1 character long.'
        )
        raise InvalidUsage(message)

    # two or more posts can not exist on the same date with the same title
    # because of the slug
    slug = slugify(datetime.utcnow(), title)
    if Post.query.filter_by(slug=slug).first():
        message = 'Title already exist on this date.'
        raise InvalidUsage(message, 409)


def validate_markup(markup):
    if len(markup) < 1:
        message = (
            'Markup is too short, needs to be at least 1 character long.'
        )
        raise InvalidUsage(message)


def validate_author_id(author_id):
    if not User.query.get(author_id):
        message = 'Unknown author id.'
        raise InvalidUsage(message)
