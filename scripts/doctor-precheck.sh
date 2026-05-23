#!/usr/bin/env bash
# Shannon doctor-precheck.sh — pre-install + post-install health verification.
# Plain bash. Asserts plugin layout + JSON validity + log writability.
# Exit 0 = PASS, 1 = FAIL with diagnostic table.
set -uo pipefail

# Default target: live installed location. Override via --target <path>.
TARGET="${SHANNON_TARGET:-$HOME/.claude/plugins/shannon-framework}"
VERBOSE=0
for arg in "$@"; do
  case "$arg" in
    --target) shift; TARGET="${1:-$TARGET}"; shift ;;
    --target=*) TARGET="${arg#--target=}" ;;
    -v|--verbose) VERBOSE=1 ;;
    -h|--help)
      cat <<EOF
Usage: $(basename "$0") [--target <path>] [-v]

  --target <path>   Plugin install location to check. Default: ~/.claude/plugins/shannon-framework
  --verbose         Print each check's detail (default: only failures + summary)

Asserts:
  - target dir exists
  - .claude-plugin/plugin.json present + valid JSON
  - hooks/hooks.json present + valid JSON
  - all hook scripts declared in hooks.json exist + executable
  - all command/skill/agent module dirs declared in plugin manifest exist
  - ~/.claude/logs/shannon/ writable
  - ~/.claude/settings.json has extraKnownMarketplaces.shannon-local
EOF
      exit 0
      ;;
  esac
done

PASS=()
FAIL=()

note() { [ "$VERBOSE" = "1" ] && echo "  $*"; }
ok()   { PASS+=("$1"); note "PASS  $1"; }
bad()  { FAIL+=("$1: $2"); echo "FAIL  $1: $2" >&2; }

if ! command -v jq >/dev/null 2>&1; then
  bad "jq" "not installed; brew install jq"
fi

if [ ! -d "$TARGET" ]; then
  bad "target-exists" "$TARGET not found"
else
  ok "target-exists"
fi

PLUGIN_JSON="$TARGET/.claude-plugin/plugin.json"
HOOKS_JSON="$TARGET/hooks/hooks.json"

if [ -f "$PLUGIN_JSON" ]; then
  if jq empty "$PLUGIN_JSON" 2>/dev/null; then
    ok "plugin.json-valid"
    NAME=$(jq -r '.name' "$PLUGIN_JSON")
    VER=$(jq -r '.version' "$PLUGIN_JSON")
    note "plugin name=$NAME version=$VER"
  else
    bad "plugin.json-valid" "$PLUGIN_JSON is not valid JSON"
  fi
else
  bad "plugin.json-exists" "$PLUGIN_JSON missing"
fi

if [ -f "$HOOKS_JSON" ]; then
  if jq empty "$HOOKS_JSON" 2>/dev/null; then
    ok "hooks.json-valid"
  else
    bad "hooks.json-valid" "$HOOKS_JSON not valid JSON"
  fi
else
  bad "hooks.json-exists" "$HOOKS_JSON missing"
fi

# Each hook script declared in hooks.json must exist + be executable.
if [ -f "$HOOKS_JSON" ]; then
  MISSING=0
  NON_EXEC=0
  # Parse script paths from command strings.
  SCRIPTS=$(jq -r '.hooks | to_entries[] | .value[] | .hooks[] | .command' "$HOOKS_JSON" 2>/dev/null \
            | grep -oE 'hooks/[a-zA-Z0-9._-]+\.[a-z]+' | sort -u)
  for s in $SCRIPTS; do
    full="$TARGET/$s"
    if [ ! -f "$full" ]; then
      bad "hook-script-exists" "$s missing at $full"
      MISSING=$((MISSING+1))
    elif [ ! -x "$full" ]; then
      bad "hook-script-executable" "$s not executable"
      NON_EXEC=$((NON_EXEC+1))
    fi
  done
  if [ "$MISSING" = "0" ] && [ "$NON_EXEC" = "0" ]; then
    COUNT=$(echo "$SCRIPTS" | grep -c .)
    ok "hook-scripts-exist (${COUNT})"
  fi
fi

# Module dirs (commands/skills/agents) — verify referenced ones exist.
for sub in modules commands skills agents lib core; do
  if [ -d "$TARGET/$sub" ]; then
    ok "dir-$sub"
  else
    bad "dir-$sub" "$TARGET/$sub missing"
  fi
done

# Log dir writable.
LOG_DIR="${SHANNON_LOG_DIR:-$HOME/.claude/logs/shannon}"
mkdir -p "$LOG_DIR" 2>/dev/null || true
TOUCH="$LOG_DIR/.doctor-touch-$$"
if touch "$TOUCH" 2>/dev/null; then
  rm -f "$TOUCH"
  ok "log-dir-writable"
else
  bad "log-dir-writable" "cannot write to $LOG_DIR"
fi

# Marketplace declared in settings.json.
SETTINGS="$HOME/.claude/settings.json"
if [ -f "$SETTINGS" ]; then
  if jq -e '.extraKnownMarketplaces["shannon-local"]' "$SETTINGS" >/dev/null 2>&1; then
    ok "marketplace-declared"
  else
    bad "marketplace-declared" "extraKnownMarketplaces.shannon-local missing in $SETTINGS"
  fi
fi

echo ""
echo "=== doctor-precheck summary ==="
echo "PASS: ${#PASS[@]}"
echo "FAIL: ${#FAIL[@]}"
if [ "${#FAIL[@]}" -gt 0 ]; then
  echo ""
  echo "Failures:"
  for f in "${FAIL[@]}"; do echo "  - $f"; done
  exit 1
fi

echo "doctor: OK"
exit 0
