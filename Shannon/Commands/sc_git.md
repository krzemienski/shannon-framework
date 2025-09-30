---
name: sc_git
description: Enhanced git workflow with wave commit patterns, checkpoint synchronization, and professional messaging
category: version-control
complexity: standard
base_command: /git
enhancement_type: wave-integration
mcp_servers: [serena]
personas: [devops, scribe]
priority: critical
wave_enabled: false
---

# /sc:git - Git Workflow Assistant with Wave Patterns

> **Enhanced SuperClaude Command**: Git workflow automation with Shannon V3's wave commit patterns, checkpoint synchronization, and professional commit message generation.

## Purpose Statement

Intelligent git workflow assistant that:
1. **Automates Git Operations**: Branch creation, staging, committing, PR creation
2. **Wave Commit Patterns**: Automatic commits after each wave completion
3. **Checkpoint Synchronization**: Trigger Serena checkpoints with git operations
4. **Professional Messaging**: Generate context-aware, professional commit messages
5. **Workflow Safety**: Prevent common git mistakes and enforce best practices

## Shannon V3 Enhancements

### Wave Commit Pattern
```yaml
wave_completion_trigger:
  automatic: true
  pattern: "After each wave completes → git commit wave results"
  message_format: "feat(wave-N): [wave deliverable summary]"
  checkpoint_sync: true
```

### Checkpoint Integration
```yaml
checkpoint_triggers:
  before_commit: "Save Serena state before committing"
  after_commit: "Update checkpoint with commit SHA"
  branch_creation: "Create checkpoint when creating feature branch"
  risky_operations: "Checkpoint before rebase/merge/reset"
```

### Professional Message Generation
```yaml
message_generation:
  context_analysis: "Analyze changed files and scope"
  conventional_commits: "Follow conventional commit format"
  wave_awareness: "Include wave/phase context when relevant"
  scribe_quality: "Professional, clear, concise messaging"
```

## Activation Triggers

**Automatic**:
- Wave completion detected
- Large changeset staged (>5 files)
- Shannon session checkpoints
- Feature branch creation requests

**Manual**:
```bash
/sc:git status                    # Enhanced status with wave context
/sc:git commit [message]          # Professional commit with checkpoint
/sc:git branch feature/[name]     # Branch creation with checkpoint
/sc:git checkpoint               # Sync git + Serena checkpoint
/sc:git pr [title]               # Professional PR creation
```

## Sub-Agent Activation

### DEVOPS Agent
**Activates For**:
- Branch management
- Merge conflict resolution
- Git configuration
- Repository health checks
- Workflow automation

**Responsibilities**:
- Ensure safe git operations
- Prevent destructive actions
- Enforce branch naming conventions
- Validate repository state

### SCRIBE Agent
**Activates For**:
- Commit message generation
- PR description writing
- Changelog creation
- Release notes
- Documentation commits

**Responsibilities**:
- Professional messaging
- Conventional commit format
- Context-aware descriptions
- Clear, concise language

## Usage Patterns

### Basic Operations

**Check Status**:
```bash
/sc:git status

# Output:
## 📋 Git Status
- Branch: feature/auth-system (tracking origin/feature/auth-system)
- Changes: 8 modified, 2 new files
- Wave Context: Wave 3 (Implementation) - 2 waves behind
- Last Commit: feat(wave-2): complete analysis phase
- Uncommitted Waves: Wave 3 complete, needs commit

## 💡 Recommendation:
Run: /sc:git commit wave-3
```

**Create Feature Branch**:
```bash
/sc:git branch feature/user-auth

# Flow:
1. Check current branch (must not be main/master)
2. Create Serena checkpoint: pre_branch_user_auth
3. Create branch: git checkout -b feature/user-auth
4. Output confirmation with checkpoint key
```

**Commit Changes**:
```bash
/sc:git commit "implement JWT authentication"

# Or for wave commits:
/sc:git commit wave-3

# Or automatic:
# (Shannon detects wave completion, suggests commit)
```

**Create Pull Request**:
```bash
/sc:git pr "Add JWT authentication system"

# Flow:
1. Ensure branch is pushed
2. Generate professional PR description (SCRIBE agent)
3. Create PR via gh CLI or provide instructions
4. Create checkpoint: pr_created_[branch-name]
```

### Wave Integration Patterns

**Automatic Wave Commit**:
```yaml
wave_completion_flow:
  step_1: "Wave N completes all deliverables"
  step_2: "Shannon suggests: /sc:git commit wave-N"
  step_3: "User confirms or modifies message"
  step_4: "Create pre-commit checkpoint"
  step_5: "Stage relevant files"
  step_6: "Generate professional commit message"
  step_7: "Commit with wave context"
  step_8: "Update post-commit checkpoint"
```

