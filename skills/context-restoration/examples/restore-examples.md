# Context Restoration Examples

## Example 1: Auto-Restore After Auto-Compact

**Scenario**: Claude Code auto-compacted conversation, user lost context

**User Experience**:
```
User: "What were we working on? I don't remember the previous conversation."

Claude: "🔍 Context loss detected. Checking for recent checkpoint..."
```

**Restoration Process**:
```python
# Step 1: Auto-detect context loss
if detect_new_conversation() and has_active_project():
    print("Context loss detected. Searching for checkpoint...")

    # Step 2: Find most recent checkpoint
    latest_key = read_memory("latest_checkpoint")
    # Returns: "precompact_checkpoint_20250930T143000Z"

    # Step 3: Load checkpoint
    checkpoint = read_memory(latest_key)

    # Step 4: Validate checkpoint
    if checkpoint and validate_checkpoint(checkpoint):
        print(f"✓ Found checkpoint from {checkpoint['metadata']['timestamp']}")
        print("Restoring context...\n")

        # Step 5: Restore all state
        restore_from_checkpoint(checkpoint)

# Output to user
print("""
✅ Context Restored Successfully

📦 Checkpoint: precompact_checkpoint_20250930T143000Z
🕐 Saved: 2025-09-30 14:30:00 UTC (2 hours ago)
📚 Restored 12 Serena memories

🔄 Project State:
   Project: taskapp_v1
   Phase: Implementation (3 of 5)
   Wave: 3 of 5 - Database Integration
   Progress: 40% complete

🎯 Current Focus:
   "Implementing authentication system"

📋 Pending Tasks:
   1. Complete JWT token generation
   2. Add refresh token logic
   3. Test login flow

▶️  Ready to continue where you left off.
""")

# User can now continue immediately
# No need to re-explain project or re-analyze
```

**Result**: User resumes work seamlessly, zero context re-establishment needed.

---

## Example 2: Restore Specific Checkpoint

**Scenario**: User wants to restore from specific point in time (not latest)

**User Command**:
```
User: /sh_restore precompact_checkpoint_20250930T120000Z
```

**Restoration Process**:
```python
# Step 1: Parse checkpoint ID from command
checkpoint_id = "precompact_checkpoint_20250930T120000Z"

# Step 2: Validate ID exists
checkpoint = read_memory(checkpoint_id)

if not checkpoint:
    print(f"❌ Checkpoint not found: {checkpoint_id}")
    print("\nAvailable checkpoints:")

    # Show all checkpoints
    all_checkpoints = [k for k in list_memories() if "checkpoint" in k]
    for cp in sorted(all_checkpoints, reverse=True)[:10]:
        cp_data = read_memory(cp)
        ts = cp_data["metadata"]["timestamp"]
        cp_type = cp_data["metadata"]["checkpoint_type"]
        print(f"  - {cp} ({ts}, {cp_type})")

    exit()

# Step 3: Show what will be restored
print(f"""
Found checkpoint: {checkpoint_id}

Checkpoint Details:
  Saved: {checkpoint['metadata']['timestamp']}
  Type: {checkpoint['metadata']['checkpoint_type']}
  Project: {checkpoint['project_state']['project_id']}
  Phase: {checkpoint['project_state']['active_phase']}
  Wave: {checkpoint['project_state']['current_wave']}

⚠️  Warning: Restoring this checkpoint will:
   - Replace current session state
   - Load project state from that point in time
   - Any work done AFTER this checkpoint will not be restored

Continue? (yes/no)
""")

# Step 4: User confirms
response = input("> ")

if response.lower() != "yes":
    print("Restoration cancelled")
    exit()

# Step 5: Restore checkpoint
print("\nRestoring checkpoint...")
restore_from_checkpoint(checkpoint)

print("""
✅ Checkpoint Restored

You are now at the state from 2025-09-30 12:00:00 UTC.

Current state:
  Wave 2 of 5 - Backend API (complete)
  Ready to start Wave 3 - Database Integration

Type /sh_wave to begin Wave 3.
""")
```

**Result**: User successfully restored from specific point in project history.

---

## Example 3: New Session Start (Next Day)

**Scenario**: User returns next day, wants to continue previous work

**User Experience**:
```
User: "Continue working on taskapp from yesterday"
```

