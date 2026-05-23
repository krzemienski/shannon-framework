---
name: install
description: Idempotent setup. Writes marketplace declaration; runs uninstall-others.sh (after y/N prompt) unless --parallel. Verifies via doctor at end. Local marketplace only (UQ-CMD-3).
replaces:
  - /oh-my-claudecode:omc-setup
  - /validationforge:vf-setup
  - /crucible:setup
argument-hint: "[--parallel | --replace]"
---

# /shannon:install

Atomic install + activation. The single command that gets Shannon working in a project.

## Inputs

- `--parallel` — coexist with other plugins (skip uninstall-others.sh)
- `--replace` — default; runs uninstall-others.sh after y/N prompt

## Behavior

1. **Verify plugin tree** — confirm Shannon files at `/Users/nick/Desktop/shannon-framework/` OR cache path. Run `scripts/_validate-manifest.js`.
2. **Marketplace declaration** — read `~/.claude/settings.json`. If `extraKnownMarketplaces.shannon-local` missing, add it (path = Shannon repo path).
3. **Install via CC** — instruct user (or auto-execute via gh CLI / Bash) `/plugin install shannon@shannon-local`.
4. **Replace mode (default)** — invoke `scripts/uninstall-others.sh`:
   - Print plan: which of 16 plugins will be disabled.
   - y/N prompt (no `-y` means no execution).
   - On y: set `enabledPlugins["<slug>"] = false` for each; print diff.
   - Tell user to restart CC.
5. **Parallel mode** — skip step 4.
6. **Verify** — invoke `/shannon:doctor`; require all checks PASS.

## Local marketplace only (v6.0)

Per UQ-CMD-3: v6.0 supports local-directory marketplaces only. v6.1 may add GitHub-based marketplaces.

## Success criteria

- Marketplace declared.
- Shannon plugin installed (visible in `/plugin list`).
- Conflicting plugins disabled (in `--replace` mode).
- `/shannon:doctor` all green.

## Hooks fired

None — this is the bootstrap; hooks are registered DURING install.

## Skills invoked

- `observability-report` (for doctor verification step)

## Examples

```
/shannon:install
/shannon:install --parallel    # coexist mode
```
