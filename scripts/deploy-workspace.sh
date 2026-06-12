#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <workspace-root>" >&2
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKSPACE_ROOT="$1"
TEMPLATE_DIR="$ROOT_DIR/templates/workspace/.ai-session"

python3 "$ROOT_DIR/scripts/build.py"

mkdir -p "$WORKSPACE_ROOT/.ai-session"
mkdir -p "$WORKSPACE_ROOT/.ai-session/tasks"
mkdir -p "$WORKSPACE_ROOT/.ai-session/session-log"
if [[ -f "$TEMPLATE_DIR/handoff.md" && ! -e "$WORKSPACE_ROOT/.ai-session/handoff.md" ]]; then
  cp "$TEMPLATE_DIR/handoff.md" "$WORKSPACE_ROOT/.ai-session/handoff.md"
fi
if [[ -d "$TEMPLATE_DIR/tasks" ]]; then
  for template_file in "$TEMPLATE_DIR"/tasks/*; do
    [[ -e "$template_file" ]] || continue
    target_file="$WORKSPACE_ROOT/.ai-session/tasks/$(basename "$template_file")"
    if [[ ! -e "$target_file" ]]; then
      cp "$template_file" "$target_file"
    fi
  done
fi
ln -sf "$ROOT_DIR/tools/copilot" "$WORKSPACE_ROOT/.github"
