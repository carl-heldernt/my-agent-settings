---
name: handoff-brief
description: Review the current state of a multi-repo development workspace at the beginning of a new session. Use when Codex needs to read `AGENTS.md`, read `.ai-session/handoff.md`, inspect git status across all repos in the workspace, summarize current project state, and suggest the next recommended steps before resuming work.
---

# Handoff Brief

## Overview

Rebuild session context quickly from durable workspace artifacts and live repo state.
Use this skill before taking action in a long-running VSCode workspace.

The active handoff scope is the platform-level workspace root (e.g., `~/workspace/GitLab/`).
Use the `.ai-session/` directory at that level for all handoff state.

## Start-of-Session Workflow

1. Read `AGENTS.md`.
2. Read the workspace's `.ai-session/handoff.md`.
3. Read relevant files in `.ai-session/tasks/`
   when the active TODO items in
   the handoff point to task-level detail.
4. Read today's session log if it exists and appears relevant.
5. Inspect the workspace root repo and each child repo with a `.git` directory.
6. Produce a concise summary of:
   - current goal
   - active repos and dirty repos
   - recent meaningful changes
   - active TODO items and linked task files when relevant
   - blockers or contradictions between the handoff and actual repo state
7. Recommend the most sensible next steps.

## Repo Inspection Rules

- Inspect each repo independently.
- Prefer `git status --short --branch` first.
- Use `git log --oneline -n 3` or `git log --oneline --decorate -n 5` when recent history matters.
- Call out repos with uncommitted changes, detached heads, merge conflicts, or branch drift.
- Avoid deep code review unless the user asks for it.

## Output Requirements

Present:

1. A short workspace state summary
2. A repo-by-repo status snapshot
3. A list of active TODO items or linked task files when relevant
4. A list of important blockers or uncertainties
5. A prioritized next-step recommendation

## Reconciliation Rules

- Trust live repo state over stale handoff notes.
- If `.ai-session/handoff.md` appears outdated, say so explicitly.
- Highlight mismatches between documented status and actual git status.
- Preserve factual uncertainty instead of guessing.

## Writing Rules

- Keep the brief concise, factual, and operational.
- Focus on what the next session needs in order to act.
- Mention exact repos, branches, and files only when they influence the next decision.
- Do not rewrite `.ai-session/handoff.md` unless
  the user asks or another workflow requires it.
- Do not rewrite task files unless the user asks or another workflow
  requires it.

## Safety Rules

- Never copy raw `~/.codex/sessions` data into the workspace.
- Do not turn the brief into a transcript of earlier chats.
- Do not report secrets or sensitive values from environment files.
