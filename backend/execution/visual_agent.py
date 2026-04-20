# # execution/visual_agent.py
# # STEP 131 — Visual Agent Loop
# # STEP 132 — Task Memory
# # STEP 134 — Tab Intelligence
# # STEP 135 — Personal Profile context

# import os
# import json
# import re
# import time
# import base64
# import cv2
# from datetime import datetime
# from openai import OpenAI

# from vision.screen_capture import capture_screen
# from automation.ui_action_engine import perform_ui_action
# from brain.context_memory import memory as ctx
# from memory.task_memory import (
#     save_task_state, clear_task_state,
#     save_to_history, load_task_state
# )

# GROQ_KEY = os.getenv("GROQ_API_KEY")
# client = None
# if GROQ_KEY:
#     client = OpenAI(
#         api_key=GROQ_KEY,
#         base_url="https://api.groq.com/openai/v1"
#     )

# MAX_STEPS    = 20
# MAX_STUCK    = 3
# STEP_DELAY   = 2.0
# VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

# SCREEN_W = 1920
# SCREEN_H = 1080
# YOUTUBE_SEARCH_X = 588
# YOUTUBE_SEARCH_Y = 145

# # -------------------------
# # KNOWN PLATFORMS
# # -------------------------

# PLATFORM_KEYWORDS = {
#     "leetcode":    "leetcode.com",
#     "naukri":      "naukri.com",
#     "indeed":      "indeed.com",
#     "internshala": "internshala.com",
#     "linkedin":    "linkedin.com",
#     "gmail":       "mail.google.com",
#     "whatsapp":    "web.whatsapp.com",
#     "telegram":    "web.telegram.org",
#     "youtube":     "youtube.com",
#     "github":      "github.com",
# }


# def _detect_platform(goal):
#     """Detect which platform a goal targets."""
#     goal_lower = goal.lower()
#     for platform, url in PLATFORM_KEYWORDS.items():
#         if platform in goal_lower or url in goal_lower:
#             return platform
#     return None


# # -------------------------
# # SYSTEM PROMPT BUILDER
# # Includes personal context when relevant
# # -------------------------

# def _build_prompt(context=None):
#     base = f"""You are Fury, an autonomous AI agent on Windows at {SCREEN_W}x{SCREEN_H}.
# Achieve the goal step by step.

# SCREEN COORDINATES:
# - YouTube search bar: x={YOUTUBE_SEARCH_X}, y={YOUTUBE_SEARCH_Y}
# - General search bar (top center): x=960, y=55
# - First result: ~x=400, y=300

# RULES:
# 1. Use open_url with direct search URL when faster
# 2. wait (time=3) after every open_url
# 3. Click elements before typing into them
# 4. Never repeat failed action — try differently
# 5. Set done=true when goal is achieved

# Return ONLY JSON. No markdown.

# {{
#   "action": "<type>",
#   "reasoning": "<one sentence>",
#   "done": false,
#   "failed": false,
#   "failure_reason": null
# }}

# Actions:
# - {{"action": "open_url", "url": "https://..."}}
# - {{"action": "click", "x": 960, "y": 55}}
# - {{"action": "type", "text": "..."}}
# - {{"action": "press", "key": "enter"}}
# - {{"action": "wait", "time": 3}}
# - {{"action": "scroll", "direction": "down", "amount": 3}}
# - {{"action": "done"}}
# - {{"action": "failed", "reason": "why"}}
# """

#     # add personal context if available
#     if context:
#         ctx_lines = []
#         if context.get("name"):
#             ctx_lines.append(f"User's name: {context['name']}")
#         if context.get("email"):
#             ctx_lines.append(f"User's email: {context['email']}")
#         if context.get("phone"):
#             ctx_lines.append(f"User's phone: {context['phone']}")
#         if context.get("role"):
#             ctx_lines.append(f"Applying for: {context['role']}")
#         if context.get("skills_summary"):
#             ctx_lines.append(f"Skills: {context['skills_summary']}")
#         if ctx_lines:
#             base += "\nUSER CONTEXT (use this to fill forms):\n"
#             base += "\n".join(ctx_lines)

#     return base


# # -------------------------
# # BROWSER FOCUS
# # -------------------------

# def _ensure_browser_focused(browser="chrome"):
#     from automation.window_manager import force_focus_window, is_window_focused
#     if is_window_focused(browser):
#         return True
#     print(f"Refocusing {browser}...")
#     success = force_focus_window(browser, timeout=3)
#     if success:
#         time.sleep(0.5)
#     return success


