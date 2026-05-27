#!/usr/bin/env bash
# Scaffold a new plugin under plugins/<name>/ and register it in marketplace.json.
# Usage: scripts/new-plugin.sh <plugin-name> "<one-line description>"
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <plugin-name> \"<one-line description>\"" >&2
  exit 2
fi

NAME="$1"
DESC="$2"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN_DIR="$ROOT/plugins/$NAME"

if [[ -e "$PLUGIN_DIR" ]]; then
  echo "error: $PLUGIN_DIR already exists" >&2
  exit 1
fi

mkdir -p "$PLUGIN_DIR/.claude-plugin" "$PLUGIN_DIR/skills" "$PLUGIN_DIR/agents"

cat > "$PLUGIN_DIR/.claude-plugin/plugin.json" <<JSON
{
  "name": "$NAME",
  "description": "$DESC",
  "version": "0.1.0",
  "author": {
    "name": "$(git config user.name 2>/dev/null || echo "anonymous")"
  }
}
JSON

cat > "$PLUGIN_DIR/README.md" <<MD
# $NAME

$DESC

## Install

\`\`\`text
/plugin marketplace add toyofukux/autonomous-dev-tools
/plugin install $NAME@autonomous-dev-tools
\`\`\`

## Develop

\`\`\`bash
claude --plugin-dir ./plugins/$NAME
\`\`\`
MD

echo "Created $PLUGIN_DIR"
echo "Next:"
echo "  1. Edit $PLUGIN_DIR/.claude-plugin/plugin.json"
echo "  2. Add skills under $PLUGIN_DIR/skills/<skill>/SKILL.md"
echo "  3. Add agents under $PLUGIN_DIR/agents/<agent>.md"
echo "  4. Add an entry to $ROOT/.claude-plugin/marketplace.json"
