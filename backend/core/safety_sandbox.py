# core/safety_sandbox.py
# STEP 125 — Safety sandbox
#
# Runs before ANY action executes.
# Three protection layers:
#   1. Blocked commands — never run no matter what
#   2. Risky actions — always ask before running
#   3. Sandbox mode — disables all destructive actions entirely
#
# Plugs into workflow_engine.py before each step executes
# and into agent_controller.py before agent.handle()
#
# When sharing Fury with others:
#   Set sandbox_mode: true in config.yaml
#   They can use Fury but it can never delete files or run dangerous commands

import os
from core.config_loader import cfg

# -------------------------
# BLOCKED FOREVER
# Never run these regardless of any setting
# -------------------------

BLOCKED_PATTERNS = [
    "format c:",
    "format c",
    "rm -rf /",
    "rm -rf",
    "del /f /s /q c:\\",
    "del /f /s /q",
    "rd /s /q c:\\",
    ":(){:|:&};",          # fork bomb
    "shutdown /r /f",
    "shutdown /s /f",
    "reg delete hklm",
    "reg delete hkcu",
    "cipher /w:c",
    "sfc /scannow",
    "bcdedit",
    "diskpart",
]

# -------------------------
# RISKY — ask before running
# -------------------------

RISKY_ACTIONS = {
    "terminal",        # any terminal command
    "run_terminal",
    "delete_file",
    "write_file",      # overwriting files
    "send_email",
    "run_python",      # running arbitrary python
    "pip_install",
}

RISKY_INTENTS = {
    "run_terminal",
    "delete_file",
    "send_email",
    "run_python",
}

# -------------------------
# SANDBOX BLOCKED ACTIONS
# These are blocked when sandbox_mode=true
# -------------------------

SANDBOX_BLOCKED = {
    "terminal",
    "run_terminal",
    "delete_file",
    "send_email",
    "run_python",
    "pip_install",
    "write_file",
}


# -------------------------
# MAIN CHECK FUNCTIONS
# -------------------------

def is_blocked(step):
    """
    Returns (True, reason) if step should NEVER run.
    Returns (False, None) if safe.

    Call this before executing any workflow step.
    """
    if not isinstance(step, dict):
        return False, None

    action = step.get("action", "")
    cmd = ""

    # extract command text
    if action == "terminal":
        cmd = step.get("cmd", "").lower()
    elif action == "skill":
        data = step.get("data", {})
        intent = data.get("intent", "")
        cmd = data.get("command", "").lower()

        # check sandbox mode
        if _sandbox_mode() and intent in SANDBOX_BLOCKED:
            return True, f"Sandbox mode: '{intent}' is disabled"

    # check blocked patterns
    for pattern in BLOCKED_PATTERNS:
        if pattern in cmd:
            return True, f"Blocked command pattern: '{pattern}'"

    # check sandbox on terminal
    if _sandbox_mode() and action in SANDBOX_BLOCKED:
        return True, f"Sandbox mode: '{action}' is disabled"

    return False, None


def is_risky(step):
    """
    Returns (True, reason) if step needs user confirmation.
    Returns (False, None) if safe to run without asking.

    Call this to decide whether to show a confirm prompt.
    """
    if not isinstance(step, dict):
        return False, None

    action = step.get("action", "")

    if action in RISKY_ACTIONS:
        cmd = step.get("cmd", "") or ""
        return True, f"Terminal command: '{cmd}'" if cmd else f"Action '{action}' requires confirmation"

    if action == "skill":
        data = step.get("data", {})
        intent = data.get("intent", "")
        if intent in RISKY_INTENTS:
            return True, f"Risky intent: '{intent}'"

    return False, None


def check_command(command):
    """
    Fast string-level check on raw command text.
    Used by final_core before planning.

    Returns (True, reason) if command should be blocked.
    Returns (False, None) if ok to proceed.
    """
    if not command or not isinstance(command, str):
        return False, None

    cmd = command.lower().strip()

    for pattern in BLOCKED_PATTERNS:
        if pattern in cmd:
            return True, f"Blocked: '{pattern}' is not allowed"

    return False, None


def confirm_risky(step, ask_fn=None):
    """
    Ask user to confirm a risky step.

    Args:
        step: the workflow step dict
        ask_fn: optional custom function to ask (default: input())

    Returns True if confirmed, False if cancelled.
    """
    _, reason = is_risky(step)

    print(f"\n⚠️  Fury: This action needs your confirmation")
    print(f"   Action : {step.get('action', '?')}")
    if reason:
        print(f"   Reason : {reason}")
    print("   Proceed? (yes / no)")

    if ask_fn:
        answer = ask_fn()
    else:
        answer = input(">>> ").strip().lower()

    return answer in ("yes", "y")


# -------------------------
# HELPERS
# -------------------------

def _sandbox_mode():
    try:
        return cfg.safety.sandbox_mode
    except:
        return False


def sandbox_is_on():
    return _sandbox_mode()


def get_blocked_commands():
    """Return the full blocked list — used by dashboard API."""
    try:
        extra = cfg.safety.blocked_commands or []
        return BLOCKED_PATTERNS + [str(c) for c in extra]
    except:
        return BLOCKED_PATTERNS