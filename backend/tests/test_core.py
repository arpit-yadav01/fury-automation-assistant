# backend/tests/test_core.py
# Basic smoke tests for Fury core modules
# Run with: cd backend && pytest tests/ -v

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# -------------------------
# CONFIG TESTS
# -------------------------

def test_config_loads():
    from core.config_loader import cfg
    assert cfg is not None
    assert cfg.fury.name == "Fury"
    assert cfg.ai.model is not None


def test_config_defaults():
    from core.config_loader import cfg
    assert cfg.confidence.high_threshold == 0.75
    assert cfg.confidence.low_threshold == 0.40
    assert cfg.safety.sandbox_mode == False


# -------------------------
# SAFETY SANDBOX TESTS
# -------------------------

def test_blocked_command():
    from core.safety_sandbox import check_command
    blocked, reason = check_command("format c:")
    assert blocked == True
    assert reason is not None


def test_safe_command():
    from core.safety_sandbox import check_command
    blocked, _ = check_command("open youtube and search lofi")
    assert blocked == False


def test_rm_rf_blocked():
    from core.safety_sandbox import check_command
    blocked, _ = check_command("run command rm -rf /")
    assert blocked == True


def test_step_blocked():
    from core.safety_sandbox import is_blocked
    step = {"action": "terminal", "cmd": "format c:"}
    blocked, _ = is_blocked(step)
    assert blocked == True


def test_safe_step():
    from core.safety_sandbox import is_blocked
    step = {"action": "open_url", "url": "https://youtube.com"}
    blocked, _ = is_blocked(step)
    assert blocked == False


# -------------------------
# PERMISSION SYSTEM TESTS
# -------------------------

def test_capabilities_defined():
    from core.permission_system import CAPABILITIES
    assert "browser" in CAPABILITIES
    assert "terminal" in CAPABILITIES
    assert "file_write" in CAPABILITIES
    assert "email" in CAPABILITIES
    assert len(CAPABILITIES) >= 8


def test_action_key_builder():
    from core.permission_system import get_action_key
    step = {"action": "skill", "data": {"intent": "write_code"}}
    key = get_action_key(step)
    assert key == "skill:write_code"

    step2 = {"action": "open_url", "url": "https://youtube.com"}
    key2 = get_action_key(step2)
    assert key2 == "open_url"


# -------------------------
# PATTERN RECOGNIZER TESTS
# -------------------------

def test_pattern_recognizer_runs():
    from brain.pattern_recognizer import analyze_patterns
    result = analyze_patterns()
    assert isinstance(result, dict)
    assert "repeated" in result
    assert "templates" in result
    assert "failures" in result
    assert "top_actions" in result


def test_template_detection():
    from brain.pattern_recognizer import _find_templates
    fake_experiences = [
        {"command": "open youtube and search lofi", "plan": {}, "success": True},
        {"command": "open youtube and search music", "plan": {}, "success": True},
        {"command": "open google and search ai tools", "plan": {}, "success": True},
    ]
    templates = _find_templates(fake_experiences)
    assert len(templates) > 0
    names = [t["template"] for t in templates]
    assert "open_and_search" in names


# -------------------------
# CONFIDENCE ENGINE TESTS
# -------------------------

def test_confidence_known_intent():
    from brain.confidence_engine import _rule_score
    task = {"intent": "open_app", "app": "notepad", "raw": "open notepad"}
    score = _rule_score(task)
    assert score > 0.5


def test_confidence_unknown_intent():
    from brain.confidence_engine import _rule_score
    task = {"intent": "unknown", "raw": "???"}
    score = _rule_score(task)
    assert score == 0.0


def test_confidence_missing_fields():
    from brain.confidence_engine import _rule_score
    task = {"intent": "open_app"}  # missing "app" field
    score = _rule_score(task)
    assert score < 0.75


# -------------------------
# COMMAND PARSER TESTS
# -------------------------

def test_parse_open_app():
    from brain.command_parser import parse_command
    result = parse_command("open notepad")
    assert result["intent"] == "open_app"
    assert result["app"] == "notepad"


def test_parse_typo_open():
    from brain.command_parser import parse_command
    result = parse_command("opne notepad")
    assert result["intent"] == "open_app"
    assert result["app"] == "notepad"


def test_parse_create_file():
    from brain.command_parser import parse_command
    result = parse_command("create test.py")
    assert result["intent"] == "create_file"
    assert result["filename"] == "test.py"


def test_parse_youtube_search():
    from brain.command_parser import parse_command
    result = parse_command("open youtube and search lofi")
    assert result is not None