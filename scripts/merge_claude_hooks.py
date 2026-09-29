#!/usr/bin/env python3
"""Merge the shared Claude Code hook config into ~/.claude/settings.json.

Unlike ~/.codex/hooks.json and ~/.gemini/antigravity-cli/hooks.json, Claude
Code hooks live inside settings.json alongside unrelated personal settings
(theme, statusLine, effortLevel, ...), so that file cannot be replaced with a
symlink. This merges just the hooks fragment in, leaving every other key and
every other configured hook untouched.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FRAGMENT = ROOT / "tools" / "claude" / "global" / "hooks.json"
SETTINGS_PATH = Path.home() / ".claude" / "settings.json"


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8").strip()
    return json.loads(text) if text else {}


def hook_entry_matches(existing: dict, command: str) -> bool:
    return any(hook.get("command") == command for hook in existing.get("hooks", []))


def merge_event(settings_event: list, matcher: str, hooks: list) -> list:
    for group in settings_event:
        if group.get("matcher") != matcher:
            continue
        for hook in hooks:
            if not hook_entry_matches(group, hook.get("command", "")):
                group.setdefault("hooks", []).append(hook)
        return settings_event
    settings_event.append({"matcher": matcher, "hooks": hooks})
    return settings_event


def merge(settings: dict, fragment: dict) -> dict:
    settings.setdefault("hooks", {})
    for event, groups in fragment.get("hooks", {}).items():
        settings["hooks"].setdefault(event, [])
        for group in groups:
            settings["hooks"][event] = merge_event(
                settings["hooks"][event], group["matcher"], group["hooks"]
            )
    return settings


def main() -> int:
    fragment = load_json(SOURCE_FRAGMENT)
    settings = load_json(SETTINGS_PATH)
    merged = merge(settings, fragment)
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
