## Shannon Framework - Universal Installation Guide

## Overview

The universal installer (`install_universal.sh`) installs Shannon Framework for **both Claude Code and Cursor IDE**, with appropriate translations for each platform's architecture.

### Platform Support

- **Claude Code**: Full Shannon Framework with skills, commands, agents, hooks
- **Cursor IDE**: Shannon Framework translated to `.cursorrules` and global settings

### Why Universal Installation?

1. **Use Shannon in both editors** without separate installations
2. **Consistent methodology** across platforms
3. **Automatic platform detection** and appropriate configuration
4. **One command** for complete setup

---

## Installation

### Quick Start

```bash
# Install for both platforms (recommended)
./install_universal.sh

# Install for specific platform
./install_universal.sh --cursor   # Cursor IDE only
./install_universal.sh --claude   # Claude Code only
```

### Prerequisites

**For Claude Code**:
- Claude Code installed
- Serena MCP configured (MANDATORY)

**For Cursor IDE**:
- Cursor installed
- No special requirements

---

## What Gets Installed

### Claude Code Installation

```
~/.claude/
├── skills/shannon/          # 17 skills
├── commands/shannon/        # 19 commands
├── agents/shannon/          # 24 agents
├── core/shannon/            # 9 behavioral patterns
├── modes/shannon/           # 2 execution modes
├── templates/shannon/       # Templates
├── hooks/shannon/           # 5 hook scripts
└── hooks.json               # Hook configuration
```

**How it works**:
- Calls `install_local.sh` internally
- Full Shannon Framework with native hook system
- Commands available as `/shannon:*`
- Skills auto-loaded via SessionStart hook

### Cursor IDE Installation

```
~/.cursor/
├── commands/                # Shannon commands (19 files) ✨ NEW
│   ├── do.md
│   ├── spec.md
│   ├── wave.md
│   └── ... (16 more)
├── shannon/                 # Shannon framework files
│   ├── core/                # Core documentation
│   ├── skills/              # Skill reference docs
│   ├── agents/              # Agent reference docs
│   ├── .templates/          # Templates
│   └── QUICK_START.md       # Quick reference
├── .vscode/                 # ✨ NEW
│   └── tasks.json           # Shannon tasks (7 tasks)
├── global.cursorrules       # Global Shannon rules (2000+ lines)
└── ...

~/Library/Application Support/Cursor/User/  (macOS)
└── settings.json            # Cursor settings (SAFELY MERGED, not overwritten) ✅

~/.config/Cursor/User/       (Linux)
└── settings.json            # Cursor settings (SAFELY MERGED, not overwritten) ✅
```

**How it works**:
- Translates Shannon Framework to Cursor's `.cursorrules` format
- Embeds complete methodology in global rules file
- Configures Cursor Chat and Composer with Shannon prompts
- Provides reference documentation for context

---

## Cursor IDE Integration

### Global Rules File

The installer creates `~/.cursor/global.cursorrules` containing:

1. **Shannon Framework Overview** - Core principles and methodology
2. **Mandatory Workflows** - Before implementation, during implementation
3. **8D Complexity Analysis** - Complete scoring algorithm
4. **NO MOCKS Testing Philosophy** - Real component requirements
5. **Wave-Based Execution** - Parallel development patterns
6. **Code Quality Standards** - Architecture, testing, documentation, security
7. **Common Rationalizations to Avoid** - Anti-patterns and counters
8. **MCP Integration** - MCP server recommendations
9. **Project Structure** - Recommended directory layout
10. **Session Workflow** - Starting, during, ending sessions
11. **Red Flags** - Warning signs of deviation
12. **Cursor-Specific Integration** - Composer and Chat integration

### settings.json Configuration

The installer updates Cursor's `settings.json` with:

```json
{
  "cursor.shannon.enabled": true,
  "cursor.shannon.version": "5.0.0",
  "cursor.shannon.enforceNoMocks": true,
  "cursor.shannon.requireComplexityAnalysis": true,
  "cursor.shannon.waveExecutionThreshold": 0.50,

  "cursor.chat.systemPrompt": "You are an AI assistant following Shannon Framework v5.4...",
  "cursor.composer.systemPrompt": "Follow Shannon Framework v5.4..."
}
```

### Usage in Cursor

#### Starting a Session

Open Cursor Chat or Composer and request:

```
"Analyze this specification using Shannon Framework's 8D complexity scoring:

Build a task management application with:
- React frontend
- Node.js/Express backend
- PostgreSQL database
- User authentication
- Real-time updates"
```

