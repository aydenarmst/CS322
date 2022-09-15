from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import  DataRequired, Length, DataRequired

from app.Model.models import Post

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Post Message', [Length(min=1, max=1500)])
    happiness_level = SelectField('Happiness Level',choices = [(3, 'I can\'t stop smiling'), (2, 'Really happy'), (1,'Happy')])
    submit = SubmitField('Post')
