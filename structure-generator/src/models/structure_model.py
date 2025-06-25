from dataclasses import dataclass
from typing import List, Optional

@dataclass
class StructureItem:
    nombre: str
    ruta_completa: str
    nivel: int
    es_carpeta: bool
    comentario: str = ""

class StructureModel:
    def __init__(self):
        self.items: List[StructureItem] = []
        self.ruta_destino = ""
        self.texto_original = ""
    
    def add_item(self, item: StructureItem):
        self.items.append(item)
    
    def clear(self):
        self.items.clear()
    
    def set_items(self, items: List[dict]):
        """Convierte diccionarios a StructureItem"""
        self.clear()
        for item_dict in items:
            item = StructureItem(
                nombre=item_dict['nombre'],
                ruta_completa=item_dict['ruta_completa'],
                nivel=item_dict['nivel'],
                es_carpeta=item_dict['es_carpeta'],
                comentario=item_dict.get('comentario', '')
            )
            self.add_item(item)
    
    def get_statistics(self):
        total_carpetas = sum(1 for item in self.items if item.es_carpeta)
        total_archivos = sum(1 for item in self.items if not item.es_carpeta)
        return total_carpetas, total_archivos
    
    def get_root_project(self):
        """Obtiene el nombre del proyecto raíz"""
        for item in self.items:
            if item.nivel == 0:
                return item.nombre
        return None