**Restoration Process**:
```python
# Step 1: Identify project
project_id = "taskapp_v1"

# Step 2: Find most recent checkpoint for this project
all_checkpoints = [k for k in list_memories() if "checkpoint" in k]

project_checkpoints = []
for cp_key in all_checkpoints:
    cp_data = read_memory(cp_key)
    if cp_data.get("project_state", {}).get("project_id") == project_id:
        project_checkpoints.append((cp_key, cp_data))

# Sort by timestamp
project_checkpoints.sort(
    key=lambda x: x[1]["metadata"]["timestamp"],
    reverse=True
)

if not project_checkpoints:
    print(f"No checkpoint found for project: {project_id}")
    print("Starting fresh project analysis")
    exit()

# Step 3: Use most recent checkpoint
latest_checkpoint_key, latest_checkpoint = project_checkpoints[0]

# Step 4: Calculate time since checkpoint
saved_time = latest_checkpoint["metadata"]["timestamp"]
age = calculate_age(saved_time)

print(f"""
Found checkpoint for {project_id}

Last saved: {age} ago
Checkpoint: {latest_checkpoint_key}

Restoring context...
""")

# Step 5: Restore
restore_from_checkpoint(latest_checkpoint)

# Step 6: Present restoration summary
print(f"""
✅ Welcome Back!

📅 Last Session: {saved_time}
📦 Checkpoint: {latest_checkpoint_key}

📊 Project Progress:
   Phase: {latest_checkpoint['project_state']['active_phase']}
   Wave: {latest_checkpoint['project_state']['current_wave']} of {latest_checkpoint['project_state']['total_waves']}

🎯 Last Working On:
   "{latest_checkpoint['active_work']['current_focus']}"

📋 Pending Tasks:
""")

for i, task in enumerate(latest_checkpoint["active_work"]["pending_tasks"], 1):
    print(f"   {i}. {task}")

print("\n▶️  Ready to continue. What would you like to work on?")
```

**Result**: User seamlessly resumes from previous day's work.

---

## Example 4: Project Switch

**Scenario**: User wants to switch from one project to another

**User Command**:
```
User: "Switch from taskapp to blogapp"
```

**Restoration Process**:
```python
# Step 1: Identify current project
current_project = "taskapp_v1"

# Step 2: Save current state
if current_project:
    print(f"💾 Saving {current_project} state...")

    # Create checkpoint for current project
    checkpoint_key = f"manual_checkpoint_{timestamp()}"
    checkpoint_data = create_checkpoint_data(current_project)
    write_memory(checkpoint_key, checkpoint_data)

    print(f"✓ {current_project} state saved: {checkpoint_key}")

# Step 3: Find checkpoint for target project
target_project = "blogapp_v1"

print(f"\n🔄 Switching to {target_project}...")

# Search for blogapp checkpoints
target_checkpoints = find_project_checkpoints(target_project)

if not target_checkpoints:
    print(f"\n⚠️  No checkpoint found for {target_project}")
    print("Starting fresh project context")
    print("\nTo begin, please provide project specification")
    exit()

# Step 4: Load most recent checkpoint for target project
latest_checkpoint_key = target_checkpoints[0]
checkpoint = read_memory(latest_checkpoint_key)

print(f"Found checkpoint: {latest_checkpoint_key}")
print(f"Saved: {checkpoint['metadata']['timestamp']}")
print("\nLoading project state...")

# Step 5: Restore
restore_from_checkpoint(checkpoint)

# Step 6: Confirm switch
print(f"""
✅ Switched to {target_project}

Previous Project: {current_project} (saved)
Current Project: {target_project}

📊 {target_project} State:
   Phase: {checkpoint['project_state']['active_phase']}
   Wave: {checkpoint['project_state']['current_wave']} of {checkpoint['project_state']['total_waves']}

🎯 Focus:
   "{checkpoint['active_work']['current_focus']}"

▶️  Ready to continue {target_project} work.

To switch back to {current_project}, use:
   /sh_restore {checkpoint_key}
""")
```

**Result**: User successfully switched between projects with state preservation.

---

## Example 5: Recovery from Error

**Scenario**: Something went wrong, user wants to rollback to last good state

**User Command**:
```
User: "That broke everything. Restore from last good checkpoint."
```

**Restoration Process**:
```python
# Step 1: Find recent checkpoints
all_checkpoints = [k for k in list_memories() if "checkpoint" in k]
sorted_checkpoints = sorted(all_checkpoints, reverse=True)

# Step 2: Present options
print("Recent checkpoints:\n")

for i, cp_key in enumerate(sorted_checkpoints[:5], 1):
    cp_data = read_memory(cp_key)
    ts = cp_data["metadata"]["timestamp"]
    cp_type = cp_data["metadata"]["checkpoint_type"]
    wave = cp_data["project_state"]["current_wave"]

    age = calculate_age(ts)

    print(f"{i}. {cp_key}")
    print(f"   Saved: {age} ago")
    print(f"   Type: {cp_type}")
    print(f"   Wave: {wave}\n")

# Step 3: User selects
print("Which checkpoint to restore? (1-5): ")
selection = input("> ")

checkpoint_key = sorted_checkpoints[int(selection) - 1]
checkpoint = read_memory(checkpoint_key)

# Step 4: Show what will be restored
print(f"""
Selected: {checkpoint_key}

This will restore to:
  Time: {checkpoint['metadata']['timestamp']}
  Phase: {checkpoint['project_state']['active_phase']}
  Wave: {checkpoint['project_state']['current_wave']}

Current work after this point will be lost.

Confirm restoration? (yes/no): """)

response = input("> ")

if response.lower() != "yes":
    print("Restoration cancelled")
    exit()

# Step 5: Restore
print("\n🔄 Rolling back to checkpoint...")
restore_from_checkpoint(checkpoint)

print("""
✅ Rollback Complete

State restored to last good checkpoint.

Recommendation: Review what went wrong before continuing:
  1. Check recent file changes
  2. Review error logs
  3. Consider alternative approach

Ready to continue safely.
""")
```

