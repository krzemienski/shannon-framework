---
name: root-cause-tracing
description: |
  Backward call chain tracing to find original trigger of deep-stack errors. Never treat surface error
  location as the actual problem. Traces backward through data flow, call stack, and component boundaries
  to locate where bug was introduced. Implements defense-in-depth at the source.

skill-type: PROTOCOL
shannon-version: ">=5.4.0"
category: debugging

invoked-by-skills:
  - systematic-debugging

related-skills:
  - systematic-debugging
  - defense-in-depth

mcp-requirements:
  recommended:
    - name: serena
      purpose: Save trace patterns for similar bugs
    - name: sequential
      purpose: Deep thinking for complex traces

allowed-tools: [Read, Grep, Bash, Sequential, Serena]
---

# Root Cause Tracing

## Purpose

Trace backward through call chains to find the **original trigger** of bugs that manifest deep in execution stacks. Surface-level error locations are symptoms—this skill finds the source.

**Core Principle**: "Trace backward through the call chain until you find the original trigger, then fix at the source."

**Shannon Integration**: Quantified trace depth, component boundary analysis, defense-in-depth at source + all layers.

---

## The Core Problem

**Scenario**: Error appears at Line 450 in `utils.ts`

**Naive Approach**: Fix Line 450 (treating symptom)

**Root Cause Approach**: Trace backward:
- Line 450 called by Line 320 in `service.ts`
- Line 320 called by Line 180 in `api.ts`
- Line 180 called by Line 90 in `controller.ts`
- **Line 90 passes invalid data** ← ORIGINAL TRIGGER

**Correct Fix**: Fix Line 90 (source) + add defense at all layers (structurally impossible)

---

## The Five-Step Process

### Step 1: Observe the Symptom

**Goal**: Document where error appears (not necessarily where it originates)

**Actions**:
```
1. Read complete error message
2. Note error location:
   - File path
   - Line number
   - Function name
   - Error type
3. Identify symptom behavior:
   - What operation failed?
   - What data was involved?
   - What was expected vs actual?
```

**Output**: Symptom documentation

Example:
```markdown
## Symptom

**Location**: src/utils/validator.ts:450
**Function**: validateUserData()
**Error**: TypeError: Cannot read property 'email' of undefined
**Data**: user object expected, received undefined
**Expected**: Valid user object with email property
```

---

### Step 2: Find Immediate Cause

**Goal**: Identify code directly producing the error

**Actions**:
```
1. Read function containing error line:
   - Complete function (all lines)
   - Function parameters
   - Variable assignments
   - Control flow

2. Identify immediate cause:
   - Which variable is undefined/null?
   - Which operation threw exception?
   - Which condition failed?

3. Check function inputs:
   - Where do parameters come from?
   - Are inputs validated?
   - What are input assumptions?
```

**Output**: Immediate cause analysis

Example:
```markdown
## Immediate Cause

**Function**: validateUserData(user)
**Problem**: Parameter 'user' is undefined
**No Input Validation**: Function assumes user is always defined
**Error on**: return user.email.length > 0
```

---

### Step 3: Ask "What Called This?"

**Goal**: Map the call stack upward to find caller

**Actions**:

1. **Read Stack Trace**
   ```
   - Note ALL frames in stack trace
   - Identify calling function (frame above error)
   - Note file and line of caller
   ```

2. **Read Calling Function**
   ```
   - Use Read tool on caller file
   - Find exact line that calls error function
   - Read complete calling function
   - Identify where caller's inputs come from
   ```

3. **Document Call Chain**
   ```
   Frame N: validateUserData() ← ERROR HERE
            src/utils/validator.ts:450

   Frame N-1: processUserRequest() ← CALLER
              src/services/userService.ts:320
              Calls: validateUserData(request.user)
              Problem: request.user might be undefined

   Frame N-2: handleApiRequest() ← CALLER OF CALLER
              src/api/users.ts:180
              Calls: processUserRequest(req)
              Problem: req not validated before passing
   ```

**Output**: Call chain documentation (working backwards)

---

### Step 4: Keep Tracing Up

**Goal**: Continue backward until finding where invalid data entered

**Actions**:

1. **For Each Caller in Chain**:
   ```
   Repeat Step 3 for each frame:
   - Read caller function completely
   - Find where caller gets its inputs
   - Check if caller validates inputs
   - Document assumptions and gaps
   ```

