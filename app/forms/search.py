from flask_wtf import Form
from wtforms import SubmitField, ValidationError, StringField
from wtforms.validators import DataRequired

class Search_form(Form):
	search_value = StringField(validators=[DataRequired()])
	submit = SubmitField("Search")