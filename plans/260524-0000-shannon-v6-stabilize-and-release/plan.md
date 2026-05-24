# Shannon v6 — Stabilization & Release

**Status:** PENDING APPROVAL · Deliberate mode · Deepened (2026-05-24)
**Target repo:** `/Users/nick/Desktop/shannon-framework/` (remote `github.com/krzemienski/shannon-framework`)
**No mutations performed during planning.**

<mock_detection_protocol>
Before executing any task, check intent:
- Creating .test.*, _test.*, *Tests.*, test_* files → STOP
- Importing mock libraries / in-memory DBs / TEST_MODE flags → STOP
This plan validates a plugin via REAL headless `claude` sessions + the existing
benchmark runner. No mocks, no synthetic logs. Fix the real system instead.
</mock_detection_protocol>

## Objective

Bring Shannon to a clean, tagged **v6.0.0** release: resolve the two-Shannons-on-disk
problem, reconcile three unmerged rebuild branches, relocate the validation plan into
the Shannon repo, and checkpoint the Phase-6 F1=1.00 milestone — WITHOUT regressing the
benchmark and WITHOUT breaking post-16's repo-reference contract.

## Where We Left Off (verified)

Shannon v6 isolated-validation reached **Phase 6 / F1=1.00 across 30 skills** (innocent-prompt
clean 90%→100%, 4 dangerous triggers killed, word-boundary matcher patched). Evidence:
`blog-series/plans/260523-1617-shannon-isolated-validation/evidence-report.md`. Work paused
when focus pivoted to LinkedIn social publishing — left at a clean milestone, not broken.

## Confirmed State (research-backed)

<facts>
  <fact id="F1" source="git rev-list main..wt/*">Three rebuild branches unmerged: core +6, integration +21, domains +25 (all 0 behind main).</fact>
  <fact id="F2" source="git tag">Tags run v2.1.0 → v5.1.0-beta. No v6 tag. CHANGELOG.md already exists.</fact>
  <fact id="F3" source="ls .claude-plugin/">Canonical manifest is .claude-plugin/plugin.json. Root plugin.json does NOT exist (correct — old root manifest was the fixed bug).</fact>
  <fact id="F4" source="ls + shasum blog-series/shannon-framework">Orphan is the post-16 BLOG-DEMO snapshot (5 hooks, functional-validation skill, code-reviewer agent, ROOT plugin.json = old structure). Content DIFFERS from canonical.</fact>
  <fact id="F5" source="e2e-evidence/repo-reference-audit.md:77,155">Post-16 + Post-07 frontmatter point at github.com/krzemienski/shannon-framework. Audit expects hooks/block-test-files.js to exist in the referenced repo.</fact>
  <fact id="F6" source=".archive/.../synthesis-A-through-N.md:46">"Two Shannons" flagged 2026-04-20 — long-standing known issue, not new drift.</fact>
</facts>

## Gaps

| # | Gap | Severity |
|---|---|---|
| G1 | Orphan `blog-series/shannon-framework/` (post-16 demo, old structure) pollutes parent `git status`, unregistered as submodule | HIGH |
| G2 | THREE rebuild branches unmerged (core/integration/domains) — merge order unknown | HIGH |
| G3 | Validation plan lives in blog-series/plans/, should live in shannon-framework | MEDIUM |
| G4 | No v6.0.0 tag / CHANGELOG entry for the Phase-6 milestone | MEDIUM |
| G5 | Empty `blog-series/plans/260523-0008-shannon-rebuild/` (abandoned) | LOW |
| G6 | Stale Desktop dirs: `shannon-agemt/` (empty), `shannon-framework-integration/` (orphan snapshot) | LOW |
| G7 | Post-16 ↔ repo contract: does post-16 expect the BLOG-DEMO content or the canonical framework? Undecided. | **BLOCKER for G1** |

---

## RALPLAN-DR Decision Block

**Principles**
1. Real-system evidence only — benchmark re-runs green after every phase
2. Project-level opt-in (`.shannon/active`) — no cross-project pollution
3. Shannon code lives only in `/Users/nick/Desktop/shannon-framework/`
4. Every destructive step is preceded by a captured-evidence safety check + reversible until a tag is pushed
5. Post-16's published repo contract is honored — no doc is silently invalidated

**Decision Drivers**
1. User's explicit cleanup ask (nested dir / new repo locality)
2. Phase-6 milestone deserves a durable tag before feature work
3. Three unmerged branches must reconcile cleanly into one releasable main

