---
name: evidence-indexing
description: Maintain README.md (purpose) and INDEX.md (artifact enumeration) in every evidence directory. Refuse to leave any evidence dir un-indexed at gate completion.
triggers:
  - "index evidence"
  - "write evidence index"
  - "evidence INDEX.md"
  - "enumerate artifacts"
---

# evidence-indexing

Every evidence directory must be navigable. This skill enforces that.

## Behavior contract

After any phase completes (and after every gate):

1. For each subdirectory under `e2e-evidence/<run-id>/`:
   - If `README.md` missing → generate: 1-paragraph purpose statement explaining what this directory contains.
   - If `INDEX.md` missing → generate: enumerated table of every artifact (path, byte count, what it represents).
2. If directory has > 10 files: split INDEX.md into sections by step/journey/role.
3. Verify every artifact in INDEX.md actually exists on disk (no phantom citations).

## INDEX.md structure

```markdown
# Evidence Index — <phase or journey name>

**Run:** <run-id>
**Phase:** <phase number + name>
**Generated:** <ISO-8601>

## Artifacts

| File | Size | Type | What it shows |
|---|---|---|---|
| step-01-login-loaded.png | 24kb | screenshot | /login renders successfully |
| step-02-submit-pressed.png | 28kb | screenshot | Submit button click registered |
| step-03-dashboard.json | 1.2kb | API response | Dashboard payload after auth |
| ... | ... | ... | ... |
```

## When to use

- After every phase artifact lands in `e2e-evidence/`
- Before invoking any gate (`completion-gate`, `oracle-review`)
- As a periodic maintenance pass

## When NOT to use

- Directories not under `e2e-evidence/` (logs/, reports/, plans/ have their own conventions)

## Iron rules

- **Refuse to leave any evidence dir un-indexed at gate-completion time.**
- **Never invent files.** Every INDEX.md entry must exist on disk.
- **Never delete an evidence file** to "clean up" the index — captured = immutable.
