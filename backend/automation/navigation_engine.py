from vision.layout_detector import detect_layout
from vision.target_selector import select_best_target
from automation.ui_click_engine import safe_click


def navigate_and_click(keyword=None):

    print("Navigation → scanning screen...")

    elements = detect_layout()

    if not elements:
        print("No UI elements found")
        return False

    target = select_best_target(elements, keyword=keyword)

    if not target:
        print("No target selected")
        return False

    print("Navigation → clicking:", target)

    return safe_click(box=target)