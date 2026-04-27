# commands/platform_commands.py
# Handles: tabs, profile, leetcode, whatsapp, telegram, gmail
# Steps 134, 135, 136, 138, 139, 140, 143, 144


def handle(command, cmd):

    # ── STEP 134 — TABS ──────────────────────
    if cmd in ("tabs", "show tabs", "fury tabs"):
        from brain.tab_intelligence import print_open_tabs
        print_open_tabs()
        return True

    if cmd.startswith("switch to "):
        from brain.tab_intelligence import switch_to_tab
        switch_to_tab(cmd.replace("switch to ", "").strip())
        return True

    # ── STEP 135 — PROFILE ───────────────────
    if cmd in ("profile", "fury profile"):
        from brain.personal_profile import profile
        profile.show()
        return True

    if cmd == "fury profile reload":
        from brain.personal_profile import profile
        profile.reload()
        print("✅ Profile reloaded")
        return True

    # ── STEP 136 + 143 — LEETCODE ────────────
    if cmd.startswith("leetcode "):
        _handle_leetcode(command, cmd)
        return True

    # ── GMAIL ────────────────────────────────
    if cmd in ("check email", "read email", "gmail"):
        from execution.visual_agent import run_visual_goal
        run_visual_goal("open gmail inbox", context={"platform": "gmail"})
        return True

    if cmd.startswith("compose email "):
        rest  = command[14:].strip().split(" about ")
        to    = rest[0].replace("to ", "").strip()
        instr = rest[1].strip() if len(rest) > 1 else command[14:]
        from platforms.gmail_agent import gmail
        gmail.compose_with_ai(to, "Message from Arpit", instr)
        return True

    # ── WHATSAPP ─────────────────────────────
    if cmd.startswith("whatsapp ") or cmd.startswith("send whatsapp "):
        rest = command.replace("send whatsapp to ", "").replace("whatsapp ", "").strip()
        if ":" in rest:
            contact, message = rest.split(":", 1)
        else:
            parts = rest.split(" ", 1)
            contact = parts[0]
            message = parts[1] if len(parts) > 1 else ""
        from execution.visual_agent import run_visual_goal
        run_visual_goal(
            f"send whatsapp message to {contact.strip()}: {message.strip()}",
            context={"platform": "whatsapp", "contact": contact.strip()}
        )
        return True

    if cmd.startswith("read whatsapp "):
        from execution.visual_agent import run_visual_goal
        run_visual_goal(
            f"read whatsapp messages from {command[14:].strip()}",
            context={"platform": "whatsapp"}
        )
        return True

    if cmd in ("check whatsapp", "whatsapp unread"):
        from execution.visual_agent import run_visual_goal
        run_visual_goal("check whatsapp unread messages",
                        context={"platform": "whatsapp"})
        return True

    # ── TELEGRAM ─────────────────────────────
    if cmd.startswith("telegram ") or cmd.startswith("send telegram "):
        rest = command.replace("send telegram to ", "").replace("telegram ", "").strip()
        if ":" in rest:
            contact, message = rest.split(":", 1)
        else:
            parts = rest.split(" ", 1)
            contact = parts[0]
            message = parts[1] if len(parts) > 1 else ""
        from execution.visual_agent import run_visual_goal
        run_visual_goal(
            f"send telegram to {contact.strip()}: {message.strip()}",
            context={"platform": "telegram", "contact": contact.strip()}
        )
        return True

    if cmd in ("check telegram", "telegram unread"):
        from execution.visual_agent import run_visual_goal
        run_visual_goal("check telegram unread",
                        context={"platform": "telegram"})
        return True

    return False


def _handle_leetcode(command, cmd):
    """LeetCode — open / solve / submit."""
    problem = command[9:].strip()
    slug    = problem.lower().replace(" ", "-")

    if cmd.startswith("leetcode solve "):
        problem = command[15:].strip()
        from platforms.leetcode_solver import solve_leetcode
        print(f"\n🧩 Solving: {problem}")
        result = solve_leetcode(problem, auto_submit=False)
        print(f"Outcome: {result['outcome']}")

    elif cmd.startswith("leetcode submit "):
        problem = command[16:].strip()
        from platforms.leetcode_solver import solve_leetcode
        print(f"\n🧩 Solving + submitting: {problem}")
        result = solve_leetcode(problem, auto_submit=True)
        print(f"Outcome: {result['outcome']}")

    else:
        url = f"https://leetcode.com/problems/{slug}/"
        from execution.visual_agent import run_visual_goal
        print(f"\n🧩 LeetCode: {problem} → {url}")
        result = run_visual_goal(
            f"open leetcode problem {problem}",
            context={"platform": "leetcode", "slug": slug, "url": url}
        )
        print(f"Outcome: {result['outcome']} in {result['steps']} steps")