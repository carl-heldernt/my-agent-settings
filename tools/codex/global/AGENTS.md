<!-- Generated from my-agent-settings v0.2.0 | 2026-08-21 -->

# AI Agent Instructions

## Git Commit Rules

- Use the 50/72 rule for commit messages.
- Format subjects as `<type>[!](<scope>): <short-description>`.
- Use lowercase types and scopes.
- Use the imperative mood.
- Do not end the subject line with a period.
- Do not include AI signatures or tool-specific metadata.
- Every commit must include a body using `- <label>: <detail>` bullets.
- Pass the body as exactly one additional `-m` argument with newline-separated
  bullets; do not include blank lines between bullets.
- Select required body labels from the commit type and change size:
  - `docs` and `chore`: small changes require `why`; medium changes require
    `what` and `why`; large changes also require `verification`.
  - `feat` and `fix`: small changes require `what` and `why`; medium changes
    also require `impact`; large changes also require `tests`.
  - Other types require `what` and `why`.
- Treat a change as small when it modifies at most 2 files and 50 lines;
  medium when it modifies at most 5 files and 200 lines; otherwise large.
- If `!` is used, include a `BREAKING CHANGE:` footer.

## Language Rules

- Communicate with the user in Traditional Chinese.
- Keep code identifiers, inline comments, block comments, and docstrings in English.
- Keep technical documentation and specifications in English.

## Security Rules

- Do not store secrets in git-tracked files.
- Do not store secrets in `.ai-session/`.
- Prefer environment variables first.
- Next check tool-specific config under `~/.config/<tool>/credentials`.
- Then use a repo-level `.env` file that is gitignored.
- Ask the user explicitly if credentials are still missing.
- Include `.env`, `.env.*`, `*.pem`, and `*.key` in template ignores.

## Workspace Context Rules

- Treat workspace roots as multi-repository environments when applicable.
- Do not initialize workspace roots as Git repositories.
- Do not create, restore, or keep a `.git/` directory at a workspace root.
- Treat directories such as `~/workspace/`, `~/workspace/GitHub/`, and
  `~/workspace/GitLab/` as coordination roots, not versioned repositories.
- Use explicit relative paths when referring to changed files.
- Keep cross-agent session state in the workspace root `.ai-session/` directory.
- Read and update handoff state through that shared directory.
- Keep temporary session data out of repo histories.

## Session Handoff Workflow

Use this workflow when a session needs to be resumed by another agent.

## Start of Session

1. Read the active agent instructions.
2. Read the workspace root `.ai-session/handoff.md`.
3. Read relevant files in `.ai-session/tasks/` when task-level detail exists.
4. When task files exist, treat `frontmatter.status` as the source of truth
   and use the filename prefix only as a quick visual index.
5. Inspect the workspace repositories and note the actual git state.

## During Work

1. Keep the durable handoff in sync with meaningful progress.
2. Store task-level detail in `.ai-session/tasks/` when the main handoff is too coarse.
3. Name task files as `<status>--<slug>.md` using only `draft`,
   `in-progress`, or `done`.
4. Keep each task file's `frontmatter.status` synchronized with its filename
   prefix.
5. Prefer explicit file paths and repository names.

## End of Session

1. Update `.ai-session/handoff.md`.
2. Refresh `.ai-session/session-log/YYYY-MM-DD.md`.
3. Capture blockers, unfinished work, and the next recommended step.
4. Avoid storing secrets, raw chat logs, or transient debugging noise.

## Keeping the Handoff Lean

`.ai-session/handoff.md` is a summary layer, not an archive. Detail belongs
in `.ai-session/tasks/`; resolved entries should shrink to a one-line
pointer once their detail lives in a task file. When `handoff.md` grows
past the point where skimming still works, run the `handoff-compact`
workflow instead of letting resolved entries accumulate in place.
