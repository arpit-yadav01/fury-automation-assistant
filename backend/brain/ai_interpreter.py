# brain/ai_interpreter.py

def interpret_command(command):

    command = command.lower()

    # GOOGLE SEARCH
    if "google" in command or "search for" in command:

        query = command.replace("google", "").replace("search for", "").strip()

        return {
            "intent": "web_search",
            "site": "google",
            "query": query
        }

    # YOUTUBE SEARCH
    if "youtube" in command and "search" in command:

        query = command.replace("search", "").replace("youtube", "").strip()

        return {
            "intent": "web_search",
            "site": "youtube",
            "query": query
        }

    return None