**Viable Options**

| Option | Pros | Cons |
|---|---|---|
| A — feature work first | velocity | ignores user ask; 3 branches rot; orphan stays |
| B — cleanup + release + stop | clean checkpoint | no features this cycle |
| **C ★ — cleanup → branch reconcile → v6.0.0 tag → Phase-9 menu** | respects ask; durable milestone; informed feature pick | one session before velocity |

**★ Recommended: Option C.**

**Pre-mortem (revised with research)**

1. *Orphan removal breaks post-16 contract (G7)* — **HIGH, confirmed**. `repo-reference-audit.md` asserts post-16 references `shannon-framework/hooks/block-test-files.js`. The published GitHub repo (not the orphan) is what readers clone, so the orphan is likely a stale local artifact — but this MUST be confirmed at VG-7.0 before any `rm`. Mitigation: resolve G7 as the FIRST gate; if post-16 depends on the orphan's exact content, migrate that content into canonical or update the post BEFORE deletion.
2. *Branch merge conflicts* — domains(25) likely supersedes core(6)+integration(21) but overlap is unverified. Mitigation: VG-8.1 computes pairwise `git log --left-right` to establish containment before any merge.
3. *Benchmark regresses after branch merge* — Mitigation: VG-8.3 re-runs `benchmarks/run-activation.js`; F1 must stay 1.00 or merge is reverted.

**Test plan (deliberate)**
- integration: `node benchmarks/run-activation.js` → F1=1.00, FPs=0 after every phase
- e2e: `scripts/drive-tests.sh` headless across 5 fixtures via `csd`; capture hooks.jsonl deltas
- observability: snapshot `~/.claude/logs/shannon/hooks.jsonl` per phase to `evidence/`
- NO unit tests (Iron Rule)

---

## Phase 7 — Workstream Cleanup

<task id="7.0" priority="blocker">
  <description>Resolve G7: determine whether post-16 depends on the orphan's content or the published GitHub repo.</description>
  <validation_gate id="VG-7.0" blocking="true">
    <execute>Read posts/post-16-claude-code-plugins/post.md; read e2e-evidence/repo-reference-audit.md sections for post-16; compare claimed file paths against canonical shannon-framework tree.</execute>
    <capture>grep -n "shannon-framework" posts/post-16-claude-code-plugins/post.md | tee evidence/vg7.0-post16-refs.txt; (cd /Users/nick/Desktop/shannon-framework &amp;&amp; ls hooks/ skills/ agents/) | tee evidence/vg7.0-canonical-tree.txt</capture>
    <pass_criteria>Documented verdict: post-16 references resolve to the PUBLISHED GitHub repo (clone target), NOT the local orphan dir. If false → orphan content must be reconciled into canonical first.</pass_criteria>
    <verdict>PASS → 7.1 | FAIL → migrate orphan content to canonical or amend post-16, re-gate</verdict>
  </validation_gate>
</task>

<task id="7.1" depends_on="7.0">
  <description>Audit all live refs to the orphan path (exclude .archive/, e2e-evidence/ historical).</description>
  <validation_gate id="VG-7.1" blocking="true">
    <capture>grep -rn "blog-series/shannon-framework\|^shannon-framework/" --include=*.md --include=*.ts --include=*.json --exclude-dir=.archive --exclude-dir=node_modules . | tee evidence/vg7.1-live-refs.txt</capture>
    <pass_criteria>Every live ref is either (a) the companion-repo concept pointing at GitHub (safe), or (b) explicitly updated in this phase. Zero refs depend on the orphan directory's local presence.</pass_criteria>
    <verdict>PASS → 7.2 | FAIL → patch refs first</verdict>
  </validation_gate>
</task>

<task id="7.2" depends_on="7.1">
  <description>Remove the orphan dir only after VG-7.0 + VG-7.1 pass. Reversible via git until parent commit.</description>
  <approach>git rm -r blog-series/shannon-framework (if tracked) OR rm -rf if untracked — confirm tracked state first with git ls-files.</approach>
  <validation_gate id="VG-7.2" blocking="true">
    <capture>git -C /Users/nick/Desktop/blog-series status --short | tee evidence/vg7.2-status.txt</capture>
    <pass_criteria>blog-series git status shows no shannon-framework entries; parent repo clean of the orphan.</pass_criteria>
    <verdict>PASS → 7.3 | FAIL → investigate residual refs</verdict>
    <mock_guard>Do NOT delete the canonical /Users/nick/Desktop/shannon-framework. Only the nested blog-series copy.</mock_guard>
  </validation_gate>
