import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QTabWidget, QHBoxLayout, QPushButton,
    QTreeWidget, QTreeWidgetItem, QSplitter, QTextEdit,
    QFileDialog, QMessageBox, QTreeView, QListView, QAbstractItemView, QStyle
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush, QDragEnterEvent, QDropEvent, QIcon
import shutil
import subprocess
import time
import threading

class DeveloperWorkspace(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Starting initialization...")
        
        # Define theme colors
        self.colors = {
            'background': '#1a2f2f',    # Dark emerald background
            'secondary_bg': '#244242',   # Lighter emerald for contrast
            'accent': '#32CD32',         # Bright emerald green
            'highlight': '#FFD700',      # Golden yellow
            'text': '#FFFFFF',           # White text
            'secondary_text': '#B0B0B0'  # Light gray text
        }
        
        # Initialize workspace directories
        self.init_workspace()
        
        # Basic window setup
        self.setWindowTitle("Developer Workspace")
        self.resize(1200, 800)
        
        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        # Create basic tabs
        self.create_ubif_tab()
        self.create_html_tab()
        self.create_chrome_tab()
        self.create_python_scripts_tab()
        self.create_python_apps_tab()
        self.create_batch_scripts_tab()
        self.create_powershell_apps_tab()
        self.create_readme_tab()
        
        # Apply theme
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {self.colors['background']};
                color: {self.colors['text']};
            }}
            QTabBar::tab {{
                background: {self.colors['secondary_bg']};
                color: {self.colors['text']};
                padding: 10px 25px;
                border: none;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background: {self.colors['accent']};
            }}
            QPushButton {{
                background-color: {self.colors['secondary_bg']};
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                margin: 2px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['accent']};
            }}
            QTreeWidget {{
                background-color: {self.colors['secondary_bg']};
                border: none;
                padding: 5px;
            }}
            QTextEdit {{
                background-color: {self.colors['secondary_bg']};
                color: {self.colors['text']};
                border: none;
                padding: 5px;
            }}
        """)
        
        print("Initialization complete")

    def init_workspace(self):
        """Initialize workspace directories in Documents folder"""
        documents_dir = os.path.expanduser("~/Documents")
        self.workspace_dir = os.path.join(documents_dir, "DeveloperWorkspace")
        
        # Define project directories
        self.dirs = {
            'ubif': os.path.join(self.workspace_dir, "UBIF_Projects"),
            'html': os.path.join(self.workspace_dir, "HTML_Projects"),
            'chrome': os.path.join(self.workspace_dir, "Chrome_Extensions"),
            'scripts': os.path.join(self.workspace_dir, "Python_Scripts"),
            'apps': os.path.join(self.workspace_dir, "Python_Apps"),
            'batch': os.path.join(self.workspace_dir, "Batch_Scripts"),
            'powershell': os.path.join(self.workspace_dir, "PowerShell_Apps")
        }
        
        # Create directories if they don't exist
        for dir_path in self.dirs.values():
            os.makedirs(dir_path, exist_ok=True)
            print(f"Initialized directory: {dir_path}")

    def create_ubif_tab(self):
        """Create UBIF tab"""
        print("Creating UBIF tab...")
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Toolbar
        toolbar = QHBoxLayout()
        new_project_btn = QPushButton("New Project")
        browse_btn = QPushButton("Browse...")
        save_btn = QPushButton("Save")
        move_to_projects_btn = QPushButton("Move to Projects")
        run_btn = QPushButton("Run")
        
        toolbar.addWidget(new_project_btn)
        toolbar.addWidget(browse_btn)
        toolbar.addWidget(save_btn)
        toolbar.addWidget(move_to_projects_btn)
        toolbar.addWidget(run_btn)
        toolbar.addStretch()
        
        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Project tree
        self.ubif_tree = QTreeWidget()
        self.ubif_tree.setHeaderLabels(["UBIF Projects"])
        self.ubif_tree.setAcceptDrops(True)
        self.load_projects(self.ubif_tree, self.dirs['ubif'])
        
        # Add double-click handler
        self.ubif_tree.itemDoubleClicked.connect(lambda item: self.run_ubif_project())
        
        # Editor
        self.ubif_editor = QTextEdit()
        
        # Add widgets to splitter
        splitter.addWidget(self.ubif_tree)
        splitter.addWidget(self.ubif_editor)
        
        layout.addLayout(toolbar)
        layout.addWidget(splitter)
        self.tabs.addTab(tab, "UBIF")
        
        # Connect signals
        self.ubif_tree.itemClicked.connect(lambda item: self.load_file(item.text(0), 'ubif'))
        save_btn.clicked.connect(lambda: self.save_file('ubif'))
        browse_btn.clicked.connect(lambda: self.browse_directory('ubif'))
        move_to_projects_btn.clicked.connect(lambda: self.move_selected_to_projects('ubif'))
        new_project_btn.clicked.connect(lambda: self.new_file('ubif'))
        run_btn.clicked.connect(self.run_ubif_project)

    def create_html_tab(self):
        print("Creating HTML tab...")
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Toolbar
        toolbar = QHBoxLayout()
        new_project_btn = QPushButton("New Project")
        browse_btn = QPushButton("Browse...")
        save_btn = QPushButton("Save")
        move_to_projects_btn = QPushButton("Move to Projects")
        run_btn = QPushButton("Run")
        
        toolbar.addWidget(new_project_btn)
        toolbar.addWidget(browse_btn)
        toolbar.addWidget(save_btn)
        toolbar.addWidget(move_to_projects_btn)
        toolbar.addWidget(run_btn)
        toolbar.addStretch()
        
        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Project tree
        self.html_tree = QTreeWidget()
        self.html_tree.setHeaderLabels(["HTML Projects"])
        self.html_tree.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        self.load_projects(self.html_tree, self.dirs['html'])
        
        # Add double-click handler
        self.html_tree.itemDoubleClicked.connect(lambda item: self.run_html_file())
        
        # Connect item clicked signal with error handling
        def safe_item_clicked(item):
            try:
                print(f"Item clicked: {item.text(0)}")
                self.load_file(item.text(0), 'html')
            except Exception as e:
                print(f"Error handling item click: {e}")
                QMessageBox.warning(self, "Error", f"Error selecting item: {str(e)}")
        
        self.html_tree.itemClicked.connect(safe_item_clicked)
        
        # Editor
        self.html_editor = QTextEdit()
        
        # Add widgets to splitter
        splitter.addWidget(self.html_tree)
        splitter.addWidget(self.html_editor)
        
        layout.addLayout(toolbar)
        layout.addWidget(splitter)
        self.tabs.addTab(tab, "HTML")
        
        # Connect other signals
        save_btn.clicked.connect(lambda: self.save_file('html'))
        browse_btn.clicked.connect(lambda: self.browse_directory('html'))
        move_to_projects_btn.clicked.connect(lambda: self.move_selected_to_projects('html'))
        run_btn.clicked.connect(self.run_html_file)

    def create_chrome_tab(self):
        print("Creating Chrome Extensions tab...")
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Toolbar
        toolbar = QHBoxLayout()
        new_project_btn = QPushButton("New Project")
        browse_btn = QPushButton("Browse...")
        save_btn = QPushButton("Save")
        move_to_projects_btn = QPushButton("Move to Projects")
        run_btn = QPushButton("Run")
        
        toolbar.addWidget(new_project_btn)
        toolbar.addWidget(browse_btn)
        toolbar.addWidget(save_btn)
        toolbar.addWidget(move_to_projects_btn)
        toolbar.addWidget(run_btn)
        toolbar.addStretch()
        
        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Project tree
        self.chrome_tree = QTreeWidget()
        self.chrome_tree.setHeaderLabels(["Chrome Extensions"])
        self.chrome_tree.setAcceptDrops(True)
        self.load_projects(self.chrome_tree, self.dirs['chrome'])
        
        # Add double-click handler
        self.chrome_tree.itemDoubleClicked.connect(lambda item: self.run_chrome_extension())
        
        # Editor
        self.chrome_editor = QTextEdit()
        
        # Add widgets to splitter
        splitter.addWidget(self.chrome_tree)
        splitter.addWidget(self.chrome_editor)
        
        layout.addLayout(toolbar)
        layout.addWidget(splitter)
        self.tabs.addTab(tab, "Chrome Extensions")
        
        # Connect signals
        self.chrome_tree.itemClicked.connect(lambda item: self.load_file(item.text(0), 'chrome'))
        save_btn.clicked.connect(lambda: self.save_file('chrome'))
        browse_btn.clicked.connect(lambda: self.browse_directory('chrome'))
        move_to_projects_btn.clicked.connect(lambda: self.move_selected_to_projects('chrome'))
        new_project_btn.clicked.connect(lambda: self.new_file('chrome'))
        run_btn.clicked.connect(self.run_chrome_extension)

    def create_python_scripts_tab(self):
        print("Creating Python Scripts tab...")
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Toolbar
        toolbar = QHBoxLayout()
        new_script_btn = QPushButton("New Script")
        browse_btn = QPushButton("Browse...")
        save_btn = QPushButton("Save")
        move_to_projects_btn = QPushButton("Move to Projects")
        run_btn = QPushButton("Run")
        
        toolbar.addWidget(new_script_btn)
        toolbar.addWidget(browse_btn)
        toolbar.addWidget(save_btn)
        toolbar.addWidget(move_to_projects_btn)
        toolbar.addWidget(run_btn)
        toolbar.addStretch()
        
        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Project tree
        self.scripts_tree = QTreeWidget()
        self.scripts_tree.setHeaderLabels(["Python Scripts"])
        self.scripts_tree.setAcceptDrops(True)
        self.load_projects(self.scripts_tree, self.dirs['scripts'])
        
        # Add double-click handler
        self.scripts_tree.itemDoubleClicked.connect(lambda item: self.run_python_script())
        
        # Editor
        self.scripts_editor = QTextEdit()
        
        # Add widgets to splitter
        splitter.addWidget(self.scripts_tree)
        splitter.addWidget(self.scripts_editor)
        
        layout.addLayout(toolbar)
        layout.addWidget(splitter)
        self.tabs.addTab(tab, "Python Scripts")
        
        # Connect signals
        self.scripts_tree.itemClicked.connect(lambda item: self.load_file(item.text(0), 'scripts'))
        save_btn.clicked.connect(lambda: self.save_file('scripts'))
        browse_btn.clicked.connect(lambda: self.browse_directory('scripts'))
        move_to_projects_btn.clicked.connect(lambda: self.move_selected_to_projects('scripts'))
        new_script_btn.clicked.connect(lambda: self.new_file('scripts'))
        run_btn.clicked.connect(self.run_python_script)

    def create_python_apps_tab(self):
        print("Creating Python Apps tab...")
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Toolbar
        toolbar = QHBoxLayout()
        new_app_btn = QPushButton("New App")
        browse_btn = QPushButton("Browse...")
        save_btn = QPushButton("Save")
        move_to_projects_btn = QPushButton("Move to Projects")
        run_btn = QPushButton("Run")
        
        toolbar.addWidget(new_app_btn)
        toolbar.addWidget(browse_btn)
        toolbar.addWidget(save_btn)
        toolbar.addWidget(move_to_projects_btn)
        toolbar.addWidget(run_btn)
        toolbar.addStretch()
        
        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Apps tree
        self.apps_tree = QTreeWidget()
        self.apps_tree.setHeaderLabels(["Python Apps"])
        self.apps_tree.setAcceptDrops(True)
        self.load_projects(self.apps_tree, self.dirs['apps'])
        
        # Add double-click handler
        self.apps_tree.itemDoubleClicked.connect(lambda item: self.run_python_app())
        
        # Editor
        self.apps_editor = QTextEdit()
        
        # Add widgets to splitter
        splitter.addWidget(self.apps_tree)
        splitter.addWidget(self.apps_editor)
        
        layout.addLayout(toolbar)
        layout.addWidget(splitter)
        self.tabs.addTab(tab, "Python Apps")
        
        # Connect signals
        self.apps_tree.itemClicked.connect(lambda item: self.load_file(item.text(0), 'apps'))
        save_btn.clicked.connect(lambda: self.save_file('apps'))
        browse_btn.clicked.connect(lambda: self.browse_directory('apps'))
        move_to_projects_btn.clicked.connect(lambda: self.move_selected_to_projects('apps'))
        new_app_btn.clicked.connect(lambda: self.new_file('apps'))
        run_btn.clicked.connect(self.run_python_app)

    def create_batch_scripts_tab(self):
        print("Creating Batch Scripts tab...")
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Toolbar
        toolbar = QHBoxLayout()
        new_script_btn = QPushButton("New Script")
        browse_btn = QPushButton("Browse...")
        save_btn = QPushButton("Save")
        move_to_projects_btn = QPushButton("Move to Projects")
        run_btn = QPushButton("Run")
        
        toolbar.addWidget(new_script_btn)
        toolbar.addWidget(browse_btn)
        toolbar.addWidget(save_btn)
        toolbar.addWidget(move_to_projects_btn)
        toolbar.addWidget(run_btn)
        toolbar.addStretch()
        
        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Scripts tree
        self.batch_tree = QTreeWidget()
        self.batch_tree.setHeaderLabels(["Batch Scripts"])
        self.batch_tree.setAcceptDrops(True)
        self.load_projects(self.batch_tree, self.dirs['batch'])
        
        # Add double-click handler
        self.batch_tree.itemDoubleClicked.connect(lambda item: self.run_batch_script())
        
        # Editor
        self.batch_editor = QTextEdit()
        
        # Add widgets to splitter
        splitter.addWidget(self.batch_tree)
        splitter.addWidget(self.batch_editor)
        
        layout.addLayout(toolbar)
        layout.addWidget(splitter)
        self.tabs.addTab(tab, "Batch Scripts")
        
        # Connect signals
        self.batch_tree.itemClicked.connect(lambda item: self.load_file(item.text(0), 'batch'))
        save_btn.clicked.connect(lambda: self.save_file('batch'))
        browse_btn.clicked.connect(lambda: self.browse_directory('batch'))
        move_to_projects_btn.clicked.connect(lambda: self.move_selected_to_projects('batch'))
        new_script_btn.clicked.connect(lambda: self.new_file('batch'))
        run_btn.clicked.connect(self.run_batch_script)

    def create_powershell_apps_tab(self):
        print("Creating PowerShell Apps tab...")
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Toolbar
        toolbar = QHBoxLayout()
        new_app_btn = QPushButton("New App")
        browse_btn = QPushButton("Browse...")
        save_btn = QPushButton("Save")
        move_to_projects_btn = QPushButton("Move to Projects")
        run_btn = QPushButton("Run")
        
        toolbar.addWidget(new_app_btn)
        toolbar.addWidget(browse_btn)
        toolbar.addWidget(save_btn)
        toolbar.addWidget(move_to_projects_btn)
        toolbar.addWidget(run_btn)
        toolbar.addStretch()
        
        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Apps tree
        self.powershell_tree = QTreeWidget()
        self.powershell_tree.setHeaderLabels(["PowerShell Apps"])
        self.powershell_tree.setAcceptDrops(True)
        self.load_projects(self.powershell_tree, self.dirs['powershell'])
        
        # Add double-click handler
        self.powershell_tree.itemDoubleClicked.connect(lambda item: self.run_powershell_app())
        
        # Editor
        self.powershell_editor = QTextEdit()
        
        # Add widgets to splitter
        splitter.addWidget(self.powershell_tree)
        splitter.addWidget(self.powershell_editor)
        
        layout.addLayout(toolbar)
        layout.addWidget(splitter)
        self.tabs.addTab(tab, "PowerShell Apps")
        
        # Connect signals
        self.powershell_tree.itemClicked.connect(lambda item: self.load_file(item.text(0), 'powershell'))
        save_btn.clicked.connect(lambda: self.save_file('powershell'))
        browse_btn.clicked.connect(lambda: self.browse_directory('powershell'))
        move_to_projects_btn.clicked.connect(lambda: self.move_selected_to_projects('powershell'))
        new_app_btn.clicked.connect(lambda: self.new_file('powershell'))
        run_btn.clicked.connect(self.run_powershell_app)

    def create_readme_tab(self):
        """Create README tab with information about the tool"""
        print("Creating README tab...")
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Create text editor for README content
        readme_text = QTextEdit()
        readme_text.setReadOnly(True)  # Make it read-only
        
        # Set the README content
        readme_content = """
