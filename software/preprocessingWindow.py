from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import numpy as np

import sys
if not './features/' in sys.path:
    sys.path.insert(0, './features/')

from features.preprocessing import Functions
from features.plotlive import AnalysisPreprocessingPlot
from features.preprocessingData import PreprocessingData
from features.database import Database_emg

class PreProcessingDialog(QDialog):

    def __init__(self, database):
        super().__init__()
        loadUi("preprocessingDialog.ui", self)
        self.database = database

        self.showColumns()
        self.showChannels()

        self.spinBoxMovement.valueChanged.connect(self.setLabel)

        

    def showColumns(self):
        columns = self.database.getCollections()
        self.comboBoxDatabaseColumns.clear()
        for c in columns:
            self.comboBoxDatabaseColumns.addItem(c)
        self.comboBoxDatabaseColumns.currentIndexChanged.connect(self.showChannels)
    
    def clearLayoutWidget(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            child.widget().deleteLater()
    
    def showPreprocessingFunctions(self):
        self.clearLayoutWidget(self.verticalLayoutPreprocessingFunctionsAnalyse)
        self.clearLayoutWidget(self.verticalLayoutPreprocessingFunctions)

        self.choiceRadioButtons = {}
        self.choiceCheckButtons = {}

        for k, _ in self.preprocessingData.f.functions.items():
            self.choiceRadioButtons[k] = QRadioButton(k)
            self.choiceRadioButtons[k].clicked.connect(self.showPlot)
            self.verticalLayoutPreprocessingFunctionsAnalyse.addWidget(
                self.choiceRadioButtons[k]
            )
            

            self.choiceCheckButtons[k] = QCheckBox(k)
            self.verticalLayoutPreprocessingFunctions.addWidget(
                self.choiceCheckButtons[k]
            )
            self.choiceCheckButtons[k].setChecked(True)
            
    
    def showChannels(self):
        currentColumn = self.comboBoxDatabaseColumns.currentText()
        data = self.database.push_data(currentColumn)
        self.comboBoxChannel.clear()

        for d in data:
            for k, v in d['data']['data'].items():
                #print(len(v))
                #exit()
                self.comboBoxChannel.addItem(k)
            break
        self.preprocessingData = PreprocessingData(data)
        self.preprocessingData.preprocessData()
        self.showPreprocessingFunctions()
    
    def setLabel(self):
        self.label = int(self.spinBoxMovement.value())
    
    def showPlot(self):
        function = ""
        for k, v in self.choiceRadioButtons.items():
            if v.isChecked():
                function = k
                break
        
        channel = self.comboBoxChannel.currentText()
        data = self.preprocessingData.getData(channel, function)
        print(data)
        #self.plotWidget = AnalysisPreprocessingPlot(self.PlotWidget.canvas, 
        #    self.preprocessingData.getRangeXAxis(channel, function))
        


d = Database_emg('Gleidson', None, None)
app = QApplication(sys.argv)
w = PreProcessingDialog(d)
w.show()
sys.exit(w.exec_())