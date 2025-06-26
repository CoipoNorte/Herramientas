import subprocess
import sys
import customtkinter as ctk
import os
import threading
import time
from datetime import datetime, timedelta
import pystray
from PIL import Image, ImageDraw
from tkinter import messagebox

# Ocultar consola en Windows
if sys.platform == "win32":
    import ctypes
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    
    SW_HIDE = 0
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, SW_HIDE)

# Configuración del tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ShutdownTimerApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Shutdown Timer")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        
        # Variables
        self.timer_running = False
        self.remaining_time = 0
        self.icon = None
        self.force_shutdown = ctk.BooleanVar(value=True)  # Por defecto forzar cierre
        
        # Configurar el protocolo de cierre
        self.root.protocol('WM_DELETE_WINDOW', self.hide_window)
        
        # Crear la interfaz
        self.setup_ui()
        
        # Centrar la ventana
        self.center_window()
        
    def setup_ui(self):
        # Frame principal con padding
        main_frame = ctk.CTkFrame(self.root, corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Temporizador de Apagado",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(30, 20))
        
        # Frame para el tiempo
        time_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        time_frame.pack(pady=20)
        
        # Etiquetas para horas y minutos
        ctk.CTkLabel(time_frame, text="Horas", font=ctk.CTkFont(size=14)).grid(row=0, column=0, padx=20)
        ctk.CTkLabel(time_frame, text="Minutos", font=ctk.CTkFont(size=14)).grid(row=0, column=2, padx=20)
        
        # Spinbox para horas
        self.hours_var = ctk.StringVar(value="0")
        self.hours_spinbox = ctk.CTkEntry(
            time_frame, 
            width=80, 
            height=50,
            font=ctk.CTkFont(size=24),
            textvariable=self.hours_var,
            justify="center"
        )
        self.hours_spinbox.grid(row=1, column=0, padx=20)
        
        # Separador ":"
        ctk.CTkLabel(time_frame, text=":", font=ctk.CTkFont(size=24)).grid(row=1, column=1)
        
        # Spinbox para minutos
        self.minutes_var = ctk.StringVar(value="30")
        self.minutes_spinbox = ctk.CTkEntry(
            time_frame, 
            width=80, 
            height=50,
            font=ctk.CTkFont(size=24),
            textvariable=self.minutes_var,
            justify="center"
        )
        self.minutes_spinbox.grid(row=1, column=2, padx=20)
        
        # Display del tiempo restante
        self.time_display = ctk.CTkLabel(
            main_frame,
            text="00:00:00",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color="#00ff41"
        )
        self.time_display.pack(pady=30)
        
        # Etiqueta de estado
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Inactivo",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.status_label.pack(pady=(0, 20))
        
        # Checkbox para forzar cierre
        force_checkbox = ctk.CTkCheckBox(
            main_frame,
            text="Forzar cierre de aplicaciones",
            variable=self.force_shutdown,
            font=ctk.CTkFont(size=14),
            corner_radius=5
        )
        force_checkbox.pack(pady=(0, 20))
        
        # Frame para botones
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        # Botón de inicio
        self.start_button = ctk.CTkButton(
            button_frame,
            text="Iniciar",
            width=120,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.start_timer,
            corner_radius=20
        )
        self.start_button.grid(row=0, column=0, padx=10)
        
        # Botón de cancelar
        self.cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            width=120,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.cancel_timer,
            state="disabled",
            corner_radius=20,
            fg_color="#ff4444",
            hover_color="#cc0000"
        )
        self.cancel_button.grid(row=0, column=1, padx=10)
        
        # Botón para minimizar a la bandeja
        minimize_button = ctk.CTkButton(
            main_frame,
            text="Minimizar a la bandeja del sistema",
            width=250,
            height=35,
            font=ctk.CTkFont(size=14),
            command=self.hide_window,
            corner_radius=20,
            fg_color="transparent",
            border_width=2
        )
        minimize_button.pack(pady=(20, 0))
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_tray_icon(self):
        # Crear un ícono simple
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='black')
        draw = ImageDraw.Draw(image)
        
        # Dibujar un círculo con un símbolo de power
        draw.ellipse([10, 10, 54, 54], fill='#1f538d', outline='white', width=2)
        draw.line([32, 20, 32, 35], fill='white', width=4)
        draw.arc([24, 24, 40, 40], start=45, end=315, fill='white', width=3)
        
        return image
    
    def setup_tray_icon(self):
        # Crear el menú del ícono
        menu = pystray.Menu(
            pystray.MenuItem("Mostrar", self.show_window),
            pystray.MenuItem("Cancelar temporizador", self.cancel_timer),
            pystray.MenuItem("Salir", self.quit_app)
        )
        
        # Crear el ícono
        image = self.create_tray_icon()
        self.icon = pystray.Icon("shutdown_timer", image, "Shutdown Timer", menu)
        
        # Ejecutar el ícono en un hilo separado
        icon_thread = threading.Thread(target=self.icon.run, daemon=True)
        icon_thread.start()
    
    def hide_window(self):
        self.root.withdraw()
        if self.icon is None:
            self.setup_tray_icon()
    
    def show_window(self, icon=None, item=None):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def quit_app(self, icon=None, item=None):
        if self.timer_running:
            # Si la ventana está oculta, mostrarla para el diálogo
            if not self.root.winfo_viewable():
                self.root.deiconify()
            
            if messagebox.askyesno("Confirmar", "Hay un temporizador activo. ¿Deseas salir de todos modos?"):
                self.timer_running = False
                if self.icon:
                    self.icon.stop()
                self.root.quit()
                sys.exit()
        else:
            if self.icon:
                self.icon.stop()
            self.root.quit()
            sys.exit()
    
    def start_timer(self):
        try:
            hours = int(self.hours_var.get() or 0)
            minutes = int(self.minutes_var.get() or 0)
            
            if hours == 0 and minutes == 0:
                messagebox.showerror("Error", "Por favor ingresa un tiempo válido")
                return
            
            total_seconds = (hours * 3600) + (minutes * 60)
            self.remaining_time = total_seconds
            self.timer_running = True
            
            # Actualizar UI
            self.start_button.configure(state="disabled")
            self.cancel_button.configure(state="normal")
            self.hours_spinbox.configure(state="disabled")
            self.minutes_spinbox.configure(state="disabled")
            
            # Calcular hora de apagado
            shutdown_time = datetime.now() + timedelta(seconds=total_seconds)
            self.status_label.configure(
                text=f"Apagado programado para: {shutdown_time.strftime('%H:%M:%S')}",
                text_color="orange"
            )
            
            # Iniciar el contador
            timer_thread = threading.Thread(target=self.countdown)
            timer_thread.daemon = True
            timer_thread.start()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa números válidos")
    
    def countdown(self):
        while self.remaining_time > 0 and self.timer_running:
            hours, remainder = divmod(self.remaining_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_format = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            # Actualizar el display
            self.time_display.configure(text=time_format)
            
            # Cambiar color según el tiempo restante
            if self.remaining_time <= 60:
                self.time_display.configure(text_color="#ff4444")
            elif self.remaining_time <= 300:
                self.time_display.configure(text_color="#ff9944")
            
            time.sleep(1)
            self.remaining_time -= 1
        
        if self.timer_running and self.remaining_time == 0:
            self.shutdown_computer()
    
    def cancel_timer(self, icon=None, item=None):
        self.timer_running = False
        self.remaining_time = 0
        
        # Resetear UI
        self.start_button.configure(state="normal")
        self.cancel_button.configure(state="disabled")
        self.hours_spinbox.configure(state="normal")
        self.minutes_spinbox.configure(state="normal")
        self.time_display.configure(text="00:00:00", text_color="#00ff41")
        self.status_label.configure(text="Cancelado", text_color="gray")
    
    def shutdown_computer(self):
        # NO mostrar ninguna ventana emergente
        # Apagado inmediato sin interrupciones
        
        if self.force_shutdown.get():
            # Forzar cierre de todas las aplicaciones
            os.system("shutdown /s /f /t 0")
        else:
            # Apagado normal (espera a que las aplicaciones se cierren)
            os.system("shutdown /s /t 0")
        
        # La aplicación se cerrará automáticamente con el sistema
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ShutdownTimerApp()
    app.run()