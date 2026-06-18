---
name: defense-in-depth
description: |
  Multi-layer validation pattern that makes bugs structurally impossible. Validates at EVERY layer
  data passes through, not just entry points. Prevents bypassing through alternate paths, test mocks,
  or future code changes. Integrated with NO MOCKS philosophy for complete system protection.

skill-type: PATTERN
shannon-version: ">=5.4.0"
category: testing

invoked-by-skills:
  - systematic-debugging
  - root-cause-tracing

related-skills:
  - functional-testing
  - systematic-debugging
  - root-cause-tracing

mcp-requirements:
  recommended:
    - name: serena
      purpose: Track defense layer coverage across features

allowed-tools: [Read, Write, Grep, Bash, Serena]
---

# Defense in Depth

## Purpose

Implement **multi-layer validation** that makes bugs structurally impossible by validating at EVERY layer data passes through, not relying on a single checkpoint that can be bypassed.

**Core Principle**: "Validate at EVERY layer data passes through. Make the bug structurally impossible."

**Shannon Integration**: Quantified layer coverage (0-4), NO MOCKS compliance (validates against real systems), Serena tracking for coverage patterns.

---

## The Core Problem

### Single-Layer Validation (Fragile)

```
❌ FRAGILE PATTERN:

User Input → API Validation → Process → Database
                    ↑
                Only validation point
```

**What Can Go Wrong**:
1. Alternate entry point bypasses API (WebSocket, CLI, internal call)
2. Test mocks bypass validation
3. Future code change removes validation
4. Validation logic has bug
5. Exception handling bypasses validation

**Result**: One failure point = system vulnerable

---

### Multi-Layer Validation (Defense-in-Depth)

```
✅ DEFENSE-IN-DEPTH:

User Input → [Layer 1: Entry Validation]
             ↓
         Business Logic → [Layer 2: Logic Validation]
             ↓
         Environment → [Layer 3: Context Guards]
             ↓
         Execution → [Layer 4: Debug Instrumentation]
```

**Benefits**:
1. Multiple entry points all validated
2. Tests cannot bypass (validation in business logic)
3. Code changes still protected (multiple layers)
4. One layer fails → others catch it
5. Exceptions handled at each layer

**Result**: Four failure points required = bug structurally impossible

---

## The Four-Layer Framework

### Layer 1: Entry Point Validation

**Purpose**: Reject problematic input at system boundaries

**Location**: API handlers, CLI parsers, event listeners, WebSocket handlers

**What to Validate**:
```
- Type checking (string, number, object)
- Null/undefined/empty checks
- Format validation (email, URL, UUID)
- Range validation (min, max, length)
- Required fields present
- Enum values valid
```

**Implementation Pattern**:
```typescript
// API Entry Point
app.post('/api/users', (req, res) => {
  // Layer 1: Entry Point Validation
  if (!req.body.email) {
    return res.status(400).json({ error: 'Email required' });
  }

  if (typeof req.body.email !== 'string') {
    return res.status(400).json({ error: 'Email must be string' });
  }

  if (req.body.email.length === 0) {
    return res.status(400).json({ error: 'Email cannot be empty' });
  }

  if (!isValidEmail(req.body.email)) {
    return res.status(400).json({ error: 'Email format invalid' });
  }

  // Proceed to Layer 2
  const result = await userService.createUser(req.body);
  res.json(result);
});
```

**Shannon Metric**: Count validation checks at entry
```
entry_validations = [
  'email required',
  'email type string',
  'email not empty',
  'email format valid'
]
layer_1_coverage = len(entry_validations)  # 4 checks
```

---

### Layer 2: Business Logic Validation

**Purpose**: Ensure data appropriateness for specific operations

**Location**: Service classes, business logic functions, domain models

**What to Validate**:
```
- Business rules (age >= 18 for adult content)
- Data relationships (user exists before assigning role)
- State transitions (order can only be cancelled if pending)
- Constraints (no duplicate emails)
- Operation preconditions (account active before transfer)
```

