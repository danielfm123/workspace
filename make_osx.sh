#!/bin/bash
rm -rf build
rm -rf dist
pyi-makespec  --windowed --icon=ec2.ico --onefile --additional-hooks-dir=. --add-data "files/*:files" workspace.py
pyinstaller workspace.spec
tar -zcvf  workspace.tar.gz dist/
