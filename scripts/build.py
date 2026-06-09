#!/usr/bin/env python3
"""Build compiled agent configuration outputs from shared rules."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SHARED_DIR = ROOT / "shared"
RULES_DIR = SHARED_DIR / "rules"
WORKFLOWS_DIR = SHARED_DIR / "workflows"
VERSION_FILE = SHARED_DIR / "VERSION"
COPILOT_INSTRUCTIONS_DIR = ROOT / "tools" / "copilot" / "instructions"


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


def load_shared_rules() -> list[tuple[str, str]]:
    paths = sorted(RULES_DIR.glob("*.md"))
    return load_markdown_files(paths)


def load_shared_workflows() -> list[tuple[str, str]]:
    paths = sorted(WORKFLOWS_DIR.glob("*.md"))
    return load_markdown_files(paths)


def load_copilot_instructions() -> list[tuple[str, str]]:
    paths = sorted(COPILOT_INSTRUCTIONS_DIR.glob("*.instructions.md"))
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


def build(validate_only: bool) -> int:
    version = load_version()
    shared_rules = load_shared_rules()
    shared_workflows = load_shared_workflows()
    copilot_instructions = load_copilot_instructions()

    codex_sections = shared_rules + shared_workflows
    copilot_sections = shared_rules + shared_workflows + copilot_instructions
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
        return 0

    for path, content in rendered.items():
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