# # -------------------------
# # VISUAL AGENT
# # -------------------------

# class VisualAgent:

#     def __init__(self):
#         self.steps_taken = []
#         self.goal = ""
#         self.start_time = None
#         self.last_screen_hash = None
#         self.stuck_count = 0
#         self.browser_mode = False
#         self.resume_from = 0

#     def run(self, goal, max_steps=MAX_STEPS, context=None, resume=False):

#         # STEP 134 — detect platform and navigate there first
#         platform = _detect_platform(goal)
#         if platform:
#             try:
#                 from brain.tab_intelligence import navigate_to_platform
#                 navigate_to_platform(platform)
#                 time.sleep(1)
#                 self.browser_mode = True
#             except Exception as e:
#                 print(f"Tab navigation error: {e}")

#         # STEP 135 — enrich context with personal profile
#         if context is None:
#             context = {}
#         try:
#             from brain.personal_profile import profile
#             form_ctx = profile.get_form_context(
#                 platform=platform,
#                 role=context.get("role"),
#                 company=context.get("company")
#             )
#             context = {**form_ctx, **context}
#         except Exception as e:
#             print(f"Profile load error: {e}")

#         # STEP 132 — resume handling
#         if resume:
#             saved = load_task_state()
#             if saved and saved.get("goal") == goal:
#                 print(f"📂 Resuming from step {saved['step_num']}")
#                 self.steps_taken = saved.get("steps_taken", [])
#                 self.resume_from = saved.get("step_num", 0)
#             else:
#                 resume = False

#         self.goal = goal
#         if not resume:
#             self.steps_taken = []
#             self.resume_from = 0
#         self.start_time = time.time()
#         self.stuck_count = 0
#         self.last_screen_hash = None

#         prompt = _build_prompt(context)

#         print(f"\n{'='*50}")
#         print(f"🤖 Visual Agent {'(resuming)' if resume else 'starting'}")
#         print(f"   Goal    : {goal}")
#         print(f"   Platform: {platform or 'general'}")
#         print(f"{'='*50}\n")

#         save_task_state(goal, self.steps_taken, 0, "running", context)

#         for step_num in range(self.resume_from + 1, max_steps + 1):

#             print(f"\n--- Step {step_num}/{max_steps} ---")

#             if self.browser_mode:
#                 _ensure_browser_focused()
#                 time.sleep(0.3)

#             screen_img = capture_screen()
#             if screen_img is None:
#                 time.sleep(1)
#                 continue

#             screen_hash = self._hash_screen(screen_img)
#             if screen_hash == self.last_screen_hash:
#                 self.stuck_count += 1
#                 print(f"Screen unchanged ({self.stuck_count}/{MAX_STUCK})")
#                 if self.stuck_count >= MAX_STUCK:
#                     if self.browser_mode:
#                         _ensure_browser_focused()
#                         time.sleep(1)
#                         self.stuck_count = 0
#                         continue
#                     return self._finish("stuck", context)
#             else:
#                 self.stuck_count = 0
#                 self.last_screen_hash = screen_hash

#             screen_desc = self._understand_screen(screen_img)
#             print(f"Screen: {screen_desc}")

#             action = self._decide_action(
#                 goal=goal,
#                 screen_desc=screen_desc,
#                 screen_img=screen_img,
#                 step_num=step_num,
#                 context=context,
#                 prompt=prompt
#             )

#             if action is None:
#                 time.sleep(2)
#                 continue

#             print(f"Action: {action.get('action')} | {action.get('reasoning','')}")

#             if action.get("action") == "done" or action.get("done"):
#                 print(f"\n✅ Goal achieved!")
#                 self._record_step(action, screen_desc, success=True)
#                 save_task_state(goal, self.steps_taken, step_num, "success", context)
#                 clear_task_state()
#                 return self._finish("success", context)

#             if action.get("action") == "failed" or action.get("failed"):
#                 reason = action.get("failure_reason") or action.get("reason", "unknown")
#                 print(f"\n❌ Failed: {reason}")
#                 return self._finish("failed", context, reason)

#             success = self._execute_smart(action)
#             self._record_step(action, screen_desc, success=success)
#             save_task_state(goal, self.steps_taken, step_num, "running", context)

