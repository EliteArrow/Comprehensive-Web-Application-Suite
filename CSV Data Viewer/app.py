from flask import Flask, render_template, request
import csv
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/'


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    return render_template('upload.html')


@app.route("/data", methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        file = request.files['csvfile']

        if file:
            filename = secure_filename(file.filename)  # make sure the filename is secure
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            data = []
            with open(filepath, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    data.append(row)
            print(data)
            return render_template('data.html', data=data)

    return render_template('data.html')


@app.route("/search", methods=['GET', 'POST'])
def search():
    return render_template('search.html')


@app.route("/searchimage", methods=['GET', 'POST'])
def searchimage():
    if request.method == 'POST':
        name = request.form['name']
        csv_reader = csv.DictReader(open('static/people.csv'))
        temp_path = ''
        for r in csv_reader:
            if name == r['Name']:
                temp_path = '../static/' + r['Picture']
        if temp_path != '':
            return render_template('search.html', image_path=temp_path, message="found")
        else:
            return render_template('search.html', error="Picture did not find!")


@app.route("/searchbysal", methods=['GET', 'POST'])
def searchbysal():
    csv_reader = csv.DictReader(open('static/people.csv'))
    temp_path = []

    for r in csv_reader:
        if r['Salary'] == '' or r['Salary'] == ' ':
            r['Salary'] = 99000;
        if int(float(r['Salary'])) < 99000:
            if r['Picture'] != ' ':
                temp_path.append('static/' + r['Picture'])
                print(temp_path)
                print(int(float(r['Salary'])))

    print(len(temp_path))
    if temp_path != '':
        return render_template('searchbysal.html', image_path=temp_path,  message="found")
    else:
        return render_template('searchbysal.html', error="Picture did not find!")


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    return render_template('edit.html')


@app.route("/editdetails", methods=['GET', 'POST'])
def editdetails():
    if request.method == 'POST':
        name = request.form['name']
        csv_reader = csv.DictReader(open('static/people.csv'))
        temp_name = ''
        for r in csv_reader:
            if name == r['Name']:
                temp_name = name
        if temp_name != '':
            return render_template('display.html', name=temp_name)
        else:
            return render_template('display.html', error="No Record Found!")


@app.route("/updatedetails", methods=['GET', 'POST'])
def updatedetails():
    if request.method == 'POST':
        name = request.form['name']
        state = request.form['state']
        salary = request.form['salary']
        grade = request.form['grade']
        room = request.form['room']
        telnum = request.form['telnum']
        picture = request.form['picture']
        keyword = request.form['keyword']
        cnt = 0

        temp = [name, state, salary, grade, room, telnum, picture, keyword]
        line = list()

        with open('static/people.csv', 'r') as f1:
            csv_reader = csv.reader(f1)
            for r in csv_reader:
                if name == r[0]:
                    line.append(temp)
                else:
                    line.append(r)
                cnt += 1

            csv_write = open('static/people.csv', 'w')
            for i in line:
                for j in i:
                    csv_write.write(j + ',')
                csv_write.write('\n')

            if cnt != 0:
                return render_template('display.html', update="One Record Updated Successfully.")
            else:
                return render_template('display.html', error="No Record Found!")


@app.route("/remove", methods=['GET', 'POST'])
def remove():
    return render_template('remove.html')

@app.route("/removedetails", methods=['GET', 'POST'])
def removedetails():
    if request.method == 'POST':
        name = request.form['name']
        cnt = 0
        line = list()
        with open('static/people.csv', 'r') as f1:
            csv_reader = csv.reader(f1)
            for r in csv_reader:
                line.append(r)
                if name == r[0]:
                    line.remove(r)
                    cnt+=1


            csv_write = open('static/people.csv', 'w')
            for i in line:
                for j in i:
                    csv_write.write(j + ',')
                csv_write.write('\n')

        if cnt != 0:
            return render_template('removedetails.html', message="Record Remove Successfully.")
        else:
            return render_template('removedetails.html', error="Record Not Found.")

@app.route("/uploadpic", methods=['GET', 'POST'])
def remove1():
    return render_template('uploadpic.html')

@app.route("/uploadnew", methods=['GET', 'POST'])
def uploadnew():
    if request.method == 'POST':
        file = request.files['img']
        file.save('static/'+file.filename)
        return render_template('uploaddisp.html', msg="Image Upload Successfully.")


if __name__ == "__main__":
    app.run(debug=True)
