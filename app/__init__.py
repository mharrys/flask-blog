from flask import Flask, Markup
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from markdown2 import markdown as md2

app = Flask(__name__)
app.config.from_object('config')

# Extensions

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


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


def timesince(value, now=None):
    """
    Formats datetime object to a string of the time since specified time value
    and current time. For example '32 seconds', '1 hour', '3 years' and so on.
    """
    # used for unit testing with a custom datetime object
    if now is None:
        now = value.utcnow()
    # constants in seconds, the approximations should suffice in this context
    total_seconds = int((now - value).total_seconds())
    minute = 60
    hour = minute * 60
    day = hour * 24
    year = day * 365
    month = year / 12
    if total_seconds >= year:
        dy = total_seconds / year
        return '%s year%s' % (dy, pluralize(dy))
    if total_seconds >= month:
        dm = total_seconds / month
        return '%s month%s' % (dm, pluralize(dm))
    if total_seconds >= day:
        dd = total_seconds / day
        return '%s day%s' % (dd, pluralize(dd))
    if total_seconds >= hour:
        dh = total_seconds / hour
        return '%s hour%s' % (dh, pluralize(dh))
    if total_seconds >= minute:
        dm = total_seconds / minute
        return '%s minute%s' % (dm, pluralize(dm))
    return '%s second%s' % (total_seconds, pluralize(total_seconds))


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
app.jinja_env.filters['timesince'] = timesince
app.jinja_env.filters['pluralize'] = pluralize
app.jinja_env.filters['month_name'] = month_name
app.jinja_env.filters['markdown'] = markdown

from app import views
