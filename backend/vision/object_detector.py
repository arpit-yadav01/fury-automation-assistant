import cv2
from vision.screen_capture import capture_screen


def detect_ui_objects():

    img = capture_screen()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    objects = []

    for cnt in contours:

        x, y, w, h = cv2.boundingRect(cnt)

        if w > 40 and h > 20:

            objects.append({
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "center": (x + w // 2, y + h // 2)
            })

    return objects