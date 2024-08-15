import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QPushButton, QLineEdit, QCheckBox, QLabel, QMessageBox
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QIcon
from datetime import datetime
import subprocess  # Para abrir la carpeta de forma compatible en distintos sistemas

# Lista de carpetas reservadas del sistema y otras carpetas que queremos ignorar
IGNORED_FOLDERS = ['System Volume Information', '$RECYCLE.BIN', 'Windows', '.git', '__pycache__', 'node_modules']

# Lista de extensiones de archivos de imágenes que queremos ignorar si está marcada la opción
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp']

# Variable global para almacenar el nombre del último archivo generado
last_filename = None

class FileStructureApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Generador de Estructura de Archivos")
        self.setGeometry(100, 100, 400, 200)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'iconos', 'icon.png')))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QWidget {
                background-color: #ffffff;
                border-radius: 10px;
            }
            QLabel {
                font-size: 16px;
                color: #333333;
            }
            QLineEdit {
                border: 2px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit:focus {
                border-color: #007bff;
            }
            QCheckBox {
                font-size: 14px;
                color: #555555;
            }
            QPushButton {
                background-color: #007bff;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin: 5px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004494;
            }
            QMessageBox {
                background-color: #ffffff;
            }
        """)

        # Crear los widgets
        self.create_widgets()

    def create_widgets(self):
        self.label = QLabel("Ruta del directorio:")
        self.layout.addWidget(self.label)

        self.entry = QLineEdit()
        self.layout.addWidget(self.entry)

        self.img_checkbox = QCheckBox("Omitir imágenes")
        self.layout.addWidget(self.img_checkbox)

        self.generate_button = QPushButton("Generar")
        self.generate_button.clicked.connect(self.on_generate)
        self.layout.addWidget(self.generate_button)

        self.copy_button = QPushButton("Copiar")
        self.copy_button.clicked.connect(self.on_copy)
        self.layout.addWidget(self.copy_button)

        self.open_folder_button = QPushButton("Abrir Carpeta")
        self.open_folder_button.clicked.connect(self.open_lecturas_folder)
        self.layout.addWidget(self.open_folder_button)

    def create_lecturas_folder(self):
        """
        Crea la carpeta 'lecturas' en la misma ubicación que el script .py si no existe.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        lecturas_dir = os.path.join(script_dir, 'lecturas')

        if not os.path.exists(lecturas_dir):
            os.makedirs(lecturas_dir)
        
        return lecturas_dir

    def get_next_file_name(self):
        """
        Obtiene el nombre del siguiente archivo .txt basado en el número identificador y la fecha y hora.
        """
        lecturas_dir = self.create_lecturas_folder()
        existing_files = os.listdir(lecturas_dir)
        next_number = len(existing_files) + 1
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        return os.path.join(lecturas_dir, f"{next_number}_{current_time}.txt")

    def generate_ascii_tree(self, root_dir, omit_images=False, prefix='', result=''):
        """
        Genera una representación en ASCII de la estructura de directorios y archivos.
        """
        if not os.path.isdir(root_dir):
            raise ValueError(f"{root_dir} no es un directorio o no existe.")

        entries = sorted(os.listdir(root_dir))
        folders = [entry for entry in entries if os.path.isdir(os.path.join(root_dir, entry)) and entry not in IGNORED_FOLDERS]
        files = [entry for entry in entries if os.path.isfile(os.path.join(root_dir, entry))]

        # Si omit_images está marcado, filtramos los archivos de imagen
        if omit_images:
            files = [file for file in files if not any(file.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)]

        for index, entry in enumerate(folders):
            path = os.path.join(root_dir, entry)
            is_last = index == len(folders) - 1 and not files

            result += f"{prefix}{'└── ' if is_last else '├── '}{entry}/\n"
            new_prefix = f"{prefix}{'    ' if is_last else '│   '}"
            result = self.generate_ascii_tree(path, omit_images, new_prefix, result)

        for index, entry in enumerate(files):
            is_last = index == len(files) - 1
            result += f"{prefix}{'└── ' if is_last else '├── '}{entry}\n"

        return result

    def save_to_file(self, text, filename, root_dir):
        """
        Guarda el texto en un archivo con el nombre del proyecto en la parte superior.
        """
        project_name = os.path.basename(root_dir)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"Proyecto: {project_name}\n")
            file.write("=" * (len(project_name) + 10) + "\n")
            file.write(text)

    def open_lecturas_folder(self):
        """
        Abre la carpeta de 'lecturas' donde se guardan los archivos.
        """
        lecturas_dir = self.create_lecturas_folder()
        if os.name == 'nt':  # Si el sistema operativo es Windows
            os.startfile(lecturas_dir)
        elif os.name == 'posix':  # Si es Linux o macOS
            subprocess.run(['xdg-open', lecturas_dir])
        else:
            QMessageBox.critical(self, "Error", "No se puede abrir la carpeta en este sistema operativo.")

    def on_generate(self):
        """
        Maneja el evento de clic en el botón "Generar".
        """
        global last_filename
        path = self.entry.text()
        if not path:
            QMessageBox.critical(self, "Error", "Por favor, ingrese una ruta.")
            return
        
        omit_images = self.img_checkbox.isChecked()  # Verifica si la casilla "Omitir imágenes" está marcada
        
        try:
            result = self.generate_ascii_tree(path, omit_images)
            last_filename = self.get_next_file_name()  # Actualiza la variable global con el nombre del archivo generado
            self.save_to_file(result, last_filename, path)
            QMessageBox.information(self, "Éxito", f"Estructura guardada en: {last_filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def on_copy(self):
        """
        Maneja el evento de clic en el botón "Copiar".
        Copia el contenido del último archivo generado.
        """
        if not last_filename:
            QMessageBox.critical(self, "Error", "No se ha generado ninguna lectura aún.")
            return

        try:
            with open(last_filename, 'r', encoding='utf-8') as file:
                text = file.read()
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            QMessageBox.information(self, "Éxito", "Lectura copiada al portapapeles.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileStructureApp()
    window.show()
    sys.exit(app.exec_())
