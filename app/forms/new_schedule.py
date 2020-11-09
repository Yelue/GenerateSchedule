from flask_wtf import FlaskForm
from wtforms import SubmitField, ValidationError, StringField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired

class New_schedule_form(FlaskForm):
    email = StringField(validators=[InputRequired()])
    name = StringField(validators=[InputRequired()])
    teachers = FileField(validators=[FileRequired()])
    subjects = FileField(validators=[FileRequired()])
    groups = FileField(validators=[FileRequired()])
    faculty = FileField(validators=[FileRequired()])
    departments = FileField(validators=[FileRequired()])
    load_list = FileField(validators=[FileRequired()])
    teacher_emails = FileField(validators=[FileRequired()])
    student_emails = FileField(validators=[FileRequired()])
    submit = SubmitField("Підтвердити")
