# Shannon CLI V3.0 - User Guide

**Version**: 3.0.0 | **Status**: Production Ready | **Date**: 2025-11-14

> Complete guide to Shannon CLI V3.0 - Intelligent AI development orchestration with live metrics, smart caching, and cost optimization.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Core Concepts](#core-concepts)
4. [Commands Reference](#commands-reference)
5. [Common Workflows](#common-workflows)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

---

## Introduction

### What is Shannon CLI V3.0?

Shannon CLI V3.0 is a production-grade AI development platform that extends Shannon Framework with intelligent orchestration, real-time monitoring, and cost optimization capabilities.

**Key Improvements Over V2**:
- Live metrics dashboard with 4 Hz refresh rate
- 3-tier intelligent caching (50-80% cost savings)
- Automatic MCP detection and installation
- Agent state tracking with pause/resume
- Smart model selection and budget enforcement
- Historical analytics database
- Context management for existing codebases
- Real-time cost tracking and optimization

**Architecture Overview**:
```
Shannon CLI V3 (9,902 lines)
    ↓
ContextAwareOrchestrator (integration hub)
    ├─ Metrics Dashboard (live monitoring)
    ├─ Cache Manager (3-tier caching)
    ├─ MCP Manager (auto-installation)
    ├─ Agent Tracker (state management)
    ├─ Cost Optimizer (model selection)
    ├─ Analytics (SQLite database)
    └─ Context Manager (onboarding system)
    ↓
Claude Agent SDK
    ↓
Shannon Framework Plugin
```

---

## Getting Started

### Prerequisites

- **Python**: 3.10 or higher
- **Claude Agent SDK**: Latest version
- **Terminal**: Modern terminal with Unicode support (recommended)
- **Operating System**: macOS, Linux, or Windows with WSL2

### Installation

#### Quick Install (Recommended)

```bash
# 1. Install Shannon CLI
pip install shannon-cli

# 2. Run interactive setup wizard
shannon setup

# The wizard will:
#   ✓ Check Python 3.10+
#   ✓ Install Claude Agent SDK if needed
#   ✓ Locate or install Shannon Framework
#   ✓ Install recommended MCPs (Serena, Filesystem, etc.)
#   ✓ Verify configuration
#   ✓ Test integration with live metrics

# 3. Verify installation
shannon --version
# Shannon CLI v3.0.0

shannon diagnostics
# ✅ All systems operational
# ✅ 7 MCPs installed and verified
# ✅ Context system ready
# ✅ Cache initialized
```

#### Manual Setup

```bash
# Prerequisites
pip install claude-agent-sdk

# Install Shannon Framework plugin in Claude Code
# /plugin marketplace add shannon-framework/shannon
# /plugin install shannon@shannon-framework

# Set framework path (optional - auto-detected)
export SHANNON_FRAMEWORK_PATH="$HOME/.claude/plugins/shannon"

# Run diagnostics
shannon diagnostics
```

### First Steps

#### 1. Your First Analysis

```bash
# Create a simple specification
cat > spec.md << 'EOF'
# Task: Build Authentication System

## Requirements
- User registration with email validation
- Login with JWT tokens
- Password reset functionality
- Session management

## Success Criteria
- All endpoints tested
- Security best practices followed
- Documentation complete
EOF

# Run analysis with live metrics
shannon analyze spec.md

# Output:
# 🎯 Complexity Analysis
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Overall Complexity: 0.35 (Medium)
# Implementation Time: ~4.2 hours
# Recommended Approach: Wave-based (2 waves)
#
# 💰 Cost Estimate: $2.40
# 📊 Cache: MISS (saved for future)
# 🔧 MCPs Recommended: 3 auto-installed
```

#### 2. Execute with Wave Orchestration

```bash
# Execute implementation
shannon wave "Build authentication system"

# Live dashboard displays:
# - Real-time progress (4 Hz refresh)
# - Current tokens/cost
# - Streaming output
# - Wave status
# - Keyboard controls (Enter=expand, q=quit, p=pause)
```

#### 3. Check Session Status

```bash
# View current session
shannon status

# Output shows:
# - Complexity analysis results
# - Completed waves
# - Total cost
# - Cache hit rate
# - Context loaded
```

---

## Core Concepts

### Sessions

A session represents a complete development task from analysis to implementation.

**Session Lifecycle**:
```
1. Create:  shannon analyze spec.md
2. Execute: shannon wave "request"
3. Monitor: shannon status
4. Save:    shannon checkpoint "milestone"
5. Resume:  shannon restore checkpoint_id
```

**Session Storage**:
```
~/.shannon/
├── sessions/
│   ├── {session-id}/
│   │   ├── spec.json           # Analysis results
│   │   ├── waves/              # Wave execution logs
│   │   ├── checkpoints/        # Saved states
│   │   └── context/            # Loaded context
├── cache/                      # 3-tier cache
├── analytics.db                # Historical database
└── config.json                 # Configuration
```

### Context Management

V3 introduces 3-tier context architecture for working with existing codebases.

**Tiers**:
- **Hot** (Memory): Instant, session-only, current state
- **Warm** (Local Files): ~100ms, permanent, local index
- **Cold** (Serena MCP): ~500ms, permanent, searchable knowledge graph

**Context Workflow**:
```bash
# 1. Onboard new project (one-time)
shannon onboard /path/to/project --project-id my-app

# Creates context index:
# - File tree structure
# - Dependency analysis
# - Architecture detection
# - Testing patterns
# - Documentation index

# 2. Prime context for session (fast reload)
shannon prime --project-id my-app

# Loads:
# - Recent changes (git diff)
# - Critical files
# - Test patterns
# - Dependencies

# 3. Update context (after changes)
shannon update --project-id my-app

# Incremental update:
# - New/modified files
# - Dependency changes
# - Test updates
```

### Live Metrics Dashboard

Real-time monitoring of SDK execution with 4 Hz refresh rate.

**Dashboard Modes**:

**Compact (default)**:
```
[████████████░░░░░░░░] 60% | Tokens: 12.5K | Cost: $0.24 | ETA: 2m 15s
Wave 2/3: Implementing auth endpoints | Enter=expand q=quit p=pause
```

**Detailed (press Enter)**:
```
┌─────────────────────────────────────────────────────────────┐
│ SHANNON LIVE DASHBOARD                                      │
├─────────────────────────────────────────────────────────────┤
│ Progress: [████████████░░░░░░░░] 60%                       │
│                                                             │
│ Metrics:                                                    │
│   Input Tokens:  8,450                                      │
│   Output Tokens: 4,120                                      │
│   Total Cost:    $0.24                                      │
│   Model:         claude-sonnet-4                            │
│   Time Elapsed:  3m 42s                                     │
│   ETA:           2m 15s                                     │
│                                                             │
│ Wave Status:                                                │
│   Current: Wave 2 of 3 - Implementing auth endpoints       │
│   Agent: BACKEND                                            │
│   Status: 🟢 Active                                         │
│                                                             │
│ Recent Output:                                              │
│   Creating JWT token generation...                         │
│   Implementing password hashing with bcrypt...              │
│   Writing endpoint tests...                                 │
│                                                             │
│ Controls: Enter=collapse Esc/q=quit p=pause                 │
└─────────────────────────────────────────────────────────────┘
```

**Keyboard Controls**:
- **Enter**: Toggle compact/detailed view
- **Esc/q**: Quit (with confirmation)
- **p**: Pause execution
- **r**: Resume execution

### Caching System

3-tier caching provides 50-80% cost savings through intelligent result reuse.

**Tier 1: Analysis Cache**
- Caches complexity analysis results
- Key: SHA-256(spec + framework_version + model + context_hash)
- TTL: 7 days
- Location: `~/.shannon/cache/analyses/`

**Tier 2: Command Cache**
- Caches stable commands (prime, discover-skills)
- Key: `{command}_{framework_version}`
- TTL: 30 days
- Location: `~/.shannon/cache/commands/`

**Tier 3: MCP Recommendation Cache**
- Caches MCP recommendations by domain signature
- Key: Domain fingerprint (deterministic)
- TTL: 90 days
- Location: `~/.shannon/cache/mcps/`

**Cache Management**:
```bash
# View cache statistics
shannon cache stats
# Hit Rate: 72%
# Total Savings: $45.80
# Entries: 127
# Size: 12.4 MB

# Clear all caches
shannon cache clear

# Clear specific tier
shannon cache clear --tier analysis
```

### MCP Auto-Installation

V3 automatically detects required MCPs and installs them.

**Recommended MCPs (7)**:
1. **Serena** - Context knowledge graph
2. **Filesystem** - File operations
3. **Git** - Version control
4. **Memory** - Shared agent memory
5. **Browser** - Web research
6. **Postgres** - Database operations
7. **Sequential-thinking** - Complex reasoning

**Auto-Installation Flow**:
```
1. Analyze spec → Detect required domains
2. Map domains → MCP recommendations
3. Check installed → Identify missing
4. Install missing → With verification
5. Verify working → Health checks
```

**Manual MCP Management**:
```bash
# Check MCP status
shannon check-mcps

# Install specific MCP
shannon mcp install serena

# Verify MCP
shannon mcp verify serena

# List all MCPs
shannon mcp list
```

### Cost Optimization

Smart model selection and budget enforcement reduce costs by 30-50%.

**Model Selection**:
```python
# Automatic based on complexity
complexity < 0.30  → claude-haiku-4     ($0.25/M tokens)
complexity < 0.60  → claude-sonnet-4    ($3.00/M tokens)
complexity >= 0.60 → claude-opus-4      ($15.00/M tokens)

# Manual override
shannon analyze spec.md --model claude-haiku-4
```

**Budget Enforcement**:
```bash
# Set budget limit
shannon config set budget.max_tokens 100000

# Pre-wave budget check
shannon wave "request"
# ⚠️  Estimated cost: $4.50 (75% of remaining budget)
# Continue? [y/N]

# Pause on budget exhaustion
# Dashboard shows: ⚠️  Budget 95% consumed - execution paused
```

**Cost Tracking**:
```bash
# View session costs
shannon status --verbose

# View analytics
shannon analytics costs --last 30d
# Total: $127.40
# Avg per session: $3.18
# Cache savings: $45.80 (36%)
```

---

## Commands Reference

### Core Commands

#### shannon setup

Interactive setup wizard for first-time configuration.

```bash
shannon setup

# Wizard steps:
# 1. Python version check (3.10+)
# 2. Claude Agent SDK installation
# 3. Shannon Framework detection/installation
# 4. MCP installation (7 recommended)
# 5. Configuration verification
# 6. Integration test with live metrics
```

**Options**: None (fully interactive)

**When to Use**:
- First-time installation
- After framework updates
- Troubleshooting configuration issues
- Adding new MCP servers

---

#### shannon analyze [SPEC_FILE]

Perform 8D complexity analysis on specification.

```bash
# Basic usage
shannon analyze spec.md

# With project context
shannon analyze spec.md --project-id my-app

# JSON output for automation
shannon analyze spec.md --json

# Specify session ID
shannon analyze spec.md --session-id abc123

# Force model selection
shannon analyze spec.md --model claude-opus-4

# Skip cache
shannon analyze spec.md --no-cache
```

**Arguments**:
- `SPEC_FILE`: Path to specification file (Markdown, text)

**Options**:
- `--json`: Output in JSON format
- `--session-id ID`: Use specific session ID
- `--project-id ID`: Load project context
- `--model MODEL`: Override model selection
- `--no-cache`: Skip cache lookup
- `--verbose, -v`: Detailed output

**Output**:
```
🎯 Complexity Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall Complexity: 0.35 (Medium)

Dimension Scores:
├─ Scope:         0.30 (Narrow)
├─ Algorithms:    0.40 (Standard)
├─ Integration:   0.35 (Few systems)
├─ State:         0.45 (Moderate)
├─ Constraints:   0.25 (Relaxed)
├─ Ambiguity:     0.30 (Clear)
├─ Tech Maturity: 0.20 (Mature)
└─ Risk:          0.35 (Moderate)

Domain Analysis:
├─ Backend:    45%
├─ Frontend:   25%
├─ Database:   20%
└─ DevOps:     10%

Recommendations:
├─ Waves:          2 waves recommended
├─ Time Estimate:  ~4.2 hours
├─ Model:          claude-sonnet-4
├─ Cost Estimate:  $2.40

MCPs Auto-Installed:
├─ ✓ filesystem (file operations)
├─ ✓ postgres (database)
└─ ✓ git (version control)

Cache: MISS → Saved for future reuse
Context: Loaded from my-app (142 files)
```

**Caching Behavior**:
- Cache key includes spec content, framework version, model, context hash
- 7-day TTL
- Cache HIT saves ~$0.50-2.00 per analysis
- Context changes invalidate cache

---

#### shannon wave [REQUEST]

Execute wave-based implementation with live monitoring.

```bash
# Basic usage
shannon wave "Build authentication system"

# Resume existing session
shannon wave "Add password reset" --session-id abc123

# With project context
shannon wave "Refactor user service" --project-id my-app

# Verbose mode
shannon wave "Add tests" --verbose

# Auto mode (no keyboard interaction)
shannon wave "Deploy to production" --auto
```

**Arguments**:
- `REQUEST`: Implementation request (quoted string)

**Options**:
- `--session-id ID`: Resume specific session
- `--project-id ID`: Load project context
- `--auto`: Non-interactive mode (no keyboard controls)
- `--verbose, -v`: Detailed logging
- `--max-waves N`: Limit wave count

**Live Dashboard**:
During execution, live dashboard displays:
- Real-time progress bar
- Current tokens and cost
- Streaming output (last 20 lines)
- Wave status and agent info
- Keyboard controls

**Keyboard Controls**:
- `Enter`: Toggle compact/detailed view
- `Esc` or `q`: Quit with confirmation
- `p`: Pause execution
- `r`: Resume execution

**Agent Tracking**:
Wave execution automatically tracks:
- Agent spawns and terminations
- Current agent state
- Message routing
- Error recovery

---

#### shannon task [SPEC_OR_FILE]

Complete workflow: analyze + implement in one command.

```bash
# From specification file
shannon task spec.md

# From inline specification
shannon task "Build REST API for user management"

# Auto mode (no pauses)
shannon task spec.md --auto

# With project context
shannon task spec.md --project-id my-app

# Specify session
shannon task spec.md --session-id abc123
```

**Arguments**:
- `SPEC_OR_FILE`: Specification file path or inline text

**Options**:
- `--auto`: Run without pauses
- `--session-id ID`: Use specific session
- `--project-id ID`: Load project context
- `--verbose, -v`: Detailed output

**Workflow**:
```
1. Analyze specification
   ↓
2. Display complexity analysis
   ↓
3. Show wave plan
   ↓
4. Wait for confirmation (unless --auto)
   ↓
5. Execute waves with live monitoring
   ↓
6. Display completion summary
```

---

#### shannon status

Show current session status and progress.

```bash
# Latest session
shannon status

# Specific session
shannon status --session-id abc123

# Detailed view
shannon status --verbose

# JSON output
shannon status --json
```

**Options**:
- `--session-id ID`: View specific session
- `--verbose, -v`: Include all details
- `--json`: JSON format output

**Output**:
```
📊 Session Status: abc123
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Created: 2025-11-14 10:30:45
Project: my-app (context loaded)

Complexity Analysis:
├─ Overall: 0.35 (Medium)
├─ Waves: 2 planned
└─ Estimate: ~4.2 hours, $2.40

Wave Progress:
├─ Wave 1: ✓ Complete (45m, $1.20)
│   └─ BACKEND: Auth endpoints
└─ Wave 2: 🔄 In Progress (12m, $0.45)
    └─ QA: Test coverage

Metrics:
├─ Total Tokens: 45,200
├─ Total Cost: $1.65
├─ Cache Hits: 3/5 (60%)
└─ Context: 142 files loaded

Next Steps:
└─ Complete Wave 2 testing
```

---

#### shannon config

Display or edit configuration.

```bash
# Show current config
shannon config

# Show detailed config
shannon config --verbose

# Edit config file
shannon config --edit

# Set specific value
shannon config set log_level DEBUG

# Get specific value
shannon config get cache.max_size_mb
```

**Options**:
- `--edit`: Open config in default editor
- `--verbose, -v`: Show all settings
- `--json`: JSON format output

**Configuration File**: `~/.shannon/config.json`

**Key Settings**:
```json
{
  "log_level": "INFO",
  "session_dir": "~/.shannon/sessions",
  "cache": {
    "enabled": true,
    "max_size_mb": 500,
    "analysis_ttl_days": 7,
    "command_ttl_days": 30,
    "mcp_ttl_days": 90
  },
  "metrics": {
    "enabled": true,
    "refresh_rate_hz": 4,
    "compact_by_default": true
  },
  "budget": {
    "max_tokens": 1000000,
    "warn_threshold": 0.80,
    "pause_threshold": 0.95
  },
  "context": {
    "auto_onboard": true,
    "max_files": 1000,
    "exclude_patterns": [".git", "node_modules"]
  }
}
```

---

### Session Management Commands

#### shannon sessions

List all available sessions.

```bash
# List all sessions
shannon sessions

# JSON output
shannon sessions --json
```

**Output**:
```
📋 Sessions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ID       Created              Project   Status    Waves  Cost
abc123   2025-11-14 10:30     my-app    Complete  2/2    $2.40
def456   2025-11-14 14:15     website   Active    1/3    $1.20
ghi789   2025-11-13 09:00     api       Complete  4/4    $5.60

Total: 3 sessions
```

---

#### shannon checkpoint [NAME]

Create checkpoint of current session state.

```bash
# Create checkpoint
shannon checkpoint "before-refactor"

# Create with description
shannon checkpoint "auth-complete" --message "All auth endpoints working"

# List checkpoints
shannon checkpoint --list

# List for specific session
shannon checkpoint --list --session-id abc123
```

**Arguments**:
- `NAME`: Checkpoint name (optional, auto-generated if not provided)

**Options**:
- `--list`: List all checkpoints
- `--session-id ID`: Session to checkpoint
- `--message MSG`: Checkpoint description
- `--verbose, -v`: Detailed output

**Output**:
```
✓ Checkpoint created: before-refactor
ID: cp_abc123_1699887045
Session: abc123
Size: 2.4 MB
Includes:
├─ Session state
├─ Wave history
├─ Context snapshot
└─ Cache state
```

---

#### shannon restore [CHECKPOINT_ID]

Restore session from checkpoint.

```bash
# Restore checkpoint
shannon restore cp_abc123_1699887045

# Restore with verification
shannon restore cp_abc123_1699887045 --verify

# Preview before restore
shannon restore cp_abc123_1699887045 --dry-run
```

**Arguments**:
- `CHECKPOINT_ID`: Checkpoint identifier

**Options**:
- `--session-id ID`: Target session
- `--verify`: Verify checkpoint integrity
- `--dry-run`: Preview without restoring
- `--verbose, -v`: Detailed output

**Restore Process**:
```
1. Verify checkpoint integrity
2. Backup current session state
3. Restore session state
4. Restore wave history
5. Restore context snapshot
6. Verify restoration success
```

---

### Context Management Commands

#### shannon onboard [PROJECT_PATH]

Onboard existing codebase into context system.

```bash
# Onboard project
shannon onboard /path/to/project --project-id my-app

# Onboard with custom settings
shannon onboard /path/to/project \
  --project-id my-app \
  --exclude "*.log" \
  --max-files 2000

# Auto-detect project ID
shannon onboard /path/to/project --auto-id
```

**Arguments**:
- `PROJECT_PATH`: Path to project directory

**Options**:
- `--project-id ID`: Project identifier (required unless --auto-id)
- `--auto-id`: Auto-generate ID from directory name
- `--exclude PATTERN`: Additional exclusion patterns
- `--max-files N`: Maximum files to index
- `--verbose, -v`: Detailed progress

**Onboarding Process**:
```
1. Scan project structure
   ↓
2. Build file tree index
   ↓
3. Analyze dependencies (package.json, requirements.txt, etc.)
   ↓
4. Detect architecture patterns
   ↓
5. Index tests and documentation
   ↓
6. Store in Serena MCP (if available)
   ↓
7. Create local cache
```

**Output**:
```
🔍 Onboarding: my-app
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scanning: /path/to/project
Files indexed: 142
Directories: 28
Total size: 2.4 MB

Analysis:
├─ Language: TypeScript (85%)
├─ Framework: Next.js 14
├─ Test framework: Jest
├─ Build tool: Turbo
└─ Dependencies: 45 packages

Architecture:
├─ Pattern: Monorepo
├─ Structure: Feature-based
└─ API: REST + GraphQL

Context stored:
├─ Hot cache: Ready
├─ Warm cache: ~/.shannon/context/my-app/
└─ Cold storage: Serena MCP

✓ Onboarding complete (12.3s)
```

---

#### shannon prime

Load context for fast session initialization.

```bash
# Prime latest project
shannon prime

# Prime specific project
shannon prime --project-id my-app

# Skip file content loading (structure only)
shannon prime --project-id my-app --structure-only

# Force full reload
shannon prime --project-id my-app --force
```

**Options**:
- `--project-id ID`: Project to prime
- `--structure-only`: Load structure only (faster)
- `--force`: Force full reload
- `--verbose, -v`: Detailed output

**Priming Loads**:
```
1. Recent changes (git diff since last session)
2. Critical files (main entry points, configs)
3. Test patterns
4. Dependency updates
5. Architecture overview
```

**Performance**:
- Warm cache: <500ms
- Cold cache: <2s
- Structure-only: <100ms

---

#### shannon update

Update project context after changes.

```bash
# Update latest project
shannon update

# Update specific project
shannon update --project-id my-app

# Force full reindex
shannon update --project-id my-app --force

# Update with git diff
shannon update --project-id my-app --since HEAD~5
```

**Options**:
- `--project-id ID`: Project to update
- `--force`: Full reindex
- `--since REF`: Git reference for diff
- `--verbose, -v`: Detailed output

**Update Process**:
```
Incremental update:
1. Detect changed files (git diff)
2. Update file index
3. Refresh dependencies (if package files changed)
4. Update architecture (if structure changed)
5. Sync to Serena MCP
```

---

### Quality Commands

#### shannon test

Run functional tests with NO MOCKS enforcement.

```bash
# Run all tests
shannon test

# Run for specific session
shannon test --session-id abc123

# Verbose output
shannon test --verbose
```

**Options**:
- `--session-id ID`: Session to test
- `--verbose, -v`: Detailed output

**Maps to**: `/shannon:test` command in Shannon Framework

**NO MOCKS Policy**:
- All tests use real components
- Real file system
- Real database (test instance)
- Real API calls (test endpoints)
- No mocking frameworks allowed

---

#### shannon reflect

Pre-completion gap analysis.

```bash
# Run reflection
shannon reflect

# For specific session
shannon reflect --session-id abc123

# Verbose output
shannon reflect --verbose
```

**Options**:
- `--session-id ID`: Session to reflect on
- `--verbose, -v`: Detailed output

**Maps to**: `/shannon:reflect` command

**Reflection Checks**:
```
1. Missing tests
2. Incomplete implementations
3. Undocumented code
4. Untested edge cases
5. Missing error handling
6. Incomplete documentation
```

**Output**:
```
🔍 Pre-Completion Reflection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Gaps Identified:

⚠️  Testing (2 gaps):
├─ Missing: Password reset flow test
└─ Missing: Token expiration test

⚠️  Error Handling (1 gap):
└─ Missing: Database connection error handling

✓ Documentation: Complete
✓ Implementation: Complete
✓ Edge Cases: Covered

Recommendation: Address gaps before claiming completion
```

---

### MCP Commands

#### shannon check-mcps

Verify MCP configuration and health.

```bash
# Check all MCPs
shannon check-mcps

# Check specific MCP
shannon check-mcps --mcp serena

# JSON output
shannon check-mcps --json
```

**Options**:
- `--mcp NAME`: Check specific MCP
- `--json`: JSON format output
- `--verbose, -v`: Detailed health checks

**Output**:
```
🔌 MCP Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MCP              Status    Version   Health
serena           ✓ Active  2.1.0     ✓ Healthy
filesystem       ✓ Active  1.5.0     ✓ Healthy
git              ✓ Active  1.2.0     ✓ Healthy
memory           ✓ Active  1.0.0     ✓ Healthy
browser          ⚠️  Error  1.3.0     ✗ Connection failed
postgres         ✗ Missing -         -
sequential       ✓ Active  1.1.0     ✓ Healthy

Summary:
├─ Active: 5/7
├─ Issues: 2
└─ Recommended: Install postgres, fix browser
```

---

#### shannon mcp install [MCP_NAME]

Install specific MCP server.

```bash
# Install MCP
shannon mcp install serena

# Install with auto-verify
shannon mcp install serena --verify

# Install all recommended
shannon mcp install --recommended
```

**Arguments**:
- `MCP_NAME`: MCP server name

**Options**:
- `--verify`: Verify after installation
- `--recommended`: Install all 7 recommended MCPs
- `--force`: Reinstall if exists

---

#### shannon mcp verify [MCP_NAME]

Verify MCP is working correctly.

```bash
# Verify specific MCP
shannon mcp verify serena

# Verify all
shannon mcp verify --all

# Deep health check
shannon mcp verify serena --deep
```

**Arguments**:
- `MCP_NAME`: MCP to verify

**Options**:
- `--all`: Verify all installed MCPs
- `--deep`: Deep health check
- `--verbose, -v`: Detailed output

---

### Skill Discovery Commands

#### shannon discover-skills

Discover available Shannon Framework skills.

```bash
# Discover all skills
shannon discover-skills

# Use cached results
shannon discover-skills --cache

# JSON output
shannon discover-skills --json
```

**Options**:
- `--cache`: Use cached skill list
- `--json`: JSON format output

**Output**:
```
📚 Available Skills (18 total)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Core Skills:
├─ spec-analysis: 8D complexity analysis
├─ wave-orchestration: Parallel wave execution
├─ agent-coordination: Multi-agent messaging
└─ functional-testing: NO MOCKS test generation

Domain Skills:
├─ backend-development: API implementation
├─ frontend-development: UI implementation
├─ database-design: Schema and queries
└─ devops-automation: CI/CD pipelines

Quality Skills:
├─ code-review: Automated review
├─ security-audit: Security analysis
└─ performance-optimization: Performance tuning

Documentation Skills:
├─ api-documentation: OpenAPI/Swagger
├─ user-guides: End-user documentation
└─ architecture-docs: System design docs
```

---

#### shannon scaffold

Generate Shannon-optimized project structure.

```bash
# Create scaffold in current directory
shannon scaffold

# Specify output directory
shannon scaffold --output ./new-project

# Use template
shannon scaffold --template api
```

**Options**:
- `--output DIR`: Output directory
- `--template NAME`: Use specific template
- `--verbose, -v`: Detailed output

**Generated Structure**:
```
project/
├── src/
│   ├── main/
│   └── test/           # Functional test structure
├── tests/
│   ├── functional/     # NO MOCKS tests
│   └── integration/
├── docs/
│   ├── api/
│   └── architecture/
├── shannon.json        # Shannon configuration
└── .shannon/           # Local session storage
```

---

### Goal Management Commands

#### shannon goal [GOAL_TEXT]

Set or view North Star goal.

```bash
# View current goal
shannon goal --show

# Set new goal
shannon goal "Build production-ready authentication system"

# Update goal
shannon goal "Build and deploy authentication system"

# Clear goal
shannon goal --clear
```

**Arguments**:
- `GOAL_TEXT`: Goal description (optional)

**Options**:
- `--show`: Display current goal
- `--clear`: Clear current goal
- `--verbose, -v`: Show goal history

**Purpose**:
The North Star goal guides all implementation decisions and keeps agents aligned.

---

#### shannon memory [PATTERN]

Track and analyze memory coordination patterns.

```bash
# View all memory
shannon memory

# Search pattern
shannon memory "auth"

# Show coordination graph
shannon memory --graph

# Export memory
shannon memory --export memory.json
```

**Arguments**:
- `PATTERN`: Search pattern (optional)

**Options**:
- `--graph`: Show coordination graph
- `--export FILE`: Export to file
- `--verbose, -v`: Detailed view

---

### Cache Commands

#### shannon cache stats

Display cache statistics.

```bash
# View cache stats
shannon cache stats

# Detailed stats
shannon cache stats --verbose

# JSON output
shannon cache stats --json
```

**Output**:
```
📊 Cache Statistics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall:
├─ Hit Rate: 72%
├─ Total Hits: 127
├─ Total Misses: 49
├─ Total Savings: $45.80
└─ Storage: 12.4 MB / 500 MB

By Tier:
├─ Analysis Cache:
│   ├─ Entries: 89
│   ├─ Hit Rate: 68%
│   ├─ Savings: $38.20
│   └─ Avg TTL: 4.2 days
├─ Command Cache:
│   ├─ Entries: 12
│   ├─ Hit Rate: 85%
│   ├─ Savings: $6.40
│   └─ Avg TTL: 18 days
└─ MCP Cache:
    ├─ Entries: 26
    ├─ Hit Rate: 92%
    ├─ Savings: $1.20
    └─ Avg TTL: 45 days

Recent Activity:
├─ Last hit: 2m ago (analysis)
├─ Last miss: 15m ago (analysis)
└─ Last eviction: 3d ago (LRU)
```

---

#### shannon cache clear

Clear cache entries.

```bash
# Clear all caches
shannon cache clear

# Clear specific tier
shannon cache clear --tier analysis

# Clear expired only
shannon cache clear --expired-only

# Clear with confirmation
shannon cache clear --confirm
```

**Options**:
- `--tier TIER`: Clear specific tier (analysis, command, mcp)
- `--expired-only`: Only clear expired entries
- `--confirm`: Skip confirmation prompt
- `--verbose, -v`: Detailed output

---

### Analytics Commands

#### shannon analytics costs

View cost analytics.

```bash
# Last 30 days
shannon analytics costs

# Specific time range
shannon analytics costs --last 7d

# By project
shannon analytics costs --project my-app

# Export to CSV
shannon analytics costs --export costs.csv
```

**Options**:
- `--last PERIOD`: Time period (7d, 30d, 90d)
- `--project ID`: Filter by project
- `--export FILE`: Export to file
- `--json`: JSON format output

**Output**:
```
💰 Cost Analytics (Last 30 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Summary:
├─ Total Cost: $127.40
├─ Average per Session: $3.18
├─ Cache Savings: $45.80 (36%)
└─ Net Cost: $81.60

By Model:
├─ claude-sonnet-4: $98.20 (77%)
├─ claude-haiku-4: $18.60 (15%)
└─ claude-opus-4: $10.60 (8%)

By Project:
├─ my-app: $65.40 (51%)
├─ website: $38.20 (30%)
└─ api: $23.80 (19%)

Trend: ↓ 12% vs. previous 30 days
```

---

#### shannon analytics trends

View usage trends.

```bash
# Show all trends
shannon analytics trends

# Specific metric
shannon analytics trends --metric cost

# Chart display
shannon analytics trends --chart
```

**Options**:
- `--metric NAME`: Specific metric (cost, tokens, sessions)
- `--chart`: Display ASCII chart
- `--last PERIOD`: Time period
- `--json`: JSON format output

---

### Utility Commands

#### shannon diagnostics

Show diagnostic information.

```bash
# Run diagnostics
shannon diagnostics

# Deep diagnostics
shannon diagnostics --deep

# Export report
shannon diagnostics --export report.txt
```

**Options**:
- `--deep`: Deep system check
- `--export FILE`: Export report
- `--json`: JSON format output

**Output**:
```
🔧 Shannon CLI Diagnostics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

System:
├─ Python: 3.11.5 ✓
├─ Platform: macOS 14.0
└─ Terminal: iTerm2 (Unicode ✓)

Shannon CLI:
├─ Version: 3.0.0 ✓
├─ Installation: /usr/local/lib/python3.11/site-packages/shannon
└─ Config: ~/.shannon/config.json ✓

Claude Agent SDK:
├─ Version: 1.2.0 ✓
├─ Installation: /usr/local/lib/python3.11/site-packages/claude
└─ Status: ✓ Operational

Shannon Framework:
├─ Version: 2.1.0 ✓
├─ Location: ~/.claude/plugins/shannon
├─ Skills: 18 discovered ✓
└─ Status: ✓ Operational

MCPs (7/7):
├─ ✓ serena (2.1.0)
├─ ✓ filesystem (1.5.0)
├─ ✓ git (1.2.0)
├─ ✓ memory (1.0.0)
├─ ✓ browser (1.3.0)
├─ ✓ postgres (1.4.0)
└─ ✓ sequential (1.1.0)

Context System:
├─ Onboarded Projects: 3
├─ Hot Cache: Ready
├─ Warm Cache: ~/.shannon/context/ ✓
└─ Cold Storage: Serena MCP ✓

Cache:
├─ Storage: 12.4 MB / 500 MB
├─ Entries: 127
└─ Status: ✓ Operational

Analytics:
├─ Database: ~/.shannon/analytics.db ✓
├─ Size: 4.2 MB
└─ Sessions: 48 recorded

✅ All systems operational
```

---

## Common Workflows

### Workflow 1: New Project from Specification

Complete workflow for implementing a new project.

```bash
# 1. Create specification
cat > spec.md << 'EOF'
# Project: User Management API

## Requirements
- RESTful API for user CRUD operations
- JWT authentication
- PostgreSQL database
- OpenAPI documentation

## Success Criteria
- All endpoints tested
- <100ms response time
- API documentation complete
EOF

# 2. Analyze complexity
shannon analyze spec.md --json > analysis.json

# View analysis
cat analysis.json | jq '.complexity'

# 3. Execute implementation
shannon task spec.md --auto

# 4. Check results
shannon status --verbose

# 5. Run tests
shannon test

# 6. Pre-completion check
shannon reflect

# 7. Create checkpoint
shannon checkpoint "v1-complete"
```

**Expected Timeline**:
- Analysis: ~30 seconds
- Implementation: ~4-6 hours (depending on complexity)
- Testing: ~30 minutes
- Total: ~5-7 hours

---

### Workflow 2: Existing Codebase Enhancement

Adding features to an existing project.

```bash
# 1. Onboard existing codebase (one-time)
shannon onboard /path/to/project --project-id my-app

# Output: Indexed 142 files, detected Next.js 14

# 2. Create feature specification
cat > add-search.md << 'EOF'
# Feature: Add Search Functionality

## Context
Existing Next.js app with PostgreSQL database.

## Requirements
- Full-text search across users and posts
- Search API endpoint
- Frontend search component
- Debounced search input

## Success Criteria
- Search returns results in <200ms
- Handles typos (fuzzy matching)
- Tests cover edge cases
EOF

# 3. Analyze with context
shannon analyze add-search.md --project-id my-app

# Output: Complexity: 0.28 (Low) - Context reduced from 0.45!

# 4. Prime context for session
shannon prime --project-id my-app

# 5. Execute with context
shannon wave "Add search feature" --project-id my-app

# Context automatically loaded - agents aware of:
# - Existing architecture
# - Database schema
# - API patterns
# - Test structure
# - Component patterns

# 6. Update context after changes
shannon update --project-id my-app

# 7. Create checkpoint
shannon checkpoint "search-feature-complete"
```

**Benefits of Context**:
- 30-40% complexity reduction
- Consistent with existing patterns
- No architectural conflicts
- Faster implementation

---

### Workflow 3: Cost-Optimized Development

Minimizing costs while maintaining quality.

```bash
# 1. Set budget limit
shannon config set budget.max_tokens 50000
shannon config set budget.warn_threshold 0.75

# 2. Enable aggressive caching
shannon config set cache.enabled true
shannon config set cache.analysis_ttl_days 14

# 3. Use Haiku for simple tasks
shannon analyze simple-spec.md --model claude-haiku-4

# 4. Check cache before analysis
shannon cache stats

# 5. Analyze with cache awareness
shannon analyze spec.md
# Cache HIT → Saved $1.20

# 6. Monitor costs during execution
shannon wave "implement feature"
# Live dashboard shows: Cost: $0.24 / $5.00 budget

# 7. Pause if approaching limit
# Dashboard: ⚠️ Budget 80% consumed - pause? [y/N]

# 8. Review cost analytics
shannon analytics costs --last 30d

# 9. Identify optimization opportunities
shannon analytics trends --metric cost --chart
```

**Cost Savings Strategies**:
- Cache hit rate >70% → 50-80% cost reduction
- Use Haiku for low complexity → 90% cheaper than Opus
- Budget enforcement → No surprise bills
- Context reuse → Reduced token usage

---

### Workflow 4: Multi-Wave Large Project

Managing complex projects with many waves.

```bash
# 1. Analyze large specification
shannon analyze large-project.md

# Output:
# Complexity: 0.78 (High)
# Recommended: 6 waves
# Estimated: ~24 hours, $45.00

# 2. Create session checkpoint (before starting)
shannon checkpoint "pre-implementation"

# 3. Execute Wave 1
shannon wave "Implement database schema and models"

# Live dashboard shows progress
# Wave 1/6: BACKEND - Database layer

# 4. Checkpoint after each wave
shannon checkpoint "wave-1-complete"

# 5. Continue with Wave 2
shannon wave "Implement API endpoints"

# If interrupted, resume from checkpoint:
# shannon restore cp_abc123_wave1

# 6. Monitor progress
shannon status --verbose

# Output:
# Wave 1: ✓ Complete (3.2h, $7.50)
# Wave 2: 🔄 In Progress (1.1h, $2.80)
# Wave 3-6: Pending

# 7. Pause if needed
# Press 'p' in dashboard or:
shannon agent pause

# 8. Resume later
shannon agent resume

# 9. After each wave, run tests
shannon test

# 10. Final reflection before completion
shannon reflect

# 11. Final checkpoint
shannon checkpoint "project-complete" --message "All 6 waves complete, tests passing"
```

**Best Practices**:
- Checkpoint after each wave
- Run tests incrementally
- Monitor budget continuously
- Pause/resume as needed
- Final reflection before claiming done

---

### Workflow 5: Team Collaboration

Using Shannon CLI in team environment.

```bash
# Team Lead: Onboard shared project
shannon onboard /shared/project --project-id team-app

# Team Lead: Share project ID with team
echo "team-app" > .shannon-project-id

# Developer 1: Prime context
shannon prime --project-id team-app

# Developer 1: Work on feature
shannon wave "Add user authentication" --project-id team-app
shannon checkpoint "auth-complete"

# Developer 1: Share checkpoint
# Export checkpoint ID and share with team

# Developer 2: Restore from checkpoint
shannon restore cp_team_auth_complete

# Developer 2: Continue work
shannon wave "Add authorization" --project-id team-app

# Team Lead: View analytics across team
shannon analytics costs --project team-app

# Output:
# Total: $127.40 (3 developers)
# Avg per developer: $42.47
# Cache savings: $45.80 (team reuse)

# Team Lead: Update context after merges
shannon update --project-id team-app --force
```

**Team Benefits**:
- Shared context reduces rework
- Checkpoints enable handoffs
- Analytics track team costs
- Cache reuse saves money

---

## Advanced Features

### Agent State Tracking

V3 tracks agent lifecycle and enables advanced control.

**Automatic Tracking**:
```python
# During wave execution, automatically tracks:
- Agent spawns (BACKEND, FRONTEND, QA, etc.)
- Message routing between agents
- Agent states (ACTIVE, PAUSED, ERROR, COMPLETE)
- Resource usage per agent
```

**Manual Control**:
```bash
# Pause specific agent
shannon agent pause --agent BACKEND

# Resume agent
shannon agent resume --agent BACKEND

# View agent states
shannon agent status

# Output:
# Agent      State    Runtime  Tokens  Cost
# BACKEND    ACTIVE   12m      8,450   $0.24
# FRONTEND   PAUSED   5m       3,200   $0.09
# QA         PENDING  -        -       -
```

**Error Recovery**:
```bash
# If agent errors, automatic retry with exponential backoff
# Dashboard shows:
# ⚠️ BACKEND agent error - Retry 1/3 in 5s...

# Manual retry
shannon agent retry --agent BACKEND

# Skip problematic agent
shannon agent skip --agent BACKEND
```

---

### Smart Model Selection

Automatic model selection based on complexity and cost targets.

**Selection Algorithm**:
```python
def select_model(complexity: float, budget_remaining: float) -> str:
    if complexity < 0.30:
        return "claude-haiku-4"    # $0.25/M tokens
    elif complexity < 0.60:
        return "claude-sonnet-4"   # $3.00/M tokens
    else:
        # Check budget
        if budget_remaining < 50000:  # tokens
            return "claude-sonnet-4"  # Cheaper option
        else:
            return "claude-opus-4"    # $15.00/M tokens
```

**Manual Override**:
```bash
# Force specific model
shannon analyze spec.md --model claude-opus-4

# Set default model
shannon config set optimization.default_model claude-sonnet-4

# Per-wave model selection
shannon wave "simple task" --model claude-haiku-4
shannon wave "complex algorithm" --model claude-opus-4
```

**Cost Comparison**:
```
Same task across models:
- Haiku:  ~8 minutes, $0.30
- Sonnet: ~5 minutes, $2.40
- Opus:   ~3 minutes, $8.50

Selection impact:
- Haiku for simple → 90% cost savings
- Opus for complex → 40% time savings
- Sonnet for medium → Balanced
```

---

### Context-Aware Caching

Cache keys include context hash for accurate reuse.

**Cache Key Computation**:
```python
def compute_cache_key(
    spec_text: str,
    framework_version: str,
    model: str,
    context_files: List[str]
) -> str:
    # Include context in key
    context_hash = hashlib.sha256(
        "".join(sorted(context_files)).encode()
    ).hexdigest()[:8]

    key_parts = [
        hashlib.sha256(spec_text.encode()).hexdigest()[:16],
        framework_version,
        model,
        context_hash
    ]

    return hashlib.sha256(
        ":".join(key_parts).encode()
    ).hexdigest()
```

**Example**:
```bash
# Same spec, different context → Different cache entries

# Without context
shannon analyze spec.md
# Cache key: 7f3a2b1c...
# Complexity: 0.45

# With context
shannon analyze spec.md --project-id my-app
# Cache key: 9d4e5c2a...  (different!)
# Complexity: 0.28  (lower due to context)

# Future reuse
shannon analyze spec.md --project-id my-app
# Cache HIT: 9d4e5c2a...
# Saved $1.20
```

---

### Budget Enforcement

Prevent cost overruns with automatic budget checks.

**Budget Configuration**:
```bash
# Set hard limit
shannon config set budget.max_tokens 100000

# Set warning threshold (80%)
shannon config set budget.warn_threshold 0.80

# Set pause threshold (95%)
shannon config set budget.pause_threshold 0.95
```

**Enforcement Flow**:
```
Before Wave:
1. Estimate cost
2. Check remaining budget
3. Warn if > 80%
4. Block if > 95%

During Wave:
1. Track actual tokens
2. Update budget usage
3. Warn at threshold
4. Pause at limit

Dashboard Display:
Budget: 45,200 / 100,000 tokens (45%)
Cost: $1.35 / ~$3.00 max
⚠️ Warning at 80,000 tokens
```

**Pause Behavior**:
```bash
# Automatic pause at limit
# Dashboard shows:
# ⚠️ Budget limit reached (95,000 / 100,000 tokens)
# Execution paused. Options:
#   1. Increase budget limit
#   2. Resume with current limit (risky)
#   3. Cancel execution

# Increase limit
shannon config set budget.max_tokens 150000

# Resume
shannon agent resume
```

---

### Historical Analytics

SQLite database tracks all sessions for insights.

**Database Schema**:
```sql
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    created_at TIMESTAMP,
    project_id TEXT,
    complexity REAL,
    waves_planned INTEGER,
    waves_completed INTEGER,
    total_tokens INTEGER,
    total_cost REAL,
    cache_hits INTEGER,
    cache_misses INTEGER,
    status TEXT
);

CREATE TABLE waves (
    id TEXT PRIMARY KEY,
    session_id TEXT,
    wave_number INTEGER,
    agent TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    tokens INTEGER,
    cost REAL,
    status TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);
```

**Query Examples**:
```bash
# Top 10 most expensive sessions
shannon analytics query "
  SELECT id, project_id, total_cost
  FROM sessions
  ORDER BY total_cost DESC
  LIMIT 10
"

# Average complexity by project
shannon analytics query "
  SELECT project_id, AVG(complexity) as avg_complexity
  FROM sessions
  GROUP BY project_id
"

# Cache hit rate over time
shannon analytics query "
  SELECT
    DATE(created_at) as date,
    SUM(cache_hits) * 100.0 / (SUM(cache_hits) + SUM(cache_misses)) as hit_rate
  FROM sessions
  WHERE created_at > date('now', '-30 days')
  GROUP BY DATE(created_at)
"
```

**Insight Generation**:
```bash
# Automatic insights
shannon analytics insights

# Output:
# 📊 Analytics Insights
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Cost Trends:
# ├─ Last 7 days: $18.40 (↓ 15% vs. previous week)
# ├─ Top project: my-app ($65.40, 51% of total)
# └─ Optimization: Use Haiku for complexity < 0.30
#
# Cache Performance:
# ├─ Hit rate: 72% (↑ from 65% last month)
# ├─ Savings: $45.80 (36% of gross cost)
# └─ Opportunity: 15 near-miss patterns identified
#
# Project Patterns:
# ├─ my-app: Backend-heavy (65% backend waves)
# ├─ website: Frontend-heavy (70% frontend waves)
# └─ api: Balanced (40% backend, 30% frontend, 30% DB)
#
# Recommendations:
# 1. Increase cache TTL for stable projects
# 2. Use context for my-app (30% complexity reduction)
# 3. Consider Haiku for website (low complexity avg)
```

---

## Troubleshooting

### Common Issues

#### Issue: Framework Not Found

**Symptom**:
```
Error: Shannon Framework not found
Searched locations:
  - ~/.claude/plugins/shannon ✗
  - ./shannon ✗
  - /usr/local/shannon ✗
```

**Solution**:
```bash
# 1. Run setup wizard
shannon setup

# 2. Or manually install framework
# In Claude Code:
# /plugin marketplace add shannon-framework/shannon
# /plugin install shannon@shannon-framework

# 3. Verify
shannon diagnostics
```

---

#### Issue: Cache HIT but Wrong Results

**Symptom**:
Analysis results don't match current specification.

**Cause**: Cache entry from old version of spec.

**Solution**:
```bash
# Clear analysis cache
shannon cache clear --tier analysis

# Or force fresh analysis
shannon analyze spec.md --no-cache
```

---

#### Issue: Budget Limit Reached

**Symptom**:
```
⚠️ Budget limit reached (95,000 / 100,000 tokens)
Execution paused.
```

**Solution**:
```bash
# Option 1: Increase budget
shannon config set budget.max_tokens 150000
shannon agent resume

# Option 2: Use cheaper model
shannon config set optimization.default_model claude-haiku-4
shannon agent resume

# Option 3: Clear cache to save tokens on future runs
shannon cache clear

# Option 4: Enable context to reduce complexity
shannon onboard /path/to/project --project-id my-app
shannon wave "continue" --project-id my-app
```

---

#### Issue: MCP Connection Failed

**Symptom**:
```
🔌 MCP Status
serena    ✗ Error    Connection failed
```

**Solution**:
```bash
# 1. Verify MCP installed
shannon mcp list

# 2. Reinstall if needed
shannon mcp install serena --force

# 3. Verify health
shannon mcp verify serena --deep

# 4. Check logs
shannon diagnostics --verbose
```

---

#### Issue: Context Load Timeout

**Symptom**:
```
⚠️ Context load timeout (>5s)
Falling back to no context
```

**Cause**: Large project or Serena MCP unavailable.

**Solution**:
```bash
# Option 1: Use structure-only (faster)
shannon prime --project-id my-app --structure-only

# Option 2: Rebuild context index
shannon update --project-id my-app --force

# Option 3: Reduce max files
shannon config set context.max_files 500
shannon update --project-id my-app --force

# Option 4: Check Serena MCP
shannon mcp verify serena
```

---

#### Issue: Agent Stuck in Loop

**Symptom**:
Agent repeats same actions without progress.

**Solution**:
```bash
# 1. Pause execution
# Press 'p' in dashboard

# 2. Check agent state
shannon agent status

# 3. Retry with fresh state
shannon agent retry --agent BACKEND

# 4. If persists, skip agent
shannon agent skip --agent BACKEND

# 5. Resume execution
shannon agent resume
```

---

#### Issue: Live Dashboard Not Updating

**Symptom**:
Dashboard frozen or not refreshing.

**Cause**: Terminal compatibility or termios issues.

**Solution**:
```bash
# Option 1: Use auto mode (no live dashboard)
shannon wave "request" --auto

# Option 2: Check terminal
shannon diagnostics

# If terminal doesn't support termios:
# Set environment variable
export SHANNON_DASHBOARD_MODE=simple

# Option 3: Update terminal
# Ensure modern terminal: iTerm2, kitty, Alacritty, etc.
```

---

#### Issue: Complexity Too High

**Symptom**:
```
Complexity: 0.85 (Very High)
Recommended: 8 waves, ~32 hours, $85.00
```

**Cause**: Specification too broad or ambiguous.

**Solution**:
```bash
# 1. Add context to reduce complexity
shannon onboard /path/to/project --project-id my-app
shannon analyze spec.md --project-id my-app
# New complexity: 0.52 (reduced by context!)

# 2. Break into smaller specs
# Create spec-phase1.md (core features)
# Create spec-phase2.md (enhancements)

# 3. Clarify ambiguous requirements
# Review 8D scores and address highest dimensions

# 4. Use more powerful model
shannon analyze spec.md --model claude-opus-4
```

---

### Debugging

#### Enable Verbose Logging

```bash
# Set log level
shannon config set log_level DEBUG

# Run command with verbose output
shannon analyze spec.md --verbose

# Check logs
tail -f ~/.shannon/logs/shannon.log
```

---

#### Export Diagnostics Report

```bash
# Full diagnostic report
shannon diagnostics --deep --export diagnostics.txt

# Include in bug report:
cat diagnostics.txt
```

---

#### Test Individual Components

```bash
# Test context system
shannon prime --project-id test --verbose

# Test cache system
shannon cache stats --verbose

# Test MCP system
shannon check-mcps --verbose

# Test analytics
shannon analytics query "SELECT COUNT(*) FROM sessions"
```

---

## Best Practices

### Specification Writing

**Good Specification Structure**:
```markdown
# Title: Clear, actionable goal

## Context
What already exists, what's changing

## Requirements
- Specific, measurable requirements
- Technical constraints
- Integration points

## Success Criteria
- How to verify completion
- Quality metrics
- Test coverage expectations

## Non-Goals
What's explicitly out of scope
```

**Anti-Patterns**:
```markdown
# Bad: "Build a website"
# Why: Too vague, no context, no success criteria

# Good: "Add search to existing Next.js blog"
# Context: Next.js 14 app with PostgreSQL
# Requirements: Full-text search, <200ms, fuzzy matching
# Success: Tests cover typos, special chars, empty results
```

---

### Context Management

**When to Onboard**:
- Starting work on existing codebase
- Complexity unexpectedly high
- Need consistency with existing patterns
- Multiple sessions on same project

**When to Update**:
- After major changes (weekly for active projects)
- Before important sessions
- After dependency updates
- When git diff shows >50 files changed

**Context Best Practices**:
```bash
# 1. Onboard once
shannon onboard /path/to/project --project-id my-app

# 2. Update regularly
shannon update --project-id my-app

# 3. Prime before each session
shannon prime --project-id my-app

# 4. Use structure-only for quick tasks
shannon prime --project-id my-app --structure-only
```

---

### Cost Optimization

**Strategies**:

1. **Use Cache Aggressively**
```bash
# Increase TTLs for stable projects
shannon config set cache.analysis_ttl_days 14
shannon config set cache.command_ttl_days 60
```

2. **Right-Size Model Selection**
```bash
# Use Haiku for simple tasks
shannon analyze simple-spec.md --model claude-haiku-4

# Reserve Opus for truly complex work
shannon analyze complex-algorithm.md --model claude-opus-4
```

3. **Leverage Context**
```bash
# Context reduces complexity → cheaper models
shannon onboard /path/to/project --project-id my-app
shannon analyze spec.md --project-id my-app
# Complexity: 0.28 (was 0.45) → Use Haiku instead of Sonnet
```

4. **Monitor Budget**
```bash
# Set conservative limits
shannon config set budget.max_tokens 50000
shannon config set budget.warn_threshold 0.70
```

5. **Review Analytics**
```bash
# Identify cost patterns
shannon analytics costs --last 30d
shannon analytics insights

# Act on recommendations
```

---

### Testing Strategy

**Follow NO MOCKS Philosophy**:
```bash
# Good: Functional tests
shannon test

# Output:
# ✓ All tests use real components
# ✓ Real database (test instance)
# ✓ Real file system
# ✓ Real API calls

# Bad: Unit tests with mocks
# Shannon Framework will reject or rewrite
```

**Pre-Completion Checklist**:
```bash
# 1. Run tests
shannon test
# All passing?

# 2. Run reflection
shannon reflect
# Any gaps identified?

# 3. Address gaps
shannon wave "Fix identified gaps"

# 4. Repeat until clean
shannon reflect
# ✓ No gaps - ready for completion
```

---

### Session Management

**Checkpoint Strategy**:
```bash
# Before risky operations
shannon checkpoint "pre-refactor"

# After each wave (large projects)
shannon checkpoint "wave-${WAVE_NUM}-complete"

# Before claiming completion
shannon checkpoint "final-pre-completion"

# After successful testing
shannon checkpoint "tests-passing"
```

**Naming Conventions**:
```bash
# Good names (descriptive)
shannon checkpoint "auth-endpoints-complete"
shannon checkpoint "database-migration-done"
shannon checkpoint "pre-deployment-checks"

# Bad names (vague)
shannon checkpoint "checkpoint1"
shannon checkpoint "backup"
shannon checkpoint "test"
```

---

### Team Collaboration

**Shared Context**:
```bash
# Team lead: Set up shared project
shannon onboard /shared/project --project-id team-app

# Document project ID
echo "team-app" > .shannon-project-id

# Team members: Use project ID
PROJECT_ID=$(cat .shannon-project-id)
shannon prime --project-id $PROJECT_ID
shannon wave "feature" --project-id $PROJECT_ID
```

**Checkpoint Sharing**:
```bash
# Developer 1: Create shareable checkpoint
shannon checkpoint "feature-complete"
# Export: cp_team_app_1699887045

# Developer 1: Share checkpoint ID with team

# Developer 2: Restore checkpoint
shannon restore cp_team_app_1699887045
```

**Cost Tracking**:
```bash
# Team lead: Monitor team costs
shannon analytics costs --project team-app

# Review regularly
shannon analytics trends --project team-app --metric cost
```

---

### CI/CD Integration

**Automated Analysis**:
```bash
#!/bin/bash
# ci-analyze.sh

# Run analysis in JSON mode
shannon analyze spec.md --json > analysis.json

# Extract complexity
COMPLEXITY=$(jq -r '.complexity' analysis.json)

# Fail if too complex
if (( $(echo "$COMPLEXITY > 0.70" | bc -l) )); then
  echo "Error: Complexity too high ($COMPLEXITY)"
  exit 1
fi

echo "Complexity OK: $COMPLEXITY"
```

**Budget Control**:
```bash
#!/bin/bash
# ci-budget-check.sh

# Set strict budget for CI
shannon config set budget.max_tokens 10000

# Run task with auto mode
shannon task spec.md --auto

# Check if budget exceeded
if [ $? -ne 0 ]; then
  echo "Error: Budget exceeded or execution failed"
  exit 1
fi
```

**Test Verification**:
```bash
#!/bin/bash
# ci-test.sh

# Run Shannon tests
shannon test --session-id $CI_SESSION_ID

# Verify no gaps
shannon reflect --session-id $CI_SESSION_ID | grep "✓ No gaps"

if [ $? -ne 0 ]; then
  echo "Error: Gaps identified - implementation incomplete"
  exit 1
fi
```

---

## Conclusion

Shannon CLI V3.0 provides a production-grade platform for AI-powered development with:

- **Real-time visibility** via live metrics dashboard
- **Cost optimization** through smart caching and model selection
- **Context awareness** for existing codebases
- **Quality enforcement** with NO MOCKS testing
- **Historical insights** from analytics database

### Getting Help

- **Documentation**: Full docs at `/docs/`
- **Issues**: GitHub issues for bug reports
- **Discussions**: GitHub discussions for questions
- **Diagnostics**: `shannon diagnostics` for troubleshooting

### Next Steps

1. **Complete Setup**: Run `shannon setup` if not done
2. **Try Examples**: Work through common workflows
3. **Onboard Project**: Add your existing codebase
4. **Explore Features**: Experiment with V3 capabilities
5. **Review Analytics**: Track your usage and costs

---

**Shannon CLI V3.0** - Intelligent AI development orchestration.

*Last Updated: 2025-11-14*
