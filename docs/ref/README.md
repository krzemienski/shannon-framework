# Shannon Reference Documentation

This directory contains permanent reference documentation for Shannon v5.0 development.

---

## Test Specifications (4 files)

**Applications Shannon will build and verify:**

1. **prd-creator-spec.md** (18KB) - Web app: React + FastAPI + PostgreSQL
2. **claude-code-expo-spec.md** (81KB) - Mobile app: React Native + Express + WebSocket
3. **repo-nexus-spec.md** (87KB) - Full-stack iOS: React Native + FastAPI + PostgreSQL + Redis
4. **shannon-cli-spec.md** (153KB) - CLI tool: Python + Click + Claude SDK (meta-circular)

---

## Claude Agent SDK Documentation (12 files)

**Complete Python SDK reference:**

1. **agent-sdk-overview.md** - SDK purpose, installation, core concepts
2. **agent-sdk-python-api-reference.md** - Complete Python API (1847 lines)
3. **agent-sdk-plugins.md** - Loading plugins programmatically
4. **agent-sdk-skills.md** - Using Skills via SDK (**setting_sources required!**)
5. **agent-sdk-slash-commands.md** - Slash command integration
6. **agent-sdk-streaming-vs-single.md** - Input modes explained
7. **agent-sdk-mcp.md** - MCP server configuration
8. **agent-sdk-subagents.md** - Programmatic agent definition
9. **agent-sdk-custom-tools.md** - Creating in-process MCP tools
10. **agent-sdk-sessions.md** - Session management and resumption
11. **agent-sdk-modifying-prompts.md** - System prompt customization
12. **agent-sdk-todo-tracking.md** - Todo system integration

---

## Claude Code CLI Documentation (3 files)

**Interactive Claude Code reference:**

1. **claude-code-cli-plugins.md** - Plugin installation and management
2. **claude-code-cli-skills.md** - Skills in Claude Code CLI
3. **claude-code-cli-slash-commands.md** - Slash commands in Claude Code CLI

---

## Additional Reference Files

**Claude Code llms.txt:**
- claude-code-llms.txt (48 lines) - Curated docs list
- claude-code-llms-full.txt (13,628 lines) - Complete Claude Code documentation

---

## Usage

**During Development:**
- Reference these docs instead of re-fetching
- Verify patterns against official documentation
- Check API changes in python-api-reference.md

**For SDK Testing:**
- agent-sdk-plugins.md - How plugins load
- agent-sdk-skills.md - **CRITICAL**: setting_sources requirement
- agent-sdk-python-api-reference.md - Complete message types

**For Shannon Testing:**
- All 4 spec files for building test applications
- agent-sdk-overview.md for SDK setup

---

**Total**: 21 files (4 specs + 12 SDK docs + 3 CLI docs + 2 llms.txt)
**Purpose**: Offline reference, prevent documentation drift, verify patterns
