import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox

# Clase principal de la ventana
class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración básica de la ventana
        self.setWindowTitle('Prueba de Interfaz PyQt')
        self.setGeometry(100, 100, 300, 200)  # x, y, ancho, alto

        # Layout principal
        layout = QVBoxLayout()

        # Etiqueta
        self.label = QLabel('Introduce tu nombre:')
        layout.addWidget(self.label)

        # Cuadro de texto
        self.texto = QLineEdit(self)
        layout.addWidget(self.texto)

        # Botón
        self.boton = QPushButton('Mostrar mensaje', self)
        self.boton.clicked.connect(self.mostrar_mensaje)  # Conectar el botón con la función
        layout.addWidget(self.boton)

        # Setear el layout en la ventana
        self.setLayout(layout)

    # Función para mostrar un mensaje cuando se presiona el botón
    def mostrar_mensaje(self):
        nombre = self.texto.text()  # Obtener el texto del cuadro de texto
        if nombre:
            # Crear un mensaje emergente con el nombre
            QMessageBox.information(self, 'Mensaje', f'¡Hola, {nombre}!')
        else:
            # Crear un mensaje si el cuadro de texto está vacío
            QMessageBox.warning(self, 'Advertencia', 'Por favor, introduce tu nombre.')

# Código principal para ejecutar la aplicación
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Crear una instancia de la ventana principal
    ventana = VentanaPrincipal()
    ventana.show()

    # Ejecutar la aplicación
    sys.exit(app.exec_())