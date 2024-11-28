import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog, QLabel,
                             QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QProgressBar)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

from DataTable import DataTableModel, DataTableView, DataTableController
from ColumnSelector import ColumnSelectorModel, ColumnSelectorView, ColumnSelectorController
from DataPreprocessor import DataPreprocessorModel, DataPreprocessorView, DataPreprocessorController
from LinearModel import LinearModelModel, LinearModelView, LinearModelController
from Menu import Menu
from Thread import FileLoaderThread
import time

class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Projecta')
        self.setGeometry(200, 300, 900, 800)

        # Configuración de la interfaz
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        """Configura el diseño y widgets de la interfaz"""
        # Layout principal vertical
        main_layout = QVBoxLayout()

        # Persistent toggle button to show/hide the menu
        self.menu_toggle_button = QPushButton("≡")
        self.menu_toggle_button.setFixedSize(60, 30)
        self.menu_toggle_button.setFont(QFont("Arial", 16, QFont.Bold))
        self.menu_toggle_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;  /* Make the background transparent */
                color: white;                    /* White text */
                border: none;                    /* Remove the border */
                padding: 5px;                    /* Add some padding around the text */
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);  /* Light hover effect */
            }
        """)
        self.menu_toggle_button.clicked.connect(self.toggle_menu_visibility)
        main_layout.addWidget(self.menu_toggle_button, alignment=Qt.AlignLeft)

        #progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #FFFFFF;
                border-radius: 5px;
                text-align: center;
                background-color: #333333;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #00BFFF;
                width: 10px;
            }""")
        main_layout.addWidget(self.progress_bar)

        # Etiqueta para mostrar el mensaje inicial
        self.label = QLabel("Select a CSV, Excel or SQLite file")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 14))
        self.label.setStyleSheet("color: white;")
        main_layout.addWidget(self.label)

        # Tabla para mostrar los datos
        self.table_model = DataTableModel()
        self.table_view = DataTableView()
        self.table_controller = DataTableController(self.table_view, self.table_model)
        main_layout.addWidget(self.table_view)

        # Layout horizontal para el selector de columnas y el preprocesador
        selector_preprocessor_layout = QHBoxLayout()
        selector_preprocessor_layout.setContentsMargins(20, 0, 0, 20)  # Margen izquierdo de 20 píxeles

        # Selector de columnas
        self.column_selector_model = ColumnSelectorModel()
        self.column_selector_view = ColumnSelectorView()
        self.column_selector_controller = ColumnSelectorController(self.column_selector_model, self.column_selector_view)

        self.column_selector_view.setFixedSize(800,400)  # Ajustar el ancho del selector de columnas
        selector_preprocessor_layout.addWidget(self.column_selector_view)

        # Preprocesador
        self.data_preprocessor_model = DataPreprocessorModel()
        self.data_preprocessor_view = DataPreprocessorView()
        self.data_preprocessor_controller = DataPreprocessorController(self.data_preprocessor_model, self.data_preprocessor_view)
        self.data_preprocessor_view.empty_cells_button.clicked.connect(self.highlight_empty_cells)
        self.data_preprocessor_view.apply_button.clicked.connect(self.apply_preprocess)
        selector_preprocessor_layout.addWidget(self.data_preprocessor_view)
        self.data_preprocessor_view.setVisible(False)  # Ocultamos el preprocesador hasta que se cargue un archivo

        # Agregar el layout horizontal al layout principal
        main_layout.addLayout(selector_preprocessor_layout)

        # Modelo lineal
        self.linear_model_model = LinearModelModel(self.table_model.df)
        self.linear_model_view = LinearModelView(self.linear_model_model)
        self.linear_model_controller = LinearModelController(self.linear_model_model, self.linear_model_view)
        self.linear_model_view.setVisible(False)
        main_layout.addWidget(self.linear_model_view)

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

        # Configurar el menú lateral
        self.menu = Menu(self)
        self.menu.hide()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.menu)


    def open_user_guide(self):
        """Muestra la guía de usuario"""
        QMessageBox.information(self, "User Guide", "✨ **Welcome to our application.** ✨\n\n"
            "1- CREATE A NEW MODEL:\nTo create a new model select the option in the top left menu and select "
                "the data that you are going to work with.\n\nThen the preprocess screen will appear, here you must "
                "select the input and outputs columns and apply the preprocess to them.\n\nOnce you finish you can "
                "create the model by pressing the button on the bottom.\n\nFinally, you will see a  graphic of the model, "
                "the most important information about it and a prediction area.\n\nYou can also add a description "
                "to your model and save it by using the buttons Save Description and Save Model.\n\n"
            "2- LOAD A MODEL:\n Just select the file with the model and it will load the same screen as when it was"
                " created but you cant modify it.\n\n"
            "🎉 Enjoy experimenting with data! 🎉", QMessageBox.Ok)

    def toggle_menu_visibility(self):
        """Toggle the visibility of the menu."""
        if self.menu.isVisible():
            self.menu.hide()    
        else:
            self.menu.show()

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
        self.table_view.setVisible(False)
        self.column_selector_view.setVisible(False)
        self.data_preprocessor_view.setVisible(False)
        self.create_model_button.setVisible(False)
        if file_name:
            self.label.setText(f"<b>Selected file:</b> <br><i>{file_name}</i>")
            self.label.setStyleSheet("color: #FFFFFF;")
            # Show the progress bar and make it visible
            self.progress_bar.setValue(0)
            self.progress_bar.setVisible(True)
            # Create a new worker thread for file loading
            self.loader_thread = FileLoaderThread(file_name, self.table_controller, self.table_model)
            # Connect signals to update the progress bar and handle file loading completion
            self.loader_thread.finished_signal.connect(self.on_file_loaded)
            # Start the worker thread
            self.loader_thread.start()
            for i in range(0,101,10):
                self.progress_bar.setValue(i)
                time.sleep(0.5)
        else:
            return

    def on_file_loaded(self, df):
        """Called when the file is successfully loaded."""
        if df is None:
            self.show_empty_file_message()
            self.progress_bar.hide()
            return
        # Hide the progress bar once loading is complete
        self.progress_bar.hide()
        self.linear_model_view.hide()
        self.table_view.show()
        # Enable related views and components
        headers = [self.table_view.horizontalHeaderItem(i).text() for i in range(self.table_view.columnCount())]
        self.column_selector_controller.update_selectors(headers)
        self.column_selector_view.show()
        self.data_preprocessor_view.show()
        self.create_model_button.show()
        # Update models with the loaded DataFrame
        self.linear_model_model.df = self.table_model.df
        self.data_preprocessor_model.df = self.table_model.df

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
                background-color: #555555;}
        """
        self.data_preprocessor_view.empty_cells_button.setStyleSheet(button_style) 

        # Estilos de la ventana y paleta de colores
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        self.setPalette(palette)

    def create_model(self):
        entry_columns, target_column = self.column_selector_view.get_selected_columns()
        if self.linear_model_controller.create_model(entry_columns, target_column):
            self.table_view.setVisible(False)
            self.column_selector_view.setVisible(False)
            self.data_preprocessor_view.setVisible(False)
            self.create_model_button.setVisible(False)
            self.linear_model_view.setVisible(True)

    def load_model(self):
        if self.linear_model_controller.load_model():
            self.table_view.setVisible(False)
            self.column_selector_view.setVisible(False)
            self.data_preprocessor_view.setVisible(False)
            self.create_model_button.setVisible(False)
            self.linear_model_view.setVisible(True)

    def apply_preprocess(self):
        entry_columns, target_column = self.column_selector_controller.get_selected_columns()
        if self.data_preprocessor_controller.apply_preprocessing(entry_columns, target_column):
            self.table_controller.update_table(self.data_preprocessor_model.df)

    def highlight_empty_cells(self):
        entry_columns, target_column = self.column_selector_controller.get_selected_columns()
        if not entry_columns and not target_column:
            self.data_preprocessor_view.show_message("Warning", "Please select columns first.", "warning")
            return False
        column_indices, missing_cells = self.data_preprocessor_controller.highlight_empty_cells(entry_columns, target_column)

        for i in range(self.table_view.rowCount()):
            for j in column_indices:
                item = self.table_view.item(i, j)
                if item and (item.text() == "" or item.text().lower() == "nan"):
                    item.setBackground(QColor(255, 0, 0, 150))  # Rojo transparente para destacar

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Interface()
    window.show()
    sys.exit(app.exec_())