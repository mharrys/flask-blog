from app import db
from app.forms import ChangeUsernameForm, ChangePasswordForm
from flask import Blueprint, render_template, redirect, url_for
from flask.ext.login import login_required, current_user

mod = Blueprint(
    'profile',
    __name__,
    url_prefix='/admin/profile',
    template_folder='../../templates/admin/profile'
)


@mod.route('/')
@login_required
def view():
    """View authenticated user profile."""
    return render_template('profile.html', user=current_user)


@mod.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password of authenticated user."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.change_password(form.new_password.data)
        db.session.commit()
        return redirect(url_for('profile.view'))
    return render_template('change_password.html', form=form)


@mod.route('/change_username', methods=['GET', 'POST'])
@login_required
def change_username():
    """Change username of authenticated user."""
    form = ChangeUsernameForm(name=current_user.name)
    if form.validate_on_submit():
        current_user.name = form.name.data
        db.session.commit()
        return redirect(url_for('profile.view'))
    return render_template('change_name.html', form=form)
