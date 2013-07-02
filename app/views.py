from app import app
from app.models import Post
from flask import render_template


@app.route('/')
@app.route('/page/<int:page>')
def blog(page=1):
    """View the blog."""
    posts = Post.query.filter_by_latest()
    if posts:
        pagination = posts.paginate(page=page, per_page=Post.PER_PAGE)
    return render_template('frontend/blog.html', pagination=pagination)


@app.route('/archive')
def archive():
    """View an overview of all visible posts."""
    posts = Post.query.filter_by_latest()
    return render_template('frontend/archive.html', posts=posts)


@app.route('/<path:slug>', methods=['GET', 'POST'])
def detail(slug):
    """View details of post with specified slug."""
    post = Post.query.slug_or_404(slug)
    return render_template('frontend/detail.html', post=post)
