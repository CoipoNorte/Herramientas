# Caracteres especiales para el árbol
TREE_CHARACTERS = [
    ("├── ", "├── Rama"),
    ("└── ", "└── Final"),
    ("│   ", "│ Línea"),
    ("    ", "Indent"),
    ("/", "/ Carpeta"),
    ("# ", "# Comentario")
]

# Colores de botones
BUTTON_COLORS = {
    "generate": {"fg": "#2e7d32", "hover": "#1b5e20"},
    "save_load": {"fg": "#4a148c", "hover": "#6a0dad"},
    "template": {"fg": "#8a2be2", "hover": "#6a0dad"},
    "clear": {"fg": "red", "hover": "darkred"}
}

# Extensión de archivos
PROJECT_EXTENSION = ".folderstruct"