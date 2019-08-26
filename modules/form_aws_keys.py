#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 23:33:56 2018

@author: dfischer
"""

from PySide2.QtWidgets import *
from modules.functions import *
import os
import re
from modules import SettingsManager
settings = SettingsManager.settingsManager()

home = os.path.expanduser("~")

class IdsForm(QDialog):
    def __init__(self,parent):
        super(IdsForm,self).__init__(parent)
        self.parent = parent
        self.setMinimumWidth(400)
        self.setWindowTitle("AWS API Manager")

        self.id = QLineEdit(settings.getParam('id'))
        self.key = QLineEdit(settings.getParam('key'))
        self.key.setEchoMode(QLineEdit.Password)
        region = settings.getParam('region')
        self.region = QLineEdit("us-east-1" if region == "" else region)


        self.mainLayout = QVBoxLayout()

        self.keys = QGridLayout()
        self.keys.addWidget(QLabel("AWS ID"),0,0)
        self.keys.addWidget(self.id, 0, 1)
        self.keys.addWidget(QLabel("AWS Key"),1,0)
        self.keys.addWidget(self.key, 1, 1)
        self.keys.addWidget(QLabel("Region"),2,0)
        self.keys.addWidget(self.region, 2, 1)

        self.save = QPushButton("Save")
        self.save.clicked.connect(self.save_to_file)

        self.mainLayout.addLayout(self.keys)
        self.mainLayout.addWidget(self.save)

        self.setLayout(self.mainLayout)

    def save_to_file(self):
        settings.setParam('id', self.id.text())
        settings.setParam('key', self.key.text())
        settings.setParam('region', self.region.text())
        settings.writeParams()

        os.system('aws configure set aws_access_key_id '+ self.id.text())
        os.system('aws configure set aws_secret_access_key ' + self.key.text())
        os.system('aws configure set default.region ' + self.region.text())

        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IdsForm(None)
    window.show()
    sys.exit(app.exec_())
    #app.exec_()





