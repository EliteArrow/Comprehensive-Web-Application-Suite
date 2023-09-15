import pyodbc
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

application = Flask(__name__)
application.config['SECRET_KEY'] = 'SecureSecretKey'
db_table = "Quiz4"

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


class InsertDataForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    abb = StringField('Abb', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    cost = IntegerField('Cost', validators=[DataRequired()])
    submit = SubmitField('Insert')

def insert_data(cursor, name, abb, year, cost):
    query = 'INSERT INTO Quiz4 (name, abb, year, cost) VALUES (?, ?, ?, ?)'
    params = (name, abb, year, cost)
    cursor.execute(query, params)
    cursor.commit()

@application.route('/insert', methods=['GET', 'POST'])
def insert():
    form = InsertDataForm()
    if form.validate_on_submit():
        try:
            conn = connection()
            cursor = conn.cursor()
            insert_data(cursor, form.name.data, form.abb.data, form.year.data, form.cost.data)
        except Exception as e:
            print(e)
    return render_template('insert.html', form=form)


def get_name_and_cost_data(cursor):
    query = 'SELECT name, cost FROM Quiz4 ORDER BY cost'
    cursor.execute(query)
    return cursor.fetchall()


@application.route('/chart', methods=['GET'])
def chart():
    try:
        conn = connection()
        cursor = conn.cursor()
        data = get_name_and_cost_data(cursor)
        return render_template('chart.html', data=data)
    except Exception as e:
        print(e)
        return render_template('chart.html', error='Failed to retrieve data.')


def get_top_n_cost_data(cursor, n):
    query = """
    SELECT abb, cost FROM Quiz4 
    ORDER BY cost DESC
    OFFSET 0 ROWS
    FETCH NEXT ? ROWS ONLY;
    """
    cursor.execute(query, (n,))
    return cursor.fetchall()


class TopNForm(FlaskForm):
    n = IntegerField('Enter N:', validators=[DataRequired()])
    submit = SubmitField('Submit')

@application.route('/top_n', methods=['GET', 'POST'])
def top_n():
    form = TopNForm()
    data = []
    if form.validate_on_submit():
        try:
            n = form.n.data
            conn = connection()
            cursor = conn.cursor()
            data = get_top_n_cost_data(cursor, n)
        except Exception as e:
            print(e)
    return render_template('top_n.html', form=form, data=data)


def get_year_and_cost_data(cursor):
    query = 'SELECT year, cost FROM Quiz4'
    cursor.execute(query)
    return cursor.fetchall()

@application.route('/scatter', methods=['GET'])
def scatter():
    try:
        conn = connection()
        cursor = conn.cursor()
        data = get_year_and_cost_data(cursor)
        return render_template('scatter.html', data=data)
    except Exception as e:
        print(e)
        return render_template('scatter.html', error='Failed to retrieve data.')





if __name__ == "__main__":
    application.run(debug=True)