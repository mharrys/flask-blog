import unittest

from app import app, db
from app.helpers import slugify
from app.models import User, Post, Comment
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
IP = '127.0.0.1'


def db_commit():
    """Helper function for testing database integrity."""
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise


def add_user(name=u'latest_user', pwd=u'pwd'):
    """Add user to database and return its model."""
    user = User(name, pwd)
    db.session.add(user)
    db.session.commit()
    return user


def add_post(title=u'latest_title', body=u'body', author_id=1, visible=True):
    """Add post to database and return its model."""
    post = Post(title, body, author_id, visible=visible)
    db.session.add(post)
    db.session.commit()
    return post


def add_comment(name=u'anon', body=u'foo', ip=IP, post_id=1, reply_id=None):
    """Add comment to database and return its model."""
    comment = Comment(name, body, ip, post_id, reply_id)
    db.session.add(comment)
    db.session.commit()
    return comment


class TestModel(unittest.TestCase):

    def setUp(self):
        db.create_all()
        # default user
        self.name = u'name'
        self.pwd = u'pwd'
        self.user = add_user(self.name, self.pwd)
        # default post
        self.title = u'title'
        self.body = u'body'
        self.author_id = self.user.id
        self.post = add_post(self.title, self.body, self.author_id)
        # default comment
        self.comment = add_comment(self.name, self.body)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestUser(TestModel):

    def test_create(self):
        # assert default user was added
        self.assertEqual(1, len(User.query.all()))
        # assert correct name and password
        q = User.query.filter_by_name(self.name)
        self.assertEqual(self.name, q.name)
        self.assertTrue(q.compare_password(self.pwd))
        # assert unique
        db.session.add(User(self.name, self.pwd))
        self.assertRaises(IntegrityError, db_commit)

    def test_change_password(self):
        # assert current password is used
        q = User.query.filter_by_name(self.name)
        self.assertTrue(q.compare_password(self.pwd))
        # update database with new user password
        new_pwd = 'new_pwd'
        q.change_password(new_pwd)
        db.session.commit()
        # assert new password is set
        q = User.query.filter_by_name(self.name)
        self.assertTrue(q.compare_password(new_pwd))

    def test_filter_by_name(self):
        # existing user
        q = User.query.filter_by_name(self.name)
        self.assertEqual(self.user.id, q.id)
        # non existing user
        q = User.query.filter_by_name(u'unknown')
        self.assertIsNone(q)

    def test_filter_by_name_or_404(self):
        # existing user
        q = User.query.filter_by_name_or_404(self.name)
        self.assertEqual(self.user.id, q.id)
        # non existing user
        self.assertRaises(NotFound,
                          User.query.filter_by_name_or_404,
                          u'unknown')

    def test_filter_by_latest(self):
        latest_user = add_user()
        q = User.query.filter_by_latest().all()
        # assert latest user is first in list
        self.assertEqual(latest_user.id, q[0].id)
        self.assertEqual(self.user.id, q[1].id)

    def test_filter_by_oldest(self):
        latest_user = add_user()
        q = User.query.filter_by_oldest().all()
        # assert latest user is last in list
        self.assertEqual(self.user.id, q[0].id)
        self.assertEqual(latest_user.id, q[1].id)


