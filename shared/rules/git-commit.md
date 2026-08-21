# Git Commit Rules

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
