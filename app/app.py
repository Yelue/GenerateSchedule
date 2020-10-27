from flask import Flask, request, jsonify, redirect, url_for, render_template
from forms.search import Search_form
from forms.new_schedule import New_schedule_form
import os
import webbrowser
from threading import Timer
from werkzeug.utils import secure_filename

from numpy import random as rd

app = Flask(__name__)

os.environ['APP_SETTINGS'] = 'config.DevelopmentConfig'
app.config['SECRET_KEY'] = 'root'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = './uploads'

@app.route("/",  methods=['GET', 'POST'])
def hello():
    return render_template('index.html',
                            search_form=Search_form(request.form),
                            new_schedule_form=New_schedule_form(request.form))


@app.route("/test",  methods=['GET', 'POST'])
def test():
    return render_template('test.html',
                            search_form=Search_form(request.form))


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


@app.route("/schedule_id_<id>", methods=['GET', 'POST'])
def schedule(id):
    # code to get data with id
    data = {
        'id': 0,
        'name': 'Example'
    }
    return render_template('schedule.html',
                            sch_data=data,
                            search_form=Search_form(request.form))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        upload_data = {
                        'email': request.form['email'],
                        'name': request.form['name']
                      }

        file = request.files['teachers']
        print(os.path.splitext(secure_filename(file.filename)))
        folder_name = '/' + str(rd.randint(0, 9999))
        os.mkdir(app.config['UPLOAD_FOLDER'] + folder_name)
        for f in request.files:
            file = request.files[f]
            filename = f + os.path.splitext(secure_filename(file.filename))[1]
            file.save(
                        os.path.join(app.config['UPLOAD_FOLDER'] + folder_name,
                                        filename)
                     )
    return render_template('upload.html',
                            search_form=Search_form(request.form),
                            data=upload_data)


if __name__ == '__main__':
    app.run()