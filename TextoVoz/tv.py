import customtkinter as ctk
import threading
import pyperclip
import re
from gtts import gTTS
import pygame
import os
import tempfile

class TextToSpeechApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Lector de Texto a Voz")
        self.geometry("600x450")
        self.configure_appearance()

        # Inicialización de pygame para control de reproducción de audio
        pygame.mixer.init()

        self.setup_layout()
        self.is_playing = False
        self.audio_files = []
        self.current_file_index = 0

        # Pegar texto del portapapeles al iniciar la aplicación
        self._paste_clipboard_text()

    def configure_appearance(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def setup_layout(self):
        # Configuración de área de texto
        self.text_area = ctk.CTkTextbox(self, width=580, height=200, corner_radius=10)
        self.text_area.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Marco de botones
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Botón de Reproducir
        self.play_button = ctk.CTkButton(self.button_frame, text="Reproducir", command=self.play)
        self.play_button.grid(row=0, column=0, padx=5, pady=5)

        # Botón de Pausar
        self.pause_button = ctk.CTkButton(self.button_frame, text="Pausar", command=self.pause)
        self.pause_button.grid(row=0, column=1, padx=5, pady=5)

        # Botón de Detener
        self.stop_button = ctk.CTkButton(self.button_frame, text="Detener", command=self.stop)
        self.stop_button.grid(row=0, column=2, padx=5, pady=5)

        # Control de velocidad
        self.speed_label = ctk.CTkLabel(self.button_frame, text="Velocidad (0.5x - 2.0x):")
        self.speed_label.grid(row=1, column=0, padx=5, pady=5)
        self.speed_slider = ctk.CTkSlider(self.button_frame, from_=0.5, to=2.0, number_of_steps=15)
        self.speed_slider.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.speed_slider.set(1.0)

    def _paste_clipboard_text(self):
        text = pyperclip.paste()
        if text:
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", text)

    def process_text(self, text):
        text = re.sub(r'\n', '. ', text)
        text = re.sub(r'[^\w\s.,]', '', text)
        text = re.sub(r'([.,])([^\s])', r'\1 \2', text)
        sentences = re.split(r'(?<=[.,])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def generate_audio_files(self, sentences):
        self.clear_audio_files()
        temp_dir = tempfile.gettempdir()
        speed = self.speed_slider.get()
        
        for i, sentence in enumerate(sentences):
            tts = gTTS(text=sentence, lang='es', slow=speed < 1.0)
            file_path = os.path.join(temp_dir, f"tts_sentence_{i}.mp3")
            tts.save(file_path)
            self.audio_files.append(file_path)

    def play(self):
        text = self.text_area.get("1.0", "end-1c").strip()
        if not text:
            text = pyperclip.paste()
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", text)

        sentences = self.process_text(text)
        self.generate_audio_files(sentences)
        
        if self.audio_files:
            self.is_playing = True
            self.current_file_index = 0
            self._play_audio_file(self.audio_files[self.current_file_index])

    def _play_audio_file(self, file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy() and self.is_playing:
            continue

        if self.is_playing and self.current_file_index < len(self.audio_files) - 1:
            self.current_file_index += 1
            self._play_audio_file(self.audio_files[self.current_file_index])
        else:
            self.stop()

    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()

    def stop(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.current_file_index = 0
            self.clear_audio_files()

    def clear_audio_files(self):
        for file_path in self.audio_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        self.audio_files.clear()

    def on_closing(self):
        self.stop()
        self.destroy()

if __name__ == "__main__":
    app = TextToSpeechApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
