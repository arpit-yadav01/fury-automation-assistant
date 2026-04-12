# execution/visual_agent.py
# STEP 131 — Visual Agent Loop
#
# The core engine for Phase 10.
# Operates the PC like a human would:
#   1. Take screenshot
#   2. Understand what's on screen (vision_understanding)
#   3. Decide next action using LLM
#   4. Execute the action (ui_action_engine)
#   5. Verify progress was made
#   6. Repeat until goal is achieved or max steps reached
#
# This is what makes LeetCode, WhatsApp, job applications possible.
# Every Phase 10 agent runs ON TOP of this loop.

import os
import json
import re
import time
import base64
import cv2
from datetime import datetime
from openai import OpenAI

from vision.screen_capture import capture_screen
from automation.ui_action_engine import perform_ui_action
from brain.context_memory import memory as ctx

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
# CONSTANTS
# -------------------------

MAX_STEPS     = 20      # max actions per goal
MAX_STUCK     = 3       # stop if screen unchanged N times
STEP_DELAY    = 1.5     # seconds between steps
VISION_MODEL  = "meta-llama/llama-4-scout-17b-16e-instruct"

# -------------------------
# SYSTEM PROMPT
# -------------------------

AGENT_PROMPT = """You are Fury, an autonomous AI agent controlling a Windows PC.
You can see the current screen. Your job is to achieve the given goal step by step.

Given:
- goal: what you need to accomplish
- current_screen: description of what's on screen right now
- steps_taken: list of actions already performed
- step_number: which step you're on

Decide the SINGLE NEXT ACTION to take.

Return ONLY a JSON object. No explanation. No markdown. No backticks.

Format:
{
  "action": "<action type>",
  "reasoning": "<why this action>",
  "done": false,
  "failed": false,
  "failure_reason": null
}

Action types and their fields:
- open_url:    {"action": "open_url", "url": "https://..."}
- click:       {"action": "click", "x": 100, "y": 200}
- type:        {"action": "type", "text": "text to type"}
- press:       {"action": "press", "key": "enter"}
- wait:        {"action": "wait", "time": 2}
- scroll:      {"action": "scroll", "direction": "down", "amount": 3}
- hotkey:      {"action": "hotkey", "keys": ["ctrl", "a"]}
- done:        {"action": "done"} — use when goal is achieved
- failed:      {"action": "failed", "reason": "why"} — use if impossible

Rules:
- Always take the simplest action that moves toward the goal
- Use open_url to navigate to websites
- Use click with coordinates to click buttons or links
- Use type to enter text into fields
- Use press "enter" to submit forms
- Use wait when page needs to load
- Set done=true when the goal is fully achieved
- Set failed=true only if the goal is truly impossible
- Never repeat the same failed action more than once
- If stuck, try a different approach
"""


# -------------------------
# MAIN LOOP
# -------------------------

