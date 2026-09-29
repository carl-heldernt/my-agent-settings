"""Tests for scripts/merge_claude_hooks.py."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts/merge_claude_hooks.py"
SPEC = importlib.util.spec_from_file_location("merge_claude_hooks", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


FRAGMENT = {
    "hooks": {
        "PreToolUse": [
            {
                "matcher": "Bash",
                "hooks": [
                    {
                        "type": "command",
                        "command": "python3 ~/.claude/hooks/validate_git_commit.py",
                        "statusMessage": "Validating git commit message",
                        "timeout": 10,
                    }
                ],
            }
        ]
    }
}


class MergeClaudeHooksTests(unittest.TestCase):
    def test_adds_hook_to_empty_settings(self) -> None:
        merged = MODULE.merge({}, FRAGMENT)
        self.assertEqual(
            merged["hooks"]["PreToolUse"][0]["hooks"][0]["command"],
            "python3 ~/.claude/hooks/validate_git_commit.py",
        )

    def test_preserves_unrelated_settings_and_hooks(self) -> None:
        settings = {
            "theme": "dark",
            "effortLevel": "medium",
            "hooks": {
                "PostToolUse": [
                    {"matcher": "Write", "hooks": [{"type": "command", "command": "prettier"}]}
                ]
            },
        }
        merged = MODULE.merge(settings, FRAGMENT)
        self.assertEqual(merged["theme"], "dark")
        self.assertEqual(merged["effortLevel"], "medium")
        self.assertEqual(merged["hooks"]["PostToolUse"][0]["matcher"], "Write")
        self.assertEqual(
            merged["hooks"]["PreToolUse"][0]["hooks"][0]["command"],
            "python3 ~/.claude/hooks/validate_git_commit.py",
        )

    def test_is_idempotent(self) -> None:
        once = MODULE.merge({}, FRAGMENT)
        twice = MODULE.merge(once, FRAGMENT)
        self.assertEqual(len(twice["hooks"]["PreToolUse"]), 1)
        self.assertEqual(len(twice["hooks"]["PreToolUse"][0]["hooks"]), 1)

    def test_merges_into_existing_bash_matcher(self) -> None:
        settings = {
            "hooks": {
                "PreToolUse": [
                    {
                        "matcher": "Bash",
                        "hooks": [{"type": "command", "command": "echo existing"}],
                    }
                ]
            }
        }
        merged = MODULE.merge(settings, FRAGMENT)
        commands = [hook["command"] for hook in merged["hooks"]["PreToolUse"][0]["hooks"]]
        self.assertIn("echo existing", commands)
        self.assertIn("python3 ~/.claude/hooks/validate_git_commit.py", commands)


if __name__ == "__main__":
    unittest.main()
