from PyQt5.QtWidgets import (QGroupBox, QListWidget, QLabel,QVBoxLayout, QHBoxLayout,
                              QWidget,QAbstractItemView, QMessageBox, QPushButton,QRadioButton)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class ColumnSelector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVisible(False)
        self.selectors_layout = QHBoxLayout()
        self.layout = QVBoxLayout(self)

        # Crear un grupo para los selectores de columnas de entrada
        self.entry_group = QGroupBox("Entry Columns")
        self.entry_group.setStyleSheet("QGroupBox { font-weight: bold; color: #99FFFF; }")  # Cambiar color y peso de la fuente
        self.entry_group.setMaximumWidth(400)  # Limitar el ancho del selector a 400px
        self.entry_group.setMaximumHeight(200)  # Limitar el ancho del selector a 400px
        self.entry_layout = QVBoxLayout(self.entry_group)

        # Agregar botones de radio para seleccionar modo
        self.single_selection_radio = QRadioButton("Single Selection")
        self.single_selection_radio.setChecked(True)  # Por defecto selecciona simple
        self.single_selection_radio.toggled.connect(self.update_selection_mode)
        self.multiple_selection_radio = QRadioButton("Multiple Selection")
        self.multiple_selection_radio.toggled.connect(self.update_selection_mode)
        self.single_selection_radio.setStyleSheet("color: white;")
        self.multiple_selection_radio.setStyleSheet("color: white;")
        

        self.list_widget_entry = QListWidget(self)
        self.list_widget_entry.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list_widget_entry.setMaximumWidth(400)  # Limitar el ancho del selector a 400px
        self.list_widget_entry.setMaximumHeight(200)  # Limitar el ancho del selector a 400px
        self.list_widget_entry.setStyleSheet("""
        QGroupBox {
            font-weight: bold;
            color: #99FFFF;
        }
        QListWidget {
            background-color: #2E2E2E;  /* Fondo gris oscuro */
            color: white;  /* Texto blanco */
        }
    """)
        self.entry_layout.addWidget(self.create_label("Select Entry Columns:"))
        self.entry_layout.addWidget(self.single_selection_radio)
        self.entry_layout.addWidget(self.multiple_selection_radio)
        self.entry_layout.addWidget(self.list_widget_entry)

        
        # Añadir el grupo al layout principal
        self.selectors_layout.addWidget(self.entry_group)

        # Crear un grupo para el selector de columna objetivo
        self.target_group = QGroupBox("Target Column")
        self.target_group.setStyleSheet("QGroupBox { font-weight: bold; color: #99FFFF; }")  # Cambiar color y peso de la fuente
        self.target_group.setMaximumWidth(400)  # Limitar el ancho del selector a 400px
        self.target_group.setMaximumHeight(200)  # Limitar el ancho del selector a 400px
        self.target_layout = QVBoxLayout(self.target_group)
        self.list_widget_target = QListWidget(self)
        self.list_widget_target.setMaximumWidth(400)  # Limitar el ancho del selector a 400px
        self.list_widget_target.setMaximumHeight(200)  # Limitar el ancho del selector a 400px
        self.list_widget_target.setStyleSheet("""
    QGroupBox {
        font-weight: bold;
        color: #99FFFF;
    }
    QListWidget {
        background-color: #2E2E2E;  /* Fondo gris oscuro */
        color: white;  /* Texto blanco */
    }
""")

        # Añadir el grupo al layout principal
        self.selectors_layout.addWidget(self.target_group)
        self.target_layout.addWidget(self.create_label("Select Target Column:"))
        self.target_layout.addWidget(self.list_widget_target)

        # Botón para confirmar selección (No visible al principio)
        self.confirm_button = QPushButton('Confirm columns selection')
        self.confirm_button.setFixedSize(300, 50)
        self.confirm_button.setVisible(False)  # Ocultar el botón al inicio
        self.confirm_button.setFont(QFont("Arial", 16, QFont.Bold))  # Aumentar tamaño de letra
        self.confirm_button.clicked.connect(self.confirm_selection)
        self.confirm_button.setStyleSheet("""
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
        
        self.layout.addLayout(self.selectors_layout)
        self.layout.addWidget(self.confirm_button, alignment=Qt.AlignCenter)

    def update_selection_mode(self):
        """Actualiza el modo de selección de columnas según el botón de radio seleccionado."""
        if self.single_selection_radio.isChecked():
            self.list_widget_entry.setSelectionMode(QAbstractItemView.SingleSelection)
  # Solo un elemento seleccionado
        else:
            self.list_widget_entry.setSelectionMode(QAbstractItemView.MultiSelection)
   # Permitir múltiples selecciones

    def create_label(self, text):
        """Crea una etiqueta con estilos personalizados"""
        label = QLabel(text)
        label.setFont(QFont("Arial", 10, QFont.Bold))  # Cambiar tipo y tamaño de fuente
        label.setStyleSheet("color: #FFFFFF;")  # Cambiar color a un amarillo claro
        return label

    def update_selectors(self, columns):
        """Actualiza los selectores con las columnas disponibles"""
        self.list_widget_entry.clear()
        self.list_widget_entry.addItems(columns)
        self.list_widget_target.clear()
        self.list_widget_target.addItems(columns)

    def get_selected_columns(self):
        """Devuelve las columnas de entrada (features) seleccionadas y la columna de salida (target)"""
        # Obtener todas las columnas seleccionadas para las entradas (selección múltiple)
        input_columns = [item.text() for item in self.list_widget_entry.selectedItems()]
        
        # Obtener la columna de salida (solo una)
        target_column = self.list_widget_target.currentItem().text() if self.list_widget_target.currentItem() else None
        
        return input_columns, target_column
    
    def confirm_selection(self):
        """Confirma la selección de columnas de entrada y salida"""
        entradas, salida = self.get_selected_columns()

        if not entradas or not salida:
            self.show_message("Error", "Debe seleccionar al menos una columna de entrada y una columna objetivo.", "warning")
        else:
            self.show_message("Success", f"Selected columns:\nEnter: {entradas}\nObjetive: {salida}", "success")

    def show_message(self, titulo, mensaje, tipo):
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