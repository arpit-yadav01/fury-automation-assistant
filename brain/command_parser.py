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

    # TYPE / WRITE TEXT
    if command.startswith("type ") or command.startswith("write "):

        text = command.split(" ", 1)[1]

        return {
            "intent": "type_text",
            "text": text
        }

    return {"intent": "unknown"}