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
import time

# Configuración de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Texto y Voz")
        self.root.geometry("800x650")
        
        # Inicializar pygame para reproducir audio
        pygame.mixer.init()
        
        # Variables de control de reproducción
        self.is_playing = False
        self.is_paused = False
        self.current_audio_file = None
        
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
        
        # Manejar el cierre de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        # Detener audio y limpiar archivos temporales
        self.stop_audio()
        self.root.destroy()
        
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
        
        # Frame para botones principales
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
        
        # Frame para controles de reproducción
        playback_frame = ctk.CTkFrame(main_frame)
        playback_frame.pack(pady=10)
        
        # Botón pausar/continuar
        self.pause_btn = ctk.CTkButton(playback_frame, text="Pausar",
                                      command=self.pause_resume_audio,
                                      width=120, state="disabled")
        self.pause_btn.grid(row=0, column=0, padx=5)
        
        # Botón detener
        self.stop_btn = ctk.CTkButton(playback_frame, text="Detener",
                                     command=self.stop_audio,
                                     width=120, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        # Estado de reproducción
        self.status_label = ctk.CTkLabel(playback_frame, text="Estado: Listo",
                                        font=ctk.CTkFont(size=12))
        self.status_label.grid(row=1, column=0, columnspan=2, pady=5)
        
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
        # Detener cualquier reproducción anterior
        self.stop_audio()
        
        text = self.text_input.get("1.0", "end-1c").strip()
        
        if not text:
            messagebox.showwarning("Advertencia", "Por favor, escribe algún texto")
            return
        
        # Deshabilitar botón de convertir mientras se procesa
        self.convert_btn.configure(state="disabled")
        self.status_label.configure(text="Estado: Generando audio...")
        
        # Ejecutar en un hilo separado para no bloquear la interfaz
        threading.Thread(target=self._convert_to_speech, args=(text,), daemon=True).start()
        
    def _convert_to_speech(self, text):
        try:
            # Usar gTTS para mejor calidad de voz
            language = self.language_var.get()
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Crear archivo temporal con un nombre único
            temp_fd, temp_filename = tempfile.mkstemp(suffix='.mp3')
            os.close(temp_fd)  # Cerrar el descriptor de archivo
            
            # Guardar el audio
            tts.save(temp_filename)
            
            # Guardar referencia al archivo actual
            self.current_audio_file = temp_filename
            
            # Reproducir el audio
            self.root.after(0, lambda: self._play_audio(temp_filename))
            
        except Exception as e:
            self.root.after(0, lambda: self._handle_tts_error(str(e)))
            
    def _play_audio(self, filename):
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            
            # Habilitar controles de reproducción
            self.pause_btn.configure(state="normal", text="Pausar")
            self.stop_btn.configure(state="normal")
            self.status_label.configure(text="Estado: Reproduciendo...")
            
            # Monitorear el estado de reproducción
            threading.Thread(target=self._monitor_playback, daemon=True).start()
            
        except Exception as e:
            self._handle_tts_error(f"Error al reproducir audio: {str(e)}")
            
    def _monitor_playback(self):
        while pygame.mixer.music.get_busy() or self.is_paused:
            time.sleep(0.1)
        
        # Reproducción terminada
        if self.is_playing and not self.is_paused:
            self.root.after(0, self._playback_finished)
            
    def _playback_finished(self):
        self.is_playing = False
        self.is_paused = False
        
        # Deshabilitar controles de reproducción
        self.pause_btn.configure(state="disabled", text="Pausar")
        self.stop_btn.configure(state="disabled")
        self.convert_btn.configure(state="normal")
        self.status_label.configure(text="Estado: Listo")
        
        # Limpiar archivo temporal
        self._cleanup_temp_file()
        
    def pause_resume_audio(self):
        if self.is_playing:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.pause_btn.configure(text="Pausar")
                self.status_label.configure(text="Estado: Reproduciendo...")
            else:
                pygame.mixer.music.pause()
                self.is_paused = True
                self.pause_btn.configure(text="Continuar")
                self.status_label.configure(text="Estado: Pausado")
                
    def stop_audio(self):
        if self.is_playing or self.is_paused:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            
            # Restablecer controles
            self.pause_btn.configure(state="disabled", text="Pausar")
            self.stop_btn.configure(state="disabled")
            self.convert_btn.configure(state="normal")
            self.status_label.configure(text="Estado: Detenido")
            
            # Limpiar archivo temporal
            self._cleanup_temp_file()
            
    def _cleanup_temp_file(self):
        if self.current_audio_file and os.path.exists(self.current_audio_file):
            try:
                # Esperar un momento para asegurar que pygame libere el archivo
                time.sleep(0.1)
                pygame.mixer.music.unload()
                os.unlink(self.current_audio_file)
                self.current_audio_file = None
            except Exception:
                # Si falla, intentar eliminar en el próximo uso
                pass
                
    def _handle_tts_error(self, error_msg):
        messagebox.showerror("Error", f"Error al convertir texto a voz: {error_msg}")
        self.convert_btn.configure(state="normal")
        self.status_label.configure(text="Estado: Error")
        self._cleanup_temp_file()
        
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
            temp_fd, temp_wav = tempfile.mkstemp(suffix='.wav')
            os.close(temp_fd)
            
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
            try:
                os.unlink(temp_wav)
            except:
                pass
            
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