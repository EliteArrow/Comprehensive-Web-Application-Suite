
# TremorTrack: Earthquake Data Platform

**Developer:** Meet Navadiya

## Description
TremorTrack is a Flask web application designed to explore and manage earthquake data stored in an Azure SQL database. With functionalities allowing users to retrieve, modify, and analyze seismic data, it serves as a comprehensive platform for earthquake enthusiasts, researchers, and data analysts.

## Features
1. **Database Connection**: Seamless integration with Azure SQL for data retrieval and management.
2. **Redis Integration**: Leverages Redis for enhanced data processing and management capabilities.
3. **Interactive Data Management**: Features to retrieve, add, update, and delete earthquake records using intuitive forms.
4. **Data Analysis**: Analyze earthquakes based on specific criteria, such as time or geographical range.

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

