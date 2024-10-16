import sys
import os
import pandas as pd
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QGroupBox, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle('Gestor de Datasets')
        self.setGeometry(100, 100, 1000, 700)  # Aumenta el tamaño para uso profesional

        # Estilo global (fuentes y color de fondo)
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f4f4;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                font-size: 14px;
                border-radius: 5px;
                padding: 10px 15px;
                border: none;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
            QGroupBox {
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                padding: 20px;
                background-color: #FFF;
                color: #333;
                font-weight: bold;
                font-size: 14px;
            }
            QTableWidget {
                background-color: #FFF;
                border: 1px solid #CCC;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #F1F1F1;
                padding: 4px;
                border: 1px solid #CCC;
                font-size: 13px;
                color: #333;
            }
        """)

        # Crear el layout principal
        layout = QVBoxLayout()

        # Grupo para la selección de archivo
        group_box = QGroupBox("Cargar Dataset")
        group_layout = QVBoxLayout()

        # Etiqueta para mostrar la ruta del archivo
        self.label_ruta = QLabel('Ruta del archivo: Ningún archivo cargado')
        self.label_ruta.setFont(QFont('Arial', 11))
        self.label_ruta.setStyleSheet("color: #0078D4; padding: 5px;")
        group_layout.addWidget(self.label_ruta)

        # Botón para abrir el explorador de archivos
        self.boton_cargar = QPushButton('Seleccionar archivo')
        self.boton_cargar.setFont(QFont('Arial', 12, QFont.Bold))
        self.boton_cargar.clicked.connect(self.open_file_dialog)  # Cambiado a la nueva función
        group_layout.addWidget(self.boton_cargar)

        # Espaciado entre el botón y el contenido
        group_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)

        # Tabla para mostrar los datos cargados
        self.tabla_datos = QTableWidget()
        self.tabla_datos.setStyleSheet("border: 1px solid #ccc; background-color: #fff;")
        layout.addWidget(self.tabla_datos)

        # Ajuste del layout
        self.setLayout(layout)

    def open_file_dialog(self):
        """Abre el diálogo de selección de archivos con filtros y carga el archivo en la tabla"""
        options = QFileDialog.Options()
        
        # Unificar todas las extensiones en un solo filtro
        file_filter = "Archivos compatibles (*.csv *.xlsx *.xls *.sqlite *.db)"  # Filtro para el buscador de archivos
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo", "", file_filter, options=options)

        # Actualizar el texto del label con el archivo seleccionado
        if file_name:
            self.label_ruta.setText(f'Ruta del archivo: <i>{file_name}</i>')
            self.label_ruta.setStyleSheet("color: #FF6347;")  
            self.load_file(file_name)  # Cargar el archivo y mostrarlo en la tabla
        else:
            self.label_ruta.setText("<b>No se seleccionó ningún archivo</b>")
            self.label_ruta.setStyleSheet("color: #FF6347;")  

    def load_file(self, file_name):
        """Carga el archivo seleccionado y lo muestra en la tabla"""
        file_extension = os.path.splitext(file_name)[1].lower()

        # Identificar el tipo de archivo y cargarlo con pandas
        if file_extension == '.csv':
            df = pd.read_csv(file_name)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_name)
        elif file_extension in ['.sqlite', '.db']:
            conn = sqlite3.connect(file_name)
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            tables = pd.read_sql(query, conn)

            if tables.empty:
                self.show_empty_file_message()  # Mostrar mensaje si no hay tablas
                return
            
            first_table = tables['name'][0]  # Obtener el nombre de la primera tabla
            df = pd.read_sql(f"SELECT * FROM {first_table};", conn)
            conn.close()
        else:
            QMessageBox.critical(self, 'Error', "Formato de archivo no soportado.")
            return

        # Verificar si el DataFrame está vacío
        if df.empty:
            self.show_empty_file_message()  # Mostrar mensaje si el archivo está vacío
            return

        # Configurar la tabla para mostrar los datos
        self.tabla_datos.setColumnCount(len(df.columns))
        self.tabla_datos.setRowCount(len(df.index))
        self.tabla_datos.setHorizontalHeaderLabels(df.columns)

        # Insertar los datos en la tabla
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                self.tabla_datos.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

        # Ajustar el tamaño de las columnas al contenido
        self.tabla_datos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_datos.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def show_empty_file_message(self):
        """Muestra un mensaje de advertencia si el archivo está vacío"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Archivo vacío")
        msg.setText("El archivo seleccionado está vacío.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

# Código principal
if __name__ == '__main__':
    app = QApplication(sys.argv)

    ventana = VentanaPrincipal()
    ventana.show()

    sys.exit(app.exec_())

