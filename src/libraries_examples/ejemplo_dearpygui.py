import dearpygui.dearpygui as dpg

# Crear el contexto de Dear PyGui
dpg.create_context()

# Crear una ventana
with dpg.window(label="Ventana principal", width=400, height=300):
    # Crear un input para ingresar el nombre
    input_text = dpg.add_input_text(label="¿Cómo te llamas?", tag="input")
    
    # Crear un texto vacío donde aparecerá el saludo
    output_text = dpg.add_text("", tag="output")
    
    # Crear un contenedor horizontal para los botones
    with dpg.group(horizontal=True):
        # Crear un botón OK
        dpg.add_button(label="OK", callback=lambda: dpg.set_value("output", f"Hola {dpg.get_value('input')}"))
        
        # Crear un botón Exit que cierra la aplicación
        dpg.add_button(label="Exit", callback=lambda: dpg.stop_dearpygui())

# Configurar el viewport (ventana principal)
dpg.create_viewport(title='Aplicación Dear PyGui', width=600, height=400)
dpg.setup_dearpygui()

# Mostrar la ventana (viewport)
dpg.show_viewport()

# Mantener la ventana abierta hasta que se cierre manualmente
dpg.start_dearpygui()

# Limpiar el contexto después de cerrar la ventana
dpg.destroy_context()
