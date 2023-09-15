import pyodbc
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

application = Flask(__name__)
application.config['SECRET_KEY'] = 'SecureSecretKey'
db_table = "EarthquakeData"

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


class Form1(FlaskForm):
    mag = StringField(label='Enter Magnitude: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


def get_magnitude_data(cursor, mag1, mag2=None):
    if mag2:
        query = 'SELECT count(*) from {} where mag >= ? and mag < ?'.format(db_table)
        params = (mag1, mag2)
        label = f'Mag. between {mag1} to {mag2}'
    else:
        query = 'SELECT count(*) from {} where mag >= ?'.format(db_table)
        params = (mag1,)
        label = f'Mag. greater than {mag1}'

    cursor.execute(query, params)
    return label, cursor.fetchone()[0]



@application.route('/form1', methods=['GET', 'POST'])
def form1():
    try:
        conn = connection()
        cursor = conn.cursor()
        cnt = 0
        result = {}
        magnitude_ranges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5,)]

        for mag_range in magnitude_ranges:
            label, mag_data = get_magnitude_data(cursor, *mag_range)
            result[label] = mag_data
            cnt += mag_data

        return render_template('form1.html', result=result, cnt=cnt, data=1)

    except Exception as e:
        print(e)
        return render_template('form1.html', error='Enter numeric value.')


class Form2(FlaskForm):
    d1 = StringField(label='Lower Range of Depth: ', validators=[DataRequired()])
    d2 = StringField(label='Upper Range of Depth: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@application.route('/form2', methods=['GET', 'POST'])
def form2():
    form = Form2()
    cnt = 0
    if form.validate_on_submit():
        try:
            conn = connection()
            cursor = conn.cursor()
            d1 = float(form.d1.data)
            d2 = float(form.d2.data)

            if d1 > d2:
                return render_template('form2.html', form=form, error='Lower range must be lower then upper range.')

            cursor.execute('SELECT count(*) as "Mag. less then 1.0" from {} where mag < 1 and depth between ? and ?'.format(db_table), d1, d2)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result = {columns[0]: row[0]}
                cnt += row[0]

            cursor.execute('SELECT count(*) as "Mag. between 1.0 to 2.0" from {} where mag >= 1.0 and  mag <2.0 and depth between ? and ?'.format(db_table), d1, d2)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            cursor.execute('SELECT count(*) as "Mag. between 2.0 to 3.0" from {} where mag >= 2.0 and mag < 3.0 and depth between ? and ?'.format(db_table), d1, d2)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            cursor.execute('SELECT count(*) as "Mag. between 3.0 to 4.0" from {} where mag >= 3.0 and mag < 4.0 and depth between ? and ?'.format(db_table), d1, d2)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            cursor.execute('SELECT count(*) as "Mag. between 4.0 to 5.0" from {} where mag >= 4.0 and mag < 5.0 and depth between ? and ?'.format(db_table), d1, d2)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            cursor.execute('SELECT count(*) as "Mag. grater then 5.0" from {} where mag >= 5.0 and depth between ? and ?'.format(db_table), d1, d2)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            return render_template('form2.html', result=result, cnt=cnt, data=1)

        except Exception as e:
            print(e)
            return render_template('form2.html', form=form, error='Enter numeric value.')

    return render_template('form2.html', form=form)


class Form3(FlaskForm):
    m1 = StringField(label='Lower Range of Magnitude: ', validators=[DataRequired()])
    m2 = StringField(label='Upper Range of Magnitude: ', validators=[DataRequired()])
    d1 = StringField(label='Lower Range of Depth: ', validators=[DataRequired()])
    d2 = StringField(label='Upper Range of Depth: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@application.route('/form3', methods=['GET', 'POST'])
def form3():
    form = Form3()
    cnt = 0
    if form.validate_on_submit():
        try:
            conn = connection()
            cursor = conn.cursor()
            m1 = float(form.m1.data)
            m2 = float(form.m2.data)
            d1 = float(form.d1.data)
            d2 = float(form.d2.data)

            if d1 > d2 or m1 > m2:
                return render_template('form3.html', form=form, error='Lower range must be lower then upper range.')

            result = dict()

            cursor.execute('select mag,depth from {} where mag BETWEEN ? and ? and depth BETWEEN ? and ? order by mag,depth'.format(db_table), m1, m2, d1, d2)
            for row in cursor.fetchall():
                for i in row:
                    result.setdefault(cnt, []).append(i)
                cnt += 1

            return render_template('form3.html', result=result, d1=d1, d2=d2, m1=m1, m2=m2, cnt=cnt, form=form, data=1)

        except Exception as e:
            print(e)
            return render_template('form3.html', form=form, error='Enter numeric value.')

    return render_template('form3.html', form=form)


@application.route('/form4', methods=['GET', 'POST'])
def form4():
    cnt = 0
    if request.method == "POST":
        try:
            conn = connection()
            cursor = conn.cursor()
            clus = request.form['type']

            cursor.execute('SELECT count(*) as "Mag. less then 1.0" from {} where mag < 1 and type = ?'.format(db_table), clus)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result = {columns[0]: row[0]}
                cnt += row[0]

            cursor.execute(
                'SELECT count(*) as "Mag. between 1.0 to 2.0" from {} where mag >= 1.0 and  mag <2.0 and type = ?'.format(db_table), clus)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            cursor.execute(
                'SELECT count(*) as "Mag. between 2.0 to 3.0" from {} where mag >= 2.0 and mag < 3.0 and type = ?'.format(db_table), clus)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            cursor.execute(
                'SELECT count(*) as "Mag. between 3.0 to 4.0" from {} where mag >= 3.0 and mag < 4.0 and type = ?'.format(db_table), clus)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            cursor.execute(
                'SELECT count(*) as "Mag. between 4.0 to 5.0" from {} where mag >= 4.0 and mag < 5.0 and type = ?'.format(db_table), clus)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            cursor.execute('SELECT count(*) as "Mag. grater then 5.0" from {} where mag >= 5.0 and type = ?'.format(db_table), clus)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            return render_template('form4.html', result=result, type=clus, cnt=cnt, data=1)

        except Exception as e:
            print(e)
            return render_template('form4.html', error=e)

    return render_template('form4.html')


if __name__ == "__main__":
    application.run(debug=True)