from flask import render_template

from app import app
from app.models import Post


@app.errorhandler(403)
def forbidden(e):
    return render_template('error/403.html'), 403


@app.errorhandler(404)
def not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500


@app.route('/')
@app.route('/page/<int:page>')
def blog(page=1):
    """Show all blog posts in a paginated list.

    This will only show posts that are marked to be visible. Number of posts
    visible per page has been hardcoded. Note that its the pagination object
    that is being sent in to the template and not the actual posts.

    """
    pagination = Post.query.filter_by(visible=True) \
                           .order_by(Post.published.desc()) \
                           .paginate(page, Post.PER_PAGE, False)
    return render_template('frontend/blog.html', pagination=pagination)


@app.route('/archive')
def archive():
    """Show all blog posts in an foreseeable view.

    This will only show posts that are marked to be visible.

    """
    posts = Post.query.filter_by(visible=True) \
                      .order_by(Post.published.desc())
    return render_template('frontend/archive.html', posts=posts)


@app.route('/<path:slug>', methods=['GET', 'POST'])
def detail(slug):
    """Show post details with specified slug.

    If the specified slug could not be found a HTTP 404 response will be
    generated. Note that this will only show details of the post if its
    marked to be visible.

    """
    post = Post.query.filter_by(visible=True, slug=slug) \
                     .first_or_404()
    return render_template('frontend/detail.html', post=post)


@app.route('/admin')
def admin():
    """Show admin overview page."""
    return render_template('admin/overview.html')


@app.route('/auth/login')
def login():
    return render_template('auth/login.html')


@app.route('/auth/logout')
def logout():
    pass