# Developer Workspace

## Purpose
Developer Workspace is a unified development environment manager designed to streamline project organization and workflow efficiency. It provides a centralized location for managing different types of development projects including HTML, Chrome Extensions, Python Scripts, Python Apps, Batch Scripts, and PowerShell Apps.

## Created By
Developed by Chris Loetz

## Why It Was Created
This tool was created to solve common challenges developers face:
- Managing multiple project types in different locations
- Switching between different development environments
- Organizing projects by type and purpose
- Streamlining the development workflow
- Reducing time spent on project management

## How to Use

### Basic Usage
1. Select the appropriate tab for your project type (HTML, Chrome Extensions, etc.)
2. Use the "Browse" button to locate existing projects
3. Use "Move to Projects" to organize them into your workspace
4. Edit and manage your projects directly in the workspace

### Example Scenario
A developer is working on:
- A Python script for automation
- A Chrome extension for productivity
- An HTML project for a website

Instead of navigating multiple folders and windows, they can:
1. Use Developer Workspace to manage all projects in one place
2. Easily switch between projects using tabs
3. Keep everything organized by project type
4. Move projects between categories as needed

## Features
- Unified project management
- Multi-project type support
- Easy file/folder organization
- Project type categorization
- Drag-and-drop support
- Multi-file selection
- Workspace organization

