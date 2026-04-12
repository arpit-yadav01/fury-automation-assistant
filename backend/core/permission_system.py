# core/permission_system.py
# STEP 126 — Permission system
#
# Like phone app permissions — each capability needs to be granted.
# Permissions are stored in memory/permissions.json
# First time Fury tries a capability, it asks the user.
# User can grant once, grant always, or deny.
#
# Capabilities:
#   file_write    — create or modify files
#   file_delete   — delete files
#   terminal      — run terminal/shell commands
#   browser       — open URLs, control browser
#   app_control   — open/close desktop applications
#   email         — send emails
#   screen_read   — capture and read screen content
#   code_execute  — run Python files
#   microphone    — use voice input
#
# Plugs into workflow_engine.py alongside safety_sandbox.py

import os
import json
from datetime import datetime

# -------------------------
# PATH
# -------------------------

_DIR = os.path.dirname(os.path.abspath(__file__))
PERMISSIONS_FILE = os.path.join(
    os.path.dirname(_DIR), "memory", "permissions.json"
)

# -------------------------
# CAPABILITY DEFINITIONS
# -------------------------

CAPABILITIES = {
    "file_write": {
        "label": "Create and write files",
        "description": "Fury wants to create or write to files on your computer",
        "actions": ["create_file", "write_file", "skill:write_code",
                    "skill:create_file", "skill:write_file"],
    },
    "file_delete": {
        "label": "Delete files",
        "description": "Fury wants to delete files from your computer",
        "actions": ["delete_file", "skill:delete_file"],
    },
    "terminal": {
        "label": "Run terminal commands",
        "description": "Fury wants to run commands in your terminal/shell",
        "actions": ["terminal", "skill:run_terminal"],
    },
    "browser": {
        "label": "Control browser",
        "description": "Fury wants to open URLs and control your browser",
        "actions": ["open_url", "skill:open_website", "skill:web_search"],
    },
    "app_control": {
        "label": "Open and close apps",
        "description": "Fury wants to open or close desktop applications",
        "actions": ["open_app", "skill:open_app"],
    },
    "email": {
        "label": "Send emails",
        "description": "Fury wants to send emails on your behalf",
        "actions": ["skill:send_email"],
    },
    "screen_read": {
        "label": "Read screen content",
        "description": "Fury wants to capture and analyze your screen",
        "actions": ["capture_screen", "skill:capture_screen"],
    },
    "code_execute": {
        "label": "Execute Python code",
        "description": "Fury wants to run Python files on your computer",
        "actions": ["skill:run_python"],
    },
    "type_text": {
        "label": "Type text into apps",
        "description": "Fury wants to type text into applications",
        "actions": ["type", "skill:type_text"],
    },
}

# map action → capability for fast lookup
_ACTION_TO_CAP = {}
for cap, info in CAPABILITIES.items():
    for action in info["actions"]:
        _ACTION_TO_CAP[action] = cap


# -------------------------
# PERMISSION VALUES
# -------------------------

GRANT_ALWAYS = "always"   # granted permanently
GRANT_ONCE   = "once"     # granted for this session only
DENY         = "deny"     # denied permanently
ASK          = "ask"      # ask every time (default)


# -------------------------
# LOAD / SAVE
# -------------------------

