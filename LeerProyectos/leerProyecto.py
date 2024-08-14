import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import subprocess  # Para abrir la carpeta de forma compatible en distintos sistemas

# Lista de carpetas reservadas del sistema y otras carpetas que queremos ignorar
IGNORED_FOLDERS = ['System Volume Information', '$RECYCLE.BIN', 'Windows', '.git', '__pycache__']

# Lista de extensiones de archivos de imágenes que queremos ignorar si está marcada la opción
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp']

# Variable global para almacenar el nombre del último archivo generado
last_filename = None

def create_lecturas_folder():
    """
    Crea la carpeta 'lecturas' en la misma ubicación que el script .py si no existe.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    lecturas_dir = os.path.join(script_dir, 'lecturas')

    if not os.path.exists(lecturas_dir):
        os.makedirs(lecturas_dir)
    
    return lecturas_dir

def get_next_file_name():
    """
    Obtiene el nombre del siguiente archivo .txt basado en el número identificador y la fecha y hora.
    """
    lecturas_dir = create_lecturas_folder()
    existing_files = os.listdir(lecturas_dir)
    next_number = len(existing_files) + 1
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    return os.path.join(lecturas_dir, f"{next_number}_{current_time}.txt")

def generate_ascii_tree(root_dir, omit_images=False, prefix='', result=''):
    """
    Genera una representación en ASCII de la estructura de directorios y archivos.
    """
    if not os.path.isdir(root_dir):
        raise ValueError(f"{root_dir} no es un directorio o no existe.")

    entries = sorted(os.listdir(root_dir))
    folders = [entry for entry in entries if os.path.isdir(os.path.join(root_dir, entry)) and entry not in IGNORED_FOLDERS]
    files = [entry for entry in entries if os.path.isfile(os.path.join(root_dir, entry))]

    # Si omit_images está marcado, filtramos los archivos de imagen
    if omit_images:
        files = [file for file in files if not any(file.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)]

    for index, entry in enumerate(folders):
        path = os.path.join(root_dir, entry)
        is_last = index == len(folders) - 1 and not files

        result += f"{prefix}{'└── ' if is_last else '├── '}{entry}/\n"
        new_prefix = f"{prefix}{'    ' if is_last else '│   '}"
        result = generate_ascii_tree(path, omit_images, new_prefix, result)

    for index, entry in enumerate(files):
        is_last = index == len(files) - 1
        result += f"{prefix}{'└── ' if is_last else '├── '}{entry}\n"

    return result

def save_to_file(text, filename, root_dir):
    """
    Guarda el texto en un archivo con el nombre del proyecto en la parte superior.
    """
    project_name = os.path.basename(root_dir)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Proyecto: {project_name}\n")
        file.write("=" * (len(project_name) + 10) + "\n")
        file.write(text)

def open_lecturas_folder():
    """
    Abre la carpeta de 'lecturas' donde se guardan los archivos.
    """
    lecturas_dir = create_lecturas_folder()
    if os.name == 'nt':  # Si el sistema operativo es Windows
        os.startfile(lecturas_dir)
    elif os.name == 'posix':  # Si es Linux o macOS
        subprocess.run(['xdg-open', lecturas_dir])
    else:
        messagebox.showerror("Error", "No se puede abrir la carpeta en este sistema operativo.")

def on_generate():
    """
    Maneja el evento de clic en el botón "Generar".
    """
    global last_filename
    path = entry.get()
    if not path:
        messagebox.showerror("Error", "Por favor, ingrese una ruta.")
        return
    
    omit_images = img_checkbox_var.get()  # Verifica si la casilla "Omitir imágenes" está marcada
    
    try:
        result = generate_ascii_tree(path, omit_images)
        last_filename = get_next_file_name()  # Actualiza la variable global con el nombre del archivo generado
        save_to_file(result, last_filename, path)
        messagebox.showinfo("Éxito", f"Estructura guardada en: {last_filename}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def on_copy():
    """
    Maneja el evento de clic en el botón "Copiar".
    Copia el contenido del último archivo generado.
    """
    if not last_filename:
        messagebox.showerror("Error", "No se ha generado ninguna lectura aún.")
        return

    try:
        with open(last_filename, 'r', encoding='utf-8') as file:
            text = file.read()
        root.clipboard_clear()
        root.clipboard_append(text)
        messagebox.showinfo("Éxito", "Lectura copiada al portapapeles.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Configuración de la ventana principal
root = tk.Tk()
root.title("Generador de Estructura de Archivos")

tk.Label(root, text="Ruta del directorio:").pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

# Checkbox para omitir imágenes
img_checkbox_var = tk.BooleanVar()
img_checkbox = tk.Checkbutton(root, text="Omitir imágenes", variable=img_checkbox_var)
img_checkbox.pack(pady=5)

tk.Button(root, text="Generar", command=on_generate).pack(pady=10)
tk.Button(root, text="Copiar", command=on_copy).pack(pady=10)
tk.Button(root, text="Carpeta", command=open_lecturas_folder).pack(pady=10)

root.mainloop()
