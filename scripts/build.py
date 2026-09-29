#!/usr/bin/env python3
"""Build compiled agent configuration outputs from shared rules."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SHARED_DIR = ROOT / "shared"
RULES_DIR = SHARED_DIR / "rules"
WORKFLOWS_DIR = SHARED_DIR / "workflows"
VERSION_FILE = SHARED_DIR / "VERSION"
COPILOT_INSTRUCTIONS_DIR = ROOT / "tools" / "copilot" / "instructions"
CLAUDE_INSTRUCTIONS_DIR = ROOT / "tools" / "claude" / "instructions"
HOOKS_CORE_FILE = SHARED_DIR / "hooks" / "validate_git_commit_core.py"

# Tool label used in the generated hook's docstring, and the deployed path
# each tool's hooks_adapter.py is compiled into.
HOOK_TOOLS = {
    "codex": ("Codex", ROOT / "tools" / "codex" / "global" / "hooks" / "validate_git_commit.py"),
    "claude": ("Claude Code", ROOT / "tools" / "claude" / "global" / "hooks" / "validate_git_commit.py"),
    "antigravity": ("Antigravity", ROOT / "tools" / "antigravity" / "global" / "hooks" / "validate_git_commit.py"),
}


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return path.read_text(encoding="utf-8").strip()


def load_version() -> str:
    return read_text(VERSION_FILE)


def load_markdown_files(paths: list[Path]) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    for path in paths:
        content = read_text(path)
        sections.append((extract_heading(content, path), strip_leading_heading(content)))
    return sections


# Rules that apply to every project on the machine (loaded via ~/.claude/CLAUDE.md and ~/.gemini/antigravity-cli/GEMINI.md).
CLAUDE_GLOBAL_RULES = ["git-commit.md", "language.md", "security.md"]
ANTIGRAVITY_GLOBAL_RULES = ["git-commit.md", "language.md", "security.md"]

# Rules that apply only at a workspace root (loaded via <workspace>/CLAUDE.md and <workspace>/GEMINI.md).
# session-handoff is intentionally excluded: it is covered by the handoff skills.
CLAUDE_WORKSPACE_RULES = ["workspace-context.md"]
ANTIGRAVITY_WORKSPACE_RULES = ["workspace-context.md"]


def load_shared_rules() -> list[tuple[str, str]]:
    paths = sorted(RULES_DIR.glob("*.md"))
    return load_markdown_files(paths)


def load_rules_by_names(names: list[str]) -> list[tuple[str, str]]:
    paths = [RULES_DIR / name for name in names]
    return load_markdown_files(paths)


def load_shared_workflows() -> list[tuple[str, str]]:
    paths = sorted(WORKFLOWS_DIR.glob("*.md"))
    return load_markdown_files(paths)


def load_copilot_instructions() -> list[tuple[str, str]]:
    paths = sorted(COPILOT_INSTRUCTIONS_DIR.glob("*.instructions.md"))
    return load_markdown_files(paths)


def load_claude_instructions() -> list[tuple[str, str]]:
    paths = sorted(CLAUDE_INSTRUCTIONS_DIR.glob("*.instructions.md"))
    return load_markdown_files(paths)


def extract_heading(content: str, path: Path) -> str:
    for line in content.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError(f"Missing top-level heading in {path}")


def strip_leading_heading(content: str) -> str:
    lines = content.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).strip()


def render_section(title: str, body: str) -> str:
    return "\n".join([f"## {title}", "", body, ""])


def render_document(title: str, version: str, sections: list[tuple[str, str]]) -> str:
    header = f"<!-- Generated from my-agent-settings v{version} | {date.today().isoformat()} -->"
    parts = [header, "", f"# {title}", ""]
    for section_title, body in sections:
        parts.append(render_section(section_title, body))
    return "\n".join(parts).rstrip() + "\n"


def render_hook_script(tool: str, version: str) -> str:
    """Concatenate the shared validation core with a tool's I/O adapter."""
    label, output_path = HOOK_TOOLS[tool]
    adapter_path = output_path.parents[1] / "hooks_adapter.py"
    core_text = read_text(HOOKS_CORE_FILE)
    adapter_text = read_text(adapter_path)

    core_body = re.sub(r'^""".*?"""\n', "", core_text, count=1, flags=re.DOTALL).strip("\n")
    core_body = core_body.replace(
        "import re\nimport shlex\nimport subprocess\nfrom collections.abc import Sequence\n",
        "import json\nimport re\nimport shlex\nimport subprocess\nimport sys\nfrom collections.abc import Sequence\n",
        1,
    )

    header = f"# Generated from my-agent-settings v{version} | {date.today().isoformat()} — do not edit directly."
    source_note = f"# Source: shared/hooks/validate_git_commit_core.py + tools/{tool}/global/hooks_adapter.py"
    docstring = f'"""Reject {label} git commits that violate the shared commit-message policy."""'

    parts = [
        "#!/usr/bin/env python3",
        docstring,
        header,
        source_note,
        "",
        core_body,
        "",
        "",
        adapter_text.strip("\n"),
    ]
    return "\n".join(parts) + "\n"


