# My Agent Settings Repository Structure Guide

This repository stores reusable AI coding agent configurations, instructions,
skills, templates, and helper scripts.

The goal is to provide a portable agent development environment that can be
shared across:

- Multiple AI agent tools (Codex CLI, Copilot CLI, and future extensions)
- Multiple machines
- Multiple repositories (Multi-repository workspaces)
- VSCode multi-root workspaces
- Long-running development sessions with seamless agent-to-agent transitions

Current supported tools:

- OpenAI Codex CLI
- GitHub Copilot CLI

The repository is designed to allow future expansion for additional tools such
as Claude Code, Gemini CLI, Cursor, or other coding agents.


---

# Directory Layout

```text
my-agent-settings/
├── shared/
│   ├── AGENTS.md
│   ├── rules/
│   │   ├── language.md
│   │   ├── git-commit.md
│   │   ├── security.md
│   │   └── workspace-context.md   # Rules for handling multi-repo environments
│   └── workflows/
│       └── session-handoff.md     # Standard operating procedure for handoffs
│
├── tools/
│   ├── codex/
│   │   ├── global/
│   │   │   └── AGENTS.md          # Compiled from shared/
│   │   ├── skills/
│   │   │   └── <skill-name>/
│   │   │       └── SKILL.md
│   │   └── templates/
│   │       └── workspace/
│   │
│   └── copilot/
│       ├── global/
│       │   └── copilot-instructions.md # Compiled from shared/
│       ├── instructions/
│       │   └── *.instructions.md
│       └── templates/
│           └── workspace/
│
├── templates/
│   ├── workspace/                 # For root directories like GitLab/ or GitHub/
│   │   └── .ai-session/           # Tool-neutral session state bridge
│   │       ├── handoff.md
│   │       └── tasks/
│   └── repo/                      # Single repository configuration
│
├── scripts/
│   ├── build.py                   # Compiles/injects shared/ rules into tool configs (DRY)
│   ├── deploy-global.sh           # Deploys global configurations (User-level / Machine-wide)
│   └── deploy-workspace.sh        # Deploys configurations using Symlinks to workspace root
│
├── docs/
├── README.md
└── LICENSE
```

---

# Directory Description

## shared/

Common rules and workflows shared by multiple AI agents.

Content in this directory is strictly **tool-neutral** and acts as the **Single Source of Truth (SSOT)**.

Examples:

- Preferred response language
- Coding conventions
- Git commit message rules (e.g., cleaning up AI metadata/signatures)
- Security requirements
- Multi-repo environment routing constraints (`workspace-context.md`)

Design rule:

Create shared knowledge once, then use `scripts/build.py` to compile and map it into each agent's native format.


### Versioning

To track rule evolution and enable agents to report which version they follow, `shared/` includes:

```text
shared/
├── VERSION           # Single-line semantic version (e.g., 1.2.0)
├── CHANGELOG.md      # Version history with Added/Changed/Removed sections
└── rules/
```

**VERSION**: Plain text file for easy parsing by `build.py`, which injects it into compiled outputs.

**CHANGELOG.md** example:
```markdown
## [1.2.0] - 2026-06-09
### Added
- workspace-context.md: New monorepo path resolution rules

### Changed
- git-commit.md: Removed default Co-authored-by trailer behavior

## [1.1.0] - 2026-05-15
### Added
- security.md: Prohibit hardcoded secrets
```

Compiled outputs (e.g., `AGENTS.md`) automatically include a header comment:
```markdown
<!-- Generated from my-agent-settings v1.2.0 | 2026-06-09 -->
```

```text
                  [ shared/rules/ ]
                          |
                   scripts/build.py
                          |
        +-----------------+-----------------+
        |                                   |
        v                                   v
tools/codex/global/AGENTS.md      tools/copilot/global/copilot-instructions.md
```


---

# tools/

Agent-specific configuration and syntax implementations.

Each supported tool owns its own directory. Tool-specific formats and specialized instructions stay here instead of being mixed with shared configurations.


## tools/codex/

OpenAI Codex specific configuration.

Used for:
- Codex user instructions
- Codex global skills
- Codex workspace initialization

Typical installation targets (via Symlinks):
```text
~/.codex/
└── AGENTS.md                      # Symlinked from tools/codex/global/AGENTS.md
└── skills/
    ├── handoff-brief/            # Symlinked from tools/codex/skills/
    ├── handoff-update/
    └── handoff-close/
```


## tools/copilot/

GitHub Copilot specific configuration.

Used for:
- Copilot repository/workspace instructions
- Copilot CLI operational behavior

Typical installation target (via Symlinks):
```text
/workspace-root/ (e.g., GitLab/)
└── .github/ -> tools/copilot/     # Symlinked folder for Copilot context
```


---

# templates/

Ready-to-copy workspace or repository templates. Unlike `tools/`, templates contain the final generated layout that should appear inside a project or a platform root directory.


## templates/workspace/

Designed for platform-level root directories containing multiple repositories (e.g., `~/workspace/GitLab/` or `~/workspace/GitHub/`).

```text
GitLab/ (Workspace Root)
├── repo-a/                        # Sub-repository A
├── repo-b/                        # Sub-repository B
├── repo-c/                        # Sub-repository C
├── .github/                       # Symlink to Copilot configurations
└── .ai-session/                   # Local physical directory (Not Symlinked)
    ├── handoff.md                 # Universal cross-agent session state bridge
    └── tasks/
```

Key Benefits:
- Allows agents to maintain a macro-perspective of the entire platform or cross-repo dependencies.
- Keeps temporary session text local to the workspace root without polluting individual repository Git histories.
- Keeps cross-workspace Codex handoff skills in one global location instead
  of duplicating them under each workspace root.

