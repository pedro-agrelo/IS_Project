import os
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget,QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt


class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Explorador de Archivos - CSV, Excel y SQLite')
        self.setGeometry(300, 150, 800, 600)  # Aumentar tamaño para la tabla

        # Llamar a los métodos de estilo y configuración
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        """Configura el diseño y widgets de la interfaz"""
        layout = QVBoxLayout()

        # Crear una etiqueta para mostrar el mensaje inicial
        self.label = QLabel("Selecciona un archivo CSV, Excel o SQLite")
        self.label.setAlignment(Qt.AlignCenter)  # Centrar el texto
        self.label.setFont(QFont("Arial", 14))
        self.label.setStyleSheet("color: white;")  # Letras blancas para el tema oscuro
        layout.addWidget(self.label)

        # Crear un botón para abrir el explorador de archivos
        self.button = QPushButton('Abrir Explorador de Archivos')
        self.button.setFixedSize(300, 50)  # Tamaño fijo para el botón
        self.button.setFont(QFont("Arial", 12, QFont.Bold))  # Aplicar fuente y tamaño al botón
        self.button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)  # Centrar el botón

        # Crear un widget de tabla para mostrar los datos, pero ocultarlo al principio
        self.table_widget = QTableWidget()
        self.table_widget.setVisible(False)  # Inicialmente oculto
        layout.addWidget(self.table_widget)

        # Crear un contenedor central con el layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


    def open_file_dialog(self):
        """Abre el diálogo de selección de archivos con filtros y carga el archivo en la tabla"""
        options = QFileDialog.Options()
        
        # Unificar todas las extensiones en un solo filtro
        file_filter = "Archivos compatibles (*.csv *.xlsx *.xls *.sqlite *.db)" #filtro para el buscador de archivos
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo", "", file_filter, options=options)

        # Actualizar el texto del label con el archivo seleccionado
        if file_name:
            self.label.setText(f"<b>Archivo seleccionado:</b> <br><i>{file_name}</i>")
            self.label.setStyleSheet("color: #FFFFFF;")  
            self.load_file(file_name)  # Cargar el archivo y mostrarlo en la tabla
        else:
            self.label.setText("<b>No se seleccionó ningún archivo</b>")
            self.label.setStyleSheet("color: #FF6347;")  


    def load_file(self, file_name):
        """Carga el archivo seleccionado en la tabla"""
        file_extension = os.path.splitext(file_name)[1].lower()

        # Identificar el tipo de archivo y cargarlo con pandas
        if file_extension in ['.csv']:
            df = pd.read_csv(file_name)
            
        elif file_extension in ['.xlsx','.xls']:
            df = pd.read_excel(file_name)

        elif file_extension in ['.sqlite','.db']:
            import sqlite3
            conn = sqlite3.connect(file_name)
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            tables = pd.read_sql(query, conn)
            print(tables.empty)
            if tables.empty:
                self.show_empty_file_message()  # Mostrar un mensaje si el archivo está vacío
                return  # No continuar si está vacío
            
            first_table = tables['name'][0]  # Get the name of the table
            df = pd.read_sql(f"SELECT * FROM {first_table};", conn)
            conn.close()
            
        # Verificar si el DataFrame está vacío
        if df.empty:
            self.show_empty_file_message()  # Mostrar un mensaje si el archivo está vacío
            return  # No continuar si está vacío

        # Establecer la cantidad de filas y columnas en el QTableWidget
        self.table_widget.setRowCount(df.shape[0])
        self.table_widget.setColumnCount(df.shape[1])




        # Rellenar la tabla con los datos
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

        # Ajustar el comportamiento de las columnas y filas
        self.table_widget.resizeColumnsToContents()  # Ajusta el tamaño de las columnas
        self.table_widget.resizeRowsToContents()  # Ajusta el tamaño de las filas

        # Habilitar scroll horizontal y vertical
        self.table_widget.setHorizontalScrollMode(self.table_widget.ScrollPerPixel)
        self.table_widget.setVerticalScrollMode(self.table_widget.ScrollPerPixel)

        # Ajustar el tamaño de las cabeceras para que se adapten al contenido
        self.table_widget.setHorizontalHeaderLabels(df.columns)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Hacer visible la tabla después de cargar el archivo
        self.table_widget.setVisible(True)


    def show_empty_file_message(self):
        """Muestra un mensaje de advertencia si el archivo está vacío"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Archivo vacío")
        msg.setText("El archivo seleccionado está vacío.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


    def apply_styles(self):
        """Aplica estilos (QSS) a los widgets"""
        # Aplicar colores al botón con el tema oscuro
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #333333;  /* Gris oscuro para el botón */
                color: white;
                border-radius: 10px;
                border: 2px solid #FFFFFF;  /* Borde blanco */
            }
            QPushButton:hover {
                background-color: #555555;  /* Efecto hover más claro */
            }
        """)

        # Cambiar el color de fondo de la ventana al negro/gris oscuro
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))  # Fondo negro/gris oscuro
        self.setPalette(palette)

# Ejecutar la aplicación
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileExplorer()
    window.show()
    sys.exit(app.exec_())
