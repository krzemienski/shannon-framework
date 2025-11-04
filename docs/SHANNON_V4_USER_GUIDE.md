# Shannon Framework V4 - User Guide

## Welcome to Shannon V4

Shannon Framework V4 is a specification-driven development framework that transforms how you build software. Built on a skill-based architecture, Shannon provides quantitative complexity analysis, intelligent wave orchestration, and functional testing principles to guide you from specification to implementation.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Core Concepts](#core-concepts)
3. [Quick Start Workflow](#quick-start-workflow)
4. [Commands Reference](#commands-reference)
5. [Advanced Workflows](#advanced-workflows)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Prerequisites

- **Claude Code** installed and running
- **Serena MCP** (mandatory) - For context preservation
- **Sequential MCP** (recommended) - For enhanced reasoning
- **Puppeteer MCP** (recommended) - For browser testing
- **Context7 MCP** (optional) - For framework patterns

### Installation

```bash
# Add Shannon marketplace (if not already added)
/plugin marketplace add shannon-framework/shannon

# Install Shannon V4
/plugin install shannon@shannon-framework

# Restart Claude Code

# Verify installation
/sh_status
```

Expected output:
```
Shannon Framework Status
Version: 4.0.0
Status: Ready
MCPs: Serena (connected), Sequential (connected), ...
```

### First-Time Setup

1. **Check MCP Status**
   ```bash
   /sh_check_mcps
   ```
   This shows which MCPs are available and provides installation guidance for missing ones.

2. **Verify Installation**
   ```bash
   /sh_status
   ```
   Confirms Shannon is ready to use.

---

## Core Concepts

### 8D Complexity Analysis

Shannon analyzes specifications across 8 dimensions:

1. **Technical Complexity** (0.0-1.0)
   - Language features, algorithms, architecture patterns
   - Higher scores = more advanced technical challenges

2. **Temporal Complexity** (0.0-1.0)
   - Time-dependent operations, scheduling, real-time processing
   - Higher scores = more timing coordination needed

3. **Integration Complexity** (0.0-1.0)
   - External APIs, third-party services, system boundaries
   - Higher scores = more integration points

4. **Cognitive Complexity** (0.0-1.0)
   - Domain knowledge, business logic, rule complexity
   - Higher scores = more domain expertise needed

5. **Environmental Complexity** (0.0-1.0)
   - Deployment, infrastructure, configuration
   - Higher scores = more operational challenges

6. **Data Complexity** (0.0-1.0)
   - Data structures, transformations, persistence
   - Higher scores = more data modeling needed

7. **Scale Complexity** (0.0-1.0)
   - Performance requirements, concurrency, load handling
   - Higher scores = more scaling challenges

8. **Unknown Complexity** (0.0-1.0)
   - Novel requirements, unclear specifications, research needed
   - Higher scores = more exploration required

**Overall Complexity Score:** Weighted average of all dimensions (0.0-1.0)

### Wave-Based Execution

For complex projects (≥ 0.50 complexity), Shannon organizes work into waves:

- **Wave:** A coordinated phase of development with clear deliverables
- **Duration:** Typically 3-7 days per wave
- **Composition:** Multiple tasks executed in parallel where possible
- **Coordination:** WAVE_COORDINATOR agent orchestrates execution

Benefits:
- Structured approach to complex projects
- Clear milestones and checkpoints
- Parallel execution where dependencies allow
- Progress tracking and visibility

### Context Preservation

Shannon never loses context:

- **Checkpoints:** Save project state at any time
- **Restoration:** Restore complete context in new conversations
- **Serena MCP Integration:** All state persists across sessions
- **Zero Manual Re-entry:** Never re-explain your project

### NO MOCKS Philosophy

Shannon's testing philosophy:

- **Functional Tests Only:** Test real implementations, not mocks
- **Real Environments:** Use Puppeteer MCP for browser testing
- **Actual APIs:** Test real endpoints, not simulated responses
- **Test Guardian:** Enforces NO MOCKS principles

Why? Mocks test mock behavior, not real behavior. Shannon validates actual functionality.

---

## Quick Start Workflow

### Simple Project (< 0.50 complexity)

```bash
# 1. Analyze specification
/sh_spec "Build a contact form with email validation"

# Output shows low complexity (< 0.50)
# Shannon provides direct implementation guidance

# 2. Implement directly
# Follow recommendations in analysis

# 3. Test implementation
/sh_test --create --platform web --feature "contact form"

# 4. Done!
```

### Complex Project (≥ 0.50 complexity)

```bash
# 1. Analyze specification
/sh_spec "Build e-commerce platform with payment processing, inventory management, and real-time order tracking"

# Output shows high complexity (≥ 0.50)
# Shannon recommends wave-based approach

# 2. Set project goal
/sh_north_star "Launch MVP to 100 beta customers by end of Q1"

# 3. Create initial checkpoint
/sh_checkpoint "project-start"

# 4. Review wave plan
/sh_wave 1 --plan

# 5. Execute wave
/sh_wave 1

# Wave coordinator guides you through implementation
# Creates checkpoints automatically

# 6. Check status
/sh_status

# 7. Continue with next wave
/sh_wave 2 --plan
/sh_wave 2

# 8. Create milestone checkpoint
/sh_checkpoint "mvp-complete"
```

---

## Commands Reference

### Core Commands

#### `/sh_spec` - Analyze Specification

Analyzes your specification using 8D complexity framework.

**Usage:**
```bash
/sh_spec "<your specification>"
```

**Example:**
```bash
/sh_spec "Build REST API with user authentication, CRUD operations, and rate limiting"
```

**Output:**
- Overall complexity score (0.0-1.0)
- Breakdown by dimension
- Domain identification
- Implementation recommendations
- Wave recommendations if complex

---

#### `/sh_wave` - Execute Development Wave

Orchestrates wave-based execution for complex projects.

**Usage:**
```bash
/sh_wave <wave_number> [--plan]
```

**Examples:**
```bash
# Plan wave (preview only)
/sh_wave 1 --plan

# Execute wave
/sh_wave 1

# Continue to next wave
/sh_wave 2
```

**Options:**
- `--plan`: Show wave plan without executing

---

#### `/sh_checkpoint` - Save Project State

Creates a checkpoint of current project state.

**Usage:**
```bash
/sh_checkpoint "<checkpoint_name>"
```

**Examples:**
```bash
/sh_checkpoint "feature-complete"
/sh_checkpoint "before-refactor"
/sh_checkpoint "pre-deployment"
```

**Output:**
- Checkpoint ID
- Saved context summary
- Restoration instructions

---

#### `/sh_restore` - Restore Project State

Restores project context from a checkpoint.

**Usage:**
```bash
/sh_restore "<checkpoint_name>"
```

**Example:**
```bash
/sh_restore "feature-complete"
```

**Output:**
- Restored specification
- Restored goals
- Restored analysis
- Project state summary

---

#### `/sh_status` - Show Project Status

Displays current project state and progress.

**Usage:**
```bash
/sh_status
```

**Output:**
- Shannon version
- Current specification
- Complexity score
- Active wave
- Checkpoints
- North star goal
- MCP status

---

#### `/sh_north_star` - Set Project Goal

Defines your overarching project goal.

**Usage:**
```bash
/sh_north_star "<goal>"
```

**Example:**
```bash
/sh_north_star "Launch MVP to 100 beta users by end of Q1"
```

**Benefits:**
- Keeps team aligned
- Guides prioritization decisions
- Included in checkpoints
- Referenced in wave planning

---

### Utility Commands

#### `/sh_check_mcps` - Check MCP Status

Shows status of all MCPs and provides installation guidance.

**Usage:**
```bash
/sh_check_mcps
```

**Output:**
- Serena MCP status (required)
- Sequential MCP status (recommended)
- Puppeteer MCP status (recommended)
- Context7 MCP status (optional)
- Installation instructions for missing MCPs

---

#### `/sh_memory` - Manage Project Memory

Interacts with Serena MCP memory system.

**Usage:**
```bash
/sh_memory --list              # List all memories
/sh_memory --read "<name>"     # Read specific memory
/sh_memory --write "<name>"    # Write new memory
```

**Examples:**
```bash
# List project memories
/sh_memory --list

# Read architecture decisions
/sh_memory --read "architecture"

# Write new decision
/sh_memory --write "api-design" "REST endpoints documented in api/docs/"
```

---

### Testing & Analysis

#### `/sh_test` - Create Functional Tests

Generates functional tests following NO MOCKS philosophy.

**Usage:**
```bash
/sh_test [--create] [--platform <platform>] [--feature "<feature>"]
```

**Examples:**
```bash
# Create web tests
/sh_test --create --platform web --feature "user login"

# Create API tests
/sh_test --create --platform api --feature "task CRUD"

# Create mobile tests
/sh_test --create --platform mobile --feature "offline sync"
```

**Platforms:**
- `web`: Browser tests using Puppeteer MCP
- `api`: API tests using real HTTP clients
- `mobile`: Mobile app tests using real devices

---

#### `/sh_analyze` - Deep Project Analysis

Performs comprehensive project analysis.

**Usage:**
```bash
/sh_analyze [--domains] [--dependencies] [--risks]
```

**Examples:**
```bash
# Analyze all domains
/sh_analyze --domains

# Analyze dependencies
/sh_analyze --dependencies

# Analyze risks
/sh_analyze --risks
```

---

#### `/sh_scaffold` - Generate Project Scaffolding

Creates initial project structure.

**Usage:**
```bash
/sh_scaffold --framework <framework> [--template <template>]
```

**Examples:**
```bash
# React project
/sh_scaffold --framework react

# Express API
/sh_scaffold --framework express

# Next.js with TypeScript
/sh_scaffold --framework nextjs --template typescript
```

---

## Advanced Workflows

### Multi-Wave Projects

For large, complex projects:

```bash
# 1. Initial analysis
/sh_spec "Build complete SaaS platform..."

# 2. Set long-term goal
/sh_north_star "Launch to 1000 paying customers in 6 months"

# 3. Review all waves
/sh_wave 1 --plan
/sh_wave 2 --plan
/sh_wave 3 --plan

# 4. Execute waves sequentially
/sh_wave 1
/sh_checkpoint "wave-1-complete"

/sh_wave 2
/sh_checkpoint "wave-2-complete"

/sh_wave 3
/sh_checkpoint "wave-3-complete"

# 5. Final status
/sh_status
```

---

### Context Loss Recovery

If you lose context (new conversation, session timeout):

```bash
# 1. Check available checkpoints
/sh_memory --list

# 2. Restore most recent checkpoint
/sh_restore "wave-2-complete"

# 3. Verify restoration
/sh_status

# 4. Continue work
/sh_wave 3
```

---

### Iterative Development

For projects that evolve:

```bash
# 1. Start with initial spec
/sh_spec "Build task manager"
/sh_checkpoint "v1-spec"

# 2. Implement v1
/sh_wave 1

# 3. Refine specification
/sh_spec "Build task manager with collaboration features"
/sh_checkpoint "v2-spec"

# 4. Implement v2 features
/sh_wave 1

# 5. Compare progress
/sh_status
```

---

### Team Coordination

Using Shannon in team environments:

```bash
# 1. Team lead analyzes spec
/sh_spec "Full project specification..."
/sh_north_star "Team goal"
/sh_checkpoint "team-baseline"

# 2. Share checkpoint with team
# Team members restore in their environments

# 3. Each team member works on assigned wave
Developer A: /sh_restore "team-baseline"
Developer A: /sh_wave 1

Developer B: /sh_restore "team-baseline"
Developer B: /sh_wave 2

# 4. Create completion checkpoints
Developer A: /sh_checkpoint "wave-1-complete"
Developer B: /sh_checkpoint "wave-2-complete"

# 5. Team lead integrates
/sh_restore "wave-1-complete"
/sh_restore "wave-2-complete"
```

---

## Best Practices

### Specification Writing

**Good Specifications:**
- Clear, specific requirements
- Include technical details
- Mention constraints
- Specify integrations
- Define success criteria

**Example:**
```
Build REST API for task management:
- User authentication with JWT
- CRUD operations for tasks
- Real-time updates via WebSocket
- PostgreSQL database
- Rate limiting (100 req/min per user)
- Deploy on AWS with auto-scaling
```

**Avoid:**
- Vague descriptions ("Build an app")
- Missing technical details
- Unclear scope
- No success criteria

---

### Checkpoint Strategy

**When to Create Checkpoints:**
- ✅ Before starting major work
- ✅ After completing waves
- ✅ Before risky changes
- ✅ At project milestones
- ✅ Before deployment

**Naming Conventions:**
```bash
/sh_checkpoint "feature-<name>-start"
/sh_checkpoint "feature-<name>-complete"
/sh_checkpoint "wave-<n>-complete"
/sh_checkpoint "pre-deployment"
/sh_checkpoint "v<x>.<y>-release"
```

---

### Wave Execution

**Best Practices:**
- Review wave plan before executing (`--plan` flag)
- Execute waves sequentially, not in parallel
- Create checkpoint after each wave
- Verify wave completion before continuing
- Don't skip waves

**Example:**
```bash
# ✅ Good
/sh_wave 1 --plan     # Review
/sh_wave 1            # Execute
/sh_checkpoint "w1"   # Save
/sh_wave 2 --plan     # Review next
/sh_wave 2            # Execute next

# ❌ Bad
/sh_wave 1 & /sh_wave 2  # Don't parallel execute
/sh_wave 3               # Don't skip waves
```

---

### Testing Philosophy

**Follow NO MOCKS:**
- Use real browsers (Puppeteer MCP)
- Use real APIs (actual endpoints)
- Use real databases (test instances)
- Use real services (dev/staging environments)

**Example:**
```bash
# ✅ Good - Functional test
/sh_test --create --platform web --feature "login"
# Generates: Puppeteer test hitting real login page

# ❌ Bad - Mock test (Shannon won't generate this)
# Mock user service
# Mock database
# Assert mock called
```

---

### Memory Management

**Effective Memory Use:**

```bash
# Save architecture decisions
/sh_memory --write "architecture" "Microservices with event-driven communication"

# Save coding standards
/sh_memory --write "standards" "Use TypeScript strict mode, ESLint, Prettier"

# Save deployment info
/sh_memory --write "deployment" "AWS ECS, RDS PostgreSQL, CloudFront CDN"

# Reference later
/sh_memory --read "architecture"
```

**What to Save:**
- Architecture decisions
- Coding standards
- Deployment procedures
- API patterns
- Testing strategies
- Team conventions

---

### Error Recovery

**If Something Goes Wrong:**

1. **Check Status**
   ```bash
   /sh_status
   ```

2. **Verify MCPs**
   ```bash
   /sh_check_mcps
   ```

3. **Restore Last Good Checkpoint**
   ```bash
   /sh_memory --list
   /sh_restore "last-good-checkpoint"
   ```

4. **Restart Wave if Needed**
   ```bash
   /sh_wave <N>  # Re-execute wave
   ```

---

## Troubleshooting

### Common Issues

#### "Serena MCP not connected"

**Cause:** Serena MCP not installed or not running

**Solution:**
```bash
# Install Serena MCP
npm install -g @anthropic/serena-mcp

# Configure in Claude Code settings
# Restart Claude Code

# Verify
/sh_check_mcps
```

---

#### "Complexity score seems incorrect"

**Cause:** Specification too vague or ambiguous

**Solution:**
- Add more technical details
- Specify integrations explicitly
- Mention performance requirements
- Include deployment constraints
- Re-run analysis:
  ```bash
  /sh_spec "<more detailed specification>"
  ```

---

#### "Wave won't execute"

**Cause:** Missing dependencies or previous wave incomplete

**Solutions:**

1. Check status:
   ```bash
   /sh_status
   ```

2. Verify previous wave complete:
   ```bash
   /sh_wave <N-1> --plan  # Check previous wave
   ```

3. Ensure checkpoint exists:
   ```bash
   /sh_memory --list
   ```

---

#### "Tests not generating"

**Cause:** Puppeteer MCP not available for web tests

**Solution:**
```bash
# Check MCP status
/sh_check_mcps

# Install Puppeteer MCP if missing
# Follow installation instructions provided

# Alternative: Shannon falls back to manual test guidance
```

---

#### "Checkpoint not restoring"

**Cause:** Checkpoint name incorrect or Serena MCP issue

**Solutions:**

1. List available checkpoints:
   ```bash
   /sh_memory --list
   ```

2. Use exact checkpoint name:
   ```bash
   /sh_restore "exact-name-from-list"
   ```

3. Verify Serena MCP connected:
   ```bash
   /sh_check_mcps
   ```

---

### Getting Help

**Resources:**
- Command Reference: `docs/SHANNON_V4_COMMAND_REFERENCE.md`
- Skill Reference: `docs/SHANNON_V4_SKILL_REFERENCE.md`
- Troubleshooting: `docs/SHANNON_V4_TROUBLESHOOTING.md`
- Migration Guide: `docs/SHANNON_V4_MIGRATION_GUIDE.md`

**Support:**
- GitHub Issues: `https://github.com/shannon-framework/shannon/issues`
- Documentation: `https://shannon-framework.dev/docs`
- Community: `https://shannon-framework.dev/community`

---

## Next Steps

Now that you understand Shannon V4:

1. **Try a Simple Project**
   ```bash
   /sh_spec "Build a to-do list app"
   ```

2. **Explore Complex Projects**
   ```bash
   /sh_spec "Build e-commerce platform..."
   /sh_wave 1 --plan
   ```

3. **Learn Advanced Features**
   - Read Command Reference
   - Study Skill Reference
   - Review Migration Guide

4. **Contribute**
   - Report issues
   - Suggest improvements
   - Share use cases

---

**Welcome to Shannon V4!** Build better software with quantitative complexity analysis, intelligent orchestration, and functional testing principles.
