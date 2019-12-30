from flask import render_template, request, Blueprint
from scurry.models import Post
from scurry.posts.forms import PostForm

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def index():
    form = PostForm()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', title='Home', posts=posts, form=form)

