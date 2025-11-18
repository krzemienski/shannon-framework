---
name: defense-in-depth
description: Use when invalid data causes failures deep in execution, requiring validation at multiple system layers - validates at every layer data passes through using Shannon validation gates to make bugs structurally impossible with quantitative coverage tracking
---

# Defense-in-Depth Validation

## Overview

When you fix a bug caused by invalid data, adding validation at one place feels sufficient. But that single check can be bypassed by different code paths, refactoring, or mocks.

**Core principle**: Validate at EVERY layer data passes through. Make the bug structurally impossible.

## Why Multiple Layers

Single validation: "We fixed the bug"
Multiple layers: "We made the bug impossible"

Different layers catch different cases:
- Entry validation catches most bugs
- Business logic catches edge cases
- Environment guards prevent context-specific dangers
- Validation gates ensure production quality
- Debug logging helps when other layers fail

## Shannon Enhancement: The Five Layers

Shannon extends Superpowers' 4-layer model with validation gates integration.

### Layer 1: Entry Point Validation
**Purpose**: Reject obviously invalid input at API boundary

```typescript
function createProject(name: string, workingDirectory: string) {
  if (!workingDirectory || workingDirectory.trim() === '') {
    throw new Error('workingDirectory cannot be empty');
  }
  if (!existsSync(workingDirectory)) {
    throw new Error(`workingDirectory does not exist: ${workingDirectory}`);
  }
  if (!statSync(workingDirectory).isDirectory()) {
    throw new Error(`workingDirectory is not a directory: ${workingDirectory}`);
  }
  // ... proceed
}
```

### Layer 2: Business Logic Validation
**Purpose**: Ensure data makes sense for this operation

```typescript
function initializeWorkspace(projectDir: string, sessionId: string) {
  if (!projectDir) {
    throw new Error('projectDir required for workspace initialization');
  }
  // ... proceed
}
```

### Layer 3: Environment Guards
**Purpose**: Prevent dangerous operations in specific contexts

```typescript
async function gitInit(directory: string) {
  // In tests, refuse git init outside temp directories
  if (process.env.NODE_ENV === 'test') {
    const normalized = normalize(resolve(directory));
    const tmpDir = normalize(resolve(tmpdir()));

    if (!normalized.startsWith(tmpDir)) {
      throw new Error(
        `Refusing git init outside temp dir during tests: ${directory}`
      );
    }
  }
  // ... proceed
}
```

### Layer 4: Validation Gates (Shannon)
**Purpose**: Run Shannon's 3-tier validation at critical checkpoints

```typescript
async function deployFeature(feature: Feature) {
  // Shannon's 3-tier validation
  const gates = await runValidationGates(feature);

  // Tier 1: Flow validation
  if (!gates.tier1.pass) {
    throw new Error(`Flow validation failed: ${gates.tier1.errors}`);
  }

  // Tier 2: Artifact validation
  if (!gates.tier2.pass) {
    throw new Error(`Artifact validation failed: ${gates.tier2.errors}`);
  }

  // Tier 3: Functional validation (NO MOCKS)
  if (!gates.tier3.pass) {
    throw new Error(`Functional validation failed: ${gates.tier3.errors}`);
  }

  // All gates passed, proceed with deployment
  // ... proceed
}
```

### Layer 5: Debug Instrumentation
**Purpose**: Capture context for forensics and Serena learning

```typescript
async function gitInit(directory: string) {
  const stack = new Error().stack;

  // Shannon: Save to Serena for pattern analysis
  await serena.write_memory(`operations/git_init/${Date.now()}`, {
    operation: 'git_init',
    directory,
    cwd: process.cwd(),
    env: process.env.NODE_ENV,
    stack_depth: stack.split('\n').length,
    timestamp: new Date().toISOString()
  });

  logger.debug('About to git init', {
    directory,
    cwd: process.cwd(),
    stack,
  });

  // ... proceed
}
```

## Applying the Pattern

When you find a bug:

1. **Trace the data flow** (use root-cause-tracing skill)
   - Where does bad value originate?
   - Where is it used?

2. **Map all checkpoints**
   - List every point data passes through
   - Identify which layers apply

3. **Add validation at each layer**
   - Layer 1: Entry point
   - Layer 2: Business logic
   - Layer 3: Environment guards
   - Layer 4: Validation gates (Shannon)
   - Layer 5: Debug instrumentation

4. **Test each layer**
   - Try to bypass layer 1, verify layer 2 catches it
   - Try to bypass layers 1-2, verify layer 3 catches it
   - Verify gates run at checkpoints (layer 4)
   - Verify instrumentation captures forensics (layer 5)

## Example from Session

Bug: Empty `projectDir` caused `git init` in source code

**Data flow**:
1. Test setup → empty string
2. `Project.create(name, '')`
3. `WorkspaceManager.createWorkspace('')`
4. `git init` runs in `process.cwd()`

