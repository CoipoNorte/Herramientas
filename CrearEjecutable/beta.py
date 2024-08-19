import os
import sys
import shutil
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QMessageBox, QFileDialog

class ExecutableCreator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Generador de Ejecutables")
        self.setGeometry(100, 100, 500, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Crear los widgets
        self.create_widgets()

    def create_widgets(self):
        self.project_label = QLabel("Ruta del proyecto:")
        self.layout.addWidget(self.project_label)

        self.project_entry = QLineEdit()
        self.layout.addWidget(self.project_entry)

        self.select_project_button = QPushButton("Seleccionar Proyecto")
        self.select_project_button.clicked.connect(self.select_project_path)
        self.layout.addWidget(self.select_project_button)

        self.main_script_label = QLabel("Archivo principal:")
        self.layout.addWidget(self.main_script_label)

        self.main_script_entry = QLineEdit()
        self.layout.addWidget(self.main_script_entry)

        self.select_script_button = QPushButton("Seleccionar Archivo Principal")
        self.select_script_button.clicked.connect(self.select_main_script)
        self.layout.addWidget(self.select_script_button)

        self.generate_button = QPushButton("Generar Ejecutable")
        self.generate_button.clicked.connect(self.on_generate)
        self.layout.addWidget(self.generate_button)

    def select_project_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta del Proyecto")
        if folder_path:
            self.project_entry.setText(folder_path)
            self.main_script_entry.clear()  # Limpiar el campo de archivo principal

    def select_main_script(self):
        project_path = self.project_entry.text()
        if not project_path:
            QMessageBox.critical(self, "Error", "Por favor, seleccione una ruta de proyecto primero.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo Principal", project_path, "Python Files (*.py);;All Files (*)")
        if file_path:
            self.main_script_entry.setText(file_path)

    def on_generate(self):
        project_path = self.project_entry.text()
        main_script = self.main_script_entry.text()

        if not project_path or not main_script:
            QMessageBox.critical(self, "Error", "Por favor, ingrese todos los campos.")
            return

        if not os.path.isfile(main_script):
            QMessageBox.critical(self, "Error", "El archivo principal no existe en la ruta proporcionada.")
            return

        # Crear una carpeta 'builds' en la misma ubicación que este script
        builds_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'builds')
        if not os.path.exists(builds_dir):
            os.makedirs(builds_dir)

        # Configurar el comando de PyInstaller
        command = [
            'pyinstaller',
            '--onefile',  # Crea un solo archivo ejecutable
            '--noconsole',  # No abre la consola al ejecutar el .exe (opcional, depende de tu aplicación)
            '--distpath', builds_dir,  # Carpeta para los ejecutables generados
            '--workpath', os.path.join(builds_dir, 'build'),  # Carpeta temporal de trabajo
            '--specpath', os.path.join(builds_dir, 'spec')  # Carpeta para el archivo .spec generado
        ]

        # Verificar si existe un archivo de ícono y agregar al comando si existe
        icon_path = os.path.join(project_path, 'icon.png')
        if os.path.isfile(icon_path):
            command += ['--icon', icon_path]

        # Detectar archivos adicionales en la carpeta del proyecto y agregarlos al comando
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith('.png') or file.endswith('.txt'):  # Puedes agregar más extensiones si es necesario
                    source_path = os.path.join(root, file)
                    relative_path = os.path.relpath(source_path, project_path)
                    command += [f'--add-data={source_path};{relative_path}']

        command.append(main_script)

        try:
            # Ejecutar el comando
            print(f"Ejecutando comando: {' '.join(command)}")  # Para depuración
            subprocess.run(command, check=True)

            # Eliminar archivos temporales generados por PyInstaller
            self.clean_builds_dir(builds_dir)

            QMessageBox.information(self, "Éxito", f"El ejecutable ha sido generado exitosamente en la carpeta 'builds'.")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Error al generar el ejecutable: {e}\n\nComando: {' '.join(command)}")

    def clean_builds_dir(self, builds_dir):
        """
        Elimina los archivos temporales generados por PyInstaller, dejando solo el ejecutable.
        """
        dist_dir = os.path.join(builds_dir, 'dist')
        if os.path.exists(dist_dir):
            for item in os.listdir(dist_dir):
                item_path = os.path.join(dist_dir, item)
                if os.path.isfile(item_path):
                    shutil.move(item_path, builds_dir)  # Mover el ejecutable a la carpeta 'builds'
            os.rmdir(dist_dir)

        # Eliminar carpetas de trabajo y especificaciones
        for folder in ['build', 'spec']:
            folder_path = os.path.join(builds_dir, folder)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExecutableCreator()
    window.show()
    sys.exit(app.exec_())
