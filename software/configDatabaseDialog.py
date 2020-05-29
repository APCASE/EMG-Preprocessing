from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

import sys
import os
import json

class ConfigDatabaseDialog(QDialog):

    def __init__(self, file="database.json", path="./"):
        super().__init__()

        self.file = file
        self.path = path

        loadUi("configDatabaseDialog.ui", self)

        self.loadDatabaseConfig()

        self.pushButtonConfig.clicked.connect(self.configDatabase)

    
    def loadDatabaseConfig(self):

        if os.path.isfile('{}{}'.format(self.path, self.file)):
            with open('{}{}'.format(self.path, self.file)) as f:
                self.data = json.load(f)
        else:
            self.data = {
                'user_name': "Usuario",
                'URI': 'localhost',
                'port': '27017'
            }
        
        self.lineEditUserName.setText(self.data['user_name'])
        self.lineEditURI.setText(self.data['URI'])
        self.lineEditPort.setText(self.data['port'])
    
    def configDatabase(self):
        self.data = {
                'user_name': self.lineEditUserName.text(),
                'URI': self.lineEditURI.text(),
                'port': self.lineEditPort.text()
            }
        with open('{}{}'.format(self.path, self.file), 'w') as json_file:
              json.dump(self.data, json_file)

'''app = QApplication(sys.argv)
w = Application()
w.show()
sys.exit(app.exec_())'''