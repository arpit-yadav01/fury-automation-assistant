# core/config_loader.py
# STEP 122 — Config system
#
# Loads config.yaml once at startup.
# All modules import `cfg` to read settings.
# Falls back to safe defaults if config.yaml missing.
#
# Usage:
#   from core.config_loader import cfg
#   model = cfg.ai.model
#   show = cfg.ui.show_thinking

import os
import yaml
from types import SimpleNamespace

# -------------------------
# PATH
# -------------------------

_DIR = os.path.dirname(os.path.abspath(__file__))
_CONFIG_PATH = os.path.join(os.path.dirname(_DIR), "config.yaml")
_TEMPLATE_PATH = os.path.join(os.path.dirname(_DIR), "config.template.yaml")

# -------------------------
# DEFAULTS
# — used if config.yaml missing or key not set
# -------------------------

DEFAULTS = {
    "fury": {
        "name": "Fury",
        "version": "1.0.0",
        "language": "en",
    },
    "ai": {
        "provider": "groq",
        "model": "llama-3.3-70b-versatile",
        "temperature": 0.3,
        "max_tokens": 1000,
        "vision_model": "meta-llama/llama-4-scout-17b-16e-instruct",
    },
    "voice": {
        "enabled": True,
        "stt_engine": "google",
        "tts_engine": "pyttsx3",
        "tts_rate": 180,
        "wake_word": "hey fury",
    },
    "browser": {
        "engine": "playwright",
        "default": "chrome",
        "headless": False,
        "wait_after_open": 3,
    },
    "memory": {
        "experience_limit": 500,
        "reflection_limit": 100,
        "episode_limit": 1000,
        "pattern_report_every": 10,
    },
    "confidence": {
        "high_threshold": 0.75,
        "low_threshold": 0.40,
        "ask_on_risky": True,
    },
    "safety": {
        "sandbox_mode": False,
        "confirm_delete": True,
        "confirm_terminal": True,
        "blocked_commands": [
            "format c:",
            "rm -rf /",
            "del /f /s /q c:\\",
        ],
    },
    "ui": {
        "show_thinking": True,
        "show_suggestions": True,
        "show_reflection": True,
        "show_confidence": True,
        "show_memory": True,
    },
    "skills": {
        "auto_learn_threshold": 3,
        "skill_dir": "skills/custom",
    },
    "logging": {
        "enabled": True,
        "log_file": "memory/fury.log",
        "level": "INFO",
    },
}


# -------------------------
# LOADER
# -------------------------

def _dict_to_namespace(d):
    """Recursively convert dict to SimpleNamespace for dot access."""
    if isinstance(d, dict):
        return SimpleNamespace(**{k: _dict_to_namespace(v) for k, v in d.items()})
    if isinstance(d, list):
        return [_dict_to_namespace(i) for i in d]
    return d


def _deep_merge(base, override):
    """Merge override into base dict, keeping base values for missing keys."""
    result = base.copy()
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def load_config():
    """
    Load config.yaml, merge with defaults, return as namespace.
    Creates config.yaml from template if missing.
    """
    # auto-create config.yaml from template if missing
    if not os.path.exists(_CONFIG_PATH):
        if os.path.exists(_TEMPLATE_PATH):
            import shutil
            shutil.copy(_TEMPLATE_PATH, _CONFIG_PATH)
            print(f"Config: created config.yaml from template")
        else:
            print("Config: no config.yaml found, using defaults")
            return _dict_to_namespace(DEFAULTS)

    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}

        merged = _deep_merge(DEFAULTS, user_config)
        print(f"Config: loaded from {_CONFIG_PATH}")
        return _dict_to_namespace(merged)

    except Exception as e:
        print(f"Config load error: {e} — using defaults")
        return _dict_to_namespace(DEFAULTS)


# -------------------------
# GLOBAL CONFIG INSTANCE
# -------------------------

cfg = load_config()


# -------------------------
# HELPERS
# -------------------------

def is_command_blocked(command):
    """Check if a terminal command is in the blocked list."""
    cmd = command.lower().strip()
    blocked = getattr(cfg.safety, "blocked_commands", [])
    return any(b.lower() in cmd for b in blocked)


def get_model():
    return cfg.ai.model


def get_vision_model():
    return cfg.ai.vision_model


def show_thinking():
    return cfg.ui.show_thinking


def show_suggestions():
    return cfg.ui.show_suggestions


def show_reflection():
    return cfg.ui.show_reflection