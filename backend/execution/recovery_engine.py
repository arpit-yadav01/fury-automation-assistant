MAX_RETRIES = 2


def recover_action(action, attempt):

    if attempt >= MAX_RETRIES:
        return None

    if action.get("action") == "click":

        # fallback click (no box)
        return {
            "action": "click"
        }

    if action.get("action") == "type":
        return action

    return None