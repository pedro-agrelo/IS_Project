from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QMessageBox, QGroupBox, QPushButton, QFileDialog
from PyQt5.QtGui import QFont
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import joblib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class LinearModel(QWidget):
    def __init__(self, table_widget, column_selector, parent=None):
        """
        Clase encargada de crear un modelo de regresión lineal.
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

        # Botón para guardar la descripción del modelo
        self.save_model_button = QPushButton("Save Model")
        self.save_model_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.save_model_button.clicked.connect(self.save_model)
        layout.addWidget(self.save_model_button)

        self.setLayout(layout)

    def create_model(self):
        """Crea el modelo de regresión lineal con las columnas seleccionadas y muestra los resultados."""
        self.description_text.clear()
        self.description_text.setVisible(True)
        self.saved_description_label.clear()
        
        entry_columns, target_column = self.column_selector.get_selected_columns()
        if not entry_columns or not target_column:
            QMessageBox.warning(self, "Warning", "Please select entry and target columns.")
            return
        
        if self.table_widget.df[entry_columns].isnull().any().any() or self.table_widget.df[target_column].isnull().any():
            QMessageBox.warning(self, "Warning", "There are missing values in the selected columns.")
            return

        df = self.table_widget.df
        X = df[entry_columns].values
        y = df[target_column].values

        # Dividir los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Crear y entrenar el modelo de regresión lineal
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)

        # Generar la fórmula de regresión
        formula = f"{target_column} = " + " + ".join(
            [f"{coef:.3f}*{col}" for coef, col in zip(self.model.coef_, entry_columns)]
        ) + f" + {self.model.intercept_:.3f}"
        self.formula_label.setText("Linear Regression Formula: " + formula)

        # Calcular y mostrar métricas de error en los datos de prueba
        y_pred_train = self.model.predict(X_train)
        y_pred_test = self.model.predict(X_test)
        
        # Métricas en entrenamiento
        mae_train = mean_absolute_error(y_train, y_pred_train)
        rmse_train = np.sqrt(root_mean_squared_error(y_train, y_pred_train))
        r2_train = r2_score(y_train, y_pred_train)
        
        # Métricas en prueba
        mae_test = mean_absolute_error(y_test, y_pred_test)
        rmse_test = np.sqrt(root_mean_squared_error(y_test, y_pred_test))
        r2_test = r2_score(y_test, y_pred_test)

        # Mostrar métricas en los datos de prueba
        self.error_label.setText(f"Training MAE: {mae_train:.3f}, RMSE: {rmse_train:.3f}, R²: {r2_train:.3f}\n"
                                 f"Test MAE: {mae_test:.3f}, RMSE: {rmse_test:.3f}, R²: {r2_test:.3f}")
        
        self.plot_regression()
        return True
    
    def plot_regression(self, entry_columns=None, target_column=None):
            self.canvas = FigureCanvas()
            self.plot_widget.layout().addWidget(self.canvas)
            # Usa las columnas seleccionadas si no se especifican
            if entry_columns is None or target_column is None:
                entry_columns, target_column = self.column_selector.get_selected_columns()

            if not entry_columns or len(entry_columns) != 1:
                # Agregar el nuevo gráfico
                self.plot_widget.layout().removeWidget(self.canvas)
                self.canvas = FigureCanvas()
                self.plot_widget.layout().addWidget(self.canvas)
                self.canvas.draw()  # Dibuja el gráfico
                QMessageBox.warning(self, "Warning", "Please select exactly one entry column for plotting.")
                return False

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

    def save_model(self):
        """Abre un diálogo para guardar el modelo y los datos asociados en el archivo seleccionado por el usuario."""
        input_columns, output_column = self.column_selector.get_selected_columns()
        description = self.description_text.toPlainText().strip()
        errors = self.error_label.text()

        # Diálogo para seleccionar el archivo de guardado
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Modelo", "", "Model Files (*.joblib)")

        # Verifica si se seleccionó un archivo
        if not file_path:
            self.show_message("Cancelado", "No se seleccionó ningún archivo.", "warning")
            return

        # Empaqueta los datos del modelo para guardar
        model_data = {"model": self.model,"input_columns": input_columns,"output_column": output_column,
                      "errors":  errors, "description": description,
                      "formula": self.get_formula(input_columns, output_column),
                      "df":self.table_widget.df}

        # Intenta guardar el archivo y maneja errores
        try:
            joblib.dump(model_data, file_path)
            self.show_message("Éxito", "Modelo guardado exitosamente.", "success")

        except Exception as e:
            self.show_message("Error", f"No se pudo guardar el modelo: {e}", "error")

    def get_formula(self, input_columns, output_column):
        """Genera la fórmula del modelo de regresión lineal como una cadena de texto."""
        coef_str = " + ".join(f"{coef:.3f} * {col}" for coef, col in zip(self.model.coef_, input_columns))
        formula = f"{output_column} = {self.model.intercept_:.3f} + {coef_str}"
        return formula
    
    def load_model(self):
        """Carga el modelo .joblib y muestra los datos correspondientes"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Model File", "", "Archivos Joblib (*.joblib)", options=options)

        if file_name:
            try:
                model_data = joblib.load(file_name)
                self.show_message("Éxito", f"Modelo cargado correctamente desde: {file_name}", "success")
                self.display_data(model_data)
                return True
            except Exception as e:
                self.show_message("Error", f"Hubo un problema al cargar el modelo: {str(e)}", "error")
                return True  
        else:
            return False

    def display_data(self, data):
        """ Muestra los datos cargados (si es un DataFrame) """
        # Establecer el modelo cargado
        self.model = data["model"]
        # Establecer el df
        self.table_widget.df = data["df"]
        # Mostrar la fórmula
        self.formula_label.setText(f"Linear Regression Formula:\n{data['formula']}")
        # Mostrar métricas de error
        self.error_label.setText(data["errors"])
        # Mostrar la descripción
        self.saved_description_label.setText(f"Model Description:\n{data['description']}")
        # ocultar caja de texto y botones de guardado
        self.description_text.setVisible(False)
        self.save_description_button.setVisible(False)
        self.save_model_button.setVisible(False)

        # Actualizar el gráfico si hay una sola columna de entrada
        if len(data["input_columns"]) == 1:
            self.plot_regression(entry_columns = data["input_columns"], target_column = data["output_column"])
        else:
            self.show_message(self, "Información", 
                                    "El gráfico solo puede generarse si el modelo tiene una única columna de entrada.",
                                    "warning")
   
    def show_message(self, title, message, msg_type):
        """Muestra un mensaje de confirmación o error según el tipo especificado."""
        msg_box = QMessageBox(self)
        if msg_type == "success":
            msg_box.setIcon(QMessageBox.Information)
        elif msg_type == "warning":
            msg_box.setIcon(QMessageBox.Warning)
        elif msg_type == "error":
            msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()