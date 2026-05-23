#!/usr/bin/env bash
# Headless driver: prove the opt-in gate in REAL claude sessions.
# Loads shannon ONLY via --plugin-dir (no global install). Per fixture, fires a
# trigger prompt and checks shannon's hooks.jsonl for a skill-activation-check fire.
#   enabled fixture (.shannon/active) -> hook fires  -> log row appears
#   unset   fixture (no .shannon)     -> gate no-ops -> NO new log row
#   disabled fixture (.shannon/disabled) -> gate no-ops -> NO new log row
set -uo pipefail
FW="/Users/nick/Desktop/shannon-framework"
LOG="$HOME/.claude/logs/shannon/hooks.jsonl"
OUT="${OUT:-$FW/benchmarks/results/driver-run}"
TO=""; command -v gtimeout >/dev/null && TO="gtimeout 120"
mkdir -p "$(dirname "$OUT")"
: > "$OUT.txt"

run_fixture() {
  local name="$1" dir="$FW/fixtures/$1"
  local before after delta fires rc
  before=$(wc -l < "$LOG" 2>/dev/null || echo 0)
  echo "=== fixture: $name (cwd=$dir) ===" | tee -a "$OUT.txt"
  ( cd "$dir" && CLAUDE_PROJECT_DIR="$dir" $TO claude -p --plugin-dir "$FW" \
      --dangerously-skip-permissions "remember this: gate proof $(date +%s)" >/dev/null 2>&1 )
  rc=$?
  after=$(wc -l < "$LOG" 2>/dev/null || echo 0)
  delta=$((after - before))
  fires=$(tail -n "${delta:-0}" "$LOG" 2>/dev/null | grep -c skill-activation-check || true)
  local sentinel=none
  [ -e "$dir/.shannon/active" ] && sentinel=active
  [ -e "$dir/.shannon/disabled" ] && sentinel=disabled
  echo "  sentinel=$sentinel exit=$rc log-delta=$delta skill-activation-fires=$fires" | tee -a "$OUT.txt"
  echo "RESULT|$name|sentinel=$sentinel|fires=$fires|exit=$rc" >> "$OUT.txt"
}

run_fixture enabled
run_fixture unset
run_fixture disabled
echo "evidence: $OUT.txt"
