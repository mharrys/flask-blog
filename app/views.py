from app import app, db
from app.forms import CommentForm
from app.models import Post, Comment
from flask import render_template, request


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
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            form.name.data,
            form.body.data,
            request.remote_addr,  # ip
            post.id,
            form.reply_id.data or None
        )
        db.session.add(comment)
        db.session.commit()
    return render_template('frontend/detail.html', post=post, form=form)
