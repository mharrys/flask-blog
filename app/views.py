from flask import render_template, redirect, url_for, Blueprint, flash
from flask.ext.login import login_required, login_user, logout_user, \
    current_user

from app import app, db
from app.forms import LoginForm, ChangePasswordForm, ChangeUsernameForm
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
        flash('Successfully changed password!', 'success')

    if chusr.submit.data and chusr.validate_on_submit():
        current_user.name = chusr.username.data
        db.session.commit()
        flash('Successfully changed username!', 'success')

    return render_template('admin/settings.html', chpwd=chpwd, chusr=chusr)


@admin.route('/posts')
@login_required
def posts():
    """Show all posts."""
    return render_template('admin/posts.html')


@admin.route('/create_post')
@login_required
def create_post():
    pass
