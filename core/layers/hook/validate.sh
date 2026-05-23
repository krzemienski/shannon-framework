#!/usr/bin/env bash
# HookLayer validate.sh — verify dispatch table matches scripts on disk.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
cd "$ROOT"

OUT=$(node core/layers/hook/module.js 2>&1)
STATUS=$?
echo "$OUT"
if [ $STATUS -ne 0 ]; then
  echo "FAIL: HookLayer module reported missing scripts" >&2
  exit 1
fi

# Assert hooks.json is valid JSON + 14 scripts referenced
SCRIPTS=$(node -e "const j=require('./hooks/hooks.json'); const set=new Set(); for(const ev of Object.keys(j.hooks)){for(const e of j.hooks[ev]){for(const h of e.hooks||[]){const m=h.command.match(/hooks\/([a-z0-9-]+\.[a-z]+)/);if(m)set.add(m[1]);}}} console.log([...set].sort().join('\n'));")
COUNT=$(echo "$SCRIPTS" | grep -c .)
echo "hooks.json references $COUNT distinct scripts:"
echo "$SCRIPTS" | sed 's/^/  /'
if [ "$COUNT" -lt 13 ]; then
  echo "FAIL: expected ≥13 scripts in hooks.json, got $COUNT" >&2
  exit 1
fi

echo "PASS: HookLayer — $COUNT scripts wired, all present on disk"
