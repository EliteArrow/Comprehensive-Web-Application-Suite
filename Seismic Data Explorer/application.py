import pyodbc
from datetime import datetime, timedelta
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired
from geopy.distance import geodesic


application = Flask(__name__)
application.config['SECRET_KEY'] = 'SecureSecretKeyQuiz'


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


class EarthquakeForm(FlaskForm):
    time = IntegerField('Enter Time:', validators=[DataRequired()])
    submit = SubmitField('Submit')


@application.route('/earthquake', methods=['GET', 'POST'])
def earthquake():
    form = EarthquakeForm()
    details = None
    nearby_quakes = None

    if form.validate_on_submit():
        time = form.time.data
        conn = connection()
        cursor = conn.cursor()
        # Query to get the earthquake at the specified time
        cursor.execute("SELECT * FROM EarthquakeData WHERE time=?", time)
        details = cursor.fetchone()

        if details:
            # Query to get earthquakes within +-2 latitude
            latitude = details[1]
            cursor.execute("SELECT * FROM EarthquakeData WHERE latitude BETWEEN ? AND ?",
                           latitude - 2, latitude + 2)
            nearby_quakes = cursor.fetchall()

        conn.close()

    return render_template('form1.html', form=form, details=details, nearby_quakes=nearby_quakes)


class Form2(FlaskForm):
    lat_min = StringField(label='Min Latitude: ', validators=[DataRequired()])
    lon_min = StringField(label='Min Longitude: ', validators=[DataRequired()])
    lat_max = StringField(label='Max Latitude: ', validators=[DataRequired()])
    lon_max = StringField(label='Max Longitude: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

@application.route('/form2', methods=['GET', 'POST'])
def form2():
    form = Form2()
    if form.validate_on_submit():
        lat_min = float(form.lat_min.data)
        lon_min = float(form.lon_min.data)
        lat_max = float(form.lat_max.data)
        lon_max = float(form.lon_max.data)
        try:
            with connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT time, latitude, longitude, mag, net, place FROM EarthquakeData WHERE latitude BETWEEN ? AND ? AND longitude BETWEEN ? AND ?",
                        (lat_min, lat_max, lon_min, lon_max)
                    )
                    earthquakes = cursor.fetchall()
            return render_template('form2.html', earthquakes=earthquakes, form=form, data=1)
        except Exception as e:
            print(e)
            return render_template('form2.html', form=form, error=str(e))
    return render_template('form2.html', form=form)

class Form3(FlaskForm):
    net_value = StringField(label='Net Value: ', validators=[DataRequired()])
    mag_min = FloatField(label='Min Mag: ', validators=[DataRequired()])
    mag_max = FloatField(label='Max Mag: ', validators=[DataRequired()])
    increment = FloatField(label='Mag Increment: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@application.route('/form3', methods=['GET', 'POST'])
def form3():
    form = Form3()
    if form.validate_on_submit():
        net_value = form.net_value.data
        mag_min = form.mag_min.data
        mag_max = form.mag_max.data
        increment = form.increment.data
        try:
            with connection() as conn:
                with conn.cursor() as cursor:
                    # Updating earthquake mag
                    cursor.execute(
                        "UPDATE EarthquakeData SET mag = mag + ? WHERE net = ? AND mag BETWEEN ? AND ?",
                        (increment, net_value, mag_min, mag_max)
                    )

                    # Getting updated earthquakes
                    cursor.execute(
                        "SELECT time, latitude, longitude, mag, net, place FROM EarthquakeData WHERE net = ? AND mag BETWEEN ? AND ?",
                        (net_value, mag_min, mag_max + increment)
                    )
                    updated_earthquakes = cursor.fetchall()
                    count = len(updated_earthquakes)

            return render_template('form3.html', earthquakes=updated_earthquakes, count=count, form=form, data=1)
        except Exception as e:
            print(e)
            return render_template('form3.html', form=form, error=str(e))
    return render_template('form3.html', form=form)


class Form4(FlaskForm):
    time = StringField(label='Time: ', validators=[DataRequired()])
    latitude = StringField(label='Latitude: ', validators=[DataRequired()])
    longitude = StringField(label='Longitude: ', validators=[DataRequired()])
    mag = StringField(label='Magnitude: ', validators=[DataRequired()])
    net = StringField(label='Net: ', validators=[DataRequired()])
    place = StringField(label='Place: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@application.route('/form4', methods=['GET', 'POST'])
def form4():
    form = Form4()
    if form.validate_on_submit():
        time = form.time.data
        latitude = float(form.latitude.data)
        longitude = float(form.longitude.data)
        mag = float(form.mag.data)
        net = form.net.data
        place = form.place.data

        try:
            with connection() as conn:
                with conn.cursor() as cursor:
                    # Add new quake data
                    cursor.execute(
                        "INSERT INTO EarthquakeData (time, latitude, longitude, mag, net, place) VALUES (?, ?, ?, ?, ?, ?)",
                        (time, latitude, longitude, mag, net, place)
                    )
                    conn.commit()

            return render_template('form4.html', form=form, success="Earthquake data added successfully!")
        except Exception as e:
            print(e)
            return render_template('form4.html', form=form, error=str(e))
    return render_template('form4.html', form=form)



class Form5(FlaskForm):
    time = StringField(label='Time: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@application.route('/form5', methods=['GET', 'POST'])
def form5():
    form = Form5()
    if form.validate_on_submit():
        time = form.time.data

        try:
            with connection() as conn:
                with conn.cursor() as cursor:
                    # Remove quake data
                    cursor.execute(
                        "DELETE FROM EarthquakeData WHERE time = ?",
                        (time,)
                    )
                    conn.commit()

            return render_template('form5.html', form=form, success="Earthquake data removed successfully!")
        except Exception as e:
            print(e)
            return render_template('form5.html', form=form, error=str(e))
    return render_template('form5.html', form=form)



if __name__ == "__main__":
    application.run(debug=True)