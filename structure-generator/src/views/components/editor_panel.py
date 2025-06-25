import customtkinter as ctk
from typing import Callable

class EditorPanel(ctk.CTkFrame):
    def __init__(self, parent, on_text_change: Callable = None):
        super().__init__(parent)
        self.on_text_change = on_text_change
        self._create_widgets()
    
    def _create_widgets(self):
        # Área de texto
        self.text_area = ctk.CTkTextbox(
            self,
            height=350,
            font=ctk.CTkFont(family="Courier New", size=12),
            wrap="none"
        )
        self.text_area.pack(pady=15, padx=15, fill="both", expand=True)
        
        # Bind para detectar cambios
        if self.on_text_change:
            self.text_area.bind("<KeyRelease>", lambda e: self.on_text_change())
            
    def get_text(self) -> str:
        return self.text_area.get("1.0", "end").strip()
    
    def set_text(self, text: str):
        self.text_area.delete("1.0", "end")
        self.text_area.insert("1.0", text)
    
    def clear(self):
        self.text_area.delete("1.0", "end")
    
    def insert_at_cursor(self, text: str):
        try:
            cursor_pos = self.text_area.index("insert")
            self.text_area.insert(cursor_pos, text)
            self.text_area.focus_set()
        except:
            self.text_area.insert("end", text)
    