---
activates:
- REFACTORING_EXPERT
- QUALITY_ENGINEER
base: SuperClaude /cleanup command
category: command
complexity: moderate
description: Systematic code cleanup and technical debt reduction with mandatory test
  validation
enhancement: Shannon V3 cleanup patterns + test validation + context preservation
mcp-servers:
- serena
- sequential
- context7
name: sc:cleanup
progressive_disclosure:
  estimated_tokens: 200
  full_content: resources/FULL.md
  tier: 1
tools:
- Read
- Edit
- MultiEdit
- Grep
- Glob
- Bash
- Serena
- Sequential
wave-enabled: false
---

/sc:cleanup - Enhanced Cleanup Command

> **Shannon V4 Skill-Based Framework**: Progressive disclosure command with linked skills

## Purpose

> **Enhanced from SuperClaude's `/cleanup` command with Shannon V3 systematic cleanup patterns, mandatory test validation, and Serena context preservation for project memory.**

## Usage Patterns

### Basic Usage

```bash
# Clean up specific file
/sc:cleanup @src/utils/helpers.ts

# Clean up directory
/sc:cleanup @src/components/

# Clean up entire project with specific patterns
/sc:cleanup --patterns "dead_code,imports,formatting"

# Clean up with specific risk tolerance
/sc:cleanup @src/ --max-risk medium
```

##

## Skill Integration

**v4 NEW**: This command activates skills:


## Quick Reference

📚 **Full Documentation**: See [resources/FULL.md](./resources/FULL.md) for:
- Complete execution algorithms
- Detailed examples
- Integration patterns
- Validation rules

---

**Shannon V4** - Skill-Based Progressive Disclosure 🚀
