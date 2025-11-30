---
name: sh:check_mcps
linked_skills:
  - shannon-mcp-validator
progressive_disclosure:
  tier: 1
  estimated_tokens: 100
---

# /sh:check_mcps
> **Skill-Based**: This command activates the `shannon-mcp-validator` skill

## Usage
```bash
/sh:check_mcps
/sh:check_mcps serena
```

## What It Does
Validates MCP server availability and provides installation guidance:
- Detect installed MCP servers (serena, sequential, puppeteer, etc.)
- Categorize: required/recommended/optional
- Generate installation guide with commands
- Provide graceful degradation strategies
- Project-specific recommendations

Outputs SITREP with:
- MCP status (installed/missing)
- Installation priority
- Quick install commands
- Documentation links

## Skill Activation
📚 **Full MCP validation logic**: `shannon-v4-plugin/skills/shannon-mcp-validator/SKILL.md`

**Progressive disclosure**: Full skill content loaded only when activated

---

**Shannon V4** - MCP Validation ✓
