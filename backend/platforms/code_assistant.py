# developer/code_assistant.py
# STEP 142 — Code assistant
#
# Reads your actual code files from disk — no screenshots needed
# Works for any project, any language
#
# Usage:
#   explain backend/visual_agent.py
#   fix bug in fury.py
#   review frontend/src/App.jsx
#   add feature to platforms/youtube_agent.py: add playlist support
#   what does execution/visual_agent.py do

import os
from openai import OpenAI

GROQ_KEY = os.getenv("GROQ_API_KEY")
client = None
if GROQ_KEY:
    client = OpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1")

# Base path for Fury project
FURY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FURY_BACKEND = os.path.join(FURY_ROOT, "backend")

# File size limit — don't send huge files to LLM
MAX_FILE_CHARS = 4000


# -------------------------
# FILE READER
# -------------------------

def read_file(file_path):
    """
    Read a code file. Accepts:
    - absolute path: C:/projects/fury/backend/fury.py
    - relative to backend: fury.py
    - relative to backend: execution/visual_agent.py
    - relative to project: backend/execution/visual_agent.py
    """
    # try as given
    if os.path.exists(file_path):
        return _read(file_path)

    # try relative to backend
    candidate = os.path.join(FURY_BACKEND, file_path)
    if os.path.exists(candidate):
        return _read(candidate)

    # try relative to project root
    candidate = os.path.join(FURY_ROOT, file_path)
    if os.path.exists(candidate):
        return _read(candidate)

    return None, f"File not found: {file_path}"


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        # truncate if too large
        if len(content) > MAX_FILE_CHARS:
            content = (
                content[:MAX_FILE_CHARS] +
                f"\n\n... [truncated — {len(content) - MAX_FILE_CHARS} more chars]"
            )
        return content, None
    except Exception as e:
        return None, str(e)


# -------------------------
# LIST FILES IN PROJECT
# -------------------------

def list_project_files(directory=None, ext=None):
    """List code files in the project."""
    base = os.path.join(FURY_BACKEND, directory) if directory else FURY_BACKEND

    if not os.path.exists(base):
        return []

    files = []
    for root, dirs, filenames in os.walk(base):
        # skip hidden and cache dirs
        dirs[:] = [d for d in dirs if not d.startswith((".", "__pycache__", "node_modules"))]
        for fname in filenames:
            if ext and not fname.endswith(ext):
                continue
            if fname.endswith((".py", ".js", ".jsx", ".ts", ".tsx", ".json", ".yaml", ".md")):
                rel = os.path.relpath(os.path.join(root, fname), FURY_BACKEND)
                files.append(rel)

    return sorted(files)


# -------------------------
# EXPLAIN FILE
# Reads file and explains what it does
# -------------------------

def explain_file(file_path):
    """Read a file and explain what it does in plain English."""
    content, err = read_file(file_path)
    if err:
        print(f"❌ {err}")
        return None

    if not client:
        print("❌ No LLM client")
        return None

    print(f"\n📖 Reading: {file_path}")
    print(f"   Size: {len(content)} chars")

    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior developer. Explain code clearly and concisely. "
                        "Focus on: what it does, key functions, how it fits in the project."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Explain this file: {file_path}\n\n"
                        f"```python\n{content}\n```\n\n"
                        f"Explain in 3-5 sentences what this file does and its key functions."
                    )
                }
            ],
            temperature=0.2,
            max_tokens=300
        )
        explanation = resp.choices[0].message.content.strip()
        print(f"\n💡 {file_path}")
        print("─" * 50)
        print(explanation)
        print()
        return explanation
    except Exception as e:
        print(f"❌ LLM error: {e}")
        return None


# -------------------------
# FIX BUG
# Reads file, finds the bug, suggests fix
# -------------------------

def fix_bug(file_path, error_message=None):
    """
    Read a file and suggest a bug fix.
    Optionally pass the error message to get a targeted fix.
    """
    content, err = read_file(file_path)
    if err:
        print(f"❌ {err}")
        return None

    if not client:
        return None

    print(f"\n🔍 Analyzing: {file_path}")

    user_msg = f"File: {file_path}\n\n```\n{content}\n```\n\n"
    if error_message:
        user_msg += f"Error: {error_message}\n\n"
    user_msg += "Find the bug and provide the exact fix. Show only the changed lines."

    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior developer. "
                        "Find bugs and provide minimal, precise fixes. "
                        "Show only what needs to change, not the whole file."
                    )
                },
                {"role": "user", "content": user_msg}
            ],
            temperature=0.1,
            max_tokens=500
        )
        fix = resp.choices[0].message.content.strip()
        print(f"\n🔧 Bug fix for {file_path}")
        print("─" * 50)
        print(fix)
        print()
        return fix
    except Exception as e:
        print(f"❌ LLM error: {e}")
        return None


# -------------------------
# REVIEW CODE
# Reads file and gives code review
# -------------------------

