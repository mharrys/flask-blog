from flask.ext.wtf import Form, TextField, TextAreaField, validators, \
    HiddenField

from app.helpers import is_name


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