2. **Identify Data Flow**:
   ```
   Trace data backwards:
   - Where does invalid data originate?
   - Which function first introduces it?
   - Was it user input, API response, database query?
   ```

3. **Find Component Boundaries**:
   ```
   Note when crossing components:
   - API layer → Service layer
   - Service layer → Database layer
   - Frontend → Backend
   - Cache → Database

   Boundaries are critical - data validation should occur here
   ```

4. **Quantify Trace Depth**:
   ```
   trace_depth = number of call chain frames analyzed
   boundary_crossings = number of component boundaries crossed

   Shannon Metric:
   - Shallow: 1-3 frames
   - Medium: 4-7 frames
   - Deep: 8-15 frames
   - Very Deep: 16+ frames
   ```

**Output**: Complete trace with depth metrics

Example:
```markdown
## Complete Trace

**Trace Depth**: 7 frames (Deep)
**Boundary Crossings**: 3 (API → Service → Utils)

Frame 7: validateUserData() ← ERROR
         src/utils/validator.ts:450

Frame 6: processUserRequest()
         src/services/userService.ts:320
         Issue: No null check before calling validateUserData

Frame 5: handleApiRequest()
         src/api/users.ts:180
         Issue: No validation of req.user before passing

Frame 4: userController()
         src/controllers/userController.ts:90
         Issue: Assumes middleware populates req.user

Frame 3: authMiddleware()
         src/middleware/auth.ts:45
         Issue: Sets req.user = undefined when auth fails

Frame 2: expressApp.use()
         src/app.ts:30
         Boundary: Middleware chain

Frame 1: HTTP Request
         External input
```

---

### Step 5: Find Original Trigger

**Goal**: Identify THE source where bug was introduced

**Actions**:

1. **Identify Trigger Point**:
   ```
   The trigger is typically:
   - Where external input enters system (API request, user input, file read)
   - Where invalid data first created (wrong default, bad transformation)
   - Where assumption made about data (middleware assumes auth always succeeds)
   ```

2. **Determine Root Cause Category**:

   | Category | Description | Example |
   |----------|-------------|---------|
   | Missing Validation | No check for invalid input | API doesn't validate user exists |
   | Wrong Assumption | Code assumes data always present | Middleware assumes auth succeeds |
   | Bad Default | Invalid default value | Default user = undefined instead of null object |
   | Data Transformation Error | Conversion introduces invalid data | JSON parse returns undefined on error |
   | Race Condition | Timing causes invalid state | Two threads access before init complete |

3. **Quantify Root Cause Confidence**:
   ```
   confidence = (evidence_items / total_possible_evidence) * 1.0

   Evidence items:
   - Stack trace confirms call chain (0.2)
   - Code reading confirms data flow (0.2)
   - Reproduction isolates trigger (0.2)
   - Similar bugs had same cause (0.2)
   - Fix at trigger resolves symptom (0.2)

   Shannon Metric: Confidence ≥ 0.80 to proceed with fix
   ```

**Output**: Root cause identification with confidence score

Example:
```markdown
## Original Trigger

**Location**: src/middleware/auth.ts:45
**Function**: authMiddleware()
**Root Cause**: Sets req.user = undefined when authentication fails

**Category**: Wrong Assumption
**Explanation**: Middleware assumes downstream code handles undefined user,
                but no downstream validation exists. Should use null or throw error.

**Confidence**: 0.90 (HIGH)

**Evidence**:
- ✅ Stack trace confirms call chain (0.2)
- ✅ Code reading confirms data flow (0.2)
- ✅ Reproduction: Unauthenticated request causes error (0.2)
- ✅ Similar bugs: 3 other endpoints had same issue (0.2)
- ✅ Hypothesis: Fix middleware, error should resolve (0.1 - not yet tested)
```

---

## Instrumentation Technique

When manual tracing is difficult (complex async, multiple threads, unclear call paths):

### Add Diagnostic Logging at Boundaries

**Strategy**: Log BEFORE problematic operations to capture context

**Implementation**:
```python
import sys
import traceback

# At each suspicious point
def log_context(label, data):
    """Log diagnostic information"""
    print(f"\n[TRACE] {label}", file=sys.stderr)
    print(f"[TRACE] Data: {data}", file=sys.stderr)
    print(f"[TRACE] Type: {type(data)}", file=sys.stderr)
    print(f"[TRACE] Stack:\n{traceback.format_stack()}", file=sys.stderr)

# Example usage
def processUserRequest(request):
    log_context("processUserRequest ENTRY", request.user)

    if request.user is None:
        log_context("processUserRequest NULL USER", None)

    result = validateUserData(request.user)
    log_context("processUserRequest EXIT", result)
    return result
```

