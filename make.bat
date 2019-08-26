pyi-makespec  --windowed --icon=ec2.ico --onefile --additional-hooks-dir=. --add-data "files/*;files" workspace.py
pyinstaller workspace.spec

