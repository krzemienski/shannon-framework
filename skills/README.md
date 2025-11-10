# Shannon Framework V4 Skills

This directory contains Shannon's behavioral skills that commands orchestrate.

## Skill Structure

Each skill follows this structure:
```
skill-name/
├── SKILL.md          # Main skill file (required)
├── references/       # Deep reference docs (progressive disclosure)
├── examples/         # Usage examples (minimum 3)
└── templates/        # Output templates (if applicable)
```

## Available Skills

## Core Shannon Skills
- spec-analysis - 8D complexity scoring
- wave-orchestration - Parallel wave execution
- phase-planning - 5-phase implementation planning
- context-preservation - Checkpoint creation
- context-restoration - Checkpoint restoration
- functional-testing - NO MOCKS enforcement
- mcp-discovery - MCP server recommendations
- memory-coordination - Serena MCP queries
- goal-management - North Star tracking
- sitrep-reporting - Military SITREP protocol for multi-agent coordination ✅
- shannon-analysis - General analysis

**Enhanced Skills** (from reference frameworks):
- confidence-check - Pre-implementation validation (from SuperClaude)
- project-indexing - Codebase compression (from SuperClaude) ✅

**Meta-Skill**:
- using-shannon - Auto-loaded via SessionStart hook

## Skill Development

See: ../../docs/SKILL_DEVELOPMENT_GUIDE.md

## Testing

```bash
# Validate skill structure
python3 shannon-plugin/tests/validate_skills.py

# Test skill invocation
python3 shannon-plugin/tests/test_skill_activation.py
```
