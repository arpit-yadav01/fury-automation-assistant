from brain.ai_interpreter import interpret_command
from brain.llm_brain import interpret_with_llm


def _attach_raw(result, command):
    """helper to attach raw text"""
    if not isinstance(result, dict):
        return None

    result["raw"] = command
    return result


def parse_command(command):

    if not command:
        return {"intent": "unknown", "raw": ""}

    original = command
    command = command.lower().strip()

    # -----------------------------
    # STEP 97 — SCREEN MEMORY
    # -----------------------------

    if "capture screen" in command or "analyze screen" in command:
        return {
            "intent": "capture_screen",
            "raw": original,
        }

    # -----------------------------
    # STEP 82 — UI ANALYSIS
    # -----------------------------

    if "analyze ui" in command:
        return {
            "intent": "analyze_ui",
            "raw": original,
        }
    

    if "search youtube" in command:

        return {
            "intent": "auto_navigate",
            "keyword": "search",
            "raw": original,
    }

    if "search google" in command:

        return {
            "intent": "auto_navigate",
            "keyword": "search",
            "raw": original,
    }

    # -----------------------------
    # OPEN WEBSITE
    # -----------------------------

    if command == "open google":
        return _attach_raw(
            {
                "intent": "open_website",
                "url": "https://www.google.com",
            },
            original,
        )

    if command == "open youtube":
        return _attach_raw(
            {
                "intent": "open_website",
                "url": "https://www.youtube.com",
            },
            original,
        )

    # -----------------------------
    # SEARCH
    # -----------------------------

    if command.startswith("search "):

        query = command.replace("search", "").strip()

        return _attach_raw(
            {
                "intent": "web_search",
                "site": "google",
                "query": query,
            },
            original,
        )

    # -----------------------------
    # DEV COMMANDS
    # -----------------------------

    if command.startswith("dev "):

        cmd = command.replace("dev", "").strip()

        return _attach_raw(
            {
                "intent": "dev",
                "dev": cmd,
            },
            original,
        )

    # -----------------------------
    # GENERATE CODE
    # -----------------------------

    if "generate" in command and "code" in command:

        language = "python"

        if "javascript" in command:
            language = "javascript"

        if "java" in command:
            language = "java"

        task = command
        task = task.replace("generate", "")
        task = task.replace("code", "")
        task = task.replace("in", "")
        task = task.replace(language, "")
        task = task.strip()

        return _attach_raw(
            {
                "intent": "generate_code",
                "language": language,
                "task": task,
            },
            original,
        )

    # -----------------------------
    # TYPE / WRITE
    # -----------------------------

    if command.startswith("type ") or command.startswith("write "):

        text = command.split(" ", 1)[1]

        return _attach_raw(
            {
                "intent": "type_text",
                "text": text,
            },
            original,
        )

    # -----------------------------
    # CREATE FILE
    # -----------------------------

    if command.startswith("create file"):

        words = command.split()

        if len(words) >= 3:

            filename = words[2]

            return _attach_raw(
                {
                    "intent": "create_file",
                    "filename": filename,
                },
                original,
            )

    if "create python file" in command:

        return _attach_raw(
            {
                "intent": "create_file",
                "filename": "main.py",
            },
            original,
        )

    # -----------------------------
    # TERMINAL
    # -----------------------------

    if command.startswith("run command"):

        cmd = command.replace("run command", "").strip()

        return _attach_raw(
            {
                "intent": "run_terminal",
                "command": cmd,
            },
            original,
        )

    if command.startswith("pip install"):

        return _attach_raw(
            {
                "intent": "run_terminal",
                "command": command,
            },
            original,
        )

    # -----------------------------
    # OPEN APP
    # -----------------------------

    if command.startswith("open "):

        app = command.replace("open", "").strip()

        if app:
            return _attach_raw(
                {
                    "intent": "open_app",
                    "app": app,
                },
                original,
            )

    # -----------------------------
    # AI interpreter
    # -----------------------------

    ai_result = interpret_command(command)

    if isinstance(ai_result, dict):
        return _attach_raw(ai_result, original)

    # -----------------------------
    # LLM fallback
    # -----------------------------

    llm_result = interpret_with_llm(command)

    if isinstance(llm_result, dict):
        return _attach_raw(llm_result, original)
    

    if "navigate" in command or "auto click" in command:
        return {
            "intent": "auto_navigate",
            "raw": original,
    }

    # -----------------------------
    # UNKNOWN (IMPORTANT)
    # -----------------------------

    return {
        "intent": "unknown",
        "raw": original,
    }