# brain/command_parser.py

from brain.ai_interpreter import interpret_command


def parse_command(command):

    command = command.lower().strip()

    # -----------------------------
    # WEBSITE COMMANDS (SPECIFIC FIRST)
    # -----------------------------

    # OPEN GOOGLE
    if "open google" in command:
        return {
            "intent": "open_website",
            "url": "https://www.google.com"
        }

    # OPEN YOUTUBE
    if "open youtube" in command:
        return {
            "intent": "open_website",
            "url": "https://www.youtube.com"
        }

    # GOOGLE SEARCH
    if command.startswith("search"):
        query = command.replace("search", "").strip()

        url = f"https://www.google.com/search?q={query}"

        return {
            "intent": "open_website",
            "url": url
        }

    # -----------------------------
    # CODE GENERATION
    # -----------------------------

    if "hello world" in command and "python" in command:
        return {
            "intent": "generate_code",
            "language": "python",
            "task": "hello_world"
        }

    # -----------------------------
    # TEXT TYPING
    # -----------------------------

    if command.startswith("type ") or command.startswith("write "):
        text = command.split(" ", 1)[1]

        return {
            "intent": "type_text",
            "text": text
        }

    # -----------------------------
    # FILE CREATION
    # -----------------------------

    if command.startswith("create file"):
        words = command.split()

        if len(words) >= 3:
            filename = words[2]

            return {
                "intent": "create_file",
                "filename": filename
            }

    if "create python file" in command:
        return {
            "intent": "create_file",
            "filename": "main.py"
        }

    # -----------------------------
    # TERMINAL COMMANDS
    # -----------------------------

    if command.startswith("run command"):
        cmd = command.replace("run command", "").strip()

        return {
            "intent": "run_terminal",
            "command": cmd
        }

    if command.startswith("run python file"):
        filename = command.replace("run python file", "").strip()

        return {
            "intent": "run_terminal",
            "command": f"python {filename}"
        }

    if command.startswith("pip install"):
        return {
            "intent": "run_terminal",
            "command": command
        }

    # -----------------------------
    # DEVELOPER WORKFLOWS
    # -----------------------------

    if command.startswith("create react app"):
        words = command.split()

        if len(words) >= 4:
            project_name = words[3]

            return {
                "intent": "run_terminal",
                "command": f"npx create-react-app {project_name}"
            }

    if command == "npm install":
        return {
            "intent": "run_terminal",
            "command": "npm install"
        }

    if command == "npm start":
        return {
            "intent": "run_terminal",
            "command": "npm start"
        }

    # -----------------------------
    # OPEN APPLICATION (GENERIC LAST)
    # -----------------------------

    if command.startswith("open"):
        words = command.split(maxsplit=1)

        if len(words) > 1:
            app = words[1]

            return {
                "intent": "open_app",
                "app": app
            }

    # -----------------------------
    # AI INTERPRETATION FALLBACK
    # -----------------------------

    ai_result = interpret_command(command)

    if ai_result:
        return ai_result

    # -----------------------------
    # UNKNOWN COMMAND
    # -----------------------------

    return {"intent": "unknown"}