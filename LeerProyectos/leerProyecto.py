import os
import tkinter as tk
from tkinter import messagebox

def generate_ascii_tree(root_dir, prefix='', result=''):
    """
    Genera una representación en ASCII de la estructura de directorios y archivos.
    
    :param root_dir: Ruta del directorio raíz.
    :param prefix: Prefijo para la visualización de subdirectorios.
    :param result: Cadena para almacenar el resultado.
    :return: Cadena con la representación ASCII de la estructura.
    """
    if not os.path.isdir(root_dir):
        raise ValueError(f"{root_dir} no es un directorio o no existe.")

    # Obtén todos los elementos en el directorio actual
    entries = sorted(os.listdir(root_dir))
    
    # Recorre todos los elementos en el directorio
    for index, entry in enumerate(entries):
        path = os.path.join(root_dir, entry)
        is_last = index == len(entries) - 1

        # Agrega el nombre del directorio/archivo con el prefijo adecuado
        result += f"{prefix}{'└── ' if is_last else '├── '}{entry}\n"

        if os.path.isdir(path):
            # Llamada recursiva para subdirectorios
            new_prefix = f"{prefix}{'    ' if is_last else '│   '}"
            result = generate_ascii_tree(path, new_prefix, result)
    
    return result

def save_to_file(text, filename):
    """
    Guarda el texto en un archivo con codificación UTF-8.
    
    :param text: Texto a guardar.
    :param filename: Nombre del archivo.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

def on_generate():
    """
    Maneja el evento de clic en el botón "Generar".
    """
    path = entry.get()
    if not path:
        messagebox.showerror("Error", "Por favor, ingrese una ruta.")
        return
    
    try:
        result = generate_ascii_tree(path)
        save_to_file(result, 'lectura.txt')
    except Exception as e:
        messagebox.showerror("Error", str(e))

def on_copy():
    """
    Maneja el evento de clic en el botón "Copiar".
    """
    try:
        with open('lectura.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        root.clipboard_clear()
        root.clipboard_append(text)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Configuración de la ventana principal
root = tk.Tk()
root.title("Generador de Estructura de Archivos")

tk.Label(root, text="Ruta del directorio:").pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

tk.Button(root, text="Generar", command=on_generate).pack(pady=10)
tk.Button(root, text="Copiar", command=on_copy).pack(pady=10)

root.mainloop()
