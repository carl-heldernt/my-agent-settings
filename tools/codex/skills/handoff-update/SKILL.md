---
name: handoff-update
description: Update workspace handoff records for a multi-repo development workspace. Use when Codex needs to refresh `.ai-session/handoff.md` and `.ai-session/session-log/YYYY-MM-DD.md` based on current workspace context, recent development activity, git status, modified files, recent commits, and current task progress during long-running or multi-day work.
---

# Handoff Update

## Overview

Refresh the durable workspace handoff documents after meaningful
progress. Summarize engineering state, not chat history.

The active handoff scope is the platform-level workspace root (e.g., `~/workspace/GitLab/`).
Use the `.ai-session/` directory at that level for all handoff state.

## Workflow

1. Read `AGENTS.md`, `.ai-session/handoff.md`,
   and today's session log if it exists.
2. Inspect the workspace root and each repo that has a `.git` directory.
3. Capture:
   - branch and cleanliness
   - modified, added, deleted, and untracked files
   - recent commits that affect the current task
   - the active goal and current progress
4. Create or update `.ai-session/tasks/*.md`
   when active TODO items need
   durable task-level detail beyond the summary handoff.
5. For every task file you create or update:
   - use the filename format `<status>--<slug>.md`
   - allow only `draft`, `in-progress`, or `done`
   - store the authoritative state in YAML frontmatter as `status`
   - keep the filename prefix synchronized with `frontmatter.status`
6. Update `.ai-session/handoff.md` to reflect
   the latest durable summary state.
7. Create or append `.ai-session/session-log/YYYY-MM-DD.md` with a short timestamped entry.

## Repo Inspection Rules

- Treat the workspace root repo and child repos as separate units.
- Prefer concise command-based inspection such as `git status --short --branch`, `git diff --stat`, and `git log --oneline -n 5`.
- Record only information that helps the next session act quickly.
- Mention cross-repo dependencies when one repo blocks or informs another.
- Keep detailed subtask notes in `.ai-session/tasks/` when they would make the main handoff noisy.

## Required Handoff Format

Use this section order in `.ai-session/handoff.md`:

1. `Current Goal`
2. `Current Status`
3. `Important Decisions`
4. `Relevant Repos / Files`
5. `Commands Already Run`
6. `Known Issues`
7. `Next Suggested Steps`

## Session Log Rules

- Use `.ai-session/session-log/YYYY-MM-DD.md`.
- Append new entries instead of rewriting the full day unless the file is still a trivial stub.
- Prefix each entry with a timestamp.
- Keep entries shorter than the main handoff unless a risk needs more detail.

## Writing Rules

- Keep summaries concise and factual.
- Prefer actionable engineering context over narrative prose.
- Mention exact repos, files, commands, and blockers when they matter.
- Do not invent progress that cannot be supported by repo state.
- Do not paste raw diffs unless a tiny excerpt is essential.

## Safety Rules

- Never copy or persist raw `~/.codex/sessions` or other Codex JSONL session files into the workspace.
- Do not turn the handoff into a transcript.
- Do not store secrets, tokens, or private credentials in handoff files.

## Expected Output Shape

Update `.ai-session/handoff.md` as the durable summary.

Update `.ai-session/tasks/*.md` when a TODO item needs:

- background or decision context
- a checklist or subtask breakdown
- validation details
- blockers or resume notes across sessions

Task files should follow this minimum shape:

```markdown
---
status: in-progress
updated_at: YYYY-MM-DD
---

# Task Title

## Summary

## Current State

## Open Questions / Blockers

## Next Actions

## Validation Notes
```

Treat `frontmatter.status` as the source of truth. If a task filename prefix
and `frontmatter.status` disagree, fix the filename on the next write.

Append an entry like this to `.ai-session/session-log/YYYY-MM-DD.md`:

```markdown
## HH:MM TZ

### Current Goal
- ...

### Current Status
- ...

### Important Decisions
- ...

### Relevant Repos / Files
- repo/path - reason

### Commands Already Run
- `...`

### Known Issues
- ...

### Next Suggested Steps
- ...
```
