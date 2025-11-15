#!/bin/bash
# Shannon Framework V4 - SessionStart Hook
# Loads using-shannon meta-skill to establish Shannon workflows

PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "<EXTREMELY_IMPORTANT>"
echo "You are using Shannon Framework V4."
echo ""
echo "**The content below is from skills/using-shannon/SKILL.md:**"
echo ""
cat "/Users/nick/.claude/skills/using-shannon/SKILL.md"
echo ""
echo "</EXTREMELY_IMPORTANT>"
