import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QInputDialog, QTextEdit, QHBoxLayout
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Comandos con PyQt5')
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Layouts para botones
        self.system_buttons_layout = QVBoxLayout()
        self.react_buttons_layout = QVBoxLayout()

        # Label para mostrar la carpeta seleccionada
        self.folder_label = QLabel('Carpeta no seleccionada', self)
        self.layout.addWidget(self.folder_label)

        # Botón para seleccionar carpeta
        self.select_folder_button = QPushButton('Seleccionar Carpeta', self)
        self.select_folder_button.clicked.connect(self.select_folder)
        self.layout.addWidget(self.select_folder_button)

        # Agregar secciones de botones al diseño principal
        self.layout.addLayout(self.system_buttons_layout)
        self.layout.addLayout(self.react_buttons_layout)

        # Agregar botones al layout de comandos del sistema
        self.create_button('cd', 'cd', False, self.system_buttons_layout)
        self.create_button('dir', 'dir', False, self.system_buttons_layout)
        self.create_button('mkdir', 'mkdir', True, self.system_buttons_layout)
        self.create_button('cls', 'cls', False, self.system_buttons_layout)
        
        # Agregar botones al layout de comandos de React
        self.create_button('npm install react-scripts@2.1.8', 'npm install react-scripts@2.1.8', False, self.react_buttons_layout)
        self.create_button('node -v', 'node -v', False, self.react_buttons_layout)
        self.create_button('npm -v', 'npm -v', False, self.react_buttons_layout)
        self.create_button('npm install -g create-react-app', 'npm install -g create-react-app', False, self.react_buttons_layout)
        self.create_button('npx create-react-app', 'npx create-react-app', True, self.react_buttons_layout)
        self.create_button('npm start', 'npm start', False, self.react_buttons_layout)

        # Área de texto para la salida de la terminal
        self.terminal_output = QTextEdit(self)
        self.terminal_output.setReadOnly(True)
        self.layout.addWidget(self.terminal_output)

    def create_button(self, text, command, needs_input, layout):
        button = QPushButton(text, self)
        button.setStyleSheet("background-color: lightblue; border-radius: 10px; padding: 10px;")
        if needs_input:
            button.clicked.connect(lambda: self.execute_command_with_input(command))
        else:
            button.clicked.connect(lambda: self.execute_command(command))
        layout.addWidget(button)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Seleccionar Carpeta')
        if folder:
            self.folder_label.setText(f'Carpeta seleccionada: {folder}')
            self.selected_folder = folder

    def execute_command(self, command):
        if not hasattr(self, 'selected_folder'):
            self.folder_label.setText('Por favor, selecciona una carpeta primero.')
            return

        # Construir el comando completo
        full_command = f'cd {self.selected_folder} && {command}'
        process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        self.terminal_output.append(f'$ {full_command}')
        if stdout:
            self.terminal_output.append(stdout)
        if stderr:
            self.terminal_output.append(stderr)

    def execute_command_with_input(self, command):
        if not hasattr(self, 'selected_folder'):
            self.folder_label.setText('Por favor, selecciona una carpeta primero.')
            return

        # Pedir al usuario que ingrese el texto del comando
        text, ok = QInputDialog.getText(self, 'Ingresar Comando', f'Ingrese los argumentos para {command}:')
        if not ok or not text:
            self.folder_label.setText('Comando cancelado o vacío.')
            return

        # Construir el comando completo
        full_command = f'cd {self.selected_folder} && {command} {text}'
        process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        self.terminal_output.append(f'$ {full_command}')
        if stdout:
            self.terminal_output.append(stdout)
        if stderr:
            self.terminal_output.append(stderr)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
