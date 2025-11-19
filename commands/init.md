---
name: shannon:init
description: Comprehensive project onboarding with deep codebase analysis and Shannon infrastructure setup
usage: /shannon:init [--quick] [--full] [--dry-run]
version: "5.5.0"
---

# Shannon Init: Project Onboarding Command

## Overview

**Complete project onboarding** for existing codebases that weren't built with Shannon from the start. Unlike `/shannon:prime` (session priming), `/shannon:init` performs deep codebase analysis, infrastructure setup, and creates a persistent Shannon context for the project.

**Think of it as**: `claude init` + deep codebase analysis + Shannon infrastructure bootstrap

**One command to**:
- ✅ Deep-scan entire codebase (every file analyzed)
- ✅ Set up Serena MCP if not configured
- ✅ Create project index and architecture map
- ✅ Generate Shannon-compatible documentation
- ✅ Configure validation gates (tests, build, lint)
- ✅ Establish baseline metrics
- ✅ Create initial checkpoint
- ✅ Make project "Shannon-ready"

**Key Difference from `/shannon:prime`**:
- **prime**: Session-level (restores context for THIS session)
- **init**: Project-level (one-time setup, persists forever)

---

## Prerequisites

**Minimal**:
- Shannon Framework installed
- Run from project root directory
- Project contains files (not empty)

**Recommended** (auto-configured if missing):
- Serena MCP available

**Auto-Detected**:
- Tech stack
- Build commands
- Test framework
- Project structure

---

## Workflow

### Step 1: Pre-Flight Checks

**Validate environment**:
```
1. Confirm running from project root (check for git, package.json, etc.)
2. Check if project already Shannon-initialized
   - Look for .shannon/ directory
   - If exists: Ask "Re-initialize? (overwrites existing setup)"
3. Verify Serena MCP availability
   - If unavailable: Offer to configure
   - If declined: Continue with limited persistence
4. Estimate project size for time estimate
   - Small (<100 files): 2-3 minutes
   - Medium (100-1000 files): 5-10 minutes
   - Large (1000+ files): 15-30 minutes
   - Huge (10000+ files): 30-60 minutes
```

**Output**:
```markdown
🌊 Shannon Init: Project Onboarding
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Project**: {detected_project_name}
**Location**: {cwd}
**Files**: ~{file_count} files
**Estimated Time**: {time_estimate}

{if serena_unavailable}
⚠️  Serena MCP not detected
   Setup recommended for full Shannon capabilities
   Configure now? (y/n)
{end if}

Proceeding with initialization...
```

### Step 2: Deep Codebase Analysis

**Invoke `@skill project-indexing` with full scan mode**:

```
@skill project-indexing
- Input:
  * mode: "init" (comprehensive scan, not quick index)
  * project_root: {cwd}
  * scan_depth: "complete"
- Options:
  * analyze_all_files: true (EVERY file)
  * detect_architecture: true
  * identify_patterns: true
  * calculate_metrics: true
  * detect_dependencies: true
  * find_entry_points: true
  * map_data_flows: true
- Output: comprehensive_project_index
```

**The skill will**:
1. Scan EVERY file in project (excluding .gitignore)
2. Detect programming languages and percentages
3. Identify frameworks and versions
4. Map directory structure and purpose
5. Find entry points (main files)
6. Detect build system (npm, gradle, cargo, etc.)
7. Identify test framework (jest, pytest, go test, etc.)
8. Calculate complexity metrics per file/module
9. Generate architecture map
10. Estimate technical debt

**Progress display** (live updates):
```
📁 Scanning codebase...
   ├─ src/: 45 files analyzed
   ├─ tests/: 12 files analyzed
   ├─ docs/: 8 files analyzed
   └─ Progress: 65/100 files (65%)
```

### Step 3: Tech Stack Detection

**Invoke `@skill spec-analysis` in detection mode**:

```
@skill spec-analysis
- Input:
  * mode: "detect"
  * project_structure: {from Step 2}
  * languages_detected: {from Step 2}
- Output: tech_stack_profile
```

**Detects**:
- **Frontend**: React 18.2.0, Vite 4.3.0
- **Backend**: Express 4.18.0, Node 18.x
- **Database**: PostgreSQL 15.2 (detected from migrations)
- **Testing**: Jest 29.5.0 (detected from package.json)
- **Build**: npm scripts (package.json), Docker (Dockerfile)
- **Infrastructure**: AWS CDK (detected from cdk.json)

