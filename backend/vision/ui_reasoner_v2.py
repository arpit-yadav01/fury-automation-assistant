# vision/ui_reasoner_v2.py

from vision.text_detection import find_text_on_screen


def find_and_validate(text):

    pos = find_text_on_screen(text)

    if not pos:
        return None

    x, y = pos

    return {
        "x": x,
        "y": y,
        "valid": True,
    }


def exists(text):

    return find_text_on_screen(text) is not None