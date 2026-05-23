#!/usr/bin/env bash
# Shannon install.sh — orchestrator.
# 1. Run setup.sh (idempotent: declares marketplace).
# 2. Print instructions for user to /plugin install in CC.
# 3. If shannon plugin already installed, run uninstall-others.sh.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SHANNON_ROOT="$(cd "$HERE/.." && pwd)"

echo "=== Shannon install orchestrator ==="

bash "$HERE/setup.sh"

echo ""
echo "Next steps (manual):"
echo "  1. In Claude Code, run: /plugin install shannon@shannon-local"
echo "  2. Then re-run: $HERE/install.sh --resume-after-cc-install"
echo ""

if [ "${1:-}" = "--resume-after-cc-install" ]; then
  if ! find "$HOME/.claude/plugins" -maxdepth 4 -type d -name shannon | grep -q .; then
    echo "REFUSE: Shannon plugin install not detected. Did you run '/plugin install shannon@shannon-local'?" >&2
    exit 1
  fi
  echo "Shannon plugin detected. Running uninstall-others.sh..."
  bash "$HERE/uninstall-others.sh"
  echo ""
  echo "Install complete."
fi
