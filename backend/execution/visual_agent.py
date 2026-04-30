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



# execution/visual_agent.py
# TOKEN-EFFICIENT — hardcoded playbooks for known tasks
# YouTube / WhatsApp / LeetCode navigation = 0 tokens
# LLM only called for unknown situations



# execution/visual_agent.py
# TOKEN-EFFICIENT — hardcoded playbooks for known tasks
# YouTube now uses direct video URL — no ads, no coordinate guessing







# execution/visual_agent.py
# FIX: YouTube reuses existing tab
# FIX: WhatsApp/LLM fallback focuses correct window, not localhost UI

import os
import json
import re
import time
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
    client = OpenAI(api_key=GROQ_KEY,
                    base_url="https://api.groq.com/openai/v1")

MAX_STEPS  = 12
MAX_STUCK  = 3
STEP_DELAY = 1.5
TEXT_MODEL = "llama-3.3-70b-versatile"
SCREEN_W   = 1920
SCREEN_H   = 1080

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

COORDS = {
    "yt_first_video":   (400, 250),
    "wa_search":        (289, 216),
    "wa_first_result":  (289, 320),
    "wa_msg_input":     (980, 987),
    "lc_lang_selector": (1006, 239),
    "lc_code_editor":   (1200, 500),
    "lc_run":           (1650, 940),
    "lc_submit":        (1750, 940),
}


# ─────────────────────────────
# HELPERS
# ─────────────────────────────

def _detect_platform(goal):
    goal_lower = goal.lower()
    for platform in PLATFORM_KEYWORDS:
        if platform in goal_lower:
            return platform
    return None


def _extract_query(goal):
    g = goal.lower()
    for p in ["play ", "search for ", "search ", "find ",
               "watch ", "listen to "]:
        if p in g:
            q = g.split(p, 1)[1]
            for s in [" on youtube", " on google", " on naukri"]:
                q = q.replace(s, "")
            return q.strip()
    return ""


def _parse_json_safe(raw):
    if not raw:
        return None
    raw = re.sub(r"```json|```", "", raw.strip())
    raw = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]', '', raw)
    try:
        return json.loads(raw)
    except:
        pass
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
    try:
        import pytesseract
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        lines = [l.strip() for l in text.splitlines()
                 if l.strip() and len(l.strip()) > 2]
        return " | ".join(lines[:6])
    except:
        return "screen captured"


def _ensure_browser_focused(platform=None):
    """
    Focus real Chrome window.
    If platform given, focuses that specific tab.
    NEVER focuses localhost/Fury UI tabs.
    """
    try:
        import win32gui, win32con
        import pygetwindow as gw

        # if platform specified, try to focus that tab first
        if platform:
            from browser.browser_agent import focus_platform_tab
            if focus_platform_tab(platform):
                return True

        # fallback — find any real browser window, skip localhost
        for w in gw.getAllWindows():
            if not w.title:
                continue
            t = w.title.lower()
            if "for testing" in t:
                continue
            if "localhost" in t:          # skip Fury React UI
                continue
            if any(b in t for b in ["chrome", "brave", "firefox", "edge"]):
                hwnd = w._hWnd
                if win32gui.IsIconic(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    time.sleep(0.3)
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.4)
                return True
    except:
        pass
    return False


def _smart_navigate(platform, url):
    """Check existing tabs first, open new only if needed."""
    try:
        from brain.tab_intelligence import scan_open_tabs, switch_to_tab
        open_tabs = scan_open_tabs()
        if platform and platform in open_tabs:
            print(f"✅ Found existing {platform} tab — switching")
            switch_to_tab(platform)
            time.sleep(1)
            _ensure_browser_focused(platform)
            return True
    except Exception as e:
        print(f"Tab scan error: {e}")

    print(f"📂 {platform} not open — opening new tab")
    from browser.browser_agent import open_website
    open_website(url)
    time.sleep(2)
    _ensure_browser_focused(platform)
    return True


# ─────────────────────────────
# HARDCODED PLAYBOOKS — 0 tokens
# ─────────────────────────────

