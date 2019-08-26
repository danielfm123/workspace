
from PySide2.QtWidgets import *
from modules import functions as fn
from modules.form_apps import appsForm


class tabApps(QWidget):

    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        layout = QVBoxLayout()

        mensaje = QLabel("Si eres usuario de linux, debes instalar sshpass y aws-cli")

        choco = QPushButton('Install Chocolatelly')
        choco.clicked.connect(self.fn_choco)

        basic = QPushButton('Install Basic Apps')
        basic.clicked.connect(self.fn_basic)

        apps = QPushButton('Install Data Scientist Tools')
        apps.clicked.connect(self.fn_apps)

        layout.addWidget(choco)
        layout.addWidget(basic)
        layout.addWidget(apps)
        layout.addWidget(mensaje)
        self.setLayout(layout)

    def fn_basic(self):
        fn.sudo('choco install git awscli winscp openssh notepadplusplus x2go -y')
        msgBox = QMessageBox()
        msgBox.setText("In order to SFTP to work you need to re open this application")
        msgBox.exec_()
        exit()

    def fn_choco(self):
        fn.sudo("\"%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe\" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command \"iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))\" && SET \"PATH=%PATH%;%ALLUSERSPROFILE%\\chocolatey\\bin\"")
        msgBox = QMessageBox()
        msgBox.setText("We need to close this app to finish setup, please re open")
        msgBox.exec_()
        quit()

    def fn_apps(self):
        win = appsForm(self)
        win.exec()

