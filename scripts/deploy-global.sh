#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Link $2 -> $1, but skip if $2 already exists and does NOT point into this repo.
safe_link() {
  local src="$1" dst="$2"
  if [[ -e "$dst" || -L "$dst" ]]; then
    local current
    current="$(readlink "$dst" 2>/dev/null || true)"
    if [[ "$current" == "$src" ]]; then
      return 0  # already correct, nothing to do
    fi
    echo "SKIP $dst (already exists and points elsewhere: ${current:-<real file>})" >&2
    return 0
  fi
  ln -sf "$src" "$dst"
}

python3 "$ROOT_DIR/scripts/build.py"

mkdir -p "$HOME/.codex"
mkdir -p "$HOME/.codex/skills"
safe_link "$ROOT_DIR/tools/codex/global/AGENTS.md" "$HOME/.codex/AGENTS.md"
safe_link "$ROOT_DIR/tools/codex/global/hooks.json" "$HOME/.codex/hooks.json"
safe_link "$ROOT_DIR/tools/codex/global/hooks" "$HOME/.codex/hooks"
for skill_dir in "$ROOT_DIR"/tools/codex/skills/*; do
  [[ -d "$skill_dir" ]] || continue
  safe_link "$skill_dir" "$HOME/.codex/skills/$(basename "$skill_dir")"
done

mkdir -p "$HOME/.claude"
mkdir -p "$HOME/.claude/skills"
safe_link "$ROOT_DIR/tools/claude/global/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
for skill_dir in "$ROOT_DIR"/tools/claude/skills/*; do
  [[ -d "$skill_dir" ]] || continue
  safe_link "$skill_dir" "$HOME/.claude/skills/$(basename "$skill_dir")"
done
