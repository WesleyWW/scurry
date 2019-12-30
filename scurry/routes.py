from flask import render_template, url_for, flash, redirect
from scurry import app, db, bcrypt
from scurry.forms import RegistrationForm, LoginForm, PostForm
from scurry.models import User, Post

posts = [
    {
        'author': 'Wesley',
        'title': 'Post Title 123',
        'content': 'Post Content 123, The First post',
        'date_posted': '12-28-19',
        'likes': '12'
    },
    {
        'author': 'Wesley',
        'title': 'Post Title 234',
        'content': 'The Second post, Post Content 234',
        'date_posted': '12-28-19',
        'likes': '2'
    },
    {
        'author': 'ShoNuff',
        'title': 'Post Title 3456',
        'content': 'Some Random content text for this post',
        'date_posted': '12-28-19',
        'likes': '62'
    }
]

user = {
        'username': 'Wesley',
        'email': 'wesley@gmail.com',
        'password': '123'
    }



@app.route('/')
@app.route('/home')
def index():
    form = PostForm()
    return render_template('home.html', title='Home', posts=posts, user=user, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
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
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'wes@gmail.com' and form.password.data == '123':
            flash(f'Logged in successfully!', 'success')
            return redirect(url_for('profile'))
        else:
            flash(f'Login Unsuccessful. Please check credentials', 'danger')
    return render_template('login.html', title="Login", form=form)

@app.route('/post', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    return render_template('create_post.html', title="Create Post", form=form)

@app.route('/profile')
def profile():
    return render_template('profile.html', title="Profile", user=user, posts=posts)