# core/thinking_engine_v2.py
# STEP 111 — Chain-of-thought reasoning (FIXED)
#
# KEY RULE: final_command must ALWAYS equal the original command.
# think() adds reasoning context but never rewrites the command string.
# Downstream parsers (command_parser, task_planner) depend on exact phrasing.

import os
import json
import re
from openai import OpenAI

# -------------------------
# SAME CLIENT AS llm_brain.py
# -------------------------

GROQ_KEY = os.getenv("GROQ_API_KEY")

client = None
if GROQ_KEY:
    client = OpenAI(
        api_key=GROQ_KEY,
        base_url="https://api.groq.com/openai/v1"
    )

# -------------------------
# VAGUE COMMAND DETECTOR
# -------------------------

VAGUE_COMMANDS = [
    "do something",
    "do something useful",
    "help me",
    "help",
    "do it",
    "start",
    "go",
    "run it",
    "do that",
    "do the thing",
    "something",
]

def is_vague(command):
    cmd = command.lower().strip()
    if cmd in VAGUE_COMMANDS:
        return True
    words = cmd.split()
    action_words = [
        "open", "create", "search", "write", "run", "type",
        "install", "build", "generate", "capture", "analyze",
        "play", "close", "delete", "copy", "move", "send"
    ]
    if len(words) <= 3 and not any(a in cmd for a in action_words):
        return True
    return False


# -------------------------
# CHAIN-OF-THOUGHT PROMPT
# -------------------------

SYSTEM_PROMPT = """You are Fury's reasoning engine.
A user gave a command. Think step by step to understand what they want.

Return ONLY a JSON object. No explanation. No markdown. No backticks.

JSON format:
{
  "goal": "<what the user actually wants in one sentence>",
  "ambiguous": true or false,
  "clarification_needed": "<question to ask user if ambiguous, else null>",
  "steps": [
    "<step 1 in plain English>",
    "<step 2 in plain English>"
  ]
}

Rules:
- ambiguous = true only if the command is genuinely unclear or missing key info
- If command is clear and actionable, set ambiguous=false
- steps must be plain English, not code
- Do NOT rewrite or rephrase the original command
- Keep steps simple — what a human would do to complete this task
"""

# -------------------------
# MAIN FUNCTION
# -------------------------

def think(command):
    """
    Chain-of-thought reasoning over a command.

    Returns a thought dict:
    {
        "original": str,
        "goal": str,
        "ambiguous": bool,
        "clarification_needed": str or None,
        "steps": list,
        "final_command": str   <- ALWAYS equals original command, never rewritten
    }

    Falls back silently if LLM fails — original command passes through unchanged.
    """

    if not command or not isinstance(command, str):
        return _fallback(command)

    if client is None:
        print("ThinkingEngine: no LLM client, skipping")
        return _fallback(command)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": command}
            ],
            temperature=0.2,
            max_tokens=300
        )

        raw = response.choices[0].message.content.strip()
        raw = re.sub(r"```json", "", raw)
        raw = re.sub(r"```", "", raw)

        thought = json.loads(raw)

        # CRITICAL: always preserve original command — never let LLM rewrite it
        thought["original"] = command
        thought["final_command"] = command

        _print_thought(thought)
        return thought

    except Exception as e:
        print(f"ThinkingEngine error: {e}")
        return _fallback(command)


# -------------------------
# HELPERS
# -------------------------

def _fallback(command):
    return {
        "original": command,
        "goal": command,
        "ambiguous": False,
        "clarification_needed": None,
        "steps": [command],
        "final_command": command
    }


def _print_thought(thought):
    print("\n--- Fury Thinking ---")
    print(f"Goal    : {thought.get('goal')}")
    print(f"Steps   : {thought.get('steps')}")
    if thought.get("ambiguous"):
        print(f"Unclear : {thought.get('clarification_needed')}")
    print(f"Command : {thought.get('final_command')}")
    print("---------------------\n")