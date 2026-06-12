#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ROOT_DIR/scripts/build.py"

mkdir -p "$HOME/.codex"
mkdir -p "$HOME/.codex/skills"
ln -sf "$ROOT_DIR/tools/codex/global/AGENTS.md" "$HOME/.codex/AGENTS.md"
for skill_dir in "$ROOT_DIR"/tools/codex/skills/*; do
  [[ -d "$skill_dir" ]] || continue
  ln -sf "$skill_dir" "$HOME/.codex/skills/$(basename "$skill_dir")"
done
