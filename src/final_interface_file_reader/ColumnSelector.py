
from PyQt5.QtWidgets import (QGroupBox, QListWidget, QLabel,QVBoxLayout, QHBoxLayout, QWidget,QAbstractItemView)
from PyQt5.QtGui import QFont

class ColumnSelector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVisible(False)
        self.layout = QHBoxLayout(self)

        # Crear un grupo para los selectores de columnas de entrada
        self.entry_group = QGroupBox("Entry Columns")
        self.entry_group.setStyleSheet("QGroupBox { font-weight: bold; color: #99FFFF; }")  # Cambiar color y peso de la fuente
        self.entry_group.setMaximumWidth(400)  # Limitar el ancho del selector a 400px
        self.entry_layout = QVBoxLayout(self.entry_group)
        

        self.list_widget_entry = QListWidget(self)
        self.list_widget_entry.setSelectionMode(QAbstractItemView.MultiSelection)
        self.list_widget_entry.setMaximumWidth(400)  # Limitar el ancho del selector a 400px
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
        self.entry_layout.addWidget(self.list_widget_entry)
        
        # Añadir el grupo al layout principal
        self.layout.addWidget(self.entry_group)

        # Crear un grupo para el selector de columna objetivo
        self.target_group = QGroupBox("Target Column")
        self.target_group.setStyleSheet("QGroupBox { font-weight: bold; color: #99FFFF; }")  # Cambiar color y peso de la fuente
        self.target_group.setMaximumWidth(400)  # Limitar el ancho del selector a 400px
        self.target_layout = QVBoxLayout(self.target_group)
        self.list_widget_target = QListWidget(self)
        self.list_widget_target.setMaximumWidth(400)  # Limitar el ancho del selector a 400px
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

        self.target_layout.addWidget(self.create_label("Select Target Column:"))
        self.target_layout.addWidget(self.list_widget_target)

        # Añadir el grupo al layout principal
        self.layout.addWidget(self.target_group)
    
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
        """Devuelve las columnas seleccionadas"""
        input_column = self.list_widget_entry.currentItem().text() if self.list_widget_entry.currentItem() else None
        target_column = self.list_widget_target.currentItem().text() if self.list_widget_target.currentItem() else None
        return input_column, target_column