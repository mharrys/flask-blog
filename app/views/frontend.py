from app import db
from app.forms import CommentForm
from app.models import Post, Comment
from flask import Blueprint, render_template, request

mod = Blueprint(
    'frontend',
    __name__,
    template_folder='../templates/frontend'
)


@mod.route('/')
@mod.route('/page/<int:page>')
def blog(page=1):
    """View the blog."""
    posts = Post.query.filter_by_latest()
    if posts:
        pagination = posts.paginate(page=page, per_page=Post.PER_PAGE)
    return render_template('blog.html', pagination=pagination)


@mod.route('/archive')
def archive():
    """View an overview of all visible posts."""
    posts = Post.query.filter_by_latest()
    return render_template('archive.html', posts=posts)


@mod.route('/<path:slug>', methods=['GET', 'POST'])
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
    return render_template('detail.html', post=post, form=form)
