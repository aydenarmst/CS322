from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import  DataRequired, Length, DataRequired
from wtforms.widgets import ListWidget, CheckboxInput

from app.Model.models import Post, Tag



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Post Message', [Length(min=1, max=1500)])
    happiness_level = SelectField('Happiness Level',choices = [(3, 'I can\'t stop smiling'), (2, 'Really happy'), (1,'Happy')])
    tag = QuerySelectMultipleField('Tags', query_factory=lambda: Tag.query.all(), get_label=lambda x: x.name, widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
    submit = SubmitField('Post')

class SortForm(FlaskForm):
    sort = SelectField('Sort',choices = [(1,'Date'), (2,'Title'), (3,'Happiness Level'), (4,'# of likes')])
    submit = SubmitField('Refresh')