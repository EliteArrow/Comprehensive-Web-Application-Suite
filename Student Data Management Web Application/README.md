
# Student Data Management Web Application

**Developer:** Meet Navadiya

## Description
A Flask web application designed for managing and viewing student data. Users can filter student records based on grade, ID range, and keyword search in student notes. Additionally, there's an option to modify student details and upload image files.

## Features
1. **View Students**: Filter students based on grade and ID range.
2. **Keyword Search**: Search student records based on keywords present in their notes.
3. **Modify Student Data**: Edit details of a student and update them in the database (CSV file).
4. **Image Upload**: A feature to upload image files and view them.

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

