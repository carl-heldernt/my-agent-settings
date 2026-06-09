<!-- Generated from my-agent-settings v0.1.0 | 2026-06-09 -->

# AI Agent Instructions

## Language Rules

# Language Rules

- Communicate with the user in Traditional Chinese.
- Keep code identifiers, inline comments, block comments, and docstrings in English.
- Keep technical documentation and specifications in English.

## Git Commit Rules

# Git Commit Rules

- Use the 50/72 rule for commit messages.
- Format subjects as `<type>[!](<scope>): <short-description>`.
- Use lowercase types and scopes.
- Use the imperative mood.
- Do not end the subject line with a period.
- Do not include AI signatures or tool-specific metadata.
- If a body is present, explain what changed and why.
- Use hyphen bullets for multi-line bodies.
- If `!` is used, include a `BREAKING CHANGE:` footer.

## Security Rules

# Security Rules

- Do not store secrets in git-tracked files.
- Do not store secrets in `.ai-session/`.
- Prefer environment variables first.
- Next check tool-specific config under `~/.config/<tool>/credentials`.
- Then use a repo-level `.env` file that is gitignored.
- Ask the user explicitly if credentials are still missing.
- Include `.env`, `.env.*`, `*.pem`, and `*.key` in template ignores.

## Workspace Context Rules

# Workspace Context Rules

- Treat workspace roots as multi-repository environments when applicable.
- Use explicit relative paths when referring to changed files.
- Keep cross-agent session state in the workspace root `.ai-session/` directory.
- Read and update handoff state through that shared directory.
- Keep temporary session data out of repo histories.
