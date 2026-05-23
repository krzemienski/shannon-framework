---
name: visual-inspection
description: Systematic visual QA for UI screenshots. iOS HIG, web WCAG 2.2, cross-platform heuristics.
triggers:
  - "visual audit"
  - "screenshot review"
  - "HIG check"
  - "WCAG check"
  - "design review"
  - "UI audit"
---

# visual-inspection

Per-screenshot visual QA protocol. Evaluates layout, typography, contrast, touch targets, dark mode, overflow, spacing, accessibility.

## Behavior contract

For each screenshot under audit, evaluate:

### Layout
- Alignment to grid (8pt / 4pt)
- Spacing scale consistency
- Touch target ≥44pt iOS / ≥48dp Android / ≥24×24px web minimum
- No horizontal overflow on mobile
- Safe-area insets respected (iOS notch, Android nav bar)

### Typography
- Font scale matches design system (e.g. display-lg, body-md tokens)
- Line height ≥1.4× for body copy
- Contrast ratios: 4.5:1 small text, 3:1 large text (WCAG AA)
- No truncation on declared minimum width

### Color
- Tokens used (no raw hex except in design-system files)
- Dark mode parity (every light state has a dark-mode counterpart)
- Focus state visible on all interactive elements

### Interactive elements
- Every button reachable by tab key
- Every form input has visible label
- Loading states present for async actions
- Error states distinguishable from idle

### Cross-platform
- iOS HIG: navigation patterns, modal dismissal, tab bar ordering
- Web WCAG 2.2: focus visible, keyboard-only navigable, screen-reader landmarks
- Android Material: FAB placement, snackbar timing

## When to use

- `/shannon:audit --scope screen`
- After any UI change before declaring done
- Pre-deploy visual regression check
- Design fidelity review against a Stitch mockup

## When NOT to use

- Pure backend / API change
- CLI tool with no UI surface

## Output format

Findings classified BLOCKING / HIGH / MEDIUM / LOW with screenshot region annotated (citation: `evidence/screen-<slug>/<screenshot>.png` + bounding-box description).
