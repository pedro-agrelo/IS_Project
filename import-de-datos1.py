import pandas as pd
import sqlite3
import openpyxl
import os

def load_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Data successfully loaded from CSV file.")
        return data.head()  # Preview the first 5 rows
    except pd.errors.EmptyDataError:
        print("Error: CSV file is empty or corrupted.")
    except Exception as e:
        print(f"Error loading CSV: {e}")


def load_excel(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print("Error: File not found.")
        return
    
    # Check if it is an .xlsx file
    if not file_path.endswith('.xlsx'):
        print("Error: The file does not have the .xlsx extension.")
        return
    
    try:
        # Try to read the file
        data = pd.read_excel(file_path, engine='openpyxl')
        if data.empty:
            print("Error: The Excel file is empty.")
            return
        print("Data successfully loaded from the Excel file.")
        return data.head()  # Preview the first 5 rows
    
    except FileNotFoundError:
        print("Error: Cannot find the specified file.")
    
    except pd.errors.EmptyDataError:
        print("Error: The Excel file is empty or corrupt.") #elimina
    
    except PermissionError: ####
        print("Error: You do not have permission to access the file.") #elimina
    
    except openpyxl.utils.exceptions.InvalidFileException: #### 
        print("Error: The file is damaged or not a valid Excel file.") #elimina
    
    except ValueError as ve:
        # Handle issues related to worksheet structure
        if 'Worksheet' in str(ve):
            print("Error: The file does not contain the expected sheet or is empty.")
        else:
            print(f"Unexpected value error: {ve}")
    
    except Exception as e:
        print(f"Unknown error while loading the Excel file: {e}")

def load_sqlite(file_path):
    try:
        conn = sqlite3.connect(file_path)
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql(query, conn)
        if tables.empty:
            print("Error: The database contains no tables.")
            return
        table_name = tables['name'][0]  # Use the first available table
        data = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        print("Data successfully loaded from SQLite database.")
        return data.head()  # Preview the first 5 rows
    except sqlite3.DatabaseError:
        print("Error: Invalid or corrupted SQLite database.")
    except Exception as e:
        print(f"Error loading SQLite: {e}")

# Function to display the menu and handle user input
def import_data_menu():
    print("Select the type of file you want to import:")
    print("1. CSV File (.csv)")
    print("2. Excel File (.xlsx,.xls)")
    print("3. SQLite Database (.sqlite, .db)")
    
    option = input("Enter the number of the desired option: ")
    
    file_path = input("Enter the file path: ")
    
    if option == '1':
        print(load_csv(file_path))
    elif option == '2':
        print(load_excel(file_path))
    elif option == '3':
        print(load_sqlite(file_path))
    else:
        print("Invalid option. Please select an option between 1 and 3.")

#Display menu
if __name__ == "__main__":
   import_data_menu()

#with open("corrupt_file.xlsx", "w") as f:
 #   f.write("This is not a valid Excel file.")
#load_excel("corrupt_file.xlsx")


#archive="D:/Escritorio/Carpeta Universidade/2024-2025/1C/PROYECTO IS/baleiro.xlsx"
#print(load_excel(archive))

#chmod 000 path/to/protected_file.xlsx
#"D:/Escritorio/Carpeta Universidade/2024-2025/1C/PROYECTO IS/protected.xlsx"