class TestPost(TestModel):

    def test_create(self):
        # assert default post added
        self.assertEqual(1, len(Post.query.all()))
        # assert correct post values
        q = Post.query.get(self.post.id)
        self.assertEqual(self.title, q.title)
        self.assertEqual(self.body, q.body)
        slug = slugify(datetime.utcnow(), self.title)
        self.assertEqual(slug, q.slug)
        self.assertEqual(self.author_id, q.author_id)
        # assert unique for same date
        db.session.add(
            Post(self.title, self.body, self.author_id, visible=True)
        )
        self.assertRaises(IntegrityError, db_commit)
        # assert not unique for diffrent date
        now = datetime.utcnow()
        latest_post = Post(self.title,
                           self.body,
                           self.author_id,
                           visible=True)
        latest_post.published = datetime(now.year - 1, now.month, now.day)
        latest_post.edit(self.title, self.body, True)
        db.session.add(latest_post)
        db.session.commit()

    def tet_edit(self):
        # assert current title is set with correct slug
        q = Post.query.get(self.post.id)
        self.assertEqual(self.title, q.title)
        slug = slugify(datetime.utcnow(), self.title)
        self.assertEqual(slug, q.slug)
        # update database with new post title
        new_title = 'foo'
        q.edit(new_title, self.body)
        self.commit()
        # assert title and slug updated
        q = Post.query.get(self.post.id)
        self.assertEqual(new_title, q.title)
        slug = slugify(datetime.utcnow(), self.new_title)
        self.assertEqual(slug, q.slug)
        # assert edit date has also been updated
        self.assertGreater(q.edited, q.published)

    def test_delete(self):
        add_post()
        self.assertEqual(2, len(Post.query.all()))
        # assert all posts by user gets deleted if user is deleted
        db.session.delete(self.user)
        db.session.commit()
        self.assertEqual(0, len(Post.query.all()))

    def test_slug(self):
        # existing post
        q = Post.query.slug(self.post.slug)
        self.assertEqual(self.post.id, q.id)
        # non existing post
        q = Post.query.slug('unknown')
        self.assertIsNone(q)
        # assert hidden does not show up
        latest_post = add_post(visible=False)
        q = Post.query.slug(latest_post.slug)
        self.assertIsNone(q)
        # assert hidden shows up when specified
        q = Post.query.slug(latest_post.slug, show_hidden=True)
        self.assertEqual(latest_post.id, q.id)

    def test_slug_or_404(self):
        # existing post
        q = Post.query.slug_or_404(self.post.slug)
        self.assertEqual(self.post.id, q.id)
        # non existing post
        self.assertRaises(NotFound, Post.query.slug_or_404, u'unknown')
        # assert hidden does not show up
        latest_post = add_post(visible=False)
        self.assertRaises(NotFound, Post.query.slug_or_404, latest_post.slug)
        # assert hidden shows up when specified
        q = Post.query.slug_or_404(latest_post.slug, show_hidden=True)
        self.assertEqual(latest_post.id, q.id)

    def test_date_archive(self):
        now = datetime.utcnow()
        q = Post.query.date_archive()
        # assert default post is grouped correctly
        self.assertEqual(now.year, q[0].year)
        self.assertEqual(now.month, q[0].month)
        # assert first post is included
        self.assertEqual(self.post.id, q[0].Post.id)
        # assert hidden does not show up
        self.post.visible = False
        db.session.commit()
        q = Post.query.date_archive()
        self.assertEqual(0, len(q))
        # assert hidden shows up when specified
        q = Post.query.date_archive(show_hidden=True)
        self.assertEqual(1, len(q))

    def test_filter_by_latest(self):
        latest_post = add_post()
        q = Post.query.filter_by_latest().all()
        # assert latest post is first in list
        self.assertEqual(latest_post.id, q[0].id)
        self.assertEqual(self.post.id, q[1].id)
        # assert hidden does not show up
        latest_post.visible = False
        db.session.commit()
        q = Post.query.filter_by_latest().all()
        self.assertEqual(self.post.id, q[0].id)  # second is now first
        # assert hidden shows up when specified
        q = Post.query.filter_by_latest(show_hidden=True).all()
        self.assertEqual(latest_post.id, q[0].id)
        self.assertEqual(self.post.id, q[1].id)

    def test_filter_by_oldest(self):
        latest_post = add_post()
        q = Post.query.filter_by_oldest().all()
        # assert latest post is last in list
        self.assertEqual(self.post.id, q[0].id)
        self.assertEqual(latest_post.id, q[1].id)
        # assert hidden does not show up
        self.post.visible = False
        db.session.commit()
        q = Post.query.filter_by_oldest().all()
        self.assertEqual(latest_post.id, q[0].id)  # second is now first
        # assert hidden shows up when specified
        q = Post.query.filter_by_oldest(show_hidden=True).all()
        self.assertEqual(self.post.id, q[0].id)
        self.assertEqual(latest_post.id, q[1].id)

    def test_filter_by_title_today(self):
        q = Post.query.filter_by_title_today(self.post.title)
        self.assertEqual(self.post.id, q.id)

    def test_filter_by_date(self):
        # assert all parameters gives default post
        now = datetime.utcnow()
        q = Post.query.filter_by_date(now.year).first()
        self.assertEqual(self.post.id, q.id)
        q = Post.query.filter_by_date(now.year, now.month).first()
        self.assertEqual(self.post.id, q.id)
        q = Post.query.filter_by_date(now.year, now.month, now.day).first()
        self.assertEqual(self.post.id, q.id)
        # all existing
        q = Post.query.filter_by_date()
        self.assertEqual(1, q.count())
        # non existing
        q = Post.query.filter_by_date(now.year - 1).first()
        self.assertIsNone(q)


