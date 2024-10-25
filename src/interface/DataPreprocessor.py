from PyQt5.QtWidgets import (QPushButton, QLabel, QComboBox, QLineEdit,
                             QVBoxLayout, QWidget, QMessageBox, QGroupBox)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class DataPreprocessor(QWidget):
    def __init__(self, table_widget, column_selector, parent=None):
        """
        Clase encargada del preprocesamiento de datos.
        :param table_widget: Widget de tabla con los datos cargados (DataTable).
        :param column_selector: Selector de columnas de entrada y objetivo.
        :param parent: Widget padre.
        """
        super().__init__(parent)
        self.table_widget = table_widget
        self.column_selector = column_selector
        self.init_ui()

    def init_ui(self):
        """Configura la interfaz gráfica para el preprocesamiento."""
        
        # Crear el layout principal del widget
        main_layout = QVBoxLayout()
        
        # Crear un QGroupBox para enmarcar las opciones de preprocesamiento
        self.group_box = QGroupBox("Handle Missing Data")
        self.group_box.setFont(QFont("Arial", 10, QFont.Bold))
        self.group_box.setMaximumHeight(200)  # Limitar el ancho del selector a 400px
        self.group_box.setStyleSheet("QGroupBox { font-weight: bold; color: #99FFFF; }")

        # Layout para el QGroupBox
        group_layout = QVBoxLayout()

        # Selección de la estrategia de manejo de NaN
        self.strategy_label = QLabel("Select strategy for missing data:")
        self.strategy_label.setFont(QFont("Arial", 10, QFont.Bold))  # Cambiar tipo y tamaño de fuente
        self.strategy_label.setStyleSheet("color: #FFFFFF;")  # Cambiar color a un amarillo claro
        group_layout.addWidget(self.strategy_label)

        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems(["Remove Rows", "Fill with Mean", "Fill with Median", "Fill with Constant Value"])
        group_layout.addWidget(self.strategy_combo)

        # Campo para el valor constante
        self.constant_label = QLabel("Enter constant value:")
        self.constant_label.setFont(QFont("Arial", 12))
        self.constant_label.setStyleSheet("color: white;")
        self.constant_label.setVisible(False)
        group_layout.addWidget(self.constant_label)

        self.constant_input = QLineEdit()
        self.constant_input.setPlaceholderText("Enter value...")
        self.constant_input.setVisible(False)
        group_layout.addWidget(self.constant_input)

        # Conectar la estrategia al comportamiento del campo constante
        self.strategy_combo.currentIndexChanged.connect(self.toggle_constant_input)

        # Botón para aplicar el preprocesado
        self.apply_button = QPushButton("Apply")
        self.apply_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.apply_button.clicked.connect(self.apply_preprocessing)
        self.apply_button.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border-radius: 10px;
                border: 2px solid #FFFFFF;
                font-size: 16px;  /* Aumentar el tamaño de la letra */
            }
            QPushButton:hover {
                background-color: #555555;
            }""")
        group_layout.addWidget(self.apply_button)

        # Asignar el layout al QGroupBox
        self.group_box.setLayout(group_layout)

        # Botón para mostrar valores vacíos
        self.empty_cells_button = QPushButton("Show Empty Cells")
        self.empty_cells_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.empty_cells_button.setFixedWidth(300)
        self.empty_cells_button.clicked.connect(self.highlight_empty_cells)
        self.empty_cells_button.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border-radius: 10px;
                border: 2px solid #FFFFFF;
                font-size: 16px;  /* Aumentar el tamaño de la letra */
            }
            QPushButton:hover {
                background-color: #555555;
            }""")
        
        # Añadir el QGroupBox al layout principal
        main_layout.addWidget(self.group_box)
        main_layout.addWidget(self.empty_cells_button, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def toggle_constant_input(self, index):
        """Muestra u oculta el campo de entrada de valor constante según la estrategia seleccionada."""
        if self.strategy_combo.currentText() == "Fill with Constant Value":
            self.constant_label.setVisible(True)
            self.constant_input.setVisible(True)
        else:
            self.constant_label.setVisible(False)
            self.constant_input.setVisible(False)

    def apply_preprocessing(self):
        """Aplica el preprocesado según la estrategia seleccionada por el usuario."""
        strategy = self.strategy_combo.currentText()
        df = self.table_widget.df

        # Aplicar preprocesado solo a las columnas seleccionadas (entrada + objetivo)
        entry_columns, target_column = self.column_selector.get_selected_columns()
        if entry_columns == [] or target_column is None:
            self.show_message("Error", "Missing entry and/or objective columns.", "warning")
            return
        if target_column not in entry_columns:
            columns_to_process = entry_columns + [target_column]

        else:
            columns_to_process = entry_columns

        if strategy == "Remove Rows":
            df.dropna(subset=columns_to_process, inplace=True)
            self.show_message("Success", "Rows with missing values in selected columns have been removed.", "info")

        elif strategy == "Fill with Mean":
            for column in columns_to_process:
                if df[column].dtype in ['float64', 'int64']:
                    df[column].fillna(df[column].mean(), inplace=True)
            self.show_message("Success", "Missing values in selected columns filled with column mean.", "info")

        elif strategy == "Fill with Median":
            for column in columns_to_process:
                if df[column].dtype in ['float64', 'int64']:
                    df[column].fillna(df[column].median(), inplace=True)
            self.show_message("Success", "Missing values in selected columns filled with column median.", "info")

        elif strategy == "Fill with Constant Value":
            constant_value = self.constant_input.text()
            if constant_value == "":
                self.show_message("Error", "Please enter a constant value.", "warning")
                return
            try:
                constant_value = float(constant_value)
            except ValueError:
                pass
            df[columns_to_process] = df[columns_to_process].fillna(constant_value)
            self.show_message("Success", f"Missing values in selected columns filled with constant value: {constant_value}", "info")

        # Actualizar la tabla con los nuevos datos del DataFrame
        self.table_widget.update_table(df)

    def show_message(self, title, message, msg_type):
        """Muestra un mensaje emergente."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning if msg_type == "warning" else QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()
        
    def highlight_empty_cells(self):
        """Resalta las celdas vacías en las columnas seleccionadas."""
        selected_columns = self.column_selector.get_selected_columns()[0]
        if not selected_columns:
            QMessageBox.warning(self, "Warning", "Please select columns first.")
            return

        # Obtener índices de columnas seleccionadas
        column_indices = [self.table_widget.df.columns.get_loc(col) for col in selected_columns]

        # Resaltar celdas vacías en las columnas seleccionadas
        for i in range(self.table_widget.rowCount()):
            for j in column_indices:
                item = self.table_widget.item(i, j)
                if item and (item.text() == "" or item.text().lower() == "nan"):
                    item.setBackground(QColor(255, 0, 0, 150))  # Rojo transparente para destacar