### Step 4: Validation Gates Configuration

**Auto-detect or prompt for validation commands**:

```
Detection Logic:
1. Check package.json "scripts" section for "test", "build", "lint"
2. Check Makefile for test/build targets
3. Check for CI config (.github/workflows, .gitlab-ci.yml)
4. If found: Auto-configure
5. If not found: Prompt user

Prompts (if auto-detection fails):
  - "Test command (e.g., 'npm test', 'pytest', 'go test ./...'): "
  - "Build command (e.g., 'npm run build', 'make build'): "
  - "Lint command (optional) (e.g., 'npm run lint', 'ruff check .'): "
```

**Configure gates**:
```json
{
  "validation_gates": {
    "test": {
      "command": "npm test",
      "required": true,
      "timeout": 300
    },
    "build": {
      "command": "npm run build",
      "required": true,
      "timeout": 600
    },
    "lint": {
      "command": "npm run lint",
      "required": false,
      "timeout": 120
    }
  }
}
```

### Step 5: NO MOCKS Testing Compliance Check

**Invoke `@skill functional-testing` in audit mode**:

```
@skill functional-testing
- Input:
  * mode: "audit"
  * test_directory: {detected_test_dir}
  * test_framework: {detected_framework}
- Options:
  * check_no_mocks: true
  * identify_violations: true
  * suggest_replacements: true
- Output: testing_compliance_report
```

**Checks for**:
- Mock library imports (jest.mock, sinon, pytest mock, etc.)
- Mock usage in tests
- Stub implementations
- Test doubles

**Output**:
```markdown
🧪 Testing Compliance Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Test Framework**: Jest
**Tests Found**: 45 test files, 234 test cases
**NO MOCKS Compliance**: 67% (157/234 tests)

❌ Mock Violations Found: 77 tests
   Top Violations:
   ├─ src/tests/api.test.js: 12 mocked fetch calls
   ├─ src/tests/auth.test.js: 8 mocked database calls
   └─ src/tests/payment.test.js: 15 mocked Stripe API

📋 Recommendations:
   1. Replace mocked fetch with real API (use test server)
   2. Replace mocked database with real test database
   3. Replace mocked Stripe with Stripe test mode

⚠️  Shannon requires NO MOCKS for functional tests
   See: TESTING_PHILOSOPHY.md for migration guide
```

### Step 6: MCP Requirements Analysis

**Invoke `@skill mcp-discovery` with project context**:

```
@skill mcp-discovery
- Input:
  * mode: "recommend"
  * domain_breakdown: {from Step 3}
  * tech_stack: {from Step 3}
  * project_type: {detected_type}
- Output: mcp_recommendations
```

**Generates tiered recommendations**:
```markdown
🔌 Required MCPs for This Project
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TIER 1 - MANDATORY:
✅ Serena MCP - Context preservation (CONNECTED)

TIER 2 - PRIMARY (Based on detected 45% Frontend):
⚠️  Puppeteer MCP - Browser testing (NOT FOUND)
   Purpose: NO MOCKS compliance for React UI tests
   Setup: /shannon:check_mcps --setup puppeteer

⚠️  Context7 MCP - React documentation (NOT FOUND)
   Purpose: Latest React patterns and APIs
   Setup: /shannon:check_mcps --setup context7

TIER 3 - SECONDARY (Based on detected Express backend):
✅ Sequential MCP - Complex debugging (CONNECTED)

📊 MCP Coverage: 2/4 recommended (50%)
   Setup missing MCPs: /shannon:check_mcps
```

### Step 7: Generate Shannon Documentation

**Create project-specific Shannon documentation**:

**Files Created in project root**:

1. **`.shannon/`** directory:
   ```
   .shannon/
   ├─ config.json          # Shannon configuration
   ├─ project-index.json   # Complete codebase index
   ├─ architecture.json    # Architecture map
   ├─ baseline-metrics.json # Initial complexity/debt metrics
   └─ sessions/            # Session checkpoints directory
   ```

