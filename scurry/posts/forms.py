from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    public = BooleanField('Make Public')
    submit = SubmitField('Post')