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
VERSION_FILE = SHARED_DIR / "VERSION"

RULE_ORDER = [
    ("language.md", "Language Rules"),
    ("git-commit.md", "Git Commit Rules"),
    ("security.md", "Security Rules"),
    ("workspace-context.md", "Workspace Context Rules"),
]

OUTPUTS = {
    ROOT / "tools" / "codex" / "global" / "AGENTS.md": "# AI Agent Instructions",
    ROOT / "tools" / "copilot" / "global" / "copilot-instructions.md": "# Copilot Instructions",
}


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return path.read_text(encoding="utf-8").strip()


def load_version() -> str:
    return read_text(VERSION_FILE)


def load_rules() -> list[tuple[str, str]]:
    rules: list[tuple[str, str]] = []
    for filename, title in RULE_ORDER:
        content = read_text(RULES_DIR / filename)
        rules.append((title, content))
    return rules


def render_document(title: str, version: str, rules: list[tuple[str, str]]) -> str:
    header = f"<!-- Generated from my-agent-settings v{version} | {date.today().isoformat()} -->"
    parts = [header, "", title, ""]
    for section_title, content in rules:
        parts.extend([f"## {section_title}", "", content, ""])
    return "\n".join(parts).rstrip() + "\n"


def build(validate_only: bool) -> int:
    version = load_version()
    rules = load_rules()
    rendered = {path: render_document(title, version, rules) for path, title in OUTPUTS.items()}

    if validate_only:
        for path, content in rendered.items():
            if not content.strip():
                raise ValueError(f"Rendered output is empty: {path}")
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
