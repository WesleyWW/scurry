import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from scurry import app, db, bcrypt
from scurry.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from scurry.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


# posts = [
#     {
#         'author': 'Wesley',
#         'title': 'Post Title 123',
#         'content': 'Post Content 123, The First post',
#         'date_posted': '12-28-19',
#         'likes': '12'
#     },
#     {
#         'author': 'Wesley',
#         'title': 'Post Title 234',
#         'content': 'The Second post, Post Content 234',
#         'date_posted': '12-28-19',
#         'likes': '2'
#     },
#     {
#         'author': 'ShoNuff',
#         'title': 'Post Title 3456',
#         'content': 'Some Random content text for this post',
#         'date_posted': '12-28-19',
#         'likes': '62'
#     }
# ]

# user = {
#         'username': 'Wesley',
#         'email': 'wesley@gmail.com',
#         'password': '123'
#     }



@app.route('/')
@app.route('/home')
def index():
    form = PostForm()
    posts = Post.query.all()
    return render_template('home.html', title='Home', posts=posts, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful, please check credentials', 'danger')
    return render_template('login.html', title="Login", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/post', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    return render_template('post.html', title="Create Post", form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.content = form.content.data
        db.session.commit()
        flash('Post has been updated', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.content.data = post.content
    return render_template('post.html', title='Update post', 
                            form=form)


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been Deleted', 'success')
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
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
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        accountForm.username.data = current_user.username
        accountForm.email.data = current_user.email
    postForm = PostForm()
    if postForm.validate_on_submit():
        post = Post(content=postForm.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post Created!', 'success')
        return redirect(url_for('index'))
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('profile.html', title="Profile", 
                            userForm=accountForm, postForm=postForm,
                            image_file=image_file)
