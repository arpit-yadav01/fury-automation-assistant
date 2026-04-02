import pyautogui


def click_xy(x, y, delay=0.2):
    try:
        pyautogui.moveTo(int(x), int(y), duration=delay)
        pyautogui.click()
        return True
    except Exception as e:
        print("Click XY failed:", e)
        return False


def click_box(box):

    if not box:
        return False

    try:
        x = box.get("x")
        y = box.get("y")
        w = box.get("w")
        h = box.get("h")

        if None in [x, y, w, h]:
            return False

        cx = int(x + w / 2)
        cy = int(y + h / 2)

        return click_xy(cx, cy)

    except Exception as e:
        print("Click box failed:", e)
        return False


def safe_click(x=None, y=None, box=None):

    if box:
        if click_box(box):
            return True

    if x is not None and y is not None:
        if click_xy(x, y):
            return True

    try:
        pyautogui.click()
        return True
    except Exception as e:
        print("Fallback click failed:", e)
        return False