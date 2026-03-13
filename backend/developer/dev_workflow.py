# developer/dev_workflow.py

from automation.software_control import open_application
from automation.window_manager import focus_window
from automation.ui_engine import type_text, press, hotkey, wait
from developer.terminal_engine import run_terminal_command


# -----------------------
# OPEN VSCODE
# -----------------------

def open_vscode():

    print("Opening VS Code")

    open_application("vscode")

    # wait for vscode to open
    wait(3)

    # focus vscode window
    focus_window("Code")

    wait(1)


# -----------------------
# CREATE NEW FILE
# -----------------------

def create_new_file(filename):

    print("Creating new file:", filename)

    # make sure vscode focused
    focus_window("Code")

    wait(1)

    # create new file
    hotkey("ctrl", "n")

    wait(2)

    # open save dialog
    hotkey("ctrl", "s")

    wait(2)

    # type filename
    type_text(filename)

    wait(1)

    press("enter")

    wait(2)


# -----------------------
# WRITE CODE
# -----------------------

def write_code(code):

    print("Writing code")

    wait(1)

    type_text(code)

    wait(1)


# -----------------------
# SAVE FILE
# -----------------------

def save_file():

    print("Saving file")

    hotkey("ctrl", "s")

    wait(2)


# -----------------------
# RUN PYTHON FILE
# -----------------------

def run_python_file(filename):

    print("Running python file")

    focus_window("Code")

    wait(1)

    # open terminal in vscode
    hotkey("ctrl", "`")

    wait(2)

    run_terminal_command(f"python {filename}")

    wait(1)


# -----------------------
# RUN TERMINAL COMMAND
# -----------------------

def run_command(cmd):

    print("Running command:", cmd)

    focus_window("Code")

    wait(1)

    hotkey("ctrl", "`")

    wait(2)

    run_terminal_command(cmd)

    wait(1)