from flask import Flask, request, jsonify, redirect, url_for, render_template
import json
import os
from threading import Timer
from werkzeug.utils import secure_filename
from numpy import random as rd
from flask_sqlalchemy import SQLAlchemy
import shutil

from app.forms.search import Search_form
from app.forms.new_schedule import New_schedule_form
from app.tasks import load_db, prepare_random_schedule,\
                        prepare_schedule_interface,\
                        load_schedule_db,search_schedule, \
                        check_schedule, genetic_algorithm


app = Flask(__name__)
#need to move to config.py
# os.environ['APP_SETTINGS'] = 'config.DevelopmentConfig'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = int(os.environ.get('SEND_FILE_MAX_AGE_DEFAULT'))
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER')

#need to add to environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = bool(int(os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')))

db = SQLAlchemy(app)

db.create_all()


@app.route("/",  methods=['GET', 'POST'])
def index():
    return render_template('index.html',
                            search_form=Search_form(request.form),
                            new_schedule_form=New_schedule_form(request.form))


@app.route("/scheduledesign",  methods=['GET', 'POST'])
def scheduledesign():
    temp_data = prepare_schedule_interface(db=db)
    return render_template('schedule_design.html',
                            data=temp_data,
                            search_form=Search_form(request.form))


@app.route("/loadfiles",  methods=['GET', 'POST'])
def schedule_files_load():
    return render_template('load_forms.html',
                            search_form=Search_form(request.form),
                            new_schedule_form=New_schedule_form(request.form))


@app.route('/post_desired_schedule', methods = ['GET', 'POST'])
def get_desired_schedule():
    data = json.loads(request.form['javascript_data'])

    load_schedule_db(data=data, db=db)
    return '', 200


@app.route("/no_schedule",  methods=['GET', 'POST'])
def search():
    s_f = Search_form(request.form)
    search_query = ''
    if request.method == 'POST':
        search_query = request.form['search_value'].strip()


    s_f.search_value.data = ''
    if check_schedule(db, search_query):
        return redirect(f'/schedule_{search_query}_w_1')
    else:
        return render_template('search_result.html',
                               search_form=s_f,
                               search_value=search_query)


@app.route("/schedule_<name>_w_<w_num>", methods=['GET', 'POST'])
def schedule(name, w_num):
    search_type, schedule = search_schedule(db, name)
    schedule = schedule[f'week{w_num}']
    week_active_dropdown = ['active disabled', ''] if w_num == '1' else ['', 'active disabled']
    return render_template('schedule.html',
                            week_active_dropdown=week_active_dropdown,
                            search_type=search_type,
                            schedule=schedule,
                            name=name,
                            search_form=Search_form(request.form))


@app.route('/upload_files', methods=['GET', 'POST'])
def upload_files():
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
    load_db(db.engine)
    shutil.rmtree(app.config['UPLOAD_FOLDER'] + folder_name)
    return render_template('upload.html',
                            search_form=Search_form(request.form),
                            data=upload_data)





if __name__ == '__main__':
    app.run()
