# memory/screen_memory.py

last_screen = None
last_elements = []


def store_screen(data):

    global last_screen
    last_screen = data


def get_last_screen():
    return last_screen


def store_elements(elements):

    global last_elements
    last_elements = elements


def get_last_elements():
    return last_elements