**Implementation Pattern**:
```typescript
// Service Layer
class UserService {
  async createUser(userData: CreateUserDto) {
    // Layer 2: Business Logic Validation

    // Validate again (entry might be bypassed)
    if (!userData.email || userData.email.length === 0) {
      throw new BusinessError('Email required for user creation');
    }

    // Business rule: Check duplicate email
    const existing = await this.userRepo.findByEmail(userData.email);
    if (existing) {
      throw new BusinessError('Email already registered');
    }

    // Business rule: Age requirement
    if (userData.age < 18) {
      throw new BusinessError('Users must be 18 or older');
    }

    // Business rule: Email domain allowed
    if (this.isBlockedDomain(userData.email)) {
      throw new BusinessError('Email domain not allowed');
    }

    // Proceed to Layer 3
    return this.userRepo.create(userData);
  }
}
```

**Shannon Metric**: Count business rule validations
```
business_validations = [
  'email required (redundant check)',
  'no duplicate email',
  'age minimum 18',
  'domain not blocked'
]
layer_2_coverage = len(business_validations)  # 4 checks
```

**Why Redundant Entry Checks?**
- Service might be called internally (bypasses API)
- Tests might call service directly
- Future refactoring might remove API layer
- **Defense principle: Never assume previous validation**

---

### Layer 3: Environment Guards

**Purpose**: Context-specific safeguards for execution environment

**Location**: Test environment checks, configuration guards, deployment gates

**What to Guard**:
```
- Test environment restrictions (no production DB in tests)
- File system boundaries (tests only write to /tmp)
- Network restrictions (tests don't call external APIs)
- Database isolation (tests use test DB, not production)
- Resource limits (operations timeout after X seconds)
```

**Implementation Pattern**:
```typescript
// Repository Layer
class UserRepository {
  async create(userData: UserData) {
    // Layer 3: Environment Guards

    // Test environment: Ensure using test database
    if (process.env.NODE_ENV === 'test') {
      if (!this.connection.database.includes('test')) {
        throw new EnvironmentError(
          'TEST VIOLATION: Test trying to write to production database'
        );
      }

      if (this.connection.host !== 'localhost') {
        throw new EnvironmentError(
          'TEST VIOLATION: Test trying to write to remote database'
        );
      }
    }

    // Production environment: Rate limiting
    if (process.env.NODE_ENV === 'production') {
      const recentCreations = await this.countRecentCreations(userData.ip);
      if (recentCreations > 10) {
        throw new RateLimitError('Too many user creations from this IP');
      }
    }

    // All environments: Validate email not null (defensive)
    if (!userData.email) {
      throw new DataError('Cannot create user without email');
    }

    // Proceed to database
    return this.db.insert('users', userData);
  }
}
```

**Shannon Metric**: Count environment guards
```
environment_guards = [
  'test database check',
  'test localhost check',
  'production rate limiting',
  'null email check'
]
layer_3_coverage = len(environment_guards)  # 4 guards
```

**Shannon NO MOCKS Integration**:
- Layer 3 guards PREVENT tests from using mocks
- Tests that bypass validation are caught here
- Forces real system usage (database, filesystem)

---

### Layer 4: Debug Instrumentation

**Purpose**: Capture diagnostic information when issues occur despite layers 1-3

**Location**: Logging, monitoring, error tracking, metrics

**What to Instrument**:
```
- Boundary crossings (data entering/leaving functions)
- Validation failures (which layer caught issue)
- Edge cases (null values, empty arrays, unexpected types)
- Performance metrics (slow operations)
- Error context (stack traces, input data, environment)
```

