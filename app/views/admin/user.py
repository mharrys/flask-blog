from app import db
from app.forms import RegisterUserForm
from app.models import User
from flask import Blueprint, render_template, redirect, url_for, request
from flask.ext.login import login_required

mod = Blueprint(
    'user',
    __name__,
    url_prefix='/admin/user',
    template_folder='../../templates/admin/user'
)


@mod.route('/')
@login_required
def overview():
    """View user overview."""
    users = User.query.filter_by_latest()
    return render_template('users.html', users=users)


@mod.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    """Create new user."""
    form = RegisterUserForm()
    if form.validate_on_submit():
        user = User(form.name.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.overview'))
    return render_template('new_user.html', form=form)


@mod.route('/delete/<name>', methods=['GET', 'POST'])
@login_required
def delete(name):
    """Delete user by specified username."""
    user = User.query.filter_by_name_or_404(name)
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('user.overview'))
    return render_template(
        'delete.html',
        title='Delete User',
        what=user.name,
        action=url_for('user.delete', name=user.name)
    )
