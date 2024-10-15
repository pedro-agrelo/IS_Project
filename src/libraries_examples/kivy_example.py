from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class MyLayout(GridLayout):
    def __init__(self,**kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.rows = 3
        # Cuadro de texto donde el usuario puede ingresar información
        self.text_input = TextInput(hint_text="Ingresa algo aquí", multiline=False)
        self.label = Label(text="Escribe algo y presiona el botón")
        # Añadir los widgets al layout
        self.add_widget(self.label)
        self.add_widget(self.text_input)
        self.add_widget(Button(text="Mostrar mensaje", on_press=self.show_message))

    def show_message(self, instance):
        # Toma el texto del cuadro de texto y lo muestra en la etiqueta
        user_text = self.text_input.text
        if user_text:
            self.label.text = f"Has ingresado: {user_text}"
        else:
            self.label.text = "El cuadro de texto está vacío"

class MyApp(App):
    def build(self):
        return MyLayout()

# Iniciar la aplicación
if __name__ == "__main__":
    MyApp().run()