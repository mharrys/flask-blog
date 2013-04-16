from app import db, bcrypt
from app.helpers import slugify
from datetime import datetime
from flask.ext.login import UserMixin
from flask.ext.sqlalchemy import BaseQuery
from sqlalchemy import and_, func


class UserQuery(BaseQuery):

    def filter_by_name(self, name):
        """Return user with specified name."""
        return self.filter_by(name=name).first()

    def filter_by_name_or_404(self, name):
        """Return user with specified name or 404."""
        return self.filter_by(name=name).first_or_404()

    def filter_by_latest(self):
        """Return users ordered by latest first."""
        return self.order_by(User.registered.desc())

    def filter_by_oldest(self):
        """Return users ordered by oldest first."""
        return self.order_by(User.registered)


class User(db.Model, UserMixin):
    query_class = UserQuery

    id = db.Column(db.Integer, primary_key=True)
    registered = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(60))
    posts = db.relationship(
        'Post',
        order_by='Post.published.desc()',
        passive_updates=False,
        cascade='all,delete-orphan',
        backref='author',
    )

    def __init__(self, name, password):
        self.name = name
        self.change_password(password)

    def __repr__(self):
        return u'<User(%s, %s)>' % (self.id, self.name)

    def compare_password(self, password):
        """Compare password against stored password hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def change_password(self, password):
        """Change current password to a new password."""
        self.password_hash = bcrypt.generate_password_hash(password)


class PostQuery(BaseQuery):

    def slug(self, slug):
        """Return post with specified slug."""
        return self.filter_by(slug=slug).first()

    def slug_or_404(self, slug):
        """Return post with specified slug or 404."""
        return self.filter_by(slug=slug).first_or_404()

    def date_archive(self):
        """Return archive where every post grouped by year and month."""
        year = func.extract('year', Post.published)
        month = func.extract('month', Post.published)
        count = func.count()
        return db.session.query(year.label('year'),
                                month.label('month'),
                                count.label('entries')) \
                         .order_by(year.desc(), month.desc()) \
                         .group_by(year, month) \
                         .all()

    def filter_by_latest(self):
        """Return posts ordered by latest first."""
        return self.order_by(Post.published.desc())

    def filter_by_oldest(self):
        """Return posts ordered by oldest first."""
        return self.order_by(Post.published)

    def filter_by_title_today(self, title):
        """Return post with slug generated from current time and title."""
        slug = slugify(datetime.utcnow(), title)
        return self.slug(slug)

    def filter_by_date(self, year=None, month=None, day=None):
        """Return posts by specified date."""
        terms = []
        if year:
            terms.append(func.extract('year', Post.published) == year)
        if month:
            terms.append(func.extract('month', Post.published) == month)
        if day:
            terms.append(func.extract('day', Post.published) == day)
        return Post.query.filter(and_(*terms))


class Post(db.Model):
    query_class = PostQuery
    PER_PAGE = 5

    id = db.Column(db.Integer, primary_key=True)
    published = db.Column(db.DateTime, nullable=False)
    edited = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False, unique=True)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False,
    )
    comments = db.relationship(
        "Comment",
        order_by="Comment.posted",
        passive_updates=False,
        cascade="all,delete-orphan",
        backref="post",
    )

    def __init__(self, title, body, author_id):
        self.published = datetime.utcnow()
        self.edited = self.published
        self.title = title
        self.body = body
        self.slug = slugify(self.published, title)
        self.author_id = author_id

    def __repr__(self):
        return u'<Post(%s,%s,%s)>' % (self.id, self.slug, self.author.name)

    def edit(self, title, body):
        """Edit post columns."""
        self.edited = datetime.utcnow()
        self.title = title
        self.body = body
        self.slug = slugify(self.published, title)


class CommentQuery(BaseQuery):

    def filter_by_name(self, name):
        """Return comments made by a specific name."""
        return self.filter_by(name=name).first()

    def filter_by_ip(self, ip):
        """Return comments made by a specific ip."""
        return self.filter_by(ip=ip).first()

    def filter_by_latest(self):
        """Return comments ordered by latest first."""
        return self.order_by(Comment.posted.desc())

    def filter_by_oldest(self):
        """Return comments ordered by oldest first."""
        return self.order_by(Comment.posted)


class Comment(db.Model):
    query_class = CommentQuery

    id = db.Column(db.Integer, primary_key=True)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(510), nullable=False)
    ip = db.Column(db.String(45), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    reply_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship(
        'Comment',
        passive_updates=False,
        cascade='all,delete-orphan',
    )

    def __init__(self, name, body, ip, post_id, reply_id=None):
        self.name = name
        self.body = body
        self.ip = ip
        self.post_id = post_id
        self.reply_id = reply_id

    def __repr__(self):
        return u'<Comment(%s,%s,%s)>' % (self.id, self.name, self.body)

    @property
    def is_root(self):
        """Validate if this is not a reply to another comment."""
        return self.reply_id is None

    @property
    def has_replies(self):
        """Validate if this comment has any comment replies."""
        return len(self.replies) > 0
