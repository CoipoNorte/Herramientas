import customtkinter as ctk
from tkinter import messagebox, filedialog
from typing import Callable
from views.components.path_selector import PathSelector
from views.components.editor_panel import EditorPanel
from views.components.preview_panel import PreviewPanel
from views.components.tools_panel import ToolsPanel
from config.settings import APP_TITLE, APP_GEOMETRY
from utils.constants import BUTTON_COLORS, PROJECT_EXTENSION
from utils.templates import TEMPLATES

class MainWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)
        self._create_widgets()
    
    def _create_widgets(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Selector de ruta
        self.path_selector = PathSelector(
            self.main_frame,
            self.controller.get_current_path(),
            self.controller.on_path_change
        )
        self.path_selector.pack(pady=20, padx=20, fill="x")
        
        # Botones en el selector de ruta
        button_frame = self.path_selector.get_button_frame()
        
        self.change_path_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Cambiar Ruta",
            command=self.controller.on_change_path,
            width=150,
            height=35
        )
        self.change_path_btn.pack(side="left", padx=5)
        
        self.generate_btn_top = ctk.CTkButton(
            button_frame,
            text="🚀 Generar Proyecto",
            command=self.controller.on_generate_structure,
            width=150,
            height=35,
            fg_color=BUTTON_COLORS["generate"]["fg"],
            hover_color=BUTTON_COLORS["generate"]["hover"]
        )
        self.generate_btn_top.pack(side="left", padx=5)
        
        self.save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Guardar Proyecto",
            command=self.controller.on_save_project,
            width=150,
            height=35,
            fg_color=BUTTON_COLORS["save_load"]["fg"],
            hover_color=BUTTON_COLORS["save_load"]["hover"]
        )
        self.save_btn.pack(side="left", padx=5)
        
        self.load_btn = ctk.CTkButton(
            button_frame,
            text="📂 Cargar Proyecto",
            command=self.controller.on_load_project,
            width=150,
            height=35,
            fg_color=BUTTON_COLORS["save_load"]["fg"],
            hover_color=BUTTON_COLORS["save_load"]["hover"]
        )
        self.load_btn.pack(side="left", padx=5)
        
        # Frame de contenido
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Título del editor
        self.editor_title = ctk.CTkLabel(
            self.content_frame,
            text="📝 Editor de Estructura:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.editor_title.pack(pady=(15, 10))
        
        # Frame horizontal
        self.horizontal_frame = ctk.CTkFrame(self.content_frame)
        self.horizontal_frame.pack(pady=(0, 20), padx=20, fill="both", expand=True)
        
        # Panel de herramientas
        self.tools_panel = ToolsPanel(
            self.horizontal_frame,
            self.controller.on_insert_character,
            self.controller.on_template_select,
            self.controller.on_clear_editor,
            list(TEMPLATES.keys())
        )
        self.tools_panel.pack(side="left", fill="y", padx=(0, 10))
        
        # Panel del editor
        self.editor_panel = EditorPanel(
            self.horizontal_frame,
            self.controller.on_text_change
        )
        self.editor_panel.pack(side="left", fill="both", expand=True)
        
        # Panel de vista previa
        self.preview_panel = PreviewPanel(self.horizontal_frame)
        self.preview_panel.pack(side="right", fill="y", padx=(10, 0))
        
        # Frame para botón principal
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=20, padx=20, fill="x")
        
        # Botón GENERAR grande
        self.generate_btn_main = ctk.CTkButton(
            self.button_frame,
            text="🚀 GENERAR ESTRUCTURA",
            command=self.controller.on_generate_structure,
            width=300,
            height=50,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=BUTTON_COLORS["generate"]["fg"],
            hover_color=BUTTON_COLORS["generate"]["hover"]
        )
        self.generate_btn_main.pack(pady=20)
        
        # Footer
        self.footer = ctk.CTkLabel(
            self,
            text="💡 Tip: Usa '/' al final para carpetas, sin '/' para archivos | Usa # para comentarios",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.footer.pack(pady=(0, 10))
    
    # Métodos de interfaz
    def get_editor_text(self) -> str:
        return self.editor_panel.get_text()
    
    def set_editor_text(self, text: str):
        self.editor_panel.set_text(text)
    
    def clear_editor(self):
        self.editor_panel.clear()
    
    def insert_character(self, char: str):
        self.editor_panel.insert_at_cursor(char)
    
    def update_preview(self, content: str):
        self.preview_panel.update_preview(content)
    
    def update_path(self, path: str):
        self.path_selector.update_path(path)
    
    # Diálogos
    def show_warning(self, message: str):
        messagebox.showwarning("⚠️ Advertencia", message)
    
    def show_error(self, message: str):
        messagebox.showerror("❌ Error", message)
    
    def show_success(self, message: str):
        messagebox.showinfo("✅ Éxito", message)
    
    def confirm_generation(self, carpetas: int, archivos: int, ruta: str) -> bool:
        preview = f"🎯 Se creará:\n\n"
        preview += f"📁 {carpetas} carpetas\n"
        preview += f"📄 {archivos} archivos\n\n"
        preview += f"📍 En: {ruta}\n\n"
        preview += "¿Continuar con la creación?"
        
        return messagebox.askyesno("🚀 Confirmar Creación", preview)
    
    def ask_directory(self, initial_dir: str) -> str:
        return filedialog.askdirectory(initialdir=initial_dir)
    
    def ask_save_file(self) -> str:
        return filedialog.asksaveasfilename(
            defaultextension=PROJECT_EXTENSION,
            filetypes=[("Folder Structure Files", f"*{PROJECT_EXTENSION}"), ("All Files", "*.*")]
        )
    
    def ask_open_file(self) -> str:
        return filedialog.askopenfilename(
            filetypes=[("Folder Structure Files", f"*{PROJECT_EXTENSION}"), ("All Files", "*.*")]
        )