**Implementation Pattern**:
```typescript
// Instrumentation Wrapper
function instrumentedValidation<T>(
  layerName: string,
  validationFn: () => T
): T {
  // Layer 4: Debug Instrumentation

  const startTime = Date.now();

  try {
    const result = validationFn();

    // Log successful validation
    logger.debug({
      layer: layerName,
      status: 'PASSED',
      duration: Date.now() - startTime
    });

    return result;
  } catch (error) {
    // Log validation failure with full context
    logger.error({
      layer: layerName,
      status: 'FAILED',
      error: error.message,
      stack: error.stack,
      duration: Date.now() - startTime,
      // Capture call stack for debugging
      callStack: new Error().stack
    });

    throw error;
  }
}

// Usage
class UserService {
  async createUser(userData: CreateUserDto) {
    return instrumentedValidation('UserService.createUser', async () => {
      // Business logic with Layer 2 validation
      if (!userData.email) {
        throw new Error('Email required');
      }
      // ... rest of validation
    });
  }
}
```

**Shannon Metric**: Instrumentation coverage
```
instrumentation_points = [
  'entry point logging',
  'business logic logging',
  'environment guard logging',
  'error context capture'
]
layer_4_coverage = len(instrumentation_points)  # 4 instruments
```

**What Layer 4 Reveals**:
- Which layers catch issues most often
- Patterns in validation failures
- Performance bottlenecks
- Data quality problems

---

## Implementation Workflow

### Step 1: Trace Data Flow

**Goal**: Map all places data passes through

**Actions**:
```
1. Start at entry point (API, CLI, event)
2. Follow data through call chain
3. Identify all functions that process data
4. Note component boundaries
5. Find final destination (database, file, external API)
```

**Output**: Data flow diagram

Example:
```
HTTP Request → API Handler → UserService → UserRepository → Database
               (Entry)       (Business)    (Environment)    (Storage)
```

---

### Step 2: Map Checkpoint Locations

**Goal**: Identify where validation should occur

**Actions**:
```
For each layer, identify checkpoint location:

Layer 1: Entry points
- API handler
- CLI argument parser
- WebSocket message handler
- Event listener

Layer 2: Business logic
- Service class methods
- Domain model validation
- Business rule enforcement

Layer 3: Environment guards
- Repository/DAO methods
- External API clients
- File system operations
- Test environment checks

Layer 4: Instrumentation
- Function entry/exit
- Error handlers
- Monitoring middleware
```

**Output**: Checkpoint map with layer assignments

---

### Step 3: Add Validation at Each Layer

**Goal**: Implement validation at all checkpoints

**Actions**:

1. **Layer 1: Entry Validation**
   ```
   - Add type checks
   - Add null/empty checks
   - Add format validation
   - Return errors before processing
   ```

2. **Layer 2: Business Validation**
   ```
   - Add business rule checks
   - Add relationship validation
   - Add state transition checks
   - Throw business errors
   ```

3. **Layer 3: Environment Guards**
   ```
   - Add test environment checks
   - Add resource limits
   - Add isolation checks
   - Throw environment errors
   ```

4. **Layer 4: Instrumentation**
   ```
   - Add logging at boundaries
   - Add error context capture
   - Add metrics collection
   - Enable debugging
   ```

**Output**: Validation code at each layer

---

### Step 4: Test Layer-Bypass Scenarios

**Goal**: Verify each layer catches issues independently

**Test Cases**:

1. **Bypass Layer 1** (simulate internal call)
   ```typescript
   // Direct service call, skipping API validation
   test('Layer 2 catches invalid data when Layer 1 bypassed', async () => {
     await expect(
       userService.createUser({ email: '' })  // Invalid
     ).rejects.toThrow('Email required');
   });
   ```

2. **Bypass Layer 2** (simulate test with mock)
   ```typescript
   // Layer 3 should catch test trying to use production DB
   test('Layer 3 catches production DB usage in tests', async () => {
     process.env.NODE_ENV = 'test';
     const prodRepo = new UserRepository(productionConnection);

     await expect(
       prodRepo.create(validUser)
     ).rejects.toThrow('TEST VIOLATION');
   });
   ```

