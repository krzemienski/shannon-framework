# Test Case: Wave Orchestration with Parallel Execution

**Test ID**: TC-004
**Priority**: Critical
**Category**: Orchestration/Performance
**Estimated Time**: 25 minutes

## Objective

Validate that Shannon's wave orchestration system correctly executes parallel waves, manages wave boundaries, coordinates sub-agents, and produces coherent results across multiple waves.

## Prerequisites

- [ ] Shannon project loaded in Claude Code
- [ ] Serena MCP configured and functional
- [ ] Sequential MCP configured and functional
- [ ] Test project with moderate complexity
- [ ] Test environment: /Users/nick/Documents/shannon

## Test Steps

### Step 1: Setup Multi-Module Test Project

```bash
# Create project structure for wave testing
cd /Users/nick/Documents/shannon
mkdir -p test-wave-project/{auth,api,database,ui,tests}
mkdir -p test-results/TC-004/{artifacts,screenshots,logs}

# Create authentication module
cat > test-wave-project/auth/user_auth.py << 'EOF'
"""User authentication module."""
from typing import Optional

class UserAuth:
    def authenticate(self, username: str, password: str) -> bool:
        # Basic authentication
        return username and password and len(password) >= 8

    def generate_token(self, user_id: int) -> str:
        # Token generation
        return f"token_{user_id}"
EOF

# Create API module
cat > test-wave-project/api/endpoints.py << 'EOF'
"""API endpoints."""
from typing import Dict, Any

class UserAPI:
    def get_user(self, user_id: int) -> Dict[str, Any]:
        # Fetch user data
        return {"id": user_id, "name": "Test User"}

    def update_user(self, user_id: int, data: Dict[str, Any]) -> bool:
        # Update user data
        return True
EOF

# Create database module
cat > test-wave-project/database/models.py << 'EOF'
"""Database models."""
from typing import Optional

class User:
    def __init__(self, id: int, username: str, email: str):
        self.id = id
        self.username = username
        self.email = email

    def save(self) -> bool:
        # Save to database
        return True
EOF

# Create UI module
cat > test-wave-project/ui/components.py << 'EOF'
"""UI components."""
from typing import List, Dict

class UserList:
    def render(self, users: List[Dict]) -> str:
        # Render user list
        return "\n".join([f"User: {u['name']}" for u in users])
EOF
```

**Expected**: Multi-module project structure created

### Step 2: Load Project and Analyze Complexity

**Commands**:
```
# Load project
/sh:load test-wave-project/

# Analyze for wave orchestration
/sh:spec "Add comprehensive error handling, input validation, logging, and unit tests across all modules"
```

**Expected Behavior**:
- Project loaded successfully
- Complexity analysis performed
- Wave count recommendation: 3-4 waves
- Parallel execution opportunities identified

**Complexity Analysis Validation**:
- [ ] Overall complexity >0.6 (moderate-high)
- [ ] Multiple modules detected (4 modules)
- [ ] Wave count recommended: 3-4
- [ ] Parallel execution feasible: Yes
- [ ] Module independence identified

### Step 3: Execute Wave Orchestration Command

**Command**:
```
/sc:implement "Add comprehensive error handling, input validation, logging, and unit tests across all modules" --wave-mode --wave-count 4
```

**Expected Behavior**:
- Wave orchestration system activates
- WAVE_ORCHESTRATOR agent coordinates execution
- 4 waves planned and executed
- Parallel operations within waves
- Progress tracking shown

### Step 4: Validate Wave Orchestration Activation

**Orchestration Behavior Checklist**:
- [ ] "Wave orchestration activated" message shown
- [ ] Wave count: 4 waves planned
- [ ] Wave boundaries defined
- [ ] Module assignment to waves shown
- [ ] Parallel execution plan outlined
- [ ] WAVE_ORCHESTRATOR agent mentioned

