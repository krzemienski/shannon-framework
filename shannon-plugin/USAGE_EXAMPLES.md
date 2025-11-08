# Shannon Framework V4.1 - Usage Examples

**Version**: 4.1.0
**Last Updated**: 2025-11-08

---

## Quick Reference

| Use Case | Command | Time |
|----------|---------|------|
| Analyze specification | `/sh_spec "..."` | 30-60s |
| Prime session | `/shannon:prime` | <60s |
| Discover skills | `/sh_discover_skills` | <10ms (cached) |
| Execute wave | `/sh_wave 1` | Variable |
| Create checkpoint | `/sh_checkpoint "name"` | ~5s |
| Restore checkpoint | `/sh_restore "name"` | ~10s |

---

## Example 1: Simple Project (Complexity <0.50)

**Scenario**: Build a contact form with email validation

```bash
# 1. Analyze specification
/sh_spec "Build a contact form with name, email, message fields. Email must be validated. Send to backend API endpoint. Show success/error messages."

# Output:
# Complexity: 0.35 (SIMPLE)
# Domains: Frontend (70%), Backend (30%)
# Recommendation: Direct implementation
# Duration: 2-4 hours

# 2. Set goal (optional)
/sh_north_star "Deploy contact form by end of day"

# 3. Implement directly
# [Implement React form, validation, API integration]

# 4. Generate functional tests
/sh_test --create --platform web --feature "contact form"

# Done! No waves needed for simple projects.
```

---

## Example 2: Medium Project (Complexity 0.50-0.70)

**Scenario**: Build task management app

```bash
# 1. Analyze specification
/sh_spec "Build task management web app. Features: user authentication, create/edit/delete tasks, task status (todo/in-progress/done), due dates, priority levels, task filtering, user dashboard showing task statistics."

# Output:
# Complexity: 0.58 (COMPLEX)
# Domains: Frontend (40%), Backend (35%), Database (15%), Security (10%)
# Recommendation: 2 waves
# Duration: 1-2 weeks

# 2. Shannon auto-generates wave plan
# Wave 1: Core functionality (auth, CRUD, database)
# Wave 2: Enhanced features (filtering, dashboard, statistics)

# 3. Set North Star
/sh_north_star "Launch beta to 20 users by end of month"

# 4. Create initial checkpoint
/sh_checkpoint "project-start"

# 5. Execute Wave 1
/sh_wave 1 --plan  # Review plan first
/sh_wave 1         # Execute
# WAVE_COORDINATOR activates
# Agents: BACKEND, FRONTEND, DATABASE_ARCHITECT, SECURITY

# 6. Check progress
/sh_status
# Shows: Wave 1 complete, Wave 2 ready

# 7. Execute Wave 2
/sh_wave 2

# 8. Final checkpoint
/sh_checkpoint "mvp-complete"
```

---

## Example 3: Complex Project (Complexity >=0.70)

**Scenario**: Build e-commerce platform

```bash
# 1. Analyze specification
/sh_spec "Build complete e-commerce platform. Features: product catalog with search/filtering, shopping cart, checkout with Stripe, order management, inventory tracking, admin dashboard, customer accounts, order history, email notifications, analytics dashboard."

# Output:
# Complexity: 0.75 (VERY COMPLEX)
# Domains: Frontend (30%), Backend (25%), Database (20%), Payments (15%), DevOps (10%)
# Recommendation: 4 waves
# Duration: 4-8 weeks

# 2. Set ambitious North Star
/sh_north_star "Process $10k revenue within first month"

# 3. Review detailed wave breakdown
# Wave 1: Core commerce (products, cart, checkout)
# Wave 2: User management (accounts, auth, orders)
# Wave 3: Admin tools (dashboard, inventory, analytics)
# Wave 4: Optimization (performance, monitoring, deployment)

# 4. Create project checkpoint
/sh_checkpoint "project-init"

# 5. Execute waves sequentially
/sh_wave 1 --plan
/sh_wave 1  # ~1-2 weeks
/sh_checkpoint "wave-1-complete"

/sh_wave 2 --plan
/sh_wave 2  # ~1-2 weeks
/sh_checkpoint "wave-2-complete"

# 6. If context compaction happens:
# Shannon auto-checkpoints via PreCompact hook
# Resume with:
/shannon:prime --resume

# 7. Continue remaining waves
/sh_wave 3
/sh_wave 4

# 8. Final production checkpoint
/sh_checkpoint "production-ready"
```

---

## Example 4: V4.1 Feature - Forced Reading Protocol

**Scenario**: Analyze 2,000-line specification completely

