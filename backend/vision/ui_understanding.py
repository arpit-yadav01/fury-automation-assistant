# vision/ui_understanding.py

import pytesseract
import cv2
from vision.screen_capture import capture_screen
from vision.layout_parser import parse_layout, find_element_by_type

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def find_input_box():
    """Find the most likely input/search box on screen."""

    el = find_element_by_type("input_field")

    if el:
        print(f"Input box found at ({el['cx']}, {el['cy']})")
        return el

    print("No input box found")
    return None


def find_button(label=None):
    """
    Find a button on screen.
    If label given, find button near that text.
    """

    if label:
        return find_element_near_text(label, "button")

    return find_element_by_type("button")


def find_element_near_text(text, element_type=None):
    """
    Find UI element near a specific text label.
    Combines OCR text position + layout detection.
    """

    img = capture_screen()

    if img is None:
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(
        gray,
        output_type=pytesseract.Output.DICT
    )

    # find text position
    text_x = text_y = None

    for i, word in enumerate(data["text"]):

        if text.lower() in word.lower():
            text_x = data["left"][i] + data["width"][i] // 2
            text_y = data["top"][i] + data["height"][i] // 2
            break

    if text_x is None:
        print(f"Text '{text}' not found on screen")
        return None

    # find nearest element to text
    elements = parse_layout()

    if element_type:
        elements = [e for e in elements if e["type"] == element_type]

    if not elements:
        return None

    nearest = min(
        elements,
        key=lambda e: abs(e["cx"] - text_x) + abs(e["cy"] - text_y)
    )

    return nearest


def read_screen_text():
    """Read all text visible on screen."""

    img = capture_screen()

    if img is None:
        return ""

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray)

    return text.strip()


def is_text_visible(text):
    """Check if specific text is visible on screen."""

    screen_text = read_screen_text()

    return text.lower() in screen_text.lower()


def get_screen_state():
    """
    Returns a summary of what's currently on screen.
    Used by agents to understand context.
    """

    text = read_screen_text()
    elements = parse_layout()

    buttons = [e for e in elements if e["type"] == "button"]
    inputs = [e for e in elements if e["type"] == "input_field"]

    return {
        "text": text[:500],
        "button_count": len(buttons),
        "input_count": len(inputs),
        "has_search": "search" in text.lower(),
        "has_error": "error" in text.lower(),
        "elements": elements[:20],
    }