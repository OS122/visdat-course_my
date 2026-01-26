# Importieren für Visualisierung und Interaktion
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import sys
#from pyvistaqt import QtInteractor #nicht benötigt!!
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
import numpy as np
from ctypes import *
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure

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
        self.main_layout = QHBoxLayout()
        central_widget.setLayout(self.main_layout)
        
        # Create menu bar
        self.create_menus()
        
        # Create status bar
        self.statusBar().showMessage("Ready")

        # Create control panel
        controls = self.create_controls()
        self.main_layout.addWidget(controls)

        # PyVista plotter (move existing plotter code here)
        # self.plotter = QtInteractor(central_widget)
        # main_layout.addWidget(self.plotter.interactor, stretch=3)  # Give more space

        # -------------------------------------------------------------------------
        # # Test von https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_qt_sgskip.html
        # static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        # # Ideally one would use self.addToolBar here, but it is slightly
        # # incompatible between PyQt6 and other bindings, so we just add the
        # # toolbar as a plain widget instead.
        # main_layout.addWidget(NavigationToolbar(static_canvas, self))
        # main_layout.addWidget(static_canvas)

        # ---------------------------------------------------------------------------

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

            ## define directories for Simulation
            #define path of example FreeDyn Input file (FDS)
            self.fdsFilePath = myos.path.abspath(myos.path.join(myos.path.dirname(myos.path.abspath(__file__)), self.filefds))

            ## initialize FreeDyn API
            fdApi.init()

            ## create model by passing path to model file (.fds)
            self.modelIndex = fdApi.createModel(self.fdsFilePath,'no')
            if(self.modelIndex < 0):
                sys.exit()

            # Update info
            self.update_info()
            
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

        ## set model as active (so that there is no need for passing modelIndex in future calls)
        fdApi.setModelAsActive(self.modelIndex)

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

        self.time = time
        self.yCoord = yCoord

        # Display results (will be refined in next step)
        self.display_results()

        # ## plot results
        # plt.ion()
        # plt.plot(time, yCoord)
        # plt.xlabel('time [s]')
        # plt.ylabel('displacement [m]')
        # plt.grid(True)
        # plt.show()

        # ## read and plot measure "mea_y"
        # vMeasures = fdApi.generateMeasureVector()

        # measureNames = fdApi.getMeasureNames()
        # meaIndex = measureNames.index("mea_y")
        # yCoord = np.zeros((nTimeSteps,1))
        # for i in range(nTimeSteps):
        #     fdApi.getMeasuresAtTimeIndex(i, vMeasures)
        #     yCoord[i,0] = vMeasures[meaIndex,0]

        # ## plot results
        # plt.plot(time, yCoord)
        # plt.xlabel('time [s]')
        # plt.ylabel('displacement [m]')
        # plt.grid(True)
        # plt.show()

        # ## delete model after last interaction
        # fdApi.deleteModel(modelIndex)

        # # Keep the plot open at the end
        # plt.ioff()
        # plt.show()

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
        
        # Simulation info
        layout.addWidget(QLabel("\nSimulation Information:"))
        self.info_label = QLabel("No Simulation loaded")
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)

        # Push controls to top
        layout.addStretch()
        
        # Fixed width for control panel
        controls.setFixedWidth(280)
        
        return controls
# -----------------------------------------------------------------------------------------------------
    # handler methods:
    def update_field_display(self, field_name):
        """Update display when field selection changes"""
        self.display_results()

    def update_display_options(self):
        """Update display when checkboxes change"""
        self.display_results()
    
# -----------------------------------------------------------------------------------------------------
    # Infos:
    def update_info(self):
        """Update Simulation information display"""
        if self.filefds is None:
            self.info_label.setText("No filefds loaded")
            return
        
        ## initialize FreeDyn API
        fdApi.init()

        ## get model infos
        modelInfos = fdApi.getModelInfos()
    
        info_text = (
            f"numAllDofs: {str(modelInfos["numAllDofs"])}\n"
            f"numPhyDofs: {str(modelInfos["numPhyDofs"])}\n"
            f"numIntDof: {str(modelInfos["numIntDof"])}\n"
            f"numExtDof: {str(modelInfos["numExtDof"])}\n"
            f"numBodies: {str(modelInfos["numBodies"])}\n"
            f"numExtConstr: {str(modelInfos["numExtConstr"])}\n"
            f"numForces: {str(modelInfos["numForces"])}\n"
            f"numMeasures: {str(modelInfos["numMeasures"])}\n"
        )
        
        self.info_label.setText(info_text)
# -----------------------------------------------------------------------------------------------------
    # Display results:
    def display_results(self):
        """Display results with current settings"""
        if self.filefds is None:
            return
        
        self.plotter.clear()
        
        # Get current field selection
        field_name = self.field_combo.currentText()
        
        ## plot results
        plt.ion()
        plt.plot(self.time, self.yCoord)
        plt.xlabel('time [s]')
        plt.ylabel('displacement [m]')
        plt.grid(True)
        #plt.show()

        #self.plotter.addWidget(plt.gcf())
        canvas = FigureCanvas(plt.gcf())
        self.main_layout.addWidget(canvas)

        self.plotter.reset_camera()
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