**Why sys.stderr / console.error?**
- Bypasses logging frameworks (which may have bugs)
- Always visible in test output
- Cannot be disabled by configuration

**What to Capture**:
```
- Input data (values, types)
- Environment context (cwd, env vars)
- Stack trace (who called this?)
- Timestamps (for race conditions)
```

**Shannon Pattern**: Use `console.error()` in JavaScript/TypeScript, `sys.stderr` in Python

---

## Defense-in-Depth Application

After finding root cause, **don't just fix the trigger**—make bug structurally impossible.

**Invoke Sub-Skill**:
```
@skill defense-in-depth

Root Cause: {identified_trigger}
Call Chain: {complete_trace}
Boundary Crossings: {list_of_boundaries}

Goal: Add validation at EVERY layer to prevent this bug class
```

**Result**: 4-layer protection

Example for "undefined user" bug:
```
Layer 1 (Entry - Controller): Validate req.user exists, reject if missing
Layer 2 (Business Logic - Service): Check user defined before processing
Layer 3 (Utilities - Validator): Assert user not undefined at function entry
Layer 4 (Debug - Logging): Log all cases where user undefined reaches validator
```

**Shannon Principle**: Fix at source + defend at all layers = bug structurally impossible

---

## Integration with Systematic Debugging

This skill is invoked during **Phase 1: Root Cause Investigation**:

```
systematic-debugging (Phase 1)
  └─> root-cause-tracing (when multi-frame stack trace detected)
       └─> Returns: Original trigger + trace depth + confidence
            └─> systematic-debugging continues to Phase 2
```

**Workflow**:
1. Systematic debugging detects multi-frame error
2. Invokes root-cause-tracing with error location
3. Tracing returns trigger + confidence ≥ 0.80
4. Systematic debugging uses trigger for Phase 2 (Pattern Analysis)

---

## Practical Tools

### Finding Test Pollution Source

When tests fail intermittently due to pollution from other tests:

**Bisection Script** (`find-polluter.sh`):
```bash
#!/bin/bash
# Binary search to find which test pollutes state

all_tests=$(find tests -name "*.test.js")
test_to_debug="tests/api/users.test.js"

# Function to run subset and check if target test fails
check_failure() {
    local test_list="$1"
    npm test -- $test_list $test_to_debug &> /dev/null
    return $?
}

# Binary search
test_array=($all_tests)
left=0
right=${#test_array[@]}

while [ $left -lt $right ]; do
    mid=$(( (left + right) / 2 ))
    subset="${test_array[@]:0:$mid}"

    if check_failure "$subset"; then
        # Pollution in first half
        right=$mid
    else
        # Pollution in second half
        left=$((mid + 1))
    fi
done

echo "Polluter found: ${test_array[$left]}"
```

**Usage**:
```bash
chmod +x find-polluter.sh
./find-polluter.sh
# Output: tests/auth/login.test.js (pollutes state)
```

---

## Examples

### Example 1: API Error Deep Stack

**Symptom**: TypeError at `src/utils/formatter.ts:230`
```
Cannot read property 'toUpperCase' of undefined
```

**Step 1**: Observed symptom - formatter expects string, receives undefined

**Step 2**: Immediate cause - `formatName(user.name)` but `user.name` undefined

**Step 3**: Caller - `src/services/userService.ts:145` calls `formatName(user.name)`

**Step 4**: Tracing up:
```
Frame 5: formatName() - ERROR
Frame 4: buildUserProfile() - calls formatName, no validation
Frame 3: getUserProfile() - retrieves user from DB
Frame 2: Database query returns user without name field
Frame 1: Database schema missing default for name field
```

**Trace Depth**: 5 frames (Medium)
**Boundary Crossings**: 2 (Service → Utils, Service → Database)

**Step 5**: Original trigger - **Database query doesn't validate schema**
```
Trigger: src/database/queries.ts:80
Issue: Query SELECT * doesn't ensure name field exists
Category: Missing Validation
Confidence: 0.85
```

**Defense-in-Depth Applied**:
```
Layer 1: Database query validates name field exists in result
Layer 2: getUserProfile() checks user.name before returning
Layer 3: buildUserProfile() validates user.name before formatting
Layer 4: formatName() asserts input is string, logs undefined cases
```

