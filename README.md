# my-agent-settings

Reusable configuration and templates for agent-driven coding workflows.

## What is here

- `shared/`: tool-neutral rules and versioned shared content
- `scripts/`: build and deployment helpers
- `tools/`: tool-specific compiled outputs and skills
- `templates/`: workspace and repository starter layouts

## Using Codex CLI

1. Deploy the workspace and global settings if needed:
   - `bash scripts/deploy-global.sh`
   - `bash scripts/deploy-workspace.sh <workspace-root>`
2. Start Codex in the workspace root.
3. Use the global Codex handoff skills from `~/.codex/skills/` when you need
   to brief, update, or close a session.
4. If you are moving from legacy `.codex` handoff files, run:
   - `bash scripts/migrate-codex-to-ai-session.sh <workspace-root>`

## Using Copilot CLI

1. Deploy the workspace settings:
   - `bash scripts/deploy-workspace.sh <workspace-root>`
2. Start Copilot in the workspace root.
3. Read and update `.ai-session/handoff.md` when resuming or closing work.
4. Use `.github/instructions/**/*.instructions.md` and `.github/copilot-instructions.md` for Copilot-specific guidance.

## Common commands

- `python3 scripts/build.py` to generate compiled tool outputs
- `python3 scripts/build.py --validate` to validate inputs only
- `bash scripts/deploy-global.sh` to install global Codex config and skills
- `bash scripts/deploy-workspace.sh <workspace-root>` to initialize a workspace root
- `bash scripts/migrate-codex-to-ai-session.sh <workspace-root>` to move legacy `.codex` handoff data into `.ai-session`

## When to run scripts

- Run `python3 scripts/build.py` whenever you change shared rules, shared workflows, or Copilot instruction sources that feed generated outputs under `tools/*/global/`.
- Run `python3 scripts/build.py --validate` when you want a quick consistency check without rewriting generated files.
- Do not run deployment or migration scripts for documentation-only changes unless you are intentionally applying the updated templates or configuration to a real workspace.
- Run `bash scripts/deploy-workspace.sh <workspace-root>` only when you need to refresh a workspace with updated `.ai-session/` templates or Copilot workspace files.
- Run `bash scripts/deploy-global.sh` only when you need to refresh the installed global Codex configuration and skills.
- Run `bash scripts/migrate-codex-to-ai-session.sh <workspace-root>` only when moving an existing workspace from legacy `.codex` handoff state.

## Task file status model

- Keep `.ai-session/tasks/` as a flat directory.
- Name task files as `<status>--<slug>.md`.
- Allowed statuses are `draft`, `in-progress`, and `done`.
- Use YAML frontmatter in every task file.
- Treat `frontmatter.status` as the source of truth.
- Keep the filename prefix synchronized with `frontmatter.status`.
- Treat `<slug>` as the stable task identity across status changes.
