# vision/layout_detector.py

import cv2
from vision.screen_capture import capture_screen


def detect_layout(debug=False):

    img = capture_screen()

    if img is None:
        print("Screen capture failed")
        return []

    # -----------------------
    # PREPROCESS
    # -----------------------

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    elements = []

    # -----------------------
    # DETECT BOXES
    # -----------------------

    for cnt in contours:

        x, y, w, h = cv2.boundingRect(cnt)

        # filter noise
        if w > 50 and h > 20:

            cx = int(x + w / 2)
            cy = int(y + h / 2)

            elements.append({
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "center": (cx, cy)  # 🔥 important for Step 98
            })

    # -----------------------
    # DEBUG VISUALIZATION
    # -----------------------

    if debug:

        debug_img = img.copy()

        for el in elements:

            x = el["x"]
            y = el["y"]
            w = el["w"]
            h = el["h"]

            # draw box
            cv2.rectangle(
                debug_img,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # draw center
            cx, cy = el["center"]
            cv2.circle(debug_img, (cx, cy), 4, (0, 0, 255), -1)

        cv2.imshow("Fury Vision Debug", debug_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return elements