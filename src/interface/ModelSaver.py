import joblib
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os

class ModelSaver:
    def __init__(self, parent=None):
        self.parent = parent

    def save_model(self, model, input_columns, output_column, mse, r2, description):
        """Abre un diálogo para guardar el modelo y los datos asociados en el archivo seleccionado por el usuario."""
        # Diálogo para seleccionar el archivo de guardado
        file_path, _ = QFileDialog.getSaveFileName(self.parent, "Guardar Modelo", "", "Model Files (*.joblib)")

        # Verifica si se seleccionó un archivo
        if not file_path:
            self.show_message("Cancelado", "No se seleccionó ningún archivo.", "warning")
            return

        # Empaqueta los datos del modelo para guardar
        model_data = {"model": model,"input_columns": input_columns,"output_column": output_column,
                      "mse": mse,"r2": r2,"description": description,
                      "formula": self.get_formula(model, input_columns, output_column),}

        # Intenta guardar el archivo y maneja errores
        try:
            joblib.dump(model_data, file_path)
            self.show_message("Éxito", "Modelo guardado exitosamente.", "success")
            
        except Exception as e:
            self.show_message("Error", f"No se pudo guardar el modelo: {e}", "error")

    def get_formula(self, model, input_columns, output_column):
        """Genera la fórmula del modelo de regresión lineal como una cadena de texto."""
        coef_str = " + ".join(
            f"{coef:.3f} * {col}" for coef, col in zip(model.coef_, input_columns)
        )
        formula = f"{output_column} = {model.intercept_:.3f} + {coef_str}"
        return formula

    
