from flask import Flask, render_template, request
import pandas as pd
import csv
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/'

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/room", methods=['GET', 'POST'])
def room():
    if request.method == 'POST':
        room = request.form['room']
        csv_reader = csv.DictReader(open('static/q0c.csv'))
        data = []
        for r in csv_reader:
            if room == r['room']:
                data.append({
                    'path': '../static/'+r['pic'],
                    'name': r['name'],
                    'descript': r['descript']
                })

        if data:
            return render_template('room.html', data=data, message="found")
        else:
            return render_template('room.html', error="Picture and Name did not find for Room!")

@app.route("/teln", methods=['GET', 'POST'])
def grade():

    if request.method == 'POST':
        t1 = request.form['t1']
        t2 = request.form['t2']
        csv_reader = csv.DictReader(open('static/q0c.csv'))
        data = []
        for r in csv_reader:
            if t1 <= r['teln'] <= t2:
                data.append({
                    'path': '../static/'+r['pic'],
                    'name': r['name'],
                    'teln': r['teln'],
                    'descript': r['descript'] 
                })

        if data:
            return render_template('teln.html', data=data, message="found")
        else:
            return render_template('teln.html', error="Picture and Name did not find for Room!")


@app.route("/editdes", methods=['GET', 'POST'])
def editdes():
    if request.method == 'POST':
        teln = request.form['teln']
        csv_reader = csv.DictReader(open('static/q0c.csv'))
        temp_teln = ''
        for r in csv_reader:
            if teln == r['teln']:
                temp_teln = teln
        if temp_teln != '':
            return render_template('distel.html', name=temp_teln)
        else:
            return render_template('distel.html', error="No Record Found!")

@app.route("/updatedes", methods=['GET', 'POST'])
def updatedes():
    if request.method == 'POST':
        teln = request.form['teln']
        new_descript = request.form['descript']
        updated = False
        new_rows = []

        with open('static/q0c.csv', 'r') as f1:
            csv_reader = csv.reader(f1)
            for r in csv_reader:
                if teln == r[3]:
                    r[4] = new_descript
                    updated = True
                new_rows.append(r)

        with open('static/q0c.csv', 'w', newline='') as f2:
            csv_writer = csv.writer(f2)
            csv_writer.writerows(new_rows)

        if updated:
            return render_template('display.html', update="One Record Updated Successfully.")
        else:
            return render_template('display.html', error="No Record Found!")

@app.route("/editdetails", methods=['GET', 'POST'])
def editdetails():
    if request.method == 'POST':
        action = request.form['action']
        name = request.form['name']
        room = request.form['room']
        teln = request.form['teln']
        descript = request.form['descript']
        new_name = request.form['new_name']
        updated = False
        new_rows = []

        if action == "add":
            new_rows.append([name, room, "", teln, descript])

        with open('static/q0c.csv', 'r') as f1:
            csv_reader = csv.reader(f1)
            for r in csv_reader:
                if name == r[0]:
                    if action == "delete":
                        continue
                    elif action == "update":
                        r = [new_name, room or r[1], r[2], teln or r[3], descript or r[4]]
                        updated = True
                new_rows.append(r)

        with open('static/q0c.csv', 'w', newline='') as f2:
            csv_writer = csv.writer(f2)
            csv_writer.writerows(new_rows)

        if updated or action == "add":
            return render_template('display.html', update="Operation executed successfully.")
        else:
            return render_template('display.html', error="No Record Found or Updated!")

if __name__ == "__main__":
    app.run(debug=True)