def _playbook_youtube(query):
    """
    Play YouTube.
    If YouTube tab exists → navigate within it (no new tab).
    If not → open new tab.
    """
    try:
        from platforms.youtube_agent import search_youtube
        results = search_youtube(query)
        if results:
            video_url = results[0]
            print(f"   🎵 Direct: {video_url}")

            # check if youtube tab already open
            try:
                from brain.tab_intelligence import scan_open_tabs
                open_tabs = scan_open_tabs()
                if "youtube" in open_tabs:
                    # reuse existing tab — navigate within it
                    return [
                        {"action": "navigate_in_tab", "url": video_url},
                        {"action": "wait", "time": 2},
                        {"action": "done"},
                    ]
            except:
                pass

            # no youtube tab — open new
            return [
                {"action": "open_url", "url": video_url},
                {"action": "wait", "time": 2},
                {"action": "done"},
            ]
    except Exception as e:
        print(f"YouTube search error: {e}")

    # fallback
    encoded = query.replace(" ", "+")
    return [
        {"action": "open_url",
         "url": f"https://www.youtube.com/results?search_query={encoded}"},
        {"action": "wait", "time": 3},
        {"action": "click", "x": COORDS["yt_first_video"][0],
         "y": COORDS["yt_first_video"][1]},
        {"action": "wait", "time": 2},
        {"action": "done"},
    ]


def _playbook_whatsapp_send(contact, message):
    return [
        {"action": "open_url", "url": "https://web.whatsapp.com"},
        {"action": "wait", "time": 4},
        {"action": "maximize"},
        {"action": "click",
         "x": COORDS["wa_search"][0], "y": COORDS["wa_search"][1]},
        {"action": "wait", "time": 1},
        {"action": "type", "text": contact},
        {"action": "wait", "time": 2},
        {"action": "click",
         "x": COORDS["wa_first_result"][0], "y": COORDS["wa_first_result"][1]},
        {"action": "wait", "time": 1},
        {"action": "click",
         "x": COORDS["wa_msg_input"][0], "y": COORDS["wa_msg_input"][1]},
        {"action": "wait", "time": 0.5},
        {"action": "type", "text": message},
        {"action": "press", "key": "enter"},
        {"action": "wait", "time": 1},
        {"action": "done"},
    ]


def _playbook_whatsapp_check():
    return [
        {"action": "open_url", "url": "https://web.whatsapp.com"},
        {"action": "wait", "time": 3},
        {"action": "maximize"},
        {"action": "done"},
    ]


def _playbook_whatsapp_read(contact):
    return [
        {"action": "open_url", "url": "https://web.whatsapp.com"},
        {"action": "wait", "time": 4},
        {"action": "maximize"},
        {"action": "click",
         "x": COORDS["wa_search"][0], "y": COORDS["wa_search"][1]},
        {"action": "wait", "time": 1},
        {"action": "type", "text": contact},
        {"action": "wait", "time": 2},
        {"action": "click",
         "x": COORDS["wa_first_result"][0], "y": COORDS["wa_first_result"][1]},
        {"action": "wait", "time": 1},
        {"action": "done"},
    ]


def _playbook_leetcode_open(slug):
    return [
        {"action": "open_url",
         "url": f"https://leetcode.com/problems/{slug}/"},
        {"action": "wait", "time": 3},
        {"action": "maximize"},
        {"action": "done"},
    ]


def _get_playbook(goal, platform, context):
    g = goal.lower()

    if platform == "youtube":
        query = _extract_query(goal) or goal
        return _playbook_youtube(query), "youtube"

    if platform == "whatsapp":
        contact = (context or {}).get("contact", "")
        if contact and any(w in g for w in ["send", "say", "message", ":"]):
            message = ""
            for sep in [":", "send message", "say "]:
                if sep in g:
                    message = g.split(sep, 1)[1].strip()
                    break
            if message:
                return _playbook_whatsapp_send(contact, message), "whatsapp_send"
        if contact and "read" in g:
            return _playbook_whatsapp_read(contact), "whatsapp_read"
        return _playbook_whatsapp_check(), "whatsapp_check"

    if platform == "leetcode":
        slug = (context or {}).get("slug", "")
        if slug:
            return _playbook_leetcode_open(slug), "leetcode_open"

    return None, None


