#!/usr/bin/env bash
# Shannon setup.sh — idempotent marketplace declaration writer.
# Adds extraKnownMarketplaces.shannon-local to ~/.claude/settings.json pointing
# at /Users/nick/Desktop/shannon-framework. Backs up settings.json first.
# Idempotent on re-run.
set -euo pipefail

SHANNON_ROOT="${SHANNON_ROOT:-/Users/nick/Desktop/shannon-framework}"
SETTINGS="${CLAUDE_SETTINGS:-$HOME/.claude/settings.json}"
TS="$(date +%Y%m%d-%H%M%S)"
BACKUP="${SETTINGS}.pre-shannon-${TS}.bak"

if ! command -v jq >/dev/null 2>&1; then
  echo "FAIL: jq is required. Install with: brew install jq" >&2
  exit 1
fi

if [ ! -f "$SETTINGS" ]; then
  echo "FAIL: settings.json not found at $SETTINGS" >&2
  exit 1
fi

if [ ! -d "$SHANNON_ROOT/.claude-plugin" ]; then
  echo "FAIL: shannon-framework not found at $SHANNON_ROOT (missing .claude-plugin/)" >&2
  exit 1
fi

# Idempotent: check if already declared.
EXISTS=$(jq -r '.extraKnownMarketplaces["shannon-local"] // empty' "$SETTINGS" 2>/dev/null || echo "")
if [ -n "$EXISTS" ]; then
  echo "OK: shannon-local marketplace already declared in $SETTINGS"
  echo "    current source: $(jq -r '.extraKnownMarketplaces["shannon-local"].source.path // "n/a"' "$SETTINGS")"
  exit 0
fi

# Back up.
cp "$SETTINGS" "$BACKUP"
echo "backup: $BACKUP"

# Write declaration via jq (safe — no manual JSON editing).
TMP=$(mktemp)
jq --arg p "$SHANNON_ROOT" \
   '.extraKnownMarketplaces = ((.extraKnownMarketplaces // {}) + {"shannon-local": {"source": {"path": $p, "source": "directory"}}})' \
   "$SETTINGS" > "$TMP"

# Validate written JSON
if ! jq empty "$TMP" 2>/dev/null; then
  echo "FAIL: jq produced invalid JSON; aborting (backup preserved at $BACKUP)" >&2
  rm -f "$TMP"
  exit 1
fi

mv "$TMP" "$SETTINGS"
echo "OK: declared shannon-local marketplace → $SHANNON_ROOT"
echo "Next: /plugin install shannon@shannon-local  (run inside Claude Code)"
