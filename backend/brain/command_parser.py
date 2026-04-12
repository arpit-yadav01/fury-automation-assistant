
# from brain.ai_interpreter import interpret_command
# from brain.llm_brain import interpret_with_llm


# def _attach_raw(result, command):

#     if not isinstance(result, dict):
#         return None

#     result["raw"] = command
#     return result


# def parse_command(command):

#     if not command:
#         return {"intent": "unknown", "raw": ""}

#     original = command
#     command = command.lower().strip()

#     # -----------------------------
#     # SCREEN
#     # -----------------------------

#     if "capture screen" in command or "analyze screen" in command:
#         return {"intent": "capture_screen", "raw": original}

#     # -----------------------------
#     # UI ANALYSIS
#     # -----------------------------

#     if "analyze ui" in command:
#         return {"intent": "analyze_ui", "raw": original}

#     # -----------------------------
#     # OPEN WEBSITE
#     # -----------------------------

#     if command == "open google":
#         return _attach_raw({
#             "intent": "open_website",
#             "url": "https://www.google.com",
#         }, original)

#     if command == "open youtube":
#         return _attach_raw({
#             "intent": "open_website",
#             "url": "https://www.youtube.com",
#         }, original)

#     # -----------------------------
#     # YOUTUBE SEARCH
#     # -----------------------------

#     if "youtube" in command and "search" in command:

#         query = command.replace("search", "").replace("youtube", "").strip()

#         return _attach_raw({
#             "intent": "web_search",
#             "site": "youtube",
#             "query": query,
#         }, original)

#     # -----------------------------
#     # GENERIC SEARCH
#     # -----------------------------

#     if command.startswith("search "):

#         query = command.replace("search", "").strip()

#         return _attach_raw({
#             "intent": "web_search",
#             "query": query,
#         }, original)

#     # -----------------------------
#     # DEV COMMANDS
#     # -----------------------------

#     if command.startswith("dev "):

#         cmd = command.replace("dev", "").strip()

#         return _attach_raw({
#             "intent": "dev",
#             "dev": cmd,
#         }, original)

#     # -----------------------------
#     # GENERATE CODE
#     # -----------------------------

#     if "generate" in command and "code" in command:

#         language = "python"

#         if "javascript" in command:
#             language = "javascript"
#         elif "java" in command:
#             language = "java"

#         task = command
#         for word in ["generate", "code", "in", language]:
#             task = task.replace(word, "")
#         task = task.strip()

#         return _attach_raw({
#             "intent": "generate_code",
#             "language": language,
#             "task": task,
#         }, original)

#     # -----------------------------
#     # CREATE FILE (FIXED)
#     # -----------------------------

#     if command.startswith("create "):

#         parts = command.split()

#         # "create file filename"
#         if len(parts) >= 3 and parts[1] == "file":
#             return _attach_raw({
#                 "intent": "create_file",
#                 "filename": parts[2],
#             }, original)

#         # "create test5342.py" — has file extension
#         if len(parts) == 2 and "." in parts[1]:
#             return _attach_raw({
#                 "intent": "create_file",
#                 "filename": parts[1],
#             }, original)

#         # "create python file"
#         if "python file" in command:
#             return _attach_raw({
#                 "intent": "create_file",
#                 "filename": "main.py",
#             }, original)

#     # -----------------------------
#     # WRITE / TYPE (FIXED)
#     # -----------------------------

#     if command.startswith("type ") or command.startswith("write "):

#         text = command.split(" ", 1)[1]

#         code_keywords = [
#             "python", "javascript", "java", "code", "function",
#             "bubble sort", "sort", "algorithm", "class", "loop",
#             "script", "program", "def ", "import "
#         ]

#         is_code = any(kw in text.lower() for kw in code_keywords)

#         if is_code:
#             return _attach_raw({
#                 "intent": "write_code",
#                 "task": text,
#             }, original)

#         return _attach_raw({
#             "intent": "type_text",
#             "text": text,
#         }, original)

#     # -----------------------------
#     # TERMINAL
#     # -----------------------------

#     if command.startswith("run command"):

#         cmd = command.replace("run command", "").strip()

#         return _attach_raw({
#             "intent": "run_terminal",
#             "command": cmd,
#         }, original)

#     if command.startswith("pip install"):

#         return _attach_raw({
#             "intent": "run_terminal",
#             "command": command,
#         }, original)

#     # -----------------------------
#     # OPEN APP
#     # -----------------------------

#     if command.startswith("open "):

#         app = command.replace("open", "").strip()

#         if app:
#             return _attach_raw({
#                 "intent": "open_app",
#                 "app": app,
#             }, original)

#     # -----------------------------
#     # AI INTERPRETER
#     # -----------------------------

#     ai_result = interpret_command(command)

#     if isinstance(ai_result, dict):
#         return _attach_raw(ai_result, original)

#     # -----------------------------
#     # LLM FALLBACK
#     # -----------------------------

#     llm_result = interpret_with_llm(command)

#     if isinstance(llm_result, dict):
#         return _attach_raw(llm_result, original)

#     # -----------------------------
#     # UNKNOWN
#     # -----------------------------

#     return {
#         "intent": "unknown",
#         "raw": original,
#     }


# brain/command_parser.py
# FIX 1: typo tolerance for "open" — catches "opne", "opem", "ope" etc.
# FIX 2: write_code and type_text now carry target_app so workflow
#         can open the app first if needed

from brain.ai_interpreter import interpret_command
from brain.llm_brain import interpret_with_llm


# -------------------------
# TYPO-TOLERANT OPEN DETECTOR
# -------------------------

# Common misspellings of "open" seen in logs
_OPEN_TYPOS = {"open", "opne", "opem", "ope", "oepn", "opeen"}

