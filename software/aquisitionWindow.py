from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer

import sys
if not './features/' in sys.path:
    sys.path.insert(0, './features/')

from features.aquisitionData import DataAquisition
from preprocessingWindow import PreProcessingDialog

class AquisitionDialog(QDialog):

    def __init__(self):
        super().__init__()
        loadUi("aquisitionDialog.ui", self)
        self.setWindowTitle('Aquisição')
        self.pushButtonStartAquisition.clicked.connect(self.startAquisition)
        self.timer = QTimer()

        self.dataAquisition = None

        self.t = 0

    def updatePlot(self):
        self.t+=self.intervalAquisition/1000
        
        if self.t>=self.timeAquisition:
            self.stopAquisition()
            #self.dataAquisition.saveData()
            self.t=0
            self.progressBarAquisition.setValue(100)
            self.pushButtonPreProcessing.clicked.connect(self.openPreProcessingDialog)
        else:
            self.dataAquisition.updateGraph(self.PlotWidget.canvas)
            self.progressBarAquisition.setValue(100*self.t/self.timeAquisition)
        
    
    def startAquisition(self):
        
        self.nChannels = int(self.lineEditnChannels.text())
        self.timeAquisition = int(self.lineEditAquisitionTime.text())
        self.frequencyAquisition = int(self.lineEditFrequency.text())
        self.batchSize = int(self.lineEditBatchSize.text())
        self.interval = [int(self.lineEditMinInterval.text()),
                int(self.lineEditMaxInterval.text())
        ]
        self.dataAquisition = DataAquisition('Gleidson', self.interval, self.frequencyAquisition, self.batchSize, self.nChannels)

        self.intervalAquisition = 1000*self.batchSize/self.frequencyAquisition
        self.timer.setInterval(self.intervalAquisition)
        self.timer.timeout.connect(self.updatePlot)
        self.timer.start()
        self.pushButtonStartAquisition.setText('Parar Aquisição')
        self.pushButtonStartAquisition.clicked.connect(self.stopAquisition)

        self.progressBarAquisition.setValue(0)

    def stopAquisition(self):
        self.timer.stop()
        self.pushButtonStartAquisition.setText('Iniciar Aquisição')
        self.pushButtonStartAquisition.clicked.connect(self.startAquisition)
        self.progressBarAquisition.setValue(100)
        self.timer = QTimer()
        
    def openPreProcessingDialog(self):
        preprocessDialog = PreProcessingDialog(self.dataAquisition)
        preprocessDialog.exec_()

app = QApplication(sys.argv)
w = AquisitionDialog()
w.show()
sys.exit(w.exec_())