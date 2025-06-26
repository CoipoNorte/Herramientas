import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import pyttsx3
import speech_recognition as sr
from pydub import AudioSegment
import os
import threading
from gtts import gTTS
import pygame
import tempfile

# Configuración de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Texto y Voz")
        self.root.geometry("800x600")
        
        # Inicializar pygame para reproducir audio
        pygame.mixer.init()
        
        # Crear el contenedor principal con pestañas
        self.tabview = ctk.CTkTabview(root)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Crear pestañas
        self.tab_text_to_speech = self.tabview.add("Texto a Voz")
        self.tab_speech_to_text = self.tabview.add("Voz a Texto")
        
        # Configurar pestaña de Texto a Voz
        self.setup_text_to_speech_tab()
        
        # Configurar pestaña de Voz a Texto
        self.setup_speech_to_text_tab()
        
    def setup_text_to_speech_tab(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.tab_text_to_speech)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="Texto a Voz", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=10)
        
        # Área de texto
        self.text_input = ctk.CTkTextbox(main_frame, height=200, 
                                         font=ctk.CTkFont(size=14))
        self.text_input.pack(fill="both", expand=True, padx=20, pady=10)
        self.text_input.insert("1.0", "Escribe aquí el texto que quieres convertir a voz...")
        
        # Frame para botones
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=10)
        
        # Botón para normalizar texto
        self.normalize_btn = ctk.CTkButton(button_frame, text="Normalizar Texto",
                                          command=self.normalize_text,
                                          width=150)
        self.normalize_btn.grid(row=0, column=0, padx=5)
        
        # Botón para convertir a voz
        self.convert_btn = ctk.CTkButton(button_frame, text="Convertir a Voz",
                                        command=self.text_to_speech,
                                        width=150)
        self.convert_btn.grid(row=0, column=1, padx=5)
        
        # Selector de idioma
        self.language_var = ctk.StringVar(value="es")
        language_frame = ctk.CTkFrame(main_frame)
        language_frame.pack(pady=10)
        
        ctk.CTkLabel(language_frame, text="Idioma:").grid(row=0, column=0, padx=5)
        self.language_menu = ctk.CTkOptionMenu(language_frame, 
                                              values=["es", "en", "fr", "de", "it"],
                                              variable=self.language_var)
        self.language_menu.grid(row=0, column=1, padx=5)
        
    def setup_speech_to_text_tab(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.tab_speech_to_text)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="Voz a Texto", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=10)
        
        # Botón para seleccionar archivo
        self.select_file_btn = ctk.CTkButton(main_frame, text="Seleccionar Audio (MP3/MP4)",
                                            command=self.select_audio_file,
                                            width=200, height=40)
        self.select_file_btn.pack(pady=20)
        
        # Label para mostrar archivo seleccionado
        self.file_label = ctk.CTkLabel(main_frame, text="No se ha seleccionado ningún archivo",
                                      font=ctk.CTkFont(size=12))
        self.file_label.pack(pady=5)
        
        # Botón para transcribir
        self.transcribe_btn = ctk.CTkButton(main_frame, text="Transcribir Audio",
                                           command=self.speech_to_text,
                                           width=200, height=40)
        self.transcribe_btn.pack(pady=10)
        
        # Área de texto para mostrar transcripción
        self.transcription_text = ctk.CTkTextbox(main_frame, height=200,
                                                font=ctk.CTkFont(size=14))
        self.transcription_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Botón para guardar transcripción
        self.save_btn = ctk.CTkButton(main_frame, text="Guardar Transcripción",
                                     command=self.save_transcription,
                                     width=200)
        self.save_btn.pack(pady=10)
        
        # Variable para almacenar ruta del archivo
        self.audio_file_path = None
        
    def normalize_text(self):
        # Obtener texto del área de texto
        text = self.text_input.get("1.0", "end-1c")
        
        # Normalizar: eliminar saltos de línea múltiples y espacios extra
        normalized = " ".join(text.split())
        
        # Actualizar el área de texto
        self.text_input.delete("1.0", "end")
        self.text_input.insert("1.0", normalized)
        
        messagebox.showinfo("Éxito", "Texto normalizado correctamente")
        
    def text_to_speech(self):
        text = self.text_input.get("1.0", "end-1c").strip()
        
        if not text:
            messagebox.showwarning("Advertencia", "Por favor, escribe algún texto")
            return
        
        # Ejecutar en un hilo separado para no bloquear la interfaz
        threading.Thread(target=self._convert_to_speech, args=(text,), daemon=True).start()
        
    def _convert_to_speech(self, text):
        try:
            # Usar gTTS para mejor calidad de voz
            language = self.language_var.get()
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Guardar en archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                temp_filename = tmp_file.name
                tts.save(temp_filename)
            
            # Reproducir el audio
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            
            # Esperar a que termine de reproducirse
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Eliminar archivo temporal
            os.unlink(temp_filename)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error al convertir texto a voz: {str(e)}"))
            
    def select_audio_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de audio",
            filetypes=[("Archivos de audio", "*.mp3 *.mp4 *.wav *.m4a")]
        )
        
        if file_path:
            self.audio_file_path = file_path
            filename = os.path.basename(file_path)
            self.file_label.configure(text=f"Archivo seleccionado: {filename}")
            
    def speech_to_text(self):
        if not self.audio_file_path:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo de audio")
            return
        
        # Mostrar mensaje de procesamiento
        self.transcription_text.delete("1.0", "end")
        self.transcription_text.insert("1.0", "Procesando audio, por favor espera...")
        
        # Ejecutar en hilo separado
        threading.Thread(target=self._transcribe_audio, daemon=True).start()
        
    def _transcribe_audio(self):
        try:
            # Convertir a WAV si es necesario
            audio = AudioSegment.from_file(self.audio_file_path)
            
            # Crear archivo temporal WAV
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                temp_wav = tmp_file.name
                audio.export(temp_wav, format="wav")
            
            # Usar speech_recognition
            recognizer = sr.Recognizer()
            
            with sr.AudioFile(temp_wav) as source:
                audio_data = recognizer.record(source)
                
            # Transcribir (usando Google Speech Recognition)
            try:
                text = recognizer.recognize_google(audio_data, language="es-ES")
                
                # Actualizar la interfaz en el hilo principal
                self.root.after(0, lambda: self._update_transcription(text))
                
            except sr.UnknownValueError:
                self.root.after(0, lambda: self._update_transcription("No se pudo entender el audio"))
            except sr.RequestError as e:
                self.root.after(0, lambda: self._update_transcription(f"Error en el servicio: {e}"))
            
            # Eliminar archivo temporal
            os.unlink(temp_wav)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error al procesar audio: {str(e)}"))
            
    def _update_transcription(self, text):
        self.transcription_text.delete("1.0", "end")
        self.transcription_text.insert("1.0", text)
        
    def save_transcription(self):
        text = self.transcription_text.get("1.0", "end-1c").strip()
        
        if not text:
            messagebox.showwarning("Advertencia", "No hay transcripción para guardar")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                messagebox.showinfo("Éxito", "Transcripción guardada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar archivo: {str(e)}")

def main():
    root = ctk.CTk()
    app = TextToSpeechApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()