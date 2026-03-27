def analyze_code(code):

    if not code:
        return {}

    return {
        "lines": len(code.splitlines()),
        "has_print": "print" in code,
        "has_loop": "for" in code or "while" in code,
        "has_function": "def " in code,
    }