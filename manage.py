from app import app, db
from datetime import datetime
from flask.ext.script import Manager

manager = Manager(app)


@manager.command
def init():
    dropdb()
    initdb()
    filldb()


@manager.command
def initdb():
    print('Initializing database...'),
    db.create_all()
    print('done!')


@manager.command
def filldb():
    print('Filling database...'),
    from app.models import User, Post

    admin = User(u'admin', u'admin')
    db.session.add(admin)
    db.session.commit()

    post = Post(
        title=u'Hello, world!',
        body=open('fill/p1.txt', 'r').read(),
        author_id=admin.id
    )
    db.session.add(post)
    db.session.commit()
    post.published = datetime(2011, 06, 13)
    post.edit(post.title, post.body)
    db.session.commit()
    post = Post(
        title=u'Random Words 1',
        body=open('fill/p5.txt', 'r').read(),
        author_id=admin.id
    )
    db.session.add(post)
    db.session.commit()
    post.published = datetime(2012, 8, 15)
    post.edit(post.title, post.body)
    db.session.commit()
    post = Post(
        title=u'Random Words 2',
        body=open('fill/p2.txt', 'r').read(),
        author_id=admin.id
    )
    db.session.add(post)
    db.session.commit()
    post.published = datetime(2012, 12, 24)
    post.edit(post.title, post.body)
    db.session.commit()
    post = Post(
        title=u'Picture of a cat!',
        body=open('fill/p3.txt', 'r').read(),
        author_id=admin.id
    )
    db.session.add(post)
    db.session.commit()
    post = Post(
        title=u'Some code',
        body=open('fill/p4.txt', 'r').read(),
        author_id=admin.id
    )
    db.session.add(post)
    db.session.commit()
    post = Post(
        title=u'Random Words 3',
        body=open('fill/p5.txt', 'r').read(),
        author_id=admin.id
    )
    db.session.add(post)
    db.session.commit()
    print('done!')


@manager.command
def dropdb():
    print('Dropping database...'),
    db.drop_all()
    print('done!')


if __name__ == '__main__':
    manager.run()
