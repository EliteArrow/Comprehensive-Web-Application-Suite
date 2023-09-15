
# DataViz: Data Management and Visualization Tool

**Developer:** Meet Navadiya

## Description
DataViz is a Flask web application tailored for the exploration, management, and visualization of data stored in an Azure SQL database. With interactive features for data insertion and various visualization types, it serves as a comprehensive tool for data enthusiasts and analysts.

## Features
1. **Database Connection**: Connects seamlessly to an Azure SQL database using the `pyodbc` library.
2. **Data Insertion**: Interactive forms for data insertion with fields like name, abbreviation, year, and cost.
3. **Data Visualization**: Offers multiple visualization types, including bar charts and scatter plots, for intuitive data exploration.
4. **Top N Data Retrieval**: Fetches the top 'N' records based on costs.

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
