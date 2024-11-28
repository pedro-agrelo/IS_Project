import os
import pandas as pd
from PyQt5.QtWidgets import (QTableWidget, QTableWidgetItem, QHeaderView)
import sqlite3
import os
import pandas as pd

class DataTableModel:
    def __init__(self):
        self.df = pd.DataFrame()  # Inicialmente vacío

    def load_file(self, file_name):
        """Carga el archivo seleccionado en el modelo (DataFrame)."""
        try:
            file_extension = os.path.splitext(file_name)[1].lower()

            if file_extension == '.csv':
                self.df = pd.read_csv(file_name)
            elif file_extension in ['.xlsx', '.xls']:
                self.df = pd.read_excel(file_name)
            elif file_extension in ['.sqlite', '.db']:
                conn = sqlite3.connect(file_name)
                query = "SELECT name FROM sqlite_master WHERE type='table';"
                tables = pd.read_sql(query, conn)
                if tables.empty:
                    return False  # No continuar si está vacío
                first_table = tables['name'][0]
                self.df = pd.read_sql(f"SELECT * FROM {first_table};", conn)
                conn.close()

            if self.df.empty:
                return False  # No continuar si está vacío

            return True
        
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            return False
    
    def get_data(self):
        """Devuelve el DataFrame actual."""
        return self.df


class DataTableView(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setVisible(False)  # Inicialmente oculto
        self.setStyleSheet("""
        QTableWidget { 
            background-color: #2E2E2E;  /* Fondo gris oscuro para las celdas */
            color: white;  /* Texto en blanco */
        }
        QHeaderView::section {
            background-color: #4A4A4A;  /* Fondo gris más claro para las cabeceras */
            color: #E0E0E0;  /* Texto gris claro en cabeceras */
            font-weight: bold;  /* Negrita */
            padding: 4px;
            border: 1px solid #666666;  /* Borde sutil */
        }
        QTableCornerButton::section {
            background-color: #4A4A4A;  /* Fondo gris claro para la esquina superior izquierda */
            border: 1px solid #666666;  /* Mismo borde que las cabeceras */}""")
        
    def update_table(self, df):
        """Actualiza el contenido de la tabla con el DataFrame."""
        self.clear()  # Limpiar la tabla para eliminar cualquier contenido previo

        self.setRowCount(df.shape[0])
        self.setColumnCount(df.shape[1])
        
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))


        # Ajustar el tamaño de las cabeceras
        self.setHorizontalHeaderLabels(df.columns)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Ajustar el comportamiento de las columnas y filas
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        return

class DataTableController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        # Conectar las señales y slots (en caso de que haya acciones del usuario)
        # Si usas señales y slots, puedes conectar aquí las acciones del usuario con los métodos del controlador

    def load_file(self, file_name):
        """Carga los datos desde el archivo usando el modelo y actualiza la vista."""
        if self.model.load_file(file_name):
            # Obtener el DataFrame actualizado
            df = self.model.get_data()

            # Actualizar la vista con los nuevos datos
            self.view.update_table(df)
            return True
        else:
            self.view.setVisible(False)
            return False
        
    def update_table(self, df):
        """Actualiza el contenido de la tabla con el DataFrame."""
        self.model.df = df
        self.view.update_table(df)
        