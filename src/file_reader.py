import pandas as pd
import sqlite3
import os

def import_file(file_path):
    # Check if the file has a valid extension
    valid_extensions = ['.xlsx', '.xls', '.csv', '.sqlite', '.db']
    file_extension = os.path.splitext(file_path)[1].lower()
    print(file_extension)

    if file_extension not in valid_extensions:
        raise ValueError("Invalid file format. Only Excel, CSV, and SQLite files are allowed.")
    
    try:
        # Excel files
        if file_extension in ['.xlsx', '.xls']:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Error: File not found at {file_path}")
                
            df = pd.read_excel(file_path)
            if df.empty:
                raise ValueError("The Excel database is empty.")
            else:
                print("File is valid! First 5 lines of the Excel file:")
                print(df.head())
            
           
            
        # CSV files
        elif file_extension == '.csv':
            df = pd.read_csv(file_path)
            if df.empty:
                raise ValueError("The CSV database is empty.")
            else:
                print("File is valid! First 5 lines of the CSV file:")
                print(df.head())
            
            
 
        # SQLite files
        elif file_extension in ['.sqlite', '.db']:
            conn = sqlite3.connect(file_path)
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            tables = pd.read_sql(query, conn)

            if tables.empty:
                raise ValueError("The SQLite database is empty or contains no tables.")
            
            first_table = tables['name'][0]  # Get the name of the table
            df = pd.read_sql(f"SELECT * FROM {first_table} LIMIT 5;", conn)
            print(f"File is valid! First 5 lines of the '{first_table}' table in the SQLite file:")
            print(df)

            conn.close()

    except Exception as e:
        raise ValueError(f"The file appears to be corrupted or invalid: {str(e)}")
    
if __name__ == '__main__':
    file_path = input('Write the path of the database:')
    import_file(file_path)