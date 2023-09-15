from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Optional
import re

application = Flask(__name__)
application.config['SECRET_KEY'] = 'ty#4nightCart*#782Th@7'
application.config['UPLOAD_FOLDER'] = 'static'


@application.route('/', methods=['GET', 'POST'])
def main():
    try:
        msg = "Welcome to Text Universe!"
        return render_template('index.html', error=msg)
    except Exception as e:
        return render_template('index.html', error=e)


class PasswordForm(FlaskForm):
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Check Password')


class AdminConfigForm(FlaskForm):
    min_length = StringField('Minimum Length', validators=[DataRequired()])
    valid_chars = StringField('Valid Characters')
    submit = SubmitField('Save Configuration')


admin_config = {
    'min_length': 8,
    'valid_chars': '',
}


def validate_password_strength(password):
    min_length = admin_config['min_length']
    valid_chars = admin_config['valid_chars']

    if len(password) < min_length:
        return 'NotValid: Password length must be more than {} characters.'.format(min_length)

    if not re.search(r'\d', password):
        return 'NotValid: Password must contain at least one number.'

    if not re.search(r'[A-Z]', password):
        return 'NotValid: Password must contain at least one uppercase letter.'

    if len(set(valid_chars) & set(password)) < 2:
        return 'NotValid: Password must contain at least two characters from the valid character list.'

    if any(char in password for char in "/*#"):
        return 'NotValid: Password must not contain any characters from "/*#".'

    return 'Valid'


@application.route('/validate_password', methods=['GET', 'POST'])
def validate_password():
    form = PasswordForm()
    if form.validate_on_submit():
        password = form.password.data[:20]  # ignore characters beyond 20th
        validation_result = validate_password_strength(password)
        return render_template('validate_password.html', form=form, validation_result=validation_result)
    return render_template('validate_password.html', form=form)


@application.route('/admin_config', methods=['GET', 'POST'])
def admin_config_route():
    form = AdminConfigForm()
    if form.validate_on_submit():
        admin_config['min_length'] = int(form.min_length.data)
        admin_config['valid_chars'] = form.valid_chars.data
    return render_template('admin_config.html', form=form, admin_config=admin_config)

class TextForm(FlaskForm):
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Submit Text')

censor_config = {
    'banned_words': [],
    'banned_phrases': [],
    'max_value': 0
}

class CensorConfigForm(FlaskForm):
    banned_words = StringField('Banned Words (comma-separated)', validators=[Optional()])
    banned_phrases = StringField('Banned Phrases (comma-separated)', validators=[Optional()])
    max_value = IntegerField('Max Value', validators=[DataRequired()])
    submit = SubmitField('Save Configuration')

@application.route("/censor_config", methods=['GET', 'POST'])
def censor_config_route():
    form = CensorConfigForm()
    if form.validate_on_submit():
        censor_config['banned_words'] = form.banned_words.data.split(',')
        censor_config['banned_phrases'] = form.banned_phrases.data.split(',')
        censor_config['max_value'] = form.max_value.data
        flash('Configuration saved!', 'success')
        return redirect(url_for('censor_config_route'))
    return render_template('censor_config.html', form=form)

@application.route('/submit_text', methods=['GET', 'POST'])
def submit_text():
    form = TextForm()
    censored_text = None
    alert_message = None

    if form.validate_on_submit():
        text = form.text.data.lower()
        banned_count = 0
        for word in censor_config['banned_words']:
            if word in text:
                banned_count += text.count(word)
                text = text.replace(word, '')

        for phrase in censor_config['banned_phrases']:
            if phrase in text:
                banned_count += text.count(phrase)
                text = text.replace(phrase, '')

        if banned_count > censor_config['max_value']:
            alert_message = 'Max banned words occurred, call the authorities'
        else:
            censored_text = text

    return render_template('submit_text.html', form=form, censored_text=censored_text, alert_message=alert_message)


text_validator_config = {
    'min_words': 0,
    'max_words': 0,
    'max_part_words': 0,
    'max_length': 0
}

class TextValidatorConfigForm(FlaskForm):
    min_words = IntegerField('Minimum Words Per Sentence (M)', validators=[DataRequired()])
    max_words = IntegerField('Maximum Words Per Sentence (X)', validators=[DataRequired()])
    max_part_words = IntegerField('Maximum Words Per Sentence Part (P)', validators=[DataRequired()])
    max_length = IntegerField('Maximum Word Length (L)', validators=[DataRequired()])
    submit = SubmitField('Save Configuration')

class TextForm(FlaskForm):
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Validate Text')

@application.route("/text_validator_config", methods=['GET', 'POST'])
def text_validator_config_route():
    form = TextValidatorConfigForm()
    if form.validate_on_submit():
        text_validator_config['min_words'] = form.min_words.data
        text_validator_config['max_words'] = form.max_words.data
        text_validator_config['max_part_words'] = form.max_part_words.data
        text_validator_config['max_length'] = form.max_length.data
        flash('Configuration saved!', 'success')
        return redirect(url_for('text_validator_config_route'))
    return render_template('text_validator_config.html', form=form)

@application.route('/validate_text', methods=['GET', 'POST'])
def validate_text():
    form = TextForm()
    result = None

    if form.validate_on_submit():
        text = form.text.data
        sentences = text.split(". ")
        for sentence in sentences:
            words = sentence.split()
            if len(words) < text_validator_config['min_words'] or len(words) > text_validator_config['max_words']:
                result = f"Sentence '{sentence}' has invalid number of words."
                break
            for word in words:
                if len(word) > text_validator_config['max_length']:
                    result = f"Word '{word}' in sentence '{sentence}' is too long."
                    break
            if result:
                break
        if not result:
            result = "Valid"
    return render_template('validate_text.html', form=form, result=result)




if __name__ == '__main__':
    application.run(debug=True, use_reloader=False)