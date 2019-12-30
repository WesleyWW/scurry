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