**Result**: User recovered from error state by restoring last good checkpoint.

---

## Example 6: Partial Restoration (Missing Memories)

**Scenario**: Some memory keys are missing, but restoration can continue

**Restoration Process**:
```python
# Step 1: Load checkpoint
checkpoint_key = "precompact_checkpoint_20250930T143000Z"
checkpoint = read_memory(checkpoint_key)

# Step 2: Attempt to restore all memories
serena_keys = checkpoint["serena_memory_keys"]
restored_memories = {}
missing_memories = []

for key in serena_keys:
    try:
        content = read_memory(key)
        restored_memories[key] = content
    except:
        missing_memories.append(key)

# Step 3: Categorize missing memories
critical_missing = []
important_missing = []
optional_missing = []

for key in missing_memories:
    if any(x in key for x in ["spec_analysis", "phase_plan"]):
        critical_missing.append(key)
    elif any(x in key for x in ["wave_", "decisions"]):
        important_missing.append(key)
    else:
        optional_missing.append(key)

# Step 4: Handle based on what's missing
if critical_missing:
    print(f"""
❌ Critical Restoration Failure

Cannot restore - missing critical memories:
""")
    for key in critical_missing:
        print(f"  - {key}")

    print("""
These memories are required for proper context restoration.

Options:
  1. Try different checkpoint
  2. Re-run specification analysis
  3. Start fresh project context

Recommended: Re-run /sh_spec to regenerate analysis
""")
    exit()

elif important_missing:
    print(f"""
⚠️  Partial Restoration Warning

Missing {len(important_missing)} important memories:
""")
    for key in important_missing:
        print(f"  - {key}")

    print(f"""
✓ Restored {len(restored_memories)} of {len(serena_keys)} memories

Impact:
  - Some wave results may be unavailable
  - Some decisions history may be missing
  - Core project context is intact

Continue with partial restoration? (yes/no): """)

    response = input("> ")

    if response.lower() != "yes":
        print("Restoration cancelled")
        exit()

# Step 5: Complete restoration with available data
print("\n🔄 Completing partial restoration...")
restore_from_checkpoint(checkpoint, restored_memories)

print(f"""
✅ Partial Restoration Complete

Restored: {len(restored_memories)} of {len(serena_keys)} memories
Missing: {len(important_missing)} important, {len(optional_missing)} optional

⚠️  Some context may be incomplete:
""")

if important_missing:
    print("\nMissing Important Context:")
    for key in important_missing:
        print(f"  - {key}")

print("""
You can continue working, but consider:
  - Some historical decisions may not be available
  - Some wave results may need to be regenerated
  - Document new decisions as you proceed

▶️  Ready to continue with available context.
""")
```

**Result**: User can continue with partial context, understanding limitations.

---

## Example 7: Auto-Restore on Session Start

**Scenario**: Shannon detects new session and auto-restores

**Automatic Behavior**:
```python
# Runs automatically when new conversation starts

def on_session_start():
    """Auto-restore check on session initialization"""

    # Step 1: Check if there was a previous session
    latest_checkpoint_key = read_memory("latest_checkpoint")

    if not latest_checkpoint_key:
        # No previous checkpoint - fresh start
        return

    # Step 2: Load checkpoint
    checkpoint = read_memory(latest_checkpoint_key)

    if not checkpoint:
        return

    # Step 3: Check age
    saved_time = checkpoint["metadata"]["timestamp"]
    age = calculate_age(saved_time)

    # Step 4: Auto-restore if recent (< 24 hours)
    if age < timedelta(hours=24):
        print(f"""
🔄 Previous session detected

Found checkpoint from {age} ago.
Auto-restoring context...
""")

        # Restore silently
        restore_from_checkpoint(checkpoint)

        print(f"""
✅ Session Restored

Project: {checkpoint['project_state']['project_id']}
Phase: {checkpoint['project_state']['active_phase']}
Wave: {checkpoint['project_state']['current_wave']} of {checkpoint['project_state']['total_waves']}

Focus: "{checkpoint['active_work']['current_focus']}"

▶️  Ready to continue. How can I help?
""")

    else:
        # Old checkpoint - ask user
        print(f"""
📅 Previous Session Found

Last checkpoint: {age} ago
Project: {checkpoint['project_state']['project_id']}

Restore previous session? (yes/no): """)

        response = input("> ")

        if response.lower() == "yes":
            restore_from_checkpoint(checkpoint)
            print("✅ Session restored")
        else:
            print("Starting fresh session")

# This runs automatically when Shannon initializes
on_session_start()
```

