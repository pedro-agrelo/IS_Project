import pytest
import pandas as pd
from sklearn.linear_model import LinearRegression
import sys
import os
import joblib
from tempfile import NamedTemporaryFile
# Agregar la carpeta 'modulo' al path
sys.path.append(os.path.abspath("D:/CopiaPedro/CLASE/2º/SOFTWARE/Proyecto/IS_Project/src/interface"))
from DataTable import DataTableModel

def test_load_data():
    # Crear el DataFrame
    data = {
        "Nombre": ["Alice", "Bob", "Charlie", "Diana"],
        "Edad": [25, 30, 35, 40],
        "Ciudad": ["Madrid", "Barcelona", "Valencia", "Sevilla"]
    }

    df = pd.DataFrame(data)

    #crear el gestor de datos de la tabla
    model = DataTableModel()
    model.load_file("D:/CopiaPedro/CLASE/2º/SOFTWARE/Proyecto/TestData.xlsx")
    assert model.df.equals(df)