**Manual Wave Commit**:
```bash
/sc:git commit wave-3

# Generated Message Example:
# feat(wave-3): implement authentication middleware
#
# - Added JWT token validation
# - Implemented user session management
# - Created authentication middleware
# - Added comprehensive error handling
#
# Wave: 3/5 (Implementation Phase)
# Phase: Core Backend Development
#
# Co-Authored-By: Shannon Framework <shannon@anthropic.com>
```

### Checkpoint Synchronization

**Before Risky Operations**:
```bash
/sc:git checkpoint

# Flow:
1. Run: /sh:checkpoint pre_git_operation
2. Run: git status
3. Save current branch, uncommitted changes to checkpoint
4. Output: Safe to proceed with git operations
```

**After Significant Commits**:
```yaml
auto_checkpoint_trigger:
  condition: "Commit affects >10 files OR wave completion"
  action: "Automatic /sh:checkpoint post_commit_[SHA]"
  metadata: "Include commit SHA in checkpoint"
```

## Execution Flow

### 1. Status Check Flow
```yaml
step_1: "Run git status and git branch"
step_2: "Analyze working tree state"
step_3: "Check for uncommitted waves (from Serena)"
step_4: "Calculate wave progress vs git commits"
step_5: "Provide recommendations"
```

### 2. Branch Creation Flow
```yaml
step_1: "Validate not on main/master"
step_2: "Create pre-branch checkpoint (Serena)"
step_3: "Execute: git checkout -b [branch-name]"
step_4: "Verify branch creation"
step_5: "Output confirmation with checkpoint key"
```

### 3. Commit Flow (Standard)
```yaml
step_1: "Analyze changed files (git diff)"
step_2: "Create pre-commit checkpoint"
step_3: "Stage files: git add [files]"
step_4: "Generate commit message (SCRIBE)"
step_5: "Review with user (if requested)"
step_6: "Execute: git commit -m '[message]'"
step_7: "Create post-commit checkpoint with SHA"
step_8: "Output commit summary"
```

### 4. Commit Flow (Wave)
```yaml
step_1: "Identify wave number from context"
step_2: "Read wave completion summary from Serena"
step_3: "Analyze changed files for wave"
step_4: "Create pre-commit checkpoint"
step_5: "Stage wave-related files"
step_6: "Generate wave commit message"
step_7: "Include wave metadata in message"
step_8: "Execute commit"
step_9: "Update wave status in Serena"
step_10: "Create post-commit checkpoint"
```

### 5. PR Creation Flow
```yaml
step_1: "Verify branch is pushed (git push -u origin [branch])"
step_2: "Analyze all commits in branch"
step_3: "Generate PR title (SCRIBE)"
step_4: "Generate PR description (SCRIBE)"
step_5: "Create PR via gh CLI or provide instructions"
step_6: "Create checkpoint: pr_created"
step_7: "Output PR URL and details"
```

## Commit Message Templates

### Standard Commit
```
type(scope): brief description

- Detailed change 1
- Detailed change 2
- Detailed change 3

[Optional: Additional context]

Co-Authored-By: Shannon Framework <shannon@anthropic.com>
```

### Wave Commit
```
feat(wave-N): wave deliverable summary

Completed deliverables:
- Deliverable 1
- Deliverable 2
- Deliverable 3

Wave: N/[total] ([Phase Name])
Phase: [Current Phase]
Status: ✅ Complete

[Optional: Testing notes, next steps]

Co-Authored-By: Shannon Framework <shannon@anthropic.com>
```

### Checkpoint Commit
```
chore(checkpoint): save progress before [operation]

Context preservation:
- Active Wave: N
- Active Phase: [Phase]
- Serena Keys: [count]
- Checkpoint: [checkpoint-key]

Co-Authored-By: Shannon Framework <shannon@anthropic.com>
```

### Types Reference
```yaml
feat: "New feature or functionality"
fix: "Bug fix"
docs: "Documentation only changes"
style: "Code style changes (formatting, etc.)"
refactor: "Code refactoring without behavior change"
perf: "Performance improvement"
test: "Adding or updating tests"
chore: "Build process, tooling, dependencies"
wave: "Wave completion (Shannon-specific)"
checkpoint: "Context preservation (Shannon-specific)"
```

## Professional Message Generation

