# Workspace Context Rules

- Treat workspace roots as multi-repository environments when applicable.
- Do not initialize workspace roots as Git repositories.
- Do not create, restore, or keep a `.git/` directory at a workspace root.
- Treat directories such as `~/workspace/`, `~/workspace/GitHub/`, and
  `~/workspace/GitLab/` as coordination roots, not versioned repositories.
- Use explicit relative paths when referring to changed files.
- Keep cross-agent session state in the workspace root `.ai-session/` directory.
- Read and update handoff state through that shared directory.
- Keep temporary session data out of repo histories.
