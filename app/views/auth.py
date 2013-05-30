from app.forms import LoginForm
from flask import Blueprint, render_template, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required

mod = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth',
    template_folder='../templates/auth'
)


@mod.route('/', methods=['GET', 'POST'])
def login():
    """Authenticate user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = form.user  # verified and fetched by form validator
        login_user(user, remember=form.remember.data)
        return redirect(url_for('admin.overview'))
    return render_template('login.html', form=form)


@mod.route('/logout')
@login_required
def logout():
    """Logout authenticated user."""
    logout_user()
    return redirect(url_for('frontend.blog'))
