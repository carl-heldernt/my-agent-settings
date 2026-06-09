#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <workspace-root>" >&2
  exit 1
fi

WORKSPACE_ROOT="$1"
SOURCE_DIR="$WORKSPACE_ROOT/.codex"
TARGET_DIR="$WORKSPACE_ROOT/.ai-session"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "No .codex directory found at $SOURCE_DIR" >&2
  exit 0
fi

mkdir -p "$TARGET_DIR" "$TARGET_DIR/tasks" "$TARGET_DIR/session-log"

migrate_file() {
  local source_file="$1"
  local target_file="$2"

  if [[ -f "$source_file" && ! -e "$target_file" ]]; then
    mv "$source_file" "$target_file"
  fi
}

migrate_tree() {
  local source_tree="$1"
  local target_tree="$2"

  if [[ ! -d "$source_tree" ]]; then
    return
  fi

  mkdir -p "$target_tree"
  shopt -s nullglob
  local source_entry
  for source_entry in "$source_tree"/*; do
    local target_entry="$target_tree/$(basename "$source_entry")"
    if [[ -d "$source_entry" ]]; then
      migrate_tree "$source_entry" "$target_entry"
      rmdir "$source_entry" 2>/dev/null || true
    elif [[ -f "$source_entry" && ! -e "$target_entry" ]]; then
      mv "$source_entry" "$target_entry"
    fi
  done
  shopt -u nullglob
}

migrate_root_contents() {
  local source_root="$1"
  local target_root="$2"

  shopt -s nullglob
  local source_entry
  for source_entry in "$source_root"/*; do
    local target_entry="$target_root/$(basename "$source_entry")"
    if [[ -d "$source_entry" ]]; then
      migrate_tree "$source_entry" "$target_entry"
      rmdir "$source_entry" 2>/dev/null || true
    elif [[ -f "$source_entry" && ! -e "$target_entry" ]]; then
      mv "$source_entry" "$target_entry"
    fi
  done
  shopt -u nullglob
}

migrate_file "$SOURCE_DIR/handoff.md" "$TARGET_DIR/handoff.md"
migrate_tree "$SOURCE_DIR/tasks" "$TARGET_DIR/tasks"
migrate_tree "$SOURCE_DIR/session-log" "$TARGET_DIR/session-log"
migrate_root_contents "$SOURCE_DIR" "$TARGET_DIR"

rmdir "$SOURCE_DIR/tasks" 2>/dev/null || true
rmdir "$SOURCE_DIR/session-log" 2>/dev/null || true
rmdir "$SOURCE_DIR" 2>/dev/null || true
