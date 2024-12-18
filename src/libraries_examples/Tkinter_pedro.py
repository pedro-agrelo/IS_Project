#Prueba de la librería Tkinter

import tkinter as tk
from tkinter import messagebox

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Interfaz Personalizada")
ventana.geometry("400x200")  # Tamaño de la ventana
ventana.config(bg="#FFC300")  # Color de fondo de la ventana, formato hexadecimal, o HTML

# Función que se ejecuta al presionar el botón
def mostrar_mensaje():
    texto_ingresado = entrada_texto.get()
    messagebox.showinfo("Mensaje", f"Has ingresado: {texto_ingresado}")

# Crear una etiqueta con formato
etiqueta = tk.Label(
    ventana, 
    text="Ingresa tu texto aquí:", 
    font=("Arial", 14, "bold"), 
    fg="#333333",  # Color del texto
    bg="#FFC300"  # Color de fondo
)
etiqueta.pack(pady=30)  # Espacio vertical entre elementos

# Crear un cuadro de texto para que el usuario ingrese datos, con formato
entrada_texto = tk.Entry(
    ventana, 
    width=30, 
    font=("Arial", 12), 
    fg="#555555",  # Color del texto
    bg="#ffffff",  # Color de fondo
    bd=2, relief="solid"  # Borde y estilo del cuadro de texto
)
entrada_texto.pack(pady=10)

# Crear un botón personalizado
boton1 = tk.Button(
    ventana, 
    text="Mostrar mensaje, Arial", 
    command=mostrar_mensaje, 
    font=("Arial", 12), 
    fg="#ffffff",  # Color del texto del botón
    bg="#007acc",  # Color de fondo del botón
    activebackground="#005f99",  # Color cuando se presiona el botón
    bd=3, relief="raised",  # Estilo del borde del botón
    width=20  # Ancho del botón
)
boton1.pack(pady=10)

boton2 = tk.Button(
    ventana, 
    text="Mostrar mensaje, ComicSans", 
    command=mostrar_mensaje, 
    font=("Comic Sans MS", 12), 
    fg="#ffffff",  # Color del texto del botón
    bg="#007acc",  # Color de fondo del botón
    activebackground="#005f99",  # Color cuando se presiona el botón
    bd=3, relief="raised",  # Estilo del borde del botón
    width=20  # Ancho del botón
)
boton2.pack(pady=10)

boton3 = tk.Button(
    ventana, 
    text="Mostrar mensaje, Times New Roman", 
    command=mostrar_mensaje, 
    font=("Times New Roman", 12), 
    fg="#ffffff",  # Color del texto del botón
    bg="#007acc",  # Color de fondo del botón
    activebackground="#005f99",  # Color cuando se presiona el botón
    bd=3, relief="raised",  # Estilo del borde del botón
    width=40  # Ancho del botón
)
boton3.pack(pady=10)

etiqueta2 = tk.Label(
    ventana, 
    text="Tkinter es multiplataforma", 
    font=("Arial", 14, "bold"), 
    fg="#433333",  # Color del texto
    bg="#FFC400"  # Color de fondo
)
etiqueta2.pack(pady=30)  # Espacio vertical entre elementos

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()
