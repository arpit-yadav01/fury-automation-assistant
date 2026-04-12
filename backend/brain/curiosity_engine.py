# brain/curiosity_engine.py
# STEP 115 — Curiosity engine
#
# Fury asks a smart clarifying question when context is missing.
# Reads ContextMemory to know what's already known,
# then asks only about what's genuinely needed to complete the task.
#
# Plugs into final_core.py — runs after think(), before create_plan()
# Only fires when confidence is low AND a key field is missing.

import os
import json
import re
from openai import OpenAI

from brain.context_memory import memory

# -------------------------
# CLIENT
# -------------------------

GROQ_KEY = os.getenv("GROQ_API_KEY")

client = None
if GROQ_KEY:
    client = OpenAI(
        api_key=GROQ_KEY,
        base_url="https://api.groq.com/openai/v1"
    )

# -------------------------
# WHAT FURY ALREADY KNOWS
# -------------------------

def _get_current_context():
    return {
        "active_app": memory.get_app(),
        "active_window": memory.get_window(),
        "last_site": memory.get_site(),
        "last_file": memory.get_file(),
        "last_action": memory.get_action(),
    }


# -------------------------
# FAST LOCAL CHECK
# — no LLM needed for obvious cases
# -------------------------

def _needs_clarification_local(command):
    """
    Quick rule-based check for commands that are obviously incomplete.
    Returns a question string or None.
    """
    cmd = command.lower().strip()

    # "send email" — to whom?
    if "send email" in cmd and "to" not in cmd:
        return "Who should I send the email to?"

    # "create file" with no name
    if cmd in ["create file", "make file", "new file"]:
        return "What should the file be named?"

    # "search" with nothing after it
    if cmd in ["search", "search for", "google"]:
        return "What do you want to search for?"

    # "open" with nothing after it
    if cmd in ["open", "launch", "start"]:
        return "What app or website should I open?"

    # "write code" with no task
    if cmd in ["write code", "generate code", "write a program"]:
        return "What should the code do?"

    # "type" with nothing after it
    if cmd in ["type", "type text", "write"]:
        return "What text should I type?"

    return None


# -------------------------
# PROMPT
# -------------------------

SYSTEM_PROMPT = """You are Fury's curiosity engine.
A user gave a command. You know what context Fury already has.
Decide if Fury needs to ask ONE clarifying question before proceeding.

Return ONLY a JSON object. No explanation. No markdown. No backticks.

Format:
{
  "needs_clarification": true or false,
  "question": "<single short question to ask, or null>",
  "missing_field": "<what info is missing: target, filename, query, app, content, or null>"
}

Rules:
- needs_clarification = true ONLY if a key piece of info is truly missing
- If the command is clear enough to execute, needs_clarification = false
- Ask ONE question maximum — the most important missing piece
- Question must be short and specific (under 10 words)
- Do NOT ask if context_memory already has the answer
- Common missing fields: target app, filename, search query, text content
"""


# -------------------------
# MAIN FUNCTION
# -------------------------

def should_ask(command, thought=None):
    """
    Decide if Fury should ask a clarifying question.

    Args:
        command: the current command string
        thought: optional thought dict from thinking_engine_v2

    Returns:
        question string if clarification needed, else None
    """

    if not command or not isinstance(command, str):
        return None

    # fast local check first — no LLM cost
    local_q = _needs_clarification_local(command)
    if local_q:
        return local_q

    # if thinking engine already flagged ambiguity, trust it
    if thought and thought.get("ambiguous") and thought.get("clarification_needed"):
        return thought.get("clarification_needed")

    # skip LLM for clearly actionable commands
    if _is_clearly_actionable(command):
        return None

    if client is None:
        return None

    ctx = _get_current_context()

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": json.dumps({
                        "command": command,
                        "current_context": ctx
                    })
                }
            ],
            temperature=0.1,
            max_tokens=150
        )

        raw = response.choices[0].message.content.strip()
        raw = re.sub(r"```json", "", raw)
        raw = re.sub(r"```", "", raw)

        result = json.loads(raw)

        if result.get("needs_clarification") and result.get("question"):
            print(f"CuriosityEngine: missing {result.get('missing_field')}")
            return result.get("question")

        return None

    except Exception as e:
        print(f"CuriosityEngine error: {e}")
        return None


# -------------------------
# HELPER
# -------------------------

def _is_clearly_actionable(command):
    """
    Returns True if command has enough info to act on immediately.
    Avoids unnecessary LLM calls for clear commands.
    """
    cmd = command.lower().strip()
    clear_patterns = [
        "open youtube", "open google", "open notepad", "open vscode",
        "search ", "create ", "open ", "type ", "write ",
        "run ", "install ", "pip install", "capture screen",
    ]
    return any(cmd.startswith(p) or p in cmd for p in clear_patterns)