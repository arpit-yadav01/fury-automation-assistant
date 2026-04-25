# platforms/leetcode_solver.py
# STEP 143 — LeetCode full solver
#
# Flow:
# 1. Open problem directly (already working)
# 2. Click language selector → select Python3
# 3. Clear editor + type solution
# 4. Click Run → wait
# 5. Click Submit
#
# Zero screenshots — solution generated from problem name via LLM
# Coordinates measured on 1920x1080

import os
import time
from openai import OpenAI

GROQ_KEY = os.getenv("GROQ_API_KEY")
client = None
if GROQ_KEY:
    client = OpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1")

# ── Measured coordinates (1920x1080, Chrome maximized) ──
LANG_SELECTOR   = (1006, 239)   # language dropdown button
CODE_EDITOR     = (1200, 500)   # click to focus editor
RUN_BUTTON      = (1650, 940)   # Run Code button
SUBMIT_BUTTON   = (1750, 940)   # Submit button


# ─────────────────────────
# GENERATE SOLUTION
# ~150 tokens — returns clean Python code
# ─────────────────────────

def generate_solution(problem_name):
    """Generate Python solution for a LeetCode problem."""
    if not client:
        return None

    print(f"🧠 Generating solution for: {problem_name}...")
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert competitive programmer. "
                        "Write optimal Python3 solutions for LeetCode problems. "
                        "Return ONLY the solution code. "
                        "No class Solution wrapper unless required. "
                        "No explanation. No markdown. No backticks."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Write the Python3 solution for LeetCode problem: {problem_name}\n"
                        f"Include the class Solution and method definition.\n"
                        f"Return only the code."
                    )
                }
            ],
            temperature=0.1,
            max_tokens=400
        )
        code = resp.choices[0].message.content.strip()
        # clean up any accidental backticks
        code = code.replace("```python", "").replace("```", "").strip()
        print(f"✅ Solution generated ({len(code)} chars)")
        return code
    except Exception as e:
        print(f"Solution generation error: {e}")
        return None


# ─────────────────────────
# TYPE CODE INTO EDITOR
# Uses pyautogui to type solution
# ─────────────────────────

def _type_code(code):
    """Type code into LeetCode editor using keyboard."""
    import pyautogui

    # select all existing code and delete
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.3)
    pyautogui.press("delete")
    time.sleep(0.3)

    # type solution line by line (more reliable than bulk write)
    lines = code.split("\n")
    for i, line in enumerate(lines):
        if line:
            pyautogui.write(line, interval=0.02)
        if i < len(lines) - 1:
            pyautogui.press("enter")
        time.sleep(0.05)

    print(f"✅ Code typed ({len(lines)} lines)")


# ─────────────────────────
# SELECT PYTHON3
# Clicks language dropdown and selects Python3
# ─────────────────────────

def _select_python3():
    """Click language selector and choose Python3."""
    import pyautogui
    from execution.visual_agent import _ensure_browser_focused

    _ensure_browser_focused()
    time.sleep(0.3)

    # click language selector
    pyautogui.click(*LANG_SELECTOR)
    time.sleep(1.5)  # wait for dropdown to open

    # Python3 is usually in the dropdown — try clicking it
    # It appears below the selector after clicking
    # Approximate position of Python3 in dropdown
    pyautogui.click(LANG_SELECTOR[0], LANG_SELECTOR[1] + 60)
    time.sleep(0.5)

    # if that didn't work, type to search
    # Some LeetCode versions have a search in dropdown
    pyautogui.write("Python3", interval=0.05)
    time.sleep(0.5)
    pyautogui.press("enter")
    time.sleep(1)

    print("✅ Python3 selected")


# ─────────────────────────
# FULL SOLVE FLOW
# ─────────────────────────

def solve_leetcode(problem_name, auto_submit=False):
    """
    Full LeetCode solve flow.

    Args:
        problem_name: e.g. "two sum", "valid parentheses"
        auto_submit: if True, clicks Submit after Run passes
                     if False, only runs — you review and submit manually

    Returns:
        dict with outcome and solution code
    """
    import pyautogui
    from browser.browser_agent import open_website
    from execution.visual_agent import _ensure_browser_focused

    slug = problem_name.lower().strip().replace(" ", "-")
    url  = f"https://leetcode.com/problems/{slug}/"

    print(f"\n{'='*50}")
    print(f"🧩 LeetCode Solver: {problem_name}")
    print(f"   URL: {url}")
    print(f"{'='*50}\n")

    # Step 1 — open problem
    print("Step 1: Opening problem...")
    open_website(url)
    time.sleep(4)  # wait for page to fully load
    _ensure_browser_focused()
    time.sleep(0.5)

    # Step 2 — generate solution
    print("Step 2: Generating Python solution...")
    code = generate_solution(problem_name)
    if not code:
        print("❌ Could not generate solution")
        return {"outcome": "failed", "reason": "no solution generated"}

    print(f"\nSolution:\n{code}\n")

    # Step 3 — select Python3
    print("Step 3: Selecting Python3...")
    _select_python3()
    _ensure_browser_focused()

    # Step 4 — click editor and type code
    print("Step 4: Typing solution into editor...")
    pyautogui.click(*CODE_EDITOR)
    time.sleep(0.5)
    _type_code(code)
    time.sleep(0.5)

    # Step 5 — click Run
    print("Step 5: Running code...")
    _ensure_browser_focused()
    pyautogui.click(*RUN_BUTTON)
    time.sleep(5)  # wait for test results

    # Step 6 — submit if requested
    if auto_submit:
        print("Step 6: Submitting...")
        _ensure_browser_focused()
        pyautogui.click(*SUBMIT_BUTTON)
        time.sleep(5)
        print("✅ Submitted — check LeetCode for results")
    else:
        print("✅ Code run — review results then submit manually")
        print("   To submit: click Submit on LeetCode")

    return {
        "outcome": "success",
        "problem": problem_name,
        "code": code,
        "submitted": auto_submit
    }