**Wave Planning Output Example**:
```
🌊 Wave Orchestration Plan

**Wave Count**: 4 waves
**Parallelization**: Enabled

Wave 1: Error Handling Foundation
  - auth/user_auth.py (error handling)
  - api/endpoints.py (error handling)
  - database/models.py (error handling)
  - ui/components.py (error handling)
  Parallel: Yes (independent modules)

Wave 2: Input Validation
  - auth/user_auth.py (validation)
  - api/endpoints.py (validation)
  Parallel: Yes

Wave 3: Logging Integration
  - All modules (logging setup)
  Parallel: Yes

Wave 4: Unit Tests
  - tests/ (test creation for all modules)
  Parallel: Yes (test files independent)
```

### Step 5: Validate Wave 1 Execution

**Wave 1: Error Handling Foundation**

**Expected Behavior**:
- [ ] Wave 1 start message shown
- [ ] All 4 modules processed in parallel
- [ ] Progress indicators for each module
- [ ] Error handling added to all modules
- [ ] Wave 1 completion message

**Parallel Execution Validation**:
```
Processing Wave 1: Error Handling Foundation
  [auth/user_auth.py] Starting...
  [api/endpoints.py] Starting...
  [database/models.py] Starting...
  [ui/components.py] Starting...

  [auth/user_auth.py] ✅ Complete
  [api/endpoints.py] ✅ Complete
  [database/models.py] ✅ Complete
  [ui/components.py] ✅ Complete

Wave 1 Complete ✅
```

**File Changes Validation**:

```bash
# Check auth module changes
grep -n "try:\|except\|raise" test-wave-project/auth/user_auth.py

# Check API module changes
grep -n "try:\|except\|raise" test-wave-project/api/endpoints.py
```

**Expected Changes**:
- [ ] Try-except blocks added
- [ ] Custom exceptions defined or imported
- [ ] Error messages clear and descriptive
- [ ] NO placeholder error handling
- [ ] Real implementation, not mocks

### Step 6: Validate Wave 2 Execution

**Wave 2: Input Validation**

**Expected Behavior**:
- [ ] Wave 2 start message shown
- [ ] auth and api modules processed in parallel
- [ ] Input validation added
- [ ] Validation logic complete (NO MOCKS)
- [ ] Wave 2 completion message

**Validation Logic Validation**:

```bash
# Check for validation functions
grep -n "def validate\|if not\|assert\|isinstance" test-wave-project/auth/user_auth.py
```

**Expected Validation**:
- [ ] Parameter type checking
- [ ] Value range checking
- [ ] Null/empty checks
- [ ] Format validation (email, etc.)
- [ ] Real validation logic (not TODO comments)

### Step 7: Validate Wave 3 Execution

**Wave 3: Logging Integration**

**Expected Behavior**:
- [ ] Wave 3 start message shown
- [ ] All modules processed for logging
- [ ] Logging statements added strategically
- [ ] Logger configuration added
- [ ] Wave 3 completion message

**Logging Implementation Validation**:

```bash
# Check for logging imports and usage
grep -n "import logging\|logger =\|logger\.\|log\." test-wave-project/auth/user_auth.py
```

**Expected Logging**:
- [ ] `import logging` at module top
- [ ] Logger instance created
- [ ] Info logs for normal operations
- [ ] Warning logs for unusual conditions
- [ ] Error logs in exception handlers
- [ ] Debug logs for troubleshooting
- [ ] NO print statements replacing logs

### Step 8: Validate Wave 4 Execution

**Wave 4: Unit Tests**

**Expected Behavior**:
- [ ] Wave 4 start message shown
- [ ] Test files created in tests/ directory
- [ ] One test file per module
- [ ] Comprehensive test coverage
- [ ] Wave 4 completion message

**Test File Validation**:

```bash
# Check test files created
ls -la test-wave-project/tests/

# Should see:
# test_user_auth.py
# test_endpoints.py
# test_models.py
# test_components.py
```

**Test Quality Validation**:

```bash
# Check test structure
cat test-wave-project/tests/test_user_auth.py
```