## Why Use This Tool
1. **Organization**: Keep all development projects neatly categorized
2. **Efficiency**: Reduce time spent managing project files and folders
3. **Flexibility**: Support for multiple project types in one interface
4. **Productivity**: Everything you need in one workspace
5. **Simplicity**: Intuitive interface for project management

## Tips for Best Use
1. Use the appropriate tab for each project type
2. Regularly organize your projects using the "Move to Projects" feature
3. Take advantage of the drag-and-drop functionality
4. Use the multi-select feature for batch operations
5. Keep your workspace organized by project type

## Support
For issues, suggestions, or contributions, please contact Chris Loetz.
"""
        readme_text.setMarkdown(readme_content)
        
        # Add to layout
        layout.addWidget(readme_text)
        
        # Style the text editor
        readme_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.colors['secondary_bg']};
                color: {self.colors['text']};
                border: none;
                padding: 15px;
                font-size: 14px;
            }}
        """)
        
        self.tabs.addTab(tab, "README")

    def load_projects(self, tree, directory):
        """Load projects from directory into tree widget with color coding"""
        try:
            tree.clear()
            # First, load items from the workspace directory
            workspace_items = []
            for item in os.listdir(directory):
                tree_item = QTreeWidgetItem([item])
                full_path = os.path.join(directory, item)
                
                # Set appropriate icon
                if os.path.isdir(full_path):
                    tree_item.setIcon(0, self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon))
                else:
                    tree_item.setIcon(0, self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
                
                tree_item.setBackground(0, QBrush(QColor(self.colors['secondary_bg'])))
                workspace_items.append(item)
                tree.addTopLevelItem(tree_item)
            
            # Then, load items from the browsed directory (if any)
            if hasattr(self, 'browsed_paths'):
                for path in self.browsed_paths.get(directory, []):
                    if os.path.exists(path):
                        # Only use the final folder/file name, not the full path
                        item_name = os.path.basename(path)
                        if item_name not in workspace_items:
                            tree_item = QTreeWidgetItem([item_name])
                            
                            # Set appropriate icon
                            if os.path.isdir(path):
                                tree_item.setIcon(0, self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon))
                            else:
                                tree_item.setIcon(0, self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
                            
                            # Use grey background for items not in workspace
                            tree_item.setBackground(0, QBrush(QColor('#808080')))
                            tree_item.setData(0, Qt.ItemDataRole.UserRole, path)  # Store full path in data
                            tree.addTopLevelItem(tree_item)
            
            # Enable selection
            tree.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
            
        except Exception as e:
            print(f"Error loading projects: {e}")

    def browse_directory(self, tab_type):
        """Open directory browser dialog with multi-selection"""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)  # Set to Directory mode
        file_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        file_dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)  # Only show directories
        
        # Show dialog
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            
            # Initialize browsed_paths if it doesn't exist
            if not hasattr(self, 'browsed_paths'):
                self.browsed_paths = {}
            
            # Initialize list for this directory if it doesn't exist
            if self.dirs[tab_type] not in self.browsed_paths:
                self.browsed_paths[self.dirs[tab_type]] = []
            
            # Add each selected path if it's not already in the list
            for path in selected_files:
                if path not in self.browsed_paths[self.dirs[tab_type]]:
                    self.browsed_paths[self.dirs[tab_type]].append(path)
            
            # Refresh the tree view
            tree = getattr(self, f'{tab_type}_tree')
            self.load_projects(tree, self.dirs[tab_type])

    def move_selected_to_projects(self, tab_type):
        """Move all external items (gray background) to projects directory"""
        print("Starting move operation...")
        tree = getattr(self, f'{tab_type}_tree')
        
        # Get all items in the tree
        root = tree.invisibleRootItem()
        item_count = root.childCount()
        external_items = []
        
        # Find all gray (external) items
        for i in range(item_count):
            item = root.child(i)
            if item.background(0).color().name() == '#808080':
                external_items.append(item)
        
        if not external_items:
            QMessageBox.information(self, "Info", "No external items to move")
            return
        
        # Ask for confirmation
        response = QMessageBox.question(
            self,
            "Confirm Move",
            f"Move {len(external_items)} external item(s) to projects?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if response == QMessageBox.StandardButton.No:
            return
        
        moved_count = 0
        for item in external_items:
            try:
                source_path = item.data(0, Qt.ItemDataRole.UserRole)
                if source_path and os.path.exists(source_path):
                    destination = os.path.join(self.dirs[tab_type], item.text(0))
                    
                    # Check if destination already exists
                    if os.path.exists(destination):
                        response = QMessageBox.question(
                            self,
                            "File Exists",
                            f"{item.text(0)} already exists in destination. Replace it?",
                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                        )
                        if response == QMessageBox.StandardButton.No:
                            continue
                        
                        # Remove existing destination
                        if os.path.isdir(destination):
                            shutil.rmtree(destination)
                        else:
                            os.remove(destination)
                    
                    # Move the file or directory
                    try:
                        if os.path.isdir(source_path):
                            shutil.copytree(source_path, destination)
                            shutil.rmtree(source_path)
                        else:
                            shutil.move(source_path, destination)
                        moved_count += 1
                        print(f"Successfully moved {item.text(0)}")
                    except Exception as e:
                        print(f"Error moving {item.text(0)}: {e}")
                        QMessageBox.warning(
                            self,
                            "Move Error",
                            f"Failed to move {item.text(0)}: {str(e)}"
                        )
                else:
                    print(f"Source path doesn't exist: {source_path}")
            
            except Exception as e:
                print(f"Error processing item {item.text(0)}: {str(e)}")
                continue
        
        # Update browsed paths
        if hasattr(self, 'browsed_paths') and self.dirs[tab_type] in self.browsed_paths:
            self.browsed_paths[self.dirs[tab_type]] = [
                path for path in self.browsed_paths[self.dirs[tab_type]]
                if os.path.exists(path)
            ]
        
        # Refresh the tree
        self.load_projects(tree, self.dirs[tab_type])
        
        # Show success message
        if moved_count > 0:
            QMessageBox.information(
                self,
                "Success",
                f"Successfully moved {moved_count} item{'s' if moved_count > 1 else ''}"
            )
        
        print("Move operation complete")

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter events"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """Handle drop events"""
        current_tab_index = self.tabs.currentIndex()
        tab_text = self.tabs.tabText(current_tab_index).lower()
        
        # Map tab text to directory type
        tab_map = {
            'html': 'html',
            'chrome extensions': 'chrome',
            'python scripts': 'scripts',
            'python apps': 'apps',
            'batch scripts': 'batch',
            'powershell apps': 'powershell'
        }
        
        target_type = tab_map.get(tab_text)
        if not target_type:
            return
            
        # Process dropped items
        for url in event.mimeData().urls():
            source_path = url.toLocalFile()
            if os.path.exists(source_path):
                try:
                    destination = os.path.join(self.dirs[target_type], os.path.basename(source_path))
                    shutil.move(source_path, destination)
                    
                    # Refresh the current tree
                    tree = getattr(self, f'{target_type}_tree')
                    self.load_projects(tree, self.dirs[target_type])
                    
                    QMessageBox.information(self, "Success", "Item moved successfully!")
                    
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Failed to move item: {str(e)}")

    def load_file(self, filename, tab_type):
        """Load file content into editor"""
        try:
            print(f"Loading file: {filename} for tab: {tab_type}")
            tree = getattr(self, f'{tab_type}_tree')
            editor = getattr(self, f'{tab_type}_editor')
            
            # Get selected item
            selected_items = tree.selectedItems()
            if not selected_items:
                print("No item selected")
                return
                
            item = selected_items[0]
            
            # Get file path
            if item.background(0).color().name() == '#808080':
                # Item from browsed directory
                file_path = item.data(0, Qt.ItemDataRole.UserRole)
            else:
                # Item from workspace
                file_path = os.path.join(self.dirs[tab_type], filename)
            
            print(f"File path: {file_path}")
            
            # Check if path exists
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return
            
            # Check if it's a directory
            if os.path.isdir(file_path):
                print("Selected item is a directory")
                editor.clear()
                return
            
            # Load file content
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                editor.setText(content)
                print("File loaded successfully")
                
        except Exception as e:
            print(f"Error loading file: {e}")
            QMessageBox.warning(self, "Error", f"Error loading file: {str(e)}")

    def run_html_file(self):
        """Run HTML file in default browser"""
        try:
            tree = self.html_tree
            selected_items = tree.selectedItems()
            
            if not selected_items:
                QMessageBox.warning(self, "Warning", "Please select a project to run")
                return
            
            item = selected_items[0]
            if item.background(0).color().name() == '#808080':
                path = item.data(0, Qt.ItemDataRole.UserRole)
            else:
                path = os.path.join(self.dirs['html'], item.text(0))
            
            # Look for index.html in the folder
            if os.path.isdir(path):
                index_path = os.path.join(path, 'index.html')
                if os.path.exists(index_path):
                    os.startfile(index_path)
                else:
                    QMessageBox.warning(self, "Error", "No index.html file found in the selected folder")
            else:
                QMessageBox.warning(self, "Error", "Please select a folder")
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to run HTML file: {str(e)}")

    def run_chrome_extension(self):
        """Run Chrome Extension (placeholder)"""
        QMessageBox.information(
            self,
            "Not Implemented",
            "Chrome Extension running functionality will be implemented in a future update."
        )

    def run_python_script(self):
        """Run Python script in a separate process"""
        try:
            print("Starting Python script runner...")
            tree = self.scripts_tree
            selected_items = tree.selectedItems()
            
            if not selected_items:
                QMessageBox.warning(self, "Warning", "Please select a folder to run")
                return
            
            item = selected_items[0]
            print(f"Selected item: {item.text(0)}")
            
            if item.background(0).color().name() == '#808080':
                path = item.data(0, Qt.ItemDataRole.UserRole)
            else:
                path = os.path.join(self.dirs['scripts'], item.text(0))
            
            print(f"Path to check: {path}")
            
            # Find and run .py file in the folder
            if os.path.isdir(path):
                print("Path is a directory, searching for files...")
                py_files = [f for f in os.listdir(path) if f.endswith('.py')]
                print(f"Found PY files: {py_files}")
                
                if py_files:
                    script_path = os.path.join(path, py_files[0])
                    print(f"Running Python file: {script_path}")
                    
                    # Create a batch file to run the Python script and pause
                    batch_path = os.path.join(path, "_temp_run.bat")
                    with open(batch_path, 'w') as f:
                        f.write(f'@echo off\n')
                        f.write(f'python "{script_path}"\n')
                        f.write('pause\n')
                    
                    # Run the batch file and clean it up after
                    subprocess.Popen(batch_path, 
                                  creationflags=subprocess.CREATE_NEW_CONSOLE,
                                  cwd=os.path.dirname(script_path))
                    
                    # Clean up the temp batch file after a short delay
                    def cleanup():
                        time.sleep(2)  # Wait 2 seconds
                        try:
                            os.remove(batch_path)
                        except:
                            pass
                    
                    threading.Thread(target=cleanup).start()
                    
                else:
                    print("No suitable files found")
                    QMessageBox.warning(
                        self, 
                        "Error", 
                        "No suitable files found in the selected folder.\nSearched for: .py"
                    )
            else:
                print("Selected item is not a directory")
                QMessageBox.warning(self, "Error", "Please select a folder")
        
        except Exception as e:
            print(f"Error running Python script: {e}")
            QMessageBox.warning(self, "Error", f"Failed to run Python script: {str(e)}")

    def run_python_app(self):
        """Run Python application in a separate process"""
        try:
            print("Starting Python app runner...")
            tree = self.apps_tree
            selected_items = tree.selectedItems()
            
            if not selected_items:
                QMessageBox.warning(self, "Warning", "Please select a folder to run")
                return
            
            item = selected_items[0]
            print(f"Selected item: {item.text(0)}")
            
            if item.background(0).color().name() == '#808080':
                path = item.data(0, Qt.ItemDataRole.UserRole)
            else:
                path = os.path.join(self.dirs['apps'], item.text(0))
            
            print(f"Path to check: {path}")
            
            # Find and run .py file in the folder
            if os.path.isdir(path):
                print("Path is a directory, searching for files...")
                py_files = [f for f in os.listdir(path) if f.endswith('.py')]
                print(f"Found PY files: {py_files}")
                
                if py_files:
                    script_path = os.path.join(path, py_files[0])
                    print(f"Running Python file: {script_path}")
                    
                    # Create a wrapper script that includes error handling
                    wrapper_path = os.path.join(path, "_temp_wrapper.py")
                    with open(wrapper_path, 'w') as f:
                        f.write('''
import sys
import traceback
from PyQt5.QtWidgets import QApplication

try:
    with open(sys.argv[1]) as script_file:
        script_content = script_file.read()
        
    # Execute the script content
    exec(script_content)
    
    # Keep the application running
    if QApplication.instance():
        sys.exit(QApplication.instance().exec_())
        
except Exception as e:
    print("Error occurred:")
    print(traceback.format_exc())
    input("Press Enter to close...")
''')
                    
                    # Create a command window that stays open
                    cmd_path = os.path.join(path, "_temp_run.cmd")
                    with open(cmd_path, 'w') as f:
                        f.write('@echo off\n')
                        f.write('title Python Application\n')
                        f.write('color 0A\n')
                        f.write('cls\n')
                        f.write('echo Installing required packages...\n')
                        # Install required packages
                        f.write(f'"{sys.executable}" -m pip install PyGithub PyQt5\n')
                        f.write('echo.\n')
                        f.write('echo Starting GUI application...\n')
                        f.write('echo.\n')
                        # Run the wrapper script with the target script as argument
                        f.write(f'"{sys.executable}" "{wrapper_path}" "{script_path}"\n')
                        f.write('if %ERRORLEVEL% NEQ 0 (\n')
                        f.write('    echo.\n')
                        f.write('    echo Application encountered an error.\n')
                        f.write('    pause\n')
                        f.write(')\n')
                    
                    # Run the command file
                    process = subprocess.Popen(
                        ['cmd', '/K', cmd_path],
                        creationflags=subprocess.CREATE_NEW_CONSOLE,
                        cwd=os.path.dirname(script_path),
                        env=dict(os.environ, PYTHONIOENCODING='utf-8')
                    )
                    
                    # Clean up the temp files after a delay
                    def cleanup():
                        time.sleep(5)
                        try:
                            if os.path.exists(cmd_path):
                                os.remove(cmd_path)
                            if os.path.exists(wrapper_path):
                                os.remove(wrapper_path)
                        except:
                            pass
                    
                    threading.Thread(target=cleanup).start()
                    
                else:
                    print("No suitable files found")
                    QMessageBox.warning(
                        self, 
                        "Error", 
                        "No suitable files found in the selected folder.\nSearched for: .py"
                    )
            else:
                print("Selected item is not a directory")
                QMessageBox.warning(self, "Error", "Please select a folder")
        
        except Exception as e:
            print(f"Error running Python app: {e}")
            QMessageBox.warning(self, "Error", f"Failed to run Python app: {str(e)}")

    def run_python_app_direct(self, script_path):
        """Direct execution fallback for Python apps"""
        try:
            # Try running with regular Python to see any error messages
            process = subprocess.Popen(
                ['python', script_path],
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                cwd=os.path.dirname(script_path)
            )
            return process.returncode == 0
        except Exception as e:
            print(f"Error in direct execution: {e}")
            return False

    def run_batch_script(self):
        """Run Batch script"""
        try:
            tree = self.batch_tree
            selected_items = tree.selectedItems()
            
            if not selected_items:
                QMessageBox.warning(self, "Warning", "Please select a folder to run")
                return
            
            item = selected_items[0]
            if item.background(0).color().name() == '#808080':
                path = item.data(0, Qt.ItemDataRole.UserRole)
            else:
                path = os.path.join(self.dirs['batch'], item.text(0))
            
            # Find and run .bat file in the folder
            if os.path.isdir(path):
                bat_files = [f for f in os.listdir(path) if f.endswith('.bat')]
                if bat_files:
                    script_path = os.path.join(path, bat_files[0])
                    os.startfile(script_path)
                else:
                    QMessageBox.warning(self, "Error", "No .bat file found in the selected folder")
            else:
                QMessageBox.warning(self, "Error", "Please select a folder")
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to run batch script: {str(e)}")

    def run_powershell_app(self):
        """Run PowerShell application"""
        try:
            print("Starting PowerShell app runner...")
            tree = self.powershell_tree
            selected_items = tree.selectedItems()
            
            if not selected_items:
                QMessageBox.warning(self, "Warning", "Please select a folder to run")
                return
            
            item = selected_items[0]
            print(f"Selected item: {item.text(0)}")
            
            if item.background(0).color().name() == '#808080':
                path = item.data(0, Qt.ItemDataRole.UserRole)
            else:
                path = os.path.join(self.dirs['powershell'], item.text(0))
            
            print(f"Path to check: {path}")
            
            # Find and run .bat or .ps1 file in the folder
            if os.path.isdir(path):
                print("Path is a directory, searching for files...")
                bat_files = [f for f in os.listdir(path) if f.endswith('.bat')]
                ps1_files = [f for f in os.listdir(path) if f.endswith('.ps1')]
                
                print(f"Found BAT files: {bat_files}")
                print(f"Found PS1 files: {ps1_files}")
                
                if bat_files:  # Try .bat first
                    script_path = os.path.join(path, bat_files[0])
                    print(f"Running BAT file: {script_path}")
                    os.startfile(script_path)
                elif ps1_files:  # Fall back to .ps1
                    script_path = os.path.join(path, ps1_files[0])
                    print(f"Running PS1 file: {script_path}")
                    os.system(f'powershell -ExecutionPolicy Bypass -File "{script_path}"')
                else:
                    print("No suitable files found")
                    QMessageBox.warning(
                        self, 
                        "Error", 
                        "No suitable files found in the selected folder.\nSearched for: .bat, .ps1"
                    )
            else:
                print("Selected item is not a directory")
                QMessageBox.warning(self, "Error", "Please select a folder")
        
        except Exception as e:
            print(f"Error running PowerShell app: {e}")
            QMessageBox.warning(self, "Error", f"Failed to run PowerShell app: {str(e)}")

    def run_ubif_project(self):
        """Run UBIF project"""
        try:
            tree = self.ubif_tree
            selected_items = tree.selectedItems()
            
            if not selected_items:
                QMessageBox.warning(self, "Warning", "Please select a project to run")
                return
            
            item = selected_items[0]
            if item.background(0).color().name() == '#808080':
                path = item.data(0, Qt.ItemDataRole.UserRole)
            else:
                path = os.path.join(self.dirs['ubif'], item.text(0))
            
            # Look for main.py or similar file in the folder
            if os.path.isdir(path):
                py_files = [f for f in os.listdir(path) if f.endswith('.py')]
                if py_files:
                    script_path = os.path.join(path, py_files[0])
                    
                    # Create a batch file to run the Python script and pause
                    batch_path = os.path.join(path, "_temp_run.bat")
                    with open(batch_path, 'w') as f:
                        f.write('@echo off\n')
                        f.write(f'python "{script_path}"\n')
                        f.write('pause\n')
                    
                    # Run the batch file
                    subprocess.Popen(batch_path, 
                                  creationflags=subprocess.CREATE_NEW_CONSOLE,
                                  cwd=os.path.dirname(script_path))
                    
                    # Clean up the temp batch file after a short delay
                    def cleanup():
                        time.sleep(2)
                        try:
                            os.remove(batch_path)
                        except:
                            pass
                    
                    threading.Thread(target=cleanup).start()
                else:
                    QMessageBox.warning(self, "Error", "No Python files found in the selected folder")
            else:
                QMessageBox.warning(self, "Error", "Please select a folder")
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to run UBIF project: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeveloperWorkspace()
    window.show()
    sys.exit(app.exec())