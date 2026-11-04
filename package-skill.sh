#!/usr/bin/env sh
# Builds dist/hipaa-compliance-masterscan.skill, a zip of the skill folder for
# uploading to claude.ai (Settings > Capabilities > Skills) or Claude Desktop.
set -eu
cd "$(dirname "$0")"
SKILL=hipaa-compliance-masterscan
mkdir -p dist
rm -f "dist/$SKILL.skill"
( cd skills && zip -qr "../dist/$SKILL.skill" "$SKILL" -x '*/__pycache__/*' '*.pyc' '*.DS_Store' )
echo "Built dist/$SKILL.skill"
unzip -l "dist/$SKILL.skill" | tail -1
