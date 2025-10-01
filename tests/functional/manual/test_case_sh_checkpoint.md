# Test Case: Checkpoint and Restore Cycle

**Test ID**: TC-002
**Priority**: Critical
**Category**: Integration/Memory
**Estimated Time**: 15 minutes

## Objective

Validate that /sh:checkpoint and /sh:restore commands correctly save and restore Shannon project state, including context, memory, and behavioral configurations.

## Prerequisites

- [ ] Shannon project loaded in Claude Code
- [ ] Serena MCP configured and functional
- [ ] .shannon/ directory initialized
- [ ] Test project with some work in progress
- [ ] Test environment: /Users/nick/Documents/shannon

## Test Steps

### Step 1: Setup Test Environment

```bash
# Create test project state
cd /Users/nick/Documents/shannon
mkdir -p test-project/src
mkdir -p test-results/TC-002/{artifacts,screenshots,logs}

# Create sample files to track
cat > test-project/src/app.py << 'EOF'
"""Test application for checkpoint validation."""

def calculate_sum(a: int, b: int) -> int:
    """Calculate sum of two numbers."""
    return a + b

def main():
    """Main application entry point."""
    result = calculate_sum(10, 20)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
EOF

cat > test-project/README.md << 'EOF'
# Test Project

Simple Python application for checkpoint testing.

## Features
- Basic arithmetic operations
- Unit testable design
EOF
```

**Expected**: Test files created successfully

### Step 2: Initialize Shannon Context

**Commands**:
```
# Load project context
/sh:load test-project/

# Verify load successful
Check output for: "Shannon project loaded"
```

**Expected Behavior**:
- Shannon project context initialized
- Files indexed by Serena MCP
- Project structure understood

### Step 3: Perform Some Work

**Simulate Development Work**:
```
# Analyze project
/sh:analyze test-project/src/

# Expected: Analysis performed, insights generated
```

**Tracked State to Validate Later**:
- Analysis results generated
- Memory entries created
- Context understanding established

### Step 4: Create Checkpoint

**Command**:
```
/sh:checkpoint "Before refactoring test project"
```

**Expected Behavior**:
- Checkpoint initiated
- Progress indicator shown
- Success message displayed

**Checkpoint Output Validation**:
- [ ] Message: "Creating checkpoint: Before refactoring test project"
- [ ] Checkpoint ID displayed (format: CKP-YYYYMMDD-HHMMSS)
- [ ] Saved items listed:
  - [ ] Project context
  - [ ] Active memory entries
  - [ ] Todo list state
  - [ ] Behavioral flags
  - [ ] MCP configurations
- [ ] Success message: "✅ Checkpoint created successfully"
- [ ] Storage location shown

### Step 5: Validate Checkpoint Artifacts

**Artifact Checklist**:

```bash
# Check checkpoint directory
ls -la .shannon/checkpoints/

# Verify checkpoint file
ls -lh .shannon/checkpoints/CKP-*.json
```

- [ ] .shannon/checkpoints/ directory exists
- [ ] Checkpoint file created: CKP-YYYYMMDD-HHMMSS.json
- [ ] File size >1KB (has substantial content)
- [ ] Timestamp matches checkpoint time (±1 minute)

**Checkpoint File Structure Validation**:

```bash
# View checkpoint structure
cat .shannon/checkpoints/CKP-*.json | head -30
```

Required JSON fields:
- [ ] `checkpoint_id`: string, format CKP-YYYYMMDD-HHMMSS
- [ ] `timestamp`: ISO 8601 format
- [ ] `description`: matches provided description
- [ ] `project_path`: absolute path to test-project
- [ ] `context`: object with project context
- [ ] `memory`: array of memory entries
- [ ] `todos`: array or object with todo items
- [ ] `behavioral_flags`: object with active flags
- [ ] `mcp_config`: object with MCP server states
- [ ] `metadata`: object with version info

### Step 6: Make Changes to Project State

**Modify Project**:

