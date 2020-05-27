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
        self.preprocessing.getDataFromDatabase()
        
        loadUi("preprocessingDialog.ui", self)
        
        self.spinBoxNChannel.setRange(0, aquisition.nChannels)
        self.verticalSliderBias.valueChanged.connect(self.setBias)

        self.addPreprocessingFunctionsWidget()
        self.setPreprocessingFunctions()

        self.plot = None
        


    def addPreprocessingFunctionsWidget(self):
        '''
        Método para adicionar widgets para seleção de funções de pré-processamento que serão utilizadas
        '''
        self.checkBoxFunctions = {}
        self.radioBoxFuctionsAnalyse = {}
        c = True
        for k, _ in self.preprocessing.fPreprocessing.functions.items():
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

    def setMinMaxRange(self, channel, function):
        min_, max_ = self.preprocessing.getMinMaxRange(channel, function)
        self.verticalSliderBias.setRange(min_, max_)
        self.verticalSliderBias.setSingleStep(.001)
        
    def setBias(self):
        self.preprocessing.setBias(self.scaler.inverse_transform(np.array(self.verticalSliderBias.value()).reshape(-1,1)))
        self.target = self.generateBinaryClassifier(self.dataAnalyse, 1)
        self.plot.updateGraph(self.dataAnalyse, self.target)

    def setPreprocessingFunctions(self):
        for k, v in self.checkBoxFunctions.items():
            if v.isChecked():
                self.preprocessing.preprocessingFunctions[k] = k
    
    def showPreprocessingFunction(self):
        channel = self.spinBoxNChannel.value()
        
        function = None
        for _, v in self.radioBoxFuctionsAnalyse.items():
            if v.isChecked():
                function = v.text()
                break
        
        self.dataAnalyse = self.preprocessing.preprocessedData[str(channel)][str(function)]
        
        if not(self.plot):
            self.plot = AnalysisPreprocessingPlot(self.PlotWidget.canvas, (0, np.shape(self.dataAnalyse)[0]))
        self.setMinMaxRange(str(channel), str(function))
        self.plot.updateGraph(self.dataAnalyse, None)