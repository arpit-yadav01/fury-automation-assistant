def fix_code(code):

    if not code:
        return code

    # basic fixes

    fixes = {
        "pritn": "print",
        "inpurt": "input",
    }

    for wrong, correct in fixes.items():
        code = code.replace(wrong, correct)

    return code