def _build_prompt(platform=None):
    base = f"""You are Fury on Windows {SCREEN_W}x{SCREEN_H}.
Decide ONE action from OCR screen text. Return ONE JSON only.
IMPORTANT: You are controlling a browser, NOT the Fury chat UI.

{{"action":"click","x":400,"y":250,"reasoning":"why","done":false,"failed":false,"failure_reason":null}}

Actions: open_url, click, type, press, wait, scroll, done, failed
Use pixel coordinates.
"""
    if platform == "whatsapp":
        base += """
WhatsApp Web coordinates:
- Search bar: x=289, y=216
- First result: x=289, y=320
- Message input: x=980, y=987
"""
    return base


# ─────────────────────────────
# VISUAL AGENT
# ─────────────────────────────

class VisualAgent:

    def __init__(self):
        self.steps_taken = []
        self.goal        = ""
        self.start_time  = None
        self.last_hash   = None
        self.stuck_count = 0
        self.last_url    = None
        self.platform    = None

    def run(self, goal, max_steps=MAX_STEPS, context=None, resume=False):

        platform      = _detect_platform(goal)
        self.platform = platform
        self.goal     = goal
        self.start_time  = time.time()
        self.stuck_count = 0
        self.last_hash   = None
        self.last_url    = None

        if not resume:
            self.steps_taken = []

        if context is None:
            context = {}
        try:
            from brain.personal_profile import profile
            context = {**profile.get_form_context(platform=platform),
                       **context}
        except:
            pass

        print(f"\n{'='*50}")
        print(f"🤖 Visual Agent: {goal}")
        print(f"   Platform: {platform or 'general'}")

        playbook, name = _get_playbook(goal, platform, context)

        if playbook:
            print(f"   Mode: PLAYBOOK ({name}) — 0 tokens")
            print(f"{'='*50}\n")
            return self._run_playbook(playbook, context)

        print(f"   Mode: LLM-assisted")
        print(f"{'='*50}\n")

        if platform:
            platform_urls = {
                "gmail":       "https://mail.google.com",
                "github":      "https://github.com",
                "naukri":      "https://www.naukri.com",
                "indeed":      "https://www.indeed.com",
                "internshala": "https://internshala.com",
                "linkedin":    "https://www.linkedin.com",
            }
            url = platform_urls.get(platform, f"https://www.{platform}.com")
            _smart_navigate(platform, url)

        save_task_state(goal, self.steps_taken, 0, "running", context)
        prompt = _build_prompt(platform)

        for step_num in range(1, max_steps + 1):
            print(f"\n--- Step {step_num}/{max_steps} ---")

            _ensure_browser_focused(platform)
            time.sleep(0.3)

            screen_img = capture_screen()
            if screen_img is None:
                time.sleep(1)
                continue

            h = self._hash(screen_img)
            if h == self.last_hash:
                self.stuck_count += 1
                print(f"Screen unchanged ({self.stuck_count}/{MAX_STUCK})")
                if self.stuck_count >= MAX_STUCK:
                    _ensure_browser_focused(platform)
                    time.sleep(1)
                    self.stuck_count = 0
                    continue
            else:
                self.stuck_count = 0
                self.last_hash = h

            screen_text = _ocr_screen(screen_img)
            print(f"Screen: {screen_text[:80]}")

            action = self._decide(goal, screen_text, step_num,
                                  context, prompt)
            if action is None:
                time.sleep(2)
                continue

            print(f"Action: {action.get('action')} | "
                  f"{action.get('reasoning','')[:60]}")

            if action.get("action") == "done" or action.get("done"):
                print("✅ Done!")
                self._record(action, screen_text, True)
                clear_task_state()
                return self._finish("success", context)

            if action.get("action") == "failed" or action.get("failed"):
                return self._finish("failed", context,
                                    action.get("failure_reason", "unknown"))

            if action.get("action") == "open_url":
                url = action.get("url", "")
                if url == self.last_url:
                    action = {"action": "click", "x": 400, "y": 250,
                              "reasoning": "already on page"}
                else:
                    self.last_url = url

            if action.get("action") == "click":
                x = action.get("x", 400)
                y = action.get("y", 300)
                if isinstance(x, float) and x <= 1.0:
                    x = int(x * SCREEN_W)
                if isinstance(y, float) and y <= 1.0:
                    y = int(y * SCREEN_H)
                action["x"], action["y"] = x, y

            self._execute(action)
            self._record(action, screen_text, True)
            save_task_state(goal, self.steps_taken, step_num,
                            "running", context)

            if action.get("action") in ("open_url", "navigate_in_tab"):
                print("Waiting for page...")
                time.sleep(3)
                _ensure_browser_focused(platform)

            time.sleep(STEP_DELAY)

        return self._finish("max_steps", context)

    # ─────────────────────────────
    # PLAYBOOK RUNNER
    # ─────────────────────────────

    def _run_playbook(self, steps, context):
        print(f"Running {len(steps)} playbook steps...\n")

        last_hash   = None
        stuck_count = 0

        for i, action in enumerate(steps, 1):
            act = action.get("action")
            print(f"Step {i}: {act} ", end="")

            if act == "done":
                print("✅")
                return self._finish("success", context)

            if act == "wait":
                t = action.get("time", 2)
                print(f"({t}s)")
                time.sleep(t)
                continue

            if act == "maximize":
                print("(maximizing browser)")
                _ensure_browser_focused(self.platform)
                time.sleep(0.5)
                continue

            print()
            self._execute(action)
            self._record(action, "playbook", True)

            if act in ("open_url", "navigate_in_tab"):
                time.sleep(3)
                _ensure_browser_focused(self.platform)
            else:
                time.sleep(0.8)

            # verify click/type changed screen
            if act in ("click", "type", "press"):
                screen_img = capture_screen()
                if screen_img is not None:
                    current_hash = self._hash(screen_img)
                    if current_hash == last_hash:
                        stuck_count += 1
                        print(f"  ⚠️  Screen unchanged ({stuck_count}/2)")
                        if stuck_count >= 2:
                            print(f"  ❌ Step failed — switching to LLM")
                            return self._llm_fallback(
                                self.goal, context,
                                completed_steps=i,
                                failure_reason=f"{act} at step {i} had no effect"
                            )
                    else:
                        stuck_count = 0
                        last_hash   = current_hash

        return self._finish("success", context)

    def _llm_fallback(self, goal, context,
                      completed_steps=0, failure_reason=""):
        print(f"\n🔄 Switching to LLM — {failure_reason}\n")

        # make sure we're focused on the RIGHT browser window
        _ensure_browser_focused(self.platform)

        prompt    = _build_prompt(self.platform)
        max_steps = max(MAX_STEPS - completed_steps, 5)

        for step_num in range(1, max_steps + 1):
            print(f"\n--- LLM Step {step_num} ---")

            _ensure_browser_focused(self.platform)
            time.sleep(0.3)

            screen_img = capture_screen()
            if screen_img is None:
                time.sleep(1)
                continue

            h = self._hash(screen_img)
            if h == self.last_hash:
                self.stuck_count += 1
                if self.stuck_count >= MAX_STUCK:
                    return self._finish("stuck", context)
            else:
                self.stuck_count = 0
                self.last_hash = h

            screen_text = _ocr_screen(screen_img)
            print(f"Screen: {screen_text[:80]}")

            action = self._decide(goal, screen_text, step_num,
                                  context, prompt)
            if action is None:
                time.sleep(2)
                continue

            print(f"Action: {action.get('action')} | "
                  f"{action.get('reasoning','')[:60]}")

            if action.get("action") == "done" or action.get("done"):
                print("✅ LLM recovered!")
                return self._finish("success", context)

            if action.get("action") == "failed" or action.get("failed"):
                return self._finish("failed", context,
                                    action.get("failure_reason", "unknown"))

            if action.get("action") == "click":
                x = action.get("x", 400)
                y = action.get("y", 300)
                if isinstance(x, float) and x <= 1.0:
                    x = int(x * SCREEN_W)
                if isinstance(y, float) and y <= 1.0:
                    y = int(y * SCREEN_H)
                action["x"], action["y"] = x, y

            self._execute(action)
            self._record(action, screen_text, True)

            if action.get("action") in ("open_url", "navigate_in_tab"):
                time.sleep(3)
                _ensure_browser_focused(self.platform)

            time.sleep(STEP_DELAY)

        return self._finish("max_steps", context)

    # ─────────────────────────────
    # LLM DECISION
    # ─────────────────────────────

    def _decide(self, goal, screen_text, step_num, context, prompt):
        if not client:
            return None
        try:
            history = [
                f"{s['action'].get('action','?')}:ok"
                for s in self.steps_taken[-3:]
            ]
            msg = json.dumps({
                "goal":    goal,
                "screen":  screen_text[:250],
                "step":    step_num,
                "history": history,
            })
            for attempt in range(3):
                try:
                    resp = client.chat.completions.create(
                        model=TEXT_MODEL,
                        messages=[
                            {"role": "system", "content": prompt},
                            {"role": "user",   "content": msg}
                        ],
                        temperature=0.1,
                        max_tokens=120
                    )
                    return _parse_json_safe(resp.choices[0].message.content)
                except Exception as e:
                    if "429" in str(e):
                        m = re.search(r'try again in (\d+)m', str(e))
                        wait = int(m.group(1)) * 60 + 5 if m else 60
                        wait = min(wait, 90)
                        print(f"Rate limit — waiting {wait}s...")
                        time.sleep(wait)
                    else:
                        print(f"Decision error: {e}")
                        return None
        except Exception as e:
            print(f"Decision error: {e}")
            return None

    # ─────────────────────────────
    # EXECUTE
    # ─────────────────────────────

    def _execute(self, action):
        act = action.get("action")
        try:
            if act == "navigate_in_tab":
                from browser.browser_agent import navigate_in_tab
                navigate_in_tab(action.get("url", ""))

            elif act == "click":
                import pyautogui
                x = int(action.get("x", 400))
                y = int(action.get("y", 300))
                _ensure_browser_focused(self.platform)
                time.sleep(0.2)
                pyautogui.click(x, y)
                print(f"  Clicked ({x}, {y})")

            elif act == "type":
                import pyautogui
                pyautogui.write(action.get("text", ""), interval=0.05)
                print(f"  Typed: {action.get('text','')}")

            elif act == "press":
                import pyautogui
                pyautogui.press(action.get("key", "enter"))

            elif act == "scroll":
                import pyautogui
                d = action.get("direction", "down")
                a = action.get("amount", 3)
                pyautogui.scroll(a if d == "down" else -a)

            elif act == "hotkey":
                import pyautogui
                pyautogui.hotkey(*action.get("keys", []))

            else:
                perform_ui_action(action)

        except Exception as e:
            print(f"  Execute error: {e}")

    # ─────────────────────────────
    # HELPERS
    # ─────────────────────────────

    def _finish(self, outcome, context=None, reason=None):
        ms = int((time.time() - self.start_time) * 1000)
        save_to_history(self.goal, outcome,
                        len(self.steps_taken), ms, context)
        if outcome in ("success", "failed"):
            clear_task_state()
        print(f"\n{'='*50}")
        print(f"🤖 {outcome.upper()} | {self.goal[:50]}")
        print(f"   Steps: {len(self.steps_taken)} | Time: {ms}ms")
        if reason:
            print(f"   Why: {reason}")
        print(f"{'='*50}\n")
        return {
            "goal":        self.goal,
            "outcome":     outcome,
            "steps":       len(self.steps_taken),
            "steps_taken": self.steps_taken,
            "duration_ms": ms,
            "reason":      reason,
        }

    def _record(self, action, screen, success=True):
        self.steps_taken.append({
            "action":    action,
            "screen":    screen[:60],
            "success":   success,
            "timestamp": str(datetime.now()),
        })

    def _hash(self, img):
        try:
            s = cv2.resize(img, (16, 16))
            g = cv2.cvtColor(s, cv2.COLOR_BGR2GRAY)
            return g.tobytes()
        except:
            return None


def run_visual_goal(goal, context=None,
                    max_steps=MAX_STEPS, resume=False):
    return VisualAgent().run(goal, max_steps=max_steps,
                             context=context, resume=resume)


def resume_last_task():
    state = load_task_state()
    if not state:
        print("No interrupted task.")
        return None
    return run_visual_goal(state.get("goal"),
                           context=state.get("context"),
                           resume=True)