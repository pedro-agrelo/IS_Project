from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QMessageBox, QGroupBox, QPushButton, QFileDialog, QLineEdit, QFormLayout
from PyQt5.QtGui import QFont
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import joblib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

class LinearModelModel():
    def __init__(self, df):
        self.df = df
        self.entry_columns = None
        self.target_column = None
        self.model = None
        self.description = ""
        self.formula = ""
        self.errors = ""

    def create_model(self, entry_columns, target_column):
        """Crea el modelo de regresión lineal con las columnas seleccionadas y muestra los resultados."""
        self.entry_columns = entry_columns
        self.target_column = target_column
        if not self.entry_columns or not self.target_column:
            return False
        
        if self.df[self.entry_columns].isnull().any().any() or self.df[self.target_column].isnull().any():
            return False

        # Verificar que todas las columnas de entrada sean numéricas
        for column in self.entry_columns:
            if not pd.api.types.is_numeric_dtype(self.df[column]):
                return False
        
        # Verificar que la columna objetivo sea numérica
        if not pd.api.types.is_numeric_dtype(self.df[self.target_column]):
            return False
        X = self.df[self.entry_columns].values
        y = self.df[self.target_column].values

        # Dividir los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Crear y entrenar el modelo de regresión lineal
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)

        # Generar la fórmula de regresión
        self.formula = f"{self.target_column} = " + " + ".join(
            [f"{coef:.3f}*{col}" for coef, col in zip(self.model.coef_, self.entry_columns)]
        ) + f" + {self.model.intercept_:.3f}"

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
        self.description = ""
        self.errors = str(f"Training MAE: {mae_train:.3f}, RMSE: {rmse_train:.3f}, R²: {r2_train:.3f}\n" + f"Test MAE: {mae_test:.3f}, RMSE: {rmse_test:.3f}, R²: {r2_test:.3f}")
        return True
    
    def plot_regression(self):
            # Usa las columnas seleccionadas si no se especifican
            if not self.entry_columns or len(self.entry_columns) != 1:
                return False

            X = self.df[self.entry_columns].values
            y = self.df[self.target_column].values
            y_pred = self.model.predict(X)
            # Configura la gráfica
            fig, ax = plt.subplots()
            ax.scatter(X, y, color='blue', label="Actual Data")
            ax.plot(X, y_pred, color='red', label="Regression Line")
            ax.set_xlabel(self.entry_columns[0])
            ax.set_ylabel(self.target_column)
            ax.legend()
            return fig
    
    def save_model(self, file_path):
        """Abre un diálogo para guardar el modelo y los datos asociados en el archivo seleccionado por el usuario."""
        # Empaqueta los datos del modelo para guardar
        model_data = {"model": self.model,"input_columns": self.entry_columns,"output_column": self.target_column,
                      "errors":  self.errors, "description": self.description, "formula": self.formula, "df":self.df}

        # Intenta guardar el archivo y maneja errores
        joblib.dump(model_data, file_path)
    
    def load_model(self, file_name):
        """Carga el modelo .joblib y muestra los datos correspondientes"""
        if file_name:
            model_data = joblib.load(file_name)
            self.model = model_data["model"]
            self.df = model_data["df"]
            self.entry_columns = model_data["input_columns"]
            self.target_column = model_data["output_column"]
            self.formula = model_data["formula"]
            self.errors = model_data["errors"]
            self.description = model_data["description"]
            return True
        else:
            return False
        
class LinearModelView(QWidget):
    def __init__(self, model, parent=None):
        """
        Clase encargada de crear un modelo de regresión lineal.
        """
        super().__init__(parent)
        self.model = model

        layout = QVBoxLayout()
        
        # Widget para añadir el gráfico
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

        # Crear la sección para realizar predicciones
        self.prediction_group_box = QGroupBox("Prediction")
        self.prediction_group_box.setFont(QFont("Arial", 12, QFont.Bold))
        self.prediction_group_box.setStyleSheet("QGroupBox { font-weight: bold; color: #99FFFF; }")
        self.prediction_layout = QFormLayout()
        self.input_fields = {}

        # Campo para mostrar la predicción
        self.prediction_label = QLabel("Prediction: Prediction result will appear here.")
        self.prediction_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.prediction_label.setStyleSheet("color: white;")  # Texto en blanco
        self.prediction_layout.addRow(self.prediction_label)

        self.prediction_button = QPushButton("Predict")
        self.prediction_layout.addRow(self.prediction_button)

        self.prediction_group_box.setLayout(self.prediction_layout)
        layout.addWidget(self.prediction_group_box)

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
        layout.addWidget(self.save_description_button)

        # Botón para guardar la descripción del modelo
        self.save_model_button = QPushButton("Save Model")
        self.save_model_button.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(self.save_model_button)

        self.setLayout(layout)

    def set_formula(self, formula):
        """Muestra la fórmula del modelo en la vista."""
        self.formula_label.setText(f"Linear Regression Formula: {formula}")

    def set_errors(self, errors):
        """Muestra las métricas de error en la vista."""
        self.error_label.setText(errors)

    def set_description(self, description):
        """Muestra la descripción ingresada por el usuario."""
        self.saved_description_label.setText(f"Model Description:\n{description}")

    def set_prediction(self, prediction):
        """Muestra la descripción ingresada por el usuario."""
        self.prediction_label.setText(f"Prediction: {prediction}")

