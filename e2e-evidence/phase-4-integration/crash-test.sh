#!/usr/bin/env bash
# Phase 4 crash tests — feed malformed payloads. Every hook must exit 0 + log to hook-errors.jsonl.
set -uo pipefail
TARGET=/tmp/shannon-test-v6
EVID=/Users/nick/Desktop/shannon-framework-integration/e2e-evidence/phase-4-integration/crash-tests
SHANNON_LOG_DIR=/tmp/shannon-test-v6/.logs-crash
mkdir -p "$EVID" "$SHANNON_LOG_DIR"
export SHANNON_LOG_DIR
rm -f "$SHANNON_LOG_DIR/hook-errors.jsonl"

HOOKS=$(ls "$TARGET/hooks/"*.js "$TARGET/hooks/"*.cjs 2>/dev/null)
for hook in $HOOKS; do
  name=$(basename "$hook")
  outdir="$EVID/$name"
  mkdir -p "$outdir"
  # Send 3 malformed payloads: empty string, invalid JSON, JSON with null tool_input.
  echo "" | node "$hook" >"$outdir/empty.stdout" 2>"$outdir/empty.stderr"; echo $? > "$outdir/empty.exit"
  echo "{not valid json" | node "$hook" >"$outdir/invalid.stdout" 2>"$outdir/invalid.stderr"; echo $? > "$outdir/invalid.exit"
  echo '{"tool_input":null}' | node "$hook" >"$outdir/null-input.stdout" 2>"$outdir/null-input.stderr"; echo $? > "$outdir/null-input.exit"
done

echo ""
echo "=== crash-test summary ==="
echo "hook-errors.jsonl: $(wc -l < "$SHANNON_LOG_DIR/hook-errors.jsonl" 2>/dev/null || echo 0) entries"
echo "non-zero exits:"
for d in "$EVID"/*/; do
  for f in "$d"*.exit; do
    rc=$(cat "$f")
    if [ "$rc" != "0" ]; then
      # Allow exit 2 if hook always emits stderr-warn (e.g., subagent-governance-inject always exits 2)
      echo "  $(basename "$d")/$(basename "$f" .exit) exit=$rc"
    fi
  done
done

# Copy errors log into evidence
cp -f "$SHANNON_LOG_DIR/hook-errors.jsonl" "$EVID/hook-errors.jsonl" 2>/dev/null || touch "$EVID/hook-errors.jsonl"