```bash
# 1. Prime session with V4.1 enhancements
/shannon:prime

# V4.1 activates forced reading for /sh_spec

# 2. Analyze large specification
/sh_spec @path/to/large-spec.md

# Shannon enforces (via FORCED_READING_PROTOCOL):
# Step 1: Count lines (2,000 lines detected)
# Step 2: Read ALL 2,000 lines sequentially
# Step 3: Verify completeness (100%)
# Step 4: Sequential MCP synthesis (200+ thoughts)
# Step 5: Present analysis

# Result: Guaranteed complete understanding
# NO skimming, NO "relevant sections", NO partial reading
```

---

## Example 5: V4.1 Feature - Automatic Skill Discovery

**Scenario**: Discover and use applicable skills automatically

```bash
# 1. Prime session (discovers all skills)
/shannon:prime

# Output:
# 📚 Skills Found: 104
#    Project: 16
#    User: 88
#    Plugin: 0

# 2. Execute command
/sh_spec "Build authentication system"

# Shannon auto-invokes (via skill-discovery):
# 🎯 Auto-Invoked Skills (2 applicable):
#    - spec-analysis (confidence: 0.85)
#    - mcp-discovery (confidence: 0.72)

# 3. Skills guide analysis automatically
# NO manual "check for applicable skills"
# NO forgotten patterns
# 100% applicable skills invoked

# 4. Verify invocation history
/sh_skill_status  # Shows which skills were used
```

---

## Example 6: V4.1 Feature - Session Resumption

**Scenario**: Resume complex project after context loss

**Before V4.1** (6 commands, 15-20 minutes):
```bash
/sh_restore latest-checkpoint
/sh_status
/sh_check_mcps
# Manually load memories...
# Manually reload spec...
# Manually verify state...
```

**With V4.1** (1 command, <60 seconds):
```bash
/shannon:prime

# Automatic 8-step sequence:
# 1. Detects: Resume mode (checkpoint 4 hours old)
# 2. Discovers: 104 skills
# 3. Verifies: All MCPs (Serena ✅, Sequential ✅)
# 4. Restores: Checkpoint (Wave 3/5, 60% complete)
# 5. Loads: 8 relevant memories
# 6. Restores: Spec + plan state
# 7. Prepares: Sequential thinking
# 8. Reports: Complete readiness

# Readiness Report:
# ✅ Context restored
# ✅ Current: "Implement payment integration"
# ✅ Next: "Add Stripe webhooks"
# ✅ Ready to continue

# Result: Immediate productivity (vs 15-20 min setup)
```

---

## Example 7: NO MOCKS Testing

**Scenario**: Test authentication feature

```bash
# 1. Implement feature
# [Implementation code...]

# 2. Generate tests (Shannon enforces NO MOCKS)
/sh_test --create --platform web --feature "authentication"

# Shannon generates:
# ✅ Real browser tests (Puppeteer MCP)
# ✅ Real API requests (actual HTTP)
# ✅ Real database operations (test instance)
# ❌ NO mocks, NO stubs, NO fake objects

# 3. Run tests
npm test

# Tests use:
# - Real browser (Puppeteer)
# - Real backend API
# - Real PostgreSQL instance
# - Real authentication flow

# Result: Confidence tests match production behavior
```

---

## Example 8: Wave Orchestration

**Scenario**: Multi-agent coordination for complex feature

```bash
# 1. Analyze feature
/sh_spec "Add real-time collaboration: WebSocket connections, operational transformation for conflict resolution, presence indicators, cursor tracking, collaborative editing"

# Complexity: 0.68 (COMPLEX)
# Recommendation: 2 waves

# 2. Execute Wave 1 (Foundation)
/sh_wave 1

# WAVE_COORDINATOR activates:
# Spawns agents:
# - BACKEND (WebSocket server)
# - DATABASE_ARCHITECT (Presence storage)
# - FRONTEND (Client-side sockets)
#
# Agents work in parallel:
# - Wave 1 Phase 1: Backend setup
# - Wave 1 Phase 2: Frontend integration
# - Wave 1 Phase 3: Basic testing
#
# Wave 1 complete: ~3-5 days

# 3. Execute Wave 2 (Advanced features)
/sh_wave 2

# Spawns agents:
# - BACKEND (OT algorithm)
# - FRONTEND (Cursor tracking, presence)
# - PERFORMANCE_ENGINEER (WebSocket optimization)
#
# Wave 2 complete: ~4-6 days

# Total: 1-2 weeks with parallel execution
# vs 3-4 weeks sequential
```

---

## Example 9: SITREP Protocol (Multi-Agent)

**Scenario**: Large project requiring coordination

