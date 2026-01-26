# Importieren von Packeten
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QFileDialog,
    QLabel, QPushButton, QLineEdit,
    QGroupBox, QComboBox
)
from PyQt6.QtGui import QAction
import subprocess
from pathlib import Path

# Eigene Module Laden
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'src')))
import Module as M

class Fenster(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Übertragungsfunktions Berechnung über Freedyn")
        self.setGeometry(100, 100, 1000, 600)

        # ------------------------------------------------------------
        # Anfangs Parameter Rauschen
        self.noise_params = {
            "fs": 100.0,
            "T1": 0.1,
            "T2": 7.0,
            "T3": 8.0,
            "dt": 0.01
        }

        # ------------------------------------------------------------
        # Erstellen Menü BAR
        self.create_menue()

        # ------------------------------------------------------------
        # STATUS BAR
        self.statusBar().showMessage("Bereit")

        # ------------------------------------------------------------
        # Zentrales WIDGET
        Zentrales_widget = QWidget()
        self.setCentralWidget(Zentrales_widget)
        main_layout = QHBoxLayout(Zentrales_widget)

        # ------------------------------------------------------------
        #  BEDIENFELD (LINKS)
        BEDIENFELD = self.Bedienfeld_erstellen()
        main_layout.addWidget(BEDIENFELD)

        # ------------------------------------------------------------
        # Grafikbereich (Rechts)
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        self.fig, self.ax = plt.subplots()
        self.ax.plot(x, y, label="sin(x)")
        self.ax.set_title("Sinus Kurve")
        self.ax.grid(True)
        self.ax.legend()

        self.canvas = FigureCanvas(self.fig)
        main_layout.addWidget(self.canvas, 4)
    
    # ------------------------------------------------------------
    def create_menue(self):
        """Anwendungsmenüs erstellen"""
        menü_bar = self.menuBar()
        file_menu = menü_bar.addMenu("Datei")

        # Simulationsdatei laden 
        open_action = QAction("&Öffnen Simulations-file...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        # Beenden
        exit_action = QAction("Beenden", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
    
    # ------------------------------------------------------------
    def open_file(self):
            """Öffnet die fds-Datei über den Dateidialog."""
            filename, _ = QFileDialog.getOpenFileName(
                self,
                "Auswählen Freedyn Simulations Datei", 
                os.path.join(os.path.dirname(__file__), "data_2"),
                "VTK Files (*.fds);;All Files (*.*)"
            )
            
            if not filename:
                return  # Benützer beendet
            
            try:
                # Lade Filefds
                self.filefds = filename
                
                # Update status
                self.statusBar().showMessage(f"Ladet: {filename}", 3000)
                
                # Update Fenster Titel
                import os
                self.setWindowTitle(f"Übertragungsfunktion für - {os.path.basename(filename)}")

                ## Verzeichnisse für die Simulation definieren
                # Pfad der Beispiel-FreeDyn-Eingabedatei (FDS) definieren
                self.fdsFilePath = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.filefds))
                
            except Exception as e:
                self.statusBar().showMessage(f"Error Laden Datei: {str(e)}", 5000)
    
    # ------------------------------------------------------------
    # Bedienfeld_Erstellen
    def Bedienfeld_erstellen(self):
        """Erstellet ein Bedienfeld mit Feldauswahl und Anzeigeoptionen."""
        Bedienfeld = QGroupBox("Bedienfeld")
        control_layout = QVBoxLayout()
        Bedienfeld.setLayout(control_layout)
                    
        # Field selection
        control_layout.addWidget(QLabel("Thema:"))
        self.field_combo = QComboBox()
        self.field_combo.addItem("Rauschen", userData=1)
        self.field_combo.addItem("Simulation", userData=2)
        self.field_combo.addItem("Übertragungsfunktion", userData=3)
        self.field_combo.currentIndexChanged.connect(self.on_field_changed)
        control_layout.addWidget(self.field_combo)

        # --------------------------------------------
        # Tasten – einmal erzeugen
        self.btn_noise = QPushButton("Rauschen darstellen")
        self.btn_noise.clicked.connect(self.show_noise)
        control_layout.addWidget(self.btn_noise)

        self.btn_sim_run = QPushButton("Simulation durchführen")
        self.btn_sim_run.clicked.connect(self.run_simulation)
        control_layout.addWidget(self.btn_sim_run)

        self.btn_sim_plot = QPushButton("Grafik darstellen")
        self.btn_sim_plot.clicked.connect(self.plot_simulation)
        control_layout.addWidget(self.btn_sim_plot)

        self.btn_tf_calc = QPushButton("Übertragungsfunktion berechnen")
        self.btn_tf_calc.clicked.connect(self.calc_transfer_function)
        control_layout.addWidget(self.btn_tf_calc)

        self.btn_tf_plot = QPushButton("Übertragungsfunktion darstellen")
        self.btn_tf_plot.clicked.connect(self.plot_transfer_function)
        control_layout.addWidget(self.btn_tf_plot)

        # Alle Buttons ausblenden
        self.btn_sim_run.setVisible(False)
        self.btn_sim_plot.setVisible(False)
        self.btn_tf_calc.setVisible(False)
        self.btn_tf_plot.setVisible(False)

        # --------------------------------------------
        # Parameter Gruppe – Rauschen
        self.noise_param_group = QGroupBox("Rauschparameter")
        param_layout = QVBoxLayout()
        self.noise_param_group.setLayout(param_layout)

        self.input_fs = QLineEdit(str(self.noise_params["fs"]))
        param_layout.addWidget(QLabel("Abtastfrequenz fs [Hz]"))
        param_layout.addWidget(self.input_fs)

        self.input_T1 = QLineEdit(str(self.noise_params["T1"]))
        param_layout.addWidget(QLabel("T1 – Ramp-Up Ende [s]"))
        param_layout.addWidget(self.input_T1)

        self.input_T2 = QLineEdit(str(self.noise_params["T2"]))
        param_layout.addWidget(QLabel("T2 – Ramp-Down Start [s]"))
        param_layout.addWidget(self.input_T2)

        self.input_T3 = QLineEdit(str(self.noise_params["T3"]))
        param_layout.addWidget(QLabel("T3 – Ramp-Down Ende [s]"))
        param_layout.addWidget(self.input_T3)

        self.input_dt = QLineEdit(str(self.noise_params["dt"]))
        param_layout.addWidget(QLabel("Zeitschritt dt [s]"))
        param_layout.addWidget(self.input_dt)

        control_layout.addWidget(self.noise_param_group)

        # --------------------------------------------
        # Fixed width for control panel
        Bedienfeld.setFixedWidth(280)

        control_layout.addStretch()  # schiebt alles nach oben
                                
        return Bedienfeld

    # ------------------------------------------------------------
    # Thema Wahl
    def on_field_changed(self, index):
        field_id = self.field_combo.itemData(index)

        # Sichtbarkeit korrekt steuern
        self.noise_param_group.setVisible(False)

        # Alle Buttons ausblenden
        self.btn_noise.setVisible(False)
        self.btn_sim_run.setVisible(False)
        self.btn_sim_plot.setVisible(False)
        self.btn_tf_calc.setVisible(False)
        self.btn_tf_plot.setVisible(False)

        if field_id == 1:
            self.noise_param_group.setVisible(True)
            self.btn_noise.setVisible(True)

        elif field_id == 2:
            # Simulation
            self.btn_sim_run.setVisible(True)
            self.btn_sim_plot.setVisible(True)

        elif field_id == 3:
            # Übertragungsfunktion
            self.btn_tf_calc.setVisible(True)
            self.btn_tf_plot.setVisible(True)

    
    # ------------------------------------------------------------
    # Definition Funktion Rauschen darstellen
    def show_noise(self):
        try:
            # ------------------------------------------------------------
            # Parameter aus GUI lesen
            fs = float(self.input_fs.text())
            T1 = float(self.input_T1.text())
            T2 = float(self.input_T2.text())
            T3 = float(self.input_T3.text())
            dt = float(self.input_dt.text())

            # ------------------------------------------------------------
            # Zeitvektor erzeugen
            t_vec = np.arange(0.0, 10.0 + dt, dt)
            self.dim = len(t_vec)

            # ------------------------------------------------------------
            # Erzeugen des rosa Rauschsignals
            x_noise = M.pink_noise_time_signal(fs, t_vec, T1, T2, T3)

            # ------------------------------------------------------------
            # Plot aktualisieren (bestehende Achse!)
            self.ax.clear()
            self.ax.plot(t_vec, x_noise)
            self.ax.set_xlabel("Zeit [s]")
            self.ax.set_ylabel("Kraft [N]")
            self.ax.set_title("Eingangssignal (Rosa Rauschen)")
            self.ax.grid(True)

            self.canvas.draw()

            # ------------------------------------------------------------
            # Statusmeldung
            self.statusBar().showMessage(
                "Rauschsignal erfolgreich erzeugt und dargestellt",
                4000
            )

        except ValueError:
            self.statusBar().showMessage(
                "Fehler: Ungültige numerische Eingabe bei Rauschparametern",
                5000
            )

    # ------------------------------------------------------------
    def run_simulation(self):
        try:
            # ------------------------------------------------------------
            # 1) Sicherheitsprüfung
            if not hasattr(self, "x_noise"):
                self.statusBar().showMessage(
                    "Fehler: Kein Eingangssignal vorhanden (zuerst Rauschen erzeugen)",
                    5000
                )
                return

            if not hasattr(self, "fdsFilePath"):
                self.statusBar().showMessage(
                    "Fehler: Keine FreeDyn-Datei geladen",
                    5000
                )
                return

            # ------------------------------------------------------------
            # 2) FFT des Eingangssignals
            X = (1.0 / self.dim) * np.fft.fft(self.x_noise)

            # ------------------------------------------------------------
            # Eingangssignal speichern
            kraft_pfad = Path(__file__).parent / "data_2" / "Kraft.txt"
            kraft_pfad.parent.mkdir(exist_ok=True)

            np.savetxt(
                kraft_pfad,
                np.column_stack((self.t_vec, self.x_noise))
            )

            # ------------------------------------------------------------
            # 3) Simulation mit FreeDyn

            free_dyn_exe = Path(
                r"C:\FreeDyn_Release_2024_9\FreeDyn_2024.9\bin\FreeDyn.exe"
            )

            if not free_dyn_exe.exists():
                raise FileNotFoundError("FreeDyn.exe nicht gefunden")

            # Sicherstellen: fdsFilePath OHNE Endung
            fds_base = Path(self.fdsFilePath).with_suffix("")

            command = [str(free_dyn_exe), str(fds_base) + ".fds"]

            self.statusBar().showMessage("Simulation läuft ...")
            subprocess.run(command, check=False)

            # ------------------------------------------------------------
            # Statusprüfung
            status_file = fds_base.with_suffix(".status")

            if not status_file.exists():
                raise FileNotFoundError("Statusdatei nicht gefunden")

            status_text = status_file.read_text(
                encoding="utf-8", errors="ignore"
            )

            if "Computation has been successfully finished" in status_text:
                self.statusBar().showMessage(
                    "Simulation erfolgreich abgeschlossen",
                    4000
                )
            else:
                self.statusBar().showMessage(
                    "Simulation beendet – Fehler im Solver",
                    5000
                )
                return

            # ------------------------------------------------------------
            # Einlesen der Messdaten
            measure_file = fds_base.with_suffix(".mrf")

            if not measure_file.exists():
                raise FileNotFoundError("Messdatei (*.mrf) nicht gefunden")

            self.t_mes, self.y = M.read_mrf(measure_file, measure_id=1)

        except Exception as e:
            self.statusBar().showMessage(
                f"Fehler Simulation: {str(e)}",
                6000
            )

    # ------------------------------------------------------------
    def plot_simulation(self):
        self.statusBar().showMessage("Simulation Grafik", 3000)
        print("Simulation Grafik darstellen")

    # ------------------------------------------------------------
    def calc_transfer_function(self):
        self.statusBar().showMessage("Übertragungsfunktion berechnen", 3000)
        print("Übertragungsfunktion berechnen")

    # ------------------------------------------------------------
    def plot_transfer_function(self):
        self.statusBar().showMessage("Übertragungsfunktion darstellen", 3000)
        print("Übertragungsfunktion darstellen")
    
    # ------------------------------------------------------------


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Fenster()
    window.show()
    sys.exit(app.exec())
