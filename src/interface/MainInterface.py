import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QFileDialog, QLabel,QVBoxLayout, QWidget,QMessageBox)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from DataTable import DataTable
from ColumnSelector import ColumnSelector

        

class FileExplorerInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('File Explorer - CSV, Excel and SQLite')
        self.setGeometry(300, 150, 800, 600)  # Aumentar tamaño para la tabla
        self.column_selector = ColumnSelector()

        # Llamar a los métodos de estilo y configuración
        self.setup_ui()
        self.apply_styles()
        
    def show_empty_file_message(self):
        """Muestra un mensaje de advertencia si el archivo está vacío"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Empty file")
        msg.setText("El archivo seleccionado está vacío.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def setup_ui(self):
        """Configura el diseño y widgets de la interfaz"""
        layout = QVBoxLayout()

        # Crear una etiqueta para mostrar el mensaje inicial
        self.label = QLabel("Select a CSV, Excel or SQLite file")
        self.label.setAlignment(Qt.AlignCenter)  # Centrar el texto
        self.label.setFont(QFont("Arial", 14))
        self.label.setStyleSheet("color: white;")  # Letras blancas para el tema oscuro
        layout.addWidget(self.label)

        # Crear un botón para abrir el explorador de archivos
        self.button = QPushButton('Open File Explorer')
        self.button.setFixedSize(300, 50)  # Tamaño fijo para el botón
        self.button.setFont(QFont("Arial", 12, QFont.Bold))  # Aplicar fuente y tamaño al botón
        self.button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)  # Centrar el botón

        # Crear un widget de tabla para mostrar los datos, pero ocultarlo al principio
        self.table_widget = DataTable()
        layout.addWidget(self.table_widget)

        # Crear un contenedor central con el layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        #selector columnas
        self.column_selector = ColumnSelector(self)
        layout.addWidget(self.column_selector)


    def open_file_dialog(self):
        """Abre el diálogo de selección de archivos con filtros y carga el archivo en la tabla"""
        options = QFileDialog.Options()
        
        # Unificar todas las extensiones en un solo filtro
        file_filter = "Archivos compatibles (*.csv *.xlsx *.xls *.sqlite *.db)" #filtro para el buscador de archivos
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "", file_filter, options=options)

        # Actualizar el texto del label con el archivo seleccionado
        if file_name:
            self.label.setText(f"<b>Selected file:</b> <br><i>{file_name}</i>")
            self.label.setStyleSheet("color: #FFFFFF;")  
            if self.table_widget.load_file(file_name):  # Cargar el archivo y mostrarlo en la tabla
                headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]
                self.column_selector.update_selectors(headers)
                self.column_selector.setVisible(True)
                
            else:
                self.column_selector.setVisible(False)
                self.show_empty_file_message()
                

        else:
            self.table_widget.setVisible(False)
            self.column_selector.setVisible(False)
            self.label.setText("<b>No file selected</b>")
            self.label.setStyleSheet("color: #FF6347;")  


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
    window = FileExplorerInterface()
    window.show()
    sys.exit(app.exec_())
