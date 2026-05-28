#!/usr/bin/env bash
# Rename the ad-* skill prefix across a plugin.
# Usage: scripts/rename-prefix.sh <plugin-name> <old-prefix> <new-prefix>
# Example: scripts/rename-prefix.sh software-factory ad zz
#   → ad-spec/ → zz-spec/, references in SKILL.md and READMEs updated.
set -euo pipefail

if [[ $# -ne 3 ]]; then
  echo "usage: $0 <plugin-name> <old-prefix> <new-prefix>" >&2
  exit 2
fi

PLUGIN="$1"
OLD="$2"
NEW="$3"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN_DIR="$ROOT/plugins/$PLUGIN"

if [[ ! -d "$PLUGIN_DIR" ]]; then
  echo "error: $PLUGIN_DIR not found" >&2
  exit 1
fi

if [[ "$OLD" == "$NEW" ]]; then
  echo "error: old and new prefix are the same" >&2
  exit 1
fi

echo "Renaming $OLD-* → $NEW-* in $PLUGIN_DIR"

# Rename skill directories
find "$PLUGIN_DIR/skills" -maxdepth 1 -type d -name "${OLD}-*" | while read -r dir; do
  base="$(basename "$dir")"
  newname="${NEW}-${base#${OLD}-}"
  echo "  dir: $base → $newname"
  git -C "$ROOT" mv "$dir" "$(dirname "$dir")/$newname" 2>/dev/null || mv "$dir" "$(dirname "$dir")/$newname"
done

# Update references inside files (SKILL.md, agents/*.md, README.md, docs/)
SED_INPLACE=(-i)
case "$(uname -s)" in
  Darwin*) SED_INPLACE=(-i "");;
esac

find "$PLUGIN_DIR" "$ROOT/docs" "$ROOT/README.md" -type f \( -name "*.md" -o -name "*.json" \) 2>/dev/null | while read -r f; do
  if grep -q "${OLD}-" "$f" 2>/dev/null; then
    sed "${SED_INPLACE[@]}" "s/\\b${OLD}-/${NEW}-/g" "$f"
    echo "  updated: $f"
  fi
done

echo
echo "Done. Review with: git diff"
echo "Don't forget to bump the plugin version if this is a release."
