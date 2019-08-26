
from modules.form_aws_keys import *
from modules.form_bucket import  BucketForm
from modules.form_pwd import  PwdForm
from modules.form_instance_id import idEc2Form
from modules import functions
import os

class tabSetup(QWidget):

    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        layout = QVBoxLayout()

        saveid = QPushButton('Set Credentials')
        saveid.clicked.connect(self.fn_saveid)

        ec2 = QPushButton('Select Lab Studio and Default Bucket')
        ec2.clicked.connect(self.fn_set_ec2)

        pwd = QPushButton('Set Password on Lab')
        pwd.clicked.connect(self.fn_set_pwd)

        ec2_api = QPushButton('Upload your Settings to Studio')
        ec2_api.clicked.connect(self.fn_upload_api)

        add_bucket = QPushButton("Connect Bucket on Lab")
        add_bucket.clicked.connect(self.fn_add_bucket)

        layout.addWidget(saveid)
        layout.addWidget(ec2)
        layout.addWidget(pwd)
        layout.addWidget(ec2_api)
        layout.addWidget(add_bucket)
        self.setLayout(layout)

    def fn_saveid(self):
        win = IdsForm(self)
        win.exec()
        self.parent.refresh()

    def fn_add_bucket(self):
        win = BucketForm(self)
        win.exec()

    def fn_set_pwd(self):
        win = PwdForm(self)
        win.exec()

    def fn_set_ec2(self):
        win = idEc2Form(self)
        win.exec()

    def fn_upload_api(self):
        home = os.path.expanduser("~")
        cum = functions.upload_file(settings.getParam("settings_path"),"/home/{}/.workspace.json".format(settings.getParam("user")))
        cum = cum and functions.upload_file(home + "/.bucket", "/home/{}/.bucket".format(settings.getParam("user")))
        cmd_api = 'echo '+settings.getParam('id')  + ':' + settings.getParam('key')+' | sudo tee /etc/passwd-s3fs;sudo chmod 600 /etc/passwd-s3fs'
        cum = cum and functions.run_script(cmd_api)
        # cum = cum and functions.run_script('mkdir ~/.aws')
        # cum = cum and functions.upload_file(home + "/.aws/config", "/home/{}/.aws/config".format(settings.getParam("user")))
        # cum = cum and functions.upload_file(home + "/.aws/credentials", "/home/{}/.aws/credentials".format(settings.getParam("user")))
        cum = cum and functions.run_script('aws configure set aws_access_key_id '+ settings.getParam("id"))
        cum = cum and functions.run_script('aws configure set aws_secret_access_key '+ settings.getParam("key"))
        cum = cum and functions.run_script('aws configure set default.region '+ settings.getParam("region"))

        if cum:
            msgBox = QMessageBox()
            msgBox.setText("Executed Correctly")
        else:
            msgBox = QMessageBox()
            msgBox.setText("Failed")
        msgBox.exec_()
