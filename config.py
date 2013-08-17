import os

DEBUG = True
SECRET_KEY = 'dev'

if DEBUG:
    root = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(root, 'sqlite3.db')
else:
    db = 'database'
    username = 'username'
    password = 'password'
    uri = 'postgres://%s:%s@localhost:5432/%s' % (username, password, db)
    SQLALCHEMY_DATABASE_URI = uri
