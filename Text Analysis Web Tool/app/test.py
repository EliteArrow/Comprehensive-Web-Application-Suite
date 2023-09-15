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
