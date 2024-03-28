import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QMainWindow, QLabel, QMdiSubWindow, QMdiArea
import pyqtgraph as pg

class PlotWindow(QMdiSubWindow):
    def __init__(self, parent=None, df=None):
        super().__init__(parent)
        self.df = df
        self.setWindowTitle('Plot Window')
        self.plotSignal()

    def plotSignal(self): # This is initial plotting to the given signal
        # Create the plot
        region = pg.LinearRegionItem()
        win = pg.GraphicsLayoutWidget()
        win.setWindowTitle('pyqtgraph example: crosshair')
        p1 = win.addPlot(row=1, col=0)
        label = pg.LabelItem(justify='right')
        win.addItem(label)
        p1.avgPen = pg.mkPen('#FFFFFF')
        p1.avgShadowPen = pg.mkPen('#8080DD', width=10)
        p2 = win.addPlot(row=2, col=0)

        region.setZValue(10)
        p2.addItem(region, ignoreBounds=True)
        if self.df==None:
            # Generate random data\
            data1 = 10000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)
            data2 = 15000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)
        else:
            data1=self.df[1]
            data1=self.df[2]
            print("================OK================")
        p1.setAutoVisible(y=True)
        p1.plot(data1, pen="r")
        p1.plot(data2, pen="g")
        p2d = p2.plot(data1, pen="w")
        region.setClipItem(p2d)

        # Connect signals
        region.sigRegionChanged.connect(lambda: self.update(region, p1))
        p1.sigRangeChanged.connect(lambda: self.updateRegion(region, p1))
        region.setRegion([1000, 2000])

        # Crosshair
        vLine = pg.InfiniteLine(angle=90, movable=False)
        hLine = pg.InfiniteLine(angle=0, movable=False)
        p1.addItem(vLine, ignoreBounds=True)
        p1.addItem(hLine, ignoreBounds=True)

        # Mouse tracking
        vb = p1.vb
        proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=lambda evt: self.mouseMoved(evt, p1, vb, label, vLine, hLine))

        self.setWidget(win)

    def update(self, region, p1):
        region.setZValue(10)
        minX, maxX = region.getRegion()
        p1.setXRange(minX, maxX, padding=0)    

    def updateRegion(self, region, p1):
        rgn = p1.viewRange()[0]
        region.setRegion(rgn)

    def mouseMoved(self, evt, p1, vb, label, vLine, hLine):
        pos = evt[0]
        if p1.sceneBoundingRect().contains(pos):
            mousePoint = vb.mapSceneToView(pos)
            index = int(mousePoint.x())
            if index > 0 and index < len(self.data1):
                label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), data1[index], data2[index]))
            vLine.setPos(mousePoint.x())
            hLine.setPos(mousePoint.y())