### Context Analysis
```yaml
analyze:
  changed_files: "List all modified, added, deleted files"
  file_types: "Categorize by frontend/backend/config/docs"
  scope: "Determine affected modules/components"

extract:
  primary_changes: "Most significant modifications"
  supporting_changes: "Related updates (tests, docs)"

classify:
  type: "feat|fix|docs|style|refactor|perf|test|chore"
  scope: "Module or component affected"
  breaking: "Does this break existing functionality?"
```

### Message Construction
```yaml
title_format: "type(scope): imperative description"
title_rules:
  - "Use imperative mood (add, not added)"
  - "Lowercase after colon"
  - "No period at end"
  - "Max 72 characters"

body_format: "Detailed list of changes"
body_rules:
  - "Use bullet points for multiple changes"
  - "Explain the what and why, not how"
  - "Reference issue numbers if applicable"
  - "Professional, clear, concise"

footer_format: "Metadata and co-authorship"
footer_rules:
  - "Include wave context if relevant"
  - "Add Shannon co-authorship"
  - "Note breaking changes if any"
```

## Checkpoint Synchronization Strategy

### Pre-Operation Checkpoints
```yaml
trigger: "Before any potentially destructive git operation"
operations: [merge, rebase, reset, force-push, branch-delete]

checkpoint_content:
  git_state:
    branch: current_branch
    uncommitted_changes: file_list
    unpushed_commits: commit_list
  serena_state:
    all_memory_keys: [keys]
    wave_state: current_wave
    phase_state: current_phase
```

### Post-Commit Checkpoints
```yaml
trigger: "After commits affecting >10 files or wave completions"

checkpoint_content:
  git_state:
    commit_sha: latest_commit_sha
    branch: current_branch
    files_changed: count
  serena_state:
    wave_completed: wave_number
    next_wave: next_wave_number
```

### Automatic Checkpoint Triggers
```yaml
auto_triggers:
  wave_commit: "Always checkpoint after wave commit"
  large_commit: "Checkpoint for commits >10 files"
  branch_creation: "Checkpoint when creating feature branch"
  pr_creation: "Checkpoint after PR created"
  risky_operation: "Checkpoint before merge/rebase/reset"
```

## Output Format

### Status Output
```markdown
## 📋 Git Status

**Branch**: feature/auth-system
**Tracking**: origin/feature/auth-system (up to date)
**Status**: 8 modified, 2 new files

**Changed Files**:
- ✏️  src/middleware/auth.js
- ✏️  src/routes/user.js
- ➕  tests/auth.test.js
... (8 more)

**Wave Context**:
- Current Wave: 3 (Implementation Phase)
- Waves Behind: 2 waves not committed yet
- Last Wave Commit: feat(wave-2): complete analysis phase (3 days ago)

## 💡 Recommendations:
1. Commit Wave 3 progress: /sc:git commit wave-3
2. Create checkpoint before continuing: /sc:git checkpoint
```

### Commit Output
```markdown
## ✅ Commit Created

**Type**: Wave Completion Commit
**Message**: feat(wave-3): implement authentication middleware
**SHA**: a1b2c3d4
**Files Changed**: 12 files
**Insertions**: +487 lines
**Deletions**: -123 lines

**Checkpoint Created**: ✅
- Pre-commit: shannon_checkpoint_pre_wave_3_commit
- Post-commit: shannon_checkpoint_post_a1b2c3d4

**Wave Status Updated**:
- Wave 3: ✅ Complete (committed)
- Wave 4: 🔄 In Progress

**Next Actions**:
- Continue Wave 4 development
- Run tests: /sc:test
- Create PR when ready: /sc:git pr
```

### PR Output
```markdown
## 🚀 Pull Request Created

**PR #**: 42
**Title**: Add JWT authentication system
**URL**: https://github.com/org/repo/pull/42
**Status**: Open

**Description Preview**:
> Implements JWT-based authentication with user session management...
> (Full description in PR)

**Branch**: feature/auth-system → main
**Commits**: 5
**Files Changed**: 18

**Checkpoint Created**: ✅
- Key: shannon_checkpoint_pr_42_created

**Next Actions**:
- Request reviews from team
- Monitor CI/CD status
- Address feedback
```

## Examples

### Example 1: Wave Completion Commit
```bash
# Shannon detects Wave 3 completed
Shannon: Wave 3 complete! Ready to commit?

User: /sc:git commit wave-3

Shannon:
1. Creating pre-commit checkpoint...
   ✅ shannon_checkpoint_pre_wave_3_commit

2. Analyzing changed files...
   Found: 12 files modified (implementation phase)

3. Generating commit message...

   Type: feat (new feature)
   Scope: wave-3
   Description: implement authentication middleware

4. Staging files...
   ✅ Staged 12 files

5. Committing...
   ✅ Commit: a1b2c3d4

6. Creating post-commit checkpoint...
   ✅ shannon_checkpoint_post_a1b2c3d4

## ✅ Wave 3 Committed Successfully
SHA: a1b2c3d4
Message: feat(wave-3): implement authentication middleware
Checkpoints: Pre & post created
```

