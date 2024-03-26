import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QMainWindow, QPushButton, QComboBox, QMessageBox, QColorDialog
from PyQt5 import QtGui
from PyQt5.QtCore import Qt 
import random
class PlotSignal(QMainWindow):
    def __init__(self, main_window, df):
        super().__init__()
        self.setWindowTitle('Plot')
        self.df = df  # Save the DataFrame
        self.initUI()

    def initUI(self):
        # Create plot area
        self.plot_widget = pg.GraphicsLayoutWidget()
        self.setCentralWidget(self.plot_widget)
        toolbar = self.addToolBar('Toolbar')
        toolbar.setOrientation(Qt.Vertical)
        self.addToolBar(Qt.LeftToolBarArea,toolbar)
        # Add buttons to the toolbar
        button = QPushButton('Change Color')
        button.clicked.connect(self.showColorDialog)
        toolbar.addWidget(button)

        # Create combobox
        combobox = QComboBox()
        for item in list(self.df):
            combobox.addItem(item)    
        combobox.currentIndexChanged.connect(self.handleComboBoxChange)

        # Add combobox to toolbar
        toolbar.addWidget(combobox)

        # Plot DataFrame
        self.plotDataFrame()

    def plotDataFrame(self):
        lengths = [len(self.df[column]) for column in self.df.columns]
        colors=[(200,0,0) , (0,200,0), (0,0,200)]
        SignalNames=['EMG', 'Pves','Pabd']
        plot_item = self.plot_widget.addPlot()
        legend = plot_item.addLegend()  # Add legend to the plot
        legend.setFont(QtGui.QFont('Arial', 20))  # Set font size to 12 (adjust as needed)
        headers=list(self.df.columns)
        print(headers)
        i=1
        if len(set(lengths)) != 1:
            print("Error: Lengths of columns are not equal")
        else:
            for column, color, sig in zip(self.df.columns, colors, SignalNames):
                curve=plot_item.plot(self.df[column], name=column, pen=color)
                print(i)
                i=i+1
            self.statusBar().showMessage('Uploaded Successfully')
        
        # if you want to remove curve from the plot 
        plot_item.removeItem(curve) 
        # legend.removeItem(curve)

    def handleComboBoxChange(self, index):
        selected_option = self.sender().currentText()  # Get the selected option
        QMessageBox.information(self, 'Selected Option', f'You selected: {selected_option}')

    def showColorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            if hasattr(self, 'curve'):  # Check if the curve object exists
                self.curve.setPen(color)  # Set the color of the curve if it exists
            else:
                self.curve = self.plot_widget.addPlot().plot(pen=color)  # Create curve with selected color
