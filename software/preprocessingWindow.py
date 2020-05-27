from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import numpy as np

import sys
if not './features/' in sys.path:
    sys.path.insert(0, './features/')

from features.preprocessing import Functions
from features.plotlive import AnalysisPreprocessingPlot
from features.preprocessingData import PreprocessingData 


class PreProcessingDialog(QDialog):

    def __init__(self, aquisition):
        super().__init__()
        self.preprocessing = PreprocessingData(aquisition)
        
        loadUi("preprocessingDialog.ui", self)
        
        

    def addPreprocessingFunctionsWidget(self):
        self.checkBoxFunctions = {}
        self.radioBoxFuctionsAnalyse = {}
        c = True
        for k, v in self.fPreprocessing.functions.items():
            self.checkBoxFunctions[k] = QCheckBox(k, self)
            self.checkBoxFunctions[k].setChecked(True)
            self.checkBoxFunctions[k].stateChanged.connect(self.setPreprocessingFunctions)
            self.radioBoxFuctionsAnalyse[k] = QRadioButton(k, self)
            if c:
                self.radioBoxFuctionsAnalyse[k].setChecked(True)
                c = not(c)
            self.radioBoxFuctionsAnalyse[k].toggled.connect(self.showPreprocessingFunction)
            

            self.verticalLayoutPreprocessingFunctions.addWidget(self.checkBoxFunctions[k])
            self.verticalLayoutPreprocessingFunctionsAnalyse.addWidget(self.radioBoxFuctionsAnalyse[k])
    
    def getDataFromDatabase(self):
        self.dataChannel = {}
        
        for i in self.database.push_data():
            for k, v in i['data'].items():
                try:
                    self.dataChannel[k].append(v)
                except:
                    self.dataChannel[k] = []
                    self.dataChannel[k].append(v)
        
        self.preprocessedData = {}
        for k, v in self.dataChannel.items():
            
            self.dataChannel[k] = np.asarray(v).reshape(-1, self.__batchsize)
            self.preprocessedData[k] = self.fPreprocessing.transform(self.dataChannel[k], self.__preprocessingFunctions)
            
                        

    def setMinMaxRange(self, channel, function):
        self.scaler = MinMaxScaler((0, 100))
        self.scaler.fit(self.preprocessedData[str(channel)][function].reshape(-1,1))

        min_ = np.min(self.scaler.transform(self.preprocessedData[str(channel)][function]))
        max_ = np.max(self.scaler.transform(self.preprocessedData[str(channel)][function]))

        self.verticalSliderBias.setRange(np.asscalar(min_),np.asscalar(max_))
        self.verticalSliderBias.setSingleStep(.001)
        
    
    def setBias(self):
        self.__bias = self.scaler.inverse_transform(np.array(self.verticalSliderBias.value()).reshape(-1,1))
        self.target = self.generateBinaryClassifier(self.dataAnalyse, self.__bias)
        self.__plot.updateGraph(self.dataAnalyse, self.target)

    def setPreprocessingFunctions(self):
        for k, v in self.checkBoxFunctions.items():
            if v.isChecked():
                self.__preprocessingFunctions[k] = k
    
    def showPreprocessingFunction(self):
        channel = self.spinBoxNChannel.value()
        
        function = None
        for _, v in self.radioBoxFuctionsAnalyse.items():
            if v.isChecked():
                function = v.text()
                break
        
        self.dataAnalyse = self.preprocessedData[str(channel)][str(function)]
        
        if not(self.__plot):
            self.__plot = AnalysisPreprocessingPlot(self.PlotWidget.canvas, (0, np.shape(self.dataAnalyse)[0]))
        self.setMinMaxRange(str(channel), str(function))
        self.__plot.updateGraph(self.dataAnalyse, None)
        
    
    @staticmethod
    def generateBinaryClassifier(data, bias):
        binary = []
        max_ = 1
        for i in range(np.shape(data)[0]):
            if data[i]>bias:
                binary.append(max_)
            else:
                binary.append(0)
        
        return np.asarray(binary)
    