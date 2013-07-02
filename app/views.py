from flask import render_template, send_file

from app import app
from app.models import Post


@app.route('/')
@app.route('/page/<int:page>')
def blog(page=1):
    """View the blog."""
    posts = Post.query.filter_by(visible=True) \
                      .order_by(Post.published.desc())
    if posts:
        pagination = posts.paginate(page=page, per_page=Post.PER_PAGE)
    return render_template('blog.html', pagination=pagination)


@app.route('/archive')
def archive():
    """View an overview of all visible posts."""
    posts = Post.query.filter_by(visible=True) \
                      .order_by(Post.published.desc())
    return render_template('archive.html', posts=posts)


@app.route('/<path:slug>', methods=['GET', 'POST'])
def detail(slug):
    """View details of post with specified slug."""
    post = Post.query.filter_by(visible=True, slug=slug) \
                     .first_or_404()
    return render_template('detail.html', post=post)


@app.route('/admin')
def admin():
    return send_file('static/admin-panel/app/index.html')
