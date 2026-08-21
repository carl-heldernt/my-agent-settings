"""Tests for the Codex git commit PreToolUse hook."""

from __future__ import annotations

import importlib.util
import io
import json
import sys
from contextlib import redirect_stderr
from pathlib import Path
import unittest


HOOK_PATH = Path(__file__).resolve().parents[1] / "tools/codex/global/hooks/validate_git_commit.py"
SPEC = importlib.util.spec_from_file_location("validate_git_commit", HOOK_PATH)
assert SPEC and SPEC.loader
HOOK = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = HOOK
SPEC.loader.exec_module(HOOK)


class ValidateGitCommitTests(unittest.TestCase):
    def validate(self, command: str, change_size: object | None = None) -> tuple[int, str]:
        payload = {"tool_name": "Bash", "tool_input": {"command": command}}
        original_stdin = HOOK.sys.stdin
        original_change_size = HOOK.get_change_size
        stderr = io.StringIO()
        try:
            HOOK.sys.stdin = io.StringIO(json.dumps(payload))
            effective_size = change_size or HOOK.ChangeSize(files=0, lines=0)
            HOOK.get_change_size = lambda _cwd: effective_size
            with redirect_stderr(stderr):
                try:
                    code = HOOK.main()
                except SystemExit as error:
                    code = int(error.code)
        finally:
            HOOK.sys.stdin = original_stdin
            HOOK.get_change_size = original_change_size
        return code, stderr.getvalue()

    def test_allows_valid_subject_and_bullet_body(self) -> None:
        code, output = self.validate('git commit -m "feat(hooks): add commit validation" -m "- what: validate commit messages\n- why: prevent invalid repository history"')
        self.assertEqual((code, output), (0, ""))

    def test_allows_ansi_c_quoted_multiline_body(self) -> None:
        command = "git commit -m \"feat(hooks): add commit validation\" -m $'- what: validate commit messages\\n- why: prevent invalid repository history'"
        code, output = self.validate(command)
        self.assertEqual((code, output), (0, ""))

    def test_allows_breaking_change_footer(self) -> None:
        code, output = self.validate('git commit -m "feat!(api): remove legacy endpoint" -m "- what: remove the legacy endpoint\n- why: complete the API migration\nBREAKING CHANGE: remove /v1/legacy."')
        self.assertEqual((code, output), (0, ""))

    def test_rejects_invalid_subject(self) -> None:
        code, output = self.validate('git commit -m "Add hook"')
        self.assertEqual(code, 2)
        self.assertIn("must match", output)

    def test_rejects_non_imperative_subject(self) -> None:
        code, output = self.validate('git commit -m "fix(hooks): fixed validation"')
        self.assertEqual(code, 2)
        self.assertIn("imperative", output)

    def test_rejects_long_subject(self) -> None:
        code, output = self.validate('git commit -m "feat(hooks): add a validation command with an excessively long subject"')
        self.assertEqual(code, 2)
        self.assertIn("50 characters", output)

    def test_rejects_body_lines_without_bullets(self) -> None:
        code, output = self.validate('git commit -m "docs(hooks): describe validation" -m "first line\nsecond line"')
        self.assertEqual(code, 2)
        self.assertIn("bullets", output)

    def test_rejects_missing_breaking_change_footer(self) -> None:
        code, output = self.validate('git commit -m "feat!(api): remove legacy endpoint" -m "- what: remove the legacy endpoint\n- why: complete the API migration"')
        self.assertEqual(code, 2)
        self.assertIn("BREAKING CHANGE", output)

    def test_rejects_ai_metadata(self) -> None:
        code, output = self.validate('git commit -m "docs(hooks): add usage guide" -m "- why: Made with Codex"')
        self.assertEqual(code, 2)
        self.assertIn("AI signatures", output)

    def test_rejects_opaque_message_source(self) -> None:
        code, output = self.validate("git commit -F message.txt")
        self.assertEqual(code, 2)
        self.assertIn("Unsupported git commit option", output)

    def test_rejects_missing_body(self) -> None:
        code, output = self.validate('git commit -m "fix(hooks): reject empty body"')
        self.assertEqual(code, 2)
        self.assertIn("Every commit", output)

    def test_rejects_multiple_body_arguments(self) -> None:
        command = 'git commit -m "fix(hooks): require contiguous body" -m "- what: require one body argument" -m "- why: avoid blank list spacing"'
        code, output = self.validate(command)
        self.assertEqual(code, 2)
        self.assertIn("exactly one -m subject", output)

    def test_rejects_blank_body_lines(self) -> None:
        command = 'git commit -m "fix(hooks): require contiguous body" -m "- what: require contiguous body bullets\n\n- why: avoid blank list spacing"'
        code, output = self.validate(command)
        self.assertEqual(code, 2)
        self.assertIn("must not contain blank lines", output)

    def test_rejects_feat_body_without_what_and_why(self) -> None:
        code, output = self.validate('git commit -m "feat(hooks): add body validation" -m "- why: enforce useful commit context"')
        self.assertEqual(code, 2)
        self.assertIn("what", output)

    def test_allows_small_docs_body_with_why(self) -> None:
        code, output = self.validate('git commit -m "docs(hooks): explain body policy" -m "- why: clarify the required commit context"')
        self.assertEqual((code, output), (0, ""))

    def test_requires_medium_feat_impact(self) -> None:
        size = HOOK.ChangeSize(files=3, lines=75)
        code, output = self.validate('git commit -m "feat(hooks): add body policy" -m "- what: validate body details\n- why: improve history quality"', size)
        self.assertEqual(code, 2)
        self.assertIn("impact", output)

    def test_allows_large_chore_verification(self) -> None:
        size = HOOK.ChangeSize(files=6, lines=201)
        command = 'git commit -m "chore(hooks): update policy checks" -m "- what: update the validation policy\n- why: require useful commit context\n- verification: run the hook test suite"'
        code, output = self.validate(command, size)
        self.assertEqual((code, output), (0, ""))

    def test_ignores_non_commit_commands(self) -> None:
        code, output = self.validate('git status && echo "git commit"')
        self.assertEqual((code, output), (0, ""))


if __name__ == "__main__":
    unittest.main()
