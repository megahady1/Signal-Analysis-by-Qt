import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QAction, QFileDialog, QTextEdit, QGridLayout, QWidget, QMenu,QComboBox,QMessageBox
import numpy as np
import pandas as pd
from PlotSignal import PlotSignal
from PlotWindow import PlotWindow
 

class MainWindow(QMainWindow):
    vectors = []
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
    # ==========================================================
        # Create toolbar
        toolbar = self.addToolBar('Main Toolbar')

        # Populate The Toolbar
    # =====================
        # Button
    # =====================
        plotAction = QAction('Estimate Pdet', self)
        plotAction.triggered.connect(self.plotSignal)
        # Add button to toolbar
        toolbar.addAction(plotAction)

        plotAction = QAction('Calculate Pdet', self)
        plotAction.triggered.connect(self.PlotWindow)
        # Add button to toolbar
        toolbar.addAction(plotAction)

    # ==========================================================        
        # Create Manubar
        menubar = self.menuBar()
        # Populate The Manubar
    # =====================
        # FIle Menu
    # =====================
        FileMenu = self.menuBar().addMenu('File')
        
        NewMenu = QAction('New Session', self)
        NewMenu.triggered.connect(self.openSubWindow)
        FileMenu.addAction(NewMenu) 
        
        ClearMenu = QAction('Clear Session', self)
        # NewMenu.triggered.connect(self.TBA)
        FileMenu.addAction(ClearMenu)   

        CloseMenu = QAction('Close Session', self)
        # NewMenu.triggered.connect(self.TBA)
        FileMenu.addAction(CloseMenu)   
    # =====================
        # View Menu
    # =====================
        windowMenu = self.menuBar().addMenu('View')

        tileActionMenu = QAction('Tile Windows', self)
        tileActionMenu.triggered.connect(self.tileSubWindows)
        windowMenu.addAction(tileActionMenu)

        cascadeActionMenu = QAction('Cascade Windows', self)
        cascadeActionMenu.triggered.connect(self.cascadeSubWindows)
        windowMenu.addAction(cascadeActionMenu)

        closeAllActionMenu = QAction('Close All Windows', self)
        closeAllActionMenu.triggered.connect(self.closeAllSubWindows)
        windowMenu.addAction(closeAllActionMenu)
    # ==========================================================
    # Create status bar
        self.statusBar().showMessage('Signal Size')
        self.setWindowTitle('SRS Medical')
        self.showMaximized()


    def handleComboBoxChange(self, index):
        selected_option = self.sender().currentText()  # Get the selected option
        QMessageBox.information(self, 'Selected Option', f'You selected: {selected_option}')


    def openSubWindow(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Open File", "","Excel Files (*.xlsx *.xls *.csv)", options=options)
        if fileName:  # Check if fileName is not empty (user selected a file)
            df = self.ReadCsv(fileName)
            if df is not None:
                self.plotSignal(df)
                self.statusBar().showMessage('Uploaded Successfully')
        else:
            QMessageBox.warning(self, 'Warning', 'No file selected.')

    def ReadCsv(self, filename):
        try:
            df = pd.read_csv(filename, header=0, skiprows=0)  # Read with header and skip first two rows
            return df
        except Exception as e:
            print("Error reading CSV file:", e)
            return None

    def plotSignal(self, df):
        plot_signal_window = PlotSignal(self, df)
        self.mdi.addSubWindow(plot_signal_window)
        plot_signal_window.show()

    def PlotWindow(self, df):
        sub = PlotWindow(self)
        self.mdi.addSubWindow(sub)
        sub.show()

    def tileSubWindows(self):
        self.mdi.tileSubWindows()
            

    def cascadeSubWindows(self):
        self.mdi.cascadeSubWindows()

    def closeAllSubWindows(self):
        sub_windows = self.mdi.subWindowList()
        for sub_window in sub_windows:
            sub_window.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

