from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import numpy as np
import random

import loadData as loader
import calculate as calc

import Range as Range
     
class MatplotlibWidget(QMainWindow):

    filename = "dane.txt"
    dataFolderPath = "resources/"
    path = dataFolderPath + filename

    newRange = False;

    dataList = []
    resultList = []
    rangeList = []
    #-------------------------------------------------------------------------------------
    #Methods
    #-------------------------------------------------------------------------------------
    def __init__(self):
        #WINDOW INIT------------------------------------------------------
        QMainWindow.__init__(self)
        loadUi("resources/testv2.ui",self)

        self.setWindowTitle("Czekoladowy Wojownik")


        #BACK------------------------------------
        self.loadFile()    
        self.rangeList, i = Range.InsertNewRange(self.rangeList,Range.Range(self.dataList[0][0],self.dataList[0][1], "x", 20))
        print(len(self.rangeList))

        #FRONT-----------------------------------
        self.rangeParametersEnabled(True)

        self.nextButton.clicked.connect(self.nextButtonClicked)
        self.previousButton.clicked.connect(self.previousButtonClicked)
        self.firstButton.clicked.connect(self.firstButtonClicked)
        self.lastButton.clicked.connect(self.lastButtonClicked)

        self.newButton.clicked.connect(self.newButtonClicked)
        self.removeButton.clicked.connect(self.removeButtonClicked)

        self.rangeComboBox.currentIndexChanged.connect(self.onRangeComboboxChanged)

        self.saveButton.clicked.connect(self.saveButtonClicked)
        self.drawButton.clicked.connect(self.drawButtonClicked)

        self.actionLoad.triggered.connect(self.loadFileDialogBox)
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

        self.addRangeToComboBox(0)

    def addRangeToComboBox(self,id):
        #self.rangeList.append(Range.Range(0,1,"",0))
        self.rangeComboBox.addItem("{} - Przemiana".format(self.rangeComboBox.count()+1))
        self.rangeComboBox.setCurrentIndex(id)
        self.printRangeData()


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
        self.calculateE()
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(self.dataList[0], self.resultList)
        self.MplWidget.canvas.draw()

    def loadFileDialogBox(self):
        output = QFileDialog.getOpenFileName( \
            self, "Open File", filter="Text files (*.txt)");

        if output[0] is not "":
            self.path = output[0]
            self.loadFile()
    
    def loadFile(self):
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
        #self.rangeComboBox.addItem("{} - Przemiana".format(self.rangeComboBox.count()+1))
        #self.rangeComboBox.setCurrentIndex(self.rangeComboBox.count() - 1)
        self.newRange = True
        self.printRangeData(True)

        if(self.rangeComboBox.count() > 0):
            self.rangeParametersEnabled(True)
        pass

    def removeButtonClicked(self):
        if self.rangeComboBox.count() > 1:
            self.rangeComboBox.removeItem(self.rangeComboBox.currentIndex())
        
        if self.rangeComboBox.count() <= 0:
            self.rangeParametersEnabled(False)

    def saveButtonClicked(self):
        if(self.newRange):
            newRange = Range.Range(float(self.minLineEdit.value()),float(self.maxLineEdit.value()),\
                self.functionLineEdit.setText, self.valueLineEdit.value(),self.nameLineEdit.text())

            self.rangeList, index = Range.InsertNewRange(self.rangeList,newRange)
            self.addRangeToComboBox(index)
            self.newRange = False;
        else:
            self.rangeList[self.rangeComboBox.currentIndex()].name = self.nameLineEdit.text()
            self.rangeList[self.rangeComboBox.currentIndex()].start = self.minLineEdit.value()
            self.rangeList[self.rangeComboBox.currentIndex()].end = self.maxLineEdit.value()
            self.rangeList[self.rangeComboBox.currentIndex()].thermalEffect = self.valueLineEdit.value()
        pass

    def drawButtonClicked(self):

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(self.dataList[0], self.resultList)
        self.MplWidget.canvas.draw()

    def onRangeComboboxChanged(self, value):
        self.newRange = False;
        print("combobox changed", value)    
        self.printRangeData()

    def rangeParametersEnabled(self, flag=True):
        self.minLineEdit.setEnabled(flag)
        self.maxLineEdit.setEnabled(flag)
        self.valueLineEdit.setEnabled(flag)
        #self.functionLineEdit.setEnabled(flag)
        self.saveButton.setEnabled(flag)

    def printRangeData(self,newRange = False):
        if newRange:
            self.nameLineEdit.setText("{} - Przemiana".format(self.rangeComboBox.count()+1))
            self.maxLineEdit.setValue(0)
            self.minLineEdit.setValue(0)
            self.valueLineEdit.setValue(0)
            #self.functionLineEdit.setIndex(-1)
            self.functionLineEdit.setEnabled(False)
        else:
            self.nameLineEdit.setText("{}".format(self.rangeList[self.rangeComboBox.currentIndex()].name))
            self.maxLineEdit.setValue(self.rangeList[self.rangeComboBox.currentIndex()].end)
            self.minLineEdit.setValue(self.rangeList[self.rangeComboBox.currentIndex()].start)
            self.valueLineEdit.setValue(self.rangeList[self.rangeComboBox.currentIndex()].thermalEffect)
            

app = QApplication([])


window = MatplotlibWidget()
window.show()
app.exec_()