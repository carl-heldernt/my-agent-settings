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
