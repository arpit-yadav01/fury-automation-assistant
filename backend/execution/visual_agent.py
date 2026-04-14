# execution/visual_agent.py
# STEP 131 — Visual Agent Loop
# STEP 132 — Task Memory integrated

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

# STEP 132
from memory.task_memory import (
    save_task_state, clear_task_state,
    save_to_history, load_task_state
)

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

MAX_STEPS    = 20
MAX_STUCK    = 3
STEP_DELAY   = 2.0
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

SCREEN_W = 1920
SCREEN_H = 1080

# Exact YouTube search bar coordinates (measured at 1920x1080)
YOUTUBE_SEARCH_X = 588
YOUTUBE_SEARCH_Y = 145

# -------------------------
# SYSTEM PROMPT
# -------------------------

AGENT_PROMPT = f"""You are Fury, an autonomous AI agent on Windows at {SCREEN_W}x{SCREEN_H}.
Achieve the goal step by step.

COORDINATES:
- YouTube search bar: x={YOUTUBE_SEARCH_X}, y={YOUTUBE_SEARCH_Y}
- YouTube first video result: ~x=400, y=300
- YouTube second video: ~x=400, y=500

RULES:
1. Use open_url with direct search URL when possible — faster than clicking search bar
   e.g. https://www.youtube.com/results?search_query=lofi+music
2. After search results load, click a video thumbnail to play it
3. wait (time=3) after every open_url
4. Never repeat a failed action — try different approach
5. Set done=true when goal is achieved

Return ONLY JSON. No markdown.

{{
  "action": "<type>",
  "reasoning": "<one sentence>",
  "done": false,
  "failed": false,
  "failure_reason": null
}}

Actions:
- {{"action": "open_url", "url": "https://..."}}
- {{"action": "click", "x": {YOUTUBE_SEARCH_X}, "y": {YOUTUBE_SEARCH_Y}}}
- {{"action": "type", "text": "..."}}
- {{"action": "press", "key": "enter"}}
- {{"action": "wait", "time": 3}}
- {{"action": "scroll", "direction": "down", "amount": 3}}
- {{"action": "done"}}
- {{"action": "failed", "reason": "why"}}
"""

# -------------------------
# BROWSER FOCUS
# -------------------------

def _ensure_browser_focused(browser="chrome"):
    from automation.window_manager import force_focus_window, is_window_focused
    if is_window_focused(browser):
        return True
    print(f"Refocusing {browser}...")
    success = force_focus_window(browser, timeout=3)
    if success:
        time.sleep(0.5)
    return success


# -------------------------
# VISUAL AGENT
# -------------------------

