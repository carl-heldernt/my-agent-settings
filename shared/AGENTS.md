# AI Agent Instructions (AGENTS.md)

## 1. General Communication & Language Standards
- **Interactions:** Always respond and communicate with the user in **Traditional Chinese (繁體中文)**.
- **Code Artifacts:** All identifiers (variables, functions, classes), inline comments, block comments, and docstrings must be written exclusively in **English**.
- **Documentation:** All technical documentation and specifications generated in files must remain in **English**.
- **Reasoning:** To ensure codebase maintainability and alignment with international open-source standards.
- **Constraint:** Even though the chat is in Traditional Chinese, all code and file-based documentation must be in English.

---

## 2. Git Commit Message Convention
Strictly follow these rules for every git commit generated:

### 2.1 Structure and Length (The 50/72 Rule)
- **Subject Line:** Max 50 characters. Summarize the change in a single line.
- **Blank Line:** Always include a blank line between the subject and the body.
- **Body Width:** Wrap each line in the body at **72 characters**.

### 2.2 Subject Line Format
- **Format:** `<type>[!](<scope>): <short-description>`
- **Types:**
  - **Group B (Minor):** `feat` (New feature)
  - **Group C (Patch):** `fix`, `perf`, `refactor`, `docs`, `style`, `test`, `chore`
- **Breaking Changes (Group A - Major):** Append a `!` after the type (e.g., `feat!:`) if it requires a major version bump.
- **Grammar:** Use lowercase for type/scope. Use the **imperative mood** (e.g., "add feature").
- **Punctuation:** Do not end the subject line with a period.

### 2.3 Body Content and Formatting
- Explain **what** was changed and **why**.
- Use a bulleted list with hyphens (`-`) for multiple changes.
- **Constraint:** Each bullet point line must not exceed 72 characters.
- **Breaking Changes Footer:** If `!` is used, you **MUST** include a footer starting with `BREAKING CHANGE: ` followed by a migration description at the very end.

### 2.4 Prohibited Content
- **NO AI Signatures:** Do NOT include metadata like "Made-with: Codex" or any AI-generated signatures. Keep it technical and clean.

### 2.5 Multi-line Commit Message Enforcement
- Commit messages MUST be generated as real multi-line text.
- NEVER include escaped newline characters such as `\n`
  or literal backslash sequences in the final commit message.
- The final output passed to `git commit` must contain actual
  line breaks, not escaped string representations.
- If using `git commit -m`, use multiple `-m` arguments instead
  of embedding `\n` inside a single string.
- Example (Correct):
  git commit -m "fix(auth): handle token refresh" \
             -m "- prevent expired token reuse
- improve retry handling"

- Example (Incorrect):
  git commit -m "fix(auth): handle token refresh\n\n- prevent expired token reuse"
- NEVER collapse a structured commit message into a single line.
- Preserve blank lines and bullet formatting exactly as specified.

---

## 3. Git Version Tagging Rule (vA.B.C)
Trigger this workflow whenever asked to "bump the version", "create a new tag", or "release".

### 3.1 Versioning Logic (Semantic Versioning)
Determine the next `vA.B.C` based on the commit history since the last tag:
- **Group A (Major - A.0.0):** Triggered by `!` in type or `BREAKING CHANGE:` footer. Increment **A**, reset **B** and **C** to 0.
- **Group B (Minor - A.B.0):** Triggered by `feat` (non-breaking). Increment **B**, reset **C** to 0.
- **Group C (Patch - A.B.C):** Triggered by `fix`, `perf`, `refactor`, `docs`, `style`, `test`, `chore`. Increment **C**.

### 3.2 Step-by-Step Execution Workflow
1. **Identify Current Version:** Run `git describe --tags --abbrev=0`. (Default to `v0.0.0` if no tags exist).
2. **Analyze Commit History:** Run `git log <latest_tag>..HEAD --oneline` to find the highest priority trigger.
3. **Calculate & Propose:** Determine the new version string. Announce: "Detected [Major/Minor/Patch] changes. Proposed version: vA.B.C".
4. **Execute Tagging:** Upon confirmation, run `git tag vA.B.C` and provide the command: `git push origin vA.B.C`.

### 3.3 Formatting Constraints
- **Tag Format:** Always prefix with a lowercase `v` (e.g., `v1.0.0`).
- **Cleanliness:** No AI signatures or tool-specific metadata in the tag message.
