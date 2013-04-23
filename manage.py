from app import app, db
from app.models import User, Post
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

    admin = User(u'admin', u'admin')
    db.session.add(admin)
    db.session.commit()

    post = Post(
        title=u'Hello, world!',
        body=POST_1,
        author_id=admin.id
    )
    db.session.add(post)
    db.session.commit()
    post.published = datetime(2011, 06, 13)
    post.edit(post.title, post.body)
    db.session.commit()
    post = Post(
        title=u'Random Words 1',
        body=POST_5,
        author_id=admin.id
    )
    db.session.add(post)
    db.session.commit()
    post.published = datetime(2012, 8, 15)
    post.edit(post.title, post.body)
    db.session.commit()
    post = Post(
        title=u'Random Words 2',
        body=POST_2,
        author_id=admin.id
    )
    db.session.add(post)
    db.session.commit()
    post.published = datetime(2012, 12, 24)
    post.edit(post.title, post.body)
    db.session.commit()
    post = Post(
        title=u'Picture of a cat!',
        body=POST_3,
        author_id=admin.id
    )
    db.session.add(post)
    db.session.commit()
    post = Post(
        title=u'Some code',
        body=POST_4,
        author_id=admin.id
    )
    db.session.add(post)
    db.session.commit()
    post = Post(
        title=u'Random Words 3',
        body=POST_5,
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


POST_1 = """
First blog post.
"""


POST_2 = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean vel ipsum
lectus. Pellentesque tempus enim sed leo imperdiet non lobortis nulla
sollicitudin. Maecenas arcu orci, interdum eu rhoncus ut, blandit id felis.
Mauris consectetur dui at felis ultricies tempus. Quisque molestie convallis
lectus vitae viverra. Duis lobortis ultrices turpis, nec eleifend est
venenatis nec. Sed sed lorem quis metus eleifend ullamcorper. Ut semper
nulla a arcu ornare **condimentum**.

> Ut et lacus ac lacus pulvinar accumsan quis eget lacus. Integer id nibh non
> eros tincidunt bibendum. Aenean diam lectus, tempus sed consequat
> consectetur, posuere non ipsum.
> > Donec vitae eleifend est. Donec at elit mi. Maecenas tempor nulla gravida
> > quam volutpat varius. Vivamus malesuada viverra mauris sed dapibus.
> > Aliquam erat volutpat.

Aliquam neque metus, posuere vitae condimentum ut, fermentum quis diam.
*Nulla facilisi*. Proin sapien felis, tristique eu venenatis at,
**accumsan** non dui. Vestibulum ante ipsum primis in faucibus orci luctus et
ultrices posuere cubilia.
"""


POST_3 = """
Maecenas ut gravida nisi. Aenean feugiat orci non quam vehicula accumsan.
Nullam scelerisque elementum sollicitudin. Sed vel tellus nisi, non tincidunt
augue. Aliquam at nulla ut sem mollis tincidunt.

![Cat](http://i.imgur.com/5wTeD7p.jpg)

Nam quis urna est. Duis vel tincidunt quam. Vivamus odio tortor, suscipit vel
pretium quis, imperdiet quis dolor. Integer molestie enim nec risus malesuada
imperdiet. Donec pellentesque justo id sem tempor varius. Etiam ut tincidunt
lorem. Nullam a tellus sem.

Vestibulum a neque sed quam pharetra interdum. Quisque euismod dictum ipsum.
Vivamus tincidunt mi at tellus pharetra placerat. Sed sed sem nisi, sit amet
ultrices neque. Quisque eget turpis et sapien luctus auctor in ac magna.
Etiam rhoncus commodo molestie.
"""


POST_4 = u"""
Testing out highlight.js. Code from highlight test.html.

    @requires_authorization
    def somefunc(param1='', param2=0):
        r'''A docstring'''
        if param1 > param2: # interesting
            print 'Greater'
        return (param2 - param1 + 1) or None

    class SomeClass:
        pass

    >>> message = '''interpreter
    ... prompt'''

Vestibulum a neque sed quam pharetra interdum. Quisque euismod dictum ipsum.
Vivamus tincidunt mi at tellus pharetra placerat. Sed sed sem nisi, sit amet
ultrices neque. Quisque eget turpis et sapien luctus auctor in ac magna.
"""


POST_5 = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean vel ipsum
lectus. Pellentesque tempus enim sed leo imperdiet non lobortis nulla
sollicitudin. Maecenas arcu orci, interdum eu rhoncus ut, blandit id felis.
Mauris consectetur dui at felis ultricies tempus. Quisque molestie convallis
lectus vitae viverra. Duis lobortis ultrices turpis, nec eleifend est
venenatis nec.

+ Quisque
+ Venenatis

Sed sed lorem quis metus eleifend ullamcorper. Ut semper nulla a arcu ornare
condimentum. Ut et lacus ac lacus pulvinar accumsan quis eget lacus. Integer
id nibh non eros tincidunt bibendum. Aenean diam lectus, tempus sed consequat
consectetur, posuere non ipsum. Donec vitae eleifend est. Donec at elit mi.
Maecenas tempor nulla gravida quam volutpat varius.

Vivamus malesuada viverra mauris sed dapibus. Aliquam erat volutpat. Aliquam
neque metus, posuere vitae condimentum ut, fermentum quis diam. Nulla
facilisi. Proin sapien felis, tristique eu venenatis at, accumsan non dui.
Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere
cubilia.
"""


if __name__ == '__main__':
    manager.run()
