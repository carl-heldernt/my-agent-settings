"""Tests for the Antigravity git commit PreToolUse hook."""

from __future__ import annotations

import importlib.util
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path
import unittest


HOOK_PATH = Path(__file__).resolve().parents[1] / "tools/antigravity/global/hooks/validate_git_commit.py"
SPEC = importlib.util.spec_from_file_location("validate_git_commit_agy", HOOK_PATH)
assert SPEC and SPEC.loader
HOOK = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = HOOK
SPEC.loader.exec_module(HOOK)


class ValidateGitCommitAgyTests(unittest.TestCase):
    def validate(self, command: str | None, tool_name: str = "run_command", change_size: object | None = None) -> dict[str, str]:
        args: dict[str, str] = {}
        if command is not None:
            args["CommandLine"] = command
            args["Cwd"] = "."
        payload = {
            "toolCall": {
                "name": tool_name,
                "args": args,
            },
            "stepIdx": 1,
            "workspacePaths": ["."],
        }
        original_stdin = HOOK.sys.stdin
        original_change_size = HOOK.get_change_size
        stdout = io.StringIO()
        try:
            HOOK.sys.stdin = io.StringIO(json.dumps(payload))
            effective_size = change_size or HOOK.ChangeSize(files=0, lines=0)
            HOOK.get_change_size = lambda _cwd: effective_size
            with redirect_stdout(stdout):
                try:
                    HOOK.main()
                except SystemExit:
                    pass
        finally:
            HOOK.sys.stdin = original_stdin
            HOOK.get_change_size = original_change_size
        output_str = stdout.getvalue().strip()
        return json.loads(output_str) if output_str else {}

    def test_allows_valid_subject_and_bullet_body(self) -> None:
        result = self.validate('git commit -m "feat(hooks): add commit validation" -m "- what: validate commit messages\n- why: prevent invalid repository history"')
        self.assertEqual(result, {"decision": "allow"})

    def test_allows_ansi_c_quoted_multiline_body(self) -> None:
        command = "git commit -m \"feat(hooks): add commit validation\" -m $'- what: validate commit messages\\n- why: prevent invalid repository history'"
        result = self.validate(command)
        self.assertEqual(result, {"decision": "allow"})

    def test_allows_breaking_change_footer(self) -> None:
        result = self.validate('git commit -m "feat!(api): remove legacy endpoint" -m "- what: remove the legacy endpoint\n- why: complete the API migration\nBREAKING CHANGE: remove /v1/legacy."')
        self.assertEqual(result, {"decision": "allow"})

    def test_rejects_invalid_subject(self) -> None:
        result = self.validate('git commit -m "Add hook"')
        self.assertEqual(result.get("decision"), "deny")
        self.assertIn("must match", result.get("reason", ""))

    def test_rejects_non_imperative_subject(self) -> None:
        result = self.validate('git commit -m "fix(hooks): fixed validation"')
        self.assertEqual(result.get("decision"), "deny")
        self.assertIn("imperative", result.get("reason", ""))

    def test_rejects_long_subject(self) -> None:
        result = self.validate('git commit -m "feat(hooks): add a validation command with an excessively long subject"')
        self.assertEqual(result.get("decision"), "deny")
        self.assertIn("50 characters", result.get("reason", ""))

    def test_rejects_body_lines_without_bullets(self) -> None:
        result = self.validate('git commit -m "docs(hooks): describe validation" -m "first line\nsecond line"')
        self.assertEqual(result.get("decision"), "deny")
        self.assertIn("bullets", result.get("reason", ""))

    def test_rejects_missing_breaking_change_footer(self) -> None:
        result = self.validate('git commit -m "feat!(api): remove legacy endpoint" -m "- what: remove the legacy endpoint\n- why: complete the API migration"')
        self.assertEqual(result.get("decision"), "deny")
        self.assertIn("BREAKING CHANGE", result.get("reason", ""))

    def test_rejects_ai_metadata(self) -> None:
        result = self.validate('git commit -m "docs(hooks): add usage guide" -m "- why: Made with Gemini"')
        self.assertEqual(result.get("decision"), "deny")
        self.assertIn("AI signatures", result.get("reason", ""))

    def test_rejects_opaque_message_source(self) -> None:
        result = self.validate("git commit -F message.txt")
        self.assertEqual(result.get("decision"), "deny")
        self.assertIn("Unsupported git commit option", result.get("reason", ""))

    def test_rejects_missing_body(self) -> None:
        result = self.validate('git commit -m "fix(hooks): reject empty body"')
        self.assertEqual(result.get("decision"), "deny")
        self.assertIn("Every commit", result.get("reason", ""))

    def test_rejects_multiple_body_arguments(self) -> None:
        command = 'git commit -m "fix(hooks): require contiguous body" -m "- what: require one body argument" -m "- why: avoid blank list spacing"'
        result = self.validate(command)
        self.assertEqual(result.get("decision"), "deny")
        self.assertIn("exactly one -m subject", result.get("reason", ""))

    def test_rejects_blank_body_lines(self) -> None:
        command = 'git commit -m "fix(hooks): require contiguous body" -m "- what: require contiguous body bullets\n\n- why: avoid blank list spacing"'
        result = self.validate(command)
        self.assertEqual(result.get("decision"), "deny")
        self.assertIn("must not contain blank lines", result.get("reason", ""))

    def test_rejects_feat_body_without_what_and_why(self) -> None:
        result = self.validate('git commit -m "feat(hooks): add body validation" -m "- why: enforce useful commit context"')
        self.assertEqual(result.get("decision"), "deny")
        self.assertIn("what", result.get("reason", ""))

    def test_allows_small_docs_body_with_why(self) -> None:
        result = self.validate('git commit -m "docs(hooks): explain body policy" -m "- why: clarify the required commit context"')
        self.assertEqual(result, {"decision": "allow"})

    def test_requires_medium_feat_impact(self) -> None:
        size = HOOK.ChangeSize(files=3, lines=75)
        result = self.validate('git commit -m "feat(hooks): add body policy" -m "- what: validate body details\n- why: improve history quality"', change_size=size)
        self.assertEqual(result.get("decision"), "deny")
        self.assertIn("impact", result.get("reason", ""))

    def test_allows_large_chore_verification(self) -> None:
        size = HOOK.ChangeSize(files=6, lines=201)
        command = 'git commit -m "chore(hooks): update policy checks" -m "- what: update the validation policy\n- why: require useful commit context\n- verification: run the hook test suite"'
        result = self.validate(command, change_size=size)
        self.assertEqual(result, {"decision": "allow"})

    def test_ignores_non_commit_commands(self) -> None:
        result = self.validate('git status && echo "git commit"')
        self.assertEqual(result, {"decision": "allow"})

    def test_ignores_non_run_command_tools(self) -> None:
        result = self.validate(None, tool_name="view_file")
        self.assertEqual(result, {"decision": "allow"})


if __name__ == "__main__":
    unittest.main()
