import pyodbc
from datetime import datetime, timedelta
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from geopy.distance import geodesic
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


@application.route('/', methods=['GET', 'POST'])
def main():
    try:
        conn = connection()
        cursor = conn.cursor()
        msg = "Database Connected Successfully"
        return render_template('index.html', error=msg)
    except Exception as e:
        return render_template('index.html', error=e)


#Search by Magnitude


class Form1(FlaskForm):
    mag = StringField(label='Enter Magnitude: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@application.route('/form1', methods=['GET', 'POST'])
def form1():
    form = Form1()
    cnt = 0
    if form.validate_on_submit():
        try:
            conn = connection()
            cursor = conn.cursor()
            mag = float(form.mag.data)
            if mag <= 5.0:
                return render_template('form1.html', form=form, error="Magnitude must be > 5.0", data=0)

            cursor.execute("SELECT * FROM EarthquakeData where mag > ?", mag)
            result = []
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                result.append(row)
                cnt += 1
            return render_template('form1.html', result=result, cnt=cnt, mag=mag, form=form, data=1)

        except Exception as e:
            print(e)
            return render_template('form1.html', form=form, error=f"Magnitude must be numeric. Error: {e}", data=0)


    return render_template('form1.html', form=form)


#Search by Range & Days


class Form2(FlaskForm):
    r1 = StringField(label='Enter Magnitude Range 1: ', validators=[DataRequired()])
    r2 = StringField(label='Enter Magnitude Range 2: ', validators=[DataRequired()])
    days = StringField(label='Enter Days: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@application.route('/form2', methods=['GET', 'POST'])
def form2():
    form = Form2()
    if form.validate_on_submit():
        try:
            conn = connection()
            cursor = conn.cursor()

            r1 = float(form.r1.data)
            r2 = float(form.r2.data)
            days = int(form.days.data) + 4

            if days - 4 > 30:
                return render_template('form2.html', form=form, error="Days must be less than or equal to 30.", data=0)
            if r1 > r2:
                return render_template('form2.html', form=form, error="Range 1 must be less than Range 2.", data=0)
            if days < 0 or r1 < 0 or r2 < 0:
                return render_template('form2.html', form=form, error="Input must be non-negative.", data=0)

            # Define today as the current date in UTC at the beginning of the day
            today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            days_ago = today - timedelta(days=days)

            cursor.execute("SELECT * FROM EarthquakeData where time >= ? AND mag BETWEEN ? AND ?", days_ago, r1, r2)

            result = []
            cnt = 0
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                result.append(row)
                cnt += 1

            return render_template('form2.html', result=result, cnt=cnt, r1=r1, r2=r2, days=days - 4, form=form, data=1)

        except Exception as e:
            return render_template('form2.html', form=form, error=f"An error occurred: {e}", data=0)

    return render_template('form2.html', form=form, data=0)




#Search by Location


class Form3(FlaskForm):
    lat = StringField(label='Enter Latitude: ', validators=[DataRequired()])
    lon = StringField(label='Enter Longitude: ', validators=[DataRequired()])
    km = StringField(label='Enter Kilometers: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@application.route('/form3', methods=['GET', 'POST'])
def form3():
    form = Form3()
    if form.validate_on_submit():
        try:
            conn = connection()
            cursor = conn.cursor()
            lat = float(form.lat.data)
            lon = float(form.lon.data)
            km = float(form.km.data)
            cnt = 0

            cursor.execute("SELECT time, latitude, longitude, mag, id, place, type FROM EarthquakeData")
            result = []
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                if geodesic((float(row[1]), float(row[2])), (lat, lon)).km <= km:
                    result.append(row)
                    cnt += 1
            return render_template('form3.html', result=result, cnt=cnt, lat=lat, lon=lon, km=km, form=form, data=1)

        except Exception as e:
            print(e)
            return render_template('form3.html', form=form, error=f"Latitude must be in the [-90; 90] range, Latitude must be in [-180; 180] and all input must be numaric. Error: {e}")
    return render_template('form3.html', form=form, data=0)


#Search by Clusters


@application.route('/form4', methods=['GET', 'POST'])
def form4():
    if request.method == 'POST':
        try:
            conn = connection()
            cursor = conn.cursor()
            clus = request.form['clus']
            cnt = 0

            cursor.execute("SELECT * FROM EarthquakeData where type = ?", clus)
            result = []
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                result.append(row)
                cnt += 1
            return render_template('form4.html', result=result, cnt=cnt, clus=clus, data=1)

        except Exception as e:
            print(e)
            return render_template('form4.html', error=f"Range 1 and Range 2 must be numeric, Range 1 > Range 2 and Days must be integer and less then 31. Error: {e}", data=0)

    return render_template('form4.html', data=0)


#Does given Magnitude occur more often at night?

@application.route('/form5', methods=['GET', 'POST'])
def form5():
    cnt = 0
    tot_cnt = 0
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute('select * from EarthquakeData where mag > 4.0')
        result = []
        while True:
            row = cursor.fetchone()
            if not row:
                break
            hour = row[0].hour  # Change this line
            if hour > 18 or hour < 7:
                result.append(row)
                cnt += 1
            tot_cnt += 1
        return render_template('form5.html', result=result, cnt=cnt, tot_cnt=tot_cnt, data=1)

    except Exception as e:
        print(e)  # this will print the error message to the console
        return render_template('form5.html', error=str(e), data=0)  # and this will display it on the webpage


if __name__ == "__main__":
    application.run(debug=True)