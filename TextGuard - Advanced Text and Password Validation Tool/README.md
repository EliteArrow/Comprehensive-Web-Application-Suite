
# TextGuard: Advanced Text and Password Validation Tool

**Developer:** Meet Navadiya

## Description
TextGuard is a Flask-based web application tailored for text and password validation. With a configurable set of rules, users can validate text and passwords against specific criteria, ensuring data integrity and security.

## Features
1. **Configurable Text Validation Rules**: Define rules such as minimum and maximum word counts, maximum words per sentence part, and maximum word length.
2. **Password Strength Checker**: Validate password strength against criteria like minimum length, presence of numbers, uppercase letters, and more.
3. **Interactive Feedback**: Users receive immediate feedback on the validity of their inputs based on the defined criteria.

## Setup and Execution
1. Ensure you have the dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the `application.py` file:
   ```bash
   python application.py
   ```
3. Access the application at `http://localhost:5000`.

## Deployment
Use Gunicorn for deployment with the command provided in `startup.txt`.

## License
This project is open-source and available for collaboration or modification.
