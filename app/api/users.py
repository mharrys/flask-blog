
from flask import Blueprint, jsonify, request

from app import db
from app.api import InvalidUsage, LinkHeaderBuilder, parse_json, parse_arg, \
    parse_pagination_args, sql_ordering, handle_invalid_usage
from app.api.auth import require_authorization
from app.api.users_validators import validate_username, validate_password
from app.models import User

bp = Blueprint('users', __name__, url_prefix='/api')


@bp.errorhandler(InvalidUsage)
def invalid_usage(error):
    return handle_invalid_usage(error)


@bp.route('/users', methods=['GET', 'POST'])
@require_authorization
def users():
    if request.method == 'POST':
        return create_user()
    else:
        return list_users()


@bp.route('/users/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@require_authorization
def user(id):
    user = User.query.get(id)

    if request.method == 'PUT':
        if user:
            return replace_user(user)
        else:
            return create_user()

    if not user:
        message = 'No user with id %s.' % id
        raise InvalidUsage(message, 404)

    if request.method == 'GET':
        return retrieve_user(user)
    if request.method == 'PATCH':
        return update_user(user)
    if request.method == 'DELETE':
        return delete_user(user)


def list_users():
    ordering = ['id', '-id', 'name', '-name']
    page, per_page, order_by = parse_pagination_args(request.args, ordering)

    name = parse_arg(request.args, str, 'name', '')
    name_sql = name.replace(' ', '%')

    pag = User.query.filter(User.name.ilike('%' + name_sql + '%')) \
                    .order_by(sql_ordering(order_by)) \
                    .paginate(page, per_page, False)

    users_json = []
    for user in pag.items:
        users_json.append(user.to_json())

    link = LinkHeaderBuilder(pag, per_page, order_by, request.base_url)
    if name:
        link.add_param('name', name)

    response = jsonify({'users': users_json})
    response.status_code = 200
    response.headers['Link'] = link.build()
    response.headers['X-Total-Count'] = pag.total
    return response


def create_user():
    name = parse_json(request.json, str, 'name')
    password = parse_json(request.json, str, 'password')

    validate_username(name)
    validate_password(password)

    user = User(name, password)
    db.session.add(user)
    db.session.commit()

    response = jsonify(user.to_json(), message='Created user.')
    response.status_code = 201
    response.headers['Location'] = request.base_url + '/' + str(user.id)
    return response


def retrieve_user(user):
    return jsonify(user.to_json()), 200


def replace_user(user):
    return jsonify(message='Not yet available.'), 410


def update_user(user):
    updated = False

    name = parse_json(request.json, str, 'name', required=False)
    password = parse_json(request.json, str, 'password', required=False)

    if name is not None:
        validate_username(name)
        user.name = name
        updated = True
    if password is not None:
        validate_password(password)
        user.change_password(password)
        updated = True

    if updated:
        db.session.commit()
        message = 'Updated user.'
    else:
        message = 'No changes.'

    return jsonify(user.to_json(), message=message), 200


def delete_user(user):
    db.session.delete(user)
    db.session.commit()
    return jsonify(), 204
