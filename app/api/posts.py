from flask import Blueprint, jsonify, request

from app import db
from app.api import InvalidUsage, LinkHeaderBuilder, parse_json, parse_arg, \
    parse_pagination_args, sql_ordering, handle_invalid_usage
from app.api.auth import require_authorization
from app.api.posts_validators import validate_title, validate_markup, \
    validate_author_id
from app.models import Post

bp = Blueprint('posts', __name__, url_prefix='/api')


@bp.errorhandler(InvalidUsage)
def invalid_usage(error):
    return handle_invalid_usage(error)


@bp.route('/posts', methods=['GET', 'POST'])
@require_authorization
def posts():
    if request.method == 'POST':
        return create_post()
    else:
        return list_posts()


@bp.route('/posts/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@require_authorization
def post(id):
    post = Post.query.get(id)

    if request.method == 'PUT':
        if post:
            return replace_post(post)
        else:
            return create_post()

    if not post:
        message = 'No post with id %s.' % id
        raise InvalidUsage(message, 404)

    if request.method == 'GET':
        return retrieve_post(post)
    if request.method == 'PATCH':
        return update_post(post)
    if request.method == 'DELETE':
        return delete_post(post)


def list_posts():
    ordering = ['id', '-id', 'title', '-title']
    page, per_page, order_by = parse_pagination_args(request.args, ordering)

    title = parse_arg(request.args, str, 'title', '')
    title_sql = title.replace(' ', '%')

    pag = Post.query.filter(Post.title.ilike('%' + title_sql + '%')) \
                    .order_by(sql_ordering(order_by)) \
                    .paginate(page, per_page, False)

    posts_json = []
    for post in pag.items:
        posts_json.append(post.to_json())

    link = LinkHeaderBuilder(pag, per_page, order_by, request.base_url)
    if title:
        link.add_param('title', title)

    response = jsonify({'posts': posts_json})
    response.status_code = 200
    response.headers['Link'] = link.build()
    response.headers['X-Total-Count'] = pag.total
    return response


def create_post():
    title = parse_json(request.json, str, 'title')
    markup = parse_json(request.json, str, 'markup')
    author_id = parse_json(request.json, int, 'author_id')
    visible = parse_json(request.json, bool, 'visible')

    validate_title(title)
    validate_markup(markup)
    validate_author_id(author_id)

    post = Post(title, markup, author_id, visible)
    db.session.add(post)
    db.session.commit()

    response = jsonify(post.to_json(), message='Created post.')
    response.status_code = 201
    response.headers['Location'] = request.base_url + '/' + str(post.id)
    return response


def retrieve_post(post):
    return jsonify(post.to_json()), 200


def replace_post(post):
    return jsonify(message='Not yet available.'), 410


def update_post(post):
    updated = False

    title = parse_json(request.json, str, 'title', required=False)
    markup = parse_json(request.json, str, 'markup', required=False)
    author_id = parse_json(request.json, int, 'author_id', required=False)
    visible = parse_json(request.json, bool, 'visible', required=False)

    if title is not None:
        validate_title(title)
        post.change_title(title)
        updated = True
    if markup is not None:
        validate_markup(markup)
        post.markup = markup
        updated = True
    if author_id is not None:
        validate_author_id(author_id)
        post.author_id = author_id
        updated = True
    if visible is not None:
        post.visible = visible
        updated = True

    if updated:
        db.session.commit()
        message = 'Updated post.'
    else:
        message = 'No changes.'

    return jsonify(post.to_json(), message=message), 200


def delete_post(post):
    db.session.delete(post)
    db.session.commit()
    return jsonify(), 204
