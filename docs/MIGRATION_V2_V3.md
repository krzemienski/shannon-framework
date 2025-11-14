# Shannon CLI V2 to V3 Migration Guide

**Version**: V2.0 → V3.0 | **Date**: 2025-11-14 | **Breaking Changes**: None

> Complete guide for upgrading from Shannon CLI V2.0 to V3.0

---

## Table of Contents

1. [Overview](#overview)
2. [What's New in V3](#whats-new-in-v3)
3. [Breaking Changes](#breaking-changes)
4. [Migration Steps](#migration-steps)
5. [Feature Comparison](#feature-comparison)
6. [Behavioral Changes](#behavioral-changes)
7. [Migration Checklist](#migration-checklist)

---

## Overview

### Executive Summary

Shannon CLI V3.0 is a **100% backward-compatible** upgrade that adds powerful new capabilities while preserving all V2 functionality.

**Good News**:
- All V2 commands work exactly the same
- All V2 sessions remain accessible
- All V2 configurations still valid
- Zero code changes required

**New Capabilities**:
- Live metrics dashboard with 4 Hz refresh
- 3-tier intelligent caching (50-80% cost savings)
- Automatic MCP detection and installation
- Context management for existing codebases
- Agent state tracking with pause/resume
- Smart model selection and budget enforcement
- Historical analytics database

**Migration Time**: 5-10 minutes
**Risk Level**: Very Low (backward compatible)

---

## What's New in V3

### V3.0 Feature Overview

#### 1. Live Metrics Dashboard

**V2 Behavior**:
```bash
shannon analyze spec.md
# Static progress bar
[████████████░░░░░░░░] 60%
```

**V3 Behavior**:
```bash
shannon analyze spec.md
# Live dashboard with 4 Hz refresh
┌─────────────────────────────────────────────────────────────┐
│ SHANNON LIVE DASHBOARD                                      │
├─────────────────────────────────────────────────────────────┤
│ Progress: [████████████░░░░░░░░] 60%                       │
│ Metrics:                                                    │
│   Input Tokens:  8,450                                      │
│   Output Tokens: 4,120                                      │
│   Total Cost:    $0.24                                      │
│   Model:         claude-sonnet-4                            │
│   Time Elapsed:  3m 42s                                     │
│   ETA:           2m 15s                                     │
│ Controls: Enter=expand Esc/q=quit p=pause                   │
└─────────────────────────────────────────────────────────────┘
```

**Enable/Disable**:
```bash
# Disable if terminal issues
shannon config set metrics.enabled false

# Use V2-style static progress
shannon analyze spec.md --auto
```

---

#### 2. Intelligent Caching System

**V2 Behavior**:
```bash
# Every analysis hits Claude API
shannon analyze spec.md  # Cost: $1.20
shannon analyze spec.md  # Cost: $1.20 (duplicate)
# Total: $2.40
```

**V3 Behavior**:
```bash
# First analysis creates cache
shannon analyze spec.md  # Cost: $1.20, Cache: MISS

# Second analysis uses cache
shannon analyze spec.md  # Cost: $0.00, Cache: HIT
# Total: $1.20 (50% savings)
```

**Cache Management**:
```bash
# View statistics
shannon cache stats

# Clear if needed
shannon cache clear

# Disable caching
shannon config set cache.enabled false
```

---

#### 3. MCP Auto-Installation

**V2 Behavior**:
```bash
# Manual MCP setup required
# User must install MCPs via Claude Code UI
```

**V3 Behavior**:
```bash
# Automatic detection and installation
shannon analyze spec.md

# Output:
# Analysis complete
# MCPs Recommended: 3
#   Installing filesystem... ✓
#   Installing postgres... ✓
#   Installing git... ✓

# Verify MCPs
shannon check-mcps
```

**Disable Auto-Installation**:
```bash
shannon config set mcp.auto_install false
```

---

#### 4. Context Management

**V2 Behavior**:
```bash
# No context awareness
shannon analyze spec.md
# Complexity: 0.45 (Medium)
```

**V3 Behavior**:
```bash
# Onboard existing codebase
shannon onboard /path/to/project --project-id my-app

# Analysis with context
shannon analyze spec.md --project-id my-app
# Complexity: 0.28 (Low) - 38% reduction!
# Context: Loaded 142 files
```

**Optional Feature**:
Context management is completely optional. If you don't use `--project-id`, V3 behaves exactly like V2.

---

#### 5. Agent State Tracking

**V2 Behavior**:
```bash
# No visibility into agent states
shannon wave "implement feature"
# Black box - can't pause/resume
```

**V3 Behavior**:
```bash
# Full agent visibility
shannon wave "implement feature"

# Live dashboard shows:
# Wave 2/3: Agent BACKEND - 🟢 Active
# Controls: p=pause r=resume

# Pause execution
# Press 'p' key

# Resume later
# Press 'r' key

# Check agent states
shannon agent status
```

---

#### 6. Smart Model Selection

**V2 Behavior**:
```bash
# Always uses claude-sonnet-4
shannon analyze spec.md
# Model: claude-sonnet-4 ($3.00/M tokens)
```

**V3 Behavior**:
```bash
# Automatic selection based on complexity
shannon analyze simple-spec.md
# Complexity: 0.25 → Model: claude-haiku-4 ($0.25/M tokens)
# Cost: $0.30 (vs. $2.40 with Sonnet - 87% savings!)

shannon analyze complex-spec.md
# Complexity: 0.75 → Model: claude-opus-4 ($15.00/M tokens)

# Manual override still works
shannon analyze spec.md --model claude-opus-4
```

**Disable Smart Selection**:
```bash
shannon config set optimization.auto_select false
shannon config set optimization.default_model claude-sonnet-4
```

---

#### 7. Budget Enforcement

**V2 Behavior**:
```bash
# No budget limits
shannon wave "implement everything"
# Runs to completion regardless of cost
```

**V3 Behavior**:
```bash
# Set budget limits
shannon config set budget.max_tokens 100000

# Pre-wave check
shannon wave "implement everything"
# ⚠️ Estimated: 150,000 tokens (exceeds budget)
# Continue anyway? [y/N]

# Automatic pause at threshold
# Dashboard: ⚠️ Budget 95% consumed - paused
```

**Disable Budget Enforcement**:
```bash
shannon config set budget.max_tokens 0  # Unlimited
```

---

#### 8. Historical Analytics

**V2 Behavior**:
```bash
# No historical tracking
# Sessions stored but not analyzed
```

**V3 Behavior**:
```bash
# SQLite database tracks all sessions
shannon analytics costs --last 30d

# Output:
# Total: $127.40
# Average per session: $3.18
# Cache savings: $45.80 (36%)
# Top project: my-app ($65.40)

# Trend analysis
shannon analytics trends --metric cost
```

**Database Location**: `~/.shannon/analytics.db`

---

## Breaking Changes

### None!

V3.0 has **zero breaking changes**. All V2 commands, options, and behaviors are preserved.

**Verified Compatibility**:
```bash
# All V2 commands work identically
shannon analyze spec.md          # ✓ Works
shannon wave "request"            # ✓ Works
shannon status                    # ✓ Works
shannon config                    # ✓ Works
shannon setup                     # ✓ Works
shannon test                      # ✓ Works
shannon reflect                   # ✓ Works
shannon checkpoint "name"         # ✓ Works
shannon restore cp_id             # ✓ Works
shannon sessions                  # ✓ Works
```

**V2 Sessions**:
```bash
# All V2 sessions remain accessible
shannon sessions
# Shows both V2 and V3 sessions

shannon status --session-id v2_session_id
# V2 sessions work perfectly
```

**V2 Configuration**:
```bash
# V2 config.json automatically upgraded
# Old settings preserved
# New settings added with defaults
```

---

## Migration Steps

### Step 1: Backup (Recommended)

```bash
# Backup V2 configuration
cp ~/.shannon/config.json ~/.shannon/config.json.v2.backup

# Backup V2 sessions
tar -czf shannon-v2-sessions.tar.gz ~/.shannon/sessions/

# Backup location
# ~/.shannon/config.json.v2.backup
# ~/shannon-v2-sessions.tar.gz
```

---

### Step 2: Upgrade Shannon CLI

```bash
# Upgrade via pip
pip install --upgrade shannon-cli

# Verify version
shannon --version
# Shannon CLI v3.0.0

# Check upgrade successful
shannon diagnostics
```

---

### Step 3: Run Setup Wizard (Optional but Recommended)

```bash
# Interactive V3 setup
shannon setup

# Wizard will:
# 1. Verify Python 3.10+             ✓
# 2. Check Claude Agent SDK          ✓
# 3. Verify Shannon Framework        ✓
# 4. Install recommended MCPs        ← New in V3
# 5. Initialize analytics database   ← New in V3
# 6. Test live metrics               ← New in V3
# 7. Verify configuration            ✓
```

**Setup is optional** - V3 works without it, but recommended for full feature access.

---

### Step 4: Test V2 Compatibility

```bash
# Test V2 sessions still work
shannon sessions
# Should show all V2 and V3 sessions

# Test V2 session status
shannon status --session-id <v2-session-id>
# Should display V2 session details

# Test V2 commands
shannon analyze test-spec.md
# Should work with V3 enhancements
```

---

### Step 5: Configure V3 Features (Optional)

```bash
# Enable/configure V3 features as desired

# Caching (recommended)
shannon config set cache.enabled true
shannon config set cache.max_size_mb 500

# Metrics (recommended)
shannon config set metrics.enabled true
shannon config set metrics.refresh_rate_hz 4

# MCP auto-install (recommended)
shannon config set mcp.auto_install true

# Budget enforcement (optional)
shannon config set budget.max_tokens 100000

# Smart model selection (recommended)
shannon config set optimization.auto_select true

# Context management (optional - use when needed)
# No configuration needed - use on-demand
```

---

### Step 6: Verify Installation

```bash
# Run comprehensive diagnostics
shannon diagnostics --deep

# Expected output:
# ✅ Shannon CLI v3.0.0
# ✅ V2 sessions accessible
# ✅ V3 features initialized
# ✅ Cache system operational
# ✅ Analytics database ready
# ✅ MCP system ready
# ✅ Metrics system operational
```

---

## Feature Comparison

### Command-by-Command Comparison

| Command | V2 | V3 | Notes |
|---------|----|----|-------|
| `shannon analyze` | Static progress | Live metrics, caching | Backward compatible |
| `shannon wave` | Basic execution | Live dashboard, agent tracking | Backward compatible |
| `shannon status` | Session info | Session + analytics | More detailed |
| `shannon config` | Basic config | Extended settings | All V2 settings preserved |
| `shannon setup` | Basic setup | MCP installation | Enhanced wizard |
| `shannon sessions` | List sessions | List + analytics | More information |
| `shannon checkpoint` | Basic checkpoint | Enhanced metadata | Backward compatible |
| `shannon restore` | Basic restore | Verification | Safer restoration |
| `shannon test` | Run tests | Run + metrics | Live monitoring |
| `shannon reflect` | Gap analysis | Gap + suggestions | More detailed |
| `shannon cache` | N/A | **New** | Cache management |
| `shannon onboard` | N/A | **New** | Context onboarding |
| `shannon prime` | N/A | **New** | Context priming |
| `shannon update` | N/A | **New** | Context updates |
| `shannon check-mcps` | N/A | **New** | MCP verification |
| `shannon mcp` | N/A | **New** | MCP management |
| `shannon analytics` | N/A | **New** | Historical insights |
| `shannon agent` | N/A | **New** | Agent control |

---

### Output Format Comparison

#### Analyze Command

**V2 Output**:
```
Complexity Analysis: 0.35

Dimension Scores:
- Scope: 0.30
- Algorithms: 0.40
- Integration: 0.35
...

Estimated: 2 waves, ~4.2 hours
```

**V3 Output**:
```
🎯 Complexity Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall Complexity: 0.35 (Medium)

Dimension Scores:
├─ Scope:         0.30 (Narrow)
├─ Algorithms:    0.40 (Standard)
├─ Integration:   0.35 (Few systems)
...

Recommendations:
├─ Waves:          2 waves recommended
├─ Time Estimate:  ~4.2 hours
├─ Model:          claude-sonnet-4        ← New
├─ Cost Estimate:  $2.40                  ← New

MCPs Auto-Installed:                       ← New
├─ ✓ filesystem
├─ ✓ postgres
└─ ✓ git

Cache: MISS → Saved for future reuse      ← New
Context: Not loaded                        ← New
```

**Both formats available**:
```bash
# V3 enhanced format (default)
shannon analyze spec.md

# V2-style simple output
shannon analyze spec.md --simple

# JSON output (both versions)
shannon analyze spec.md --json
```

---

#### Status Command

**V2 Output**:
```
Session: abc123
Created: 2025-11-14 10:30
Complexity: 0.35
Waves: 2/2 complete
```

**V3 Output**:
```
📊 Session Status: abc123
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Created: 2025-11-14 10:30:45
Project: my-app (context loaded)          ← New

Complexity Analysis:
├─ Overall: 0.35 (Medium)
├─ Waves: 2 planned
└─ Estimate: ~4.2 hours, $2.40

Wave Progress:
├─ Wave 1: ✓ Complete (45m, $1.20)
└─ Wave 2: ✓ Complete (38m, $1.05)

Metrics:                                   ← New
├─ Total Tokens: 45,200
├─ Total Cost: $2.25
├─ Cache Hits: 3/5 (60%)
└─ Context: 142 files loaded

Status: ✓ Complete
```

---

## Behavioral Changes

### Changes That Enhance Behavior (No Breaking)

#### 1. Cache-Aware Analysis

**V2**: Every `shannon analyze` makes fresh API call

**V3**: Checks cache first, uses cached result if valid

**Impact**: 50-80% cost reduction for repeated analyses

**Opt-out**:
```bash
# Disable caching
shannon config set cache.enabled false

# Or skip cache per-command
shannon analyze spec.md --no-cache
```

---

#### 2. MCP Auto-Installation

**V2**: User must manually install MCPs

**V3**: Automatically installs recommended MCPs after analysis

**Impact**: Better first-run experience, fewer manual steps

**Opt-out**:
```bash
shannon config set mcp.auto_install false
```

---

#### 3. Live Progress Updates

**V2**: Static progress bar updated every ~5 seconds

**V3**: Live dashboard updated 4 times per second

**Impact**: Better visibility, more responsive

**Opt-out**:
```bash
# Use simple mode
shannon analyze spec.md --auto

# Or disable metrics
shannon config set metrics.enabled false
```

---

#### 4. Model Selection

**V2**: Always uses `claude-sonnet-4`

**V3**: Selects model based on complexity:
- Low (<0.30) → Haiku
- Medium (0.30-0.60) → Sonnet
- High (>0.60) → Opus

**Impact**: 30-50% cost reduction for simple tasks

**Opt-out**:
```bash
# Disable auto-selection
shannon config set optimization.auto_select false

# Force specific model
shannon config set optimization.default_model claude-sonnet-4
```

---

#### 5. Session Storage

**V2**: Sessions stored as individual JSON files

**V3**: Sessions stored as JSON + recorded in analytics database

**Impact**: Historical tracking and insights

**Note**: V2 sessions NOT migrated to database automatically (only new V3 sessions)

**Migration**:
```bash
# Optional: Migrate V2 sessions to database
shannon analytics migrate-v2-sessions

# This is optional - V2 sessions work fine without migration
```

---

## Migration Checklist

### Pre-Migration

- [ ] Backup V2 configuration: `cp ~/.shannon/config.json ~/.shannon/config.json.v2.backup`
- [ ] Backup V2 sessions: `tar -czf shannon-v2-sessions.tar.gz ~/.shannon/sessions/`
- [ ] Note custom configuration settings
- [ ] Document active session IDs

---

### Migration

- [ ] Upgrade Shannon CLI: `pip install --upgrade shannon-cli`
- [ ] Verify version: `shannon --version` shows v3.0.0
- [ ] Run diagnostics: `shannon diagnostics`
- [ ] Run setup wizard: `shannon setup` (optional but recommended)

---

### Post-Migration Testing

- [ ] Test V2 sessions accessible: `shannon sessions`
- [ ] Test V2 session status: `shannon status --session-id <v2-id>`
- [ ] Test analyze command: `shannon analyze test-spec.md`
- [ ] Test wave command: `shannon wave "simple test"`
- [ ] Verify live metrics working: Check dashboard displays
- [ ] Test cache system: Run same analysis twice, verify cache hit

---

### V3 Feature Adoption

**Immediate (Recommended)**:
- [ ] Enable caching: `shannon config set cache.enabled true`
- [ ] Enable metrics: `shannon config set metrics.enabled true`
- [ ] Enable MCP auto-install: `shannon config set mcp.auto_install true`
- [ ] Install recommended MCPs: `shannon setup`

**As Needed (Optional)**:
- [ ] Onboard existing projects: `shannon onboard /path/to/project --project-id my-app`
- [ ] Set budget limits: `shannon config set budget.max_tokens 100000`
- [ ] Review analytics: `shannon analytics costs`

---

### Verification

- [ ] Run comprehensive diagnostics: `shannon diagnostics --deep`
- [ ] Verify all systems operational
- [ ] Test full workflow: `shannon task test-spec.md`
- [ ] Check cache statistics: `shannon cache stats`
- [ ] Review analytics: `shannon analytics costs`

---

## Common Migration Scenarios

### Scenario 1: Minimal Upgrade

**Goal**: Upgrade to V3 but keep V2 behavior

```bash
# 1. Upgrade
pip install --upgrade shannon-cli

# 2. Disable V3 features
shannon config set cache.enabled false
shannon config set metrics.enabled false
shannon config set mcp.auto_install false
shannon config set optimization.auto_select false

# 3. Use V2-style commands
shannon analyze spec.md --auto
shannon wave "request" --auto

# Result: V3 installed but behaves like V2
```

---

### Scenario 2: Gradual Adoption

**Goal**: Enable V3 features incrementally

```bash
# Week 1: Enable caching only
shannon config set cache.enabled true
# Test and monitor cache hit rate

# Week 2: Enable metrics
shannon config set metrics.enabled true
# Get familiar with live dashboard

# Week 3: Enable MCP auto-install
shannon config set mcp.auto_install true
shannon setup  # Install MCPs

# Week 4: Enable smart model selection
shannon config set optimization.auto_select true
# Monitor cost savings

# Week 5: Start using context for main project
shannon onboard /path/to/project --project-id main
```

---

### Scenario 3: Full V3 Adoption

**Goal**: Enable all V3 features immediately

```bash
# 1. Upgrade and setup
pip install --upgrade shannon-cli
shannon setup

# 2. Enable all features (done by setup wizard)
# All features enabled by default

# 3. Onboard main projects
shannon onboard /path/to/project1 --project-id proj1
shannon onboard /path/to/project2 --project-id proj2

# 4. Set budget limits
shannon config set budget.max_tokens 200000

# 5. Start using V3
shannon analyze spec.md --project-id proj1
shannon wave "feature" --project-id proj1

# 6. Monitor analytics
shannon analytics costs
```

---

## Rollback Plan

If you encounter issues and need to rollback:

```bash
# 1. Uninstall V3
pip uninstall shannon-cli

# 2. Install V2
pip install shannon-cli==2.0.0

# 3. Restore V2 config
cp ~/.shannon/config.json.v2.backup ~/.shannon/config.json

# 4. V2 sessions still accessible (no changes made)
shannon sessions

# 5. Verify V2 working
shannon diagnostics
```

**Note**: V3 doesn't modify V2 data, so rollback is safe.

---

## FAQ

### Q: Do I need to migrate my V2 sessions?

**A**: No. V2 sessions work perfectly in V3 without migration. Migration to analytics database is optional and only needed if you want historical insights.

---

### Q: Will V3 break my existing scripts?

**A**: No. All V2 commands and options work identically in V3. Scripts using `shannon analyze`, `shannon wave`, etc. will work without changes.

---

### Q: Can I disable V3 features?

**A**: Yes. All V3 features can be disabled via configuration. See "Minimal Upgrade" scenario above.

---

### Q: How do I get V2-style output?

**A**: Use `--simple` flag or `--auto` flag for commands. Or disable metrics: `shannon config set metrics.enabled false`

---

### Q: What happens to my cache if I rollback to V2?

**A**: V3 cache is stored in `~/.shannon/cache/`. If you rollback to V2, cache is simply ignored (V2 doesn't use caching). Re-upgrading to V3 will reuse the cache.

---

### Q: Do I need to reconfigure Claude Code?

**A**: No. V3 uses the same Claude Agent SDK and Shannon Framework as V2. No Claude Code changes needed.

---

### Q: What's the performance impact of V3 features?

**A**: Minimal. Live metrics adds <1% overhead. Caching actually improves performance (cache hits are instant). Context loading adds ~100-500ms but significantly reduces complexity.

---

### Q: Can I use V3 and V2 side-by-side?

**A**: Not recommended. Install either V2 or V3, not both. Use V3 with features disabled if you want V2 behavior.

---

## Support

### Getting Help

- **Documentation**: See `/docs/USER_GUIDE.md` for full V3 documentation
- **Diagnostics**: Run `shannon diagnostics --deep` and include output in bug reports
- **GitHub Issues**: Report problems at github.com/shannon-cli/issues
- **Migration Issues**: Tag with `migration` label

---

### Reporting Issues

If you encounter migration issues:

```bash
# 1. Capture diagnostics
shannon diagnostics --deep --export diagnostics.txt

# 2. Capture configuration
cat ~/.shannon/config.json > config.txt

# 3. Include version info
shannon --version

# 4. Submit GitHub issue with:
#    - diagnostics.txt
#    - config.txt
#    - Version info
#    - Steps to reproduce
```

---

## Summary

### Key Takeaways

1. **Zero Breaking Changes**: V3 is 100% backward compatible with V2
2. **Optional Features**: All V3 features can be disabled if needed
3. **Safe Upgrade**: V2 data preserved, rollback possible
4. **Gradual Adoption**: Enable features incrementally
5. **Cost Savings**: 50-80% cost reduction through caching and optimization

### Recommended Path

```bash
# 1. Backup (5 minutes)
cp ~/.shannon/config.json ~/.shannon/config.json.v2.backup
tar -czf shannon-v2-sessions.tar.gz ~/.shannon/sessions/

# 2. Upgrade (2 minutes)
pip install --upgrade shannon-cli

# 3. Setup (3 minutes)
shannon setup

# 4. Test (2 minutes)
shannon diagnostics
shannon sessions
shannon analyze test-spec.md

# Total: ~12 minutes
```

### Next Steps

1. Complete migration steps above
2. Review V3 features in User Guide
3. Start with caching and metrics (biggest immediate value)
4. Onboard projects as needed
5. Explore analytics and insights

---

**Shannon CLI V3.0** - Enhanced power, zero disruption.

*Last Updated: 2025-11-14*
