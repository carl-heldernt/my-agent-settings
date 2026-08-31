---
name: handoff-compact
description: Compact a bloated `.ai-session/handoff.md` in a multi-repo workspace. Use when `handoff.md` has grown large (many long, already-resolved entries duplicating detail that already lives in `.ai-session/tasks/`), when `handoff-close` or `handoff-update` flagged it as oversized, or when the user asks to clean up / shrink / compact the handoff file.
---

# Handoff Compact

## Overview

Shrink `.ai-session/handoff.md` back to a true summary layer by collapsing
resolved entries into short pointers, without losing any information —
because the detail either already lives in `.ai-session/tasks/`, or gets
moved there before the entry is collapsed.

This skill only rewrites `.ai-session/handoff.md` (and, when detail would
otherwise be lost, creates/updates a file in `.ai-session/tasks/`). It does
not summarize sessions or record new progress — that is `handoff-update`'s
and `handoff-close`'s job.

The active handoff scope is the platform-level workspace root (e.g.,
`~/workspace/GitLab/` or `~/workspace/GitHub/`). Use the `.ai-session/` directory at that level.

## When to Run

- `handoff.md` has grown past a size where skimming it no longer works
  (rule of thumb: more than ~150 lines, or any single entry longer than
  ~10 lines).
- `handoff-close` or `handoff-update` printed a compaction suggestion.
- The user explicitly asks for it.

This skill is invoked on demand, not automatically, because collapsing
history is a judgment call with real blast radius (an over-aggressive
collapse can delete context someone still needs). Always run identification
first and let the user see what will change before rewriting.

## Workflow

1. Read `.ai-session/handoff.md` in full.
2. Read every file in `.ai-session/tasks/`.
3. Classify each entry/bullet under `Current Goal` (and other sections that
   have accumulated long entries) into one of:
   - **Collapsible** — marked done/resolved (✅, "結案", "DONE", or clearly
     superseded) AND either already has a linked task file, or its detail
     can be moved into one.
   - **Keep as-is** — still open, blocked, or actively referenced; or a
     short entry that isn't causing bloat.
   - **Ambiguous** — status unclear from the text alone. Do not guess;
     list these separately for the user instead of collapsing them.
4. For each **Collapsible** entry:
   - If a linked task file already fully covers the detail in the entry,
     collapse the entry to one line: status marker, one-sentence outcome,
     and the existing task file path.
   - If no task file exists yet, or the task file is missing detail that
     only exists in `handoff.md`, first write/update that detail into
     `.ai-session/tasks/done--<slug>.md` (using the standard task
     structure), then collapse the `handoff.md` entry to point at it.
   - Never delete information outright — it must land in a task file
     before the handoff entry shrinks.
5. Leave **Keep as-is** and **Ambiguous** entries untouched.
6. Rewrite `.ai-session/handoff.md` with the same required section order
   (`Current Goal`, `Current Status`, `Important Decisions`,
   `Relevant Repos / Files`, `Commands Already Run`, `Known Issues`,
   `Next Suggested Steps`), collapsed entries included as one-liners.
7. Report a before/after summary to the user (line count, number of
   entries collapsed, list of any new/updated task files, list of
   Ambiguous entries left untouched) before finishing.

## Collapsed Entry Format

```text
- ✅ DONE (YYYY-MM-DD): <one-sentence outcome>. Detail: `.ai-session/tasks/done--<slug>.md`.
```

Keep the one sentence factual and specific enough to be useful in a
directory-level skim (what broke / what shipped), not a generic label.

## Safety Rules

- Do not collapse an entry unless its detail is verified to exist in a
  task file after this run.
- Do not collapse entries that are still `IN PROGRESS`, `BLOCKED`, or
  otherwise open, even if they are long.
- Do not touch `.ai-session/session-log/`.
- Do not invent resolution status — if the entry's status is ambiguous,
  leave it and flag it instead of collapsing it.
- Preserve any information about pushed/unpushed commits, unresolved
  owners, or follow-up items — these are exactly the details that go
  missing when compaction is done carelessly.
- Never copy raw Antigravity session data into the workspace.
