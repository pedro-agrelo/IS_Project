import pickle
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scikittest import load_file, preprocess_data, train_model

#Usando el módulo de test de scikitt:
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
            model=train_model(X, y)

# Guardar el modelo en un archivo con pickle
with open('linear_model.pkl', 'wb') as file:
    pickle.dump(model, file)

# Cargar el modelo desde el archivo
with open('linear_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# Prueba para asegurar que el modelo funciona después de la carga
y_pred_original = model.predict(X)
y_pred_loaded = loaded_model.predict(X)

# Comparar los resultados antes y después de la carga
print("Error cuadrático medio antes de guardar:", mean_squared_error(y, y_pred_original))
print("Error cuadrático medio después de cargar:", mean_squared_error(y, y_pred_loaded))
