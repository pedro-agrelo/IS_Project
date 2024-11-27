import pytest
import pandas as pd
from sklearn.linear_model import LinearRegression
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'D:/CopiaPedro/CLASE/2º/SOFTWARE/Proyecto/IS_Project/src/interface')))
from LinearModel import LinearModelModel
import joblib
from tempfile import NamedTemporaryFile

def test_create_model():
    # Crear datos de ejemplo
    data = {
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [2, 4, 6, 8, 10],
        'target': [1.1, 2.0, 2.9, 4.1, 5.0]
    }
    df = pd.DataFrame(data)

    # Instanciar el modelo
    model = LinearModelModel(df)

    # Definir columnas de entrada y salida
    entry_columns = ['feature1', 'feature2']
    target_column = 'target'

    # Llamar al método create_model
    result = model.create_model(entry_columns, target_column)

    # Verificar que el modelo se creó correctamente
    assert result is True, "El modelo no se creó correctamente."
    assert isinstance(model.model, LinearRegression), "El modelo no es una instancia de LinearRegression."

    # Verificar las columnas seleccionadas
    assert model.entry_columns == entry_columns, "Las columnas de entrada no coinciden."
    assert model.target_column == target_column, "La columna objetivo no coincide."

    # Verificar que se generó la fórmula correctamente
    assert model.formula.startswith(f"{target_column} ="), "La fórmula no se generó correctamente."
    assert len(model.formula) > 0, "La fórmula está vacía."

    # Verificar las métricas
    assert "Training MAE" in model.errors, "Las métricas de error no se generaron correctamente."
    assert "Test MAE" in model.errors, "Las métricas de error no incluyen el conjunto de prueba."

def test_save_model():
    # Crear datos de ejemplo
    data = {
        'feature1': [1, 2, 3],
        'feature2': [4, 5, 6],
        'target': [7, 8, 9]
    }
    df = pd.DataFrame(data)

    # Crear instancia del modelo
    model = LinearModelModel(df)
    model.entry_columns = ['feature1', 'feature2']
    model.target_column = 'target'
    model.model = "mock_model"  # Usar un mock para simplificar la prueba
    model.description = "Mock model for testing"
    model.formula = "target = 0.1*feature1 + 0.2*feature2 + 0.3"
    model.errors = "MAE: 0.1, RMSE: 0.2, R²: 0.9"

    # Guardar el modelo en un archivo temporal
    with NamedTemporaryFile(delete=False, suffix=".joblib") as temp_file:
        file_path = temp_file.name
        model.save_model(file_path)

    # Verificar que el archivo se creó
    assert os.path.exists(file_path), "El archivo no fue creado por save_model."

    # Cargar el archivo y verificar su contenido
    loaded_data = joblib.load(file_path)
    assert loaded_data["input_columns"] == ['feature1', 'feature2'], "Las columnas de entrada no coinciden."
    assert loaded_data["output_column"] == 'target', "La columna objetivo no coincide."
    assert loaded_data["description"] == "Mock model for testing", "La descripción no coincide."
    assert loaded_data["formula"] == "target = 0.1*feature1 + 0.2*feature2 + 0.3", "La fórmula no coincide."
    assert loaded_data["errors"] == "MAE: 0.1, RMSE: 0.2, R²: 0.9", "Las métricas de error no coinciden."
    assert loaded_data["df"].equals(df), "El DataFrame no coincide."

    # Limpiar el archivo temporal
    os.remove(file_path)

def test_load_model():
    # Crear datos simulados para el archivo
    data = {
        'feature1': [1, 2, 3],
        'feature2': [4, 5, 6],
        'target': [7, 8, 9]
    }
    df = pd.DataFrame(data)
    mock_data = {
        "model": "mock_model",
        "input_columns": ['feature1', 'feature2'],
        "output_column": 'target',
        "errors": "MAE: 0.1, RMSE: 0.2, R²: 0.9",
        "description": "Mock model for testing",
        "formula": "target = 0.1*feature1 + 0.2*feature2 + 0.3",
        "df": df
    }

    # Guardar datos simulados en un archivo temporal
    with NamedTemporaryFile(delete=False, suffix=".joblib") as temp_file:
        file_path = temp_file.name
        joblib.dump(mock_data, file_path)

    # Cargar los datos con el método load_model
    model = LinearModelModel(None)
    result = model.load_model(file_path)

    # Verificar que los datos se cargaron correctamente
    assert result is True, "load_model no devolvió True."
    assert model.model == "mock_model", "El modelo no coincide."
    assert model.entry_columns == ['feature1', 'feature2'], "Las columnas de entrada no coinciden."
    assert model.target_column == 'target', "La columna objetivo no coincide."
    assert model.description == "Mock model for testing", "La descripción no coincide."
    assert model.formula == "target = 0.1*feature1 + 0.2*feature2 + 0.3", "La fórmula no coincide."
    assert model.errors == "MAE: 0.1, RMSE: 0.2, R²: 0.9", "Las métricas de error no coinciden."
    assert model.df.equals(df), "El DataFrame no coincide."

    # Limpiar el archivo temporal
    os.remove(file_path)
