# Shannon CLI V3.0 - MCP Setup Guide

**Version**: 3.0.0 | **Date**: 2025-11-14

> Complete guide to installing, configuring, and troubleshooting MCP servers for Shannon CLI V3.0

---

## Table of Contents

1. [Overview](#overview)
2. [Recommended MCPs](#recommended-mcps)
3. [Installation Methods](#installation-methods)
4. [Individual MCP Setup](#individual-mcp-setup)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)
7. [Integration Examples](#integration-examples)

---

## Overview

### What are MCPs?

MCP (Model Context Protocol) servers extend Claude's capabilities with specialized tools for:
- File operations (filesystem)
- Version control (git)
- Database access (postgres)
- Knowledge graph storage (Serena)
- Web research (browser)
- Shared memory (memory)
- Complex reasoning (sequential-thinking)

### Why MCPs Matter for Shannon CLI

Shannon CLI V3.0 leverages MCPs to:
1. **Context Management**: Serena MCP stores project context permanently
2. **File Operations**: Filesystem MCP enables code generation and modification
3. **Version Control**: Git MCP tracks changes and enables rollback
4. **Database Operations**: Postgres MCP for schema and query operations
5. **Research**: Browser MCP for documentation lookup
6. **Memory**: Memory MCP for agent coordination
7. **Reasoning**: Sequential-thinking MCP for complex problems

### Auto-Installation

V3 automatically detects required MCPs and installs them:

```bash
# Run analysis - MCPs auto-installed
shannon analyze spec.md

# Output:
# MCPs Recommended: 3
#   Installing filesystem... ✓
#   Installing postgres... ✓
#   Installing git... ✓
```

**Manual installation** is only needed if:
- Auto-installation disabled
- Specific MCP configuration required
- Troubleshooting issues

---

## Recommended MCPs

Shannon CLI V3.0 works best with these 7 MCPs:

### 1. Serena (Highly Recommended)

**Purpose**: Knowledge graph for permanent context storage

**Capabilities**:
- Store project context
- Semantic search
- Relationship tracking
- Historical queries

**Installation Priority**: **CRITICAL** - Required for context system

---

### 2. Filesystem (Essential)

**Purpose**: File system operations

**Capabilities**:
- Read/write files
- Directory navigation
- File search
- Permission management

**Installation Priority**: **ESSENTIAL** - Required for code generation

---

### 3. Git (Essential)

**Purpose**: Version control operations

**Capabilities**:
- Commit changes
- Track history
- Branch management
- Diff generation

**Installation Priority**: **ESSENTIAL** - Required for change tracking

---

### 4. Memory (Recommended)

**Purpose**: Shared memory across agents

**Capabilities**:
- Store agent state
- Share context between agents
- Coordination messages
- Session persistence

**Installation Priority**: **RECOMMENDED** - Improves multi-agent coordination

---

### 5. Browser (Recommended)

**Purpose**: Web research and documentation lookup

**Capabilities**:
- Search documentation
- Fetch web pages
- Parse HTML
- Screenshot capture

**Installation Priority**: **RECOMMENDED** - Helps with unfamiliar libraries

---

### 6. Postgres (As Needed)

**Purpose**: PostgreSQL database operations

**Capabilities**:
- Execute queries
- Schema inspection
- Migration management
- Data manipulation

**Installation Priority**: **AS NEEDED** - Only for database projects

---

### 7. Sequential-thinking (Advanced)

**Purpose**: Enhanced reasoning for complex problems

**Capabilities**:
- Step-by-step reasoning
- Problem decomposition
- Logic verification
- Complex algorithm design

**Installation Priority**: **ADVANCED** - For high complexity tasks

---

## Installation Methods

### Method 1: Setup Wizard (Recommended)

Easiest way to install all recommended MCPs:

```bash
# Run interactive setup
shannon setup

# Wizard steps:
# ...
# Step 4: MCP Installation
#   Install recommended MCPs? [Y/n] y
#
#   Installing Serena MCP...        ✓
#   Installing Filesystem MCP...    ✓
#   Installing Git MCP...           ✓
#   Installing Memory MCP...        ✓
#   Installing Browser MCP...       ✓
#   Installing Postgres MCP...      ✓
#   Installing Sequential MCP...    ✓
#
#   All MCPs installed successfully!
```

---

### Method 2: Auto-Installation

MCPs are automatically installed when needed:

```bash
# Analyze spec - auto-installs required MCPs
shannon analyze spec.md

# Domains detected: Backend (60%), Database (40%)
# MCPs Recommended: filesystem, postgres, git
#   Installing filesystem... ✓
#   Installing postgres... ✓
#   Installing git... ✓
```

**Enable/Disable Auto-Installation**:
```bash
# Enable (default)
shannon config set mcp.auto_install true

# Disable
shannon config set mcp.auto_install false
```

---

### Method 3: Manual Installation

Install specific MCPs manually:

```bash
# Install single MCP
shannon mcp install serena

# Install with verification
shannon mcp install serena --verify

# Install all recommended
shannon mcp install --recommended

# Install with custom config
shannon mcp install postgres --config postgres-config.json
```

---

### Method 4: Claude Code UI

Install via Claude Code interface:

```
1. Open Claude Code
2. Type: /mcp install serena
3. Wait for installation
4. Verify: /mcp list
```

---

## Individual MCP Setup

### Serena MCP

**Installation**:

```bash
# Via Shannon CLI
shannon mcp install serena --verify

# Via Claude Code
/mcp install serena
```

**Configuration** (`~/.claude/mcp_config.json`):

```json
{
  "mcps": {
    "serena": {
      "command": "npx",
      "args": ["-y", "@anthropics/serena-mcp"],
      "config": {
        "storage_path": "~/.serena/knowledge",
        "max_graph_size_mb": 1000
      }
    }
  }
}
```

**Verification**:

```bash
# Check installed
shannon check-mcps

# Deep health check
shannon mcp verify serena --deep

# Expected output:
# MCP: serena
# Status: ✓ Active
# Version: 2.1.0
# Health: ✓ Healthy
# Storage: ~/.serena/knowledge (12.4 MB)
```

**Testing**:

```bash
# Test Serena storage
shannon onboard /path/to/project --project-id test-serena

# Expected:
# Context stored in Serena MCP ✓
```

**Troubleshooting**:

```bash
# Issue: Connection failed
# Solution 1: Restart Serena
/mcp restart serena

# Solution 2: Reinstall
shannon mcp install serena --force

# Solution 3: Check logs
tail -f ~/.serena/logs/serena.log
```

---

### Filesystem MCP

**Installation**:

```bash
# Via Shannon CLI
shannon mcp install filesystem --verify

# Via Claude Code
/mcp install filesystem
```

**Configuration**:

```json
{
  "mcps": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropics/filesystem-mcp"],
      "config": {
        "allowed_paths": [
          "~/projects",
          "~/Documents"
        ],
        "denied_paths": [
          "~/.ssh",
          "~/.aws"
        ]
      }
    }
  }
}
```

**Verification**:

```bash
# Verify filesystem access
shannon mcp verify filesystem

# Test file operations
shannon wave "Create a test file"
# Should successfully create file
```

**Security Considerations**:

```bash
# Limit access to specific directories
# Edit ~/.claude/mcp_config.json

{
  "filesystem": {
    "config": {
      "allowed_paths": ["/path/to/safe/directory"],
      "read_only": false
    }
  }
}
```

**Troubleshooting**:

```bash
# Issue: Permission denied
# Solution: Check allowed_paths in config

# Issue: File not found
# Solution: Verify path is in allowed_paths
```

---

### Git MCP

**Installation**:

```bash
# Via Shannon CLI
shannon mcp install git --verify

# Via Claude Code
/mcp install git
```

**Configuration**:

```json
{
  "mcps": {
    "git": {
      "command": "npx",
      "args": ["-y", "@anthropics/git-mcp"],
      "config": {
        "allowed_repos": [
          "~/projects/*"
        ],
        "auto_commit": false,
        "commit_message_template": "[Shannon] {action}"
      }
    }
  }
}
```

**Verification**:

```bash
# Verify Git MCP
shannon mcp verify git

# Test git operations
cd /path/to/git/repo
shannon wave "Show git status"
# Should display current status
```

**Best Practices**:

```bash
# Enable auto-commit for Shannon operations
{
  "git": {
    "config": {
      "auto_commit": true,
      "commit_message_template": "[Shannon Wave {wave}] {description}"
    }
  }
}

# Track changes per wave
shannon checkpoint "wave-1-complete"
# Creates git commit automatically
```

**Troubleshooting**:

```bash
# Issue: Not a git repository
# Solution: Initialize repo
cd /path/to/project
git init

# Issue: Permission denied
# Solution: Check allowed_repos in config
```

---

### Memory MCP

**Installation**:

```bash
# Via Shannon CLI
shannon mcp install memory --verify

# Via Claude Code
/mcp install memory
```

**Configuration**:

```json
{
  "mcps": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@anthropics/memory-mcp"],
      "config": {
        "storage_path": "~/.shannon/memory",
        "max_memory_mb": 100,
        "persistence": true
      }
    }
  }
}
```

**Verification**:

```bash
# Verify Memory MCP
shannon mcp verify memory

# Test memory operations
shannon memory
# Should show shared memory state
```

**Use Cases**:

- **Agent Coordination**: Share state between BACKEND and FRONTEND agents
- **Session Persistence**: Maintain context across sessions
- **Goal Tracking**: Store and retrieve North Star goals

**Troubleshooting**:

```bash
# Issue: Memory limit exceeded
# Solution: Increase max_memory_mb

# Issue: Persistence not working
# Solution: Check storage_path permissions
```

---

### Browser MCP

**Installation**:

```bash
# Via Shannon CLI
shannon mcp install browser --verify

# Via Claude Code
/mcp install browser
```

**Configuration**:

```json
{
  "mcps": {
    "browser": {
      "command": "npx",
      "args": ["-y", "@anthropics/browser-mcp"],
      "config": {
        "headless": true,
        "timeout_ms": 30000,
        "allowed_domains": ["*"],
        "denied_domains": []
      }
    }
  }
}
```

**Verification**:

```bash
# Verify Browser MCP
shannon mcp verify browser --deep

# Test web search
shannon wave "Search for Next.js 14 documentation"
# Should fetch and summarize docs
```

**Rate Limiting**:

```json
{
  "browser": {
    "config": {
      "rate_limit": {
        "requests_per_minute": 10,
        "concurrent_requests": 2
      }
    }
  }
}
```

**Troubleshooting**:

```bash
# Issue: Connection timeout
# Solution: Increase timeout_ms

# Issue: CAPTCHA blocking
# Solution: Use headless=false for manual intervention

# Issue: Rate limited
# Solution: Reduce requests_per_minute
```

---

### Postgres MCP

**Installation**:

```bash
# Via Shannon CLI
shannon mcp install postgres --verify

# Via Claude Code
/mcp install postgres
```

**Configuration**:

```json
{
  "mcps": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@anthropics/postgres-mcp"],
      "config": {
        "connections": {
          "local": {
            "host": "localhost",
            "port": 5432,
            "database": "myapp",
            "user": "postgres",
            "password": "${POSTGRES_PASSWORD}"
          },
          "test": {
            "host": "localhost",
            "port": 5432,
            "database": "myapp_test",
            "user": "postgres",
            "password": "${POSTGRES_PASSWORD}"
          }
        },
        "default_connection": "local"
      }
    }
  }
}
```

**Environment Variables**:

```bash
# Set database credentials
export POSTGRES_PASSWORD="your_password"

# Or use .env file
echo "POSTGRES_PASSWORD=your_password" > ~/.shannon/.env
```

**Verification**:

```bash
# Verify Postgres MCP
shannon mcp verify postgres --deep

# Expected:
# MCP: postgres
# Status: ✓ Active
# Health: ✓ Healthy
# Connections:
#   local: ✓ Connected
#   test: ✓ Connected
```

**Testing**:

```bash
# Test database operations
shannon wave "Show database schema"
# Should display tables and columns

shannon wave "Count users in database"
# Should execute query and return count
```

**Security**:

```json
{
  "postgres": {
    "config": {
      "read_only_mode": false,
      "allowed_operations": ["SELECT", "INSERT", "UPDATE"],
      "denied_operations": ["DROP", "TRUNCATE"]
    }
  }
}
```

**Troubleshooting**:

```bash
# Issue: Connection refused
# Solution 1: Check PostgreSQL running
sudo service postgresql status

# Solution 2: Verify credentials
psql -h localhost -U postgres -d myapp

# Issue: Permission denied
# Solution: Grant permissions
GRANT ALL ON DATABASE myapp TO postgres;
```

---

### Sequential-thinking MCP

**Installation**:

```bash
# Via Shannon CLI
shannon mcp install sequential --verify

# Via Claude Code
/mcp install sequential-thinking
```

**Configuration**:

```json
{
  "mcps": {
    "sequential": {
      "command": "npx",
      "args": ["-y", "@anthropics/sequential-thinking-mcp"],
      "config": {
        "max_depth": 10,
        "enable_backtracking": true,
        "reasoning_mode": "verbose"
      }
    }
  }
}
```

**Verification**:

```bash
# Verify Sequential MCP
shannon mcp verify sequential

# Test reasoning
shannon wave "Design algorithm for optimal pathfinding"
# Should show step-by-step reasoning
```

**Use Cases**:

- **Complex Algorithms**: Design sorting, searching, graph algorithms
- **Architecture Decisions**: Evaluate trade-offs systematically
- **Debug Logic**: Step through complex logic bugs
- **Optimization**: Find optimal solutions through reasoning

**Configuration Options**:

```json
{
  "sequential": {
    "config": {
      "max_depth": 15,           // Max reasoning steps
      "enable_backtracking": true, // Allow rethinking
      "reasoning_mode": "concise", // "verbose" or "concise"
      "show_thought_process": true
    }
  }
}
```

**Troubleshooting**:

```bash
# Issue: Reasoning too verbose
# Solution: Set reasoning_mode to "concise"

# Issue: Max depth reached
# Solution: Increase max_depth for complex problems
```

---

## Verification

### Check All MCPs

```bash
# Quick status check
shannon check-mcps

# Output:
# MCP              Status    Version   Health
# serena           ✓ Active  2.1.0     ✓ Healthy
# filesystem       ✓ Active  1.5.0     ✓ Healthy
# git              ✓ Active  1.2.0     ✓ Healthy
# memory           ✓ Active  1.0.0     ✓ Healthy
# browser          ✓ Active  1.3.0     ✓ Healthy
# postgres         ✓ Active  1.4.0     ✓ Healthy
# sequential       ✓ Active  1.1.0     ✓ Healthy
```

### Deep Health Check

```bash
# Comprehensive verification
shannon check-mcps --verbose

# Per-MCP deep check
shannon mcp verify serena --deep

# Output:
# MCP: serena
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Status: ✓ Active
# Version: 2.1.0
# Process ID: 12345
# Uptime: 2h 15m
# Memory: 45.2 MB
#
# Health Checks:
#   ✓ Process running
#   ✓ Port 3000 listening
#   ✓ API responding
#   ✓ Storage accessible
#   ✓ Disk space sufficient (850 GB free)
#
# Performance:
#   Response time: 12ms (avg)
#   Request rate: 2.3/min
#   Error rate: 0.0%
#
# Storage:
#   Path: ~/.serena/knowledge
#   Size: 12.4 MB
#   Files: 142
#   Graphs: 3
```

### Automated Verification

```bash
# Run verification script
cat > verify_mcps.sh << 'EOF'
#!/bin/bash

echo "Verifying all MCPs..."

MCPS=("serena" "filesystem" "git" "memory" "browser" "postgres" "sequential")

for mcp in "${MCPS[@]}"; do
    echo "Checking $mcp..."
    if shannon mcp verify $mcp --quiet; then
        echo "  ✓ $mcp OK"
    else
        echo "  ✗ $mcp FAILED"
        exit 1
    fi
done

echo "All MCPs verified successfully!"
EOF

chmod +x verify_mcps.sh
./verify_mcps.sh
```

---

## Troubleshooting

### Common Issues

#### Issue: MCP Not Starting

**Symptoms**:
```
shannon check-mcps
# postgres    ✗ Error    Process not running
```

**Diagnosis**:
```bash
# Check MCP logs
shannon mcp logs postgres

# Check configuration
cat ~/.claude/mcp_config.json | jq '.mcps.postgres'

# Test manually
npx -y @anthropics/postgres-mcp
```

**Solutions**:

1. **Restart MCP**:
```bash
shannon mcp restart postgres
```

2. **Reinstall MCP**:
```bash
shannon mcp install postgres --force
```

3. **Check Dependencies**:
```bash
# For Postgres MCP, ensure PostgreSQL running
sudo service postgresql status
```

---

#### Issue: Connection Timeout

**Symptoms**:
```
shannon mcp verify serena
# Error: Connection timeout after 5s
```

**Solutions**:

1. **Increase Timeout**:
```json
{
  "serena": {
    "config": {
      "timeout_ms": 10000
    }
  }
}
```

2. **Check Network**:
```bash
# Test connectivity
curl http://localhost:3000/health

# Check firewall
sudo ufw status
```

3. **Restart MCP**:
```bash
shannon mcp restart serena
```

---

#### Issue: Permission Denied

**Symptoms**:
```
shannon wave "Create file"
# Error: Permission denied: /path/to/file
```

**Solutions**:

1. **Check Allowed Paths** (Filesystem MCP):
```json
{
  "filesystem": {
    "config": {
      "allowed_paths": [
        "~/projects",
        "/path/to/file"  // Add this
      ]
    }
  }
}
```

2. **File System Permissions**:
```bash
# Fix permissions
chmod 755 /path/to/directory
```

3. **Run with Elevated Permissions** (not recommended):
```bash
sudo shannon wave "Create file"
```

---

#### Issue: Out of Memory

**Symptoms**:
```
shannon mcp verify memory
# Warning: Memory usage 95% (95 MB / 100 MB)
```

**Solutions**:

1. **Increase Memory Limit**:
```json
{
  "memory": {
    "config": {
      "max_memory_mb": 200
    }
  }
}
```

2. **Clear Memory**:
```bash
shannon memory clear
```

3. **Restart MCP**:
```bash
shannon mcp restart memory
```

---

#### Issue: Database Connection Failed

**Symptoms**:
```
shannon wave "Query database"
# Error: FATAL: password authentication failed
```

**Solutions**:

1. **Check Credentials**:
```bash
# Test manually
psql -h localhost -U postgres -d myapp

# Update credentials in config
shannon config set mcp.postgres.password "new_password"
```

2. **Verify Database Running**:
```bash
sudo service postgresql status

# Start if needed
sudo service postgresql start
```

3. **Check pg_hba.conf**:
```bash
# Edit PostgreSQL config
sudo nano /etc/postgresql/*/main/pg_hba.conf

# Add line:
# local   all   postgres   md5

# Restart PostgreSQL
sudo service postgresql restart
```

---

### Debugging Tools

#### MCP Logs

```bash
# View MCP logs
shannon mcp logs serena

# Follow logs in real-time
shannon mcp logs serena --follow

# Filter errors only
shannon mcp logs serena --level error
```

#### Configuration Validation

```bash
# Validate MCP config
shannon mcp validate-config

# Expected output:
# ✓ Configuration valid
# ✓ All MCPs properly configured
# ✓ No conflicts detected
```

#### Network Diagnostics

```bash
# Check MCP ports
shannon diagnostics --network

# Output:
# Port 3000 (serena):      ✓ Listening
# Port 3001 (filesystem):  ✓ Listening
# Port 3002 (git):         ✓ Listening
# ...
```

---

## Integration Examples

### Example 1: Context Onboarding with Serena

```bash
# Onboard project to Serena
shannon onboard /path/to/project --project-id my-app

# How it works:
# 1. Scans project structure
# 2. Indexes files
# 3. Analyzes dependencies
# 4. Stores in Serena MCP knowledge graph
# 5. Creates local warm cache
# 6. Ready for fast retrieval

# Verify storage
shannon mcp verify serena --deep
# Storage: 12.4 MB, 142 files indexed
```

### Example 2: File Operations with Filesystem + Git

```bash
# Generate code with automatic git tracking
shannon wave "Create authentication endpoints"

# Behind the scenes:
# 1. Filesystem MCP creates files
# 2. Git MCP stages changes
# 3. Shannon creates checkpoint
# 4. Git MCP commits with message
# 5. Change tracked in history

# View changes
git log --oneline
# a1b2c3d [Shannon Wave 1] Create authentication endpoints
```

### Example 3: Database Operations with Postgres

```bash
# Database-aware development
shannon analyze "Add user authentication with PostgreSQL"

# Auto-installs Postgres MCP

shannon wave "Implement user authentication"

# Behind the scenes:
# 1. Postgres MCP inspects existing schema
# 2. Generates migration for users table
# 3. Creates authentication endpoints
# 4. Generates tests using real database
# 5. All operations tracked in Git
```

### Example 4: Multi-Agent with Memory

```bash
# Multi-wave project with agent coordination
shannon wave "Build full-stack authentication"

# Wave 1: BACKEND agent
#   - Creates API endpoints
#   - Stores progress in Memory MCP
#
# Wave 2: FRONTEND agent
#   - Reads API spec from Memory MCP
#   - Builds UI components
#   - Stores component structure in Memory
#
# Wave 3: QA agent
#   - Reads implementation from Memory
#   - Generates tests
#   - Validates both backend and frontend

# Memory MCP enables coordination without duplication
```

### Example 5: Research with Browser

```bash
# Unfamiliar library documentation
shannon wave "Integrate Stripe payment processing"

# Behind the scenes:
# 1. Browser MCP searches Stripe docs
# 2. Fetches latest API documentation
# 3. Identifies recommended patterns
# 4. Implements using current best practices
# 5. No outdated examples or deprecated APIs
```

---

## Best Practices

### 1. Install Core MCPs First

**Priority Order**:
```bash
# Critical (install first)
shannon mcp install serena
shannon mcp install filesystem
shannon mcp install git

# Recommended (install second)
shannon mcp install memory

# As needed (install when required)
shannon mcp install browser
shannon mcp install postgres
shannon mcp install sequential
```

### 2. Verify After Installation

```bash
# Always verify after installing
shannon mcp install serena --verify

# Or verify manually
shannon mcp verify serena --deep
```

### 3. Configure Security

```bash
# Limit filesystem access
{
  "filesystem": {
    "config": {
      "allowed_paths": ["~/safe/directory"],
      "read_only": false
    }
  }
}

# Limit database operations
{
  "postgres": {
    "config": {
      "allowed_operations": ["SELECT", "INSERT", "UPDATE"],
      "denied_operations": ["DROP"]
    }
  }
}
```

### 4. Monitor MCP Health

```bash
# Regular health checks
shannon check-mcps

# Automated monitoring
cat > monitor_mcps.sh << 'EOF'
#!/bin/bash
while true; do
    shannon check-mcps --quiet || {
        echo "MCP health check failed! $(date)"
        shannon mcp restart --all
    }
    sleep 300  # Check every 5 minutes
done
EOF
```

### 5. Keep MCPs Updated

```bash
# Update all MCPs
shannon mcp update --all

# Update specific MCP
shannon mcp update serena

# Check for updates
shannon mcp check-updates
```

---

## Summary

### Quick Start Checklist

- [ ] Run setup wizard: `shannon setup`
- [ ] Install core MCPs (Serena, Filesystem, Git)
- [ ] Verify installation: `shannon check-mcps`
- [ ] Configure security settings
- [ ] Test with simple task
- [ ] Install additional MCPs as needed

### Maintenance Checklist

- [ ] Weekly: Check MCP health
- [ ] Monthly: Update MCPs
- [ ] As needed: Review MCP logs
- [ ] Before major tasks: Verify all MCPs operational

### Troubleshooting Checklist

- [ ] Check `shannon check-mcps`
- [ ] View logs: `shannon mcp logs <name>`
- [ ] Verify config: `shannon mcp validate-config`
- [ ] Try restart: `shannon mcp restart <name>`
- [ ] Reinstall if needed: `shannon mcp install <name> --force`

---

**Shannon CLI V3.0** - MCP integration for powerful, extensible AI development.

*Last Updated: 2025-11-14*
