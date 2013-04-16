import os

DEBUG = True
SECRET_KEY = 'dev'

root = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(root, 'sqlite3.db')
