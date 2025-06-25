import re
import os
from typing import List, Dict

class ParserService:
    @staticmethod
    def parse_structure(texto: str) -> List[Dict]:
        """Parsea la estructura usando indentación real"""
        lineas = texto.strip().split('\n')
        estructura = []
        stack_padres = []

        for linea in lineas:
            if not linea.strip():
                continue

            # Calcular indentación real
            contenido_match = re.search(r'[^│├└─\s]', linea)
            if not contenido_match:
                continue

            indentacion = contenido_match.start()
            contenido = linea[indentacion:].strip()

            if not contenido:
                continue

            # Separar nombre del comentario
            if '#' in contenido:
                nombre_parte = contenido.split('#')[0].strip()
                comentario = contenido.split('#')[1].strip()
            else:
                nombre_parte = contenido
                comentario = ""

            # Determinar si es carpeta
            es_carpeta = nombre_parte.endswith('/')
            nombre = nombre_parte.rstrip('/')

            if not nombre:
                continue

            # Calcular nivel
            nivel = indentacion // 4

            # Ajustar stack
            while len(stack_padres) > nivel:
                stack_padres.pop()

            # Construir ruta
            if nivel == 0:
                ruta_completa = nombre
                stack_padres = [nombre]
            else:
                ruta_completa = os.path.join(*stack_padres, nombre)
                if es_carpeta:
                    stack_padres.append(nombre)

            estructura.append({
                'nombre': nombre,
                'ruta_completa': ruta_completa,
                'nivel': nivel,
                'es_carpeta': es_carpeta,
                'comentario': comentario
            })

        return estructura