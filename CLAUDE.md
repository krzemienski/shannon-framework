# Shannon Framework - Installation Guide

**This is the Shannon Framework repository.**

**Current Version**: Shannon v5.6.0 "Comprehensive Quality & Intelligence"

**Latest Release Highlights**:
- ✅ 14 new skills (testing, security, architecture, coordination)
- ✅ `/shannon:health` command for real-time health dashboard
- ✅ Auto-activation hook for large files/prompts
- ✅ Advanced testing: mutation, performance regression, anti-patterns
- ✅ Security automation: vulnerability detection, compliance
- See: `docs/v5.6/CHANGELOG.md` for complete details

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
- **[Shannon Plugin README](README.md)** - Complete guide
- Commands, agents, skills, examples
- Installation, configuration, troubleshooting

### Quick Start

```bash
# Verify installation
/shannon:status

# Analyze a specification
/shannon:spec "Build a web app with React and Node.js"

# Prime a session (V4.1)
/shannon:prime

# Discover skills (V4.1)
/shannon:discover_skills
```

---

## For Shannon Developers

Working on Shannon Framework itself? You're in the right place.

### Plugin Source

**Location**: root directory
- Commands: `commands/` (14 commands: 13 sh_* + 1 shannon_prime)
- Agents: `agents/` (24 agents)
- Skills: `skills/` (17 skills)
- Core: `core/` (9 behavioral patterns)
- Hooks: `hooks/`

### Testing Locally (Interactive)

```bash
# In Claude Code:
/plugin marketplace add /path/to/shannon-framework
/plugin uninstall shannon@shannon-framework  # If already installed
/plugin install shannon@shannon-framework

# Restart Claude Code

# Test your changes
/shannon:status
/shannon:shannon_prime
```

### Testing via SDK (Programmatic)

**CRITICAL**: Shannon plugin must be INSTALLED to work with Python SDK.

```bash
# Step 1: Create marketplace.json at repo root (.claude-plugin/marketplace.json)
# Step 2: Add marketplace
claude plugin marketplace add /path/to/shannon-framework

# Step 3: Install plugin
claude plugin install shannon@shannon-framework

# Step 4: Restart Claude Code (if running)
```

**Then in Python:**
```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    setting_sources=["user", "project"],  # REQUIRED!
    permission_mode="bypassPermissions",
    allowed_tools=["Skill"]
)

# Use namespaced commands
async for message in query(
    prompt="/shannon:spec \"specification text\"",
    options=options
):
    print(message)
```

**Key requirements:**
- `setting_sources=["user", "project"]` required for plugin loading
- Commands are namespaced: `/shannon:spec` (not `/shannon:spec`)
- Plugin must be installed via marketplace (cannot load from local path directly)

### Development Workflow

1. **Edit Files**: Make changes in root directory
2. **Test Locally**: Install plugin from local path
3. **Validate**: Test commands and skills
4. **Commit**: Follow conventional commit format
5. **PR**: Submit for review

---

## Version

**Current**: v5.6.0

**V5.6 Enhancements**:
- ✅ 14 new skills (testing, security, architecture, coordination)
- ✅ `/shannon:health` command for real-time health dashboard
- ✅ Auto-activation hook for large files/prompts
- ✅ Advanced testing: mutation, performance regression, anti-patterns
- ✅ Security automation: vulnerability detection, compliance

**Previous V4.1 Enhancements**:
- 🔴 Forced Complete Reading Protocol
- 🔴 Automatic Skill Discovery & Invocation
- 🔴 Unified /shannon:prime Command

**See**: [SHANNON_V4.1_FINAL_SUMMARY.md](SHANNON_V4.1_FINAL_SUMMARY.md) for details

---

**Install Shannon**: `/plugin install shannon@shannon-framework`
**Documentation**: [README.md](README.md)