#             if action.get("action") == "open_url":
#                 self.browser_mode = True
#                 print("Waiting for page load...")
#                 time.sleep(3)
#                 _ensure_browser_focused()

#             time.sleep(STEP_DELAY)

#         return self._finish("max_steps", context)

#     def _execute_smart(self, action):
#         act = action.get("action")

#         if act == "click":
#             try:
#                 import pyautogui
#                 x = action.get("x", YOUTUBE_SEARCH_X)
#                 y = action.get("y", YOUTUBE_SEARCH_Y)
#                 _ensure_browser_focused()
#                 time.sleep(0.2)
#                 pyautogui.click(x, y)
#                 print(f"Clicked ({x}, {y})")
#                 return True
#             except Exception as e:
#                 print(f"Click error: {e}")
#                 return False

#         if act == "type":
#             try:
#                 import pyautogui
#                 text = action.get("text", "")
#                 pyautogui.write(text, interval=0.05)
#                 print(f"Typed: {text}")
#                 return True
#             except Exception as e:
#                 print(f"Type error: {e}")
#                 return False

#         if act == "scroll":
#             import pyautogui
#             direction = action.get("direction", "down")
#             amount = action.get("amount", 3)
#             pyautogui.scroll(amount if direction == "down" else -amount)
#             return True

#         if act == "hotkey":
#             import pyautogui
#             keys = action.get("keys", [])
#             if keys:
#                 pyautogui.hotkey(*keys)
#             return True

#         try:
#             return perform_ui_action(action)
#         except Exception as e:
#             print(f"Execute error: {e}")
#             return False

#     def _understand_screen(self, img):
#         try:
#             b64 = self._encode_image(img)
#             if not b64 or client is None:
#                 return self._ocr_describe(img)
#             response = client.chat.completions.create(
#                 model=VISION_MODEL,
#                 messages=[{
#                     "role": "user",
#                     "content": [
#                         {
#                             "type": "text",
#                             "text": (
#                                 "Describe this screen in 1-2 sentences. "
#                                 "What app? What's visible? Buttons, forms, input fields? "
#                                 "Include pixel coordinates of key elements."
#                             )
#                         },
#                         {
#                             "type": "image_url",
#                             "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
#                         }
#                     ]
#                 }],
#                 temperature=0.1,
#                 max_tokens=200
#             )
#             return response.choices[0].message.content.strip()
#         except Exception as e:
#             return self._ocr_describe(img)

#     def _decide_action(self, goal, screen_desc, screen_img, step_num, context=None, prompt=None):
#         if client is None:
#             return None
#         try:
#             b64 = self._encode_image(screen_img)
#             steps_summary = [
#                 f"{s['action'].get('action','?')}:{'ok' if s['success'] else 'fail'}"
#                 for s in self.steps_taken[-5:]
#             ]

#             user_content = [{
#                 "type": "text",
#                 "text": json.dumps({
#                     "goal": goal,
#                     "screen": screen_desc,
#                     "step": step_num,
#                     "history": steps_summary,
#                     "context": {k: v for k, v in (context or {}).items()
#                                 if k in ("name","email","phone","role","company",
#                                         "skills_summary","cover_letter")}
#                 })
#             }]

#             if b64:
#                 user_content.append({
#                     "type": "image_url",
#                     "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
#                 })

#             response = client.chat.completions.create(
#                 model=VISION_MODEL,
#                 messages=[
#                     {"role": "system", "content": prompt or _build_prompt(context)},
#                     {"role": "user", "content": user_content}
#                 ],
#                 temperature=0.2,
#                 max_tokens=300
#             )

#             raw = response.choices[0].message.content.strip()
#             raw = re.sub(r"```json|```", "", raw)
#             return json.loads(raw)

#         except Exception as e:
#             print(f"Decision error: {e}")
#             return None

#     def _finish(self, outcome, context=None, reason=None):
#         duration_ms = int((time.time() - self.start_time) * 1000)
#         save_to_history(
#             goal=self.goal,
#             outcome=outcome,
#             steps=len(self.steps_taken),
#             duration_ms=duration_ms,
#             context=context
#         )
#         if outcome in ("success", "failed"):
#             clear_task_state()

#         result = {
#             "goal": self.goal,
#             "outcome": outcome,
#             "steps": len(self.steps_taken),
#             "steps_taken": self.steps_taken,
#             "duration_ms": duration_ms,
#             "reason": reason
#         }

