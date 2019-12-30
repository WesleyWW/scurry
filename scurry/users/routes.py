from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from scurry import db, bcrypt
from scurry.models import User, Post
from scurry.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from scurry.users.utils import save_picture
from scurry.posts.forms import PostForm

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title="Register", form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful, please check credentials', 'danger')
    return render_template('login.html', title="Login", form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

# Get User Posts
@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    accountForm = UpdateAccountForm()
    if accountForm.validate_on_submit():
        if accountForm.picture.data:
            picture_file = save_picture(accountForm.picture.data)
            current_user.image_file = picture_file
        current_user.username = accountForm.username.data
        current_user.email = accountForm.email.data
        db.session.commit()
        flash('Account has been updated!', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        accountForm.username.data = current_user.username
        accountForm.email.data = current_user.email
    postForm = PostForm()
    if postForm.validate_on_submit():
        post = Post(content=postForm.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post Created!', 'success')
        return redirect(url_for('main.index'))
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('profile.html', title="Profile", 
                            userForm=accountForm, postForm=postForm,
                            image_file=image_file)
