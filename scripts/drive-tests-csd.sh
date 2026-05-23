#!/usr/bin/env bash
# csd-driven proof: launch a headless worker per fixture, converse with a
# trigger prompt, capture the full event stream + final assistant turn.
# Produces per-fixture evidence dirs with events.jsonl + turn.md + meta.txt.
set -uo pipefail
FW="/Users/nick/Desktop/shannon-framework"
CSD="/Users/nick/.claude/plugins/cache/superpowers-marketplace/claude-session-driver/3.0.0/skills/driving-claude-code-sessions/scripts/csd"
EV_ROOT="${EV_ROOT:-$FW/benchmarks/results/csd-run-$(date +%s)}"
SHANNON_LOG="$HOME/.claude/logs/shannon/hooks.jsonl"
PROMPT="remember this: csd proof at $(date +%H%M%S)"
mkdir -p "$EV_ROOT"

run_fixture() {
  local name="$1"
  local fdir="$FW/fixtures/$name"
  local edir="$EV_ROOT/$name"
  local tag="shannon-$name-$RANDOM"
  mkdir -p "$edir"

  local sentinel=none
  [ -e "$fdir/.shannon/active" ]   && sentinel=active
  [ -e "$fdir/.shannon/disabled" ] && sentinel=disabled

  echo "=== $name (sentinel=$sentinel, tag=$tag) ===" | tee -a "$EV_ROOT/SUMMARY.txt"

  local before; before=$(wc -l < "$SHANNON_LOG" 2>/dev/null || echo 0)

  # Launch worker with shannon loaded ONLY via --plugin-dir
  local shim
  shim=$("$CSD" launch "$tag" "$fdir" -- --plugin-dir "$FW" 2>"$edir/launch.stderr")
  if [ -z "$shim" ] || [ ! -x "$shim" ]; then
    echo "  LAUNCH FAILED — see $edir/launch.stderr" | tee -a "$EV_ROOT/SUMMARY.txt"
    return 1
  fi
  echo "  shim=$shim" | tee -a "$EV_ROOT/SUMMARY.txt"

  # Converse: send trigger prompt, wait for completion
  "$shim" converse --with-turn "$PROMPT" 180 > "$edir/turn.md" 2>"$edir/converse.stderr"
  local cvexit=$?

  # Pull full event stream
  "$shim" read-events > "$edir/events.jsonl" 2>/dev/null

  local after; after=$(wc -l < "$SHANNON_LOG" 2>/dev/null || echo 0)
  local delta=$((after - before))
  # Tail the shannon log delta into a fixture-local copy
  if [ "$delta" -gt 0 ]; then
    tail -n "$delta" "$SHANNON_LOG" > "$edir/shannon-hooks-delta.jsonl"
  else
    : > "$edir/shannon-hooks-delta.jsonl"
  fi

  # Per-event-type counts
  local n_total n_prompt n_pre n_stop
  n_total=$(wc -l < "$edir/events.jsonl" | tr -d ' ')
  n_prompt=$(grep -c '"user_prompt_submit"' "$edir/events.jsonl" 2>/dev/null || echo 0)
  n_pre=$(grep -c '"pre_tool_use"' "$edir/events.jsonl" 2>/dev/null || echo 0)
  n_stop=$(grep -c '"stop"' "$edir/events.jsonl" 2>/dev/null || echo 0)

  local n_fires
  n_fires=$(grep -c '"script":"skill-activation-check"' "$edir/shannon-hooks-delta.jsonl" 2>/dev/null || echo 0)

  {
    echo "fixture=$name"
    echo "sentinel=$sentinel"
    echo "converse_exit=$cvexit"
    echo "events_total=$n_total"
    echo "events_user_prompt=$n_prompt"
    echo "events_pre_tool=$n_pre"
    echo "events_stop=$n_stop"
    echo "shannon_skill_activation_fires=$n_fires"
    echo "shannon_log_delta=$delta"
    echo "prompt=$PROMPT"
  } | tee "$edir/meta.txt" | sed 's/^/  /' | tee -a "$EV_ROOT/SUMMARY.txt"

  # Show first lines of turn so we can eyeball whether shannon hint got rendered
  echo "  --- turn.md head ---" | tee -a "$EV_ROOT/SUMMARY.txt"
  head -5 "$edir/turn.md" 2>/dev/null | sed 's/^/    /' | tee -a "$EV_ROOT/SUMMARY.txt"

  "$shim" stop >/dev/null 2>&1 || true
  echo "" | tee -a "$EV_ROOT/SUMMARY.txt"
}

run_fixture enabled
run_fixture unset
run_fixture disabled

echo "===========================" | tee -a "$EV_ROOT/SUMMARY.txt"
echo "evidence root: $EV_ROOT"     | tee -a "$EV_ROOT/SUMMARY.txt"
echo "SUMMARY        : $EV_ROOT/SUMMARY.txt"
echo "per-fixture    : $EV_ROOT/{enabled,unset,disabled}/{events.jsonl,turn.md,meta.txt,shannon-hooks-delta.jsonl}"