#         print(f"\n{'='*50}")
#         print(f"🤖 Visual Agent — {outcome.upper()}")
#         print(f"   Goal  : {self.goal}")
#         print(f"   Steps : {len(self.steps_taken)}")
#         print(f"   Time  : {duration_ms}ms")
#         if reason:
#             print(f"   Why   : {reason}")
#         print(f"{'='*50}\n")

#         return result

#     def _record_step(self, action, screen_desc, success=True):
#         self.steps_taken.append({
#             "action": action,
#             "screen": screen_desc[:100],
#             "success": success,
#             "timestamp": str(datetime.now())
#         })

#     def _encode_image(self, img):
#         try:
#             h, w = img.shape[:2]
#             if w > 1280:
#                 scale = 1280 / w
#                 img = cv2.resize(img, (1280, int(h * scale)))
#             _, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 70])
#             return base64.b64encode(buf).decode("utf-8")
#         except:
#             return None

#     def _hash_screen(self, img):
#         try:
#             small = cv2.resize(img, (32, 32))
#             gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
#             return gray.tobytes()
#         except:
#             return None

#     def _ocr_describe(self, img):
#         try:
#             import pytesseract
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             text = pytesseract.image_to_string(gray)
#             lines = [l.strip() for l in text.splitlines() if l.strip()][:3]
#             return " | ".join(lines) if lines else "screen captured"
#         except:
#             return "screen captured"


# # -------------------------
# # ENTRY POINTS
# # -------------------------

# def run_visual_goal(goal, context=None, max_steps=MAX_STEPS, resume=False):
#     agent = VisualAgent()
#     return agent.run(goal, max_steps=max_steps, context=context, resume=resume)


# def resume_last_task():
#     from memory.task_memory import load_task_state
#     state = load_task_state()
#     if not state:
#         print("No interrupted task found.")
#         return None
#     goal = state.get("goal")
#     context = state.get("context")
#     print(f"Resuming: {goal}")
#     return run_visual_goal(goal, context=context, resume=True)


# execution/visual_agent.py
# STEP 131-135 integrated
# FIX: use direct search URLs always — clicking search bar unreliable


# execution/visual_agent.py
# TOKEN-EFFICIENT version
# - Uses OCR for screen reading (free, no tokens)
# - Uses LLM text-only for decisions (cheap ~200 tokens vs 3500 for vision)
# - Uses vision ONLY when OCR fails completely
# - Maximizes browser window before starting
# - Single browser instance

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
from memory.task_memory import (
    save_task_state, clear_task_state,
    save_to_history, load_task_state
)

GROQ_KEY = os.getenv("GROQ_API_KEY")
client = None
if GROQ_KEY:
    client = OpenAI(
        api_key=GROQ_KEY,
        base_url="https://api.groq.com/openai/v1"
    )

MAX_STEPS    = 12
MAX_STUCK    = 3
STEP_DELAY   = 1.5
# Use cheap text model for decisions — ~200 tokens vs 3500 for vision
TEXT_MODEL   = "llama-3.3-70b-versatile"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
SCREEN_W     = 1920
SCREEN_H     = 1080

PLATFORM_KEYWORDS = {
    "leetcode":    "leetcode.com",
    "naukri":      "naukri.com",
    "indeed":      "indeed.com",
    "internshala": "internshala.com",
    "linkedin":    "linkedin.com",
    "gmail":       "mail.google.com",
    "whatsapp":    "web.whatsapp.com",
    "telegram":    "web.telegram.org",
    "youtube":     "youtube.com",
    "github":      "github.com",
}

# Known click coordinates for common UI elements
KNOWN_COORDS = {
    "youtube_first_video":   (400, 250),
    "youtube_second_video":  (400, 450),
    "youtube_search_bar":    (588, 145),
    "leetcode_run_button":   (1650, 940),
    "leetcode_submit":       (1750, 940),
    "leetcode_lang_selector": (1050, 340),
    "whatsapp_search":       (300, 90),
    "whatsapp_message_input": (960, 1020),
}

def _detect_platform(goal):
    goal_lower = goal.lower()
    for platform in PLATFORM_KEYWORDS:
        if platform in goal_lower:
            return platform
    return None