3. **Bypass Layers 1-3** (simulate bug in validation)
   ```typescript
   // Layer 4 should log the issue for debugging
   test('Layer 4 logs invalid data that bypassed validation', async () => {
     const logSpy = jest.spyOn(logger, 'error');

     try {
       await userService.createUser({ email: null });
     } catch (e) {
       // Layer 4 should have logged error with context
       expect(logSpy).toHaveBeenCalledWith(
         expect.objectContaining({
           layer: 'UserService.createUser',
           status: 'FAILED',
           error: expect.stringContaining('Email required')
         })
       );
     }
   });
   ```

**Success Criteria**: Each layer independently catches issues

---

## Shannon Quantitative Metrics

### Defense Layer Coverage Score

```
layer_coverage = (implemented_layers / 4) * 100

Examples:
- 0 layers: 0% (No defense)
- 1 layer: 25% (Fragile - single point of failure)
- 2 layers: 50% (Basic - some redundancy)
- 3 layers: 75% (Good - multiple defenses)
- 4 layers: 100% (Excellent - defense-in-depth)

Shannon Target: ≥75% (3+ layers) for mission-critical features
```

### Validation Redundancy Score

```
redundancy = (total_validations across all layers) / (unique validation rules)

Example:
- Email validation appears in 3 layers
- Unique rule: "Email required"
- Redundancy: 3.0 (validated at 3 layers)

Shannon Target: ≥2.0 (each rule validated at 2+ layers)
```

### Bypass Resistance Score

```
bypass_resistance = (layers_tested_independently / 4) * 100

Example:
- Test Layer 1 bypass: ✅ Layer 2 caught it
- Test Layer 2 bypass: ✅ Layer 3 caught it
- Test Layer 3 bypass: ✅ Layer 4 logged it
- Bypass resistance: 75%

Shannon Target: 100% (all layers tested for bypass resistance)
```

---

## Examples

### Example 1: User Creation with Defense-in-Depth

**Scenario**: Prevent creating users with invalid emails

**Layer 1: Entry Point (API)**
```typescript
app.post('/api/users', (req, res) => {
  // Validation 1.1: Email required
  if (!req.body.email) {
    return res.status(400).json({ error: 'Email required' });
  }

  // Validation 1.2: Email type
  if (typeof req.body.email !== 'string') {
    return res.status(400).json({ error: 'Email must be string' });
  }

  // Validation 1.3: Email not empty
  if (req.body.email.trim().length === 0) {
    return res.status(400).json({ error: 'Email cannot be empty' });
  }

  // Validation 1.4: Email format
  if (!isValidEmail(req.body.email)) {
    return res.status(400).json({ error: 'Invalid email format' });
  }

  const result = await userService.createUser(req.body);
  res.json(result);
});
```

**Layer 2: Business Logic (Service)**
```typescript
class UserService {
  async createUser(userData: CreateUserDto) {
    // Validation 2.1: Email required (redundant by design)
    if (!userData.email || userData.email.trim().length === 0) {
      throw new BusinessError('Email required for user creation');
    }

    // Validation 2.2: Duplicate email
    const existing = await this.userRepo.findByEmail(userData.email);
    if (existing) {
      throw new BusinessError('Email already registered');
    }

    // Validation 2.3: Blocked domains
    const domain = userData.email.split('@')[1];
    if (this.blockedDomains.includes(domain)) {
      throw new BusinessError(`Email domain ${domain} not allowed`);
    }

    return this.userRepo.create(userData);
  }
}
```

**Layer 3: Environment Guards (Repository)**
```typescript
class UserRepository {
  async create(userData: UserData) {
    // Guard 3.1: Test environment check
    if (process.env.NODE_ENV === 'test') {
      if (!this.db.database.includes('test')) {
        throw new EnvironmentError(
          'TEST VIOLATION: Attempting to write to production database'
        );
      }
    }

    // Guard 3.2: Email validation (defensive - should never be null here)
    if (!userData.email) {
      throw new DataError('Invalid state: User email is null');
    }

    // Guard 3.3: Email length
    if (userData.email.length > 255) {
      throw new DataError('Email exceeds database field length');
    }

    return this.db.insert('users', userData);
  }
}
```

