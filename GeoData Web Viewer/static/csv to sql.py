import csv
import os

def create_sql_insert(file_path):
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        with open('insert_queries.sql', 'w', encoding='utf-8') as insert_query_file:
            for row in reader:
                columns = ', '.join(row.keys())
                values = ', '.join(f"'{value}'" for value in row.values())
                query = f"INSERT INTO EarthquakeData ({columns}) VALUES ({values});\n"
                insert_query_file.write(query)


print(f"Current working directory: {os.getcwd()}")  # This will print the current working directory

# Call the function with your CSV file
create_sql_insert('all_month.csv')
