# Shannon Framework V3

**Context Engineering Framework for Claude Code**

Shannon V3 is a markdown-based behavioral framework that enhances Claude Code with advanced orchestration, specification analysis, and wave-based execution capabilities.

## Architecture

Shannon is **NOT** a Python execution framework. It is a **context engineering system** that:

1. **Behavioral Programming**: Markdown files containing instructions Claude follows
2. **System Prompt Injection**: Claude Code reads .md files and follows behavioral patterns
3. **Python Installer**: Copies markdown files to `~/.claude/` for Claude Code to discover
4. **No Code Execution**: Framework configures behavior, doesn't execute code

## Directory Structure

```
Shannon/
├── Core/           # 8 core behavioral pattern files
├── Agents/         # 19 sub-agent definitions (5 new + 14 enhanced)
├── Commands/       # 29 commands (4 new /sh: + 25 enhanced /sc:)
├── Modes/          # 9 modes (2 new + 7 from SuperClaude)
└── Hooks/          # 1 critical PreCompact hook (Python)
```

## Key Innovations Over SuperClaude

1. **8-Dimensional Spec Analysis**: Automatic complexity scoring across 8 dimensions
2. **5-Phase Planning**: Structured planning with validation gates
3. **Wave Orchestration**: Parallel sub-agent execution with context sharing
4. **PreCompact Hook**: Prevents context loss via checkpoint/restore
5. **NO MOCKS Testing**: Functional testing mandate with Puppeteer/iOS simulator
6. **Dynamic MCP Discovery**: Suggests 6-15 MCPs based on domain analysis
7. **Cross-Wave Context**: All agents read all previous wave results via Serena

## Installation

```bash
pip install shannon-framework
shannon install
```

## Commands

All Shannon commands use the `/sh:` prefix:

- `/sh:analyze-spec` - 8-dimensional complexity analysis
- `/sh:create-waves` - Generate wave execution plan
- `/sh:checkpoint` - Manual context preservation
- `/sh:restore` - Restore from checkpoint

Plus 25 enhanced commands from SuperClaude (still available as `/sc:`)

## Current Status

**Version**: 3.0.0-dev
**Stage**: Initial structure created
**Branch**: master
**Specification**: SHANNON_V3_SPECIFICATION.md (approved)

## Environment Details

- **Agent CWD**: `/Users/nick/Documents/shannon`
- **Codebase Directory**: `/Users/nick/Documents/shannon`
- **Deployment Target**: `~/.claude/` (Claude Code reads from here)

## Next Steps

1. Implement Core behavioral files (SPEC_ANALYSIS.md, PHASE_PLANNING.md, etc.)
2. Implement Sub-Agent definitions
3. Implement Command files
4. Implement Modes
5. Implement PreCompact hook (Python)
6. Create Python installer (fork SuperClaude's setup/)
7. Test installation and validation

## Documentation

See `SHANNON_V3_SPECIFICATION.md` for complete technical specification.