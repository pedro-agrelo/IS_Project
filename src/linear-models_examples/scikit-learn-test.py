import os
import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error, r2_score

# Function to load files
def load_file(file_path):
    """
    Function to load CSV, XLSX, XLS, and SQLite database files.
    It checks for corrupt, empty, and invalid files.
    """
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError("The file does not exist. Please verify the path.")

        # Check the file extension
        ext = os.path.splitext(file_path)[1].lower()

        # Load CSV file
        if ext == '.csv':
            data = pd.read_csv(file_path)
        # Load Excel file (xlsx, xls)
        elif ext in ['.xlsx', '.xls']:
            data = pd.read_excel(file_path)
        # Load SQLite or DB file
        elif ext in ['.sqlite', '.db']:
            conn = sqlite3.connect(file_path)
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            tables = pd.read_sql(query, conn)
            if tables.empty:
                raise ValueError("The database does not contain any tables.")
            table_name = tables['name'][0]  # Use the first available table
            data = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        else:
            raise ValueError("Unsupported file type. Use CSV, XLSX, XLS, or SQLite/DB.")
        
        # Check if the file is empty
        if data.empty:
            raise ValueError("The file is empty.")
        
        print("File loaded successfully.")
        return data

    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty or corrupt.")
    except sqlite3.DatabaseError:
        print("Error: The SQLite database is invalid or corrupt.")
    except Exception as e:
        print(f"Error: {e}")

# Function to preprocess the data
def preprocess_data(data):
    """
    Preprocess the data for model training.
    It assumes that the target column is 'median_house_value' and excludes the categorical 'ocean_proximity'.
    """
    # Fill missing values in the 'total_bedrooms' column
    if 'total_bedrooms' in data.columns:
        data['total_bedrooms'] = data['total_bedrooms'].fillna(data['total_bedrooms'].mean())  # Direct assignment

    # Select features (X) and target variable (y)
    if 'median_house_value' in data.columns:
        X = data.drop(columns=['median_house_value', 'ocean_proximity'])  # Exclude target and categorical column
        y = data['median_house_value']
        return X, y
    else:
        print("The data does not have the 'median_house_value' column.")
        return None, None

# Function to train the model
def train_model(X, y):
    """
    Train a linear regression model with preprocessed data.
    Returns the model and performance metrics on training (MSE and R²).
    """
    # Split data into training and testing sets (70% training, 30% testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Create and train the linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predictions on the training data
    y_train_pred = model.predict(X_train)

    # Calculate training error (MSE and R²)
    mse_train = root_mean_squared_error(y_train, y_train_pred)
    r2_train = r2_score(y_train, y_train_pred)

    print(f"Mean Squared Error (MSE) on training: {mse_train}")
    print(f"R² score on training: {r2_train}")
    
    return model

# Main execution
if __name__ == "__main__":
    # Ask the user for the file path
    file_path = input("Enter the file path: ")
    
    # Step 1: Load the data
    data = load_file(file_path)
    
    if data is not None:
        # Step 2: Preprocess the data
        X, y = preprocess_data(data)
        
        if X is not None and y is not None:
            # Step 3: Train the model
            train_model(X, y)

# D:/Escritorio/Carpeta Universidade/2024-2025/1C/PROYECTO IS/housing.xlsx