**Layer 4: Debug Instrumentation**
```typescript
// Instrumentation in each layer
logger.info({
  layer: 'API',
  action: 'user_creation',
  email: userData.email,
  timestamp: new Date()
});

// Error instrumentation
try {
  await userService.createUser(userData);
} catch (error) {
  logger.error({
    layer: 'UserService',
    action: 'user_creation',
    error: error.message,
    stack: error.stack,
    input: userData,
    timestamp: new Date()
  });
  throw error;
}
```

**Metrics**:
```
Layer Coverage: 4/4 = 100%
Total Validations: 11
Unique Rules: 5 (required, type, empty, format, duplicate)
Redundancy Score: 2.2 (email required validated 3 times)
Bypass Resistance: 100% (all layers tested independently)
```

---

### Example 2: File Operations with Defense-in-Depth

**Scenario**: Prevent deleting files outside allowed directories

**Layer 1: Entry Point (API)**
```typescript
app.delete('/api/files/:filepath', (req, res) => {
  const filepath = req.params.filepath;

  // Validation 1.1: Path required
  if (!filepath) {
    return res.status(400).json({ error: 'File path required' });
  }

  // Validation 1.2: No path traversal
  if (filepath.includes('..')) {
    return res.status(400).json({ error: 'Path traversal not allowed' });
  }

  // Validation 1.3: Allowed directory
  if (!filepath.startsWith('/uploads/')) {
    return res.status(400).json({ error: 'Can only delete from /uploads/' });
  }

  await fileService.deleteFile(filepath);
  res.json({ success: true });
});
```

**Layer 2: Business Logic (Service)**
```typescript
class FileService {
  async deleteFile(filepath: string) {
    // Validation 2.1: Path required (redundant)
    if (!filepath || filepath.length === 0) {
      throw new BusinessError('File path required');
    }

    // Validation 2.2: Path traversal (redundant)
    const normalized = path.normalize(filepath);
    if (normalized.includes('..')) {
      throw new SecurityError('Path traversal detected');
    }

    // Validation 2.3: Resolve absolute path
    const absolutePath = path.resolve(filepath);
    const allowedDir = path.resolve('/uploads/');

    if (!absolutePath.startsWith(allowedDir)) {
      throw new SecurityError('Path outside allowed directory');
    }

    // Validation 2.4: File exists
    const exists = await fs.pathExists(absolutePath);
    if (!exists) {
      throw new BusinessError('File not found');
    }

    return this.fileRepo.delete(absolutePath);
  }
}
```

**Layer 3: Environment Guards (Repository)**
```typescript
class FileRepository {
  async delete(filepath: string) {
    // Guard 3.1: Test environment - restrict to /tmp
    if (process.env.NODE_ENV === 'test') {
      if (!filepath.startsWith('/tmp/')) {
        throw new EnvironmentError(
          'TEST VIOLATION: Tests can only delete from /tmp/'
        );
      }
    }

    // Guard 3.2: Production safeguard - no system directories
    const dangerousDirs = ['/etc/', '/usr/', '/bin/', '/sys/'];
    if (dangerousDirs.some(dir => filepath.startsWith(dir))) {
      throw new SecurityError('Cannot delete from system directories');
    }

    // Guard 3.3: Path validation (defensive)
    if (!filepath || filepath === '/') {
      throw new DataError('Invalid file path');
    }

    await fs.unlink(filepath);
  }
}
```

**Layer 4: Debug Instrumentation**
```typescript
// Audit logging for file deletions
logger.warn({
  layer: 'FileRepository',
  action: 'file_deletion',
  filepath: filepath,
  user: req.user.id,
  ip: req.ip,
  timestamp: new Date()
});

// Error logging with context
try {
  await fileRepo.delete(filepath);
} catch (error) {
  logger.error({
    layer: 'FileRepository',
    action: 'file_deletion',
    filepath: filepath,
    error: error.message,
    stack: error.stack,
    user: req.user.id,
    timestamp: new Date()
  });
  throw error;
}
```