**Result**: Seamless continuation between sessions without manual restore command.

---

## Common Patterns

### Pattern: Progressive Disclosure

```python
# Don't dump all checkpoint data at once
# Show summary first, details on request

# Summary
print("""
✅ Context Restored

Project: taskapp_v1
Phase: Implementation (Wave 3/5)
Pending: 3 tasks

Type 'details' for full context
""")

# If user asks for details
if user_input == "details":
    print("""
📦 Full Checkpoint Details:

Checkpoint: precompact_checkpoint_20250930T143000Z
Saved: 2025-09-30 14:30:00 UTC

Restored Memories (12):
  - spec_analysis_taskapp
  - phase_plan_taskapp
  - wave_1_complete_taskapp
  - wave_2_complete_taskapp
  ...

Completed Waves:
  Wave 1: Frontend Components ✓
  Wave 2: Backend API ✓

Current Wave:
  Wave 3: Database Integration (in progress)

Pending Tasks:
  1. Complete JWT token generation
  2. Add refresh token logic
  3. Test login flow

In-Progress Files:
  - /path/to/auth.ts
  - /path/to/login.tsx
""")
```

### Pattern: Validation Before Action

```python
# Always validate before restoring

def safe_restore(checkpoint_id):
    """Restore with validation"""

    # Load checkpoint
    checkpoint = read_memory(checkpoint_id)

    # Validate structure
    if not validate_checkpoint_schema(checkpoint):
        raise ValueError("Invalid checkpoint structure")

    # Validate age
    age = calculate_age(checkpoint["metadata"]["timestamp"])
    if age > timedelta(days=30):
        warn_user(f"Checkpoint is {age.days} days old")

    # Validate file references
    for file_path in checkpoint["active_work"]["in_progress_files"]:
        if not os.path.exists(file_path):
            warn_user(f"File no longer exists: {file_path}")

    # Validate MCP availability
    for mcp_name in checkpoint.get("required_mcps", []):
        if not check_mcp_available(mcp_name):
            raise ValueError(f"Required MCP not available: {mcp_name}")

    # All valid - proceed with restore
    restore_from_checkpoint(checkpoint)
```

### Pattern: Graceful Degradation

```python
# If full restore fails, try partial

try:
    # Attempt full restoration
    restore_from_checkpoint(checkpoint)
except FullRestoreError:
    print("Full restoration failed. Attempting partial...")

    # Restore in priority order
    priorities = ["critical", "important", "optional"]

    for priority in priorities:
        try:
            restore_priority_level(checkpoint, priority)
        except Exception as e:
            print(f"Could not restore {priority}: {e}")
            continue

    print("Partial restoration complete")
    print("Some features may be limited")
```

## Testing Restoration

### Test 1: Basic Restore
```python
# Create checkpoint
checkpoint_id = create_checkpoint()

# Simulate context loss (clear all variables)
clear_context()

# Restore
restore_from_checkpoint(checkpoint_id)

# Verify
assert project_id == original_project_id
assert current_wave == original_wave
assert len(pending_tasks) == original_task_count
```

### Test 2: Missing Memories
```python
# Create checkpoint
checkpoint_id = create_checkpoint()

# Delete some non-critical memories
delete_memory("optional_memory_key")

# Restore should succeed with warning
result = restore_from_checkpoint(checkpoint_id)

assert result.status == "partial"
assert len(result.warnings) > 0
assert result.can_continue == True
```

### Test 3: Corrupted Checkpoint
```python
# Create valid checkpoint
checkpoint_id = create_checkpoint()

# Corrupt it
corrupt_checkpoint(checkpoint_id)

# Restore should fail gracefully
try:
    restore_from_checkpoint(checkpoint_id)
    assert False, "Should have raised error"
except CheckpointCorruptedError as e:
    assert "corrupted" in str(e).lower()
    assert e.suggestions is not None
```

## Summary

Context restoration enables:

1. **Zero-Downtime Recovery**: Resume after context loss
2. **Session Continuity**: Seamless day-to-day workflow
3. **Project Switching**: Quick context changes
4. **Error Recovery**: Rollback to known-good state
5. **Flexible Restoration**: Auto or manual, full or partial

Combined with context-checkpoint, provides complete session state preservation across all Shannon operations.
