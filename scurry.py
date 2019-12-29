from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, PostForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '2d6d7cc921s64dcdgh8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='noprofile.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.content}', '{self.date_posted}')"

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
    return render_template('home.html', title='Home', posts=posts, user=user, form=form)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
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