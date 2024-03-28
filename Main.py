# This is self contained GUI. Please note, we have to classes in this program
# Created by: Mohamed Abdelhady
# A 
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QAction, QFileDialog, QTextEdit, QGridLayout, QWidget, QMenu,QComboBox,QMessageBox
import numpy as np
import pandas as pd
# from PlotSignal import PlotSignal
# from PlotWindow import PlotWindow

class MainWindow(QMainWindow):
    vectors = []
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        # Create toolbars
        self.toolbar1 = self.addToolBar('Main Toolbar')
        self.toolbar2 = self.addToolBar('Second Toolbar')
        self.toolbar3 = self.addToolBar('Third Toolbar')
        self.toolbar1.setToolTip('Main Toolbar')

        # Populate toolbars
        self.populateToolbars()


        # Create menu
        self.createMenu()

        # Create status bar
        self.statusBar().showMessage('Signal ----')
        self.setWindowTitle('Medical')
        self.showMaximized()

    def populateToolbars(self):
        # Populate toolbar 1
        plotAction = QAction('Estimate Pdet', self)
        plotAction.triggered.connect(self.TBA)
        self.toolbar1.addAction(plotAction)

        plotAction1 = QAction('Calculate Pdet', self)
        plotAction1.triggered.connect(self.PlotWindow)
        self.toolbar1.addAction(plotAction1)

        # Populate toolbar 2 (can add more actions here if needed)
        plotAction2 = QAction('ToolBar A', self)
        self.toolbar2.addAction(plotAction2)

        # Populate toolbar 3 (can add more actions here if needed)
        plotAction3 = QAction('ToolBar C', self)
        self.toolbar3.addAction(plotAction3)

    def TBA(self):
        pass



    def toggleToolbar(self, toolbar, checked):
        toolbar.setVisible(checked)

    def createMenu(self):
        # Create Menubar
        menubar = self.menuBar()

        # File Menu
        fileMenu = menubar.addMenu('File')
        
        newMenu = QAction('New Session', self)
        newMenu.triggered.connect(self.openSubWindow)
        fileMenu.addAction(newMenu) 
        
        clearMenu = QAction('Clear Session', self)
        fileMenu.addAction(clearMenu)   

        closeMenu = QAction('Close Session', self)
        fileMenu.addAction(closeMenu)   

        # View Menu
        viewMenu = menubar.addMenu('View')

        tileActionMenu = QAction('Tile Windows', self)
        tileActionMenu.triggered.connect(self.tileSubWindows)
        viewMenu.addAction(tileActionMenu)

        cascadeActionMenu = QAction('Cascade Windows', self)
        cascadeActionMenu.triggered.connect(self.cascadeSubWindows)
        viewMenu.addAction(cascadeActionMenu)

        closeAllActionMenu = QAction('Close All Windows', self)
        closeAllActionMenu.triggered.connect(self.closeAllSubWindows)
        viewMenu.addAction(closeAllActionMenu)

        tileActionMenu = QAction('Tile Windows', self)
        tileActionMenu.triggered.connect(self.tileSubWindows)
        viewMenu.addAction(tileActionMenu)
        
        menu = self.menuBar().addMenu('View Toolbars')

        # Action to toggle visibility of toolbar 1
        toggleToolbar1Action = QAction('Toggle Toolbar 1', self, checkable=True)
        toggleToolbar1Action.setChecked(True)
        toggleToolbar1Action.triggered.connect(lambda checked: self.toggleToolbar(self.toolbar1, checked))
        menu.addAction(toggleToolbar1Action)

        # Action to toggle visibility of toolbar 2
        toggleToolbar2Action = QAction('Toggle Toolbar 2', self, checkable=True)
        toggleToolbar2Action.setChecked(True)
        toggleToolbar2Action.triggered.connect(lambda checked: self.toggleToolbar(self.toolbar2, checked))
        menu.addAction(toggleToolbar2Action)

        # Action to toggle visibility of toolbar 3
        toggleToolbar3Action = QAction('Toggle Toolbar 3', self, checkable=True)
        toggleToolbar3Action.setChecked(True)
        toggleToolbar3Action.triggered.connect(lambda checked: self.toggleToolbar(self.toolbar3, checked))
        menu.addAction(toggleToolbar3Action)

    def openSubWindow(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Open File", "","Excel Files (*.xlsx *.xls *.csv)", options=options)
        if fileName:  
            df = self.readCsv(fileName)
            if df is not None:
                # self.plotSignal(df)  IF YOU NEED TO PLOY THE SIGNAL
                self.statusBar().showMessage('Uploaded Successfully')
        else:
            QMessageBox.warning(self, 'Warning', 'No file selected.')

    def readCsv(self, filename):
        try:
            df = pd.read_csv(filename, header=0, skiprows=0)  
            return df
        except Exception as e:
            print("Error reading CSV file:", e)
            return None

    def PlotWindow(self):
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
