# commands/code_commands.py
# Handles: code assistant, screen watcher
# Steps 142, 145


def handle(command, cmd):

    # ── STEP 142 — CODE ASSISTANT ────────────
    if cmd.startswith("explain ") and any(
        cmd.endswith(e) for e in [".py", ".js", ".jsx", ".ts", ".tsx", ".yaml", ".json"]
    ):
        from developer.code_assistant import explain_file
        explain_file(command[8:].strip())
        return True

    if cmd.startswith("fix bug in ") or cmd.startswith("fix error in "):
        fp = cmd.replace("fix bug in ", "").replace("fix error in ", "").strip()
        from developer.code_assistant import fix_bug
        fix_bug(fp)
        return True

    if cmd.startswith("review ") and "." in cmd:
        from developer.code_assistant import review_code
        review_code(command[7:].strip())
        return True

    if cmd in ("list files",) or cmd.startswith("list files in "):
        from developer.code_assistant import handle_code_command
        handle_code_command(command)
        return True

    if cmd.startswith("code "):
        from developer.code_assistant import handle_code_command
        handle_code_command(command[5:].strip())
        return True

    # ── STEP 145 — SCREEN WATCHER ────────────
    if (cmd.startswith("watch ") or
        cmd in ("stop watching", "watch status") or
        cmd.startswith("alert me when ") or
        cmd.startswith("notify when ")):
        from developer.screen_watcher import handle_watch_command
        handle_watch_command(command)
        return True

    return False