from app import db
from app.forms import PostForm
from app.models import Post
from flask import Blueprint, render_template, redirect, url_for, request
from flask.ext.login import current_user, login_required

mod = Blueprint(
    'post',
    __name__,
    url_prefix='/admin/post',
    template_folder='../../templates/admin/post'
)


@mod.route('/')
@login_required
def overview():
    """View post overview."""
    posts = Post.query.filter_by_latest(show_hidden=True)
    return render_template('posts.html', posts=posts)


@mod.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    """Create new post."""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(form.title.data,
                    form.body.data,
                    current_user.id,
                    form.visible.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post.edit', slug=post.slug))
    return render_template('new_post.html', form=form)


@mod.route('/edit/<path:slug>', methods=['GET', 'POST'])
@login_required
def edit(slug):
    """Edit post with specified slug."""
    post = Post.query.slug_or_404(slug=slug, show_hidden=True)
    form = PostForm(prev_title=post.title,
                    title=post.title,
                    body=post.body,
                    visible=post.visible)
    if form.validate_on_submit():
        post.edit(form.title.data, form.body.data, form.visible.data)
        db.session.commit()
    return render_template('edit_post.html', post=post, form=form)


@mod.route('/delete/<path:slug>', methods=['GET', 'POST'])
@login_required
def delete(slug):
    """Delete post with specified slug."""
    post = Post.query.slug_or_404(slug=slug, show_hidden=True)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('post.overview'))
    return render_template(
        'delete.html',
        title='Delete Post',
        what=post.title,
        action=url_for('post.delete', slug=post.slug)
    )
