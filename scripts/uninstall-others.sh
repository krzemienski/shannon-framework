#!/usr/bin/env bash
# Shannon uninstall-others.sh — atomic uninstall of 16 consolidated plugins.
# Per SHANNON-V6-INVENTORY.md §1.
# - Requires Shannon plugin to be installed first (precondition).
# - Backs up installed_plugins.json + settings.json before write.
# - Disables each plugin in settings.json (enabledPlugins → false).
# - Optionally removes plugin install dirs from ~/.claude/plugins/.
# - NO --parallel mode (atomic only — user is sole user).
set -euo pipefail

SETTINGS="${CLAUDE_SETTINGS:-$HOME/.claude/settings.json}"
INSTALLED="${CLAUDE_INSTALLED:-$HOME/.claude/plugins/installed_plugins.json}"
TS="$(date +%Y%m%d-%H%M%S)"

PLUGINS_TO_REMOVE=(
  "kaizen@context-engineering-kit"
  "sadd@context-engineering-kit"
  "sdd@context-engineering-kit"
  "reflexion@context-engineering-kit"
  "deepest-plan@deepest-plan-dev"
  "start@the-startup"
  "autoresearch@autoresearch"
  "anneal-cast@anneal-umbrella-dev"
  "anneal-alloy@anneal-umbrella-dev"
  "anneal-temper@anneal-umbrella-dev"
  "planning-with-files@planning-with-files"
  "prd-generator"
  "claude-hud@claude-hud"
  "validationforge@validationforge"
  "crucible@crucible-local"
  "oh-my-claudecode@omc"
)

if ! command -v jq >/dev/null 2>&1; then
  echo "FAIL: jq is required. brew install jq" >&2
  exit 1
fi

# Precondition: Shannon plugin must be installed.
if ! jq -e '.enabledPlugins["shannon@shannon-local"]' "$SETTINGS" >/dev/null 2>&1 && \
   ! find "$HOME/.claude/plugins" -maxdepth 4 -type d -name shannon 2>/dev/null | grep -q .; then
  echo "REFUSE: Shannon plugin not installed yet. Run scripts/setup.sh then '/plugin install shannon@shannon-local' first." >&2
  echo "       This script refuses to uninstall replacements while Shannon is absent." >&2
  exit 1
fi

# Print plan.
echo "About to disable ${#PLUGINS_TO_REMOVE[@]} plugins:"
for p in "${PLUGINS_TO_REMOVE[@]}"; do echo "  - $p"; done
echo ""

# Confirm (skip when SHANNON_AUTO=1 — used by /shannon:install)
if [ "${SHANNON_AUTO:-0}" != "1" ]; then
  read -r -p "Proceed? (y/N) " ans
  if [ "$ans" != "y" ] && [ "$ans" != "Y" ]; then
    echo "Aborted." >&2
    exit 1
  fi
fi

# Backup.
cp "$SETTINGS" "${SETTINGS}.pre-uninstall-${TS}.bak"
echo "backup: ${SETTINGS}.pre-uninstall-${TS}.bak"
if [ -f "$INSTALLED" ]; then
  cp "$INSTALLED" "${INSTALLED}.pre-uninstall-${TS}.bak"
  echo "backup: ${INSTALLED}.pre-uninstall-${TS}.bak"
fi

# Snapshot enabled state for rollback.
SNAP_DIR="$HOME/.claude/.shannon"
mkdir -p "$SNAP_DIR"
SNAP="$SNAP_DIR/uninstall-rollback-${TS}.json"
jq --argjson keys "$(printf '%s\n' "${PLUGINS_TO_REMOVE[@]}" | jq -R . | jq -s .)" \
   '{enabledPlugins: (.enabledPlugins // {}), targetKeys: $keys}' \
   "$SETTINGS" > "$SNAP"
echo "rollback snapshot: $SNAP"

# Disable each in settings.json.
TMP=$(mktemp)
jq --argjson keys "$(printf '%s\n' "${PLUGINS_TO_REMOVE[@]}" | jq -R . | jq -s .)" \
   '.enabledPlugins = (.enabledPlugins // {}) | reduce $keys[] as $k (.; .enabledPlugins[$k] = false)' \
   "$SETTINGS" > "$TMP"

if ! jq empty "$TMP" 2>/dev/null; then
  echo "FAIL: produced invalid JSON; aborting" >&2
  rm -f "$TMP"
  exit 1
fi
mv "$TMP" "$SETTINGS"
echo "OK: disabled ${#PLUGINS_TO_REMOVE[@]} plugins in settings.json"

echo ""
echo "Restart Claude Code for changes to take effect."
echo "Rollback: scripts/rollback.sh $SNAP"
