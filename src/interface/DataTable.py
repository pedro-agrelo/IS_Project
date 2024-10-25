import os
import pandas as pd
from PyQt5.QtWidgets import (QTableWidget, QTableWidgetItem, QHeaderView)


class DataTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setVisible(False)  # Inicialmente oculto
        self.df = pd.DataFrame()  # Inicialmente vacío

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
        border: 1px solid #666666;  /* Mismo borde que las cabeceras */
    }
""")
        
    def load_file(self, file_name):
        """Carga el archivo seleccionado en la tabla"""
        file_extension = os.path.splitext(file_name)[1].lower()

        # Identificar el tipo de archivo y cargarlo con pandas
        if file_extension in ['.csv']:
            self.df = pd.read_csv(file_name)
            
        elif file_extension in ['.xlsx','.xls']:
            self.df = pd.read_excel(file_name)

        elif file_extension in ['.sqlite','.db']:
            import sqlite3
            conn = sqlite3.connect(file_name)
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            tables = pd.read_sql(query, conn)
            if tables.empty:
                self.setVisible(False)
                return False # No continuar si está vacío
            
            first_table = tables['name'][0]  # Get the name of the table
            self.df = pd.read_sql(f"SELECT * FROM {first_table};", conn)
            conn.close()
            
        # Verificar si el DataFrame está vacío
        if self.df.empty:
            self.setVisible(False)
            return False  # No continuar si está vacío

        # Establecer la cantidad de filas y columnas en el QTableWidget
        self.setRowCount(self.df.shape[0])
        self.setColumnCount(self.df.shape[1])

        # Rellenar la tabla con los datos
        for i in range(self.df.shape[0]):
            for j in range(self.df.shape[1]):
                self.setItem(i, j, QTableWidgetItem(str(self.df.iat[i, j])))

        # Ajustar el comportamiento de las columnas y filas
        self.resizeColumnsToContents()  # Ajusta el tamaño de las columnas
        self.resizeRowsToContents()  # Ajusta el tamaño de las filas

        # Habilitar scroll horizontal y vertical
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.setVerticalScrollMode(self.ScrollPerPixel)

        # Ajustar el tamaño de las cabeceras para que se adapten al contenido
        self.setHorizontalHeaderLabels(self.df.columns)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Hacer visible la tabla después de cargar el archivo
        self.setVisible(True)
        return True
    
    def update_table(self, df):
        self.df = df
        # Establecer la cantidad de filas y columnas en el QTableWidget
        self.setRowCount(self.df.shape[0])
        self.setColumnCount(self.df.shape[1])

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

        # Ajustar el comportamiento de las columnas y filas
        self.resizeColumnsToContents()  # Ajusta el tamaño de las columnas
        self.resizeRowsToContents()  # Ajusta el tamaño de las filas

        # Habilitar scroll horizontal y vertical
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.setVerticalScrollMode(self.ScrollPerPixel)

        # Ajustar el tamaño de las cabeceras para que se adapten al contenido
        self.setHorizontalHeaderLabels(self.df.columns)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)