2. **`SHANNON.md`** - Project Shannon integration guide:
   ```markdown
   # Shannon Framework Integration

   This project has been initialized with Shannon Framework.

   ## Quick Start

   ```bash
   # Start new session
   /shannon:prime

   # Check project status
   /shannon:status

   # Analyze specification
   /shannon:spec "your task description"

   # Execute with waves
   /shannon:wave
   ```

   ## Project Profile

   - **Complexity**: {detected_complexity}/1.0
   - **Domains**: Frontend (45%), Backend (35%), Database (20%)
   - **Architecture**: {detected_pattern}
   - **Testing**: {test_framework} ({compliance}% NO MOCKS compliant)

   ## Validation Gates

   - **Test**: `{test_command}`
   - **Build**: `{build_command}`
   - **Lint**: `{lint_command}`

   ## MCP Requirements

   {mcp_recommendations_summary}

   ## Next Steps

   1. Configure missing MCPs: `/shannon:check_mcps`
   2. {if low_no_mocks_compliance}Migrate tests to NO MOCKS: See TESTING_PHILOSOPHY.md
   3. Set North Star goal: `/shannon:north_star "your project goal"`
   4. Begin development with Shannon
   ```

3. **`AGENTS.md`** - Agent onboarding context:
   ```markdown
   # Project Context for AI Agents

   ## Architecture Overview

   {architecture_description}

   ## Key Components

   {component_map}

   ## Tech Stack

   {detailed_tech_stack}

   ## Development Workflow

   {workflow_description}

   ## Testing Strategy

   {testing_approach}
   ```

4. **Update `.gitignore`** (add Shannon directories):
   ```
   # Shannon Framework
   .shannon/sessions/
   .shannon/*.log
   ```

### Step 8: Create Initial Checkpoint

**Invoke `@skill context-preservation`**:

```
@skill context-preservation
- checkpoint_name: "shannon-init-baseline"
- context_to_save: [
    "project_index",
    "architecture_map",
    "tech_stack_profile",
    "baseline_metrics",
    "validation_gates",
    "mcp_recommendations",
    "testing_compliance_report"
  ]
- purpose: "Initial Shannon onboarding baseline"
```

**Saves to Serena**:
- Complete project snapshot
- Baseline metrics for future comparison
- Configuration for future sessions

### Step 9: Run Initial Validation (Optional)

**If `--full` flag provided, run validation gates**:

```
1. Run test command: {test_command}
   ├─ Expected: May pass or fail (baseline)
   └─ Record: Test count, pass/fail ratio

2. Run build command: {build_command}
   ├─ Expected: Should pass (project builds)
   └─ Record: Build time, artifacts

3. Run lint command (if configured): {lint_command}
   ├─ Expected: May have violations (baseline)
   └─ Record: Violation count, types
```

**Record baseline results** for future comparison.

### Step 10: Present Summary

**Format comprehensive initialization report**:

