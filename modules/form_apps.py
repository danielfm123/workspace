#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 23:33:56 2018

@author: dfischer
"""

from PySide2.QtWidgets import *
from modules.functions import *
from modules import SettingsManager as sm, functions as fn

class appsForm(QDialog):
    def __init__(self,parent):
        super(appsForm,self).__init__(parent)
        self.settings = sm.settingsManager()
        self.parent = parent
        self.setMinimumWidth(400)
        self.setWindowTitle("Apps")

        self.mainLayout = QVBoxLayout()


        avivable_apps = ["git",
                         "r.studio",
                         "r.project",
                         "dbeaver",
                         "pycharm-community",
                         "vscode",
                         "bitvise-ssh-client",
                         "giteye",
                         "obs-studio",
                         "7zip",
                         "python",
                         "winscp",
                         "awscli",
                         "googlechrome",
                         "miktex",
                         "texstudio",
                         "notepadplusplus",
                         "office365proplus",
                         "x2go"]
        self.apps = [QCheckBox(a) for a in avivable_apps]

        self.install = QPushButton("Install Selected Apps")
        self.install.clicked.connect(self.fn_install)

        for a in self.apps:
            self.mainLayout.addWidget(a)
        self.mainLayout.addWidget(self.install)

        self.setLayout(self.mainLayout)

    def fn_install(self):
        checked = [a.text() if a.isChecked() else "" for a in self.apps]
        checked = " ".join(checked)
        command = "choco install " + checked + " -y"
        print(command)
        fn.sudo(command)
        if "winscp" in checked:
            msgBox = QMessageBox()
            msgBox.setText("In order to SFTP to work you need to re open this application")
            msgBox.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = appsForm(None)
    window.show()
# sys.exit(app.exec_())
    app.exec_()





