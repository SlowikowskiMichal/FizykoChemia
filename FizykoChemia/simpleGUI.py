from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import numpy as np
import random

import loadData as loader
import calculate as calc

import Range as bj
     
class MatplotlibWidget(QMainWindow):

    filename = "dane.txt"
    dataFolderPath = "resources/"
    path = dataFolderPath + filename

    dataList = loader.load(path)
    resultList = []

    rangeList = []
    #-------------------------------------------------------------------------------------
    #Methods
    #-------------------------------------------------------------------------------------
    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi("resources/testv2.ui",self)

        self.setWindowTitle("Czekoladowy Wojownik")

        self.nextButton.clicked.connect(self.nextButtonClicked)
        self.previousButton.clicked.connect(self.previousButtonClicked)
        self.firstButton.clicked.connect(self.firstButtonClicked)
        self.lastButton.clicked.connect(self.lastButtonClicked)

        self.newButton.clicked.connect(self.newButtonClicked)
        self.removeButton.clicked.connect(self.removeButtonClicked)

        self.rangeComboBox.currentIndexChanged.connect(self.onRangeComboboxChanged)

        self.saveButton.clicked.connect(self.saveButtonClicked)

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
        self.rangeList.append(bj.Range(0,1,"",0))
        
        self.rangeComboBox.addItem("{} - Przemiana".format(self.rangeComboBox.count()+1))
        self.rangeComboBox.setCurrentIndex(self.rangeComboBox.count() - 1)

        print(self.rangeList[0].start)

        if(self.rangeComboBox.count() > 0):
            self.rangeParametersEnabled(True)

    def removeButtonClicked(self):
        if self.rangeComboBox.count() > 0:
            self.rangeComboBox.removeItem(self.rangeComboBox.currentIndex())
        
        if self.rangeComboBox.count() <= 0:
            self.rangeParametersEnabled(False)

    def saveButtonClicked(self):
        pass

    def onRangeComboboxChanged(self, value):
        print("combobox changed", value)    
        self.printRangeData()

    def printRangeData(self):
        if self.rangeComboBox.count() <= 0:
            self.maxLineEdit.setText("")
            self.minLineEdit.setText("")
            self.valueLineEdit.setText("")
            #self.functionLineEdit.setIndex(-1)
            self.functionLineEdit.setEnabled(False)
        else:
            self.maxLineEdit.setText("{}".format(self.rangeList[self.rangeComboBox.currentIndex()].end))
            self.minLineEdit.setText("{}".format(self.rangeList[self.rangeComboBox.currentIndex()].start))
            self.valueLineEdit.setText("{}".format(self.rangeList[self.rangeComboBox.currentIndex()].thermalEffect))
            

    def rangeParametersEnabled(self, flag=False):
        self.minLineEdit.setEnabled(flag)
        self.maxLineEdit.setEnabled(flag)
        self.valueLineEdit.setEnabled(flag)
        #self.functionLineEdit.setEnabled(flag)
        self.saveButton.setEnabled(flag)

app = QApplication([])


window = MatplotlibWidget()
window.show()
app.exec_()