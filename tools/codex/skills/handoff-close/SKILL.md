---
name: handoff-close
description: Close out a work session in a multi-repo development workspace. Use when Codex needs to summarize completed work, summarize unfinished work, record blockers or risks, propose next actions, and refresh `.ai-session/handoff.md` before ending major work or handing off to a future session.
---

# Handoff Close

## Overview

Capture the end-of-session engineering state before context is lost.
Refresh the durable handoff so the next session can resume quickly.

The active handoff scope is the platform-level workspace root (e.g., `~/workspace/GitLab/`).
Use the `.ai-session/` directory at that level for all handoff state.

## Closeout Workflow

1. Review `AGENTS.md`, `.ai-session/handoff.md`,
   and the current workspace state.
2. Review relevant files in `.ai-session/tasks/*.md` for unfinished or active TODO items when they
   exist.
3. Inspect each relevant repo for:
   - branch and cleanliness
   - modified or untracked files
   - recent commits in the active workstream
4. Summarize:
   - completed work
   - unfinished work
   - blockers, risks, and unresolved decisions
   - recommended next actions
5. Refresh `.ai-session/tasks/*.md` for any
   unfinished detailed TODO items.
6. Refresh `.ai-session/handoff.md`.
7. Append a concise closeout entry to `.ai-session/session-log/YYYY-MM-DD.md`.

## Required Content

Ensure the handoff covers:

1. `Current Goal`
2. `Current Status`
3. `Important Decisions`
4. `Relevant Repos / Files`
5. `Commands Already Run`
6. `Known Issues`
7. `Next Suggested Steps`

## Closeout Emphasis

- Distinguish clearly between finished and unfinished work.
- Record blockers and risks that could cause the next session to stall.
- Mention any validation that was completed and any validation still missing.
- Highlight dirty repos that must not be forgotten.
- Keep `.ai-session/handoff.md` concise and move
  detailed unfinished task context into `.ai-session/tasks/`
  when needed.

## Writing Rules

- Keep the summary concise and factual.
- Prefer durable engineering context over conversational detail.
- Name exact repos, files, branches, and commands when they matter.
- Use plain language that helps the next session decide what to do first.

## Safety Rules

- Never copy raw `~/.codex/sessions` or other JSONL session artifacts into the workspace.
- Do not store secrets, customer data, or environment values in handoff notes.
- Do not claim work is complete if repo state or tests do not support it.
