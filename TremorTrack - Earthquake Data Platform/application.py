import pyodbc
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
import time
import redis
import random
import os

application = Flask(__name__)
application.config['SECRET_KEY'] = 'SecureSecretKey'
print(os.environ.get('PYTHONPATH'))


def connection():
    try:
        server = 'server_link'
        database = 'database_name'
        username = 'username'
        password = 'password'
        driver = '{ODBC Driver 18 for SQL Server}'
        conn = pyodbc.connect(
            'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        return conn
    except Exception as e:
        print(e)


def redisconnection():
    try:
        r = redis.StrictRedis(host='quiz3-meet.redis.cache.windows.net', port=6380, password='MBgXXuxbOaoZ0VfEoeOs0b5Kn06ES3KMMAzCaPoiFUg=', ssl=True)
        return r
    except Exception as e:
        print(e)


@application.route('/', methods=['GET', 'POST'])
def main():
    try:
        conn = connection()
        cursor = conn.cursor()
        msg = "Database Connected Successfully"
        return render_template('index.html', error=msg)
    except Exception as e:
        return render_template('index.html', error=e)


class EarthquakeForm(FlaskForm):
    start_time = IntegerField(label='Start Time: ', validators=[DataRequired()])
    end_time = IntegerField(label='End Time: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@application.route('/form1', methods=['GET', 'POST'])
def form1():
    try:
        form = EarthquakeForm()
        if form.validate_on_submit():
            conn = connection()
            cursor = conn.cursor()
            start_time = form.start_time.data
            end_time = form.end_time.data

            if start_time < 0 or end_time > 10**9: # Adjust the values according to the expected time range
                return render_template('form1.html', form=form, error='Time range must be reasonable')

            query = f'SELECT latitude, longitude, place, time FROM EarthquakeData WHERE time BETWEEN {start_time} AND {end_time}'

            t1 = time.time()
            cursor.execute(query)
            rows = cursor.fetchall()
            total_time = time.time() - t1
            time_per_tuple = total_time / len(rows) if rows else 0

            return render_template('form1.html', form=form, quakes=rows, total_time=total_time, time_per_tuple=time_per_tuple)

        return render_template('form1.html', form=form)

    except Exception as e:
        print(e)
        return render_template('form1.html', form=form, error=f'Error: {e}')


class Form2(FlaskForm):
    start_time = IntegerField(label='Start Time: ', validators=[DataRequired()])
    end_time = IntegerField(label='End Time: ', validators=[DataRequired()])
    num_quakes = IntegerField(label='Number of Quakes: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@application.route('/form2', methods=['GET', 'POST'])
def form2():
    try:
        form = Form2()
        if form.validate_on_submit():
            conn = connection()
            cursor = conn.cursor()
            start_time = form.start_time.data
            end_time = form.end_time.data
            num_quakes = form.num_quakes.data

            if start_time < 0 or end_time > 10**9:
                return render_template('form2.html', form=form, error='Time range must be reasonable')

            query = f'SELECT latitude, longitude, place, time FROM EarthquakeData WHERE time BETWEEN {start_time} AND {end_time}'

            t1 = time.time()
            cursor.execute(query)
            rows = cursor.fetchall()

            if num_quakes <= len(rows):
                selected_quakes = random.sample(rows, num_quakes)
            else:
                selected_quakes = random.choices(rows, k=num_quakes)

            query_time = time.time() - t1

            return render_template('form2.html', form=form, quakes=selected_quakes, query_time=query_time)

        return render_template('form2.html', form=form)

    except Exception as e:
        print(e)
        return render_template('form2.html', form=form, error=f'Error: {e}')



class Form3(FlaskForm):
    net = StringField(label='Net: ', validators=[DataRequired()])
    min_time = IntegerField(label='Minimum Time: ', validators=[DataRequired()])
    max_time = IntegerField(label='Maximum Time: ', validators=[DataRequired()])
    decrement = IntegerField(label='Decrement: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@application.route('/form3', methods=['GET', 'POST'])
def form3():
    try:
        form = Form3()
        if form.validate_on_submit():
            conn = connection()
            cursor = conn.cursor()
            net = form.net.data
            min_time = form.min_time.data
            max_time = form.max_time.data
            decrement = form.decrement.data

            query = f"""UPDATE EarthquakeData SET time = time - {decrement} WHERE net = '{net}' AND time BETWEEN {min_time} AND {max_time}"""
            t1 = time.time()
            cursor.execute(query)
            conn.commit()

            query = f"""SELECT time, latitude, longitude, mag, net, place FROM EarthquakeData WHERE net = '{net}' AND time BETWEEN {min_time} AND {max_time - decrement}"""
            cursor.execute(query)
            updated_quakes = cursor.fetchall()
            query_time = time.time() - t1

            count = len(updated_quakes)
            return render_template('form3.html', form=form, quakes=updated_quakes, count=count, query_time=query_time)

        return render_template('form3.html', form=form)

    except Exception as e:
        print(e)
        return render_template('form3.html', form=form, error=f'Error: {e}')


if __name__ == "__main__":
    application.run(debug=True)