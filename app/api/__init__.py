from flask import request, jsonify


# http://flask.pocoo.org/docs/patterns/apierrors/
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


# http://flask.pocoo.org/docs/patterns/apierrors/
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


class LinkHeaderBuilder:
    """Builder class for building paginated links as described by RFC 5988.

    Link to implementation details:
    http://tools.ietf.org/html/rfc5988#page-6
    """

    def __init__(self, pagination, per_page, order_by, base_url):
        self.pagination = pagination
        self.per_page = per_page
        self.order_by = order_by
        self.base_url = base_url
        self.params = []
        self.add_param('per_page', per_page)
        self.add_param('order_by', order_by)

    def add_param(self, name, value):
        """Add parameter with value to be included in every link.
        """
        self.params.append('&%s=%s' % (name, value))

    def build_link(self, page, rel):
        """Build link for specified page and name.
        """
        url_params = '?page=%s' % page
        for param in self.params:
            url_params += param
        return '<%s%s>; rel="%s"' % (self.base_url, url_params, rel)

    def build(self):
        """Return built link header.
        """
        page = 1
        header = self.build_link(page, 'first')
        if self.pagination.has_next:
            page = self.pagination.next_num
            header += ', ' + self.build_link(page, 'next')
        if self.pagination.has_prev:
            page = self.pagination.prev_num
            header += ', ' + self.build_link(page, 'prev')
        page = self.pagination.pages
        header += ', ' + self.build_link(page, 'last')
        return header


def parse_json(json, data_type, prop, required=True):
    """Return json with specified datatype or None.

    InvalidUsage exception if the property could not be found but specified
    to be required. None will be returned if property could not be found and
    is not required.

    InvalidUsage exception if the property could not be parsed into specified
    data type.

    """
    if not prop in json and required:
        message = 'Missing required json property %s.' % prop
        raise InvalidUsage(message)
    if not prop in json and not required:
        return None
    try:
        return data_type(request.json[prop])
    except ValueError:
        message = (
            'Expected data type %s for json property %s.' % (data_type, prop)
        )
        raise InvalidUsage(message)


def parse_arg(args, data_type, name, default):
    """Return argument with specified datatype.

    If the argument could not be found the specified default value will be
    used instead.

    InvalidUsage exception if the argument could not be parsed into specified
    data type, this remains true for the specified default value.

    """
    try:
        return data_type(args.get(name, default))
    except ValueError:
        message = (
            'Expected data type %s for parameter %s.' % (data_type, name)
        )
        raise InvalidUsage(message)


def parse_pagination_args(args, ordering):
    """Return page, per_page and order_by values from request arguments.

    Helper function for parsing the three essential argument for a paginated
    list. The ordering must be specified with an array where descending order
    is specified with a - (minus) character.

    InvalidUsage exception if any argument could not be parsed into expected
    data type.

    InvalidUsage exception if page and per_page has bad integer values such as
    for example negative values.

    InvalidUsage exception if the ordering could not be found in the specified
    array.

    """
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 10
    DEFAULT_ORDER_BY = 'id'
    MAX_PER_PAGE = 100

    page = parse_arg(args, int, 'page', DEFAULT_PAGE)
    if page < 1:
        message = 'Argument page must be a positive number.'
        raise InvalidUsage(message)

    per_page = parse_arg(args, int, 'per_page', DEFAULT_PER_PAGE)
    if per_page < 1 or per_page > MAX_PER_PAGE:
        message = (
            'Argument per_page must be between 1 and %s.' % MAX_PER_PAGE
        )
        raise InvalidUsage(message)

    order_by = parse_arg(args, str, 'order_by', DEFAULT_ORDER_BY)
    if order_by not in ordering:
        message = 'Unknown value %s for argument order_by.' % order_by
        raise InvalidUsage(message)

    return page, per_page, order_by


def sql_ordering(order_by):
    """Return ordering name for use with SQLAlchemy.

    SQLAlchemy expect '<attribute>' or '<attribute> desc' but the API use a
    - (minus) character to determine ascending or descending order.

    """
    if order_by.startswith('-'):
        return order_by[1:] + ' desc'
    else:
        return order_by
