from app import db
from app.forms import LoginForm, PostForm, ChangeUsernameForm, \
    RegisterUserForm, ChangePasswordForm
from app.models import Post, User, Comment
from flask import Blueprint, render_template, redirect, url_for, request
from flask.ext.login import login_user, logout_user, current_user, \
    login_required

mod = Blueprint(
    'admin',
    __name__,
    url_prefix='/admin',
    template_folder='../templates/admin'
)


@mod.route('/login', methods=['GET', 'POST'])
def login():
    """Authenticate user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = form.user  # verified and fetched by form validator
        login_user(user, remember=form.remember.data)
        return redirect(url_for('admin.overview'))
    return render_template('login.html', form=form)


@mod.route('/user/profile')
@login_required
def profile():
    """View authenticated user profile."""
    return render_template('user/profile.html', user=current_user)


@mod.route('/user/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password of authenticated user."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.change_password(form.new_password.data)
        db.session.commit()
    return render_template('user/change_password.html', form=form)


@mod.route('/user/change_username', methods=['GET', 'POST'])
@login_required
def change_username():
    """Change username of authenticated user."""
    form = ChangeUsernameForm(name=current_user.name)
    if form.validate_on_submit():
        current_user.name = form.name.data
        db.session.commit()
        return redirect(url_for('admin.profile'))
    return render_template('user/change_name.html', form=form)


@mod.route('/logout')
@login_required
def logout():
    """Logout authenticated user."""
    logout_user()
    return redirect(url_for('frontend.blog'))


@mod.route('/')
@login_required
def overview():
    """View admin overview."""
    return render_template('overview.html')


@mod.route('/users')
@login_required
def users():
    """View users."""
    users = User.query.filter_by_latest()
    return render_template('user/list.html', users=users)


@mod.route('/users/new', methods=['GET', 'POST'])
@login_required
def new_user():
    """Create new user."""
    form = RegisterUserForm()
    if form.validate_on_submit():
        user = User(form.name.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.users'))
    return render_template('user/new.html', form=form)


@mod.route('/users/delete/<name>', methods=['GET', 'POST'])
@login_required
def delete_user(name):
    """Delete user by specified username."""
    user = User.query.filter_by_name_or_404(name)
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('admin.users'))
    return render_template(
        'delete.html',
        title='Delete User',
        what=user.name,
        action=url_for('admin.delete_user', name=user.name)
    )


@mod.route('/posts')
@login_required
def posts():
    """View all posts."""
    posts = Post.query.filter_by_latest(show_hidden=True)
    return render_template('post/list.html', posts=posts)


@mod.route('/posts/user/<name>')
def posts_by_user(name):
    """View all posts published by specified author."""
    user = User.query.filter_by_name_or_404(name=name)
    archive = Post.query.date_archive(user.id, show_hidden=True)
    return render_template('post/list.html', user=user, archive=archive)


@mod.route('/posts/new', methods=['GET', 'POST'])
@login_required
def new_post():
    """Add new post."""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(form.title.data,
                    form.body.data,
                    current_user.id,
                    form.visible.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('admin.edit_post', slug=post.slug))
    return render_template('post/new.html', form=form)


@mod.route('/posts/edit/<path:slug>', methods=['GET', 'POST'])
@login_required
def edit_post(slug):
    """Edit post with specified slug."""
    post = Post.query.slug_or_404(slug=slug, show_hidden=True)
    form = PostForm(prev_title=post.title,
                    title=post.title,
                    body=post.body,
                    visible=post.visible)
    if form.validate_on_submit():
        post.edit(form.title.data, form.body.data, form.visible.data)
        db.session.commit()
    return render_template('post/edit.html', post=post, form=form)


@mod.route('/posts/delete/<path:slug>', methods=['GET', 'POST'])
@login_required
def delete_post(slug):
    """Delete post with specified slug."""
    post = Post.query.slug_or_404(slug=slug, show_hidden=True)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('admin.posts'))
    return render_template(
        'delete.html',
        title='Delete Post',
        what=post.title,
        action=url_for('admin.delete_post', slug=post.slug)
    )


@mod.route('/posts/comments/<path:slug>')
@login_required
def post_comments(slug):
    """View comments for specified slug."""
    post = Post.query.slug_or_404(slug=slug, show_hidden=True)
    return render_template('comment/list.html',
                           post=post,
                           comments=post.comments)


@mod.route('/comments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    """Delete comment with specified id."""
    comment = Comment.query.get_or_404(id)
    if request.method == 'POST':
        post_id = comment.post_id
        db.session.delete(comment)
        db.session.commit()
        # redirect to the remaining post comments
        slug = Post.query.get_or_404(post_id).slug
        return redirect(url_for('admin.post_comments', slug=slug))
    return render_template(
        'delete.html',
        title='Delete Comment',
        what='comment',
        action=url_for('admin.delete_comment', id=comment.id)
    )
