from flask.ext.login import current_user
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, BooleanField, PasswordField, \
    SubmitField
from wtforms.validators import Required, length, EqualTo, ValidationError

from app.helpers import is_name
from app.models import User


class PostForm(Form):
    title = TextField('Title', [
        Required(),
        length(min=1, max=256)
    ])
    markup = TextAreaField('Markup', [
        Required()
    ])
    visible = BooleanField('Visible to public', default=False)


class LoginForm(Form):
    username = TextField('Username', [
        Required(),
        length(min=1, max=64)
    ])
    password = PasswordField('Password', [
        Required(),
        length(min=1, max=64)
    ])
    remember_me = BooleanField('Remember me', default=False)

    def validate(form):
        """Validate login credentials.

        The error messages has been purposely left out so an attacker gain no
        knowledge which field is wrong.

        """
        # Validate built in validators
        if not Form.validate(form):
            return False
        # Validate user credentials
        username = form.username.data
        password = form.password.data
        form.user = User.query.filter_by(name=username).first()
        if not form.user or not form.user.compare_password(password):
            return False
        # Successfully validated
        return True


class ChangePasswordForm(Form):
    password = PasswordField('Current Password', [
        Required(),
        length(min=1, max=64)
    ])
    new_password = PasswordField('New Password', [
        Required(),
        length(min=1, max=64),
        EqualTo('confirm', message='Passwords must match.'),
    ])
    confirm = PasswordField('Confirm New Password', [
        Required(),
        length(min=1, max=64)
    ])
    submit = SubmitField('Change Password')

    def validate_password(form, field):
        password = field.data
        if not current_user.compare_password(password):
            raise ValidationError('Current password is wrong.')


class ChangeUsernameForm(Form):
    username = TextField('New Username', [
        Required(),
        length(min=2, max=64),
        is_name
    ])
    submit = SubmitField('Change Username')

    def validate_username(form, field):
        username = field.data
        form.user = User.query.filter_by(name=username).first()
        if form.user:
            raise ValidationError('Username already exists.')
