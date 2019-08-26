#echo s3fs#$BUCKET /mnt/$BUCKET fuse _netdev,uid=userbda,gid=analytics,allow_other,umask=002,endpoint=us-east-2 0 0 >> /etc/fstab

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 23:33:56 2018

@author: dfischer
"""

from PySide2.QtWidgets import *
from modules.functions import *
from modules import functions
from modules import SettingsManager
settings = SettingsManager.settingsManager()

class BucketForm(QDialog):
    def __init__(self,parent):
        super(BucketForm,self).__init__(parent)
        self.parent = parent
        self.setMinimumWidth(400)
        self.setWindowTitle("Bucket Connector")

        self.api_access = settings.getParam('aws_access_key_id')
        self.api_secret = settings.getParam('aws_secret_access_key')
        self.user = settings.getParam('user')
        self.region = settings.getParam('region')

        self.mainLayout = QVBoxLayout()

        self.session = settings.getSession()
        s3 = self.session.resource("s3",use_ssl=False)
        self.buckets = {x.name: x for x in list(s3.buckets.all())}

        self.combo_bucket = QComboBox()
        self.combo_bucket.addItems(list(self.buckets.keys()))

        self.connect = QPushButton("Connect")
        self.connect.clicked.connect(self.fm_connect)

        self.mainLayout.addWidget(self.combo_bucket)
        self.mainLayout.addWidget(self.connect)

        self.setLayout(self.mainLayout)

    def fm_connect(self):
        ec2_id = settings.getParam('ec2_id')
        ec2 = self.session.resource("ec2", use_ssl=False)
        i = ec2.Instance(id=ec2_id)
        cmd_limpiar = 'cat /etc/fstab | sudo grep -v {} | sudo tee /etc/fstab.tmp'.format(self.combo_bucket.currentText())
        cmd_move = 'sudo mv /etc/fstab.tmp /etc/fstab'
        cmd_fstab = 'echo s3fs#{bucket} /mnt/{bucket} fuse ' \
                    '_netdev,uid={user},allow_other,umask=002,endpoint={region} 0 0 ' \
                    '| sudo tee -a /etc/fstab;'.format(bucket = self.combo_bucket.currentText(),
                                            region = self.region,
                                            user = self.user)
        cmd_mount = 'sudo mkdir /mnt/{bucket};sudo mount /mnt/{bucket}'.format(bucket =self.combo_bucket.currentText())
        result = functions.run_script(cmd_limpiar)
        result = result and functions.run_script(cmd_move)
        result = result and functions.run_script(cmd_fstab)
        result = result and functions.run_script(cmd_mount)
        msgBox = QMessageBox()
        if result:
            msgBox.setText("Executed Correctly")
        else:
            msgBox.setText("Failed")
        msgBox.exec_()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BucketForm(None)
    window.show()
    app.exec_()





