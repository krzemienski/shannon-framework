---
authority: TEST_GUARDIAN blocks non-compliant tests
base: SuperClaude /test command
category: command
command: /sc:test
description: Shannon V3 enhanced testing command with NO MOCKS enforcement and functional
  validation
enhancements: NO MOCKS enforcement, Puppeteer/Simulator testing, TEST_GUARDIAN activation
linked_skills:
- shannon-browser-test
mcp_servers:
- puppeteer
- playwright
- serena
name: sc:test
performance-profile: standard
progressive_disclosure:
  estimated_tokens: 200
  full_content: resources/FULL.md
  tier: 1
sub_agents:
- TEST_GUARDIAN
- QA
wave-enabled: false
---

/sc:test - Shannon V3 Enhanced Testing Command

> **Shannon V4 Skill-Based Framework**: Progressive disclosure command with linked skills

## Purpose

**Base**: Enhanced from SuperClaude's `/test` command
**Enhancement Focus**: Functional testing first, NO MOCKS philosophy, platform-specific validation
**Primary Agent**: TEST_GUARDIAN (enforcement authority)
**Secondary Agents**: QA persona, implementation-worker (test code generation)

---

## Usage Patterns

**1. Generate Functional Tests for Feature**
```bash
/sc:test feature auth-flow

# Generates:
# - Puppeteer tests for login UI (web)
# - XCUITests for login flow (iOS)
# - HTTP tests for auth API endpoints
# - Database validation tests
```

**2. Generate Tests for Specific Platform**
```bash
/sc:test web --scope src/components/TaskList.tsx

# Generates Puppeteer functional tests:
# - Render task list with real API data
# - Add task through real UI interaction
# - Delete task and verify real database removal
# - Filter tasks with real backend filtering
```

**3. Run Compliance Scan**
```bash
/sc:test --scan-mocks

# TEST_GUARDIAN scans codebase for:
# - Mock library imports
# - Stub/fake implementations
# - Simulated responses
# - Reports violations with functional alternatives
```

**4. Generate Test Environment**
```bash
/sc:test --setup-env

# Generates:
# - docker-compose.test.yml (services)
# - Test database initialization scripts
# - Environment variable configuration
# - Setup/teardown scripts
```

**5. Execute Full Test Suite**
```bash
/sc:test --run-all

# Executes:
# 1. Start test environment (Docker Compose)
# 2. Run all functional tests
# 3. Collect coverage metrics
# 4. Validate quality gates
# 5. Generate completion report
```

##

## Skill Integration

**v4 NEW**: This command activates skills:

- `shannon-browser-test`

## Quick Reference

📚 **Full Documentation**: See [resources/FULL.md](./resources/FULL.md) for:
- Complete execution algorithms
- Detailed examples
- Integration patterns
- Validation rules

---

**Shannon V4** - Skill-Based Progressive Disclosure 🚀
