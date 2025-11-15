# Exec Skill Reference Documentation

This directory contains the core protocol documentation for Shannon Framework's autonomous execution system (V3.5).

## Overview

These protocols were extracted from the working Shannon CLI V3.5 implementation (`/Users/nick/Desktop/shannon-cli/src/shannon/executor/prompts.py`) and provide the foundational instructions for autonomous code execution with validation and git automation.

## Documents

### 1. [Library Discovery Protocol](./LIBRARY_DISCOVERY_PROTOCOL.md)
**Lines:** 606 | **Size:** 17KB

Mandatory research phase that occurs BEFORE implementing features. Ensures agents discover and use existing open-source libraries instead of reinventing the wheel.

**Key Topics:**
- Package registry search (npm, PyPI, CocoaPods, Maven, crates.io)
- Evaluation criteria (stars, maintenance, downloads, license)
- Common libraries by category (auth, UI, networking, forms, data, testing)
- When to build custom vs. use library
- Integration checklist

**Use When:**
- Starting any substantial feature implementation
- Need to add common functionality (auth, forms, charts, etc.)
- Want to avoid reinventing solved problems

### 2. [Functional Validation Protocol](./FUNCTIONAL_VALIDATION_PROTOCOL.md)
**Lines:** 888 | **Size:** 20KB

Three-tier validation system that ALL code must pass before committing. Ensures code doesn't just compile—it actually works from the user's perspective.

**Key Topics:**
- **Tier 1**: Static validation (~10s) - Build, types, lint
- **Tier 2**: Tests (~1-5min) - Unit, integration, regression
- **Tier 3**: Functional (~2-10min) - User perspective validation
- Platform-specific validation (Node.js, Python, iOS, React Native, Rust)
- Validation failure handling
- Automated validation scripts

**Critical Principle:**
> Building ≠ Compiling ≠ Working
> 
> Code that compiles and passes tests but doesn't work for users is worthless.

**Use When:**
- Before committing ANY code change
- Setting up CI/CD validation gates
- Training agents on quality standards

### 3. [Git Workflow Protocol](./GIT_WORKFLOW_PROTOCOL.md)
**Lines:** 905 | **Size:** 21KB

Strict git workflow with atomic commits. NEVER leave uncommitted changes. NEVER commit unvalidated code. Every commit should be deployable.

**Key Topics:**
- Pre-execution checks (clean working directory, feature branches)
- Atomic commit workflow (one change → validate → commit)
- Commit message format (WHY, WHAT, VALIDATION)
- Rollback on failure procedures
- Branch naming conventions
- Emergency procedures

**Critical Rules:**
- ✅ Commit after EVERY validated change
- ✅ ALL three validation tiers MUST pass
- ✅ Rollback immediately on failure
- ❌ NEVER commit unvalidated code
- ❌ NEVER leave uncommitted changes

**Use When:**
- Executing any code changes
- Setting up git automation
- Training agents on version control practices

## Integration

These protocols work together in the exec skill workflow:

```
User Request
    ↓
Library Discovery Protocol
    ↓ (find libraries to use)
Code Implementation (/shannon:wave)
    ↓
Functional Validation Protocol
    ↓ (validate 3 tiers)
Git Workflow Protocol
    ↓ (commit validated changes)
Success / Retry
```

## Protocol Philosophy

### 1. Library-First Development
- Research before building
- Use battle-tested solutions
- Contribute to open source ecosystem

### 2. Validation-First Commits
- Tier 1: Does it compile?
- Tier 2: Does it break anything?
- Tier 3: Does it ACTUALLY WORK?

### 3. Atomic Git History
- One logical change per commit
- Every commit is deployable
- Easy to review and revert

## Usage in Skills

These protocols are referenced by:
- **exec skill** (`../SKILL.md`) - Main autonomous execution skill
- **wave-orchestration** - Code generation phase
- **functional-testing** - Tier 3 validation implementation

## Source

Extracted from Shannon CLI V3.5 implementation:
- **File**: `/Users/nick/Desktop/shannon-cli/src/shannon/executor/prompts.py`
- **Tested**: calculator.py creation (99 lines, fully functional)
- **Proven**: Wave integration, validation, git automation working

## Version

**Shannon Framework:** V5.1.0
**Shannon CLI:** V3.5.0
**Status:** Production
**Date:** November 15, 2025

## Related Documentation

- **Parent Skill**: [`../SKILL.md`](../SKILL.md) - Exec skill implementation
- **Framework Docs**: `/Users/nick/Desktop/shannon-framework/docs/`
- **CLI Implementation**: `/Users/nick/Desktop/shannon-cli/`