</task>

<task id="7.3" depends_on="7.2">
  <description>Relocate the validation plan into the Shannon repo (G3); leave an .archive pointer in blog-series.</description>
  <approach>Copy blog-series/plans/260523-1617-shannon-isolated-validation/ → shannon-framework/plans/ ; write a one-line .archive/MANIFEST pointer in blog-series.</approach>
  <validation_gate id="VG-7.3" blocking="true">
    <capture>ls /Users/nick/Desktop/shannon-framework/plans/260523-1617-shannon-isolated-validation/ | tee evidence/vg7.3-relocated.txt</capture>
    <pass_criteria>Plan + evidence-report.md + evidence/ present under shannon-framework/plans/; blog-series retains an archive pointer (no silent data loss).</pass_criteria>
    <verdict>PASS → 7.4 | FAIL → restore from blog-series copy</verdict>
  </validation_gate>
</task>

<task id="7.4" depends_on="7.3">
  <description>Delete empty plans/260523-0008-shannon-rebuild/ (G5) and stale Desktop dirs shannon-agemt/, shannon-framework-integration/ (G6) — AFTER explicit user confirmation in the execution turn.</description>
  <validation_gate id="VG-7.4" blocking="true">
    <prerequisites>find each target -type f | wc -l captured to prove emptiness/staleness BEFORE rm.</prerequisites>
    <capture>find /Users/nick/Desktop/shannon-framework-integration -type f | wc -l | tee evidence/vg7.4-staleness.txt</capture>
    <pass_criteria>shannon-agemt empty (0 files); shannon-framework-integration confirmed orphan snapshot (no unique unpushed work vs canonical). User confirms deletion.</pass_criteria>
    <verdict>PASS → Phase 8 | FAIL → keep dir, note in report</verdict>
  </validation_gate>
</task>

**Phase 7 exit:** `node benchmarks/run-activation.js` → F1=1.00 (cleanup must not touch plugin behavior). Single atomic commit in shannon-framework.

---

## Phase 8 — Branch Reconciliation & Release v6.0.0

<task id="8.1">
  <description>Establish containment among the three rebuild branches before merging (G2).</description>
  <validation_gate id="VG-8.1" blocking="true">
    <capture>cd /Users/nick/Desktop/shannon-framework; for b in core integration domains; do echo "== $b =="; git log --oneline main..wt/shannon-rebuild-$b; done | tee evidence/vg8.1-branch-divergence.txt; git log --left-right --oneline wt/shannon-rebuild-domains...wt/shannon-rebuild-integration | tee evidence/vg8.1-domains-vs-integration.txt</capture>
    <pass_criteria>Documented merge order. Determine if domains(25) is a superset of core(6)+integration(21) or if each carries unique commits. Output an explicit ordered merge sequence.</pass_criteria>
    <verdict>PASS → 8.2 | FAIL → escalate to user if branches conflict irreconcilably</verdict>
  </validation_gate>
</task>

<task id="8.2" depends_on="8.1">
  <description>Merge the reconciled branch(es) into main per the VG-8.1 order, via PR, self-merge after green.</description>
  <approach>Prefer fast-forward where divergence is 0-behind. For overlapping branches, merge lowest-unique-commit branch first; resolve conflicts by honoring the opt-in gate + word-boundary matcher as source of truth.</approach>
  <validation_gate id="VG-8.2" blocking="true">
    <capture>git -C /Users/nick/Desktop/shannon-framework log --oneline -5 main | tee evidence/vg8.2-main-head.txt; git status --short | tee -a evidence/vg8.2-main-head.txt</capture>
    <pass_criteria>main contains the opt-in gate commit (a2d9626 lineage) + plugin manifest fix (9fdedc2); working tree clean; no merge conflict markers remain.</pass_criteria>
    <verdict>PASS → 8.3 | FAIL → abort merge, restore main, re-plan order</verdict>
  </validation_gate>
</task>

