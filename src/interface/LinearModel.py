from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QMessageBox, QGroupBox, QPushButton
from PyQt5.QtGui import QFont
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class LinearModel(QWidget):
    def __init__(self, table_widget, column_selector, parent=None):
        """
        Clase encargada de crear un modelo de regresión lineal.
        :param table_widget: Widget de tabla con los datos cargados (DataTable).
        :param column_selector: Selector de columnas de entrada y objetivo.
        :param parent: Widget padre.
        """
        super().__init__(parent)
        self.table_widget = table_widget
        self.column_selector = column_selector
        self.model = None
        self.init_ui()

    def init_ui(self):
        """Configura la interfaz gráfica para el modelo lineal."""
        layout = QVBoxLayout()
        
        # Widget para incrustar el gráfico
        self.plot_widget = QWidget(self)
        plot_layout = QVBoxLayout(self.plot_widget)  # Layout para la sección del gráfico
        self.plot_widget.setLayout(plot_layout)
        layout.addWidget(self.plot_widget)

        # Crear un QGroupBox para la fórmula y las métricas de error
        self.info_group_box = QGroupBox("Model Information")
        self.info_group_box.setFont(QFont("Arial", 12, QFont.Bold))
        self.info_group_box.setStyleSheet("QGroupBox { font-weight: bold; color: #99FFFF; }")  # Celeste
        
        # Layout para el QGroupBox de información del modelo
        info_layout = QVBoxLayout()
        
        # Etiqueta para mostrar la fórmula de la regresión
        self.formula_label = QLabel("Linear Regression Formula will appear here.")
        self.formula_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.formula_label.setStyleSheet("color: white;")  # Texto en blanco
        info_layout.addWidget(self.formula_label)

        # Etiqueta para mostrar las métricas de error
        self.error_label = QLabel("Error Metrics will appear here.")
        self.error_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.error_label.setStyleSheet("color: white;")  # Texto en blanco
        info_layout.addWidget(self.error_label)

        self.info_group_box.setLayout(info_layout)
        layout.addWidget(self.info_group_box)

        # Etiqueta para mostrar la información del modelo en un recuadro con letras blancas
        self.saved_description_label = QLabel("Model Description:")
        self.saved_description_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.saved_description_label.setStyleSheet("""
            background-color: #2E2E2E;
            color: white;
            padding: 8px;
            border: 1px solid #FFFFFF;
            border-radius: 5px;
        """)
        self.saved_description_label.setWordWrap(True)  # Permitir salto de línea en el texto
        layout.addWidget(self.saved_description_label)

        # Caja de texto para la descripción del modelo
        self.description_text = QTextEdit(self)
        self.description_text.setPlaceholderText("Enter model description here...")
        layout.addWidget(self.description_text)

        # Botón para guardar la descripción del modelo
        self.save_description_button = QPushButton("Save Description")
        self.save_description_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.save_description_button.clicked.connect(self.save_description)
        layout.addWidget(self.save_description_button)

        self.setLayout(layout)

    def create_model(self):
        """Crea el modelo de regresión lineal con las columnas seleccionadas y muestra los resultados."""
        self.description_text.clear()
        self.saved_description_label.clear()
        # Obtener las columnas seleccionadas
        entry_columns, target_column = self.column_selector.get_selected_columns()
        
        if not entry_columns or not target_column:
            QMessageBox.warning(self, "Warning", "Please select entry and target columns.")
            return

        df = self.table_widget.df
        X = df[entry_columns].values
        y = df[target_column].values

        # Crear y entrenar el modelo de regresión lineal
        self.model = LinearRegression()
        self.model.fit(X, y)

        # Generar la fórmula de regresión
        formula = f"{target_column} = " + " + ".join(
            [f"{coef:.3f}*{col}" for coef, col in zip(self.model.coef_, entry_columns)]
        ) + f" + {self.model.intercept_:.3f}"

        self.formula_label.setText("Linear Regression Formula: " + formula)

        # Calcular y mostrar métricas de error
        y_pred = self.model.predict(X)
        mae = mean_absolute_error(y, y_pred)
        rmse = np.sqrt(mean_squared_error(y, y_pred))
        self.error_label.setText(f"MAE: {mae:.3f}\nRMSE: {rmse:.3f}")
        
        self.plot_regression()
        return True
    
    def plot_regression(self):
        entry_columns, target_column = self.column_selector.get_selected_columns()
        if not entry_columns or len(entry_columns) != 1:
            # Agregar el nuevo gráfico
            self.plot_widget.layout().removeWidget(self.canvas)
            self.canvas = FigureCanvas()
            self.plot_widget.layout().addWidget(self.canvas)
            self.canvas.draw()  # Dibuja el gráfico
            QMessageBox.warning(self, "Warning", "Please select exactly one entry column for plotting.")
            return

        X = self.table_widget.df[entry_columns].values
        y = self.table_widget.df[target_column].values
        y_pred = self.model.predict(X)

        # Configura la gráfica
        fig, ax = plt.subplots()
        ax.scatter(X, y, color='blue', label="Actual Data")
        ax.plot(X, y_pred, color='red', label="Regression Line")
        ax.set_xlabel(entry_columns[0])
        ax.set_ylabel(target_column)
        ax.legend()

        # Limpia el gráfico previo en el layout
        for i in reversed(range(self.plot_widget.layout().count())):
            widget_to_remove = self.plot_widget.layout().itemAt(i).widget()
            widget_to_remove.setParent(None)
        
        # Agregar el nuevo gráfico
        self.canvas = FigureCanvas(fig)
        self.plot_widget.layout().addWidget(self.canvas)
        self.canvas.draw()  # Dibuja el gráfico

    def save_description(self):
        """Guarda y muestra la descripción ingresada por el usuario."""
        description = self.description_text.toPlainText().strip()
        if not description:
            QMessageBox.warning(self, "Warning", "Please enter a description before saving.")
            return

        # Mostrar la información del modelo en el recuadro
        self.saved_description_label.setText(f"Model Description:\n{description}")
