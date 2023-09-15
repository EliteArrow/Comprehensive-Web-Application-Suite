from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import csv
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = '/static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@application.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@application.route("/grade_range", methods=['GET', 'POST'])
def name():
    return render_template('grade_range.html')

@application.route("/display_grad_details", methods=['GET', 'POST'])
def grade_range_disp():
    if request.method == 'POST':
        range1 = int(request.form.get('range1') or 0)
        range2 = int(request.form.get('range2') or 0)
        id_range1 = int(request.form.get('id_range1') or 0)
        id_range2 = int(request.form.get('id_range2') or 0)
        keyword = request.form.get('keyword') or ''
        students = []
        if (range1 or range2) and (id_range1 or id_range2) and not keyword:
            return render_template('display_grad_details.html', error="Keyword is missing")
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # gets the directory of the current file
        file_path = os.path.join(BASE_DIR, 'static', 'q1c.csv')  # constructs the path to the csv file
        with open(file_path) as file:
            csv_reader = csv.DictReader(file)
            for r in csv_reader:
                grade_check = r['grade'].strip().isdigit() and range1 <= int(r['grade']) <= range2 if range1 or range2 else True
                id_check = r['id'].strip().isdigit() and id_range1 <= int(r['id'].strip()) <= id_range2 if id_range1 or id_range2 else True
                keyword_check = keyword.lower() in r['notes'].lower() if keyword else True
                if grade_check and id_check and keyword_check:
                    student = dict()
                    student['name'] = r['name']
                    student['grade'] = r['grade']
                    student['id'] = r['id']
                    student['notes'] = r['notes']
                    if r['pic'].strip():
                        student['pic'] = 'static/' + r['pic']
                    else:
                        student['pic'] = 'static/no_picture.png'
                    students.append(student)
        if students:
            return render_template('display_grad_details.html', students=students)
        else:
            return render_template('display_grad_details.html', error="No students found in this grade range")

@application.route("/add_user", methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        grade = request.form['grade']
        id = request.form['id']
        pic = request.form['pic']
        notes = request.form['notes']

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # gets the directory of the current file
        file_path = os.path.join(BASE_DIR, 'static', 'q1c.csv')  # constructs the path to the csv file

        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, grade, id, pic, notes])

        return render_template('add_user.html', message="User added successfully!")
    else:
        return render_template('add_user.html')


@application.route("/delete_user", methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        name = request.form['name']
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # gets the directory of the current file
        file_path = os.path.join(BASE_DIR, 'static', 'q1c.csv')  # constructs the path to the csv file

        lines = []
        with open(file_path, 'r') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                lines.append(row)
                for field in row:
                    if field == name:
                        lines.remove(row)

        with open(file_path, 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)

        return render_template('delete_user.html', message="User deleted successfully!")
    else:
        return render_template('delete_user.html')

@application.route("/modify_user_input", methods=['GET'])
def modify_user_input():
    return render_template('modify_user.html')

@application.route("/modify_user", methods=['GET', 'POST'])
def modify_user_form():
    if request.method == 'POST':
        name = request.form.get('name')
        student = None
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, 'static', 'q1c.csv')
        with open(file_path) as file:
            csv_reader = csv.DictReader(file)
            for r in csv_reader:
                if r['name'] == name:
                    student = r
                    break
        if student:
            return render_template('modify_user_form.html', student=student)
        else:
            return render_template('modify_user_form.html', error="No student found with this name")

    return render_template('modify_user_form.html')


@application.route("/perform_user_modification", methods=['POST'])
def perform_user_modification():
    name = request.form.get('name')
    new_grade = request.form.get('grade')
    new_id = request.form.get('id')
    new_pic = request.form.get('pic')
    new_notes = request.form.get('notes')

    students = []
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, 'static', 'q1c.csv')
    with open(file_path) as file:
        csv_reader = csv.DictReader(file)
        for r in csv_reader:
            student = dict(r)
            if student['name'] == name:
                student['grade'] = new_grade
                student['id'] = new_id
                student['pic'] = new_pic
                student['notes'] = new_notes
            students.append(student)

    # Now write the updated data back to the file
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'grade', 'id', 'pic', 'notes'])
        writer.writeheader()
        for student in students:
            writer.writerow(student)

    return render_template('modify_user_form.html', message="User updated successfully")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route('/upload_img', methods=['GET', 'POST'])
def upload_img():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('upload_img.html', error="No file part")
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return render_template('upload_img.html', error="No selected file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('upload_img.html')

@application.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(application.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    application.run(debug=True)