import PySimpleGUI as sg

#tema
sg.theme('DarkTeal9')

#ventana principal
def main():
    #definimos elementos gráficos
    layout = [[sg.Text("What's your name?")],
              [sg.Input(key='-INPUT-')],
              [sg.Text(size=(40,1), key='-OUTPUT-')],
              [sg.Button('OK'), sg.Button('EXIT')]]
    #creamos la ventana con el layout ya definido
    window = sg.Window('Facialix', layout)
    #iniciamos la ejecución de la ventana con un bucle while
    while True:
        #podemos leer los valores y elementos de nuestra ventana
        event, values = window.read()
        # el elemento por defecto para cerrar la ventana es EXIT
        if event == 'EXIT' or event == sg.WINDOW_CLOSED:
            break
        #es posible actualizar valores de los elementos gráficos en tiempo de ejecución
        window['-OUTPUT-'].update('Hello ' + values['-INPUT-'])
    #cerramos la ventana al finalizar
    window.close()

if __name__ == '__main__':
    main()