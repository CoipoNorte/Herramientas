import json
import datetime
from typing import Dict, Optional

class FileService:
    @staticmethod
    def save_project(estructura: str, ruta_destino: str, file_path: str) -> None:
        """Guarda el proyecto en un archivo JSON"""
        proyecto = {
            "estructura": estructura,
            "ruta_destino": ruta_destino,
            "fecha": datetime.datetime.now().isoformat()
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(proyecto, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_project(file_path: str) -> Optional[Dict]:
        """Carga un proyecto desde un archivo JSON"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)