class LinearModelController():
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Conectar botones con acciones
        self.view.save_description_button.clicked.connect(self.save_description)
        self.view.save_model_button.clicked.connect(self.save_model)
        self.view.prediction_button.clicked.connect(self.make_prediction)

    def create_model(self, entry_columns, target_column):
        if self.model.create_model(entry_columns, target_column):
            self.view.description_text.clear()
            for i in reversed(range(self.view.plot_widget.layout().count())):
                    widget_to_remove = self.view.plot_widget.layout().itemAt(i).widget()
                    widget_to_remove.setParent(None)

            if len(entry_columns) == 1:
                fig = self.model.plot_regression()
                self.view.plot_widget.layout().addWidget(FigureCanvas(fig))

            self.view.set_formula(self.model.formula)
            self.view.set_errors(self.model.errors)
            self.view.set_description(self.model.description)

            self.allow_inputs_prediction()

            self.view.description_text.setVisible(True)
            self.view.save_description_button.setVisible(True)
            self.view.save_model_button.setVisible(True)
            return True
        else:
            self.show_message("Error", f"No columns given or columns with no numeric or empty values", "error")


    def save_description(self):
        """Guardar la descripción proporcionada por el usuario"""
        description = self.view.description_text.toPlainText().strip()
        self.model.description = description
        self.view.set_description(description)

    def save_model(self):
        """Guardar el modelo entrenado en un archivo"""
        file_path, _ = QFileDialog.getSaveFileName(self.view, "Save Model", "", "Model Files (*.joblib)")
        if file_path:
            try:
                self.model.save_model(file_path)
                self.show_message("Success", "Model saved successfully!", "success")
            except Exception as e:
                self.show_message("Error", f"Failed to save model: {str(e)}", "error")

    def load_model(self):
        """Cargar el modelo desde un archivo .joblib"""
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Load Model", "", "Model Files (*.joblib)")
        if file_path:
            try:
                self.model.load_model(file_path)
                self.view.set_formula(self.model.formula)
                self.view.set_errors(self.model.errors)
                self.view.set_description(self.model.description)

                for i in reversed(range(self.view.plot_widget.layout().count())):
                    widget_to_remove = self.view.plot_widget.layout().itemAt(i).widget()
                    widget_to_remove.setParent(None)
                if len(self.model.entry_columns) == 1:
                    fig = self.model.plot_regression()
                    self.view.plot_widget.layout().addWidget(FigureCanvas(fig))

                self.allow_inputs_prediction()

                self.view.set_prediction("Prediction: Prediction result will appear here.")

                self.view.description_text.setVisible(False)
                self.view.save_description_button.setVisible(False)
                self.view.save_model_button.setVisible(False)

                self.show_message("Success", "Model loaded successfully!", "success")
                return True
            except Exception as e:
                self.show_message("Error", f"Failed to load model: {str(e)}", "error")
                return False

    def make_prediction(self):
        """Realizar la predicción utilizando los valores ingresados"""
        # Obtener los valores de las columnas de entrada
        input_values = []
        try:
            for col in self.model.entry_columns:
                value = float(self.view.input_fields[col].text())  # Convertir a float
                input_values.append(value)
            # Realizar la predicción
            prediction = self.model.model.predict([input_values])[0]  # La predicción es un valor único

            # Mostrar la predicción
            self.view.set_prediction(prediction)
            
        except Exception:
            self.show_message("Error", f"Introduce the values needed to predict", "error")

    def allow_inputs_prediction(self):
        # Iterar sobre el layout y eliminar todas las filas, excepto las dos primeras
        for i in range(self.view.prediction_layout.count() - 1, 1, -1):  # Comienza desde la última fila hasta la tercera fila
            item = self.view.prediction_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()  # Eliminar el widget

        # Crear campos de entrada para las columnas de entrada
        self.view.input_fields = {}
        if self.model.entry_columns:
            for col in self.model.entry_columns:
                input_field = QLineEdit()
                input_field.setPlaceholderText(f"Enter value for {col}")
                label = QLabel(f"{col}:")
                label.setStyleSheet("color: white;")  # Establecer el color blanco para el texto
                self.view.prediction_layout.addRow(label, input_field)
                self.view.input_fields[col] = input_field

    def show_message(self, title, message, msg_type):
        """Mostrar mensaje en la vista"""
        msg_box = QMessageBox(self.view)
        if msg_type == "success":
            msg_box.setIcon(QMessageBox.Information)
        elif msg_type == "error":
            msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()