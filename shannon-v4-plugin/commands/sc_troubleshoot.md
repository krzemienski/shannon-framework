---
activates-agents:
- ANALYZER
base: SuperClaude /troubleshoot
category: command
command: /sc:troubleshoot
complexity: moderate-to-high
description: Enhanced systematic debugging and root cause analysis with evidence tracking
enhancement: Shannon V3 structured debugging framework + Serena evidence tracking
mcp-servers:
- serena
- sequential
name: sc:troubleshoot
progressive_disclosure:
  estimated_tokens: 200
  full_content: resources/FULL.md
  tier: 1
tools:
- Read
- Grep
- Glob
- Sequential
- Serena
- Bash
wave-enabled: true
---

/sc:troubleshoot Command

> **Shannon V4 Skill-Based Framework**: Progressive disclosure command with linked skills

## Purpose

> **Enhanced from SuperClaude's /troubleshoot with Shannon V3 structured debugging framework and evidence-based investigation.**

## Usage Patterns

### Pattern 1: Bug Investigation

```bash
/sc:troubleshoot "form submission fails on production"

# Activates:
# 1. ANALYZER agent for systematic investigation
# 2. Evidence collection via Read, Grep, Glob
# 3. Hypothesis testing with Sequential MCP
# 4. Root cause identification
# 5. Fix recommendation with validation
```

**Investigation Flow**:
1. Document symptom and context
2. Collect evidence from code, logs, configs
3. Form hypotheses about potential causes
4. Test hypotheses systematically
5. Identify root cause via Five Whys
6. Recommend fix with validation criteria
7. Save investigation to Serena

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
