# brain/command_parser.py

def parse_command(command):

    command = command.lower()

    # OPEN APPLICATION
    if command.startswith("open"):

        words = command.split(maxsplit=1)

        if len(words) > 1:

            app = words[1]

            return {
                "intent": "open_app",
                "app": app
            }

    # PYTHON HELLO WORLD PROGRAM
    if "hello world" in command and "python" in command:

        return {
            "intent": "generate_code",
            "language": "python",
            "task": "hello_world"
        }

    # TYPE TEXT
    if command.startswith("type ") or command.startswith("write "):

        text = command.split(" ", 1)[1]

        return {
            "intent": "type_text",
            "text": text
        }

    # CREATE FILE
    if command.startswith("create file"):

        words = command.split()

        if len(words) >= 3:

            filename = words[2]

            return {
                "intent": "create_file",
                "filename": filename
            }

    # CREATE PYTHON FILE
    if "create python file" in command:

        return {
            "intent": "create_file",
            "filename": "main.py"
        }

    # RUN TERMINAL COMMAND
    if command.startswith("run command"):

        cmd = command.replace("run command", "").strip()

        return {
            "intent": "run_terminal",
            "command": cmd
        }

    # RUN PYTHON FILE
    if command.startswith("run python file"):

        filename = command.replace("run python file", "").strip()

        return {
            "intent": "run_terminal",
            "command": f"python {filename}"
        }

    # INSTALL PYTHON PACKAGE
    if command.startswith("pip install"):

        return {
            "intent": "run_terminal",
            "command": command
        }


            # CREATE REACT APP
    if command.startswith("create react app"):

        words = command.split()

        if len(words) >= 4:

            project_name = words[3]

            return {
                "intent": "run_terminal",
                "command": f"npx create-react-app {project_name}"
            }

    # RUN NPM INSTALL
    if command == "npm install":

        return {
            "intent": "run_terminal",
            "command": "npm install"
        }

    # RUN NPM START
    if command == "npm start":

        return {
            "intent": "run_terminal",
            "command": "npm start"
        }

    return {"intent": "unknown"}