# automation/file_manager.py

import os


def create_file(filename):

    try:

        with open(filename, "w") as f:
            pass

        print(f"File created: {filename}")

    except Exception as e:

        print("Error creating file:", e)


def write_to_file(filename, content):

    try:

        with open(filename, "w") as f:
            f.write(content)

        print(f"Written to file: {filename}")

    except Exception as e:

        print("Error writing file:", e)