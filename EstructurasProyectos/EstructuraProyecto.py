import sys
import os
import shutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QSplitter, QTreeWidget, QTreeWidgetItem,
                             QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit,
                             QMenu, QAction, QInputDialog, QFileDialog)
from PyQt5.QtCore import Qt

class DragDropProjectOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Organizador de Proyectos")
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Main layout
        main_layout = QVBoxLayout(self.central_widget)

        # Top layout (for project name and generate button)
        top_layout = QHBoxLayout()
        self.project_name_input = QLineEdit(self)
        self.project_name_input.setPlaceholderText("Nombre del Proyecto")
        self.generate_button = QPushButton("Generar", self)
        self.generate_button.clicked.connect(self.generate_project_structure)
        top_layout.addWidget(self.project_name_input)
        top_layout.addWidget(self.generate_button)
        main_layout.addLayout(top_layout)

        # Splitter for left panel (categories), central panel (workspace), and right panel (structures)
        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter)

        # Panel Izquierdo (Categories)
        self.categories_panel = QTreeWidget()
        self.categories_panel.setHeaderLabel("Categorías de Carpetas")
        self.categories_panel.setDragEnabled(True)  # Enable dragging items
        self.categories_panel.setDragDropMode(QTreeWidget.DragOnly)
        self.categories_panel.setAcceptDrops(True)
        self.categories_panel.setDropIndicatorShown(True)

        # Adding categories
        categories = {
            "Código fuente y lógica de la aplicación": ["src/", "app/", "lib/", "components/", "utils/", "helpers/", "controllers/", "models/", "services/"],
            "Recursos y assets": ["assets/", "images/", "audio/", "video/", "fonts/", "svg/"],
            "Estilos": ["css/", "sass/", "less/"],
            "Documentación": ["docs/", "markdown/"],
            "Configuración": ["config/", ".git/", "docker/"],
            "Scripts y herramientas": ["scripts/", "tools/"],
            "Pruebas": ["tests/", "spec/"],
            "Datos": ["data/", "database/"],
            "Salida compilada/construida": ["dist/", "build/"],
            "Servidor y API": ["server/", "api/"],
            "Rutas y middleware": ["routes/", "middleware/"],
            "Interfaz de usuario": ["views/", "templates/", "layouts/"],
            "Contenido estático": ["public/", "static/"],
            "Seguridad": ["secure/", "keys/"],
            "Temporales y caché": ["temp/", "cache/"],
            "Logs": ["logs/"],
            "Internacionalización": ["lang/", "locales/"],
            "Ejemplos y demos": ["examples/", "demo/"]
        }
        
        for category, items in categories.items():
            cat_item = QTreeWidgetItem(self.categories_panel, [category])
            for item in items:
                QTreeWidgetItem(cat_item, [item])
        
        self.splitter.addWidget(self.categories_panel)

        # Panel Central (Workspace)
        self.workspace = QTreeWidget()
        self.workspace.setHeaderLabel("Área de Trabajo")
        self.workspace.setDragEnabled(True)
        self.workspace.setAcceptDrops(True)
        self.workspace.setDropIndicatorShown(True)
        self.workspace.setDragDropMode(QTreeWidget.InternalMove)
        self.workspace.setContextMenuPolicy(Qt.CustomContextMenu)
        self.workspace.customContextMenuRequested.connect(self.show_context_menu)
        self.splitter.addWidget(self.workspace)

        # Panel Derecho (Structures)
        self.structures_panel = QVBoxLayout()
        self.structures_buttons = {
            "Vanilla JS": ["src", "dist", "assets", "index.html"],
            "PHP": ["public", "src", "config", "tests"],
            "Python": ["src", "tests", "docs", "requirements.txt"],
            "C++": ["src", "include", "lib", "build"],
            "Java": ["src/main/java", "src/main/resources", "test", "target"],
            "TypeScript": ["src", "dist", "types", "tests"],
            "CSS/HTML": ["css", "js", "images", "index.html"],
            "MVC": ["models", "views", "controllers", "public"],
            "Arquitectura Hexagonal": ["application", "domain", "infrastructure", "interfaces"]
        }
        for structure_name in self.structures_buttons:
            button = QPushButton(structure_name, self)
            button.clicked.connect(lambda checked, b=structure_name: self.add_structure_to_workspace(b))
            self.structures_panel.addWidget(button)

        right_panel = QWidget()
        right_panel.setLayout(self.structures_panel)
        self.splitter.addWidget(right_panel)

        # Panel Inferior Derecho (Action buttons)
        self.action_buttons = QHBoxLayout()
        self.create_folder_button = QPushButton("Crear Carpeta", self)
        self.rename_folder_button = QPushButton("Renombrar Carpeta", self)
        self.delete_folder_button = QPushButton("Eliminar Carpeta", self)
        self.create_folder_button.clicked.connect(self.create_folder)
        self.rename_folder_button.clicked.connect(self.rename_folder)
        self.delete_folder_button.clicked.connect(self.delete_folder)
        self.action_buttons.addWidget(self.create_folder_button)
        self.action_buttons.addWidget(self.rename_folder_button)
        self.action_buttons.addWidget(self.delete_folder_button)
        main_layout.addLayout(self.action_buttons)

    def add_structure_to_workspace(self, structure_name):
        # Clear workspace
        self.workspace.clear()

        # Add the selected structure to the workspace
        if structure_name in self.structures_buttons:
            for item in self.structures_buttons[structure_name]:
                if '.' in item:
                    # It's a file
                    item = QTreeWidgetItem(self.workspace, [item])
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                else:
                    # It's a folder
                    self.create_folders([item], self.workspace.invisibleRootItem())

    def generate_project_structure(self):
        # Obtener el nombre del proyecto y validarlo
        project_name = self.project_name_input.text().strip()
        if not project_name:
            project_name = "mi proyecto"

        # Abrir diálogo de selección de carpeta para crear el proyecto
        project_location = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Proyecto", "")

        if not project_location:
            return

        # Crear carpeta raíz del proyecto con el nombre del proyecto
        project_root = os.path.join(project_location, project_name)

        # Si ya existe la carpeta, eliminarla
        if os.path.exists(project_root):
            shutil.rmtree(project_root)

        # Crear la nueva estructura de carpetas dentro de la carpeta raíz
        os.makedirs(project_root, exist_ok=True)

        # Crear la estructura de carpetas desde el área de trabajo
        self.create_folders_from_workspace(project_root)

    def create_folders(self, folder_list, parent_item):
        # Correctamente crea la estructura en el área de trabajo
        for folder in folder_list:
            child_item = QTreeWidgetItem(parent_item, [folder])
            child_item.setFlags(child_item.flags() | Qt.ItemIsEditable)
            if '.' in folder:
                # Es un archivo
                self.create_file(os.path.join(self.workspace.invisibleRootItem().text(0), folder))
            else:
                # Es una carpeta
                self.create_folders([], child_item)

    def create_folders_from_workspace(self, base_path):
        def create_from_item(item, parent_path):
            folder_name = item.text(0)
            folder_path = os.path.join(parent_path, folder_name)
            if '.' in folder_name:
                # Es un archivo
                self.create_file(folder_path)
            else:
                # Es una carpeta
                os.makedirs(folder_path, exist_ok=True)
                for i in range(item.childCount()):
                    create_from_item(item.child(i), folder_path)

        # Comenzar la creación desde el área de trabajo
        create_from_item(self.workspace.invisibleRootItem(), base_path)

    def create_file(self, file_path):
        # Crear archivo vacío
        try:
            with open(file_path, 'w') as file:
                pass
        except Exception as e:
            print(f"No se pudo crear el archivo {file_path}: {e}")

    def create_folder(self):
        # Crear una nueva carpeta en el área de trabajo
        selected_item = self.workspace.currentItem()
        if selected_item:
            folder_name, ok = QInputDialog.getText(self, "Nueva Carpeta", "Nombre de la carpeta:", text="nueva_carpeta")
            if ok and folder_name:
                folder_path = os.path.join(self.get_item_path(selected_item), folder_name)
                os.makedirs(folder_path, exist_ok=True)
                self.create_folders([folder_name], selected_item)

    def rename_folder(self):
        # Renombrar la carpeta seleccionada
        selected_item = self.workspace.currentItem()
        if selected_item:
            new_name, ok = QInputDialog.getText(self, "Renombrar Carpeta", "Nuevo nombre:", text=selected_item.text(0))
            if ok and new_name:
                parent_item = selected_item.parent()
                old_path = self.get_item_path(selected_item)
                new_path = os.path.join(os.path.dirname(old_path), new_name)
                os.rename(old_path, new_path)
                selected_item.setText(0, new_name)

    def delete_folder(self):
        # Eliminar la carpeta seleccionada
        selected_item = self.workspace.currentItem()
        if selected_item:
            folder_path = self.get_item_path(selected_item)
            if os.path.isdir(folder_path):
                shutil.rmtree(folder_path)
            elif os.path.isfile(folder_path):
                os.remove(folder_path)
            index = selected_item.parent().indexOfChild(selected_item) if selected_item.parent() else self.workspace.indexOfTopLevelItem(selected_item)
            if index != -1:
                if selected_item.parent():
                    selected_item.parent().removeChild(selected_item)
                else:
                    self.workspace.takeTopLevelItem(index)

    def get_item_path(self, item):
        path_parts = []
        while item:
            path_parts.append(item.text(0))
            item = item.parent()
        return os.path.join(*reversed(path_parts))

    def show_context_menu(self, pos):
        context_menu = QMenu(self)
        
        # Opciones que deseas mantener en el menú contextual
        new_folder_action = QAction("Nueva Carpeta", self)
        rename_folder_action = QAction("Cambiar Nombre", self)
        delete_action = QAction("Eliminar Carpeta", self)
        
        # Conectar las acciones a los métodos correspondientes
        new_folder_action.triggered.connect(self.create_folder_from_context_menu)
        rename_folder_action.triggered.connect(self.rename_folder_from_context_menu)
        delete_action.triggered.connect(self.delete_folder_from_context_menu)
        
        # Agregar acciones al menú contextual
        context_menu.addAction(new_folder_action)
        context_menu.addAction(rename_folder_action)
        context_menu.addAction(delete_action)
        
        # Mostrar el menú contextual en la posición del clic
        context_menu.exec_(self.workspace.viewport().mapToGlobal(pos))

    def create_folder_from_context_menu(self):
        selected_item = self.workspace.currentItem()
        if selected_item:
            folder_name, ok = QInputDialog.getText(self, "Nueva Carpeta", "Nombre de la carpeta:", text="nueva_carpeta")
            if ok and folder_name:
                folder_path = os.path.join(self.get_item_path(selected_item), folder_name)
                os.makedirs(folder_path, exist_ok=True)
                self.create_folders([folder_name], selected_item)

    def rename_folder_from_context_menu(self):
        selected_item = self.workspace.currentItem()
        if selected_item:
            new_name, ok = QInputDialog.getText(self, "Cambiar Nombre", "Nuevo nombre:", text=selected_item.text(0))
            if ok and new_name:
                parent_item = selected_item.parent()
                old_path = self.get_item_path(selected_item)
                new_path = os.path.join(os.path.dirname(old_path), new_name)
                os.rename(old_path, new_path)
                selected_item.setText(0, new_name)

    def delete_folder_from_context_menu(self):
        selected_item = self.workspace.currentItem()
        if selected_item:
            folder_path = self.get_item_path(selected_item)
            if os.path.isdir(folder_path):
                shutil.rmtree(folder_path)
            elif os.path.isfile(folder_path):
                os.remove(folder_path)
            index = selected_item.parent().indexOfChild(selected_item) if selected_item.parent() else self.workspace.indexOfTopLevelItem(selected_item)
            if index != -1:
                if selected_item.parent():
                    selected_item.parent().removeChild(selected_item)
                else:
                    self.workspace.takeTopLevelItem(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DragDropProjectOrganizer()
    window.show()
    sys.exit(app.exec_())