<task id="8.3" depends_on="8.2">
  <description>Post-merge benchmark + e2e regression gate.</description>
  <validation_gate id="VG-8.3" blocking="true">
    <execute>node benchmarks/run-activation.js ; bash scripts/drive-tests.sh (headless csd across 5 fixtures)</execute>
    <capture>node benchmarks/run-activation.js | tee evidence/vg8.3-benchmark.txt; cp ~/.claude/logs/shannon/hooks.jsonl evidence/vg8.3-hooks-snapshot.jsonl</capture>
    <pass_criteria>F1=1.00, FPs=0 on main; enabled fixture fires hooks, disabled+unset fixtures stay silent (gate holds post-merge).</pass_criteria>
    <verdict>PASS → 8.4 | FAIL → bisect the regressing merge commit, fix real system, re-run from VG-8.3</verdict>
    <mock_guard>If a fixture fails, fix the gate logic — do NOT relax the benchmark thresholds to pass.</mock_guard>
  </validation_gate>
</task>

<task id="8.4" depends_on="8.3">
  <description>Tag v6.0.0, write CHANGELOG entry, update README opt-in docs (G4 + G7-doc).</description>
  <approach>Annotated tag summarizing Phase 0–6 evidence. CHANGELOG: F1 90%→100% delta, 4 trigger fixes, word-boundary matcher, opt-in gate. README: .shannon/active model + /shannon:enable + /shannon:disable.</approach>
  <validation_gate id="VG-8.4" blocking="true">
    <capture>git tag --verify v6.0.0 2>&amp;1 | tee evidence/vg8.4-tag.txt; head -40 CHANGELOG.md | tee evidence/vg8.4-changelog.txt</capture>
    <pass_criteria>v6.0.0 annotated tag present on the merged main HEAD; CHANGELOG entry cites specific F1 metrics + evidence paths; README documents the opt-in gate with both commands.</pass_criteria>
    <verdict>PASS → push tag + Phase 9 menu | FAIL → fix tag/notes</verdict>
  </validation_gate>
</task>

**Phase 8 exit:** `git push origin main --tags`; GitHub release visible. This is the first irreversible step — everything before VG-8.4 is locally reversible.

---

## Phase 9 — Direction Menu (DEFERRED to user)

Starts as a fresh ralplan once user picks one:
- **9a** Marketplace listing — publish shannon@6.0.0 to the Claude Code plugin marketplace
- **9b** Skill expansion — next skill batch (user names domains)
- **9c** Downstream integration tests — run against orbit / anneal / ValidationForge real projects
- **9d** Public launch — pair post-16 with a `/shannon:enable` tutorial
- **9e** User-proposed direction

---

## Gate Manifest

<gate_manifest>
  <total_gates>9</total_gates>
  <sequence>VG-7.0 → VG-7.1 → VG-7.2 → VG-7.3 → VG-7.4 → VG-8.1 → VG-8.2 → VG-8.3 → VG-8.4</sequence>
  <policy>All gates BLOCKING. No advancement on FAIL.</policy>
  <evidence_dir>plans/260524-0000-shannon-v6-stabilize-and-release/evidence/</evidence_dir>
  <regression>Benchmark gate (F1=1.00) re-runs at Phase-7 exit AND VG-8.3. Any drop = revert.</regression>
  <reversibility>All steps reversible until VG-8.4 push. The push is the point of no return.</reversibility>
</gate_manifest>

## ADR

| Field | Value |
|---|---|
| **Decision** | Stabilize Shannon at v6.0.0 (orphan cleanup + 3-branch reconcile + tag) before any feature work; defer direction to a post-release menu. |
| **Drivers** | (1) explicit user cleanup ask; (2) Phase-6 F1=1.00 milestone worth tagging; (3) 3 unmerged branches must converge. |
| **Alternatives** | A (features first) — rejected: ignores user ask, branches rot. B (cleanup+release+stop) — rejected: leaves momentum unused. |
| **Why chosen** | Lowest-regret: every step reversible until the v6.0.0 push; benchmark gate guards behavior; post-16 contract protected by VG-7.0. |
| **Consequences** | (+) clean repos, durable milestone, plan in correct home; (−) no features this cycle; (−) G7 may force post-16 edit or content migration. |
| **Follow-ups** | Phase-9 pick; decide whether shannon-cli + shannon-mcp + shannon-framework should converge into a monorepo or stay separate repos. |

## Open Questions

<open_questions>
  <q id="OQ1" blocking="VG-7.0">Does post-16 expect the orphan's BLOG-DEMO content, or is the published GitHub repo the sole clone target? Resolved at VG-7.0.</q>
  <q id="OQ2" blocking="VG-8.1">Is wt/shannon-rebuild-domains a superset of core+integration, or do all three carry unique commits requiring ordered merges?</q>
  <q id="OQ3" deferred="true">Long-term: monorepo for the three shannon-* repos, or keep separate? Phase-9 concern, not blocking.</q>
</open_questions>