class VisualAgent:
    """
    The core visual agent loop.
    Give it a goal, it operates the PC until done.
    """

    def __init__(self):
        self.steps_taken = []
        self.goal = ""
        self.start_time = None
        self.last_screen_hash = None
        self.stuck_count = 0

    def run(self, goal, max_steps=MAX_STEPS, context=None):
        """
        Run the visual agent loop to achieve a goal.

        Args:
            goal: plain English goal e.g. "solve LeetCode problem 1"
            max_steps: maximum actions before giving up
            context: optional dict with extra context (account, url, etc.)

        Returns:
            dict with outcome, steps_taken, duration_ms
        """
        self.goal = goal
        self.steps_taken = []
        self.start_time = time.time()
        self.stuck_count = 0
        self.last_screen_hash = None

        print(f"\n{'='*50}")
        print(f"🤖 Visual Agent starting")
        print(f"   Goal: {goal}")
        print(f"{'='*50}\n")

        for step_num in range(1, max_steps + 1):

            print(f"\n--- Step {step_num}/{max_steps} ---")

            # 1. capture screen
            screen_img = capture_screen()
            if screen_img is None:
                print("No screen captured, retrying...")
                time.sleep(1)
                continue

            # 2. check if stuck (screen not changing)
            screen_hash = self._hash_screen(screen_img)
            if screen_hash == self.last_screen_hash:
                self.stuck_count += 1
                print(f"Screen unchanged ({self.stuck_count}/{MAX_STUCK})")
                if self.stuck_count >= MAX_STUCK:
                    print("Agent stuck — stopping")
                    return self._result("stuck")
            else:
                self.stuck_count = 0
                self.last_screen_hash = screen_hash

            # 3. understand screen
            screen_desc = self._understand_screen(screen_img)
            print(f"Screen: {screen_desc}")

            # 4. decide next action
            action = self._decide_action(
                goal=goal,
                screen_desc=screen_desc,
                screen_img=screen_img,
                step_num=step_num,
                context=context
            )

            if action is None:
                print("Could not decide action")
                continue

            print(f"Action: {action}")
            print(f"Reason: {action.get('reasoning', '?')}")

            # 5. check if done or failed
            if action.get("action") == "done" or action.get("done"):
                print(f"\n✅ Goal achieved: {goal}")
                self._record_step(action, screen_desc, success=True)
                return self._result("success")

            if action.get("action") == "failed" or action.get("failed"):
                reason = action.get("failure_reason") or action.get("reason", "unknown")
                print(f"\n❌ Agent failed: {reason}")
                return self._result("failed", reason)

            # 6. execute action
            success = self._execute(action)
            self._record_step(action, screen_desc, success=success)

            if not success:
                print(f"Action failed, continuing...")

            # 7. wait for screen to update
            time.sleep(STEP_DELAY)

        print(f"\n⏰ Max steps reached ({max_steps})")
        return self._result("max_steps")

    # -------------------------
    # SCREEN UNDERSTANDING
    # -------------------------

    def _understand_screen(self, img):
        """Get a plain English description of what's on screen."""
        try:
            b64 = self._encode_image(img)
            if not b64 or client is None:
                return self._ocr_describe(img)

            response = client.chat.completions.create(
                model=VISION_MODEL,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Describe this Windows screen in 1-2 sentences. "
                                "Include: what app is open, what's visible, "
                                "any input fields or buttons. Be specific and brief."
                            )
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
                        }
                    ]
                }],
                temperature=0.1,
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Screen understanding error: {e}")
            return self._ocr_describe(img)

    # -------------------------
    # ACTION DECISION
    # -------------------------

    def _decide_action(self, goal, screen_desc, screen_img, step_num, context=None):
        """Use LLM + vision to decide the next action."""
        if client is None:
            return None

        try:
            b64 = self._encode_image(screen_img)

            context_str = json.dumps(context) if context else "none"
            steps_summary = [
                f"Step {i+1}: {s['action'].get('action','?')} — {s['screen'][:50]}"
                for i, s in enumerate(self.steps_taken[-5:])  # last 5 steps
            ]

            user_content = [
                {
                    "type": "text",
                    "text": json.dumps({
                        "goal": goal,
                        "current_screen": screen_desc,
                        "step_number": step_num,
                        "steps_taken": steps_summary,
                        "extra_context": context_str
                    })
                }
            ]

            # add screenshot if available
            if b64:
                user_content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
                })

            response = client.chat.completions.create(
                model=VISION_MODEL,
                messages=[
                    {"role": "system", "content": AGENT_PROMPT},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.2,
                max_tokens=300
            )

            raw = response.choices[0].message.content.strip()
            raw = re.sub(r"```json", "", raw)
            raw = re.sub(r"```", "", raw)

            action = json.loads(raw)
            return action

        except Exception as e:
            print(f"Decision error: {e}")
            return None

    # -------------------------
    # ACTION EXECUTION
    # -------------------------

    def _execute(self, action):
        """Execute an action using ui_action_engine."""
        try:
            act = action.get("action")

            # handle scroll separately
            if act == "scroll":
                import pyautogui
                direction = action.get("direction", "down")
                amount = action.get("amount", 3)
                clicks = amount if direction == "down" else -amount
                pyautogui.scroll(clicks)
                return True

            # handle hotkey separately
            if act == "hotkey":
                import pyautogui
                keys = action.get("keys", [])
                if keys:
                    pyautogui.hotkey(*keys)
                return True

            # delegate everything else to existing ui_action_engine
            return perform_ui_action(action)

        except Exception as e:
            print(f"Execute error: {e}")
            return False

    # -------------------------
    # HELPERS
    # -------------------------

    def _record_step(self, action, screen_desc, success=True):
        self.steps_taken.append({
            "action": action,
            "screen": screen_desc,
            "success": success,
            "timestamp": str(datetime.now())
        })

    def _result(self, outcome, reason=None):
        duration_ms = int((time.time() - self.start_time) * 1000)
        result = {
            "goal": self.goal,
            "outcome": outcome,
            "steps": len(self.steps_taken),
            "steps_taken": self.steps_taken,
            "duration_ms": duration_ms,
            "reason": reason
        }
        self._print_summary(result)
        return result

    def _print_summary(self, result):
        print(f"\n{'='*50}")
        print(f"🤖 Visual Agent finished")
        print(f"   Goal    : {result['goal']}")
        print(f"   Outcome : {result['outcome']}")
        print(f"   Steps   : {result['steps']}")
        print(f"   Time    : {result['duration_ms']}ms")
        if result.get('reason'):
            print(f"   Reason  : {result['reason']}")
        print(f"{'='*50}\n")

    def _encode_image(self, img):
        try:
            h, w = img.shape[:2]
            if w > 1280:
                scale = 1280 / w
                img = cv2.resize(img, (1280, int(h * scale)))
            _, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 70])
            return base64.b64encode(buf).decode("utf-8")
        except:
            return None

    def _hash_screen(self, img):
        """Simple hash to detect if screen changed."""
        try:
            small = cv2.resize(img, (32, 32))
            gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
            return gray.tobytes()
        except:
            return None

    def _ocr_describe(self, img):
        """Fallback description using pytesseract."""
        try:
            import pytesseract
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            lines = [l.strip() for l in text.splitlines() if l.strip()][:3]
            return " | ".join(lines) if lines else "screen captured"
        except:
            return "screen captured"


# -------------------------
# GLOBAL INSTANCE
# -------------------------

visual_agent = VisualAgent()


# -------------------------
# CONVENIENCE FUNCTION
# -------------------------

def run_visual_goal(goal, context=None, max_steps=MAX_STEPS):
    """
    Run the visual agent to achieve a goal.
    This is the main entry point for all Phase 10 agents.

    Usage:
        from execution.visual_agent import run_visual_goal
        result = run_visual_goal("solve LeetCode problem 1")
        result = run_visual_goal("send WhatsApp message to John: hello")
        result = run_visual_goal("play lofi music on YouTube")
    """
    agent = VisualAgent()
    return agent.run(goal, max_steps=max_steps, context=context)