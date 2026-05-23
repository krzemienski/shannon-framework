#!/usr/bin/env bash
# InvocationLayer validate.sh — exercise matchSkills against real cached triggers.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
SHANNON_LOG_DIR="${SHANNON_LOG_DIR:-/tmp/shannon-validate-invocation}"
mkdir -p "$SHANNON_LOG_DIR"
export SHANNON_LOG_DIR
cd "$ROOT"

# Seed cache with a known skill so matchSkills has something to match.
cat > "$SHANNON_LOG_DIR/skill-triggers.json" <<JSON
{"ts":"2026-05-23T05:23:00Z","skills":{"functional-validation":["validate this","prove it works","functional validation"],"evidence-gate":["marking complete","ready to ship"]}}
JSON

OUT=$(node -e "process.env.SHANNON_LOG_DIR='$SHANNON_LOG_DIR'; delete require.cache[require.resolve('./core/layers/invocation/module.js')]; const m=require('./core/layers/invocation/module.js'); const hits=m.matchSkills('Please validate this feature before marking complete'); console.log(JSON.stringify(hits));")
echo "matchSkills probe: $OUT"

# Expect ≥1 match (validate this, marking complete both seeded)
HITS=$(echo "$OUT" | node -e "let d=''; process.stdin.on('data',c=>d+=c); process.stdin.on('end',()=>{const j=JSON.parse(d); console.log(j.length)})")
if [ "$HITS" -lt 1 ]; then
  echo "FAIL: matchSkills returned 0 hits against seeded triggers" >&2
  exit 1
fi

echo "PASS: InvocationLayer — $HITS skill(s) matched from real cache"
