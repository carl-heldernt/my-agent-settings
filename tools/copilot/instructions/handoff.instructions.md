# Handoff Instructions

When working in a workspace that uses `.ai-session/`, follow this handoff flow:

## Start of Session

1. Read `.ai-session/handoff.md` first.
2. Read `.ai-session/tasks/` when the handoff references task files.
3. Treat task file `frontmatter.status` as authoritative when task files use
   status prefixes in their filenames.
4. Inspect the repositories in the workspace and trust live git state over stale notes.

## During Work

1. Keep the handoff aligned with meaningful progress.
2. Track cross-repo context using explicit relative paths.
3. Use `.ai-session/tasks/` for detailed task context when needed.
4. Name task files as `<status>--<slug>.md` and keep the filename prefix
   aligned with `frontmatter.status`.

## End of Session

1. Update `.ai-session/handoff.md`.
2. Append a concise entry to `.ai-session/session-log/YYYY-MM-DD.md`.
3. Capture completed work, unfinished work, blockers, and the next suggested step.

## Safety

- Do not store secrets in handoff files.
- Do not copy raw session transcripts into the workspace.