### Example 2: Feature Branch Creation
```bash
User: /sc:git branch feature/user-profile

Shannon:
1. Checking current branch...
   ✅ Currently on: main (safe to create branch)

2. Creating pre-branch checkpoint...
   ✅ shannon_checkpoint_pre_branch_user_profile

3. Creating branch...
   ✅ Branch created: feature/user-profile
   ✅ Switched to: feature/user-profile

## ✅ Feature Branch Created

**Branch**: feature/user-profile
**Base**: main
**Checkpoint**: shannon_checkpoint_pre_branch_user_profile

**Safe to proceed with development**
To restore if needed: /sh:restore shannon_checkpoint_pre_branch_user_profile
```

### Example 3: Professional PR Creation
```bash
User: /sc:git pr "User profile management"

Shannon:
1. Checking branch status...
   ✅ Branch: feature/user-profile
   ⚠️  Not pushed to origin

2. Pushing branch...
   Executing: git push -u origin feature/user-profile
   ✅ Pushed

3. Analyzing commits...
   Found: 3 commits, 8 files changed

4. Generating PR description (SCRIBE agent)...

   Title: Add user profile management system

   Description:
   ## Summary
   Implements complete user profile management with CRUD operations

   ## Changes
   - User profile API endpoints
   - Profile update validation
   - Avatar upload handling
   - Profile privacy settings

   ## Testing
   - Unit tests: 95% coverage
   - Integration tests: All passing
   - Manual testing: Verified flows

   ## Screenshots
   (Attach screenshots if available)

   🤖 Generated with Shannon Framework

5. Creating PR...
   ✅ PR #43 created

6. Creating checkpoint...
   ✅ shannon_checkpoint_pr_43_created

## 🚀 Pull Request Created
PR #43: Add user profile management system
URL: https://github.com/org/repo/pull/43
```

## Boundaries & Safety

### Will Do
- ✅ Check git status before operations
- ✅ Create checkpoints before risky operations
- ✅ Generate professional commit messages
- ✅ Enforce branch naming conventions
- ✅ Prevent commits to main/master
- ✅ Stage appropriate files
- ✅ Sync git state with Serena checkpoints
- ✅ Provide clear operation summaries

### Will Not Do
- ❌ Force push without explicit confirmation
- ❌ Delete branches without confirmation
- ❌ Commit to main/master directly
- ❌ Skip checkpoint creation on risky operations
- ❌ Generate vague commit messages
- ❌ Commit files matching .gitignore

### Safety Mechanisms
```yaml
branch_protection:
  - "Cannot commit directly to main/master"
  - "Requires feature branch creation"

checkpoint_protection:
  - "Always checkpoint before destructive operations"
  - "Automatic pre-commit checkpoints"

message_protection:
  - "Must follow conventional commit format"
  - "Professional language required"
  - "No vague messages like 'fix', 'update'"
```

## Integration Points

### With SuperClaude
- **Base**: SuperClaude /git command functionality
- **Enhancement**: Wave patterns, checkpoint sync
- **Personas**: DEVOPS for operations, SCRIBE for messaging

### With Shannon
- **Wave Coordination**: Automatic commits after wave completion
- **Checkpoint System**: Sync git operations with Serena checkpoints
- **Phase Awareness**: Include phase context in commit messages

### With Serena MCP
- **write_memory**: Save pre/post-commit checkpoints
- **read_memory**: Load wave completion data for messages
- **list_memories**: Track all checkpoints for git operations

## Command Relationships

```yaml
complements:
  - "/sh:checkpoint - Manual checkpoint creation"
  - "/sh:restore - Restore from git checkpoint"
  - "/sc:implement - Development that leads to commits"
  - "/sc:build - Build results that get committed"

precedes:
  - "/sc:test - Test before commit"
  - "/sc:document - Document changes in commit"

follows:
  - "/sc:implement - Implement then commit"
  - "Wave completion - Commit wave results"
```

---

**Related Commands**:
- `/sh:checkpoint` - Manual checkpoint creation
- `/sh:restore` - Context restoration
- `/sc:implement` - Feature implementation
- `/sc:test` - Testing workflows

**Base Command**: SuperClaude /git
**Enhancement Level**: Major (wave integration, checkpoint sync)
**Shannon Version**: 3.0.0