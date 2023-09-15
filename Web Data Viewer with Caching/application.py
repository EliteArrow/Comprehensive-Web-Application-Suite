import pyodbc
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import time
import redis
import hashlib
import os
import pickle


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
        r = redis.StrictRedis(host='host_name.redis.cache.windows.net', port=6380, password='password', ssl=True)
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


class Form1(FlaskForm):
    num = StringField(label='No. of Query Execution: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@application.route('/form1', methods=['GET', 'POST'])
def form1():
    try:
        form = Form1()
        if form.validate_on_submit():
            conn = connection()
            cursor = conn.cursor()
            r = redisconnection()
            num = int(form.num.data)

            if num < 1 or num > 1000:
                return render_template('form1.html', form=form, error='No. of Queries must be between 1 and 1000')

            query = 'SELECT time from EarthquakeData'
            key = hashlib.sha224(query.encode()).hexdigest()

            # Check if data is in Redis
            rows = r.get(key)

            # If not, get data from DB and store in Redis
            if not rows:
                cursor.execute(query)
                rows = cursor.fetchall()
                # Convert row objects to list of dictionaries
                rows = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
                # We're storing the entire result set as a serialized string
                r.set(key, pickle.dumps(rows))

            diff1 = 0
            for i in range(num):
                # timing DB query
                start1 = time.time()
                cursor.execute(query)
                cursor.fetchall()
                diff1 += time.time() - start1

            # timing Redis query
            start2 = time.time()
            # Deserialize the string back into Python object
            rows = pickle.loads(r.get(key))
            diff2 = time.time() - start2

            return render_template('form1.html', form=form, num=num, diff1=diff1, diff2=diff2, data=1)

        return render_template('form1.html', form=form)

    except Exception as e:
        print(e)
        return render_template('form1.html', form=form, error=f'Error: {e}')




class Form2(FlaskForm):
    num = StringField(label='No. of Query Execution: ', validators=[DataRequired()])
    mag1 = StringField(label='Lower Magnitude Range: ', validators=[DataRequired()])
    mag2 = StringField(label='Upper Magnitude Range: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@application.route('/form2', methods=['GET', 'POST'])
def form2():
    try:
        form = Form2()
        if form.validate_on_submit():
            conn = connection()
            cursor = conn.cursor()
            r = redisconnection()
            num = int(form.num.data)
            mag1 = float(form.mag1.data)
            mag2 = float(form.mag2.data)

            if num < 1 or num > 1000:
                return render_template('form2.html', form=form, error='No. of Queries must be between 1 and 1000')

            if mag1 > mag2:
                return render_template('form2.html', form=form, error='Lower Magnitude Range must be lower than Higher Magnitude Range')

            r.flushall()
            query = f'SELECT time from EarthquakeData where mag between {mag1} and {mag2}'
            key = hashlib.sha224(query.encode()).hexdigest()

            # Check if data is in Redis
            rows = r.get(key)

            # If not, get data from DB and store in Redis
            if not rows:
                cursor.execute(query)
                rows = cursor.fetchall()
                # Convert row objects to list of dictionaries
                rows = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
                # We're storing the entire result set as a serialized string
                r.set(key, pickle.dumps(rows))

            t1 = time.time()
            for i in range(num):
                cursor.execute(query)
                cursor.fetchall()
            diff1 = time.time() - t1

            t1 = time.time()
            # Deserialize the string back into Python object
            rows = pickle.loads(r.get(key))
            diff2 = time.time() - t1

            return render_template('form2.html', form=form, num=num, mag1=mag1, mag2=mag2, diff1=diff1, diff2=diff2, data=1)

        return render_template('form2.html', form=form)

    except Exception as e:
        print(e)
        return render_template('form2.html', form=form, error=f'Error: {e}')


if __name__ == "__main__":
    application.run(debug=True)