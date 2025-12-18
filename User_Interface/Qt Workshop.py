# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Build an FEM Visualization Application:

# -------------------------------------------------------------------------------------------------------
# Block 1: Application Structure and File Loading (45 min)

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import sys

from pyvistaqt import QtInteractor
import pyvista as pv
from PyQt6.QtWidgets import QFileDialog


class FEMViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FEM Results Viewer")
        self.resize(1200, 800)
        
        # State variables
        self.mesh = None
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout (horizontal split)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Left side will be controls (later)
        # For now, just add plotter
        
        # Right side: PyVista 3D view
        self.plotter = QtInteractor(central_widget)
        main_layout.addWidget(self.plotter.interactor)
        
        # # Add a sample sphere for testing
        # sphere = pv.Sphere()
        # self.plotter.add_mesh(sphere, color='lightblue', show_edges=True)
        # self.plotter.reset_camera()
        
        # Create menus and status bar
        self.create_menus()
        self.statusBar().showMessage("Ready")
    
    #--------------------------
    def create_menus(self):
        """Create application menus"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        open_action = QAction("&Open Mesh...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_mesh)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        reset_action = QAction("&Reset Camera", self)
        reset_action.setShortcut("R")
        reset_action.triggered.connect(self.reset_camera)
        view_menu.addAction(reset_action)
    
    def open_mesh(self):
        """Open mesh file using file dialog"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Mesh File",
            "c:/visdat-course/data",  # Starting directory
            "VTK Files (*.vtu *.vtk *.vti);;All Files (*.*)"
        )
        
        if not filename:
            return  # User canceled
        
        try:
            # Load mesh
            self.mesh = pv.read(filename)
            
            # Clear previous display
            self.plotter.clear()
            
            # Display mesh
            self.plotter.add_mesh(
                self.mesh,
                color='lightgray',
                show_edges=True
            )
            self.plotter.reset_camera()
            
            # Update status
            self.statusBar().showMessage(f"Loaded: {filename}", 3000)
            
            # Update window title
            import os
            self.setWindowTitle(f"FEM Viewer - {os.path.basename(filename)}")
            
        except Exception as e:
            self.statusBar().showMessage(f"Error loading file: {str(e)}", 5000)
    
    def reset_camera(self):
        """Reset camera view"""
        if self.plotter:
            self.plotter.reset_camera()
            self.statusBar().showMessage("Camera reset", 2000)

def main():
    app = QApplication(sys.argv)
    window = FEMViewer()
    window.show()
    sys.exit(app.exec())

def closeEvent(self, event):
    """Clean up VTK resources before closing"""
    if self.plotter:
        self.plotter.close()
        self.plotter = None
    event.accept()

if __name__ == "__main__":
    main()

