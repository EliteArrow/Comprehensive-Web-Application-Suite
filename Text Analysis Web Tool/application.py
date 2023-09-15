import os
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import nltk
import codecs
from collections import defaultdict
from time import time


nltk.download(['punkt', 'stopwords'])
porter = PorterStemmer()


application = Flask(__name__)
application.config['SECRET_KEY'] = 'DontTellAnyone'
application.config['UPLOAD_FOLDER'] = 'static'
application.config['PROCESSED_FOLDER'] = 'static/processed_data'
application.config['ALLOWED_EXTENSIONS'] = {'txt'}


@application.route('/', methods=['GET', 'POST'])
def main():
    try:
        msg = "Welcome to Search Engine!"
        return render_template('index.html', error=msg)
    except Exception as e:
        return render_template('index.html', error=e)


stop_words = set(stopwords.words(['english', 'spanish', 'french']))


ps = PorterStemmer()


def preprocess_text(input_file, output_file):
    with codecs.open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in application.config['ALLOWED_EXTENSIONS']


class UploadForm(FlaskForm):
    textfile = FileField('Text File', validators=[
        FileRequired(),
        FileAllowed(application.config['ALLOWED_EXTENSIONS'], 'Text files only!')
    ])
    submit = SubmitField('Upload and Process')


def process_text(text):
    processed_text = []
    lines = text.split('\n')
    for i, line in enumerate(lines):
        words = word_tokenize(line)
        words = [word.lower() for word in words if word.isalpha()]
        words = [word for word in words if not word in stop_words]
        words = [porter.stem(word) for word in words]
        processed_line = ' '.join(words)
        processed_text.append(f"{i+1}: {processed_line}")
    return '\n'.join(processed_text)


@application.route('/upload', methods=['GET', 'POST'])
def upload():
    success_message = ""
    form = UploadForm()
    if form.validate_on_submit():
        f = form.textfile.data
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            file_path = os.path.join(application.config['UPLOAD_FOLDER'], filename)
            f.save(file_path)
            with codecs.open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                text = file.read()
                processed_text = process_text(text)
                new_file_path = os.path.join(application.config['PROCESSED_FOLDER'], filename)
                with codecs.open(new_file_path, 'w', encoding='utf-8') as new_file:
                    new_file.write(processed_text)
                success_message = f"File uploaded and processed successfully. The filename is: {filename}"
    return render_template('upload.html', form=form, success_message=success_message)


class SearchForm(FlaskForm):
    query = StringField('Search Query', [InputRequired()])
    submit = SubmitField('Search')


def process_query(query):
    words = word_tokenize(query)
    words = [word.lower() for word in words if word.isalpha()]
    words = [word for word in words if not word in stop_words]
    words = [porter.stem(word) for word in words]
    return words


@application.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    results = defaultdict(list)
    start_time = time()
    if form.validate_on_submit():
        query = form.query.data
        query = process_query(query)
        for filename in os.listdir(application.config['PROCESSED_FOLDER']):
            file_path = os.path.join(application.config['PROCESSED_FOLDER'], filename)
            with codecs.open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    words = line.split()
                    if words and any(word in words for word in query):
                        results[filename].append((i+1, line))
        results = {k: v for k, v in results.items() if v}
        if not results:
            flash("No results found for your query.", "danger")
    elapsed_time = time() - start_time
    return render_template('search.html', form=form, results=results, elapsed_time=elapsed_time)


if __name__ == '__main__':
    application.run(debug=True, use_reloader=False)