```python
# Edit app.py - add new function
cat > test-project/src/app.py << 'EOF'
"""Test application - MODIFIED VERSION."""

def calculate_sum(a: int, b: int) -> int:
    """Calculate sum of two numbers."""
    return a + b

def calculate_product(a: int, b: int) -> int:
    """Calculate product of two numbers - NEW FUNCTION."""
    return a * b

def main():
    """Main application entry point."""
    sum_result = calculate_sum(10, 20)
    product_result = calculate_product(10, 20)
    print(f"Sum: {sum_result}, Product: {product_result}")

if __name__ == "__main__":
    main()
EOF
```

**Simulate Additional Work**:
```
# Perform additional analysis
/sh:analyze test-project/src/app.py

# This should update context and memory
```

**State Changes to Verify**:
- [ ] File modified (app.py has new function)
- [ ] New analysis performed
- [ ] Memory updated with new insights
- [ ] Context changed from checkpoint state

### Step 7: Verify Changed State

**Validation Before Restore**:

```bash
# Check current file content
cat test-project/src/app.py | grep "calculate_product"
# Should find new function

# Check memory state
# (Serena MCP should show updated memory)
```

- [ ] New function present in app.py
- [ ] Recent analysis reflects changes
- [ ] Context includes new function understanding

### Step 8: Restore from Checkpoint

**Command**:
```
/sh:restore CKP-YYYYMMDD-HHMMSS
```

**Expected Behavior**:
- Checkpoint validation performed
- Restoration progress shown
- Success message displayed
- State restored to checkpoint point

**Restore Output Validation**:
- [ ] Message: "Restoring from checkpoint: CKP-YYYYMMDD-HHMMSS"
- [ ] Checkpoint description shown
- [ ] Restored items listed:
  - [ ] Project context
  - [ ] Memory entries
  - [ ] Todo list state
  - [ ] Behavioral flags
  - [ ] MCP configurations
- [ ] Success message: "✅ Checkpoint restored successfully"
- [ ] Change summary shown (if files were modified)

### Step 9: Validate Restored State

**Project Context Validation**:
- [ ] Project path matches original
- [ ] File understanding reverted to checkpoint state
- [ ] Analysis results match checkpoint time

**Memory State Validation**:

```bash
# Query Serena MCP for memory entries
# Should match checkpoint state, not post-checkpoint state
```

- [ ] Memory entries match checkpoint
- [ ] Post-checkpoint memories NOT present
- [ ] Analysis insights from checkpoint restored

**Todo State Validation**:
- [ ] Todo list matches checkpoint state
- [ ] Post-checkpoint todos removed
- [ ] Task statuses match checkpoint

**Behavioral Flags Validation**:
- [ ] Active flags match checkpoint
- [ ] MCP server configurations restored
- [ ] Agent states match checkpoint

### Step 10: Verify File State (Critical)

**File Content Validation**:

```bash
# Check if file reverted
cat test-project/src/app.py | grep "calculate_product"
# Should NOT find new function if file restoration enabled
```

**Important Note**:
Current Shannon behavior (v0.1):
- Context and memory restored: ✅
- Physical files NOT restored: ❌ (future feature)

**Validation Based on Current Implementation**:
- [ ] Context understanding reverted (Shannon knows old state)
- [ ] Memory entries reverted (old analysis present)
- [ ] Physical files unchanged (calculate_product still exists)
- [ ] Shannon behaves as if checkpoint state despite file mismatch

### Step 11: Test Checkpoint Listing

**Command**:
```
/sh:checkpoint --list
```

**Expected Output**:
```
Available Checkpoints:

CKP-20250930-143022
  Created: 2025-09-30 14:30:22
  Description: Before refactoring test project
  Size: 2.3 KB

Total: 1 checkpoint
```

**Listing Validation**:
- [ ] All checkpoints listed
- [ ] Checkpoint ID shown
- [ ] Timestamp displayed
- [ ] Description present
- [ ] File size shown
- [ ] Chronological order (newest first)

### Step 12: Test Invalid Checkpoint ID

**Command**:
```
/sh:restore CKP-INVALID-ID
```

**Expected Behavior**:
- [ ] Error message: "Checkpoint not found: CKP-INVALID-ID"
- [ ] Available checkpoints suggested
- [ ] No state changes made
- [ ] Graceful error handling

## Expected Results

**Successful Checkpoint Cycle**:

