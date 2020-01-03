from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from sqlalchemy import or_
from flask_login import current_user, login_required
from scurry import db
from scurry.models import Post, User, PostShare
from scurry.posts.forms import PostForm

posts = Blueprint('posts', __name__)

@posts.route('/post', methods=['GET', 'POST'])
def new_post():
    postForm = PostForm()
    if postForm.validate_on_submit():
        post = Post(private=postForm.private.data, content=postForm.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post Created!', 'success')
        return redirect(request.referrer)
    return render_template('post.html', title="Create Post", postForm=postForm)

@posts.route('/underground', methods=['GET', 'POST'])
@login_required
def underground():
    postForm = PostForm()
    if postForm.validate_on_submit():
        post = Post(private=postForm.private.data, content=postForm.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post Created!', 'success')
        return redirect(request.referrer)
    page = request.args.get('page', 1, type=int)
    shared_posts = Post.query.filter(Post.shares) #.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    private_posts = Post.query.filter_by(private=True)
    posts = shared_posts.union(private_posts).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('underground.html', title="Underground Feed", postForm=postForm, posts=posts)

@posts.route('/burrow', methods=['GET', 'POST'])
@login_required
def burrow():
    postForm = PostForm()
    if postForm.validate_on_submit():
        post = Post(private=postForm.private.data, content=postForm.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post Created!', 'success')
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = user.followed_posts().paginate(page=page, per_page=5)
    return render_template('burrow.html', postForm=postForm, title="My Burrow", posts=posts)

@posts.route('/like/<int:post_id>/<action>')  
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)

@posts.route('/post/share/<int:post_id>')
@login_required
def share_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author == current_user:
        abort(404)
    # new_post = Post(private=True, author=post.author, content=post.content)
    current_user.share_post(post)
    # db.session.add(post)
    db.session.commit()
    flash('Post has been shared', 'success')
    return redirect(url_for('posts.underground'))

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)
 
@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    postForm = PostForm()
    if postForm.validate_on_submit():
        post.content = postForm.content.data
        db.session.commit()
        flash('Post has been updated', 'success')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        postForm.content.data = post.content
    return render_template('post.html', title='Update post', 
                            postForm=postForm)


@posts.route('/post/<int:post_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been Deleted', 'success')
    return redirect(url_for('main.index'))


