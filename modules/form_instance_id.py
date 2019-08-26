#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 23:33:56 2018

@author: dfischer
"""

from modules.functions import *
from PySide2.QtWidgets import *
import os
from modules import SettingsManager
import platform
settings = SettingsManager.settingsManager()

home = os.path.expanduser("~")

class idEc2Form(QDialog):
    def __init__(self,parent):
        super(idEc2Form,self).__init__(parent)
        self.parent = parent
        self.setMinimumWidth(400)
        self.setWindowTitle("AWS API Manager")

        self.bucket = QComboBox()

        try:
            con = settings.getSession()
            ec2 = con.resource("ec2", use_ssl = False)
            instances = list(ec2.instances.all())
            s3 = con.resource("s3", use_ssl=False)
            buckets = {x.name: x for x in list(s3.buckets.all())}
            for b in buckets:
                self.bucket.addItem(b)
        except:
            pass

        dict = {i.id : tagsToDict(i.tags)["Name"]  for i in instances if i.tags is not None}

        self.combo_ec2 = QComboBox()
        for i in dict.keys():
            self.combo_ec2.addItem(dict[i],i)
        try:
            self.combo_ec2.setCurrentText(dict[settings.getParam("ec2_id")])
        except:
            pass

        self.os = QComboBox()
        for os in ['Linux','Windows']:
            self.os.addItem(os)

        self.mainLayout = QVBoxLayout()

        self.keys = QGridLayout()
        self.keys.addWidget(QLabel("EC2 Lab Name"),0,0)
        self.keys.addWidget(self.combo_ec2, 0, 1)
        self.keys.addWidget(QLabel("Operating System"), 1, 0)
        self.keys.addWidget(self.os, 1, 1)
        self.pwd = QLineEdit()
        self.pwd.setEchoMode(QLineEdit.Password)
        self.keys.addWidget(QLabel("Lab Current Password"), 2, 0)
        self.keys.addWidget(self.pwd, 2, 1)
        self.keys.addWidget(QLabel("Default Bucket"), 3, 0)
        self.keys.addWidget(self.bucket, 3, 1)
        self.bucket.setCurrentText(settings.getParam("bucket"))
        self.save = QPushButton("Save")
        self.save.clicked.connect(self.save_to_file)

        self.mainLayout.addLayout(self.keys)
        self.mainLayout.addWidget(self.save)

        self.setLayout(self.mainLayout)

    def save_to_file(self):
        id = self.combo_ec2.currentData()
        print(self.combo_ec2.currentData())
        settings.setParam('ec2_id',id)
        settings.setParam('os', self.os.currentText())
        #settings.setParam('team', self.bucket.currentText()) #legacy
        settings.setParam('bucket', self.bucket.currentText())
        settings.setParam('ec2_passwd', self.pwd.text())
        if self.os.currentText() == 'Windows':
            settings.setParam('user', 'Administrator')
        else:
            settings.setParam('user', 'user')
        settings.writeParams()
        self.parent.parent.refresh()

        with open(home + "/.bucket","+w") as f:
            f.write(self.bucket.currentText())

        if platform.system() == 'Windows':
            with open(home + "/Documents/.bucket","+w") as f:
                f.write(self.bucket.currentText())

        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = idEc2Form(None)
    window.show()
# sys.exit(app.exec_())
    app.exec_()





