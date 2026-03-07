# brain/command_parser.py

def parse_command(command):

    command = command.lower()

    # OPEN VSCODE
    if "open" in command and "vscode" in command:
        return {
            "intent": "open_app",
            "app": "vscode"
        }

    # OPEN CHROME
    if "open" in command and "chrome" in command:
        return {
            "intent": "open_app",
            "app": "chrome"
        }

    # WRITE PYTHON CODE
    if "write" in command and "python" in command:
        return {
            "intent": "write_code",
            "language": "python"
        }

    # UNKNOWN COMMAND
    return {
        "intent": "unknown"
    }