**Expected Test Structure**:
- [ ] Import unittest or pytest
- [ ] Import module under test
- [ ] Multiple test cases defined
- [ ] Test error handling
- [ ] Test validation logic
- [ ] Test normal operations
- [ ] Test edge cases
- [ ] NO placeholder tests
- [ ] Tests are runnable

**Sample Expected Test**:
```python
import unittest
from auth.user_auth import UserAuth

class TestUserAuth(unittest.TestCase):
    def setUp(self):
        self.auth = UserAuth()

    def test_authenticate_valid_credentials(self):
        result = self.auth.authenticate("user", "password123")
        self.assertTrue(result)

    def test_authenticate_short_password(self):
        result = self.auth.authenticate("user", "pass")
        self.assertFalse(result)

    def test_authenticate_empty_username(self):
        result = self.auth.authenticate("", "password123")
        self.assertFalse(result)

    def test_generate_token(self):
        token = self.auth.generate_token(123)
        self.assertIsInstance(token, str)
        self.assertIn("token_", token)
```

### Step 9: Validate Wave Boundaries and Coordination

**Wave Boundary Validation**:
- [ ] Each wave completes before next starts
- [ ] No file conflicts between waves
- [ ] Changes build upon previous waves
- [ ] Wave dependencies respected
- [ ] Parallel operations within waves only

**Coordination Validation**:
- [ ] Wave 1 changes present before Wave 2
- [ ] Wave 2 changes present before Wave 3
- [ ] Wave 3 changes present before Wave 4
- [ ] Tests (Wave 4) validate earlier wave changes
- [ ] No overwrites or conflicts

**Coordination Check**:
```bash
# Check that error handling (Wave 1) is preserved
# after validation (Wave 2) and logging (Wave 3)
grep -c "try:" test-wave-project/auth/user_auth.py  # Should have error handling
grep -c "if not" test-wave-project/auth/user_auth.py  # Should have validation
grep -c "logger" test-wave-project/auth/user_auth.py  # Should have logging
```

### Step 10: Validate Parallel Execution Performance

**Performance Metrics**:

**Expected Timing** (approximate):
- Sequential execution: ~15-20 minutes
- Wave orchestration: ~8-12 minutes
- Performance gain: 30-40%

**Performance Validation**:
- [ ] Total execution time <15 minutes
- [ ] Faster than sequential equivalent
- [ ] Parallel operations visible in logs
- [ ] No race conditions or conflicts

### Step 11: Validate Final Artifact Quality

**Complete Module Validation (auth/user_auth.py)**:

```python
# Expected final state after all waves
import logging

logger = logging.getLogger(__name__)

class AuthenticationError(Exception):
    """Custom authentication exception."""
    pass

class UserAuth:
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user with validation and error handling."""
        # Input validation (Wave 2)
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        if not isinstance(password, str):
            raise TypeError("Password must be a string")
        if not username:
            logger.warning("Authentication attempted with empty username")
            return False
        if not password:
            logger.warning("Authentication attempted with empty password")
            return False

        # Error handling (Wave 1)
        try:
            # Logging (Wave 3)
            logger.info(f"Authentication attempt for user: {username}")

            # Validation logic
            if len(password) < 8:
                logger.warning(f"Password too short for user: {username}")
                return False

            # Successful authentication
            logger.info(f"User authenticated successfully: {username}")
            return True

        except Exception as e:
            logger.error(f"Authentication error for {username}: {str(e)}")
            raise AuthenticationError(f"Authentication failed: {str(e)}")

    def generate_token(self, user_id: int) -> str:
        """Generate authentication token with validation."""
        # Input validation (Wave 2)
        if not isinstance(user_id, int):
            raise TypeError("User ID must be an integer")
        if user_id <= 0:
            raise ValueError("User ID must be positive")

        try:
            # Logging (Wave 3)
            logger.info(f"Generating token for user ID: {user_id}")
            token = f"token_{user_id}"
            logger.debug(f"Token generated: {token}")
            return token

        except Exception as e:
            logger.error(f"Token generation error: {str(e)}")
            raise
```

