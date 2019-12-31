from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    private = BooleanField('Make Private')
    submit = SubmitField('Post') 