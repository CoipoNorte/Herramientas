import customtkinter as ctk
from typing import Callable, List, Dict
from utils.constants import TREE_CHARACTERS, BUTTON_COLORS

class ToolsPanel(ctk.CTkFrame):
    def __init__(self, parent, on_character_insert: Callable, on_template_select: Callable, 
                 on_clear: Callable, templates: List[str], width: int = 200):
        super().__init__(parent, width=width)
        self.pack_propagate(False)
        self.on_character_insert = on_character_insert
        self.on_template_select = on_template_select
        self.on_clear = on_clear
        self.templates = templates
        self._create_widgets()
    
    def _create_widgets(self):
        # Título
        self.title_label = ctk.CTkLabel(
            self,
            text="🔧 Herramientas",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.title_label.pack(pady=(15, 10))
        
        # Botones de caracteres
        for char, descripcion in TREE_CHARACTERS:
            btn = ctk.CTkButton(
                self,
                text=descripcion,
                command=lambda c=char: self.on_character_insert(c),
                width=180,
                height=30,
                font=ctk.CTkFont(family="Courier New", size=12)
            )
            btn.pack(pady=2, padx=10)
        
        # Separador
        separator = ctk.CTkLabel(self, text="───────────", text_color="gray")
        separator.pack(pady=5)
        
        # Menú de plantillas
        self.template_menu = ctk.CTkOptionMenu(
            self,
            values=["Seleccione una plantilla"] + self.templates,
            command=self.on_template_select,
            fg_color=BUTTON_COLORS["template"]["fg"],
            button_color=BUTTON_COLORS["template"]["hover"],
            dropdown_fg_color=BUTTON_COLORS["template"]["fg"],
            dropdown_text_color="white",
            width=180,
            height=30
        )
        self.template_menu.pack(pady=2, padx=10)
        
        # Botón limpiar
        self.clear_button = ctk.CTkButton(
            self,
            text="🧹 Limpiar Todo",
            command=self.on_clear,
            width=180,
            height=30,
            fg_color=BUTTON_COLORS["clear"]["fg"],
            hover_color=BUTTON_COLORS["clear"]["hover"]
        )
        self.clear_button.pack(pady=2, padx=10)