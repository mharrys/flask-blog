from functools import wraps

from flask import Blueprint, request, jsonify

from app.models import User

bp = Blueprint('auth', __name__, url_prefix='/api')


def validate_user(username, password):
    """Validate username and password.
    """
    user = User.query.filter_by(name=username).first()
    if not user:
        return False
    else:
        return user.compare_password(password)


def request_authorization(message):
    """Return HTTP Basic challenge-response.

    For web browsers the 'Authentication Required' window appers and asks for
    username and password if the original client request has no or a invalid
    authorization token. The browser typically makes a cache for the token
    which can give unexpected result in a RESTful application.

    """
    response = jsonify(message=message)
    response.status_code = 401
    response.headers['WWW-Authenticate'] = 'Basic realm="admin"'
    return response


def require_authorization(f):
    """Decorate function with a HTTP Basic authorization contraint.

    The server returns a 'HTTP 401 Unauthorized' response if the client
    request has no authorization or if the authorization could not be
    validated as a valid login. The server will not do a challenge-response
    if the authorization token is missing or invalid.

    """
    @wraps(f)
    def wrapper(*args, **kwds):
        auth = request.authorization
        if not auth:
            message = 'No authorization.'
            return jsonify(message=message), 401
        if not validate_user(auth.username, auth.password):
            message = 'Invalid authorization.'
            return jsonify(message=message), 401
        return f(*args, **kwds)
    return wrapper


@bp.route('/auth')
@require_authorization
def auth():
    """Validate HTTP Basic authentication request.

    The server returns a 'HTTP 204 OK' response along with the user resource
    for which the authorization token is valid for.

    """
    user = User.query.filter_by(name=request.authorization.username).first()
    return jsonify(user.to_json()), 200
