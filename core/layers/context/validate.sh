#!/usr/bin/env bash
# ContextLayer validate.sh — exercise buildContext + cacheTriggers + run against real fs.
# Iron rule: real execution, no fakes, no test files.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
SHANNON_LOG_DIR="${SHANNON_LOG_DIR:-/tmp/shannon-validate-context}"
mkdir -p "$SHANNON_LOG_DIR"
export SHANNON_LOG_DIR

cd "$ROOT"

OUT=$(node -e "const m=require('./core/layers/context/module.js'); const ctx=m.buildContext(); const p=m.cacheTriggers(); console.log(JSON.stringify({contextBytes: ctx.length, triggersCache: p, hasContent: ctx.length>0}));")
echo "ContextLayer probe: $OUT"

# Assert context was built (length > 0 — real CLAUDE.md exists on this machine)
LEN=$(echo "$OUT" | node -e "let d=''; process.stdin.on('data',c=>d+=c); process.stdin.on('end',()=>{console.log(JSON.parse(d).contextBytes)})")
if [ "$LEN" -lt 100 ]; then
  echo "FAIL: context too small ($LEN bytes — expected real CLAUDE.md)" >&2
  exit 1
fi

# Assert skill-triggers.json written
if [ ! -f "$SHANNON_LOG_DIR/skill-triggers.json" ]; then
  echo "FAIL: skill-triggers.json not written to $SHANNON_LOG_DIR" >&2
  exit 1
fi

echo "PASS: ContextLayer — $LEN bytes context, triggers cache at $SHANNON_LOG_DIR/skill-triggers.json"
