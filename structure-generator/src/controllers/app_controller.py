import os
import threading
from tkinter import messagebox
from models.structure_model import StructureModel
from services.parser_service import ParserService
from services.generator_service import GeneratorService
from services.file_service import FileService
from views.main_window import MainWindow
from config.settings import DEFAULT_PATH, PREVIEW_UPDATE_INTERVAL
from utils.templates import TEMPLATES, DEFAULT_EXAMPLE

class AppController:
    def __init__(self):
        self.model = StructureModel()
        self.model.ruta_destino = DEFAULT_PATH
        self.parser = ParserService()
        self.generator = GeneratorService()
        self.file_service = FileService()
        self.view = MainWindow(self)
        
        # Cargar ejemplo inicial
        self.view.set_editor_text(DEFAULT_EXAMPLE)
        
        # Iniciar actualización periódica
        self._start_periodic_update()
    
    def _start_periodic_update(self):
        """Inicia la actualización periódica de la vista previa"""
        def update():
            while True:
                self.on_text_change()
                threading.Event().wait(PREVIEW_UPDATE_INTERVAL)
        
        thread = threading.Thread(target=update, daemon=True)
        thread.start()
    
    def get_current_path(self) -> str:
        return self.model.ruta_destino
    
    def on_path_change(self, new_path: str):
        self.model.ruta_destino = new_path
    
    def on_change_path(self):
        """Maneja el cambio de ruta"""
        new_path = self.view.ask_directory(self.model.ruta_destino)
        if new_path:
            self.model.ruta_destino = new_path
            self.view.update_path(new_path)
    
    def on_text_change(self):
        """Actualiza la vista previa cuando cambia el texto"""
        texto = self.view.get_editor_text()
        
        if not texto:
            self.view.update_preview("Escribe una estructura para ver la vista previa...")
            return
        
        try:
            estructura = self.parser.parse_structure(texto)
            if not estructura:
                self.view.update_preview("Estructura no válida")
                return
            
            # Actualizar modelo
            self.model.set_items(estructura)
            
            # Generar vista previa
            preview = self._generate_preview()
            self.view.update_preview(preview)
            
        except Exception as e:
            self.view.update_preview(f"Error al generar vista previa:\n{str(e)}")
    
    def _generate_preview(self) -> str:
        """Genera una representación visual de la estructura"""
        if not self.model.items:
            return "Estructura vacía"
        
        resultado = []
        for item in self.model.items:
            indent = "    " * item.nivel
            if item.es_carpeta:
                resultado.append(f"{indent}📁 {item.nombre}/")
            else:
                resultado.append(f"{indent}📄 {item.nombre}")
        
        return "\n".join(resultado)
    
    def on_generate_structure(self):
        """Maneja la generación de estructura"""
        texto = self.view.get_editor_text()
        
        if not texto:
            self.view.show_warning("Por favor, ingresa una estructura de carpetas.")
            return
        
        try:
            if not os.path.exists(self.model.ruta_destino):
                self.view.show_error(f"La ruta no existe: {self.model.ruta_destino}")
                return
            
            # Parsear estructura
            estructura = self.parser.parse_structure(texto)
            if not estructura:
                self.view.show_warning("No se pudo interpretar la estructura.")
                return
            
            self.model.set_items(estructura)
            self.model.texto_original = texto
            
            # Obtener estadísticas
            carpetas, archivos = self.model.get_statistics()
            
            # Confirmar con el usuario
            if self.view.confirm_generation(carpetas, archivos, self.model.ruta_destino):
                # Generar estructura
                rutas_creadas, proyecto_raiz = self.generator.create_structure(
                    self.model, 
                    self.model.ruta_destino,
                    self.model.texto_original
                )
                
                # Mensaje de éxito
                mensaje = f"🎉 ¡Estructura creada exitosamente!\n\n"
                mensaje += f"📁 Proyecto: {proyecto_raiz}\n"
                mensaje += f"📍 Ubicación: {self.model.ruta_destino}\n"
                mensaje += f"📊 Total: {len(rutas_creadas)} elementos\n"
                
                self.view.show_success(mensaje)
                
        except Exception as e:
            self.view.show_error(str(e))
    
    def on_save_project(self):
        """Maneja el guardado del proyecto"""
        texto = self.view.get_editor_text()
        if not texto:
            self.view.show_warning("No hay estructura para guardar")
            return
        
        file_path = self.view.ask_save_file()
        if not file_path:
            return
        
        try:
            self.file_service.save_project(texto, self.model.ruta_destino, file_path)
            self.view.show_success("Proyecto guardado correctamente")
        except Exception as e:
            self.view.show_error(f"No se pudo guardar el proyecto: {str(e)}")
    
    def on_load_project(self):
        """Maneja la carga del proyecto"""
        file_path = self.view.ask_open_file()
        if not file_path:
            return
        
        try:
            proyecto = self.file_service.load_project(file_path)
            
            # Cargar estructura
            self.view.set_editor_text(proyecto.get("estructura", ""))
            
            # Cargar ruta si existe
            if "ruta_destino" in proyecto and os.path.exists(proyecto["ruta_destino"]):
                self.model.ruta_destino = proyecto["ruta_destino"]
                self.view.update_path(self.model.ruta_destino)
            
            self.view.show_success("Proyecto cargado correctamente")
        except Exception as e:
            self.view.show_error(f"No se pudo cargar el proyecto: {str(e)}")
    
    def on_template_select(self, template_name: str):
        """Maneja la selección de plantilla"""
        if template_name == "Seleccione una plantilla":
            return
        
        template_text = TEMPLATES.get(template_name, "")
        if template_text:
            self.view.set_editor_text(template_text)
    
    def on_insert_character(self, character: str):
        """Inserta un carácter en el editor"""
        self.view.insert_character(character)
    
    def on_clear_editor(self):
        """Limpia el editor"""
        self.view.clear_editor()
    
    def run(self):
        """Ejecuta la aplicación"""
        self.view.mainloop()