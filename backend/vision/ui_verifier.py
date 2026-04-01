import numpy as np
from vision.screen_capture import capture_screen


def compare_frames(img1, img2):

    if img1 is None or img2 is None:
        return False

    diff = np.sum(np.abs(img1.astype("int") - img2.astype("int")))

    return diff > 1000000


def verify_action(before, after):

    changed = compare_frames(before, after)

    return {
        "changed": changed,
        "success": changed
    }