```markdown
═══════════════════════════════════════════════════════════════
✅ SHANNON INITIALIZATION COMPLETE
═══════════════════════════════════════════════════════════════

**Project**: {project_name}
**Initialized**: {timestamp}
**Duration**: {init_duration}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 PROJECT PROFILE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Codebase Size**:
├─ Files: {file_count}
├─ Lines of Code: {loc}
└─ Languages: {language_breakdown}

**Architecture**:
├─ Pattern: {architecture_pattern}
├─ Complexity: {complexity_score}/1.0 ({complexity_label})
└─ Technical Debt: {debt_score}/100

**Domains**:
{for each domain}
├─ {domain_name}: {percentage}%

**Tech Stack**:
{tech_stack_summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️  CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Validation Gates**:
✅ Test: `{test_command}`
✅ Build: `{build_command}`
{if lint_configured}✅ Lint: `{lint_command}`{end if}

{if full_validation_run}
**Baseline Results**:
├─ Tests: {test_count} tests, {pass_count} passing ({pass_rate}%)
├─ Build: {build_status} ({build_time}s)
└─ Lint: {violation_count} violations
{end if}

**Testing Compliance**:
├─ Framework: {test_framework}
├─ NO MOCKS Compliance: {compliance_percentage}%
{if compliance_percentage < 80}
└─ ⚠️  Action Required: Migrate {violation_count} mocked tests
{else}
└─ ✅ Good compliance level
{end if}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔌 MCP STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Required**: {required_count}/{required_total} configured
**Primary**: {primary_count}/{primary_total} configured
**Coverage**: {mcp_coverage_percentage}%

{if missing_mcps}
⚠️  Missing MCPs:
{for each missing_mcp}
├─ {mcp_name}: {purpose}
   Setup: /shannon:check_mcps --setup {mcp_name}
{end for}
{else}
✅ All recommended MCPs configured
{end if}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 FILES CREATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ .shannon/config.json           # Shannon configuration
✅ .shannon/project-index.json    # Complete codebase index
✅ .shannon/architecture.json     # Architecture map
✅ .shannon/baseline-metrics.json # Baseline metrics
✅ .shannon/sessions/             # Checkpoints directory
✅ SHANNON.md                     # Shannon integration guide
✅ AGENTS.md                      # Agent onboarding context
✅ .gitignore (updated)           # Shannon directories excluded

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💾 CHECKPOINT CREATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{if serena_available}
✅ Initial checkpoint saved to Serena MCP
   Key: shannon-init-baseline
   Restore: /shannon:restore shannon-init-baseline
{else}
⚠️  Checkpoint saved locally only (Serena MCP not configured)
   Limited restoration capabilities
   Recommendation: Configure Serena MCP
{end if}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Review generated documentation:
   - Read SHANNON.md for project integration guide
   - Review AGENTS.md for architecture context

2. {if missing_mcps}Configure missing MCPs:
   /shannon:check_mcps

3. {end if}{if low_no_mocks_compliance}Migrate mocked tests to NO MOCKS:
   See TESTING_PHILOSOPHY.md for guidance
   Priority: {top_violation_files}

4. {end if}Prime your first Shannon session:
   /shannon:prime

5. Set North Star goal for project:
   /shannon:north_star "your project vision"

6. Start development with Shannon:
   /shannon:do "your first task"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SHANNON READINESS SCORE: {readiness_score}/100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Breakdown:
├─ MCP Coverage: {mcp_score}/30 points
├─ Testing Quality: {testing_score}/25 points
├─ Documentation: {docs_score}/20 points
├─ Validation Gates: {gates_score}/15 points
└─ Architecture Clarity: {arch_score}/10 points

{if readiness_score >= 80}
✅ Project is Shannon-ready!
{else if readiness_score >= 60}
⚠️  Good start, address items in Next Steps
{else}
⚠️  Additional setup recommended (see Next Steps)
{end if}

═══════════════════════════════════════════════════════════════

**Welcome to Shannon Framework** 🌊
Your project is now onboarded and ready for specification-driven development.

Run `/shannon:status` anytime to check Shannon integration health.
═══════════════════════════════════════════════════════════════
```

---

## Command Flags

### --quick
Fast initialization with minimal analysis:
```bash
/shannon:init --quick
```

