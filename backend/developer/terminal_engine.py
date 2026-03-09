# developer/terminal_engine.py

import subprocess


def run_terminal_command(command):

    try:

        print(f"Running command: {command}")

        subprocess.run(command, shell=True)

    except Exception as e:

        print("Terminal command failed:", e)