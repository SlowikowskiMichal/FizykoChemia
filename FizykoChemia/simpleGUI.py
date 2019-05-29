from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import numpy as np
import random

import loadData as loader
import calculate as calc
     
class MatplotlibWidget(QMainWindow):

    filename = "dane.txt"
    dataFolderPath = "resources/"
    path = dataFolderPath + filename

    dataList = loader.load(path)
    resultList = []
    #-------------------------------------------------------------------------------------
    #Methods
    #-------------------------------------------------------------------------------------
    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi("resources/testv2.ui",self)

        self.setWindowTitle("PyQt5 & Matplotlib Example GUI")

        self.nextButton.clicked.connect(self.nextButtonClicked)
        self.previousButton.clicked.connect(self.previousButtonClicked)
        self.firstButton.clicked.connect(self.firstButtonClicked)
        self.lastButton.clicked.connect(self.lastButtonClicked)

        self.newButton.clicked.connect(self.newButtonClicked)
        self.removeButton.clicked.connect(self.lastButtonClicked)

        self.rangeComboBox.addItem("1")
        self.rangeComboBox.addItem("2")
        self.rangeComboBox.addItem("3")
        self.rangeComboBox.addItem("4")



        self.actionLoad.triggered.connect(self.loadFile)
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

    def update_graph(self):

        fs = 500
        f = random.randint(1, 100)
        ts = 1/fs
        length_of_signal = 100
        t = np.linspace(0,1,length_of_signal)
        
        cosinus_signal = np.cos(2*np.pi*f*t)
        sinus_signal = np.sin(2*np.pi*f*t)

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(t, cosinus_signal)
        self.MplWidget.canvas.axes.plot(t, sinus_signal)
        self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'),loc='upper right')
        self.MplWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
        self.MplWidget.canvas.draw()

    def print_graph(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(self.dataList[0], self.resultList)
        self.MplWidget.canvas.draw()

    def loadFile(self):
        output = QFileDialog.getOpenFileName( \
            self, "Open File", filter="Text files (*.txt)");

        if output[0] is not "":
            self.path = output[0]
            print(self.path)
            self.dataList = loader.load(self.path)
            print(self.dataList[0])
            self.calculateE()
            self.print_graph()


    def calculateE(self):
        self.dataList = calc.interpolate(self.dataList)
        self.resultList = calc.calculateE(self.dataList[0],self.dataList[1])
        
    def firstButtonClicked(self):
        self.rangeComboBox.setCurrentIndex(0)

    def lastButtonClicked(self):
        self.rangeComboBox.setCurrentIndex(self.rangeComboBox.count() - 1)

    def nextButtonClicked(self):
        if self.rangeComboBox.currentIndex()+1 < self.rangeComboBox.count():
            self.rangeComboBox.setCurrentIndex(self.rangeComboBox.currentIndex()+1)

    
    def previousButtonClicked(self):
        if self.rangeComboBox.currentIndex() > 0:
            self.rangeComboBox.setCurrentIndex(self.rangeComboBox.currentIndex()-1)

    def newButtonClicked(self):
        pass

    def removeButton(self):
        pass
app = QApplication([])


window = MatplotlibWidget()
window.show()
app.exec_()