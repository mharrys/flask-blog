from flask import Blueprint, render_template
from flask.ext.login import login_required

mod = Blueprint(
    'admin',
    __name__,
    url_prefix='/admin',
    template_folder='../../templates/admin'
)


@mod.route('/')
@login_required
def overview():
    """View admin overview."""
    return render_template('overview.html')
