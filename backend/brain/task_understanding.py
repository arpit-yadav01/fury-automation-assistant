def understand_task(text):

    if not text:
        return None

    text = text.lower().strip()

    result = {
        "goal": None,
        "type": None,
        "name": None,
        "raw": text,
    }

    # -----------------------
    # BUILD / CREATE
    # -----------------------

    if "build" in text or "create" in text:

        result["goal"] = "build"

        if "python" in text:
            result["type"] = "python"

        elif "react" in text:
            result["type"] = "react"

        elif "node" in text:
            result["type"] = "node"

    # -----------------------
    # INSTALL
    # -----------------------

    elif "install" in text:

        result["goal"] = "install"

    # -----------------------
    # SOLVE
    # -----------------------

    elif "solve" in text:

        result["goal"] = "solve"

    return result