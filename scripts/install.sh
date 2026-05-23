#!/usr/bin/env bash
# Shannon install.sh — atomic orchestrator.
#
# Sequence:
#   1. Run setup.sh (declare marketplace; idempotent)
#   2. Print instructions for user's interactive `/plugin install` step
#   3. On --resume-after-cc-install: verify install, run doctor-precheck,
#      optionally trigger uninstall-others.sh.
#
# Modes:
#   (default)              — phase 1 setup + instruction print
#   --resume-after-cc-install  — phase 2 verify + precheck + uninstall-others prompt
#   --dry-run              — print all planned actions; mutate nothing
#   --auto                 — non-interactive (SHANNON_AUTO=1 → skips prompts)
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
SHANNON_ROOT="$(cd "$HERE/.." && pwd)"

DRY_RUN=0
AUTO=0
RESUME=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --auto)    AUTO=1 ;;
    --resume-after-cc-install) RESUME=1 ;;
    -h|--help)
      cat <<EOF
Usage: $(basename "$0") [--dry-run] [--auto] [--resume-after-cc-install]

  --dry-run                    Print actions; no file mutations.
  --auto                       Non-interactive (skip prompts; uninstall-others will run).
  --resume-after-cc-install    Phase 2 — verify CC install + precheck + uninstall-others.

Phase 1 (default): declares marketplace, prints user instruction for /plugin install.
Phase 2 (--resume-after-cc-install): verifies install, runs doctor-precheck,
  optionally invokes uninstall-others.sh to disable the 16 superseded plugins.
EOF
      exit 0
      ;;
  esac
done

echo "=== Shannon install orchestrator ==="
echo "  shannon root: $SHANNON_ROOT"
echo "  dry-run:      $DRY_RUN"
echo "  auto:         $AUTO"
echo "  phase:        $([ "$RESUME" = "1" ] && echo "2 (resume)" || echo "1 (setup)")"

if [ "$RESUME" = "0" ]; then
  # Phase 1: marketplace setup
  if [ "$DRY_RUN" = "1" ]; then
    echo "[dry-run] bash $HERE/setup.sh"
  else
    bash "$HERE/setup.sh"
  fi
  echo ""
  echo "Next steps (manual):"
  echo "  1. In Claude Code, run: /plugin install shannon@shannon-local"
  echo "  2. Then re-run: $HERE/install.sh --resume-after-cc-install"
  echo ""
  exit 0
fi

# Phase 2: verify install + precheck + optional uninstall-others
INSTALL_DIR=""
for cand in \
  "$HOME/.claude/plugins/shannon-framework" \
  "$HOME/.claude/plugins/shannon" \
  "$HOME/.claude/plugins/shannon-local"; do
  if [ -d "$cand" ]; then INSTALL_DIR="$cand"; break; fi
done

if [ -z "$INSTALL_DIR" ]; then
  if [ "$DRY_RUN" = "1" ]; then
    echo "[dry-run] would REFUSE: shannon plugin install not detected"
    INSTALL_DIR="$HOME/.claude/plugins/shannon-framework"
  else
    echo "REFUSE: Shannon plugin install not detected. Did you run '/plugin install shannon@shannon-local'?" >&2
    exit 1
  fi
fi
echo "shannon plugin detected at: $INSTALL_DIR"

# Doctor precheck.
echo ""
echo "=== doctor-precheck ==="
if [ "$DRY_RUN" = "1" ]; then
  echo "[dry-run] would run: bash $HERE/doctor-precheck.sh --target $INSTALL_DIR"
else
  if ! bash "$HERE/doctor-precheck.sh" --target "$INSTALL_DIR"; then
    echo "REFUSE: doctor-precheck FAIL — fix issues above before continuing." >&2
    exit 1
  fi
fi

# Prompt for uninstall-others.
echo ""
if [ "$AUTO" = "1" ] || [ "${SHANNON_AUTO:-0}" = "1" ]; then
  PROCEED="y"
else
  read -r -p "Run uninstall-others.sh to disable 16 superseded plugins? (y/N) " PROCEED
fi

if [ "$PROCEED" = "y" ] || [ "$PROCEED" = "Y" ]; then
  if [ "$DRY_RUN" = "1" ]; then
    echo "[dry-run] would run: bash $HERE/uninstall-others.sh"
  else
    SHANNON_AUTO="$([ "$AUTO" = "1" ] && echo 1 || echo 0)" bash "$HERE/uninstall-others.sh"
  fi
else
  echo "skipped: uninstall-others.sh"
fi

echo ""
echo "Install complete. Restart Claude Code to fully activate."