**Expected Response**: 8D complexity breakdown, execution strategy, MCP recommendations, testing strategy

#### During Development

The AI will:
- ✅ Reference global.cursorrules automatically
- ✅ Enforce NO MOCKS testing
- ✅ Suggest wave-based execution for complexity >= 0.50
- ✅ Provide quantitative complexity scores
- ✅ Recommend functional tests with real components

#### Common Prompts

**Complexity Analysis**:
```
"Run Shannon 8D complexity analysis on: [specification]"
```

**Wave Planning**:
```
"Generate Shannon wave execution plan for this project"
```

**Test Generation**:
```
"Create functional tests (NO MOCKS) using Puppeteer for [feature]"
```

**Checkpoint**:
```
"Create Shannon checkpoint documenting current session state"
```

---

## Command Reference

### Installation

```bash
# Default: Install for both platforms
./install_universal.sh

# Explicit install for both
./install_universal.sh --both --install

# Install for Cursor only
./install_universal.sh --cursor

# Install for Claude Code only
./install_universal.sh --claude
```

### Update

```bash
# Update both platforms
./install_universal.sh --update

# Update specific platform
./install_universal.sh --cursor --update
./install_universal.sh --claude --update
```

### Uninstall

```bash
# Uninstall from both platforms
./install_universal.sh --uninstall

# Uninstall from specific platform
./install_universal.sh --cursor --uninstall
./install_universal.sh --claude --uninstall
```

### Help

```bash
./install_universal.sh --help
```

---

## Platform Detection

The installer automatically detects installed platforms:

```
Detected: Claude Code
Detected: Cursor IDE
Installation target: both
```

If only one platform is detected, the installer adjusts:

```
Detected: Cursor IDE
Claude Code not detected, installing for Cursor only
Installation target: cursor
```

---

## Verification

### Claude Code

```bash
# Start Claude Code
# In a new session:
/shannon:status

# Expected:
# Shannon Framework v5.4 active
```

### Cursor IDE

```bash
# View global rules
cat ~/.cursor/global.cursorrules

# View quick start
cat ~/.cursor/shannon/QUICK_START.md

# Start Cursor
# In Chat/Composer:
"Show me Shannon Framework version and status"

# Expected: AI references global.cursorrules and confirms Shannon v5.0
```

---

## Troubleshooting

### Claude Code Issues

See `INSTALL_LOCAL.md` for Claude Code-specific troubleshooting.

### Cursor IDE Issues

**Issue**: Global rules not being followed

**Solutions**:
1. Verify rules file exists: `ls -l ~/.cursor/global.cursorrules`
2. Check file size: `wc -l ~/.cursor/global.cursorrules` (should be 500+ lines)
3. Restart Cursor completely
4. In Chat, explicitly reference: "Following global.cursorrules, analyze..."

**Issue**: Settings not applied

**Solutions**:
1. Check settings.json location:
   - macOS: `~/Library/Application Support/Cursor/User/settings.json`
   - Linux: `~/.config/Cursor/User/settings.json`
2. Verify Shannon settings present: `grep shannon ~/Library/Application\ Support/Cursor/User/settings.json`
3. Restart Cursor

**Issue**: Reference docs not found

**Solutions**:
1. Verify installation: `ls ~/.cursor/shannon/`
2. Check quick start: `cat ~/.cursor/shannon/QUICK_START.md`
3. Re-run installer: `./install_universal.sh --cursor --update`

---

## Platform Differences

### Claude Code

**Advantages**:
- Native command system (`/shannon:spec`, `/shannon:wave`, etc.)
- Hook system (automatic SessionStart, PreCompact, PostToolUse)
- Skill discovery and invocation
- MCP integration (Serena required)

**How Shannon Works**:
- Commands invoke skills
- Skills enforce workflows
- Hooks trigger automatically
- Core files define behaviors

### Cursor IDE

**Advantages**:
- VS Code extension ecosystem
- Composer for multi-file edits
- No MCP requirement
- Works with existing Cursor features

**How Shannon Works**:
- Global rules embedded in all sessions
- AI references rules automatically
- Prompts trigger Shannon workflows
- Manual enforcement (AI-driven, not hook-driven)

### Key Difference

**Claude Code**: Shannon is **enforced** via hooks and skills
**Cursor**: Shannon is **guided** via rules and prompts

Both provide the same methodology, but enforcement mechanisms differ.

---

## Examples

### Example 1: New Project in Cursor

