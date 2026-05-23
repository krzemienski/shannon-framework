---
name: disable
description: Opt this project OUT of Shannon enforcement. Writes .shannon/disabled and removes .shannon/active. Sticky — survives until /shannon:enable --force.
---

# /shannon:disable

Deactivate Shannon hooks for the current project.

## Behavior

1. Resolve project root: `$CLAUDE_PROJECT_DIR` if set, else `pwd`.
2. `mkdir -p .shannon`.
3. Remove `.shannon/active` if present.
4. Write `.shannon/disabled` with ISO timestamp + reason (from `$1` if given).
5. Print confirmation.

## Implementation (Bash)

```bash
ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
mkdir -p "$ROOT/.shannon"
rm -f "$ROOT/.shannon/active"
REASON="${1:-user-requested}"
printf '{"disabled":"%s","reason":"%s"}\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$REASON" > "$ROOT/.shannon/disabled"
echo "Shannon disabled at $ROOT/.shannon/disabled"
```

## Re-enable

`/shannon:enable --force` removes `.shannon/disabled` and rewrites
`.shannon/active`.

## Why "sticky" off

Some projects pin Shannon as permanently off (e.g. legacy repos, vendored deps).
Sticky disabled prevents accidental re-activation by tooling or other plugins.
