# Importieren für Visualisierung und Interaktion
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

from PyQt6.QtWidgets import (
    QGroupBox, QComboBox, QCheckBox,
    QPushButton
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QFileDialog,
    QGroupBox, QComboBox, QCheckBox,
    QPushButton, QSlider  # Add QSlider
)

# Importieren für Freedyn
import os as myos
import sys
import numpy as np
from ctypes import *
import matplotlib.pyplot as plt

sys.path.insert(0, 'C:\\Users\\olive\\OneDrive\\Dokumente\\Freedyn\\FreeDynAPI_2024.9\\FreeDynAPI\\fdApi')
import fdApi

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class USolverViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Übertragungsfunktions Solver")
        self.resize(1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Create menu bar
        self.create_menus()
        
        # Create status bar
        self.statusBar().showMessage("Ready")

        # Create control panel
        controls = self.create_controls()
        main_layout.addWidget(controls)

        # PyVista plotter (move existing plotter code here)
        self.plotter = QtInteractor(central_widget)
        main_layout.addWidget(self.plotter.interactor, stretch=3)  # Give more space to 3D view

        # Create menus and status bar
        self.create_menus()
        self.statusBar().showMessage("Ready")
# -----------------------------------------------------------------------------------------------------            
    def create_menus(self):
        """Create application menus"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        open_action = QAction("&Open Simulation-file...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
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
    
# -----------------------------------------------------------------------------------------------------
    def open_file(self):
        """Open fds file using file dialog"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Freedyn Simulation File", 
            myos.path.join(myos.path.dirname(__file__), "data"), # Starting directory
            "VTK Files (*.fds);;All Files (*.*)"
        )
        
        if not filename:
            return  # User canceled
        
        try:
            # Load Filefds
            self.filefds = filename
                    
            # Update status
            self.statusBar().showMessage(f"Loaded: {filename}", 3000)
            
            # Update window title
            import os
            self.setWindowTitle(f"Übertragungsfunktion für - {os.path.basename(filename)}")
            
        except Exception as e:
            self.statusBar().showMessage(f"Error loading file: {str(e)}", 5000)
# -----------------------------------------------------------------------------------------------------
    # Reset Camera   
    def reset_camera(self):
        """Reset camera view (to be implemented)"""
        self.statusBar().showMessage("Reset camera - not implemented yet", 2000)
# -----------------------------------------------------------------------------------------------------
    # Run Calculation   
    def Run_Calculation(self):
        """Run Calculation"""
        self.statusBar().showMessage("Run Calculation", 2000)
        # ---------------------------------------------------------------------------------------------
        # Berechnung anhand Demo 1:

        ## define directories
        #define path of example FreeDyn Input file (FDS)
        fdsFilePath = myos.path.abspath(myos.path.join(myos.path.dirname(myos.path.abspath(__file__)), self.filefds))

        ## initialize FreeDyn API
        fdApi.init()

        ## create model by passing path to model file (.fds)
        modelIndex = fdApi.createModel(fdsFilePath,'no')
        if(modelIndex < 0):
            sys.exit()

        ## set model as active (so that there is no need for passing modelIndex in future calls)
        fdApi.setModelAsActive(modelIndex)

        ## get model infos
        modelInfos = fdApi.getModelInfos()
        print("model infos:")
        print("\tnumAllDofs: "   + str(modelInfos["numAllDofs"]))
        print("\tnumPhyDofs: "   + str(modelInfos["numPhyDofs"]))
        print("\tnumIntDof: "    + str(modelInfos["numIntDof"]))
        print("\tnumExtDof: "    + str(modelInfos["numExtDof"]))
        print("\tnumBodies: "    + str(modelInfos["numBodies"]))
        print("\tnumExtConstr: " + str(modelInfos["numExtConstr"]))
        print("\tnumForces: "    + str(modelInfos["numForces"]))
        print("\tnumMeasures: "  + str(modelInfos["numMeasures"]))

        ## start simulation (simulation and solver settings according to .fds file)
        solveEomSuc = fdApi.solveEoM()
        if(solveEomSuc < 0):
            print("Simulation not successful!")
            sys.exit()

        ## postprocessing
        # get number of time steps
        nTimeSteps = fdApi.getNumTimeSteps()

        ## read states and filter Y-displacements
        states = fdApi.generateStateVectors()
        time = np.zeros((nTimeSteps,1))
        yCoord = np.zeros((nTimeSteps,1))
        for i in range(nTimeSteps):
            time[i,0] = fdApi.getStatesAtTimeIndex(i,states["Q"])
            yCoord[i,0] = states["Q"][1,0]

        ## plot results
        plt.ion()
        plt.plot(time, yCoord)
        plt.xlabel('time [s]')
        plt.ylabel('displacement [m]')
        plt.grid(True)
        plt.show()

        ## read and plot measure "mea_y"
        vMeasures = fdApi.generateMeasureVector()

        measureNames = fdApi.getMeasureNames()
        meaIndex = measureNames.index("mea_y")
        yCoord = np.zeros((nTimeSteps,1))
        for i in range(nTimeSteps):
            fdApi.getMeasuresAtTimeIndex(i, vMeasures)
            yCoord[i,0] = vMeasures[meaIndex,0]

        ## plot results
        plt.plot(time, yCoord)
        plt.xlabel('time [s]')
        plt.ylabel('displacement [m]')
        plt.grid(True)
        plt.show()

        ## delete model after last interaction
        fdApi.deleteModel(modelIndex)

        # Keep the plot open at the end
        plt.ioff()
        plt.show()

# -----------------------------------------------------------------------------------------------------
    # Control Panel
    def create_controls(self):
        """Create control panel with field selection and display options"""
        controls = QGroupBox("Control")
        layout = QVBoxLayout()
        controls.setLayout(layout)
        
        # Field selection
        layout.addWidget(QLabel("Display Field:"))
        self.field_combo = QComboBox()
        layout.addWidget(self.field_combo)

        # Run button
        reset_button = QPushButton("Run Calculation")
        reset_button.clicked.connect(self.Run_Calculation)
        layout.addWidget(reset_button)
        
        # Push controls to top
        layout.addStretch()
        
        # Fixed width for control panel
        controls.setFixedWidth(280)
        
        return controls
# -----------------------------------------------------------------------------------------------------
    # handler methods:
    def update_field_display(self, field_name):
        """Update display when field selection changes"""
        self.display_mesh()

    def update_display_options(self):
        """Update display when checkboxes change"""
        self.display_mesh()
# -----------------------------------------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    window = USolverViewer()
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