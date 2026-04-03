# vision/text_detection.py

import pytesseract
import cv2
from vision.screen_capture import capture_screen


def find_text_on_screen(target_text):

    try:
        img = capture_screen()

        if img is None:
            print("TextDetection → no screen")
            return None

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

        for i, text in enumerate(data["text"]):

            if target_text.lower() in text.lower():

                x = data["left"][i]
                y = data["top"][i]
                w = data["width"][i]
                h = data["height"][i]

                return {
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h
                }

        return None

    except Exception as e:
        print("Text detection error:", e)
        return None