**Metrics**:
```
Layer Coverage: 4/4 = 100%
Total Validations: 11
Unique Rules: 6 (required, traversal, directory, exists, test isolation, system dirs)
Redundancy Score: 1.8 (path traversal validated 2 times)
Bypass Resistance: 100%
```

---

## Integration with Shannon Skills

**Used By**:
- `systematic-debugging` (Phase 4: Implementation)
- `root-cause-tracing` (after finding trigger)
- `functional-testing` (test each layer independently)

**Uses**:
- `functional-testing` (NO MOCKS testing of each layer)

**Workflow**:
```
systematic-debugging → Finds root cause
                    → Implements fix at source
                    → Invokes defense-in-depth
                         → Adds 4 layers of protection
                         → Tests each layer bypass
                         → Returns layer coverage metrics
```

---

## Anti-Rationalization

### Rationalization 1: "Entry validation is enough"

**COUNTER**:
- ❌ Entry can be bypassed (internal calls, tests, future refactoring)
- ❌ Single layer = single point of failure
- ✅ Multi-layer = redundancy and safety
- ✅ Each layer takes 5-10 minutes to add

**Rule**: Always implement at least 3 layers (Entry + Business + Environment)

---

### Rationalization 2: "Redundant validation is inefficient"

**COUNTER**:
- ❌ "Efficiency" argument ignores bugs caused by bypassed validation
- ❌ Validation cost << debugging cost
- ✅ Redundancy = safety
- ✅ Performance impact negligible (microseconds per check)

**Rule**: Redundancy is a feature, not inefficiency

---

### Rationalization 3: "Tests don't need Layer 3 guards"

**COUNTER**:
- ❌ Tests are where guards are most important (prevent production data corruption)
- ❌ Without guards, tests can bypass validation via mocks
- ✅ Layer 3 enforces Shannon's NO MOCKS philosophy
- ✅ Guards prevent accidental production access from tests

**Rule**: Layer 3 (environment guards) is CRITICAL for test safety

---

## Serena Integration

**Track Layer Coverage**:
```
write_memory("shannon_defense_layers_{feature}", {
  feature: "{feature_name}",
  layer_1_validations: [list of entry checks],
  layer_2_validations: [list of business rules],
  layer_3_guards: [list of environment checks],
  layer_4_instrumentation: [list of logging points],
  layer_coverage: {0.00-1.00},
  redundancy_score: {0.0-4.0},
  bypass_resistance: {0.00-1.00},
  timestamp: "{ISO_timestamp}"
})
```

**Coverage Analysis**:
```
all_features = list_memories(pattern="shannon_defense_layers_*")
avg_coverage = mean([f.layer_coverage for f in all_features])

# Shannon Target: ≥0.75 average coverage
if avg_coverage < 0.75:
  recommend: "Add more layers to features with < 75% coverage"
```

---

## Testing Requirements

Following Shannon's functional testing protocol:

### RED Phase (Baseline)
- Test WITHOUT defense-in-depth
- Use single-layer validation only
- Attempt bypass via internal call
- Document how bypass succeeds

### GREEN Phase (Compliance)
- Implement all 4 layers
- Test each layer independently
- Attempt bypasses
- All bypasses caught by remaining layers

### REFACTOR Phase (Pressure)
- Multiple entry points
- Complex data flow
- Test environment isolation
- Verify all layers hold under pressure

**Success Criteria**: Layer coverage ≥75%, bypass resistance 100%

---

## Status

**Implementation Status**: ✅ Ready for functional testing
**Version**: 5.4.0
**Dependencies**: functional-testing
**MCP Required**: Serena (optional)

---

**The Bottom Line**: One layer = fragile. Four layers = structurally impossible to break. Redundancy is safety, not inefficiency.
