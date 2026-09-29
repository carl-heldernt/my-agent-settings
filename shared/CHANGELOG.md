# Changelog

## [0.4.0] - 2026-09-29
### Added
- Claude Code Git commit validation `PreToolUse` hook (`tools/claude/global/hooks.json` and `tools/claude/global/hooks/validate_git_commit.py`), mirroring the Codex and Antigravity hooks.
- `scripts/merge_claude_hooks.py` to merge the shared hook fragment into `~/.claude/settings.json` without disturbing personal settings or other hooks, since that file cannot be symlinked wholesale like `~/.codex/hooks.json`.
- `deploy-global.sh` support for symlinking `~/.claude/hooks/` and running the settings merge.
- Unit tests for the Claude Code commit validation hook (`tests/test_validate_git_commit_claude.py`) and the settings merge (`tests/test_merge_claude_hooks.py`).
- CI validation checks for the new Claude Code hook files.

## [0.3.0] - 2026-08-31
### Added
- Antigravity CLI (`agy`) support: `tools/antigravity/global/GEMINI.md` and `tools/antigravity/workspace/GEMINI.md` compiled from shared rules.
- Antigravity handoff skills (`handoff-brief`, `handoff-update`, `handoff-close`, `handoff-compact`) under `tools/antigravity/skills/`.
- Antigravity Git commit validation `PreToolUse` hook (`tools/antigravity/global/hooks.json` and `tools/antigravity/global/hooks/validate_git_commit.py`).
- `deploy-global.sh` support for Antigravity rules, hooks, and skills deployed into `~/.gemini/antigravity-cli/`.
- `deploy-workspace.sh` support for Antigravity workspace rules (`$WORKSPACE_ROOT/GEMINI.md`).
- Unit tests for Antigravity commit validation hook (`tests/test_validate_git_commit_agy.py`).
- CI validation checks for Antigravity configuration files, skills, and unit tests.

## [0.2.0] - 2026-06-17
### Added
- Claude Code support: `tools/claude/global/CLAUDE.md` compiled from shared rules.
- `deploy-global.sh` now symlinks `~/.claude/CLAUDE.md`.
- `deploy-workspace.sh` now symlinks `$WORKSPACE_ROOT/CLAUDE.md`.
- CI validation checks for `tools/claude/global/CLAUDE.md`.
- Claude Code handoff skills (`handoff-brief`, `handoff-update`, `handoff-close`)
  under `tools/claude/skills/`, mirroring the Codex skills.
- `deploy-global.sh` now symlinks Claude skills into `~/.claude/skills/`.
- CI validation checks for the Codex and Claude handoff skill files.

## [0.1.0] - 2026-06-09
### Added
- Shared rule files for language, commits, security, and workspace context.
- Shared version marker for compiled outputs.
- Initial build script and tool-specific global instruction outputs.
- Workspace and repo template scaffolding.