**Quality Checklist**:
- [ ] All wave changes integrated
- [ ] Error handling complete
- [ ] Validation complete
- [ ] Logging complete
- [ ] Tests exist and pass
- [ ] NO conflicts between wave changes
- [ ] Professional code quality

### Step 12: Run Unit Tests

**Test Execution**:

```bash
cd test-wave-project
python -m pytest tests/ -v
```

**Expected Test Results**:
- [ ] All tests discovered
- [ ] All tests pass
- [ ] No syntax errors
- [ ] Test coverage reasonable (>70%)
- [ ] Tests validate wave implementations

### Step 13: Validate Wave Orchestration Artifacts

**Artifact Validation**:

```bash
# Check for wave execution logs
ls -la .shannon/waves/

# Check for wave metadata
cat .shannon/waves/wave_execution_*.json
```

**Expected Artifacts**:
- [ ] .shannon/waves/ directory exists
- [ ] Wave execution log file created
- [ ] Wave metadata includes:
  - [ ] Wave count
  - [ ] Wave boundaries
  - [ ] Module assignments
  - [ ] Execution times
  - [ ] Success status
  - [ ] Parallel execution flag

## Expected Results

**Successful Wave Orchestration**:

1. **Wave Planning**: 4 waves defined with clear boundaries
2. **Wave 1**: Error handling added to all modules
3. **Wave 2**: Input validation added where needed
4. **Wave 3**: Logging integrated across codebase
5. **Wave 4**: Comprehensive tests created
6. **Performance**: 30-40% faster than sequential
7. **Quality**: All changes integrated cleanly
8. **Tests**: All unit tests pass

## Validation Criteria

**Pass Criteria**:
- ✅ 4 waves executed successfully
- ✅ Parallel execution within waves
- ✅ All modules enhanced with error handling
- ✅ Validation logic added and complete
- ✅ Logging integrated throughout
- ✅ Unit tests created and passing
- ✅ NO MOCKS or placeholder implementations
- ✅ Wave boundaries respected
- ✅ Performance gain over sequential
- ✅ Wave artifacts generated

**Fail Criteria**:
- ❌ Wave orchestration not activated
- ❌ Sequential execution instead of parallel
- ❌ Incomplete implementations (mocks/TODOs)
- ❌ File conflicts between waves
- ❌ Tests not created or failing
- ❌ No performance gain
- ❌ Missing wave artifacts

## Debug Information

**Logs to Collect**:
- [ ] Copy wave orchestration output: test-results/TC-004/wave_output.md
- [ ] Copy all modified files: test-results/TC-004/artifacts/
- [ ] Copy test results: test-results/TC-004/test_results.txt
- [ ] Copy wave metadata: test-results/TC-004/artifacts/wave_execution.json
- [ ] Screenshots: test-results/TC-004/screenshots/

**Debug Commands**:
```bash
# Check all modifications
git diff test-wave-project/

# Count error handling additions
grep -r "try:\|except" test-wave-project/ | wc -l

# Count validation additions
grep -r "if not\|isinstance\|assert" test-wave-project/ | wc -l

# Count logging additions
grep -r "logger\." test-wave-project/ | wc -l

# Run tests
cd test-wave-project && python -m pytest tests/ -v --tb=short

# Check wave artifacts
ls -la .shannon/waves/
cat .shannon/waves/wave_execution_*.json | jq .
```

## Notes

**Record Observations**:
- Total execution time: _____ minutes
- Wave 1 time: _____ seconds
- Wave 2 time: _____ seconds
- Wave 3 time: _____ seconds
- Wave 4 time: _____ seconds
- Parallel operations count: _____
- Test pass rate: _____ %
- Performance gain: _____ %
- File conflicts: _____ (count)

**Known Issues**:
- None at test creation time

**Advanced Scenarios to Test**:
1. Wave orchestration with dependencies
2. Dynamic wave count adjustment
3. Wave failure and recovery
4. Cross-wave rollback
5. Nested wave orchestration
