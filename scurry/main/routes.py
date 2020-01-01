from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user
from scurry import db
from scurry.models import Post, User
from scurry.posts.forms import PostForm

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home', methods=['POST', 'GET'])
def index():
    postForm = PostForm()
    if postForm.validate_on_submit():
        post = Post(private=postForm.private.data, content=postForm.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post Created!', 'success')
    
    user = User.query.filter_by(username=current_user.username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(private=False).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', title='Home', posts=posts, user=user, postForm=postForm)

