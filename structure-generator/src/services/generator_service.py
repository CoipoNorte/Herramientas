import os
from typing import List, Tuple
from models.structure_model import StructureModel

class GeneratorService:
    def create_structure(self, model: StructureModel, ruta_destino: str, texto_original: str) -> Tuple[List[str], str]:
        """Crea la estructura de carpetas y archivos"""
        try:
            rutas_creadas = []
            proyecto_raiz = model.get_root_project()

            for item in model.items:
                ruta_completa = os.path.join(ruta_destino, item.ruta_completa)

                if item.es_carpeta:
                    if not os.path.exists(ruta_completa):
                        os.makedirs(ruta_completa)
                        rutas_creadas.append(f"📁 {item.ruta_completa}/")
                else:
                    directorio = os.path.dirname(ruta_completa)
                    if directorio and not os.path.exists(directorio):
                        os.makedirs(directorio)

                    if not os.path.exists(ruta_completa):
                        with open(ruta_completa, 'w', encoding='utf-8') as f:
                            if item.comentario:
                                f.write(f"// {item.comentario}\n")
                        rutas_creadas.append(f"📄 {item.ruta_completa}")

            # Crear README.md automáticamente
            if proyecto_raiz:
                readme_path = os.path.join(ruta_destino, proyecto_raiz, 'README.md')
                if not any(item.nombre == 'README.md' for item in model.items):
                    with open(readme_path, 'w', encoding='utf-8') as f:
                        f.write(f"# {proyecto_raiz.title()}\n\n")
                        f.write("## Estructura del Proyecto\n\n")
                        f.write("```\n")
                        f.write(texto_original)
                        f.write("\n```\n")
                    rutas_creadas.append(f"📄 {proyecto_raiz}/README.md")

            return rutas_creadas, proyecto_raiz

        except Exception as e:
            raise Exception(f"Error al crear estructura: {str(e)}")