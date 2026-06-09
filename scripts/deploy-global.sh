#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ROOT_DIR/scripts/build.py"

mkdir -p "$HOME/.codex"
ln -sf "$ROOT_DIR/tools/codex/global/AGENTS.md" "$HOME/.codex/AGENTS.md"
