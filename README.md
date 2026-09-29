# my-agent-settings

Reusable configuration and templates for agent-driven coding workflows.

## What is here

- `shared/`: tool-neutral rules and versioned shared content
- `scripts/`: build and deployment helpers
- `tools/`: tool-specific compiled outputs and skills
- `templates/`: workspace and repository starter layouts

## Using Claude Code

1. Deploy the global settings:
   - `bash scripts/deploy-global.sh`
2. Start Claude Code in any directory. Global instructions are loaded from
   `~/.claude/CLAUDE.md` automatically.
3. To also apply instructions at a workspace root level, run:
   - `bash scripts/deploy-workspace.sh <workspace-root>`
   This creates a `CLAUDE.md` symlink at the workspace root.
4. Use the global Claude Code handoff skills from `~/.claude/skills/`
   (`handoff-brief`, `handoff-update`, `handoff-close`) when you need to brief,
   update, or close a session. They are installed by `deploy-global.sh` and work
   from any workspace root. Run `handoff-compact` on demand (or when
   `handoff-update`/`handoff-close` flags `.ai-session/handoff.md` as
   oversized) to collapse resolved entries into one-line pointers to
   `.ai-session/tasks/`.

## Claude Code Commit Validation Hook

`deploy-global.sh` also merges a `PreToolUse` hook into `~/.claude/settings.json`
that validates Claude Code-initiated `git commit` commands before Git runs,
mirroring the Codex and Antigravity hooks. Every commit must use explicit `-m`
arguments for both the subject and body, and the required body bullets scale
by commit type and staged change size the same way as the other tools. Because
`~/.claude/settings.json` also holds personal, non-repo settings (theme,
status line, model, ...), `deploy-global.sh` cannot symlink it outright;
instead `scripts/merge_claude_hooks.py` merges just the shared hook fragment
from `tools/claude/global/hooks.json` into it, leaving every other key and
hook untouched. Re-run `bash scripts/deploy-global.sh` after any policy update
to refresh the merged hook. Use `/hooks` in Claude Code to review it.

## Shared Commit Validation Logic

The Codex, Claude Code, and Antigravity commit-validation hooks all enforce
the same policy but speak different stdin/stdout protocols. Rather than
maintain three near-duplicate scripts, the policy itself lives once in
`shared/hooks/validate_git_commit_core.py`; each tool supplies a small
`tools/<tool>/global/hooks_adapter.py` with just its protocol glue, and
`python3 scripts/build.py` compiles core + adapter into each deployed
`tools/<tool>/global/hooks/validate_git_commit.py`. Edit the policy in the
core file, run `python3 scripts/build.py`, and all three tools pick up the
change.

## Using Codex CLI

1. Deploy the workspace and global settings if needed:
   - `bash scripts/deploy-global.sh`
   - `bash scripts/deploy-workspace.sh <workspace-root>`
2. Start Codex in the workspace root.
3. Use the global Codex handoff skills from `~/.codex/skills/` when you need
   to brief, update, or close a session (`handoff-brief`, `handoff-update`,
   `handoff-close`). Run `handoff-compact` on demand (or when
   `handoff-update`/`handoff-close` flags `.ai-session/handoff.md` as
   oversized) to collapse resolved entries into one-line pointers to
   `.ai-session/tasks/`.
4. If you are moving from legacy `.codex` handoff files, run:
   - `bash scripts/migrate-codex-to-ai-session.sh <workspace-root>`

## Codex Commit Validation Hook

`deploy-global.sh` also installs a Codex `PreToolUse` hook that validates
Codex-initiated `git commit` commands before Git runs. Every commit must use
explicit `-m` arguments for both the subject and body. The required body
bullets scale by commit type and staged change size: `docs`/`chore` changes
start with a `why`, while `feat`/`fix` changes require `what` and `why`; larger
changes additionally require impact, tests, or verification details. Use one
body `-m` argument containing newline-separated bullets without blank lines.
Opaque
message sources such as `-F` or editor-based commits are rejected.

After the first installation, start Codex and use `/hooks` to review and trust
the hook. Codex skips changed non-managed hooks until they are trusted again.
The hook only governs Bash commands issued by Codex; it does not replace a Git
`commit-msg` hook for manual or other-agent commits.

## Using Antigravity CLI (`agy`)

1. Deploy the global settings:
   - `bash scripts/deploy-global.sh`
2. Start `agy` in any directory. Global instructions are loaded from
   `~/.gemini/antigravity-cli/GEMINI.md` automatically.
3. To also apply instructions at a workspace root level, run:
   - `bash scripts/deploy-workspace.sh <workspace-root>`
   This creates a `GEMINI.md` symlink at the workspace root.
4. Use the global Antigravity handoff skills from `~/.gemini/antigravity-cli/skills/`
   (`handoff-brief`, `handoff-update`, `handoff-close`, `handoff-compact`) when you need to
   brief, update, close, or compact a session. They are installed by `deploy-global.sh` and
   work from any workspace root.

## Antigravity Commit Validation Hook

`deploy-global.sh` installs an Antigravity `PreToolUse` hook in
`~/.gemini/antigravity-cli/hooks.json` that validates agent-initiated `git commit` commands
before `run_command` executes. Every commit must follow the shared 50/72 commit-message
policy and include required body bullets. Non-compliant commits are rejected with a descriptive
reason.

## Using Copilot CLI

1. Deploy the workspace settings:
   - `bash scripts/deploy-workspace.sh <workspace-root>`
2. Start Copilot in the workspace root.
3. Read and update `.ai-session/handoff.md` when resuming or closing work.
4. Use `.github/instructions/**/*.instructions.md` and `.github/copilot-instructions.md` for Copilot-specific guidance.

## Common commands

- `python3 scripts/build.py` to generate compiled tool outputs
- `python3 scripts/build.py --validate` to validate inputs only
- `bash scripts/deploy-global.sh` to install global Codex, Claude Code, and Antigravity config (including the Claude Code commit-validation hook merge)
- `bash scripts/deploy-workspace.sh <workspace-root>` to initialize a workspace root
- `bash scripts/migrate-codex-to-ai-session.sh <workspace-root>` to move legacy `.codex` handoff data into `.ai-session`

## When to run scripts

- Run `python3 scripts/build.py` whenever you change shared rules, shared workflows, Copilot instruction sources, or the shared commit-validation hook (`shared/hooks/validate_git_commit_core.py`) or a tool's `hooks_adapter.py`, since all of these feed generated outputs under `tools/*/global/`.
- Run `python3 scripts/build.py --validate` when you want a quick consistency check without rewriting generated files.
- Do not run deployment or migration scripts for documentation-only changes unless you are intentionally applying the updated templates or configuration to a real workspace.
- Run `bash scripts/deploy-workspace.sh <workspace-root>` only when you need to refresh a workspace with updated `.ai-session/` templates, Copilot workspace files, or the workspace-level `CLAUDE.md`/`GEMINI.md` symlinks.
- Run `bash scripts/deploy-global.sh` only when you need to refresh the installed global Codex, Claude Code, and Antigravity configuration.

- Run `bash scripts/migrate-codex-to-ai-session.sh <workspace-root>` only when moving an existing workspace from legacy `.codex` handoff state.

## Task file status model

- Keep `.ai-session/tasks/` as a flat directory.
- Name task files as `<status>--<slug>.md`.
- Allowed statuses are `draft`, `in-progress`, and `done`.
- Use YAML frontmatter in every task file.
- Treat `frontmatter.status` as the source of truth.
- Keep the filename prefix synchronized with `frontmatter.status`.
- Treat `<slug>` as the stable task identity across status changes.
