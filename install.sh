#!/usr/bin/env sh
# Installs the hipaa-compliance-masterscan skill into a Claude Code skills directory.
#
#   sh install.sh            -> ~/.claude/skills/hipaa-compliance-masterscan   (user scope)
#   sh install.sh --project  -> ./.claude/skills/hipaa-compliance-masterscan   (current repo)
#
# Or without cloning:
#   curl -fsSL https://raw.githubusercontent.com/mikenguyendev/hipaa-compliance-masterscan/main/install.sh | sh
set -eu

SKILL=hipaa-compliance-masterscan
REPO=https://github.com/mikenguyendev/hipaa-compliance-masterscan

if [ "${1:-}" = "--project" ]; then
  DEST="$(pwd)/.claude/skills/$SKILL"
else
  DEST="$HOME/.claude/skills/$SKILL"
fi

SRC_DIR="$(cd "$(dirname "$0")" 2>/dev/null && pwd || true)"
if [ -n "$SRC_DIR" ] && [ -f "$SRC_DIR/skills/$SKILL/SKILL.md" ]; then
  SRC="$SRC_DIR/skills/$SKILL"
else
  TMP="$(mktemp -d)"
  trap 'rm -rf "$TMP"' EXIT
  git clone --depth 1 --quiet "$REPO" "$TMP/repo"
  SRC="$TMP/repo/skills/$SKILL"
fi

if [ -e "$DEST" ]; then
  echo "Updating existing install at $DEST"
  rm -rf "$DEST"
fi
mkdir -p "$(dirname "$DEST")"
cp -R "$SRC" "$DEST"
echo "Installed $SKILL to $DEST"
echo "Restart Claude Code, then ask: \"Run a HIPAA Compliance MasterScan on this repo\""
