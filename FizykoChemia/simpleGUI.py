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
    min = 0
    max = 0
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
        self.rangeList, i = Range.InsertNewRange(self.rangeList,Range.Range(self.min,self.max,self.dataList[0][0],\
            self.dataList[0][1], "x", 20, "{} - Przemiana".format(self.rangeComboBox.count()+1)))
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

        self.methodComboBox.currentIndexChanged.connect(self.onMethodComboboxChanged)

        self.saveButton.clicked.connect(self.saveButtonClicked)
        self.drawButton.clicked.connect(self.drawButtonClicked)

        self.actionLoad.triggered.connect(self.loadFileDialogBox)
        self.actionSaveResult.triggered.connect(self.saveFileDialogBox)
        self.actionSaveResultAndData.triggered.connect(self.saveBigFileDialogBox)
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

        self.addRangeToComboBox(0)

    def addRangeToComboBox(self,id,itemName = ""):
        if not itemName:
            itemName = "{} - Przemiana".format(self.rangeComboBox.count()+1)
        self.rangeComboBox.addItem(itemName)
        self.rangeComboBox.setCurrentIndex(id)
        self.printRangeData()

    def print_graph(self):
        self.calculateE()
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.set_xlabel('Temperatura')
        self.MplWidget.canvas.axes.set_ylabel('Entalpia')
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
        self.min = self.dataList[0][0]
        self.max = self.dataList[0][-1]
        self.print_graph()

    def saveBigFileDialogBox(self):
        self.saveFileDialogBox(True)

    def saveFileDialogBox(self,additionalInfo = False):
        output = QFileDialog.getSaveFileName( \
            self, "Save File", filter="CSV files (*.csv)");

        if output[0] is not "":

            path = output[0]
            self.saveFile(path,additionalInfo)
    def saveFile(self,path,additionalInfo = False):
        if additionalInfo:
            text = "Temperatura,Data,Entalpia,\n"
            for i,r in enumerate(self.resultList):
                text+="{},{},{}\n".format(self.dataList[0][i],self.dataList[1][i],r)
        else:
            text = "Temperatura,Entalpia,\n"
            for i,r in enumerate(self.resultList):
                text+="{},{}\n".format(self.dataList[0][i],r)

        try:
            file = open(path,'w+')
            file.write(text)
            file.close()
        except IOError:
            self.showWarning("Błąd zapisu pliku",\
                "Nie można zapisać do wskazanego pliku",\
                "Uwaga",\
                "Brak dostępu do podanego pliku")


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
        self.newRange = True
        self.printRangeData(True)

        if(self.rangeComboBox.count() > 0):
            self.rangeParametersEnabled(True)
        pass

    def removeButtonClicked(self):
        if self.rangeComboBox.count() > 1:
            self.rangeComboBox.removeItem(self.rangeComboBox.currentIndex())
            self.rangeList = Range.RemoveRange(self.rangeList,self.rangeComboBox.currentIndex())
            self.printRangeData()
        
        if self.rangeComboBox.count() <= 0:
            self.rangeParametersEnabled(True)

    def saveButtonClicked(self):
        if(self.newRange):
            try:
                newRange = Range.Range(self.min,self.max,float(self.minLineEdit.value()),float(self.maxLineEdit.value()),\
                    self.functionLineEdit.setText, self.valueLineEdit.value(),self.nameLineEdit.text())
            except ValueError as e:
                self.showWarning("Niepoprawne wartości!",\
                    "Przedział zawiera niepoprawne wartości!",\
                    "Uwaga",\
                    "Początek i koniec przedziału są równe.")
                self.printRangeData()
                return
            except AssertionError:
                self.showWarning("Niepoprawne wartości!",\
                    "Przedział zawiera niepoprawne wartości!",\
                    "Uwaga",\
                    "Wartości nowego przedziału wykraczają poza wartości wczytanych temperatur.")
                self.printRangeData()
                return

            try:
                self.rangeList, index = Range.InsertNewRange(self.rangeList,newRange)
            except AssertionError:
                self.showWarning("Niepoprawne wartości!",\
                    "Przedział zawiera niepoprawne wartości!",\
                    "Uwaga",\
                    "Porzedziały nakładają się na siebie.")
                self.printRangeData()
                return

            self.addRangeToComboBox(index, self.nameLineEdit.text())
            self.newRange = False;
        else:
            try:
                newRange = Range.Range(self.min,self.max,float(self.minLineEdit.value()),float(self.maxLineEdit.value()),\
                    self.functionLineEdit.setText, self.valueLineEdit.value(),self.nameLineEdit.text())
            except ValueError as e:
                self.showWarning("Niepoprawne wartości!",\
                    "Przedział zawiera niepoprawne wartości!",\
                    "Uwaga",\
                    "Początek i koniec przedziału są równe.")
                self.printRangeData()
                return
            except AssertionError:
                self.showWarning("Niepoprawne wartości!",\
                    "Przedział zawiera niepoprawne wartości!",\
                    "Uwaga",\
                    "Wartości nowego przedziału wykraczają poza wartości wczytanych temperatur.")
                self.printRangeData()
                return

            buffList = self.rangeList.copy()
            del buffList[self.rangeComboBox.currentIndex()]
            try:
                buffList, index = Range.InsertNewRange(buffList,newRange)
            except AssertionError:
                self.showWarning("Niepoprawne wartości!",\
                    "Przedział zawiera niepoprawne wartości!",\
                    "Uwaga",\
                    "Porzedziały nakładają się na siebie.")
                self.printRangeData()
                return

            self.rangeList = buffList.copy()

            self.loadRangeComboBoxFromList()

        pass

    def loadRangeComboBoxFromList(self):
        self.rangeComboBox.clear()
        i = 0
        for r in self.rangeList:
            self.addRangeToComboBox(i,r.name)
            i+=1


    def showWarning(self,header,info,title,detail):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(header)
        msg.setInformativeText(info)
        msg.setWindowTitle(title)
        msg.setDetailedText(detail)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def drawButtonClicked(self):
        self.calculateE()
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.xlabel("Temperatura")
        self.MplWidget.canvas.ylabel("Entalpia")
        self.MplWidget.canvas.axes.plot(self.dataList[0], self.resultList)
        self.MplWidget.canvas.draw()

    def onRangeComboboxChanged(self, value):
        self.newRange = False;
        print("combobox changed", value)    
        self.printRangeData()

    def rangeParametersEnabled(self, flag=True):
        self.nameLineEdit.setEnabled(flag)
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
            self.nameLineEdit.setText(self.rangeList[self.rangeComboBox.currentIndex()].name)
            self.maxLineEdit.setValue(self.rangeList[self.rangeComboBox.currentIndex()].end)
            self.minLineEdit.setValue(self.rangeList[self.rangeComboBox.currentIndex()].start)
            self.valueLineEdit.setValue(self.rangeList[self.rangeComboBox.currentIndex()].thermalEffect)
            

    def onMethodComboboxChanged(self):
        print(self.methodComboBox.currentText().lower())
        self.functionLineEdit.setEnabled(self.methodComboBox.currentText().lower() == "equation")
        


app = QApplication([])


window = MatplotlibWidget()
window.show()
app.exec_()