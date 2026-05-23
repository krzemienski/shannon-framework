---
name: doctor
description: Health check. Validates plugin manifest, hooks.json registration, settings.json sanity, log dirs writable, marketplace declarations.
replaces:
  - /oh-my-claudecode:omc-doctor
  - /crucible:doctor
  - /crucible:status
argument-hint: "[--verbose]"
---

# /shannon:doctor

Self-diagnostic. Reports installation health + drift.

## Inputs

- `--verbose` — include per-check details (default: summary only)

## Behavior

Runs these checks in order; emits PASS / FAIL per check:

1. **Plugin manifest** — `.claude-plugin/plugin.json` present, version=6.0.0, fields complete.
2. **Marketplace declaration** — `.claude-plugin/marketplace.json` present, name=shannon-local.
3. **Hooks registration** — `hooks/hooks.json` references all 14 scripts; all scripts present on disk.
4. **Settings.json sanity** — `~/.claude/settings.json` valid JSON; `extraKnownMarketplaces.shannon-local` present.
5. **Log dirs writable** — `~/.claude/logs/shannon/` exists and writable; can append to `hooks.jsonl` and `hook-errors.jsonl`.
6. **CLI marketplace registration** — `/plugin list` includes `shannon@shannon-local`.
7. **Conflicting plugins** — list which of the 16 consolidated plugins are still enabled; recommend disabling.

Output: stdout summary + `reports/doctor-<run-id>.md` with full details.

## Success criteria

- All 7 checks PASS = healthy install.
- Any FAIL → actionable remediation message + path to relevant docs.

## Hooks fired

None — read-only health check.

## Skills invoked

- `observability-report` (drift detection + dashboard formatting)

## Examples

```
/shannon:doctor
/shannon:doctor --verbose
```
