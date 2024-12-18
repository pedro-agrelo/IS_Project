import pandas as pd
from PyQt5.QtWidgets import (QPushButton, QLabel, QComboBox, QLineEdit,
                             QVBoxLayout, QWidget, QMessageBox, QGroupBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor



class DataPreprocessorModel:
    def __init__(self):
        self.df = pd.DataFrame()

    def set_dataframe(self, df):
        self.df = df

    def get_dataframe(self):
        return self.df

    def preprocess_missing_data(self, columns, strategy, constant_value=None):
        if strategy == "Remove Rows":
            self.df.dropna(subset=columns, inplace=True)
        elif strategy == "Fill with Mean":
            for column in columns:
                if self.df[column].dtype in ['float64', 'int64']:
                    self.df[column].fillna(self.df[column].mean(), inplace=True)
        elif strategy == "Fill with Median":
            for column in columns:
                if self.df[column].dtype in ['float64', 'int64']:
                    self.df[column].fillna(self.df[column].median(), inplace=True)
        elif strategy == "Fill with Constant Value" and constant_value is not None:
            try:
                constant_value = float(constant_value)
            except ValueError:
                return False
            self.df[columns] = self.df[columns].fillna(constant_value)
        
        return True

    def get_missing_cells(self, columns):
        return self.df[columns].isna()

class DataPreprocessorView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Crea la interfaz gráfica para el preprocesador de datos."""
        # Layout principal
        main_layout = QVBoxLayout()

        # GroupBox para opciones de preprocesamiento
        self.group_box = QGroupBox("Handle Missing Data")
        self.group_box.setStyleSheet("QGroupBox { font-weight: bold; color: #99FFFF; }")
        group_layout = QVBoxLayout()

        # Estrategia de manejo de NaN
        self.strategy_label = QLabel("Select strategy for missing data:")
        self.strategy_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.strategy_label.setStyleSheet("color: #FFFFFF;")
        group_layout.addWidget(self.strategy_label)

        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems(["Remove Rows", "Fill with Mean", "Fill with Median", "Fill with Constant Value"])
        group_layout.addWidget(self.strategy_combo)

        # Campo para valor constante
        self.constant_label = QLabel("Enter constant value:")
        self.constant_label.setFont(QFont("Arial", 12))
        self.constant_label.setStyleSheet("color: white;")
        self.constant_label.setVisible(False)
        group_layout.addWidget(self.constant_label)

        self.constant_input = QLineEdit()
        self.constant_input.setPlaceholderText("Enter value...")
        self.constant_input.setVisible(False)
        group_layout.addWidget(self.constant_input)

        # Botón para aplicar preprocesado
        self.apply_button = QPushButton("Apply")
        self.apply_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.apply_button.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border-radius: 10px;
                border: 2px solid #FFFFFF;
                font-size: 16px;  /* Aumentar el tamaño de la letra */
            }
            QPushButton:hover {
                background-color: #555555;}
        """)
        group_layout.addWidget(self.apply_button)

        # Configuración del GroupBox
        self.group_box.setLayout(group_layout)
        self.group_box.setFixedHeight(200)  # Ajustar el ancho del selector de columnas
        main_layout.addWidget(self.group_box)

        # Botón para resaltar celdas vacías
        self.empty_cells_button = QPushButton("Show Empty Cells")
        self.empty_cells_button.setFont(QFont("Arial", 16, QFont.Bold))
        self.empty_cells_button.setFixedSize(300, 50)
        main_layout.addWidget(self.empty_cells_button, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def show_message(self, title, message, msg_type):
        """Muestra un mensaje emergente."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning if msg_type == "warning" else QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()


class DataPreprocessorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Conectar señales de la vista
        self.view.strategy_combo.currentIndexChanged.connect(self.toggle_constant_input)

    def toggle_constant_input(self):
        """Muestra/oculta la entrada de valor constante."""
        if self.view.strategy_combo.currentText() == "Fill with Constant Value":
            self.view.constant_label.setVisible(True)
            self.view.constant_input.setVisible(True)
        else:
            self.view.constant_label.setVisible(False)
            self.view.constant_input.setVisible(False)

    def apply_preprocessing(self, entry_columns, target_column):
        """Aplica el preprocesado según la estrategia seleccionada."""
        strategy = self.view.strategy_combo.currentText()
        constant_value = self.view.constant_input.text() if self.view.constant_input.isVisible() else None
        
        if not entry_columns or not target_column:
            self.view.show_message("Error", "Select entry and target columns.", "warning")
            return False

        # Procesar columnas seleccionadas
        columns_to_process = entry_columns + ([target_column] if target_column not in entry_columns else [])
        if self.model.preprocess_missing_data(columns_to_process, strategy, constant_value):
            self.view.show_message("Success", "Changes applied.", "info")
            return True
        else:
            self.view.show_message("Warning", "No numeric value", "warning")
            return False

        
    def highlight_empty_cells(self, entry_columns, target_column):
        """Resalta las celdas vacías en las columnas seleccionadas."""
        selected_columns = entry_columns + [target_column]

        if not selected_columns:
            self.view.show_message("Warning", "Please select columns first.", "warning")
            return

        missing_cells = self.model.get_missing_cells(selected_columns)
        column_indices = [self.model.df.columns.get_loc(col) for col in selected_columns]

        return column_indices, missing_cells

