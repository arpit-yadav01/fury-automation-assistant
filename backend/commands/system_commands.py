# commands/system_commands.py
# Handles: permissions, debug stats, help


def handle(command, cmd):

    # ── PERMISSIONS ───────────────────────────
    if cmd in ("permissions", "show permissions"):
        from core.permission_system import show_permissions
        show_permissions()
        return True

    if cmd.startswith("fury permission grant "):
        from core.permission_system import grant_permission
        grant_permission(cmd.replace("fury permission grant ", "").strip())
        return True

    if cmd.startswith("fury permission deny "):
        from core.permission_system import deny_permission
        deny_permission(cmd.replace("fury permission deny ", "").strip())
        return True

    if cmd == "fury permission reset":
        from core.permission_system import reset_permissions
        reset_permissions()
        return True

    # ── DEBUG ─────────────────────────────────
    if cmd == "fury stats":
        from core.final_core import final_core
        final_core.show_stats()
        return True

    if cmd == "fury patterns":
        from core.final_core import final_core
        final_core.show_patterns()
        return True

    if cmd == "fury failures":
        from core.final_core import final_core
        final_core.show_failures()
        return True

    if cmd.startswith("fury knows "):
        from core.final_core import final_core
        final_core.what_do_i_know(cmd.replace("fury knows ", "").strip())
        return True

    # ── HELP ──────────────────────────────────
    if cmd == "fury help":
        print("""
=== FURY COMMANDS ===
exit / voice mode / text mode / jarvis mode

--- VISUAL AGENT ---
visual <goal>               e.g. visual play lofi on youtube
resume / visual history
decompose <goal>

--- LEETCODE ---
leetcode <problem>          open only
leetcode solve <problem>    generate + type + run
leetcode submit <problem>   generate + run + submit

--- JOB TOOLS (safe) ---
search jobs <role> <platform>
cover letter for <role> at <company>
write cover letter <role> <company>
draft email <email> <role> <company>
[paste any job description]

--- CODE ASSISTANT ---
explain <file.py>
fix bug in <file.py>
review <file.py>
list files / list files in <folder>
code <question about your code>

--- SCREEN WATCHER ---
watch for <keyword>
watch whatsapp messages
watch leetcode result
stop watching / watch status

--- MESSAGING ---
whatsapp <contact> <message>
check whatsapp
telegram <contact> <message>
check telegram
check email

--- PROFILE & TABS ---
profile / fury profile reload
tabs / switch to <platform>

--- PERMISSIONS ---
permissions
fury permission grant/deny <cap>

--- DEBUG ---
fury stats / fury patterns / fury failures
fury help
=====================
""")
        return True

    return False