```bash
# 1. Analyze (complexity >=0.70 triggers SITREP)
/sh_spec "Build complete microservices platform..."

# Complexity: 0.82 (CRITICAL)
# SITREP protocol auto-activated

# 2. Execute wave with SITREP
/sh_wave 1

# Each agent reports via SITREP:

# BACKEND Agent SITREP:
# SITUATION: Implementing 3 microservices
# OBJECTIVES: Auth, Users, Products services complete
# PROGRESS: Auth 100%, Users 80%, Products 50%
# BLOCKERS: Products needs database schema from DATABASE_ARCHITECT
# NEXT: Complete Products service (ETA: 2 hours)

# DATABASE_ARCHITECT SITREP:
# SITUATION: Designing 5 schemas
# OBJECTIVES: All schemas designed and validated
# PROGRESS: 4/5 complete (Products schema in progress)
# BLOCKERS: None
# NEXT: Products schema complete (ETA: 30 min)

# WAVE_COORDINATOR:
# "DATABASE_ARCHITECT completing Products schema in 30 min, then BACKEND can proceed. No blockers. On track for wave completion."

# Result: Clear coordination, no duplicate work, efficient execution
```

---

## Example 10: Goal Alignment

**Scenario**: Validate decisions against North Star

```bash
# 1. Set North Star
/sh_north_star "Launch MVP to 100 beta users by Q1 2025"

# 2. During development, make decision
# Agent: "Should I build admin dashboard or user analytics first?"

# 3. Shannon checks alignment (via goal-alignment skill)
# Admin dashboard: 60% alignment (nice-to-have, not MVP)
# User analytics: 85% alignment (helps beta users, MVP-critical)

# Result: Build user analytics first (aligns with North Star)
```

---

## Example 11: Context Preservation & Restoration

**Scenario**: Complex multi-week project with context compaction

```bash
# Week 1:
/sh_spec "..." # Complexity 0.75
/sh_checkpoint "week-1-start"
/sh_wave 1
/sh_wave 2
/sh_checkpoint "week-1-complete"

# Context compaction happens (automatic PreCompact hook)
# Shannon auto-saves checkpoint

# Week 2 (new conversation):
/shannon:prime --resume

# Shannon restores:
# ✅ Specification
# ✅ Complexity analysis (0.75)
# ✅ North Star goal
# ✅ Wave progress (2/4 complete)
# ✅ Next: Wave 3
# ✅ All memories loaded

# Continue where you left off:
/sh_wave 3  # No re-explanation needed
```

---

## Example 12: Cross-Validation with Confidence Check

**Scenario**: Ensure implementation readiness

```bash
# 1. Complete implementation
# [Code written...]

# 2. Run confidence check
/sh_analyze --confidence

# Shannon checks (via confidence-check skill):
# ✅ Specification coverage: 95%
# ✅ Tests coverage: 90%
# ✅ Documentation: 85%
# ⚠️  Error handling: 60%
# ❌ Edge cases: 40%

# Overall confidence: 72% (MEDIUM - needs improvement)

# 3. Address gaps
# Focus on: Error handling + edge cases

# 4. Re-check
/sh_analyze --confidence

# Overall confidence: 92% (HIGH - ready for deployment)
```

---

## Example 13: MCP Discovery

**Scenario**: Get MCP recommendations for project

```bash
# 1. Analyze specification
/sh_spec --mcps "Build real-time collaboration app with WebSockets, video calls, screen sharing"

# Shannon recommends (via mcp-discovery skill):

# REQUIRED:
# ✅ Serena MCP - Context preservation
# ✅ Puppeteer MCP - Browser testing

# RECOMMENDED:
# 📦 WebRTC MCP - Video/audio integration
# 📦 Socket.io MCP - WebSocket management

# CONDITIONAL:
# ⚙️  Redis MCP - If using Redis for presence
# ⚙️  PostgreSQL MCP - If using Postgres

# 2. Setup recommended MCPs
# [Install WebRTC MCP, Socket.io MCP]

# 3. Re-run spec analysis
/sh_spec --mcps "..."

# Now shows:
# ✅ WebRTC MCP - Connected
# ✅ Socket.io MCP - Connected
```

---

## Example 14: Project Indexing (Token Efficiency)

**Scenario**: Analyze large codebase efficiently

```bash
# 1. Without indexing (expensive):
/sh_analyze large-project/
# Reads all files: ~150,000 tokens

# 2. With indexing (efficient):
/sh_analyze large-project/ --index

# Shannon uses project-indexing skill:
# - Creates SHANNON_INDEX.md (3,000 tokens)
# - 94% compression (3K vs 58K tokens)
# - Same analysis quality

# Result: 20x token savings
```

---

## Example 15: Complete V4.1 Workflow

**Scenario**: Using all three V4.1 enhancements together

