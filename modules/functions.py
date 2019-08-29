import re
import os
import sys
import paramiko
from os.path import expanduser
from modules import SettingsManager

import boto3
import json
from pkg_resources import resource_filename

settings = SettingsManager.settingsManager()

def tagsToDict(tags):
    return({x["Key"]: x["Value"] for x in tags})

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    path = os.path.join(base_path, relative_path)
    return(path)

def run_script(script):
    instance = settings.getInstance()
    print(instance.tags)
    if instance.state["Name"] == "running":
        try:
            print("Conectando")
            #key = paramiko.RSAKey.from_private_key_file(resource_path(os.path.join('files', 'lab_key')))
            ip = settings.getIP()
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=settings.getParam("user"),password=settings.getParam("ec2_passwd"))

            print("Ejecutando")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(script)
            print(ssh_stdout.read())
            ssh.close()
            return True
        except:
            return False
    else:
        return False

def upload_file(origin,destiny):
    instance = settings.getInstance()
    print(instance.tags)
    if instance.state["Name"] == "running":
        try:
            print("Conectando")
            #key = paramiko.RSAKey.from_private_key_file(resource_path(os.path.join('files', 'lab_key')))
            ip = settings.getIP()
            username = settings.getParam('user')
            password = settings.getParam("ec2_passwd")
            transport = paramiko.Transport((ip, 22))
            transport.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.put(origin,destiny)
            sftp.close()
            return True
        except:
            return False

    return False


def sudo(cmd):
    sudo = resource_path("files\elevate.exe ")
    command = sudo + cmd
    print(command)
    os.system(command)

def setNxXML(ip):
    with open(resource_path(os.path.join('files', 'sessions')),'r') as nx:
        nxs = nx.readlines()
    home = expanduser("~")

    nxs = [re.sub('@ip@',ip,x) for x in nxs ]
    #nxs = [re.sub('@export@', "C:\#1;", x) for x in nxs]

    nx_path = os.path.join(home,'.sessions')

    with open(nx_path,'w+') as nx:
        nx.writelines(nxs)

    return nx_path


# Search product filter
FLT = '[{{"Field": "tenancy", "Value": "shared", "Type": "TERM_MATCH"}},'\
      '{{"Field": "operatingSystem", "Value": "{o}", "Type": "TERM_MATCH"}},'\
      '{{"Field": "preInstalledSw", "Value": "NA", "Type": "TERM_MATCH"}},'\
      '{{"Field": "instanceType", "Value": "{t}", "Type": "TERM_MATCH"}},'\
      '{{"Field": "location", "Value": "{r}", "Type": "TERM_MATCH"}},' \
      '{{"Field": "capacitystatus", "Value":"Used", "Type": "TERM_MATCH" }}]'


# Get current AWS price for an on-demand instance
def get_price(instance, region='US East (N. Virginia)' ,os='Linux'):
    try:
        client = boto3.client('pricing',aws_access_key_id=settings.getParam("id"),aws_secret_access_key=settings.getParam("key"))
        f = FLT.format(r=region, t=instance, o=os)
        data = client.get_products(ServiceCode='AmazonEC2', Filters=json.loads(f))
        od = json.loads(data['PriceList'][0])['terms']['OnDemand']
        id1 = list(od)[0]
        id2 = list(od[id1]['priceDimensions'])[0]
        return od[id1]['priceDimensions'][id2]['pricePerUnit']['USD']
    except:
        return 'Price not found'

# Translate region code to region name
def get_region_name(region_code):
    default_region = 'EU (Ireland)'
    endpoint_file = resource_filename('botocore', 'data/endpoints.json')
    try:
        with open(endpoint_file, 'r') as f:
            data = json.load(f)
        return data['partitions'][0]['regions'][region_code]['description']
    except IOError:
        return default_region