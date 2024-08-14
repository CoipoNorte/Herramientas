import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QSplitter, QListWidget, QTextEdit, QSizePolicy,
    QFrame, QListWidgetItem, QMessageBox, QInputDialog, QMenu, QAction
)
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

class DraggableListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def startDrag(self, supportedActions):
        drag = QDrag(self)
        mimeData = QMimeData()
        mimeData.setText(self.currentItem().text())
        drag.setMimeData(mimeData)
        drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            item_text = event.mimeData().text()
            item = QListWidgetItem(item_text)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.addItem(item)
            event.accept()
        else:
            event.ignore()

    def show_context_menu(self, pos):
        menu = QMenu(self)
        create_action = QAction('Crear', self)
        rename_action = QAction('Renombrar', self)
        delete_action = QAction('Eliminar', self)
        
        create_action.triggered.connect(self.create_item)
        rename_action.triggered.connect(self.rename_item)
        delete_action.triggered.connect(self.delete_item)
        
        menu.addAction(create_action)
        menu.addAction(rename_action)
        menu.addAction(delete_action)
        
        menu.exec_(self.viewport().mapToGlobal(pos))

    def create_item(self):
        text, ok = QInputDialog.getText(self, 'Crear Elemento', 'Ingrese el nombre del nuevo elemento:')
        if ok and text:
            item = QListWidgetItem(text)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.addItem(item)

    def rename_item(self):
        selected_item = self.currentItem()
        if selected_item:
            text, ok = QInputDialog.getText(self, 'Renombrar Elemento', 'Ingrese el nuevo nombre:')
            if ok and text:
                selected_item.setText(text)
        else:
            QMessageBox.warning(self, 'Error', 'Seleccione un elemento para renombrar.')

    def delete_item(self):
        selected_item = self.currentItem()
        if selected_item:
            self.takeItem(self.row(selected_item))
        else:
            QMessageBox.warning(self, 'Error', 'Seleccione un elemento para eliminar.')

class ProjectOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Project Organizer')
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        header_layout = QHBoxLayout()
        main_layout.addLayout(header_layout)

        self.title_field = QTextEdit()
        self.title_field.setPlaceholderText('Campo para el Título')
        self.title_field.setFixedHeight(30)

        generate_button = QPushButton('Generar Proyecto')
        generate_button.clicked.connect(self.generate_project)

        header_layout.addWidget(self.title_field)
        header_layout.addWidget(generate_button)

        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter)

        self.left_panel = QFrame()
        self.left_panel.setFrameShape(QFrame.StyledPanel)
        left_layout = QVBoxLayout(self.left_panel)

        self.source_list = DraggableListWidget(self)
        self.source_list.addItems([
            'src/', 'assets/', 'index.html', 'css/', 'js/', 'images/'
        ])
        left_layout.addWidget(self.source_list)

        self.right_panel = QFrame()
        self.right_panel.setFrameShape(QFrame.StyledPanel)
        right_layout = QVBoxLayout(self.right_panel)

        self.project_buttons = QVBoxLayout()
        self.project_buttons.addWidget(QPushButton('Vanilla JavaScript', self, clicked=self.add_vanilla_js_structure))
        self.project_buttons.addWidget(QPushButton('PHP', self, clicked=self.add_php_structure))
        self.project_buttons.addWidget(QPushButton('Python', self, clicked=self.add_python_structure))
        self.project_buttons.addWidget(QPushButton('C++', self, clicked=self.add_cpp_structure))
        self.project_buttons.addWidget(QPushButton('Java', self, clicked=self.add_java_structure))
        self.project_buttons.addWidget(QPushButton('TypeScript', self, clicked=self.add_typescript_structure))
        self.project_buttons.addWidget(QPushButton('CSS/HTML', self, clicked=self.add_css_html_structure))
        self.project_buttons.addWidget(QPushButton('MVC', self, clicked=self.add_mvc_structure))
        self.project_buttons.addWidget(QPushButton('Arquitectura Hexagonal', self, clicked=self.add_hexagonal_structure))

        right_layout.addLayout(self.project_buttons)

        self.workspace = DraggableListWidget()
        self.workspace.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.workspace)
        self.splitter.addWidget(self.right_panel)

    def clear_workspace(self):
        # No borra el contenido del área de trabajo en este método
        pass

    def generate_project(self):
        title = self.title_field.toPlainText().strip()
        if title:
            self.print_workspace_content(title)  # Imprime el nombre del proyecto y el contenido del área de trabajo
            self.create_folders(title)
        else:
            QMessageBox.warning(self, 'Error', 'Por favor, ingrese un título.')

    def print_workspace_content(self, title):
        print(f"Nombre del Proyecto: {title}")
        print("Contenido del área de trabajo:")
        for index in range(self.workspace.count()):
            item_text = self.workspace.item(index).text().strip()
            print(f' - {item_text}')

    def create_folders(self, root_folder_name):
        base_path = os.path.join(os.getcwd(), root_folder_name)

        # Eliminar la carpeta raíz si ya existe y recrearla
        if os.path.exists(base_path):
            for root, dirs, files in os.walk(base_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(base_path)
        
        os.makedirs(base_path)

        # Crear las carpetas desde el área de trabajo
        for index in range(self.workspace.count()):
            item_text = self.workspace.item(index).text().strip()
            if item_text:
                folder_name = item_text.rstrip('/')  # Quitar el '/' al final si está presente
                path = os.path.join(base_path, folder_name)
                if not os.path.exists(path):
                    os.makedirs(path)

        QMessageBox.information(self, 'Éxito', f'Proyecto "{root_folder_name}" generado exitosamente.')

    def add_structure(self, structure_lines):
        self.clear_workspace()
        for line in structure_lines:
            if line.strip():
                item = QListWidgetItem(line.strip())
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.workspace.addItem(item)

    def add_vanilla_js_structure(self):
        self.add_structure([
            'src/',
            'dist/',
            'assets/',
            'index.html'
        ])

    def add_php_structure(self):
        self.add_structure([
            'public/',
            'src/',
            'config/',
            'tests/'
        ])

    def add_python_structure(self):
        self.add_structure([
            'project_name/',
            'tests/',
            'docs/',
            'requirements.txt'
        ])

    def add_cpp_structure(self):
        self.add_structure([
            'src/',
            'include/',
            'lib/',
            'build/'
        ])

    def add_java_structure(self):
        self.add_structure([
            'src/main/java/',
            'src/main/resources/',
            'test/',
            'target/'
        ])

    def add_typescript_structure(self):
        self.add_structure([
            'src/',
            'dist/',
            'types/',
            'tests/'
        ])

    def add_css_html_structure(self):
        self.add_structure([
            'css/',
            'js/',
            'images/',
            'index.html'
        ])

    def add_mvc_structure(self):
        self.add_structure([
            'models/',
            'views/',
            'controllers/',
            'public/'
        ])

    def add_hexagonal_structure(self):
        self.add_structure([
            'application/',
            'domain/',
            'infrastructure/',
            'interfaces/'
        ])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProjectOrganizer()
    window.show()
    sys.exit(app.exec_())
