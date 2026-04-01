def score_object(obj, keyword=None):

    score = 0

    # Size importance
    w = obj.get("w", 0)
    h = obj.get("h", 0)
    area = w * h

    score += area / 1000

    # Center bias (screen center ≈ better target)
    cx = obj.get("x", 0) + w / 2
    cy = obj.get("y", 0) + h / 2

    dist = abs(cx - 960) + abs(cy - 540)
    score -= dist / 50

    return score


def select_best_target(objects, keyword=None):

    if not objects:
        return None

    best = None
    best_score = -999999

    for obj in objects:

        s = score_object(obj, keyword)

        if s > best_score:
            best_score = s
            best = obj

    return best