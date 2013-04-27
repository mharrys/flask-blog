from app.helpers import is_name
from app.models import Post, User
from flask.ext.wtf import Form, TextField, TextAreaField, validators, \
    ValidationError, HiddenField, PasswordField, BooleanField


class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    remember = BooleanField('Remember me')

    def validate(self):
        """Verify login credentials."""
        if not Form.validate(self):
            return False
        self.user = User.query.filter_by_name(self.username.data)
        # valid username?
        if not self.user:
            self.username.errors.append('Unknown username.')
            return False
        # valid password?
        if not self.user.compare_password(self.password.data):
            self.user = None
            self.password.errors.append('Invalid password.')
            return False
        # successfully verified
        return True


class EditUserForm(Form):
    name = TextField('Name', [
        validators.Required(),
        validators.Length(min=2, max=50),
        is_name
    ])


class UserForm(EditUserForm):
    password = PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match.'),
    ])
    confirm = PasswordField('Confirm password', [
        validators.Required(),
    ])


class PostForm(Form):
    prev_title = HiddenField('Previous Title')
    title = TextField('Title', [validators.Required()])
    body = TextAreaField('Body', [validators.Required()])
    visible = BooleanField('Visible')

    def validate_title(form, field):
        title = field.data
        # avoid name clash when editing post
        if form.prev_title.data == title:
            return
        # check if there is a post on this date and title
        if Post.query.filter_by_title_today(title):
            raise ValidationError('Title already exist on this date.')


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
