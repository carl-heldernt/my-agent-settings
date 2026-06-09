# Session Handoff Workflow

Use this workflow when a session needs to be resumed by another agent.

## Start of Session

1. Read the active agent instructions.
2. Read the workspace root `.ai-session/handoff.md`.
3. Read relevant files in `.ai-session/tasks/` when task-level detail exists.
4. Inspect the workspace repositories and note the actual git state.

## During Work

1. Keep the durable handoff in sync with meaningful progress.
2. Store task-level detail in `.ai-session/tasks/` when the main handoff is too coarse.
3. Prefer explicit file paths and repository names.

## End of Session

1. Update `.ai-session/handoff.md`.
2. Refresh `.ai-session/session-log/YYYY-MM-DD.md`.
3. Capture blockers, unfinished work, and the next recommended step.
4. Avoid storing secrets, raw chat logs, or transient debugging noise.
