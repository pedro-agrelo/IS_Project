import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal

class FileLoaderThread(QThread):
    # Señal para comunicar la finalización y pasar el DataFrame cargado
    finished_signal = pyqtSignal(object)  # Se usará 'object' para permitir cualquier tipo de dato (como un DataFrame)
    
    def __init__(self, file_name, table_controller, table_model):
        super().__init__()
        self.file_name = file_name
        self.table_controller = table_controller
        self.table_model = table_model

    def run(self):
        """Este método corre en el hilo en segundo plano"""
        try:
            # Cargar el archivo en el modelo
            file_loaded = self.table_controller.load_file(self.file_name)
            
            if file_loaded:
                # Emitir el DataFrame cargado a la interfaz principal
                self.finished_signal.emit(self.table_model.df)
            else:
                # Si el archivo no se carga correctamente, emitir un valor de error
                self.finished_signal.emit(None)
                
        except Exception as e:
            # Manejo de excepciones: si ocurre un error, emitir un valor nulo o mensaje de error
            print(f"Error durante la carga del archivo: {e}")
            self.finished_signal.emit(None)  # Emitir None para indicar que hubo un error

