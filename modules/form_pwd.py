#echo s3fs#$BUCKET /mnt/$BUCKET fuse _netdev,uid=userbda,gid=analytics,allow_other,umask=002,endpoint=us-east-2 0 0 >> /etc/fstab

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 23:33:56 2018

@author: dfischer
"""

from modules.functions import *
from modules import functions
from modules import SettingsManager
from PySide2.QtWidgets import *

settings = SettingsManager.settingsManager()

class PwdForm(QDialog):
    def __init__(self,parent):
        super(PwdForm,self).__init__(parent)
        self.parent = parent
        self.setMinimumWidth(400)
        self.setWindowTitle("Password Setup")

        self.mainLayout = QVBoxLayout()

        self.pwd_old = QLineEdit()
        self.pwd_old.setEchoMode(QLineEdit.Password)
        self.pwd_new = QLineEdit()
        self.pwd_new.setEchoMode(QLineEdit.Password)

        self.save = QPushButton("save")
        self.save.clicked.connect(self.fn_save)

        self.mainLayout.addWidget(QLabel("Current Password"))
        self.mainLayout.addWidget(self.pwd_old)
        self.mainLayout.addWidget(QLabel("New Password"))
        self.mainLayout.addWidget(self.pwd_new)
        self.mainLayout.addWidget(self.save)

        self.setLayout(self.mainLayout)

    def fn_save(self):
        session = settings.getSession()
        ec2_id = settings.getParam('ec2_id')
        ec2 = session.resource("ec2", use_ssl=False)
        i = ec2.Instance(id=ec2_id)
        settings.setParam("ec2_passwd",self.pwd_old.text())
        cmd = 'echo "{}:{}" | sudo chpasswd'.format(settings.getParam("user"),self.pwd_new.text())
        print(cmd)
        result = functions.run_script(cmd)
        msgBox = QMessageBox()
        if result:
            settings.setParam("ec2_passwd",self.pwd_new.text())
            settings.writeParams()
            msgBox.setText("Executed Correctly")
        else:
            msgBox.setText("Failed!")
        msgBox.exec_()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PwdForm(None)
    window.show()
# sys.exit(app.exec_())
    app.exec_()
