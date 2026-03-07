# automation/software_control.py

import subprocess


def open_application(app):

    try:

        aliases = {
            "calculator": "calc",
            "calc": "calc",
            "notepad": "notepad",
            "chrome": "chrome",
            "edge": "msedge",
            "vscode": "code",
            "setting": "ms-settings:",
            "settings": "ms-settings:",
            "outlook": "msedge --app=https://outlook.office.com",
            "docker": r'"C:\Program Files\Docker\Docker\Docker Desktop.exe"',
            "docker desktop": r'"C:\Program Files\Docker\Docker\Docker Desktop.exe"'
        }

        command = aliases.get(app, app)

        print(f"Launching {command}...")

        subprocess.Popen(f'start "" {command}', shell=True)

    except Exception as e:

        print("Failed to open application:", e)