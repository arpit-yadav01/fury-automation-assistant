# brain/command_parser.py

def parse_command(command):

    command = command.lower()

    # OPEN ANY APPLICATION
    if command.startswith("open"):

        app = command.replace("open", "", 1).strip()

        if app:

            return {
                "intent": "open_app",
                "app": app
            }

    # WRITE PYTHON CODE
    if "write" in command and "python" in command:

        return {
            "intent": "write_code",
            "language": "python"
        }

    return {"intent": "unknown"}