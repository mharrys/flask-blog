from flask.ext.wtf import Form, TextField, TextAreaField, validators, \
    HiddenField, BooleanField, PasswordField

from app.helpers import is_name
from app.models import User


class LoginForm(Form):
    username = TextField('Username', [
        validators.Required(),
        validators.length(min=1, max=64)
    ])
    password = PasswordField('Password', [
        validators.Required(),
        validators.length(min=1, max=64)
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


class CommentForm(Form):
    name = TextField('Name', [
        validators.Required(),
        validators.Length(min=2, max=50),
        is_name,
    ])
    body = TextAreaField('Comment', [
        validators.Required(),
        validators.Length(min=2, max=510),
    ])
    user_id = HiddenField('user_id')
    reply_id = HiddenField('reply_id')
