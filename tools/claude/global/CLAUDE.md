<!-- Generated from my-agent-settings v0.2.0 | 2026-08-21 -->

# Claude Code Instructions

## Git Commit Rules

- Use the 50/72 rule for commit messages.
- Format subjects as `<type>[!](<scope>): <short-description>`.
- Use lowercase types and scopes.
- Use the imperative mood.
- Do not end the subject line with a period.
- Do not include AI signatures or tool-specific metadata.
- Every commit must include a body using `- <label>: <detail>` bullets.
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
