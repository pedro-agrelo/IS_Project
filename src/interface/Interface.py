import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog, QLabel,
                             QVBoxLayout, QWidget, QMessageBox)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from DataTable import DataTable
from ColumnSelector import ColumnSelector

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
        layout = QVBoxLayout()

        # Etiqueta para mostrar el mensaje inicial
        self.label = QLabel("Select a CSV, Excel or SQLite file")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 14))
        self.label.setStyleSheet("color: white;")
        layout.addWidget(self.label)

        # Botón para abrir el explorador de archivos
        self.button = QPushButton('Open File Explorer')
        self.button.setFixedSize(300, 50)
        self.button.setFont(QFont("Arial", 16, QFont.Bold))  # Aumentar tamaño de letra
        self.button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)

        # Tabla para mostrar los datos
        self.table_widget = DataTable()
        layout.addWidget(self.table_widget)

        # Selector de columnas
        self.column_selector = ColumnSelector(self)
        layout.addWidget(self.column_selector)

        # Botón para confirmar selección (No visible al principio)
        self.confirm_button = QPushButton('Confirm columns selection')
        self.confirm_button.setFixedSize(300, 50)
        self.confirm_button.setVisible(False)  # Ocultar el botón al inicio
        self.confirm_button.setFont(QFont("Arial", 16, QFont.Bold))  # Aumentar tamaño de letra
        self.confirm_button.clicked.connect(self.confirmar_seleccion)
        layout.addWidget(self.confirm_button, alignment=Qt.AlignCenter)

        # Contenedor central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

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
                self.column_selector.setVisible(True)
                self.confirm_button.setVisible(True)  # Mostrar el botón de confirmación
            else:
                self.column_selector.setVisible(False)
                self.confirm_button.setVisible(False)  # Ocultar el botón si no se carga el archivo
                self.show_empty_file_message()
        else:
            self.table_widget.setVisible(False)
            self.column_selector.setVisible(False)
            self.confirm_button.setVisible(False)  # Ocultar el botón si no hay archivo
            self.label.setText("<b>No file selected</b>")
            self.label.setStyleSheet("color: #FF6347;")

    def confirmar_seleccion(self):
        """Confirma la selección de columnas de entrada y salida"""
        entradas, salida = self.column_selector.get_selected_columns()

        if not entradas or not salida:
            self.mostrar_mensaje("Error", "Debe seleccionar al menos una columna de entrada y una columna de salida.", "warning")
        else:
            self.mostrar_mensaje("Success", f"Selected columns:\nEnter: {entradas}\nExit: {salida}", "success")

    def mostrar_mensaje(self, titulo, mensaje, tipo):
        """Muestra un cuadro de diálogo con el estilo adecuado"""
        msg_box = QMessageBox(self)

        # Ajustar estilo según el tipo de mensaje
        if tipo == "warning":
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #333;
                    color: white;
                }
                QLabel {
                    font-size: 14px;  /* Aumentar el tamaño de la letra */
                    color: white;
                }
                QPushButton {
                    background-color: #555;
                    color: white;
                    border: 2px solid #FFFFFF;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 14px;  /* Aumentar el tamaño de la letra */
                }
                QPushButton:hover {
                    background-color: #777;
                }
            """)
        elif tipo == "success":
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #333;
                    color: white;
                }
                QLabel {
                    font-size: 14px;  /* Aumentar el tamaño de la letra */
                    color: white;
                }
                QPushButton {
                    background-color: #0078d4;
                    color: white;
                    border: 2px solid #FFFFFF;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 14px;  /* Aumentar el tamaño de la letra */
                }
                QPushButton:hover {
                    background-color: #005A9E;
                }
            """)

        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensaje)
        msg_box.exec_()

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
        self.confirm_button.setStyleSheet(button_style)  # Botón de confirmar selección

        # Estilos de la ventana y paleta de colores
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        self.setPalette(palette)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileExplorerInterface()
    window.show()
    sys.exit(app.exec_())
