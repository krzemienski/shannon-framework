---
name: enable
description: Opt this project into Shannon enforcement by writing the .shannon/active sentinel. Hooks become no-ops in projects that have not opted in.
argument-hint: "[--force]"
---

# /shannon:enable

Activate Shannon hooks for the current project. Without this, all Shannon hooks
silently exit 0 — they do not pollute unrelated projects.

## Behavior

1. Resolve project root: `$CLAUDE_PROJECT_DIR` if set, else `pwd`.
2. `mkdir -p .shannon`.
3. If `.shannon/disabled` exists: remove it (only if `--force`, else refuse).
4. Write `.shannon/active` with ISO timestamp + Shannon version.
5. Print confirmation + cite gate semantics.

## Implementation (Bash)

```bash
ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
mkdir -p "$ROOT/.shannon"
if [ -f "$ROOT/.shannon/disabled" ]; then
  if [ "$1" = "--force" ]; then
    rm "$ROOT/.shannon/disabled"
  else
    echo "Refusing: .shannon/disabled present. Re-run with --force to override." >&2
    exit 1
  fi
fi
printf '{"activated":"%s","version":"6.0.0"}\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$ROOT/.shannon/active"
echo "Shannon enabled at $ROOT/.shannon/active"
```

## Reversal

`/shannon:disable` writes `.shannon/disabled` (sticky off-switch) and removes
`.shannon/active`. Re-enable with `/shannon:enable --force`.

## Gate semantics

- `.shannon/active` present, `.shannon/disabled` absent → hooks fire
- `.shannon/disabled` present → hooks no-op (sticky off)
- neither present → hooks no-op (default off; explicit opt-in required)
- `SHANNON_DISABLE=1` env → hooks no-op (per-shell escape)
- `SHANNON_GLOBAL=1` env → hooks fire everywhere (override; for testing)
