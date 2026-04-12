# vision/vision_understanding.py
# STEP 114 — Semantic vision
#
# Goes beyond OCR (text_detection.py finds text positions).
# This understands WHAT is on screen — what app, what state,
# what the user is looking at, what actions are possible.
#
# Uses Groq LLaMA vision model via base64 encoded screenshot.
# Falls back to OCR summary if vision model unavailable.

import os
import cv2
import json
import re
import base64
import tempfile
from openai import OpenAI

from vision.screen_capture import capture_screen
from vision.text_detection import find_text_on_screen

# -------------------------
# CLIENT — Groq vision
# -------------------------

GROQ_KEY = os.getenv("GROQ_API_KEY")

client = None
if GROQ_KEY:
    client = OpenAI(
        api_key=GROQ_KEY,
        base_url="https://api.groq.com/openai/v1"
    )

# -------------------------
# VISION PROMPT
# -------------------------

SYSTEM_PROMPT = """You are Fury's vision engine analyzing a Windows screenshot.
Return ONLY a JSON object. No explanation. No markdown. No backticks.

Format:
{
  "app": "<active app name or null>",
  "state": "<what is happening on screen in one sentence>",
  "visible_text": ["<key text item 1>", "<key text item 2>"],
  "possible_actions": ["<action 1>", "<action 2>", "<action 3>"],
  "error_detected": true or false,
  "error_message": "<error text if visible, else null>",
  "ready_for_input": true or false
}

Rules:
- app should be the foreground application name (notepad, chrome, vscode, etc.)
- state is one clear sentence describing what the user sees
- visible_text lists up to 5 most important text items on screen
- possible_actions lists what a user could do next (max 3)
- error_detected is true if any error dialog, red text, or failure message is visible
- ready_for_input is true if a text field or terminal is waiting for input
"""


# -------------------------
# MAIN FUNCTIONS
# -------------------------

def understand_screen():
    """
    Take a screenshot and return semantic understanding of what's on screen.

    Returns a dict with app, state, visible_text, possible_actions, etc.
    Falls back to OCR-based summary if vision LLM unavailable.
    """

    img = capture_screen()

    if img is None:
        return _empty_understanding("No screen captured")

    # encode to base64 for LLM
    b64 = _encode_image(img)

    if client is None or b64 is None:
        return _ocr_fallback(img)

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": SYSTEM_PROMPT
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.1,
            max_tokens=400
        )

        raw = response.choices[0].message.content.strip()
        raw = re.sub(r"```json", "", raw)
        raw = re.sub(r"```", "", raw)

        understanding = json.loads(raw)
        _print_understanding(understanding)
        return understanding

    except Exception as e:
        print(f"VisionUnderstanding error: {e}")
        return _ocr_fallback(img)


def check_for_error():
    """
    Quick check — is there an error on screen right now?
    Returns error message string or None.
    """
    understanding = understand_screen()
    if understanding.get("error_detected"):
        return understanding.get("error_message")
    return None


def get_screen_state():
    """
    Returns a plain English description of what's on screen.
    Used by other agents to make decisions.
    """
    understanding = understand_screen()
    return understanding.get("state", "unknown")


def is_ready_for_input():
    """
    Returns True if screen has an active input field waiting.
    """
    understanding = understand_screen()
    return understanding.get("ready_for_input", False)


# -------------------------
# HELPERS
# -------------------------

def _encode_image(img):
    """Encode OpenCV image to base64 JPEG string."""
    try:
        # resize to reduce tokens — 1280px wide max
        h, w = img.shape[:2]
        if w > 1280:
            scale = 1280 / w
            img = cv2.resize(img, (1280, int(h * scale)))

        _, buffer = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 75])
        return base64.b64encode(buffer).decode("utf-8")
    except Exception as e:
        print(f"Image encode error: {e}")
        return None


def _ocr_fallback(img):
    """
    When vision LLM is unavailable, extract text via pytesseract
    and return a basic understanding dict.
    """
    try:
        import pytesseract
        import cv2 as _cv2
        gray = _cv2.cvtColor(img, _cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        lines = [l.strip() for l in text.splitlines() if l.strip()][:5]
        return {
            "app": None,
            "state": "Screen captured via OCR fallback",
            "visible_text": lines,
            "possible_actions": [],
            "error_detected": any(
                w in text.lower() for w in ["error", "failed", "exception"]
            ),
            "error_message": None,
            "ready_for_input": False
        }
    except Exception as e:
        return _empty_understanding(f"OCR fallback failed: {e}")


def _empty_understanding(reason=""):
    return {
        "app": None,
        "state": reason or "unknown",
        "visible_text": [],
        "possible_actions": [],
        "error_detected": False,
        "error_message": None,
        "ready_for_input": False
    }


def _print_understanding(u):
    print("\n--- Vision Understanding ---")
    print(f"App     : {u.get('app')}")
    print(f"State   : {u.get('state')}")
    print(f"Actions : {u.get('possible_actions')}")
    if u.get("error_detected"):
        print(f"ERROR   : {u.get('error_message')}")
    print("----------------------------\n")