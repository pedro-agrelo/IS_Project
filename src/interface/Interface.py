import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog, QLabel,
                             QVBoxLayout, QHBoxLayout, QWidget, QMessageBox)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from DataTable import DataTable
from ColumnSelector import ColumnSelector
from DataPreprocessor import DataPreprocessor
from Linear_Model2 import LinearModel

class FileExplorerInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('File Explorer - CSV, Excel and SQLite')
        self.setGeometry(300, 150, 800, 600)  # Tamaño de la ventana
        self.column_selector = ColumnSelector()

        # Configuración de la interfaz
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        """Configura el diseño y widgets de la interfaz"""
        # Layout principal vertical
        main_layout = QVBoxLayout()

        # Etiqueta para mostrar el mensaje inicial
        self.label = QLabel("Select a CSV, Excel or SQLite file")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 14))
        self.label.setStyleSheet("color: white;")
        main_layout.addWidget(self.label)

        # Botón para abrir el explorador de archivos
        self.button = QPushButton('Open File Explorer')
        self.button.setFixedSize(300, 50)
        self.button.setFont(QFont("Arial", 16, QFont.Bold))  # Aumentar tamaño de letra
        self.button.clicked.connect(self.open_file_dialog)
        main_layout.addWidget(self.button, alignment=Qt.AlignCenter)

        # Tabla para mostrar los datos
        self.table_widget = DataTable()
        main_layout.addWidget(self.table_widget)

        # Layout horizontal para el selector de columnas y el preprocesador
        selector_preprocessor_layout = QHBoxLayout()
        selector_preprocessor_layout.setContentsMargins(20, 0, 0, 0)  # Margen izquierdo de 20 píxeles

        # Selector de columnas
        self.column_selector = ColumnSelector(self)
        self.column_selector.setFixedWidth(800)  # Ajustar el ancho del selector de columnas
        selector_preprocessor_layout.addWidget(self.column_selector)

        # Preprocesador
        self.data_preprocessor = DataPreprocessor(self.table_widget, self.column_selector)
        selector_preprocessor_layout.addWidget(self.data_preprocessor)
        self.data_preprocessor.setVisible(False)  # Ocultamos el preprocesador hasta que se cargue un archivo

        # Agregar el layout horizontal al layout principal
        main_layout.addLayout(selector_preprocessor_layout)

        # Modelo lineal
        self.linear_model_widget = LinearModel(self.table_widget, self.column_selector)
        self.linear_model_widget.setVisible(False)
        main_layout.addWidget(self.linear_model_widget)

        # Botón para crear el modelo
        self.create_model_button = QPushButton("Create Linear Model")
        self.create_model_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.create_model_button.clicked.connect(self.create_model)
        self.create_model_button.setVisible(False)
        main_layout.addWidget(self.create_model_button)

        # Contenedor central
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def show_empty_file_message(self):
        """Muestra un mensaje de advertencia si el archivo está vacío"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Empty file")
        msg.setText("El archivo seleccionado está vacío.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def open_file_dialog(self):
        """Abre el diálogo de selección de archivos con filtros y carga el archivo en la tabla"""
        options = QFileDialog.Options()
        file_filter = "Archivos compatibles (*.csv *.xlsx *.xls *.sqlite *.db)"
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "", file_filter, options=options)

        if file_name:
            self.label.setText(f"<b>Selected file:</b> <br><i>{file_name}</i>")
            if self.table_widget.load_file(file_name):
                headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]
                self.column_selector.update_selectors(headers)
                self.linear_model_widget.setVisible(False)
                self.column_selector.setVisible(True)
                self.data_preprocessor.setVisible(True) 
                self.create_model_button.setVisible(True) 
                self.column_selector.confirm_button.setVisible(True)  # Mostrar el botón de confirmación
                self.label.setStyleSheet("color: #FFFFFF;")

            else:
                self.column_selector.setVisible(False)
                self.column_selector.confirm_button.setVisible(False)  # Ocultar el botón si no se carga el archivo
                self.data_preprocessor.setVisible(False)
                self.create_model_button.setVisible(False)
                self.show_empty_file_message()
        else:
            self.table_widget.setVisible(False)
            self.column_selector.setVisible(False)
            self.data_preprocessor.setVisible(False)
            self.create_model_button.setVisible(False)
            self.column_selector.confirm_button.setVisible(False)  # Ocultar el botón si no hay archivo
            self.label.setText("<b>No file selected</b>")
            self.label.setStyleSheet("color: #FF6347;")

    def apply_styles(self):
        """Aplica estilos (QSS) a los widgets"""
        # Estilos para el botón de abrir archivo y el botón de confirmar selección
        button_style = """
            QPushButton {
                background-color: #333333;
                color: white;
                border-radius: 10px;
                border: 2px solid #FFFFFF;
                font-size: 16px;  /* Aumentar el tamaño de la letra */
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """
        self.button.setStyleSheet(button_style)  # Botón de abrir archivos

        # Estilos de la ventana y paleta de colores
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        self.setPalette(palette)

    def create_model(self):
        if self.linear_model_widget.create_model():
            self.table_widget.setVisible(False)
            self.column_selector.setVisible(False)
            self.data_preprocessor.setVisible(False)
            self.create_model_button.setVisible(False)
            self.linear_model_widget.setVisible(True)
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileExplorerInterface()
    window.show()
    sys.exit(app.exec_())