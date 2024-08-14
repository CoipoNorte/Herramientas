import customtkinter as ctk
import pyttsx3
import threading
import pyperclip
import re

class TextToSpeechApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Lector de Texto")
        self.geometry("600x400")

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.text_area = ctk.CTkTextbox(self, width=580, height=200, corner_radius=10)
        self.text_area.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.play_button = ctk.CTkButton(self.button_frame, text="Reproducir", command=self.play)
        self.play_button.grid(row=0, column=0, padx=5, pady=5)

        self.speed_label = ctk.CTkLabel(self.button_frame, text="Velocidad (palabras por minuto):")
        self.speed_label.grid(row=1, column=0, padx=5, pady=5)

        self.speed_slider = ctk.CTkSlider(self.button_frame, from_=100, to=300, number_of_steps=200)
        self.speed_slider.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.speed_slider.set(200)

        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        spanish_voice = next((v for v in voices if 'spanish' in v.languages), None)
        if spanish_voice:
            self.engine.setProperty('voice', spanish_voice.id)
        self.engine.setProperty('rate', 200)

        self.is_playing = False
        self.current_sentence = 0
        self.sentences = []
        self.lock = threading.Lock()

        # Pegamos el texto del portapapeles al iniciar la aplicación
        self._paste_clipboard_text()

    def _paste_clipboard_text(self):
        text = pyperclip.paste()
        if text:
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", text)

    def process_text(self, text):
        # Reemplazar saltos de línea por puntos
        text = re.sub(r'\n', '. ', text)
        # Eliminar caracteres no deseados, manteniendo solo puntos y comas
        text = re.sub(r'[^\w\s.,]', '', text)
        # Asegurar que haya un espacio después de cada punto y coma
        text = re.sub(r'([.,])([^\s])', r'\1 \2', text)
        # Dividir el texto en oraciones
        sentences = re.split(r'(?<=[.,])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def play(self):
        if not self.is_playing:
            text = self.text_area.get("1.0", "end-1c")
            if not text:
                text = pyperclip.paste()
                self.text_area.delete("1.0", "end")
                self.text_area.insert("1.0", text)
            
            self.sentences = self.process_text(text)
            self.is_playing = True
            self.current_sentence = 0
            self.play_button.configure(state="disabled")
            threading.Thread(target=self._play_thread, daemon=True).start()

    def _play_thread(self):
        while self.current_sentence < len(self.sentences) and self.is_playing:
            self.engine.setProperty('rate', self.speed_slider.get())
            
            sentence = self.sentences[self.current_sentence]
            self.engine.say(sentence)
            self.engine.runAndWait()
            
            if self.is_playing:
                self.current_sentence += 1
        
        self.is_playing = False
        self.current_sentence = 0
        self.play_button.configure(state="normal")

if __name__ == "__main__":
    app = TextToSpeechApp()
    app.mainloop()