**Behavior**:
- Scan directory structure only (don't analyze file contents)
- Auto-detect basic tech stack
- Skip compliance checks
- Skip baseline validation
- Time: 30-60 seconds

**Use when**: Quick setup, will refine later

### --full
Comprehensive initialization with validation:
```bash
/shannon:init --full
```

**Behavior**:
- Deep file-by-file analysis
- Run all validation gates (test, build, lint)
- Full compliance audit
- Comprehensive metrics
- Time: 2x standard init time

**Use when**: Production setup, want complete baseline

### --dry-run
Show what would be initialized without executing:
```bash
/shannon:init --dry-run
```

**Behavior**:
- Analyze project
- Show configuration that would be created
- Don't create files
- Don't save checkpoints
- Time: Standard init time (analysis only)

**Use when**: Reviewing before commitment, auditing existing project

---

## Re-Initialization

**If project already Shannon-initialized**:

```bash
/shannon:init --force
```

**Behavior**:
1. Backup existing .shannon/ directory
2. Re-scan project (detects changes since last init)
3. Update configuration
4. Preserve session checkpoints
5. Show delta report (what changed)

**Delta Report Example**:
```markdown
📊 Re-Initialization Delta
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Since Last Init** (15 days ago):
├─ Files Added: 23
├─ Files Modified: 67
├─ Files Deleted: 5
├─ Complexity Change: +0.12 (0.58 → 0.70)
└─ Technical Debt Change: +15 points

**Updated Configuration**:
├─ Tech Stack: React 18.2.0 → React 18.3.0
├─ New Dependencies: 8 added
└─ Test Coverage: 67% → 72% (+5%)

**Recommendation**: Complexity increased to COMPLEX tier
   Consider using wave-based execution for future work
```

---

## Integration with Other Commands

### Shannon Init + Prime Pattern

**Typical workflow for new-to-Shannon project**:

```bash
# Step 1: Initialize project (one-time)
/shannon:init

# Step 2: Prime first session
/shannon:prime

# Step 3: Set goal
/shannon:north_star "Build admin dashboard"

# Step 4: Start work
/shannon:do "implement user management"
```

### Shannon Init + Do Pattern

**After init, `/shannon:do` becomes smarter**:

```bash
# Before init
/shannon:do "add feature X"
# → Does NOT know project context, slow exploration

# After init
/shannon:do "add feature X"
# → Loads cached project index, knows architecture, fast execution
```

**Speedup**: 3-5x faster first-time execution after init

---

## Skill Dependencies

- **project-indexing** (REQUIRED) - Comprehensive codebase scan
- **spec-analysis** (REQUIRED) - Tech stack detection
- **functional-testing** (REQUIRED) - NO MOCKS compliance audit
- **mcp-discovery** (REQUIRED) - MCP recommendations
- **context-preservation** (REQUIRED) - Initial checkpoint

---

## MCP Dependencies

**Required**:
- None (works without MCPs, limited functionality)

**Strongly Recommended**:
- **Serena MCP**: Persistent project context, checkpoints

**Optional**:
- **Sequential MCP**: Deep analysis for complex projects
- **Context7 MCP**: Framework-specific pattern detection

---

## Success Criteria

Shannon Init succeeds when:
- ✅ Every file in project analyzed
- ✅ Tech stack accurately detected
- ✅ Validation gates configured
- ✅ Architecture pattern identified
- ✅ MCP requirements determined
- ✅ Documentation generated (SHANNON.md, AGENTS.md)
- ✅ Initial checkpoint created
- ✅ Shannon Readiness Score >= 60/100

---

## Performance

**Initialization Times by Project Size**:
- Small (<100 files): 2-3 minutes
- Medium (100-1K files): 5-10 minutes
- Large (1K-10K files): 15-30 minutes
- Huge (10K+ files): 30-60 minutes

**With --quick flag**: 50-70% faster

**With --full flag**: 2x slower (includes validation runs)

---

## Comparison: init vs prime

| Aspect | `/shannon:init` | `/shannon:prime` |
|--------|----------------|-----------------|
| **When** | Once per project (onboarding) | Every session (context restore) |
| **Duration** | 5-30 minutes | 30-60 seconds |
| **Scope** | Entire codebase | Session context only |
| **Purpose** | Project setup | Session restoration |
| **Output** | Config files + docs | Loaded context |
| **Persistence** | Permanent (.shannon/ dir) | Session-only (Serena checkpoint) |
| **Frequency** | Once (or rare re-init) | Every session start |

**Analogy**:
- **init**: Installing an operating system
- **prime**: Booting up the computer

---

## Troubleshooting

### "Project too large" Error

**Symptom**: Init times out or runs very slowly

**Solutions**:
1. Use `--quick` flag for faster (less comprehensive) init
2. Exclude large directories: Add to .shannonignore
3. Split into sub-projects if monorepo

### "Cannot detect tech stack" Warning

**Symptom**: Tech stack detection incomplete

**Solutions**:
1. Manually configure in .shannon/config.json after init
2. Ensure package.json, Cargo.toml, or equivalent exists
3. Check if project root is correct directory

### "Serena MCP unavailable" Warning

**Symptom**: Init completes but no persistent storage

**Impact**: Limited checkpoint persistence, no cross-session context

**Solutions**:
1. Configure Serena MCP: `/shannon:check_mcps --setup serena`
2. Re-run init after Serena configured
3. Accept limited functionality (local-only persistence)

---

## Notes

- **NEW in V5.5**: First project-level onboarding command
- **One-time operation**: Run once per project (not per session)
- **Comprehensive**: Analyzes EVERY file (no shortcuts)
- **Smart**: Auto-detects tech stack, validates tests, recommends MCPs
- **Persistent**: Creates .shannon/ directory with permanent config
- **Shannon-Ready**: After init, project fully integrated with Shannon

---

## Related Commands

**After `/shannon:init`**:
- `/shannon:prime` - Start first Shannon session
- `/shannon:status` - Check Shannon Readiness Score
- `/shannon:check_mcps` - Configure missing MCPs

**Enhances**:
- `/shannon:do` - 3-5x faster with init context
- `/shannon:wave` - Better wave planning with architecture map
- `/shannon:analyze` - Leverages cached project index

---

**Version**: 5.5.0 (NEW in V5.5)
**Status**: Core onboarding command
**Prerequisite for**: Optimal Shannon integration

