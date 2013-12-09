from flask import render_template, redirect, url_for, Blueprint, flash
from flask.ext.login import login_required, login_user, logout_user, \
    current_user

from app import app, db
from app.forms import LoginForm, ChangePasswordForm, ChangeUsernameForm, \
    PostForm
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
                           .order_by(Post.created.desc()) \
                           .paginate(page, Post.PER_PAGE, False)
    return render_template('frontend/blog.html', pagination=pagination)


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


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Show login page."""
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user=form.user, remember=form.remember_me.data)
        return redirect(url_for('admin.overview'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """Logout authenticated user."""
    logout_user()
    return redirect(url_for('blog'))


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@login_required
def overview():
    """Show admin overview page."""
    return render_template('admin/overview.html')


@admin.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Show settings for authenticated user."""
    chpwd = ChangePasswordForm(prefix='pwd')
    chusr = ChangeUsernameForm(prefix='usr')

    if chpwd.submit.data and chpwd.validate_on_submit():
        current_user.change_password(chpwd.new_password.data)
        db.session.commit()
        flash('Changed password!', 'success')

    if chusr.submit.data and chusr.validate_on_submit():
        current_user.name = chusr.username.data
        db.session.commit()
        flash('Changed username!', 'success')

    return render_template('admin/settings.html', chpwd=chpwd, chusr=chusr)


@admin.route('/posts')
@admin.route('/posts/page/<int:page>')
@login_required
def posts(page=1):
    """Show all posts."""
    pagination = Post.query.filter_by() \
                           .order_by(Post.created.desc()) \
                           .paginate(page, Post.PER_PAGE, False)
    return render_template('admin/post/list.html', pagination=pagination)


@admin.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            form.title.data,
            form.markup.data,
            current_user.id,
            form.visible.data
        )
        db.session.add(post)
        db.session.commit()
        flash('Created post <strong>%s</strong>!' % post.title, 'success')
        return redirect(url_for('admin.edit_post', id=post.id))
    return render_template('admin/post/new.html', form=form)


@admin.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm(title=post.title, markup=post.markup, visible=post.visible)
    if form.validate_on_submit():
        post.update(form.title.data, form.markup.data, form.visible.data)
        db.session.commit()
        flash('Saved changes!', 'info')
    return render_template('admin/post/edit.html', post=post, form=form)


@admin.route('/delete_post/<int:id>')
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Deleted post <strong>%s</strong>!' % post.title, 'danger')
    return redirect(url_for('.posts'))
