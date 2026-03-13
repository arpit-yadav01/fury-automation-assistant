# brain/ai_interpreter.py

def clean_query(text):

    words_to_remove = [
        "open",
        "and",
        "youtube",
        "google",
        "search",
        "for",
    ]

    for w in words_to_remove:
        text = text.replace(w, "")

    return text.strip()


def interpret_command(command):

    command = command.lower().strip()

    # -------------------------
    # YOUTUBE SEARCH
    # -------------------------

    if "youtube" in command and "search" in command:

        query = clean_query(command)

        return {
            "intent": "web_search",
            "site": "youtube",
            "query": query
        }

    # -------------------------
    # GOOGLE SEARCH
    # -------------------------

    if "google" in command or command.startswith("search"):

        query = clean_query(command)

        return {
            "intent": "web_search",
            "site": "google",
            "query": query
        }

    return None