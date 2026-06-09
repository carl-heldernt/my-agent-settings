# my-agent-settings

Reusable configuration and templates for agent-driven coding workflows.

## What is here

- `shared/`: tool-neutral rules and versioned shared content
- `scripts/`: build and deployment helpers
- `tools/`: tool-specific compiled outputs and skills
- `templates/`: workspace and repository starter layouts

## Common commands

- `python3 scripts/build.py` to generate compiled tool outputs
- `python3 scripts/build.py --validate` to validate inputs only
- `bash scripts/deploy-global.sh` to install global Codex config
- `bash scripts/deploy-workspace.sh <workspace-root>` to initialize a workspace root
- `bash scripts/migrate-codex-to-ai-session.sh <workspace-root>` to move legacy `.codex` handoff data into `.ai-session`