def _starts_with_open(command):
    """Returns (True, rest) if command starts with open or a known typo."""
    parts = command.split(" ", 1)
    if parts[0].lower() in _OPEN_TYPOS:
        return True, parts[1] if len(parts) > 1 else ""
    return False, ""


def _attach_raw(result, command):
    if not isinstance(result, dict):
        return None
    result["raw"] = command
    return result


# -------------------------
# MAIN PARSER
# -------------------------

def parse_command(command):

    if not command:
        return {"intent": "unknown", "raw": ""}

    original = command
    command = command.lower().strip()

    # -----------------------------
    # SCREEN
    # -----------------------------

    if "capture screen" in command or "analyze screen" in command:
        return {"intent": "capture_screen", "raw": original}

    # -----------------------------
    # UI ANALYSIS
    # -----------------------------

    if "analyze ui" in command:
        return {"intent": "analyze_ui", "raw": original}

    # -----------------------------
    # OPEN WEBSITE (exact)
    # -----------------------------

    if command == "open google":
        return _attach_raw({
            "intent": "open_website",
            "url": "https://www.google.com",
        }, original)

    if command == "open youtube":
        return _attach_raw({
            "intent": "open_website",
            "url": "https://www.youtube.com",
        }, original)

    # -----------------------------
    # YOUTUBE SEARCH
    # -----------------------------

    if "youtube" in command and "search" in command:
        query = command.replace("search", "").replace("youtube", "").strip()
        return _attach_raw({
            "intent": "web_search",
            "site": "youtube",
            "query": query,
        }, original)

    # -----------------------------
    # GENERIC SEARCH
    # -----------------------------

    if command.startswith("search "):
        query = command.replace("search", "").strip()
        return _attach_raw({
            "intent": "web_search",
            "query": query,
        }, original)

    # -----------------------------
    # DEV COMMANDS
    # -----------------------------

    if command.startswith("dev "):
        cmd = command.replace("dev", "").strip()
        return _attach_raw({
            "intent": "dev",
            "dev": cmd,
        }, original)

    # -----------------------------
    # GENERATE CODE
    # -----------------------------

    if "generate" in command and "code" in command:

        language = "python"
        if "javascript" in command:
            language = "javascript"
        elif "java" in command:
            language = "java"

        task = command
        for word in ["generate", "code", "in", language]:
            task = task.replace(word, "")
        task = task.strip()

        return _attach_raw({
            "intent": "generate_code",
            "language": language,
            "task": task,
        }, original)

    # -----------------------------
    # CREATE FILE
    # -----------------------------

    if command.startswith("create "):

        parts = command.split()

        if len(parts) >= 3 and parts[1] == "file":
            return _attach_raw({
                "intent": "create_file",
                "filename": parts[2],
            }, original)

        if len(parts) == 2 and "." in parts[1]:
            return _attach_raw({
                "intent": "create_file",
                "filename": parts[1],
            }, original)

        if "python file" in command:
            return _attach_raw({
                "intent": "create_file",
                "filename": "main.py",
            }, original)

    # -----------------------------
    # WRITE / TYPE
    # FIX: carry target_app so workflow knows where to type
    # -----------------------------

    if command.startswith("type ") or command.startswith("write "):

        text = command.split(" ", 1)[1]

        code_keywords = [
            "python", "javascript", "java", "code", "function",
            "bubble sort", "sort", "algorithm", "class", "loop",
            "script", "program", "def ", "import "
        ]

        is_code = any(kw in text.lower() for kw in code_keywords)

        # detect target app from context if mentioned earlier in sentence
        target_app = None
        app_hints = {"notepad": "notepad", "vscode": "vscode",
                     "code": "vscode", "word": "word"}
        for hint, app in app_hints.items():
            if hint in command:
                target_app = app
                break

        if is_code:
            return _attach_raw({
                "intent": "write_code",
                "task": text,
                "target_app": target_app,   # ✅ carries app context
            }, original)

        return _attach_raw({
            "intent": "type_text",
            "text": text,
            "target_app": target_app,       # ✅ carries app context
        }, original)

    # -----------------------------
    # TERMINAL
    # -----------------------------

    if command.startswith("run command"):
        cmd = command.replace("run command", "").strip()
        return _attach_raw({
            "intent": "run_terminal",
            "command": cmd,
        }, original)

    if command.startswith("pip install"):
        return _attach_raw({
            "intent": "run_terminal",
            "command": command,
        }, original)

    # -----------------------------
    # OPEN APP
    # FIX: typo-tolerant — catches "opne", "opem" etc.
    # -----------------------------

    is_open, rest = _starts_with_open(command)

    if is_open and rest:

        # filter out website keywords — those go to open_website not open_app
        web_keywords = ["google", "youtube", "http", "www", ".com"]

        if not any(w in rest for w in web_keywords):
            return _attach_raw({
                "intent": "open_app",
                "app": rest.strip(),
            }, original)

        # website fallback
        site_map = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
        }
        for name, url in site_map.items():
            if name in rest:
                return _attach_raw({
                    "intent": "open_website",
                    "url": url,
                }, original)

    # -----------------------------
    # AI INTERPRETER
    # -----------------------------

    ai_result = interpret_command(command)
    if isinstance(ai_result, dict):
        return _attach_raw(ai_result, original)

    # -----------------------------
    # LLM FALLBACK
    # -----------------------------

    llm_result = interpret_with_llm(command)
    if isinstance(llm_result, dict):
        return _attach_raw(llm_result, original)

    # -----------------------------
    # UNKNOWN
    # -----------------------------

    return {
        "intent": "unknown",
        "raw": original,
    }