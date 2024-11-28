import os
import pandas as pd
import sqlite3
from PyQt5.QtWidgets import QHeaderView, QTableView, QSizePolicy, QAbstractScrollArea
from PyQt5.QtCore import Qt, QAbstractTableModel


class DataTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.df = pd.DataFrame()  # Inicialmente vacío

    def setDataFrame(self, dataframe):
        """
        Método para establecer un nuevo DataFrame en el modelo.
        """
        self.beginResetModel()  # Notificar el inicio del cambio de datos
        self.df = dataframe
        self.endResetModel()  # Notificar el fin del cambio de datos

    def rowCount(self, parent=None):
        """
        Devuelve el número de filas en el DataFrame.
        """
        return self.df.shape[0]

    def columnCount(self, parent=None):
        """
        Devuelve el número de columnas en el DataFrame.
        """
        return self.df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        """
        Devuelve el dato para una celda dada (fila, columna).
        """
        if not index.isValid():
            return None
        
        if role == Qt.DisplayRole:  # Mostrar datos en la vista
            value = self.df.iloc[index.row(), index.column()]
            return str(value)
        
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        Devuelve los encabezados de las columnas o los índices de las filas.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                # Encabezados de columna
                return self.df.columns[section]
            elif orientation == Qt.Vertical:
                # Encabezados de fila
                return section + 1 

        return None

    def load_file(self, file_name):
        """
        Carga el archivo seleccionado en el modelo como DataFrame.
        """
        try:
            file_extension = os.path.splitext(file_name)[1].lower()

            if file_extension == '.csv':
                df = pd.read_csv(file_name)
            elif file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(file_name)
            elif file_extension in ['.sqlite', '.db']:
                conn = sqlite3.connect(file_name)
                query = "SELECT name FROM sqlite_master WHERE type='table';"
                tables = pd.read_sql(query, conn)
                if tables.empty:
                    raise ValueError("El archivo SQLite no contiene tablas.")
                first_table = tables['name'][0]
                df = pd.read_sql(f"SELECT * FROM {first_table};", conn)
                conn.close()
            else:
                raise ValueError(f"Extensión de archivo no soportada: {file_extension}")

            if df.empty:
                raise ValueError("El archivo no contiene datos.")

            self.setDataFrame(df)
            return True

        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            return False

    def get_data(self):
        """
        Devuelve el DataFrame actual.
        """
        return self.df


class DataTableView(QTableView):
    def __init__(self):
        super().__init__()
        self.setVisible(False)  # Inicialmente oculto
        self.setStyleSheet("""
        QTableView { 
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
        }""")
        
    def update_table(self, model):
        """
        Actualiza el contenido de la tabla con el modelo.
        """
        self.setModel(model)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


class DataTableController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

    def load_file(self, file_name):
        """
        Carga los datos desde el archivo usando el modelo y actualiza la vista.
        """
        if self.model.load_file(file_name):
            self.view.update_table(self.model)
            return True
        else:
            self.view.setVisible(False)
            return False

    def update_table(self):
        """
        Actualiza el contenido de la tabla con el modelo actual.
        """
        self.view.update_table(self.model)