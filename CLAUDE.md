# Shannon Framework - Installation Guide

**This is the Shannon Framework repository.**

For Shannon users: **Install via plugin system** (recommended)
For Shannon developers: This directory contains plugin source code

---

## For Shannon Users

### Installation

```bash
# In Claude Code:
/plugin marketplace add shannon-framework/shannon
/plugin install shannon@shannon-framework

# Restart Claude Code
```

### Documentation

Complete documentation is in the plugin:
- **[Shannon Plugin README](shannon-plugin/README.md)** - Complete guide
- Commands, agents, skills, examples
- Installation, configuration, troubleshooting

### Quick Start

```bash
# Verify installation
/sh_status

# Analyze a specification
/sh_spec "Build a web app with React and Node.js"

# Prime a session (V4.1)
/shannon:prime

# Discover skills (V4.1)
/sh_discover_skills
```

---

## For Shannon Developers

Working on Shannon Framework itself? You're in the right place.

### Plugin Source

**Location**: `shannon-plugin/`
- Commands: `shannon-plugin/commands/` (48 commands)
- Agents: `shannon-plugin/agents/` (26 agents)
- Skills: `shannon-plugin/skills/` (20 skills)
- Core: `shannon-plugin/core/` (9 behavioral patterns)
- Hooks: `shannon-plugin/hooks/`

### Testing Locally

```bash
# In Claude Code:
/plugin marketplace add /path/to/shannon-framework
/plugin uninstall shannon@shannon  # If already installed
/plugin install shannon@shannon

# Restart Claude Code

# Test your changes
/sh_status
/shannon:prime
```

### Development Workflow

1. **Edit Files**: Make changes in `shannon-plugin/`
2. **Test Locally**: Install plugin from local path
3. **Validate**: Test commands and skills
4. **Commit**: Follow conventional commit format
5. **PR**: Submit for review

---

## Version

**Current**: v4.1.0

**V4.1 Enhancements**:
- 🔴 Forced Complete Reading Protocol
- 🔴 Automatic Skill Discovery & Invocation
- 🔴 Unified /shannon:prime Command

**See**: [SHANNON_V4.1_FINAL_SUMMARY.md](SHANNON_V4.1_FINAL_SUMMARY.md) for details

---

**Install Shannon**: `/plugin install shannon@shannon-framework`
**Documentation**: [shannon-plugin/README.md](shannon-plugin/README.md)