def _extract_query(goal):
    g = goal.lower()
    if " and play " in g:
        return g.split(" and play ", 1)[1].replace(" on youtube", "").strip()
    if " and search " in g:
        return g.split(" and search ", 1)[1].strip()
    for p in ["play ", "search ", "find ", "watch ", "listen to "]:
        if p in g:
            q = g.split(p, 1)[1]
            for suffix in [" on youtube", " on google", " on naukri", " on indeed"]:
                q = q.replace(suffix, "")
            return q.strip()
    return ""

def _get_direct_url(goal, platform, context=None):
    """Build direct URL — only when we have a clean query."""
    if platform == "youtube":
        query = _extract_query(goal)
        if query:
            return f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    if platform == "leetcode":
        # get slug from context if available
        slug = (context or {}).get("slug")
        if slug:
            return f"https://leetcode.com/problems/{slug}/"
    return None

def _parse_json_safe(raw):
    """Extract first valid JSON object from LLM response."""
    if not raw:
        return None
    raw = raw.strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    raw = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]', '', raw)
    # try direct
    try:
        return json.loads(raw)
    except:
        pass
    # extract first { ... }
    try:
        start = raw.index("{")
        depth = 0
        for i, ch in enumerate(raw[start:], start):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(raw[start:i+1])
    except:
        pass
    return None

def _ocr_screen(img):
    """Read screen text using pytesseract — FREE, no tokens."""
    try:
        import pytesseract
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        lines = [l.strip() for l in text.splitlines() if l.strip() and len(l.strip()) > 2]
        return " | ".join(lines[:8])
    except:
        return "screen captured"

def _maximize_browser():
    """Maximize the browser window so coordinates are correct."""
    try:
        import pyautogui
        import pygetwindow as gw
        for w in gw.getAllWindows():
            if not w.title:
                continue
            if any(b in w.title.lower() for b in ["chrome", "brave", "firefox"]):
                # skip Chrome for Testing
                if "for testing" in w.title.lower():
                    continue
                try:
                    w.maximize()
                    time.sleep(0.5)
                    print(f"Maximized: {w.title[:50]}")
                    return True
                except:
                    pass
    except:
        pass
    # fallback: Win key + Up arrow
    try:
        import pyautogui
        pyautogui.hotkey("win", "up")
        time.sleep(0.3)
    except:
        pass
    return False

def _ensure_browser_focused(browser="chrome", skip_testing=True):
    """Focus browser window — skip Chrome for Testing if real Chrome exists."""
    from automation.window_manager import force_focus_window, is_window_focused
    try:
        import pygetwindow as gw
        import win32gui
        import win32con

        # find best browser window
        best = None
        for w in gw.getAllWindows():
            if not w.title:
                continue
            title = w.title.lower()
            if not any(b in title for b in ["chrome", "brave", "firefox", "edge"]):
                continue
            if skip_testing and "for testing" in title:
                continue
            best = w
            break

        if best:
            hwnd = best._hWnd
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                time.sleep(0.3)
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.3)
            return True
    except:
        pass
    try:
        return force_focus_window(browser, timeout=3)
    except:
        return False


# -------------------------
# DECISION PROMPT — TEXT ONLY (cheap)
# -------------------------

def _build_text_prompt(context=None):
    base = f"""You are Fury, an AI agent on Windows {SCREEN_W}x{SCREEN_H}.
You see OCR text from the screen. Decide ONE action.

COORDINATES (1920x1080):
- YouTube first video: x=400, y=250
- YouTube second video: x=400, y=450
- LeetCode language selector: x=1050, y=340
- LeetCode code editor: x=1200, y=500
- LeetCode Run button: x=1650, y=940
- LeetCode Submit: x=1750, y=940
- WhatsApp search: x=300, y=90
- WhatsApp message input: x=960, y=1020
- General back button: x=100, y=50

RULES:
1. Return ONE JSON object only
2. Use pixel coordinates not fractions
3. If you see video results on YouTube, click x=400,y=250 to play first one
4. If you see a 404 error, use open_url to navigate to the correct page
5. If goal is achieved set done=true
6. Do NOT repeat the same URL that already failed

Return ONLY:
{{"action":"click","x":400,"y":250,"reasoning":"clicking first video","done":false,"failed":false,"failure_reason":null}}
"""
    if context:
        for k in ("name","email","phone","role","slug","url"):
            if context.get(k):
                base += f"\n{k}: {context[k]}"
    return base


