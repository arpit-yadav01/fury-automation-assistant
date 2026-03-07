# automation/software_control.py

import subprocess

def open_application(app):

    if app == "chrome":
        subprocess.Popen(
            ["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"]
        )

    elif app == "vscode":
        subprocess.Popen(["code"])

    else:
        print(f"Application {app} not supported yet")