import customtkinter as ctk
from controllers.app_controller import AppController
from config.settings import THEME_MODE, THEME_COLOR

def main():
    # Configurar tema
    ctk.set_appearance_mode(THEME_MODE)
    ctk.set_default_color_theme(THEME_COLOR)
    
    # Iniciar aplicación
    app = AppController()
    app.run()

if __name__ == "__main__":
    main()