**Result**: Bug impossible - validated at 4 layers

---

### Example 2: Race Condition

**Symptom**: Intermittent null pointer in `src/cache/manager.ts:340`

**Step 1**: Observed symptom - cache.get() returns null unexpectedly

**Step 2**: Immediate cause - cache accessed before initialization complete

**Step 3**: Caller - `src/services/dataService.ts:90` calls `cache.get(key)`

**Step 4**: Tracing up:
```
Frame 4: cache.get() - ERROR (race condition)
Frame 3: dataService.fetchData() - assumes cache ready
Frame 2: API handler calls fetchData() immediately
Frame 1: App initialization: cache.init() called but not awaited
```

**Trace Depth**: 4 frames (Medium)
**Boundary Crossings**: 2 (API → Service → Cache)

**Step 5**: Original trigger - **App doesn't await cache initialization**
```
Trigger: src/app.ts:25
Issue: cache.init() started but not awaited before starting server
Category: Race Condition
Confidence: 0.88
```

**Instrumentation Added**:
```javascript
// Before problematic operation
console.error(`[TRACE] Cache state: ${cache.isInitialized()}`);
console.error(`[TRACE] Caller: ${new Error().stack}`);
```

**Defense-in-Depth Applied**:
```
Layer 1: App awaits cache.init() before starting server
Layer 2: Cache.get() checks initialization, throws if not ready
Layer 3: DataService waits for cache ready event before first use
Layer 4: Monitoring logs all "cache not ready" occurrences
```

**Result**: Race condition eliminated at source + 4 safety layers

---

## Anti-Rationalization

### Rationalization 1: "Error location is obvious, fix it there"

**COUNTER**:
- ❌ Error location = symptom location, not cause location
- ❌ Fixing symptom = bug reappears elsewhere
- ✅ Tracing takes 5-10 minutes
- ✅ Fixing source = eliminates entire bug class

**Rule**: Always trace to original trigger, even if "obvious"

---

### Rationalization 2: "Stack trace is too deep, just fix the visible part"

**COUNTER**:
- ❌ Deep traces = important architectural flows
- ❌ Partial fix = technical debt
- ✅ Instrumentation makes deep traces tractable
- ✅ Defense-in-depth protects all layers

**Rule**: Trace depth doesn't matter - find the source

---

### Rationalization 3: "Multiple places could be the cause, fix all of them"

**COUNTER**:
- ❌ Fixing multiple places = shotgun debugging
- ❌ Confounds which fix actually worked
- ✅ Trace identifies THE trigger
- ✅ Defense-in-depth adds systematic protection

**Rule**: Identify ONE trigger, fix at source, defend at all layers

---

## Serena Integration

**Save Trace for Pattern Detection**:
```
write_memory("shannon_trace_{timestamp}", {
  symptom_location: "{file:line}",
  trace_depth: {number},
  boundary_crossings: {count},
  trigger_location: "{file:line}",
  trigger_category: "{category}",
  confidence: {0.00-1.00},
  defense_layers: [list of 4 layers],
  timestamp: "{ISO_timestamp}"
})
```

**Pattern Detection**:
```
# Query similar traces
all_traces = list_memories(pattern="shannon_trace_*")
similar = [t for t in all_traces if t.trigger_category == "Missing Validation"]

# Learn: 70% of bugs are "Missing Validation" at API boundaries
# Recommendation: Add API validation framework
```

---

## Testing Requirements

Following Shannon's functional testing protocol:

### RED Phase (Baseline)
- Test tracing WITHOUT systematic process
- Agent stops at symptom location
- Agent proposes fix without finding trigger
- Document all violations

### GREEN Phase (Compliance)
- Test tracing WITH 5-step process
- Agent traces to original trigger
- Agent applies defense-in-depth
- All violations prevented

### REFACTOR Phase (Pressure)
- Very deep trace (15+ frames)
- Multiple boundary crossings
- Unclear call path (async, callbacks)
- Verify tracing succeeds

**Success Criteria**: >85% of traces find original trigger with confidence ≥ 0.80

---

## Status

**Implementation Status**: ✅ Ready for functional testing
**Version**: 5.4.0
**Dependencies**: defense-in-depth, systematic-debugging
**MCP Required**: Serena (optional), Sequential (optional)

---

**The Bottom Line**: Surface errors are symptoms. Original triggers are root causes. Fix at the source, defend at every layer, make bugs structurally impossible.