1. **Checkpoint Creation**:
   - Artifact: .shannon/checkpoints/CKP-YYYYMMDD-HHMMSS.json
   - Size: >1KB
   - Content: Valid JSON with all required fields

2. **State Restoration**:
   - Context restored: ✅
   - Memory restored: ✅
   - Todos restored: ✅
   - Flags restored: ✅
   - Physical files: ❌ (not yet supported)

3. **Behavioral Consistency**:
   - Shannon operates as if checkpoint state
   - Memory queries return checkpoint data
   - Context understanding matches checkpoint
   - Analysis references checkpoint state

## Validation Criteria

**Pass Criteria**:
- ✅ Checkpoint file created with valid structure
- ✅ All required JSON fields present
- ✅ Restore command succeeds
- ✅ Context restored to checkpoint state
- ✅ Memory entries match checkpoint
- ✅ Todo state matches checkpoint
- ✅ Checkpoint listing works
- ✅ Invalid checkpoint ID handled gracefully

**Fail Criteria**:
- ❌ Checkpoint file not created
- ❌ Invalid or incomplete JSON structure
- ❌ Restore command fails
- ❌ Context not restored correctly
- ❌ Memory state corrupted
- ❌ Error handling missing

## Advanced Test Scenarios

### Scenario A: Multiple Checkpoints

```bash
# Create checkpoint 1
/sh:checkpoint "Checkpoint 1"

# Make changes and create checkpoint 2
/sh:checkpoint "Checkpoint 2"

# Make more changes and create checkpoint 3
/sh:checkpoint "Checkpoint 3"

# List all checkpoints
/sh:checkpoint --list

# Restore to checkpoint 2 (middle checkpoint)
/sh:restore CKP-[checkpoint-2-id]
```

**Validation**:
- [ ] All 3 checkpoints listed
- [ ] Can restore to any checkpoint
- [ ] State matches selected checkpoint, not latest

### Scenario B: Checkpoint After Error

```bash
# Cause an error state
/sh:implement "Intentionally broken feature"

# Create checkpoint in error state
/sh:checkpoint "Error state checkpoint"

# Fix the error
# ...

# Verify checkpoint still valid
/sh:restore [error-checkpoint-id]
```

**Validation**:
- [ ] Checkpoint created despite error state
- [ ] Error state restored correctly
- [ ] Shannon remembers error context

### Scenario C: Cross-Session Checkpoint

```bash
# Session 1: Create checkpoint
/sh:checkpoint "Session 1 state"

# Exit Claude Code and restart
# Session 2: Restore checkpoint
/sh:restore [session-1-checkpoint-id]
```

**Validation**:
- [ ] Checkpoint persists across sessions
- [ ] Restoration works in new session
- [ ] Context fully restored

## Debug Information

**Logs to Collect**:
- [ ] Copy checkpoint creation output: test-results/TC-002/checkpoint_create.md
- [ ] Copy restore output: test-results/TC-002/restore.md
- [ ] Copy checkpoint JSON: test-results/TC-002/artifacts/CKP-*.json
- [ ] Copy checkpoint listing: test-results/TC-002/checkpoint_list.md
- [ ] Screenshots: test-results/TC-002/screenshots/

**Debug Commands**:
```bash
# List all checkpoints
ls -lh .shannon/checkpoints/

# View checkpoint structure
cat .shannon/checkpoints/CKP-*.json | jq .

# Validate JSON
cat .shannon/checkpoints/CKP-*.json | jq empty

# Check checkpoint size
du -h .shannon/checkpoints/

# Count memory entries in checkpoint
cat .shannon/checkpoints/CKP-*.json | jq '.memory | length'
```

## Notes

**Record Observations**:
- Checkpoint creation time: _____ seconds
- Checkpoint file size: _____ KB
- Restore time: _____ seconds
- Memory entries count: _____
- Context fields restored: _____
- Any warnings: _____
- File restoration working: _____ (Y/N)

**Known Limitations**:
1. Physical file restoration not yet implemented
2. Large projects may have larger checkpoint files
3. Binary files not included in checkpoints

**Future Enhancements to Test**:
- File system snapshot integration
- Incremental checkpoints (delta encoding)
- Checkpoint compression
- Checkpoint expiration/cleanup
- Checkpoint annotations
