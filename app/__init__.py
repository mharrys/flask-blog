from flask import Flask, Markup
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from markdown2 import markdown as md2

app = Flask(__name__)
app.config.from_object('config')

# Extensions

db = SQLAlchemy(app)

lm = LoginManager(app)
lm.login_view = 'auth.login'
lm.login_message = None


# Jinja

def date(value):
    """Formats datetime object to a yyyy-mm-dd string."""
    return value.strftime('%Y-%m-%d')


def date_pretty(value):
    """Formats datetime object to a Month dd, yyyy string."""
    return value.strftime('%B %d, %Y')


def datetime(value):
    """Formats datetime object to a yyyy-mm-dd hh:mm string."""
    return value.strftime('%Y-%m-%d %H:%M')


def pluralize(value, one='', many='s'):
    """Returns the plural suffix when needed."""
    return one if abs(value) == 1 else many


def month_name(value):
    """Return month name for a month number."""
    from calendar import month_name
    return month_name[value]


def markdown(value):
    """Convert plain text to HTML."""
    extras = ['fenced-code-blocks', 'wiki-tables']
    return Markup(md2(value, extras=extras))


app.jinja_env.filters['date'] = date
app.jinja_env.filters['date_pretty'] = date_pretty
app.jinja_env.filters['datetime'] = datetime
app.jinja_env.filters['pluralize'] = pluralize
app.jinja_env.filters['month_name'] = month_name
app.jinja_env.filters['markdown'] = markdown


# Blueprints

from app import views

app.register_blueprint(views.auth)
app.register_blueprint(views.admin)