class VisualAgent:

    def __init__(self):
        self.steps_taken = []
        self.goal = ""
        self.start_time = None
        self.last_screen_hash = None
        self.stuck_count = 0
        self.browser_mode = False
        self.resume_from = 0

    def run(self, goal, max_steps=MAX_STEPS, context=None, resume=False):
        """
        Run visual agent to achieve goal.

        Args:
            goal: plain English goal
            max_steps: max steps before giving up
            context: optional extra context
            resume: if True, tries to resume from saved state
        """
        # STEP 132 — check for resume
        if resume:
            saved = load_task_state()
            if saved and saved.get("goal") == goal:
                print(f"📂 Resuming from step {saved['step_num']}")
                self.steps_taken = saved.get("steps_taken", [])
                self.resume_from = saved.get("step_num", 0)
            else:
                resume = False

        self.goal = goal
        if not resume:
            self.steps_taken = []
            self.resume_from = 0
        self.start_time = time.time()
        self.stuck_count = 0
        self.last_screen_hash = None
        self.browser_mode = False

        print(f"\n{'='*50}")
        print(f"🤖 Visual Agent {'(resuming)' if resume else 'starting'}")
        print(f"   Goal: {goal}")
        print(f"{'='*50}\n")

        # STEP 132 — save initial state
        save_task_state(goal, self.steps_taken, 0, "running", context)

        for step_num in range(self.resume_from + 1, max_steps + 1):

            print(f"\n--- Step {step_num}/{max_steps} ---")

            if self.browser_mode:
                _ensure_browser_focused()
                time.sleep(0.3)

            screen_img = capture_screen()
            if screen_img is None:
                time.sleep(1)
                continue

            screen_hash = self._hash_screen(screen_img)
            if screen_hash == self.last_screen_hash:
                self.stuck_count += 1
                print(f"Screen unchanged ({self.stuck_count}/{MAX_STUCK})")
                if self.stuck_count >= MAX_STUCK:
                    if self.browser_mode:
                        _ensure_browser_focused()
                        time.sleep(1)
                        self.stuck_count = 0
                        continue
                    return self._finish("stuck", context)
            else:
                self.stuck_count = 0
                self.last_screen_hash = screen_hash

            screen_desc = self._understand_screen(screen_img)
            print(f"Screen: {screen_desc}")

            action = self._decide_action(
                goal=goal,
                screen_desc=screen_desc,
                screen_img=screen_img,
                step_num=step_num,
                context=context
            )

            if action is None:
                time.sleep(2)
                continue

            print(f"Action: {action.get('action')} | {action.get('reasoning','')}")

            if action.get("action") == "done" or action.get("done"):
                print(f"\n✅ Goal achieved!")
                self._record_step(action, screen_desc, success=True)
                # STEP 132 — save success state
                save_task_state(goal, self.steps_taken, step_num, "success", context)
                clear_task_state()
                return self._finish("success", context)

            if action.get("action") == "failed" or action.get("failed"):
                reason = action.get("failure_reason") or action.get("reason", "unknown")
                print(f"\n❌ Failed: {reason}")
                return self._finish("failed", context, reason)

            success = self._execute_smart(action)
            self._record_step(action, screen_desc, success=success)

            # STEP 132 — save state after every step
            save_task_state(goal, self.steps_taken, step_num, "running", context)

            if action.get("action") == "open_url":
                self.browser_mode = True
                print("Waiting for page load...")
                time.sleep(3)
                _ensure_browser_focused()

            time.sleep(STEP_DELAY)

        return self._finish("max_steps", context)

    # -------------------------
    # SMART EXECUTE
    # -------------------------

    def _execute_smart(self, action):
        act = action.get("action")

        if act == "click":
            try:
                import pyautogui
                x = action.get("x", YOUTUBE_SEARCH_X)
                y = action.get("y", YOUTUBE_SEARCH_Y)
                _ensure_browser_focused()
                time.sleep(0.2)
                pyautogui.click(x, y)
                print(f"Clicked ({x}, {y})")
                return True
            except Exception as e:
                print(f"Click error: {e}")
                return False

        if act == "type":
            try:
                import pyautogui
                text = action.get("text", "")
                pyautogui.write(text, interval=0.05)
                print(f"Typed: {text}")
                return True
            except Exception as e:
                print(f"Type error: {e}")
                return False

        if act == "scroll":
            import pyautogui
            direction = action.get("direction", "down")
            amount = action.get("amount", 3)
            pyautogui.scroll(amount if direction == "down" else -amount)
            return True

        if act == "hotkey":
            import pyautogui
            keys = action.get("keys", [])
            if keys:
                pyautogui.hotkey(*keys)
            return True

        try:
            return perform_ui_action(action)
        except Exception as e:
            print(f"Execute error: {e}")
            return False

    # -------------------------
    # SCREEN UNDERSTANDING
    # -------------------------

    def _understand_screen(self, img):
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
                                "Describe this screen in 1-2 sentences. "
                                "What app? What's visible? Buttons, search bars, videos? "
                                "Include pixel coordinates of key elements."
                            )
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
                        }
                    ]
                }],
                temperature=0.1,
                max_tokens=200
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return self._ocr_describe(img)

    # -------------------------
    # ACTION DECISION
    # -------------------------

    def _decide_action(self, goal, screen_desc, screen_img, step_num, context=None):
        if client is None:
            return None
        try:
            b64 = self._encode_image(screen_img)
            steps_summary = [
                f"{s['action'].get('action','?')}:{'ok' if s['success'] else 'fail'}"
                for s in self.steps_taken[-5:]
            ]

            user_content = [{
                "type": "text",
                "text": json.dumps({
                    "goal": goal,
                    "screen": screen_desc,
                    "step": step_num,
                    "history": steps_summary,
                    "context": context or {}
                })
            }]

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
            raw = re.sub(r"```json|```", "", raw)
            return json.loads(raw)

        except Exception as e:
            print(f"Decision error: {e}")
            return None

    # -------------------------
    # FINISH + HISTORY
    # -------------------------

    def _finish(self, outcome, context=None, reason=None):
        duration_ms = int((time.time() - self.start_time) * 1000)

        # STEP 132 — save to history
        save_to_history(
            goal=self.goal,
            outcome=outcome,
            steps=len(self.steps_taken),
            duration_ms=duration_ms,
            context=context
        )

        # clear running state if done
        if outcome in ("success", "failed"):
            clear_task_state()

        result = {
            "goal": self.goal,
            "outcome": outcome,
            "steps": len(self.steps_taken),
            "steps_taken": self.steps_taken,
            "duration_ms": duration_ms,
            "reason": reason
        }

        print(f"\n{'='*50}")
        print(f"🤖 Visual Agent — {outcome.upper()}")
        print(f"   Goal  : {self.goal}")
        print(f"   Steps : {len(self.steps_taken)}")
        print(f"   Time  : {duration_ms}ms")
        if reason:
            print(f"   Why   : {reason}")
        print(f"{'='*50}\n")

        return result

    # -------------------------
    # HELPERS
    # -------------------------

    def _record_step(self, action, screen_desc, success=True):
        self.steps_taken.append({
            "action": action,
            "screen": screen_desc[:100],
            "success": success,
            "timestamp": str(datetime.now())
        })

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
        try:
            small = cv2.resize(img, (32, 32))
            gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
            return gray.tobytes()
        except:
            return None

    def _ocr_describe(self, img):
        try:
            import pytesseract
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            lines = [l.strip() for l in text.splitlines() if l.strip()][:3]
            return " | ".join(lines) if lines else "screen captured"
        except:
            return "screen captured"


# -------------------------
# ENTRY POINTS
# -------------------------

def run_visual_goal(goal, context=None, max_steps=MAX_STEPS, resume=False):
    """
    Main entry point for Phase 10 agents.

    Examples:
        run_visual_goal("play lofi music on youtube")
        run_visual_goal("solve leetcode two sum", resume=True)
        run_visual_goal("send whatsapp to John: hello")
    """
    agent = VisualAgent()
    return agent.run(goal, max_steps=max_steps, context=context, resume=resume)


def resume_last_task():
    """Resume the last interrupted visual task."""
    from memory.task_memory import load_task_state
    state = load_task_state()
    if not state:
        print("No interrupted task found.")
        return None
    goal = state.get("goal")
    context = state.get("context")
    print(f"Resuming: {goal}")
    return run_visual_goal(goal, context=context, resume=True)