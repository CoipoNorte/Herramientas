import customtkinter as ctk

class PreviewPanel(ctk.CTkFrame):
    def __init__(self, parent, width: int = 300):
        super().__init__(parent, width=width)
        self.pack_propagate(False)
        self._create_widgets()
    
    def _create_widgets(self):
        # Título
        self.title_label = ctk.CTkLabel(
            self,
            text="👁️ Vista Previa",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.title_label.pack(pady=(10, 5))
        
        # Área de vista previa
        self.preview_area = ctk.CTkTextbox(
            self,
            height=350,
            font=ctk.CTkFont(family="Courier New", size=12),
            wrap="none",
            state="disabled"
        )
        self.preview_area.pack(pady=5, padx=5, fill="both", expand=True)
    
    def update_preview(self, content: str):
        self.preview_area.configure(state="normal")
        self.preview_area.delete("1.0", "end")
        self.preview_area.insert("1.0", content)
        self.preview_area.configure(state="disabled")