# vision/layout_parser.py

import cv2
import numpy as np
from vision.screen_capture import capture_screen


def parse_layout():
    """
    Detect all UI elements on screen.
    Returns list of elements with type, position, size.
    """

    img = capture_screen()

    if img is None:
        return []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elements = []

    # -------------------------
    # DETECT RECTANGLES (buttons, inputs, boxes)
    # -------------------------

    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:

        x, y, w, h = cv2.boundingRect(cnt)

        # filter noise — only reasonable UI element sizes
        if w < 20 or h < 10:
            continue

        if w > 1200 or h > 200:
            continue

        aspect = w / h

        # classify by shape
        if 1.5 <= aspect <= 8 and 20 <= h <= 50:
            element_type = "input_field"

        elif 1.5 <= aspect <= 6 and 20 <= h <= 45:
            element_type = "button"

        elif aspect > 8:
            element_type = "toolbar"

        else:
            element_type = "box"

        elements.append({
            "type": element_type,
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "cx": x + w // 2,
            "cy": y + h // 2,
        })

    return elements


def find_element_by_type(element_type):
    """Find first element matching type."""

    elements = parse_layout()

    for el in elements:
        if el["type"] == element_type:
            return el

    return None


def find_all_by_type(element_type):
    """Find all elements matching type."""

    elements = parse_layout()

    return [el for el in elements if el["type"] == element_type]


def save_debug_image(path="debug_layout.png"):
    """Save screenshot with detected elements drawn on it."""

    img = capture_screen()
    elements = parse_layout()

    colors = {
        "input_field": (0, 255, 0),
        "button":      (255, 0, 0),
        "toolbar":     (0, 0, 255),
        "box":         (128, 128, 128),
    }

    for el in elements:

        color = colors.get(el["type"], (200, 200, 200))

        cv2.rectangle(
            img,
            (el["x"], el["y"]),
            (el["x"] + el["w"], el["y"] + el["h"]),
            color,
            2
        )

        cv2.putText(
            img,
            el["type"],
            (el["x"], el["y"] - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            color,
            1
        )

    cv2.imwrite(path, img)
    print(f"Debug layout saved: {path}")