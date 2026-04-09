from brain.context_memory import memory
from brain.pattern_engine import get_frequent_command


def enrich_command(command):

    if not isinstance(command, str):
        return command

    cmd = command.lower().strip()

    # -------------------------
    # CASE 1 — vague commands
    # -------------------------

    if cmd in ["play something", "play music", "play"]:

        patterns = get_frequent_command()

        for p, count in patterns:

            if "youtube" in p and "music" in p:
                return "open youtube and search music"

            if "youtube" in p:
                return p

        return "open youtube and search music"

    # -------------------------
    # CASE 2 — search without site
    # -------------------------

    if cmd.startswith("search"):

        site = memory.get_site()

        if site == "youtube":
            return f"open youtube and {cmd}"

        if site == "google":
            return f"open google and {cmd}"

    return command