def _load():
    os.makedirs(os.path.dirname(PERMISSIONS_FILE), exist_ok=True)
    if not os.path.exists(PERMISSIONS_FILE):
        return {}
    try:
        with open(PERMISSIONS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def _save(data):
    os.makedirs(os.path.dirname(PERMISSIONS_FILE), exist_ok=True)
    with open(PERMISSIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)


# session grants (grant_once) — not persisted
_session_grants = set()


# -------------------------
# CORE CHECK
# -------------------------

def check_permission(action_key):
    """
    Check if Fury has permission to perform an action.

    Args:
        action_key: the action string e.g. "open_url", "skill:write_code"

    Returns:
        True  — allowed to proceed
        False — denied, stop execution
    """
    cap = _ACTION_TO_CAP.get(action_key)

    if cap is None:
        # unknown capability — allow by default
        return True

    # check session grants
    if cap in _session_grants:
        return True

    perms = _load()
    status = perms.get(cap, ASK)

    if status == GRANT_ALWAYS:
        return True

    if status == DENY:
        print(f"\n🚫 Fury: Permission denied for '{CAPABILITIES[cap]['label']}'")
        print(f"   To grant access, run: fury permission grant {cap}")
        return False

    if status == ASK:
        return _ask_permission(cap, perms)

    return True


def _ask_permission(cap, perms):
    """Ask user to grant permission for a capability."""
    info = CAPABILITIES[cap]

    print(f"\n🔐 Fury needs permission:")
    print(f"   {info['description']}")
    print(f"   Capability: {info['label']}")
    print()
    print("   Options:")
    print("   [1] Allow always  — remember this choice")
    print("   [2] Allow once    — just this time")
    print("   [3] Deny          — block this action")
    print()

    answer = input(">>> ").strip()

    if answer == "1":
        perms[cap] = GRANT_ALWAYS
        _save(perms)
        print(f"✅ Permission granted always for: {info['label']}")
        return True

    elif answer == "2":
        _session_grants.add(cap)
        print(f"✅ Permission granted once for: {info['label']}")
        return True

    elif answer == "3":
        perms[cap] = DENY
        _save(perms)
        print(f"🚫 Permission denied for: {info['label']}")
        return False

    else:
        # default deny on unknown input
        print(f"🚫 Permission denied (invalid input)")
        return False


# -------------------------
# STEP ACTION KEY BUILDER
# -------------------------

def get_action_key(step):
    """
    Build the action key for a workflow step.
    e.g. {"action": "skill", "data": {"intent": "write_code"}} → "skill:write_code"
    """
    if not isinstance(step, dict):
        return None

    action = step.get("action", "")

    if action == "skill":
        intent = step.get("data", {}).get("intent", "")
        return f"skill:{intent}" if intent else "skill"

    return action


# -------------------------
# MANAGEMENT COMMANDS
# -------------------------

def grant_permission(cap):
    """Grant always permission for a capability."""
    if cap not in CAPABILITIES:
        print(f"Unknown capability: {cap}")
        print(f"Available: {list(CAPABILITIES.keys())}")
        return
    perms = _load()
    perms[cap] = GRANT_ALWAYS
    _save(perms)
    print(f"✅ Granted always: {CAPABILITIES[cap]['label']}")


def deny_permission(cap):
    """Deny a capability."""
    if cap not in CAPABILITIES:
        print(f"Unknown capability: {cap}")
        return
    perms = _load()
    perms[cap] = DENY
    _save(perms)
    print(f"🚫 Denied: {CAPABILITIES[cap]['label']}")


def reset_permissions():
    """Reset all permissions to ask."""
    if os.path.exists(PERMISSIONS_FILE):
        os.remove(PERMISSIONS_FILE)
    _session_grants.clear()
    print("✅ All permissions reset to ask")


def show_permissions():
    """Print current permission state."""
    perms = _load()
    print("\n--- Fury Permissions ---")
    for cap, info in CAPABILITIES.items():
        status = perms.get(cap, ASK)
        icon = "✅" if status == GRANT_ALWAYS else "⏳" if status == ASK else "🚫"
        session = " (session)" if cap in _session_grants else ""
        print(f"  {icon} {info['label']:<30} {status}{session}")
    print("------------------------\n")


def get_permissions_dict():
    """Return permissions as dict — used by dashboard API."""
    perms = _load()
    result = {}
    for cap, info in CAPABILITIES.items():
        result[cap] = {
            "label": info["label"],
            "description": info["description"],
            "status": perms.get(cap, ASK),
            "session": cap in _session_grants,
        }
    return result