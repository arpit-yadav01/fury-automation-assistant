# brain/task_understanding.py


def understand_task(text):

    text = text.lower().strip()

    result = {
        "goal": None,
        "type": None,
        "name": None,
        "raw": text,
    }

    # -----------------------
    # BUILD PROJECT
    # -----------------------

    if "build" in text or "create" in text:

        result["goal"] = "build"

        if "python" in text:
            result["type"] = "python"

        if "react" in text:
            result["type"] = "react"

        if "node" in text:
            result["type"] = "node"

    # -----------------------
    # INSTALL
    # -----------------------

    if "install" in text:

        result["goal"] = "install"

        # ✅ extract package name
        words = text.split()

        if len(words) > 1:
            result["name"] = words[-1]

    # -----------------------
    # SOLVE
    # -----------------------

    if "solve" in text:

        result["goal"] = "solve"

    # -----------------------
    # UI ANALYSIS
    # -----------------------

    if "analyze ui" in text:
        result["goal"] = "analyze_ui"

    # -----------------------

    return result