# brain/decision_engine.py


def decide_action(options):

    if not options:
        return None

    # pick first valid option
    for opt in options:
        if isinstance(opt, dict):
            return opt

    return options[0]