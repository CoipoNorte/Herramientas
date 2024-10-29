import customtkinter as ctk
import os
from tkinter import filedialog, messagebox
from PIL import Image

# Estructura de carpetas por tópico
project_templates = {
    "Vanilla JS": ["src", "dist", "assets", "index.html"],
    "PHP": ["public", "src", "config", "tests"],
    "Python": ["src", "tests", "docs", "requirements.txt"],
    "C++": ["src", "include", "lib", "build"],
    "Java": ["src/main/java", "src/main/resources", "test", "target"],
    "TypeScript": ["src", "dist", "types", "tests"],
    "CSS/HTML": ["css", "js", "images", "index.html"],
    "MVC": ["models", "views", "controllers", "public"],
    "Arquitectura Hexagonal": ["application", "domain", "infrastructure", "interfaces"]
}

class ProjectSetupApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de ventana
        self.title("Creador de Estructura de Proyecto")
        self.geometry("800x570")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Variables de la interfaz
        self.selected_template = None
        self.project_name = ctk.StringVar()
        self.project_path = ctk.StringVar()
        self.buttons = {}  # Para gestionar los colores de los botones

        # Diseño de la interfaz
        self.setup_interface()

    def setup_interface(self):
        # Botones para cada tipo de proyecto
        grid_frame = ctk.CTkFrame(self)
        grid_frame.pack(pady=10)

        for idx, (topic, structure) in enumerate(project_templates.items()):
            btn = ctk.CTkButton(grid_frame, text=topic, command=lambda t=topic: self.select_template(t))
            btn.grid(row=idx // 3, column=idx % 3, padx=10, pady=10)
            self.buttons[topic] = btn  # Guardamos el botón

        # Previsualización de estructura de carpetas
        self.preview_frame = ctk.CTkFrame(self, width=300, height=200)
        self.preview_frame.pack(pady=20)
        self.preview_label = ctk.CTkLabel(self.preview_frame, text="Estructura de Proyecto:")
        self.preview_label.pack(anchor="w", padx=10, pady=5)
        self.preview_text = ctk.CTkTextbox(self.preview_frame, width=400, height=150)
        self.preview_text.pack(padx=10, pady=5)

        # Entrada de nombre del proyecto
        name_frame = ctk.CTkFrame(self)
        name_frame.pack(pady=10)

        ctk.CTkLabel(name_frame, text="Nombre del Proyecto: ").grid(row=0, column=0, padx=10)
        ctk.CTkEntry(name_frame, textvariable=self.project_name).grid(row=0, column=1, padx=10)

        # Botón para seleccionar la ruta del proyecto
        path_frame = ctk.CTkFrame(self)
        path_frame.pack(pady=10)

        ctk.CTkLabel(path_frame, text="Ruta de Proyecto: ").grid(row=0, column=0, padx=10)
        ctk.CTkEntry(path_frame, textvariable=self.project_path, width=300).grid(row=0, column=1, padx=10)
        ctk.CTkButton(path_frame, text="Seleccionar Ruta", command=self.select_path).grid(row=0, column=2, padx=10)

        # Botón de creación
        create_button = ctk.CTkButton(self, text="Crear Proyecto", command=self.create_project)
        create_button.pack(pady=20)


    def select_template(self, template):
        # Resalta el botón seleccionado
        for btn_template, btn in self.buttons.items():
            if btn_template == template:
                btn.configure(fg_color=("light blue", "light blue"))
            else:
                btn.configure(fg_color="transparent")
        
        # Actualizamos la plantilla seleccionada y mostramos la previsualización
        self.selected_template = template
        self.preview_text.delete("1.0", "end")
        structure = project_templates[template]
        for item in structure:
            self.preview_text.insert("end", f"{item}\n")

    def select_path(self):
        path = filedialog.askdirectory()
        if path:
            self.project_path.set(path)

    def create_project(self):
        # Validaciones
        if not self.selected_template:
            messagebox.showwarning("Falta selección", "Por favor selecciona un tipo de proyecto")
            return
        if not self.project_name.get():
            messagebox.showwarning("Falta nombre", "Por favor ingresa un nombre para el proyecto")
            return
        if not self.project_path.get():
            messagebox.showwarning("Falta ruta", "Por favor selecciona una ruta de destino")
            return

        # Construcción de la estructura
        project_root = os.path.join(self.project_path.get(), f"{self.project_name.get()} - {self.selected_template}")
        if not os.path.exists(project_root):
            os.makedirs(project_root)
        
        for item in project_templates[self.selected_template]:
            path = os.path.join(project_root, item)
            if '.' in item:
                open(path, 'w').close()  # Crear archivo
            else:
                os.makedirs(path, exist_ok=True)  # Crear carpeta

        messagebox.showinfo("Proyecto creado", f"Proyecto '{self.project_name.get()}' creado exitosamente en:\n{self.project_path.get()}")

if __name__ == "__main__":
    app = ProjectSetupApp()
    app.mainloop()
