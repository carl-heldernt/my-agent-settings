# Changelog

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
