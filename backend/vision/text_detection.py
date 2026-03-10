# vision/text_detection.py

import pytesseract
import cv2
from vision.screen_capture import capture_screen


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def find_text_on_screen(target_text):

    img = capture_screen()

    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    for i, text in enumerate(data["text"]):

        if target_text.lower() in text.lower():

            x = data["left"][i]
            y = data["top"][i]
            w = data["width"][i]
            h = data["height"][i]

            center_x = x + w // 2
            center_y = y + h // 2

            return (center_x, center_y)

    return None