**Five layers added** (Shannon enhancement):
- Layer 1: `Project.create()` validates not empty/exists/writable
- Layer 2: `WorkspaceManager` validates projectDir not empty
- Layer 3: `WorktreeManager` refuses git init outside tmpdir in tests
- Layer 4: Validation gates before critical operations
- Layer 5: Stack trace logging + Serena persistence

**Result**: All 1847 tests passed, bug impossible to reproduce

**Shannon tracking**:
```python
defense_coverage = {
    "bug_id": "empty_projectDir",
    "layers_added": 5,
    "coverage": {
        "entry_point": True,
        "business_logic": True,
        "environment_guards": True,
        "validation_gates": True,
        "instrumentation": True
    },
    "tests_passed": "1847/1847",
    "bug_reproducible": False,
    "timestamp": ISO_timestamp
}

serena.write_memory("defense/coverage/empty_projectDir", defense_coverage)
```

## Shannon-Specific Patterns

### Integration with Validation Gates

**At critical checkpoints, run Shannon's 3-tier validation**:

```typescript
async function criticalOperation(data: unknown) {
  // Layer 1: Entry validation
  validateInput(data);

  // Layer 2: Business validation
  validateBusinessRules(data);

  // Layer 3: Environment guards
  if (process.env.NODE_ENV === 'production') {
    requireProductionChecks(data);
  }

  // Layer 4: Shannon validation gates
  const gates = await runValidationGates({
    tier1: () => checkFlow(data),
    tier2: () => checkArtifacts(data),
    tier3: () => checkFunctional(data)  // NO MOCKS
  });

  if (!gates.allPass) {
    throw new ValidationError('Gates failed', gates.failures);
  }

  // Layer 5: Instrumentation
  await logToSerena('criticalOperation', { data, gates });

  // Now safe to proceed
  // ...
}
```

### Quantitative Coverage Tracking

**Shannon requirement**: Track defense coverage quantitatively:

```python
# After adding defense layers
coverage_metrics = {
    "total_layers": 5,
    "layers_implemented": {
        "entry_point": True,
        "business_logic": True,
        "environment_guards": True,
        "validation_gates": True,
        "instrumentation": True
    },
    "coverage_percentage": 100.0,  # 5/5 layers
    "test_verification": {
        "bypass_attempts": 5,
        "all_caught": True,
        "layer_effectiveness": {
            "layer1_catches": 3,  # 60% of bypass attempts
            "layer2_catches": 1,  # 20%
            "layer3_catches": 1,  # 20%
            "layer4_catches": 0,  # All caught before gates
            "layer5_detected": 5  # 100% logged
        }
    }
}

serena.write_memory("defense/metrics/{feature_id}", coverage_metrics)
```

### Pattern Learning from Defense Layers

**Shannon learns which patterns work**:

```python
# Query historical defense implementations
defense_history = serena.query_memory("defense/metrics/*")

# Analyze effectiveness
analysis = {
    "total_defenses": len(defense_history),
    "avg_layers": average([d["total_layers"] for d in defense_history]),
    "most_effective_layer": "entry_point",  # Catches 65% on average
    "least_bypassed": "validation_gates",  # Never bypassed
    "recommendation": "Always implement layer 4 (gates) for critical operations"
}

# Use this to guide future defense implementations
```

## Key Insight

All five layers were necessary. During testing, each layer caught bugs the others missed:
- Different code paths bypassed entry validation
- Mocks bypassed business logic checks (Shannon NO MOCKS prevents this)
- Edge cases on different platforms needed environment guards
- Validation gates caught integration issues
- Debug logging identified structural misuse

**Don't stop at one validation point.** Add checks at every layer.

## Integration with Other Skills

**This skill works with**:
- **root-cause-tracing** - Find all layers data passes through
- **systematic-debugging** - After finding root cause, add defense
- **verification-before-completion** - Verify all layers work
- **test-driven-development** - Write tests for each layer

**Shannon integration**:
- **Validation gates** - Layer 4 runs 3-tier validation
- **Serena MCP** - Track defense patterns, learn effectiveness
- **NO MOCKS** - Layer 4 must use real systems

## Verification Checklist

After adding defense layers:

- [ ] Layer 1: Entry point validation added
- [ ] Layer 2: Business logic validation added
- [ ] Layer 3: Environment guards added (if applicable)
- [ ] Layer 4: Validation gates integrated (Shannon)
- [ ] Layer 5: Debug instrumentation + Serena logging
- [ ] **Tested each layer independently**
- [ ] **Verified bypass attempts caught**
- [ ] **All tests pass**
- [ ] **Coverage tracked in Serena**

## The Bottom Line

**One layer = fixed the bug. Five layers = made it impossible.**

Shannon's quantitative tracking + validation gates makes defense-in-depth measurable and verifiable.

Not "seems solid" - **proven solid** through multi-layer verification.

