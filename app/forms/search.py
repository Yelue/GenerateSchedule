from flask_wtf import FlaskForm
from wtforms import SubmitField, ValidationError, StringField
from wtforms.validators import DataRequired


class Search_form(FlaskForm):
	search_value = StringField(validators=[DataRequired()])
	submit = SubmitField("Шукати")
