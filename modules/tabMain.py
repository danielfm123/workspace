from PySide2.QtWidgets import *
from PySide2.QtGui import *
import time
import pandas as pd
from modules import functions
import os
import subprocess
import platform
import shutil
from modules import SettingsManager
settings = SettingsManager.settingsManager()

class tabMain(QWidget):

    global settings

    def __init__(self,parent):
        super().__init__(parent)

        self.instance_types = pd.read_csv(functions.resource_path('files/instances.csv'))

        # Acciones
        self.hbox_manipulate = QHBoxLayout()
        self.hbox_manipulate.addWidget(QLabel("Actions:"))

        self.on = QPushButton("Turn On")
        self.off = QPushButton("Turn Off")
        self.reset = QPushButton("Reset")

        self.grid_manipulate = QGridLayout()
        self.grid_manipulate.addWidget(self.on, 0, 0)
        self.grid_manipulate.addWidget(self.off, 0, 1)
        self.grid_manipulate.addWidget(self.reset, 0, 2)

        self.on.clicked.connect(self.fn_prender)
        self.off.clicked.connect(self.fn_apagar)
        self.reset.clicked.connect(self.fn_reset)

        # Tamaño
        self.grid_manipulate.addWidget(QLabel('Instance Size:'), 1, 0)
        self.instance_type = QComboBox()


        self.grid_manipulate.addWidget(self.instance_type, 1, 1)
        self.set_type = QPushButton("Set Size")
        self.grid_manipulate.addWidget(self.set_type, 1, 2)
        self.set_type.clicked.connect(self.fn_set_type)

        # Atributos
        self.hbox_attr = QHBoxLayout()
        self.hbox_attr.addWidget(QLabel("Instance Information:"))

        self.grid_attr = QGridLayout()
        self.grid_attr.addWidget(QLabel('Name'), 0, 0)
        self.name = QLineEdit()
        self.name.setReadOnly(True)
        self.grid_attr.addWidget(self.name, 0, 1)

        self.grid_attr.addWidget(QLabel('Type'), 1, 0)
        self.type = QLineEdit()
        self.type.setReadOnly(True)
        self.grid_attr.addWidget(self.type, 1, 1)

        self.grid_attr.addWidget(QLabel('USD / hour'), 2, 0)
        self.price = QLineEdit()
        self.price.setReadOnly(True)
        self.grid_attr.addWidget(self.price, 2, 1)

        self.grid_attr.addWidget(QLabel('IP'), 3, 0)
        self.ip = QLineEdit()
        self.ip.setReadOnly(True)
        self.grid_attr.addWidget(self.ip, 3, 1)


        self.grid_attr.addWidget(QLabel('Status'), 4, 0)
        self.status = QLineEdit()
        self.status.setReadOnly(True)
        self.grid_attr.addWidget(self.status, 4, 1)

        # Servicios
        self.hbox_serv = QHBoxLayout()
        self.hbox_serv.addWidget(QLabel("Launch Services:"))


        self.nomachine = QPushButton("Remote Desktop")
        self.rstudio = QPushButton("RStudio")
        self.jupyter = QPushButton("Jupyter")
        self.ssh = QPushButton("SSH")
        self.sftp = QPushButton("File Transfer")

        self.nomachine.clicked.connect(self.launch_nx)
        self.rstudio.clicked.connect(self.launch_rstudio)
        self.jupyter.clicked.connect(self.launch_jupyter)
        self.ssh.clicked.connect(self.launch_ssh)
        self.sftp.clicked.connect(self.launch_sftp)

        self.hbox_url = QGridLayout()
        self.hbox_url.addWidget(self.nomachine,0,0)
        self.hbox_url.addWidget(self.rstudio,0,1)
        self.hbox_url.addWidget(self.jupyter,1,0)
        self.hbox_url.addWidget(self.ssh, 1, 1)
        self.hbox_url.addWidget(self.sftp, 2, 0)

        self.refresh = QPushButton("Refresh")
        self.refresh.clicked.connect(self.fn_status)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox_manipulate)
        self.vbox.addLayout(self.grid_manipulate)
        self.vbox.addLayout(self.hbox_attr)
        self.vbox.addLayout(self.grid_attr)
        self.vbox.addWidget(self.refresh)
        self.vbox.addLayout(self.hbox_serv)
        self.vbox.addLayout(self.hbox_url)

        self.setLayout(self.vbox)
        self.fn_status()


    def fn_status(self):

        global settings

        if settings.getParam('os') == 'Linux':
            self.rstudio.setEnabled(True)
            self.jupyter.setEnabled(True)
        elif settings.getParam('os') == 'Windows':
            self.rstudio.setEnabled(False)
            self.jupyter.setEnabled(False)


        self.id_ec2 = settings.getParam('ec2_id')
        self.session = settings.getSession()

        self.i = settings.getInstance()
        if self.i == None:
            print("please setup api keys")

        try:
            state = self.i.state["Name"]
            self.status.setText(state)

            self.instance_type.clear()

            for x in self.instance_types.values:
                self.instance_type.addItem(x[1],x[2])

            current_type = self.instance_types.loc[self.instance_types.id ==self.i.instance_type].values
            self.instance_type.setCurrentText(current_type[0][1])

            tags = functions.tagsToDict(self.i.tags)
            #print(tags)
            self.name.setText(tags["Name"])
            self.type.setText(self.i.instance_type)
            self.price.setText(functions.get_price(self.i.instance_type))
        except:
            self.name.setText("Invalid ID")
        try:
            self.ip.setText(settings.getIP())
        except:
            self.ip.setText("")

    def fn_prender(self):
        self.i.start()
        while self.i.state["Name"] != "running":
            print(".", end="")
            self.status.setText(self.i.state["Name"])
            time.sleep(2)
            self.i.reload()
        self.fn_status()

    def fn_apagar(self):
        self.i.stop()
        time.sleep(2)
        self.i.reload()
        self.status.setText(self.i.state["Name"])

    def fn_reset(self):
        functions.run_script(self.i,'reboot')


    def fn_set_type(self):
        if (self.i.state["Name"] == "stopped"):
            #print(self.instance_type.currentData())
            self.i.modify_attribute(Attribute='instanceType', Value=self.instance_type.currentData())
        self.fn_status()

    def launch_nx(self):
        global settings
        if settings.getParam('os') == 'Linux':
            file = functions.setNxXML(self.ip.text())
            params =  [
                '--session-conf={}'.format(file),
                '--sessionid=20181207145907927',
                '--no-menu',
                '--no-session-edit',
                '--tray-icon',
                '--clipboard=both',
                '--dpi=96',
                '--add-to-known-hosts']
            if platform.system() == 'Windows':
                subprocess.Popen(["C:\\Program Files (x86)\\x2goclient\\x2goclient.exe"]+params + ["--disable-pulse"])
            else:
                subprocess.Popen(["x2goclient"] + params)
            pass
        else:
            params = ["/v:"+self.ip.text()]
            subprocess.Popen(["mstsc"] + params)


    def launch_rstudio(self):
        QDesktopServices.openUrl(
            "http://" + self.ip.text() + ":8787/")

    def launch_jupyter(self):
        QDesktopServices.openUrl(
            "http://" + self.ip.text() + ":8000/")

    def launch_ssh(self):
        ip =  self.ip.text()
        user = settings.getParam('user')

        if platform.system() == 'Windows':
            subprocess.Popen( [functions.resource_path(os.path.join('files','putty.exe')), user + '@' + ip] )
        else:
            cmd = ' ssh  -o "StrictHostKeyChecking no" ' + user + '@' + ip + ' &'
            if shutil.which('sshpass') != None:
                cmd = "sshpass -p '{}' ".format(settings.getParam('ec2_passwd')) + cmd
            if shutil.which('konsole') != None:
                os.system('konsole -e ' + cmd)
            elif shutil.which('xfce4-terminal') != None:
                os.system('xfce4-terminal -x ' + cmd)
            elif shutil.which('gnome-terminal') != None:
                os.system('gnome-terminal ' + cmd)
            elif shutil.which('xterm') != None:
                os.system('xterm -e ' + cmd)

    def launch_sftp(self):
        ip =  self.ip.text()
        if settings.getParam("os") == "Windows":
            user = "Administrator"
        else:
            user = settings.getParam('user')

        if platform.system() == 'Windows':
            subprocess.Popen( ["winscp", user +':' + settings.getParam("ec2_passwd") + '@' + ip] )
        else:
            os.system( 'dolphin sftp://'+ user +':' + settings.getParam("ec2_passwd") + '@' + ip + ' &')

