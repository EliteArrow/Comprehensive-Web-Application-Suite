
# Seismic Data Explorer

**Developer:** Meet Navadiya

## Description
A Flask web application tailored for exploring and managing seismic data stored in an Azure SQL database. Users can view, add, modify, and delete earthquake records using various functionalities provided in the application.

## Features
1. **Database Connection**: Connects to an Azure SQL database to fetch and manage earthquake data.
2. **View Earthquake Data**: Allows users to input specific time and retrieve earthquake data related to that time, along with quakes within a certain latitude range.
3. **Data Management**: Features to add, update, and delete earthquake records.
4. **Interactive Forms**: Utilizes Flask-WTF forms for a smooth user interaction with the data.

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