class TestComment(TestModel):

    def test_create(self):
        # assert default comment was added
        self.assertEqual(1, len(Comment.query.all()))
        # assert correct comment values
        q = Comment.query.get(self.comment.id)
        self.assertEqual(self.name, q.name)
        self.assertEqual(self.body, q.body)
        self.assertEqual(self.post.id, q.post_id)

    def test_delete_post(self):
        add_comment()
        self.assertEqual(2, len(Comment.query.all()))
        # assert all comments to a post gets deleted if post is deleted
        db.session.delete(self.post)
        db.session.commit()
        self.assertEqual(0, len(Comment.query.all()))

    def test_delete_root(self):
        # assert childs to root are deleted when root is deleted
        comment_reply = add_comment(reply_id=self.comment.id)
        add_comment(reply_id=comment_reply.id)
        db.session.delete(self.comment)
        db.session.commit()
        self.assertEqual(0, len(Comment.query.all()))

    def test_filter_by_name(self):
        # existing comment
        q = Comment.query.filter_by_name(self.name)
        self.assertEqual(self.comment.id, q.id)
        # non existing comment
        q = Comment.query.filter_by_name(u'unknown')
        self.assertIsNone(q)

    def test_filter_by_ip(self):
        # existing comment
        q = Comment.query.filter_by_ip(IP)
        self.assertEqual(self.comment.id, q.id)
        # non existing comment
        q = Comment.query.filter_by_name(u'unknown')
        self.assertIsNone(q)

    def test_filter_by_latest(self):
        latest_comment = add_comment()
        q = Comment.query.filter_by_latest().all()
        # assert latest comment is first in list
        self.assertEqual(latest_comment.id, q[0].id)
        self.assertEqual(self.comment.id, q[1].id)

    def test_filter_by_oldest(self):
        latest_comment = add_comment()
        q = Comment.query.filter_by_oldest().all()
        # assert latest comment is last in list
        self.assertEqual(self.comment.id, q[0].id)
        self.assertEqual(latest_comment.id, q[1].id)

    def test_is_root(self):
        # assert default comment is root (not a comment reply)
        self.assertTrue(self.comment.is_root)
        # assert comment reply to default comment is not root
        comment_reply = add_comment(reply_id=self.comment.id)
        self.assertFalse(comment_reply.is_root)
        self.assertTrue(self.comment.is_root)

    def test_has_replies(self):
        # assert default comment has no replies
        self.assertFalse(self.comment.has_replies)
        # assert default comment has a reply when added a comment reply
        comment_reply = add_comment(reply_id=self.comment.id)
        self.assertTrue(self.comment.has_replies)
        self.assertFalse(comment_reply.has_replies)