```bash
# SESSION START

# 1. Prime session (Enhancement #3: Unified Prime)
/shannon:prime

# Executes 8 steps automatically:
# ✅ Skill discovery (Enhancement #2: finds all 104 skills)
# ✅ MCP verification
# ✅ Forced reading activation (Enhancement #1)
# ✅ Ready in 42 seconds

# 2. Analyze specification (Enhancement #1: Forced Reading)
/sh_spec @path/to/spec.md  # 2,500 lines

# Shannon enforces:
# - Counts: 2,500 lines
# - Reads: ALL 2,500 lines sequentially
# - Verifies: 100% completeness
# - Synthesizes: 250 Sequential MCP thoughts
# - Presents: Complete 8D analysis

# 3. Auto-skill invocation (Enhancement #2: Skills)
# Shannon auto-invoked:
# 🎯 spec-analysis (confidence: 0.95)
# 🎯 mcp-discovery (confidence: 0.78)
# 🎯 confidence-check (confidence: 0.72)

# 4. Execute with all enhancements active
/sh_wave 1

# Wave execution with:
# ✅ Complete reading of wave plan (Enhancement #1)
# ✅ Auto-invoked skills (Enhancement #2: wave-orchestration, sitrep-reporting)
# ✅ Fast resumption if context lost (Enhancement #3: /shannon:prime)

# Result: Highest quality execution with maximum efficiency
```

---

## Tips & Best Practices

### Always Prime at Session Start

```bash
# First command in new conversation:
/shannon:prime

# Benefits:
# - All skills discovered
# - All MCPs verified
# - Forced reading active
# - Context restored (if applicable)
```

### Use Checkpoints Liberally

```bash
# Before major milestones:
/sh_checkpoint "wave-1-complete"
/sh_checkpoint "feature-complete"
/sh_checkpoint "pre-deployment"

# After context loss:
/shannon:prime --resume  # Auto-restores latest
```

### Let Skills Guide You

```bash
# Don't skip skill discovery:
/sh_discover_skills

# Shannon auto-invokes applicable skills
# Trust the confidence scoring (>=0.70 means use it)
```

### Follow NO MOCKS Philosophy

```bash
# Always use functional testing:
/sh_test --create --platform web  # Generates Puppeteer tests
/sh_test --create --platform api  # Generates real HTTP tests

# NEVER:
# - @mock decorators
# - jest.fn() mocking
# - Stub objects
```

---

## Common Patterns

### Pattern 1: Spec → Wave → Test → Deploy

```bash
/sh_spec "..."           # Analyze
/sh_wave 1              # Implement
/sh_test --create       # Test
/sh_checkpoint "v1.0"   # Save
```

### Pattern 2: Prime → Spec → Multi-Wave → Deploy

```bash
/shannon:prime                # Start fresh
/sh_spec "..."               # Complex analysis
/sh_north_star "Q1 launch"  # Set goal
/sh_wave 1                   # Execute
/sh_wave 2                   # Continue
/sh_checkpoint "release"     # Finalize
```

### Pattern 3: Resume → Continue → Complete

```bash
/shannon:prime --resume      # Restore everything
/sh_status                   # Check progress
/sh_wave N                   # Continue from Wave N
/sh_checkpoint "complete"    # Final state
```

---

## Advanced Usage

### Custom Wave Structure

```bash
# Override auto-generated wave plan:
/sh_wave 1 --custom --phases 4

# Define custom phases within wave
```

### Selective Skill Invocation

```bash
# Discover specific skills:
/sh_discover_skills --filter authentication

# Manually invoke skill:
Skill("spec-analysis")
```

### Deep Analysis Mode

```bash
# Ultra-thorough specification analysis:
/sh_spec --deep --mcps --save "..."

# Enables:
# - Deep domain analysis (10+ domains)
# - Complete MCP recommendations
# - Auto-save to Serena MCP
```

---

## Integration Examples

### With Git Workflows

```bash
# Feature branch workflow:
git checkout -b feature/new-feature
/sh_spec "feature requirements"
/sh_wave 1
/sh_checkpoint "feature-complete"
git add . && git commit -m "feat: implement feature"
git checkout main
```

### With CI/CD

```bash
# Pre-deployment validation:
/sh_analyze --confidence
# Must reach >=90% confidence before deploy

/sh_test --verify
# All functional tests must pass

/sh_checkpoint "pre-deploy-$(date +%Y%m%d)"
```

---

## Troubleshooting Examples

### Example: Skill Not Found

```bash
# Problem:
/sh_spec "..." # spec-analysis skill not loading

# Diagnosis:
/sh_discover_skills --refresh  # Rebuild cache

# Verify:
/sh_discover_skills --filter spec
# Should show: spec-analysis found
```

### Example: Checkpoint Restoration Failed

```bash
# Problem:
/shannon:prime --resume
# Error: Checkpoint corrupted

# Solution:
/shannon:prime --fresh  # Start fresh instead
/sh_restore "earlier-checkpoint"  # Or restore specific checkpoint
```

---

**Shannon Framework V4.1.0** - Usage Examples
**For More**: See shannon-plugin/README.md
