---
name: research-validation
description: Gather standards, best practices, applicable criteria before validation planning. Maps standards (WCAG, HIG, security) to Shannon validation skills.
triggers:
  - "research validation standards"
  - "applicable criteria"
  - "WCAG criteria"
  - "HIG criteria"
  - "security standards"
---

# research-validation

Phase 0 of `/shannon:validate` for new platforms. Maps external standards to Shannon-internal validation criteria.

## Behavior contract

1. Identify what's being validated (platform, surface, feature type).
2. Map to applicable standards:
   - **Web UI** → WCAG 2.2 AA, Core Web Vitals (LCP/INP/CLS)
   - **iOS UI** → Apple HIG, accessibility audit checklist
   - **API** → OpenAPI compliance, OWASP API top 10
   - **CLI** → POSIX argument conventions, exit-code semantics
   - **Security** → OWASP top 10, secrets management
3. For each applicable standard: fetch current version via WebFetch or context7. Save to `research/<topic>/standards/<standard>-<timestamp>.md`.
4. Map each standard's criteria to Shannon skill: which skill (visual-inspection, functional-validation, etc.) covers which criterion?
5. Output: `research/<topic>/SUMMARY.md` — table of (standard, criterion, mapped skill, evidence type required).

## When to use

- New project / new platform onboarding
- Validating against a new compliance regime
- Pre-`/shannon:validate` for high-stakes features

## When NOT to use

- Already-mapped standards in a recurring project
- Internal-only tool with no compliance dimension

## Iron rules

- Always fetch live — no training-data recall of standards.
- Cite specific section / criterion number, not "WCAG says".
- Include retrieval timestamp.