def validate_rendered_document(path: Path, content: str, section_titles: list[str]) -> None:
    if not content.strip():
        raise ValueError(f"Rendered output is empty: {path}")
    if not content.startswith("<!-- Generated from my-agent-settings v"):
        raise ValueError(f"Missing generated header: {path}")
    search_from = 0
    for section_title in section_titles:
        marker = f"\n## {section_title}\n"
        index = content.find(marker, search_from)
        if index == -1:
            raise ValueError(f"Missing section {section_title} in {path}")
        search_from = index + len(marker)


def validate_hook_script(path: Path, content: str) -> None:
    if not content.startswith("#!/usr/bin/env python3\n"):
        raise ValueError(f"Missing shebang: {path}")
    if "# Generated from my-agent-settings v" not in content:
        raise ValueError(f"Missing generated header: {path}")
    for required in ("def validate_body(", "def main(", 'if __name__ == "__main__":'):
        if required not in content:
            raise ValueError(f"Missing {required!r} in {path}")
    compile(content, str(path), "exec")


def build(validate_only: bool) -> int:
    version = load_version()
    shared_rules = load_shared_rules()
    shared_workflows = load_shared_workflows()
    copilot_instructions = load_copilot_instructions()
    claude_instructions = load_claude_instructions()
    claude_global_rules = load_rules_by_names(CLAUDE_GLOBAL_RULES)
    claude_workspace_rules = load_rules_by_names(CLAUDE_WORKSPACE_RULES)
    antigravity_global_rules = load_rules_by_names(ANTIGRAVITY_GLOBAL_RULES)
    antigravity_workspace_rules = load_rules_by_names(ANTIGRAVITY_WORKSPACE_RULES)

    # Codex and Copilot include all shared rules + workflows (no skills equivalent).
    codex_sections = shared_rules + shared_workflows
    copilot_sections = shared_rules + shared_workflows + copilot_instructions
    # Claude global: personal rules only; session-handoff covered by skills.
    claude_global_sections = claude_global_rules + claude_instructions
    # Claude workspace: workspace-scoped rules only; loaded when CWD is a workspace root.
    claude_workspace_sections = claude_workspace_rules
    # Antigravity global: personal rules only; session-handoff covered by skills.
    antigravity_global_sections = antigravity_global_rules
    # Antigravity workspace: workspace-scoped rules only; loaded when CWD is a workspace root.
    antigravity_workspace_sections = antigravity_workspace_rules

    hook_scripts = {output_path: render_hook_script(tool, version) for tool, (_, output_path) in HOOK_TOOLS.items()}

    rendered = {
        ROOT / "tools" / "codex" / "global" / "AGENTS.md": render_document(
            "AI Agent Instructions",
            version,
            codex_sections,
        ),
        ROOT / "tools" / "copilot" / "global" / "copilot-instructions.md": render_document(
            "Copilot Instructions",
            version,
            copilot_sections,
        ),
        ROOT / "tools" / "claude" / "global" / "CLAUDE.md": render_document(
            "Claude Code Instructions",
            version,
            claude_global_sections,
        ),
        ROOT / "tools" / "claude" / "workspace" / "CLAUDE.md": render_document(
            "Claude Code Workspace Instructions",
            version,
            claude_workspace_sections,
        ),
        ROOT / "tools" / "antigravity" / "global" / "GEMINI.md": render_document(
            "Antigravity Instructions",
            version,
            antigravity_global_sections,
        ),
        ROOT / "tools" / "antigravity" / "workspace" / "GEMINI.md": render_document(
            "Antigravity Workspace Instructions",
            version,
            antigravity_workspace_sections,
        ),
    }

    if validate_only:
        validate_rendered_document(
            ROOT / "tools" / "codex" / "global" / "AGENTS.md",
            rendered[ROOT / "tools" / "codex" / "global" / "AGENTS.md"],
            [title for title, _ in codex_sections],
        )
        validate_rendered_document(
            ROOT / "tools" / "copilot" / "global" / "copilot-instructions.md",
            rendered[ROOT / "tools" / "copilot" / "global" / "copilot-instructions.md"],
            [title for title, _ in copilot_sections],
        )
        validate_rendered_document(
            ROOT / "tools" / "claude" / "global" / "CLAUDE.md",
            rendered[ROOT / "tools" / "claude" / "global" / "CLAUDE.md"],
            [title for title, _ in claude_global_sections],
        )
        validate_rendered_document(
            ROOT / "tools" / "claude" / "workspace" / "CLAUDE.md",
            rendered[ROOT / "tools" / "claude" / "workspace" / "CLAUDE.md"],
            [title for title, _ in claude_workspace_sections],
        )
        validate_rendered_document(
            ROOT / "tools" / "antigravity" / "global" / "GEMINI.md",
            rendered[ROOT / "tools" / "antigravity" / "global" / "GEMINI.md"],
            [title for title, _ in antigravity_global_sections],
        )
        validate_rendered_document(
            ROOT / "tools" / "antigravity" / "workspace" / "GEMINI.md",
            rendered[ROOT / "tools" / "antigravity" / "workspace" / "GEMINI.md"],
            [title for title, _ in antigravity_workspace_sections],
        )
        for tool, (_, output_path) in HOOK_TOOLS.items():
            validate_hook_script(output_path, hook_scripts[output_path])
        return 0

    for path, content in rendered.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    for path, content in hook_scripts.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true", help="Validate inputs without writing outputs")
    args = parser.parse_args(argv)
    return build(args.validate)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
