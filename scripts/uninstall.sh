#!/usr/bin/env bash
# Shannon uninstall.sh — reverse self-install.
# - Removes shannon@shannon-local from enabledPlugins (settings.json)
# - Removes extraKnownMarketplaces.shannon-local from settings.json
# - Optionally deletes ~/.claude/logs/shannon/ (prompted unless --purge-logs)
# - Does NOT reinstall the 16 plugins uninstall-others.sh removed.
#   (User reinstalls those manually from their original marketplace sources.)
set -euo pipefail

SETTINGS="${CLAUDE_SETTINGS:-$HOME/.claude/settings.json}"
LOG_DIR="${SHANNON_LOG_DIR:-$HOME/.claude/logs/shannon}"
TS="$(date +%Y%m%d-%H%M%S)"

PURGE_LOGS=0
DRY_RUN=0
for arg in "$@"; do
  case "$arg" in
    --purge-logs) PURGE_LOGS=1 ;;
    --dry-run)    DRY_RUN=1 ;;
    -h|--help)
      cat <<EOF
Usage: $(basename "$0") [--dry-run] [--purge-logs]

  --dry-run       Print what would happen; mutate nothing.
  --purge-logs    Delete ${LOG_DIR}/ without prompting.

Removes Shannon plugin from Claude Code:
  1. Disables shannon@shannon-local in settings.json enabledPlugins
  2. Removes extraKnownMarketplaces.shannon-local from settings.json
  3. Optionally purges ${LOG_DIR}/
EOF
      exit 0
      ;;
  esac
done

if ! command -v jq >/dev/null 2>&1; then
  echo "FAIL: jq required. brew install jq" >&2
  exit 1
fi

if [ ! -f "$SETTINGS" ]; then
  echo "FAIL: settings.json not found at $SETTINGS" >&2
  exit 1
fi

action() {
  if [ "$DRY_RUN" = "1" ]; then
    echo "[dry-run] $*"
  else
    echo "$*"
  fi
}

# Diff plan first.
echo "=== Shannon uninstall plan ==="
EXISTS_ENABLE=$(jq -r '.enabledPlugins["shannon@shannon-local"] // empty' "$SETTINGS")
EXISTS_MARKET=$(jq -r '.extraKnownMarketplaces["shannon-local"] // empty' "$SETTINGS")
[ -n "$EXISTS_ENABLE" ] && echo "  - disable enabledPlugins[\"shannon@shannon-local\"] (current: $EXISTS_ENABLE)" || echo "  - (already absent) enabledPlugins[\"shannon@shannon-local\"]"
[ -n "$EXISTS_MARKET" ] && echo "  - remove extraKnownMarketplaces[\"shannon-local\"]" || echo "  - (already absent) extraKnownMarketplaces[\"shannon-local\"]"
if [ -d "$LOG_DIR" ]; then
  echo "  - log dir present: $LOG_DIR ($(find "$LOG_DIR" -type f 2>/dev/null | wc -l | tr -d ' ') files)"
fi

if [ "$DRY_RUN" = "1" ]; then
  echo ""
  echo "[dry-run] no changes made"
  exit 0
fi

# Confirm.
if [ "${SHANNON_AUTO:-0}" != "1" ]; then
  read -r -p "Proceed? (y/N) " ans
  if [ "$ans" != "y" ] && [ "$ans" != "Y" ]; then
    echo "Aborted."
    exit 1
  fi
fi

# Backup.
cp "$SETTINGS" "${SETTINGS}.pre-shannon-uninstall-${TS}.bak"
action "backup: ${SETTINGS}.pre-shannon-uninstall-${TS}.bak"

# Mutate.
TMP=$(mktemp)
jq 'del(.enabledPlugins["shannon@shannon-local"]) | del(.extraKnownMarketplaces["shannon-local"])' \
  "$SETTINGS" > "$TMP"
if ! jq empty "$TMP" 2>/dev/null; then
  echo "FAIL: produced invalid JSON; aborting" >&2
  rm -f "$TMP"
  exit 1
fi
mv "$TMP" "$SETTINGS"
echo "OK: shannon disabled + shannon-local marketplace removed from $SETTINGS"

# Logs.
if [ -d "$LOG_DIR" ]; then
  if [ "$PURGE_LOGS" = "1" ]; then
    rm -rf "$LOG_DIR"
    echo "OK: purged $LOG_DIR"
  else
    if [ "${SHANNON_AUTO:-0}" != "1" ]; then
      read -r -p "Delete $LOG_DIR? (y/N) " ans
      if [ "$ans" = "y" ] || [ "$ans" = "Y" ]; then
        rm -rf "$LOG_DIR"
        echo "OK: purged $LOG_DIR"
      else
        echo "kept: $LOG_DIR"
      fi
    fi
  fi
fi

echo ""
echo "Shannon uninstalled. Restart Claude Code for changes to take effect."
echo "Note: the 16 plugins disabled by uninstall-others.sh remain disabled."
echo "      Reinstall them manually from their original marketplaces if needed."
