from app import db
from app.models import Post, Comment
from flask import Blueprint, render_template, redirect, url_for, request
from flask.ext.login import login_required

mod = Blueprint(
    'comment',
    __name__,
    url_prefix='/admin/comment',
    template_folder='../../templates/admin/comment'
)


@mod.route('/comments/<path:slug>')
@login_required
def view_for_post(slug):
    """View comments for specified slug."""
    post = Post.query.slug_or_404(slug=slug, show_hidden=True)
    return render_template('comments.html', post=post, comments=post.comments)


@mod.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    """Delete comment with specified id."""
    comment = Comment.query.get_or_404(id)
    if request.method == 'POST':
        post_id = comment.post_id
        db.session.delete(comment)
        db.session.commit()
        # redirect to the remaining post comments
        slug = Post.query.get_or_404(post_id).slug
        return redirect(url_for('comment.post_comments', slug=slug))
    return render_template(
        'delete.html',
        title='Delete Comment',
        what='comment',
        action=url_for('comment.delete', id=comment.id)
    )
