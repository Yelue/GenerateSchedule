from flask import Flask, request, jsonify, redirect, url_for, render_template
import json
import os
from threading import Timer
from werkzeug.utils import secure_filename
from numpy import random as rd
from flask_sqlalchemy import SQLAlchemy

from app.forms.search import Search_form
from app.forms.new_schedule import New_schedule_form
from app.tasks import load_db


app = Flask(__name__)
#need to move to config.py
os.environ['APP_SETTINGS'] = 'config.DevelopmentConfig'
app.config['SECRET_KEY'] = 'root'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = 'app/uploads'
#need to add to environment variables
username = 'wcqtmsosaglntk'
password = '9f6497000b9a5f82fd288a15597cc09876c377b17f1b521848bc12a2f42577ef'
database = 'dful1hqqvuc8a0'
host = 'ec2-34-253-148-186.eu-west-1.compute.amazonaws.com'
port = '5432'

ENGINE_PATH_WIN_AUTH = f'postgres://{username}:{password}@{host}:{port}/{database}'
app.config['SQLALCHEMY_DATABASE_URI'] = ENGINE_PATH_WIN_AUTH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

db.create_all()

load_db(db.engine)

@app.route("/",  methods=['GET', 'POST'])
def hello():
    return render_template('index.html',
                            search_form=Search_form(request.form),
                            new_schedule_form=New_schedule_form(request.form))


@app.route("/test",  methods=['GET', 'POST'])
def test():
    return render_template('test.html',
                            search_form=Search_form(request.form))


@app.route('/postmethod', methods = ['GET', 'POST'])
def get_post_javascript_data():
    data = json.loads(request.form['javascript_data'])

    json_to_DB = {
        'day1': [0, 0, 0, 0, 0, 0],
        'day2': [0, 0, 0, 0, 0, 0],
        'day3': [0, 0, 0, 0, 0, 0],
        'day4': [0, 0, 0, 0, 0, 0],
        'day5': [0, 0, 0, 0, 0, 0],
        'day6': [0, 0, 0, 0, 0, 0],
        'day7': [0, 0, 0, 0, 0, 0],
        'day8': [0, 0, 0, 0, 0, 0],
        'day9': [0, 0, 0, 0, 0, 0],
        'day10':[0, 0, 0, 0, 0, 0],
        'day11':[0, 0, 0, 0, 0, 0],
        'day12':[0, 0, 0, 0, 0, 0]
    }

    for lesson in data:
        day = 'day' + str(lesson['day'] + 6*lesson['week'] + 1)
        json_to_DB[day][lesson['les_num']] = lesson['les_id']

    for i in json_to_DB:
        print(i, ': ', json_to_DB[i])

    return '', 200


@app.route("/search",  methods=['GET', 'POST'])
def search():
    s_f = Search_form(request.form)
    search_val = ''
    if request.method == 'POST':
        search_val = request.form['search_value']

    s_f.search_value.data = ''
    return render_template('search_result.html',
                            search_form=s_f,
                            search_value=search_val)


@app.route("/schedule_id_<id>_w_<w_num>", methods=['GET', 'POST'])
def schedule(id, w_num):
    # code to get data with id
    data = {
        'id': 0,
        'name': 'Example'
    }
    week_active = ['active', ''] if w_num == '1' else ['', 'active']
    return render_template('schedule.html',
                            week_active=week_active,
                            sch_data=data,
                            search_form=Search_form(request.form))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        upload_data = {
                        'email': request.form['email'],
                        'name': request.form['name']
                      }
        file_names = ['table_teacher',
                      'table_lesson',
                      'table_groups',
                      'table_faculty',
                      'table_depart',
                      'table_cards',
                      'table_teacher_emails',
                      'table_student_emails']
        file = request.files['teachers']
        print(os.path.splitext(secure_filename(file.filename)))
        folder_name = '/' + str(rd.randint(0, 9999))
        os.mkdir(app.config['UPLOAD_FOLDER'] + folder_name)

        for f, new_name in zip(request.files, file_names):
            file = request.files[f]
            filename = new_name + os.path.splitext(secure_filename(file.filename))[1]
            file.save(
                        os.path.join(app.config['UPLOAD_FOLDER'] + folder_name,
                                        filename)
                     )
    return render_template('upload.html',
                            search_form=Search_form(request.form),
                            data=upload_data)


if __name__ == '__main__':
    app.run()
