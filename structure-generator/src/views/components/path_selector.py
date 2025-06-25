import customtkinter as ctk
from typing import Callable

class PathSelector(ctk.CTkFrame):
    def __init__(self, parent, initial_path: str, on_path_change: Callable = None):
        super().__init__(parent)
        self.current_path = initial_path
        self.on_path_change = on_path_change
        self._create_widgets()
    
    def _create_widgets(self):
        # Título
        self.title_label = ctk.CTkLabel(
            self,
            text="📁 Ruta de Destino:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.title_label.pack(pady=(15, 5))
        
        # Label de ruta
        self.path_label = ctk.CTkLabel(
            self,
            text=self.current_path,
            font=ctk.CTkFont(size=12),
            text_color="lightblue"
        )
        self.path_label.pack(pady=(0, 10))
        
        # Frame para botones
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=(0, 15))
    
    def update_path(self, new_path: str):
        self.current_path = new_path
        self.path_label.configure(text=new_path)
        if self.on_path_change:
            self.on_path_change(new_path)
    
    def get_button_frame(self):
        return self.button_frame