Workspace root constraint:
- Workspace roots are coordination directories, not Git repositories.
- Do not create, restore, or retain a `.git/` directory at roots such as
  `~/workspace/`, `~/workspace/GitHub/`, or `~/workspace/GitLab/`.


## templates/repo/

Single repository configuration for isolated projects.


---

# scripts/

Automation and synchronization helpers.

### `build.py` (Rule Compiler)
Dynamically injects tool-neutral rules from `shared/rules/` into specific agent configuration templates (e.g., combining `git-commit.md` and `security.md` into Copilot's system instructions). This prevents duplication and ensures alignment across tools.

**Validation Mode (`--validate`)**:

The build script includes validation to prevent broken or oversized outputs:

| Check | Description |
|-------|-------------|
| Token limits | Copilot instructions should be < 8K tokens (uses `tiktoken`) |
| Required sections | Ensures `## Security`, `## Language`, etc. are present |
| Markdown syntax | Validates format via `mdformat` or `markdownlint` |
| No residual placeholders | Confirms no `{{placeholder}}` remains unreplaced |

Example output:
```bash
$ python scripts/build.py --validate
✓ tools/codex/global/AGENTS.md (2,847 tokens)
✓ tools/copilot/global/copilot-instructions.md (3,102 tokens)
✗ tools/copilot/instructions/debug.instructions.md
  → ERROR: Exceeds 8000 token limit (8,234 tokens)
  → WARNING: Missing ## Security section
```

### `deploy-global.sh` (Global Setup Manager)
Initializes user-level and machine-wide configuration files. It creates standard global config directories (e.g., `~/.codex/`) and establishes symbolic links targeting compiled global rules and shared Codex skills.

### `deploy-workspace.sh` (Workspace Deployment Manager)
Initializes a target workspace root directory (e.g., `~/workspace/GitLab/`).
- **Uses Symbolic Links (`ln -sf`)** for workspace-level configurations so that updates in this settings repository propagate instantly across all development environments without manual re-installation.
- **Initializes local `.ai-session/` templates** if they do not already exist to track local session variables safely.
- **Does not install Codex skills into the workspace root.** Shared Codex
  handoff skills are installed globally under `~/.codex/skills/` by
  `deploy-global.sh`.

---

# Secrets Management Convention

Agents must have clear guidance on where secrets are (and are not) stored.

### Prohibited Locations
- `.ai-session/` directory
- Any Git-tracked files
- Inline in instructions or rules

### Lookup Order
When credentials are needed, agents should check these locations in order:

1. **Environment variables** — prefer `$XYZ_API_KEY` naming convention
2. **Tool-specific config** — `~/.config/<tool>/credentials`
3. **Repo-level `.env`** — must be gitignored
4. **Ask the user** — prompt explicitly rather than failing silently

### Default `.gitignore` Entries
Templates should include:
```gitignore
.env
.env.*
*.pem
*.key
```


---

# Testing Strategy (CI Validation)

Automated checks ensure repository integrity and prevent broken configurations.

## GitHub Actions Workflow

`.github/workflows/validate.yml`:
```yaml
name: Validate Settings

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check required files exist
        run: |
          test -f shared/AGENTS.md
          test -f shared/rules/security.md
          test -d tools/codex/global
          test -d tools/copilot/global

      - name: Lint Markdown
        uses: DavidAnson/markdownlint-cli2-action@v16
        with:
          globs: '**/*.md'

      - name: Run build and validate
        run: |
          pip install tiktoken
          python scripts/build.py --validate

      - name: Verify symlink targets exist
        run: |
          # Ensure all symlink sources referenced in deploy scripts exist
          grep -oP '(?<=-> ).*' scripts/deploy-workspace.sh | while read target; do
            test -e "$target" || (echo "Missing: $target" && exit 1)
          done
```

## Local Pre-commit Hook

`scripts/pre-commit`:
```bash
#!/bin/bash
python scripts/build.py --validate || exit 1
```

Install with:
```bash
ln -sf ../../scripts/pre-commit .git/hooks/pre-commit
```


---

# Session Handoff Strategy (Cross-Tool Continuity)

To ensure seamless transition when switching between tools (e.g., exhausting Codex CLI quotas and instantly switching to Copilot CLI), agents must share a persistent, tool-agnostic state layer.

Instead of tool-specific state stores, all agents are instructed to communicate via a universal tracking directory at the workspace root:

```text
.ai-session/
├── handoff.md
└── tasks/
```

### Shared State Protocol:
1. **Initialization:** Every agent session begins by reading `.ai-session/handoff.md` to instantly absorb the current technical context, high-level business goals, completed changes, and pending tasks.
2. **Explicit Routing:** In `shared/rules/workspace-context.md`, agents are instructed to acknowledge they are operating at a multi-repo root level and to track modified files using explicit relative paths (e.g., `./repo-a/src/main.py`).
3. **Session Closure:** Upon completing a task or intercepting a session close command, the active agent updates the current state in `.ai-session/handoff.md` for the next agent to consume.

**Do not store:** Raw conversation logs, credentials, tokens, or environment secrets.


---

# Adding a New Agent Tool

To onboard a new agent (e.g., `tools/claude/`, `tools/gemini/`, `tools/cursor/`):

1. Keep foundational logic and architectural principles in `shared/`.
2. Map out tool-specific entrypoints in `tools/<tool-name>/` (e.g., `.cursorrules` or `.claudecodejson`).
3. Update `scripts/build.py` to support the new tool's compilation targets.
4. Update `scripts/deploy-workspace.sh` or `deploy-global.sh` to include the symlink paths for the new tool.


---

# Design Principle

Agent sessions are temporary.  
Engineering context must be persistent and tool-neutral.  

This repository governs the persistent context layer that bridges the gaps between disparate AI coding workflows.
