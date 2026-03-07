# fury.py

from brain.command_parser import parse_command


def start_fury():

    print("=================================")
    print("🔥 FURY AI ASSISTANT STARTED")
    print("Type 'exit' to stop Fury")
    print("=================================")

    while True:

        command = input(">>> ")

        if command.lower() == "exit":
            print("Shutting down Fury...")
            break

        # SEND COMMAND TO PARSER
        task = parse_command(command)

        print("Parsed Command:", task)


if __name__ == "__main__":
    start_fury()