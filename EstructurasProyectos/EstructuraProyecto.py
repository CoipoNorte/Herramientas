import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QTreeWidget, QTreeWidgetItem, QFileDialog
from PyQt5.QtCore import Qt

class ProjectOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Folder Organizer")
        self.setGeometry(100, 100, 800, 600)
        
        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Lista de carpetas disponibles
        self.folder_list = QListWidget()
        self.folders = [
            'admin', 'custom', 'models', 'src', 'database', 'images', 'api', 'debug', 'import', 'other', 'app', 'interface',
            'packages', 'archive', 'dist', 'pdf', 'docker', 'audio', 'docs', 'svg', 'base', 'task', 'private',
            'keys', 'batch', 'project', 'temp', 'event', 'layout', 'template', 'examples', 'less', 'public',
            'lib', 'test', 'theme', 'export', 'cart', 'log', 'tools', 'class', 'markdown', 'utils', 'command',
            'messages', 'review', 'robot', 'meta', 'git', 'components', 'config', 'middleware', 'routes', 'video',
            'connection', 'rules', 'views', 'sass', 'mobile', 'console', 'container', 'scripts', 'graphql',
            'content', 'context', 'secure', 'server', 'helper', 'controller', 'webpack', 'home', 'css'
        ]
        
        for folder in self.folders:
            self.folder_list.addItem(folder)

        self.layout.addWidget(QLabel("Drag folders to organize your project structure"))
        self.layout.addWidget(self.folder_list)
        
        # Área de visualización de la estructura
        self.structure_view = QTreeWidget()
        self.structure_view.setHeaderHidden(True)
        self.layout.addWidget(self.structure_view)

        # Botón para guardar la estructura
        self.save_button = QPushButton("Save Structure")
        self.save_button.clicked.connect(self.save_structure)
        self.layout.addWidget(self.save_button)

        # Conectar el drag and drop
        self.folder_list.setDragEnabled(True)
        self.structure_view.setAcceptDrops(True)
        self.structure_view.setDragDropMode(QTreeWidget.InternalMove)

        self.folder_list.itemDoubleClicked.connect(self.add_folder)

    def add_folder(self, item):
        """Agrega una carpeta al árbol de la estructura."""
        folder_name = item.text()
        tree_item = QTreeWidgetItem([folder_name])
        self.structure_view.addTopLevelItem(tree_item)

    def save_structure(self):
        """Genera físicamente la estructura de carpetas en el sistema de archivos."""
        # Abrir un diálogo para seleccionar la ubicación donde se crearán las carpetas
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")

        if folder_path:
            self.create_folders(self.structure_view.invisibleRootItem(), folder_path)
            print("Structure saved successfully!")

    def create_folders(self, tree_item, parent_path):
        """Crea las carpetas recursivamente según la estructura."""
        for i in range(tree_item.childCount()):
            child = tree_item.child(i)
            folder_name = child.text(0)
            folder_path = os.path.join(parent_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            self.create_folders(child, folder_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProjectOrganizer()
    window.show()
    sys.exit(app.exec_())
