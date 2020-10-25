from flask import Flask, request, jsonify, redirect, url_for, render_template
from forms.search import Search_form
import os
import webbrowser
from threading import Timer

app = Flask(__name__)

os.environ['APP_SETTINGS'] = 'config.DevelopmentConfig'
app.config['SECRET_KEY'] = 'root'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/",  methods=['GET', 'POST'])
def hello():
    return render_template('index.html', search_form=Search_form(request.form))


@app.route("/test",  methods=['GET', 'POST'])
def test():
    return render_template('test.html', search_form=Search_form(request.form))


@app.route("/search",  methods=['GET', 'POST'])
def search():
    s_f = Search_form(request.form)
    search_val = ''
    if request.method == 'POST':
        search_val = request.form['search_value']

    s_f.search_value.data = ''
    return render_template('search_result.html', search_form=s_f, search_value=search_val)


@app.route("/schedule_id_<id>", methods=['GET', 'POST'])
def schedule(id):
    # code to get data with id
    data = {
        'id': 0,
        'name': 'Example'
    }
    return render_template('schedule.html', sch_data=data, search_form=Search_form(request.form))


if __name__ == '__main__':
    Timer(2, webbrowser.open_new('http://127.0.0.1:5000/'))
    app.run()

