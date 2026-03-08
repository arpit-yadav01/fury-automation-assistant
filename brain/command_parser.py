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

    # WRITE PYTHON HELLO WORLD PROGRAM
    if "hello world" in command and "python" in command:

        return {
            "intent": "generate_code",
            "language": "python",
            "task": "hello_world"
        }

    return {"intent": "unknown"}