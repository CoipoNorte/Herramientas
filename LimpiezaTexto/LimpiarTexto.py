import tkinter as tk
from tkinter import messagebox
import pyperclip
import re

def clean_text_basic(text):
    """
    Realiza una limpieza básica del texto.
    Elimina índices, números de página y membretes.
    """
    # Reemplaza números de página y miembros comunes de texto
    cleaned_text = re.sub(r'\d+\n', '', text)  # Elimina números de página que están en líneas nuevas
    cleaned_text = re.sub(r'\n\d+\n', '\n', cleaned_text)  # Elimina números de página entre líneas
    cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_text)  # Elimina líneas vacías
    # Puede agregar más reglas de limpieza específicas según el contenido

    return cleaned_text

def clean_text_advanced(text):
    """
    Realiza una limpieza avanzada del texto.
    Elimina saltos de línea y espacios redundantes.
    """
    cleaned_text = clean_text_basic(text)
    # Reemplaza saltos de línea por un solo espacio
    cleaned_text = cleaned_text.replace('\n', ' ')
    # Reemplaza espacios dobles o múltiples por un solo espacio
    cleaned_text = ' '.join(cleaned_text.split())
    
    return cleaned_text

def process_text():
    """
    Procesa el texto del portapapeles y guarda dos versiones.
    """
    try:
        # Obtener texto del portapapeles
        text = pyperclip.paste()
        if not text:
            raise ValueError("El portapapeles está vacío o no contiene texto válido.")

        # Procesar texto y guardar archivos
        basic_cleaned_text = clean_text_basic(text)
        advanced_cleaned_text = clean_text_advanced(text)

        with open('texto_basico_limpio.txt', 'w', encoding='utf-8') as file:
            file.write(basic_cleaned_text)

        with open('texto_avanzado_limpio.txt', 'w', encoding='utf-8') as file:
            file.write(advanced_cleaned_text)

        messagebox.showinfo("Éxito", "Textos limpios guardados con éxito.")
    
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Configuración de la ventana principal
root = tk.Tk()
root.title("Limpiador de Texto")

tk.Label(root, text="Pega el texto en el portapapeles y haz clic en Procesar.").pack(pady=10)

tk.Button(root, text="Procesar Texto", command=process_text).pack(pady=10)

root.mainloop()
