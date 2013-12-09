from datetime import datetime

from flask.ext.bcrypt import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

from app import db, lm
from app.helpers import slugify


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    registered = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(64))
    posts = db.relationship(
        'Post',
        order_by='Post.created.desc()',
        passive_updates=False,
        cascade='all,delete-orphan',
        backref='author',
    )
    last_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(45))
    current_login_at = db.Column(db.DateTime)
    current_login_ip = db.Column(db.String(45))

    def __init__(self, name, password):
        self.name = name
        self.change_password(password)

    def __repr__(self):
        return u'<User(%s, %s)>' % (self.id, self.name)

    def compare_password(self, password):
        """Compare password against stored password hash."""
        return check_password_hash(self.password_hash, password)

    def change_password(self, password):
        """Change current password to a new password."""
        self.password_hash = generate_password_hash(password, 6)


@lm.user_loader
def load_user(id):
    return User.query.get(id)


class Post(db.Model):
    PER_PAGE = 5

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False)
    updated = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(256), nullable=False)
    markup = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False, unique=True)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False,
    )
    visible = db.Column(db.Boolean, default=False)

    def __init__(self, title, markup, author_id, visible):
        self.created = datetime.utcnow()
        self.updated = self.created
        self.title = title
        self.markup = markup
        self.slug = slugify(self.created, title)
        self.author_id = author_id
        self.visible = visible

    def __repr__(self):
        return u'<Post(%s,%s,%s)>' % (self.id, self.slug, self.author.name)

    def update(self, title, markup, visible):
        """Update post values.

        Handles title slug and last update tracking.

        """
        self.updated = datetime.utcnow()
        self.title = title
        self.markup = markup
        self.slug = slugify(self.created, title)
        self.visible = visible

    @property
    def is_updated(self):
        """Validate if this post has been updated since created."""
        return self.updated > self.created