class VisualAgent:

    def __init__(self):
        self.steps_taken  = []
        self.goal         = ""
        self.start_time   = None
        self.last_screen_hash = None
        self.stuck_count  = 0
        self.browser_mode = False
        self.resume_from  = 0
        self.last_url     = None
        self.failed_urls  = set()

    def run(self, goal, max_steps=MAX_STEPS, context=None, resume=False):

        platform = _detect_platform(goal)

        # navigate to platform in new tab
        if platform:
            try:
                from brain.tab_intelligence import navigate_to_platform
                navigate_to_platform(platform, force_new_tab=True)
                time.sleep(2)
                self.browser_mode = True
            except Exception as e:
                print(f"Navigation error: {e}")

        # maximize browser
        _ensure_browser_focused()
        _maximize_browser()
        time.sleep(0.5)

        # enrich context
        if context is None:
            context = {}
        try:
            from brain.personal_profile import profile
            form_ctx = profile.get_form_context(platform=platform)
            context  = {**form_ctx, **context}
        except:
            pass

        # resume
        if resume:
            saved = load_task_state()
            if saved and saved.get("goal") == goal:
                self.steps_taken = saved.get("steps_taken", [])
                self.resume_from = saved.get("step_num", 0)
            else:
                resume = False

        self.goal        = goal
        self.start_time  = time.time()
        self.stuck_count = 0
        self.last_screen_hash = None
        self.last_url    = None
        self.failed_urls = set()
        if not resume:
            self.steps_taken = []
            self.resume_from = 0

        prompt = _build_text_prompt(context)
        direct_url = _get_direct_url(goal, platform, context)

        print(f"\n{'='*50}")
        print(f"🤖 Visual Agent starting")
        print(f"   Goal    : {goal}")
        print(f"   Platform: {platform or 'general'}")
        if direct_url:
            print(f"   Direct  : {direct_url}")
        print(f"{'='*50}\n")

        save_task_state(goal, self.steps_taken, 0, "running", context)

        # direct URL step 0
        if direct_url and not resume:
            print(f"--- Step 0: Direct URL ---")
            self._execute_smart({"action": "open_url", "url": direct_url})
            self.last_url = direct_url
            self.browser_mode = True
            self._record_step({"action": "open_url", "url": direct_url},
                              "direct navigation", True)
            print("Waiting for page load...")
            time.sleep(3)
            _ensure_browser_focused()
            _maximize_browser()

        for step_num in range(self.resume_from + 1, max_steps + 1):

            print(f"\n--- Step {step_num}/{max_steps} ---")

            if self.browser_mode:
                _ensure_browser_focused()
                time.sleep(0.3)

            screen_img = capture_screen()
            if screen_img is None:
                time.sleep(1)
                continue

            # stuck detection
            screen_hash = self._hash_screen(screen_img)
            if screen_hash == self.last_screen_hash:
                self.stuck_count += 1
                print(f"Screen unchanged ({self.stuck_count}/{MAX_STUCK})")
                if self.stuck_count >= MAX_STUCK:
                    if self.browser_mode:
                        _ensure_browser_focused()
                        _maximize_browser()
                        time.sleep(1)
                        self.stuck_count = 0
                        continue
                    return self._finish("stuck", context)
            else:
                self.stuck_count = 0
                self.last_screen_hash = screen_hash

            # OCR screen — FREE
            screen_text = _ocr_screen(screen_img)
            print(f"Screen: {screen_text[:100]}")

            # decide action using TEXT model — cheap
            action = self._decide_action_text(goal, screen_text, step_num,
                                              context, prompt)
            if action is None:
                time.sleep(2)
                continue

            print(f"Action: {action.get('action')} | {action.get('reasoning','')[:70]}")

            if action.get("action") == "done" or action.get("done"):
                print(f"\n✅ Goal achieved!")
                self._record_step(action, screen_text, True)
                clear_task_state()
                return self._finish("success", context)

            if action.get("action") == "failed" or action.get("failed"):
                reason = action.get("failure_reason") or action.get("reason", "unknown")
                return self._finish("failed", context, reason)

            # prevent duplicate URL
            if action.get("action") == "open_url":
                url = action.get("url", "")
                if url in self.failed_urls:
                    print(f"Skipping failed URL: {url}")
                    action = {"action": "click", "x": 400, "y": 250,
                              "reasoning": "clicking first result instead"}
                elif url == self.last_url:
                    print(f"Skipping duplicate URL")
                    action = {"action": "click", "x": 400, "y": 250,
                              "reasoning": "already on this page, clicking result"}
                else:
                    self.last_url = url

            # fix relative coordinates
            if action.get("action") == "click":
                x = action.get("x", 400)
                y = action.get("y", 300)
                if isinstance(x, float) and x <= 1.0:
                    x = int(x * SCREEN_W)
                if isinstance(y, float) and y <= 1.0:
                    y = int(y * SCREEN_H)
                action["x"] = x
                action["y"] = y

            success = self._execute_smart(action)
            self._record_step(action, screen_text, success)
            save_task_state(goal, self.steps_taken, step_num, "running", context)

            if action.get("action") == "open_url":
                self.browser_mode = True
                print("Waiting for page load...")
                time.sleep(3)
                _ensure_browser_focused()
                _maximize_browser()

            time.sleep(STEP_DELAY)

        return self._finish("max_steps", context)

    def _decide_action_text(self, goal, screen_text, step_num,
                            context=None, prompt=None):
        """
        Decide action using TEXT-ONLY model.
        ~200 tokens vs ~3500 for vision model.
        Saves ~94% of token budget.
        """
        if client is None:
            return None
        try:
            steps_summary = [
                f"{s['action'].get('action','?')}:{'ok' if s['success'] else 'fail'}"
                for s in self.steps_taken[-3:]
            ]
            user_msg = json.dumps({
                "goal": goal,
                "screen_text": screen_text[:300],  # limit OCR text
                "step": step_num,
                "history": steps_summary,
            })

            # handle rate limit with wait
            for attempt in range(3):
                try:
                    response = client.chat.completions.create(
                        model=TEXT_MODEL,
                        messages=[
                            {"role": "system", "content": prompt or _build_text_prompt(context)},
                            {"role": "user",   "content": user_msg}
                        ],
                        temperature=0.1,
                        max_tokens=150  # keep response tiny
                    )
                    raw = response.choices[0].message.content
                    return _parse_json_safe(raw)

                except Exception as e:
                    err = str(e)
                    if "429" in err or "rate_limit" in err.lower():
                        # extract wait time
                        wait = 30
                        m = re.search(r'try again in (\d+)m', err)
                        if m:
                            wait = int(m.group(1)) * 60 + 10
                        else:
                            m2 = re.search(r'try again in (\d+\.?\d*)s', err)
                            if m2:
                                wait = int(float(m2.group(1))) + 5
                        print(f"Rate limit — waiting {wait}s...")
                        time.sleep(min(wait, 120))  # max 2 min wait
                        continue
                    else:
                        print(f"Decision error: {e}")
                        return None

        except Exception as e:
            print(f"Decision error: {e}")
            return None

    def _execute_smart(self, action):
        act = action.get("action")

        if act == "click":
            try:
                import pyautogui
                x = int(action.get("x", 400))
                y = int(action.get("y", 300))
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
            amount    = action.get("amount", 3)
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

    def _finish(self, outcome, context=None, reason=None):
        duration_ms = int((time.time() - self.start_time) * 1000)
        save_to_history(self.goal, outcome, len(self.steps_taken),
                        duration_ms, context)
        if outcome in ("success", "failed"):
            clear_task_state()
        result = {
            "goal": self.goal, "outcome": outcome,
            "steps": len(self.steps_taken),
            "steps_taken": self.steps_taken,
            "duration_ms": duration_ms, "reason": reason
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

    def _record_step(self, action, screen_text, success=True):
        self.steps_taken.append({
            "action": action, "screen": screen_text[:80],
            "success": success, "timestamp": str(datetime.now())
        })

    def _hash_screen(self, img):
        try:
            small = cv2.resize(img, (32, 32))
            gray  = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
            return gray.tobytes()
        except:
            return None

    def _encode_image(self, img):
        try:
            h, w = img.shape[:2]
            if w > 1280:
                scale = 1280 / w
                img = cv2.resize(img, (1280, int(h * scale)))
            _, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 65])
            return base64.b64encode(buf).decode("utf-8")
        except:
            return None


def run_visual_goal(goal, context=None, max_steps=MAX_STEPS, resume=False):
    agent = VisualAgent()
    return agent.run(goal, max_steps=max_steps, context=context, resume=resume)


def resume_last_task():
    from memory.task_memory import load_task_state
    state = load_task_state()
    if not state:
        print("No interrupted task found.")
        return None
    return run_visual_goal(state.get("goal"),
                           context=state.get("context"), resume=True)