from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from configDatabaseDialog import ConfigDatabaseDialog
from aquisitionWindow import AquisitionDialog
from preprocessingWindow import PreProcessingDialog

import sys

class Application(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi("mainWindow.ui", self)

        self.actionConfigurar.triggered.connect(self.showConfigDataBaseDialog)
        self.pushButtonAquisitionDialog.clicked.connect(self.showAquisitionWindowDialog)
        self.pushButtonPreprocessingDialog.clicked.connect(self.showPreprocessingDialog)
    def loadDatabaseConfig(self, file, path='./'):
        pass
    
    def showConfigDataBaseDialog(self):
        config_database_dialog = ConfigDatabaseDialog()
        config_database_dialog.exec_()
    
    def showAquisitionWindowDialog(self):
        aquisition_dialog = AquisitionDialog()
        aquisition_dialog.exec_()
    
    def showPreprocessingDialog(self):
        preprocessing_dialog = PreProcessingDialog()
        preprocessing_dialog.exec_()

app = QApplication(sys.argv)
w = Application()
w.show()
sys.exit(app.exec_())