```
User (in Cursor Chat):
"I want to build a real-time chat application with React, Socket.io, and MongoDB.
Analyze using Shannon Framework."

AI Response:
"# Shannon Framework 8D Complexity Analysis

## Requirements Summary
Real-time chat application with React frontend, Socket.io for WebSocket
communication, MongoDB for persistence.

## 8D Complexity Breakdown

1. **Scope**: 65/100 - Multiple features (messages, rooms, users, auth, real-time)
2. **Technical Complexity**: 70/100 - WebSocket management, real-time sync, state management
3. **Integration Complexity**: 60/100 - Socket.io integration, MongoDB connection, auth service
4. **Domain Knowledge**: 40/100 - Standard web patterns, some real-time expertise needed
5. **Uncertainty**: 50/100 - Scaling considerations unclear, deployment strategy TBD
6. **Testing Complexity**: 75/100 - Real-time testing complex, multiple clients, concurrency
7. **Deployment Complexity**: 55/100 - WebSocket server, MongoDB hosting, HTTPS/WSS
8. **Documentation**: 50/100 - API docs, Socket.io events, deployment guide

**Total**: 465/800 = **0.58** (Complex)

## Domain Breakdown
- Frontend: 35%
- Backend: 40%
- Database: 20%
- DevOps: 5%

## Execution Strategy
**Complex (0.58)** - WAVE-BASED EXECUTION REQUIRED

Recommended: 4-5 waves
- Wave 1: Architecture & Design (component structure, API contracts, Socket.io events)
- Wave 2: Frontend Implementation (React components, Socket.io client integration)
- Wave 3: Backend Implementation (Express server, Socket.io server, MongoDB integration)
- Wave 4: Integration & Testing (Connect frontend/backend, functional E2E tests)
- Wave 5: Deployment & Documentation

## Testing Strategy
**NO MOCKS** - Functional tests only:
- Frontend: Puppeteer (real browser, multiple tabs for multi-user testing)
- Backend: Real MongoDB instance (Docker container)
- WebSocket: Real Socket.io connections (test with actual clients)
- Integration: Full stack E2E tests

## Recommended Tools
- Frontend Testing: Puppeteer
- Backend Testing: Jest + Real MongoDB
- Socket.io Testing: socket.io-client for test clients
- Database: Docker MongoDB container for tests

Would you like me to generate the detailed wave plan?"
```

### Example 2: Test Generation in Cursor

```
User (in Cursor Composer):
"Create functional tests for the user authentication flow. NO MOCKS."

AI Response:
"I'll create functional E2E tests using Puppeteer (real browser) and a test
MongoDB instance. Following Shannon NO MOCKS philosophy.

[Generates test file with:]
- Real browser automation via Puppeteer
- Real MongoDB test database
- Real HTTP requests to backend
- Actual form submissions and navigation
- Real JWT token validation
"
```

---

## Migration from Plugin Installation

If you previously used the plugin-only installer:

```bash
# Run universal installer
./install_universal.sh --both

# This will:
# 1. Install for Claude Code (via install_local.sh)
# 2. Install for Cursor (new)
# 3. Both platforms configured
```

---

## Updating

```bash
# Pull latest from repository
cd /path/to/shannon-framework
git pull

# Update both platforms
./install_universal.sh --update

# Or update specific platform
./install_universal.sh --cursor --update
```

---

## Uninstallation

```bash
# Remove from both platforms
./install_universal.sh --uninstall

# Or remove from specific platform
./install_universal.sh --cursor --uninstall
```

**What gets removed**:
- Claude Code: All Shannon directories, hooks.json
- Cursor: Shannon directory, global.cursorrules (backed up), settings.json (Shannon entries removed)

---

## Support

**Installation Issues**:
- Check log: `~/.shannon_install.log`
- Review this guide's Troubleshooting section

**Usage Questions (Claude Code)**:
- Commands: `~/.claude/commands/shannon/*.md`
- Skills: `~/.claude/skills/shannon/*/SKILL.md`
- Core: `~/.claude/core/shannon/*.md`

**Usage Questions (Cursor)**:
- Quick Start: `~/.cursor/shannon/QUICK_START.md`
- Global Rules: `~/.cursor/global.cursorrules`
- Core Docs: `~/.cursor/shannon/core/*.md`

**Issues**:
- GitHub: https://github.com/shannon-framework/shannon/issues

---

## License

MIT License - See LICENSE file in repository root.

---

**Shannon Framework v5.4** - Quantitative Development for Claude Code and Cursor IDE

