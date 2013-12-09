import re
import unidecode

from datetime import datetime

from wtforms.validators import regexp

is_name = regexp(
    # not using \w since it allows for unlimited underscores
    r'^[a-zA-Z0-9]+([ \-\_][a-zA-Z0-9]+)*$',
    message='Field characters can only be letters and digits with one space, \
            underscore or hyphen as separator.'
)


def slugify(now, str):
    """Return slug genereated from date and specified unicoded string."""
    date = datetime.date(now)
    unistr = unidecode.unidecode(str).lower()
    title = re.sub(r'\W+', '-', unistr).strip('-')
    return '%i/%i/%i/%s' % (date.year, date.month, date.day, title)