def review_code(file_path):
    """Give a code review — improvements, issues, suggestions."""
    content, err = read_file(file_path)
    if err:
        print(f"❌ {err}")
        return None

    if not client:
        return None

    print(f"\n🔎 Reviewing: {file_path}")

    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior code reviewer. "
                        "Give practical, actionable feedback. "
                        "Be concise — top 3 issues max."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Review this code: {file_path}\n\n"
                        f"```\n{content}\n```\n\n"
                        f"Give top 3 issues or improvements. Be specific."
                    )
                }
            ],
            temperature=0.2,
            max_tokens=400
        )
        review = resp.choices[0].message.content.strip()
        print(f"\n📝 Code review: {file_path}")
        print("─" * 50)
        print(review)
        print()
        return review
    except Exception as e:
        print(f"❌ LLM error: {e}")
        return None


# -------------------------
# ADD FEATURE
# Reads file and suggests how to add a feature
# -------------------------

def add_feature(file_path, feature_description):
    """Suggest code to add a feature to a file."""
    content, err = read_file(file_path)
    if err:
        print(f"❌ {err}")
        return None

    if not client:
        return None

    print(f"\n⚡ Adding feature to: {file_path}")
    print(f"   Feature: {feature_description}")

    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior developer. "
                        "Add features cleanly. Show only the new/changed code."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"File: {file_path}\n\n"
                        f"```\n{content}\n```\n\n"
                        f"Add this feature: {feature_description}\n\n"
                        f"Show only the new/modified code with brief explanation."
                    )
                }
            ],
            temperature=0.2,
            max_tokens=600
        )
        suggestion = resp.choices[0].message.content.strip()
        print(f"\n✨ Feature suggestion")
        print("─" * 50)
        print(suggestion)
        print()
        return suggestion
    except Exception as e:
        print(f"❌ LLM error: {e}")
        return None


# -------------------------
# ANSWER QUESTION ABOUT CODE
# -------------------------

def ask_about_code(file_path, question):
    """Answer any question about a code file."""
    content, err = read_file(file_path)
    if err:
        print(f"❌ {err}")
        return None

    if not client:
        return None

    print(f"\n❓ Question about {file_path}: {question}")

    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Answer questions about code clearly and concisely."
                },
                {
                    "role": "user",
                    "content": (
                        f"File: {file_path}\n\n"
                        f"```\n{content}\n```\n\n"
                        f"Question: {question}"
                    )
                }
            ],
            temperature=0.2,
            max_tokens=400
        )
        answer = resp.choices[0].message.content.strip()
        print(f"\n💬 Answer")
        print("─" * 50)
        print(answer)
        print()
        return answer
    except Exception as e:
        print(f"❌ LLM error: {e}")
        return None


# -------------------------
# SMART ROUTER
# Parses natural language code commands
# -------------------------

def handle_code_command(command):
    """
    Route natural language code commands.

    Examples:
      explain fury.py
      fix bug in execution/visual_agent.py
      review platforms/job_desc_parser.py
      add feature to youtube_agent.py: add playlist support
      what does brain/tab_intelligence.py do
      list files
      list python files in platforms
    """
    cmd = command.strip()
    cmd_lower = cmd.lower()

    # list files
    if cmd_lower.startswith("list files") or cmd_lower == "list":
        directory = None
        if " in " in cmd_lower:
            directory = cmd_lower.split(" in ", 1)[1].strip()
        files = list_project_files(directory)
        if files:
            print(f"\n📁 Project files ({len(files)} found):")
            for f in files[:30]:
                print(f"  {f}")
            if len(files) > 30:
                print(f"  ... and {len(files)-30} more")
        else:
            print("No files found")
        return

    # explain / what does
    for prefix in ["explain ", "what does ", "what is "]:
        if cmd_lower.startswith(prefix):
            file_path = cmd[len(prefix):].strip().replace(" do", "").replace(" does", "")
            explain_file(file_path)
            return

    # fix bug
    if "fix bug" in cmd_lower or "fix error" in cmd_lower or "debug " in cmd_lower:
        # extract file path
        for sep in [" in ", " for ", " "]:
            if sep in cmd_lower:
                parts = cmd.split(sep, 1)
                file_path = parts[-1].strip()
                fix_bug(file_path)
                return

    # review
    if cmd_lower.startswith("review "):
        file_path = cmd[7:].strip()
        review_code(file_path)
        return

    # add feature
    if cmd_lower.startswith("add ") and " to " in cmd_lower:
        # "add feature to file.py: description"
        if ":" in cmd:
            parts = cmd.split(":", 1)
            file_part = parts[0]
            feature   = parts[1].strip()
            # extract file from "add X to file.py"
            if " to " in file_part.lower():
                file_path = file_part.split(" to ", 1)[1].strip()
                add_feature(file_path, feature)
                return

    # question about file
    if " in " in cmd_lower and "?" in cmd:
        parts = cmd.split(" in ", 1)
        question  = parts[0].strip()
        file_path = parts[1].strip()
        ask_about_code(file_path, question)
        return

    # default — treat as question about fury.py
    print(f"❓ Code command: {cmd}")
    print("Try: explain fury.py / fix bug in X / review X / list files")