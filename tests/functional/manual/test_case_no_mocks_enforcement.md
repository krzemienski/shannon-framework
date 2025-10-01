# Test Case: NO MOCKS Rule Enforcement

**Test ID**: TC-006
**Priority**: Critical
**Category**: Behavioral/Quality Enforcement
**Estimated Time**: 20 minutes

## Objective

Validate that Shannon consistently enforces the NO MOCKS rule across all commands, preventing placeholder implementations, incomplete code, and TODO comments in generated artifacts.

## Prerequisites

- [ ] Shannon project loaded in Claude Code
- [ ] Serena MCP configured and functional
- [ ] Test project structure available
- [ ] Test environment: /Users/nick/Documents/shannon

## Test Steps

### Step 1: Setup Test Project Structure

```bash
# Create test project
cd /Users/nick/Documents/shannon
mkdir -p test-no-mocks/{src,tests,api}
mkdir -p test-results/TC-006/{artifacts,violations,logs}

# Create initial baseline file
cat > test-no-mocks/src/base_module.py << 'EOF'
"""Base module for NO MOCKS testing."""
from typing import Dict, List

class DataService:
    def fetch_data(self, query: str) -> List[Dict]:
        """Fetch data from source."""
        # Real implementation
        return [{"id": 1, "value": "test"}]

    def save_data(self, data: Dict) -> bool:
        """Save data to storage."""
        # Real implementation
        return True
EOF
```

**Expected**: Clean baseline without mocks

### Step 2: Test Case 1 - Simple Feature Implementation

**Command**:
```
/sc:implement "Add input validation to DataService.fetch_data method"
```

**Expected Behavior**:
- Real validation logic implemented
- NO TODO comments
- NO placeholder implementations
- NO mock validation

**Validation Checklist**:

```bash
# Check for mock patterns
grep -i "todo\|mock\|placeholder\|fix.*me\|implement.*later" test-no-mocks/src/base_module.py
```

- [ ] Exit code: 1 (no matches found)
- [ ] NO `# TODO: add validation`
- [ ] NO `# Mock implementation`
- [ ] NO `# FIXME: complete this`
- [ ] NO `pass  # Implement later`

**Expected Implementation**:

```python
def fetch_data(self, query: str) -> List[Dict]:
    """Fetch data from source with validation."""
    # Real validation (NOT mock)
    if not query:
        raise ValueError("Query cannot be empty")
    if not isinstance(query, str):
        raise TypeError("Query must be a string")
    if len(query) > 1000:
        raise ValueError("Query too long (max 1000 characters)")

    # Real implementation
    return [{"id": 1, "value": "test", "query": query}]
```

**Quality Validation**:
- [ ] Validation logic complete and functional
- [ ] Error messages descriptive
- [ ] Type checking implemented
- [ ] Edge cases handled
- [ ] NO placeholder comments

### Step 3: Test Case 2 - Complex Feature with Multiple Components

**Command**:
```
/sc:implement "Add authentication system with user registration, login, logout, and token management"
```

**Expected Behavior**:
- Complete authentication implementation
- Real password hashing (not mocked)
- Real token generation (not mocked)
- Real session management (not mocked)

**Implementation Validation**:

```bash
# Check for mocks in authentication
grep -i "todo\|mock\|placeholder" test-no-mocks/src/auth.py
```

**Expected Implementation Patterns**:

```python
# ✅ ACCEPTABLE - Real Implementation
import hashlib
import secrets
from datetime import datetime, timedelta

class AuthService:
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt or similar."""
        salt = secrets.token_hex(16)
        hash_value = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt.encode(),
            100000
        )
        return f"{salt}${hash_value.hex()}"

    def generate_token(self, user_id: int) -> str:
        """Generate JWT or session token."""
        token = secrets.token_urlsafe(32)
        expiry = datetime.utcnow() + timedelta(hours=24)
        # Store token with expiry in database/cache
        return token
```

**Anti-Pattern Detection**:

```python
# ❌ UNACCEPTABLE - Mock Implementation
def hash_password(self, password: str) -> str:
    """Hash password using bcrypt or similar."""
    # TODO: implement actual hashing
    return password  # Mock - return plaintext

# ❌ UNACCEPTABLE - Placeholder
def generate_token(self, user_id: int) -> str:
    """Generate JWT or session token."""
    # FIXME: use real JWT library
    return "mock_token_123"
```

**Validation Checklist**:
- [ ] Password hashing: Real algorithm (bcrypt, argon2, pbkdf2)
- [ ] Token generation: Cryptographically secure (secrets module)
- [ ] User registration: Complete validation and storage
- [ ] Login: Real authentication flow
- [ ] Logout: Real token invalidation
- [ ] NO mocks or placeholders anywhere

### Step 4: Test Case 3 - API Endpoint Creation

**Command**:
```
/sc:implement "Create REST API endpoint POST /api/users with request validation, error handling, and database integration"
```

**Expected Behavior**:
- Real request validation
- Real error responses
- Real database operations (or clear interface)
- NO mock database calls

**Validation Checklist**:

```bash
# Check API implementation
cat test-no-mocks/api/users.py
grep -i "todo\|mock\|placeholder" test-no-mocks/api/users.py
```

**Expected Implementation**:

```python
# ✅ ACCEPTABLE
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, validator

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        # Additional password complexity checks
        return v

@router.post("/api/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user with validation."""
    try:
        # Real database operation
        hashed_password = hash_password(user.password)
        user_id = database.insert_user({
            "username": user.username,
            "email": user.email,
            "password_hash": hashed_password
        })
        return {"id": user_id, "username": user.username}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
```

**Anti-Pattern Detection**:

```python
# ❌ UNACCEPTABLE
@router.post("/api/users")
async def create_user(user: UserCreate):
    """Create a new user."""
    # TODO: add validation
    # TODO: implement database integration
    return {"id": 1, "username": user.username}  # Mock response
```

**Validation Checklist**:
- [ ] Request validation: Pydantic models with validators
- [ ] Error handling: Try-except with appropriate HTTP errors
- [ ] Database integration: Real database calls or clear DAO layer
- [ ] Response format: Structured and complete
- [ ] NO TODO comments
- [ ] NO mock responses

### Step 5: Test Case 4 - Test Generation

**Command**:
```
/sc:implement "Create comprehensive unit tests for DataService class"
```

**Expected Behavior**:
- Real test cases (not empty)
- Tests actually test functionality
- Assertions present and meaningful
- NO placeholder tests

**Test Quality Validation**:

```bash
# Check test implementation
cat test-no-mocks/tests/test_data_service.py
grep -i "todo\|mock.*test\|placeholder" test-no-mocks/tests/test_data_service.py
```

**Expected Test Implementation**:

```python
# ✅ ACCEPTABLE - Real Tests
import unittest
from src.base_module import DataService

class TestDataService(unittest.TestCase):
    def setUp(self):
        self.service = DataService()

    def test_fetch_data_valid_query(self):
        """Test fetch_data with valid query."""
        result = self.service.fetch_data("test query")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn("id", result[0])
        self.assertIn("value", result[0])

    def test_fetch_data_empty_query_raises_error(self):
        """Test fetch_data with empty query raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.service.fetch_data("")
        self.assertIn("cannot be empty", str(context.exception))

    def test_fetch_data_invalid_type_raises_error(self):
        """Test fetch_data with non-string query raises TypeError."""
        with self.assertRaises(TypeError):
            self.service.fetch_data(123)  # type: ignore

    def test_save_data_valid_dict(self):
        """Test save_data with valid dictionary."""
        data = {"id": 1, "value": "test"}
        result = self.service.save_data(data)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
```

**Anti-Pattern Detection**:

```python
# ❌ UNACCEPTABLE - Mock Tests
def test_fetch_data(self):
    """Test fetch_data."""
    # TODO: implement test
    pass

def test_save_data(self):
    """Test save_data."""
    result = self.service.save_data({})
    # TODO: add assertions
```

**Validation Checklist**:
- [ ] Tests have implementations (not pass statements)
- [ ] Assertions present and meaningful
- [ ] Edge cases tested
- [ ] Error conditions tested
- [ ] Tests are runnable
- [ ] NO TODO comments in tests
- [ ] NO placeholder test methods

### Step 6: Test Case 5 - Error Handling Addition

**Command**:
```
/sc:implement "Add comprehensive error handling to all methods in DataService"
```

**Expected Behavior**:
- Real try-except blocks
- Specific exception types
- Meaningful error messages
- NO generic exception handlers

**Error Handling Validation**:

```bash
# Check error handling patterns
grep -A 5 "try:\|except" test-no-mocks/src/base_module.py
```

**Expected Implementation**:

```python
# ✅ ACCEPTABLE - Real Error Handling
def fetch_data(self, query: str) -> List[Dict]:
    """Fetch data with error handling."""
    try:
        # Validation
        if not query:
            raise ValueError("Query cannot be empty")

        # Real implementation with specific error handling
        result = self._execute_query(query)
        return result

    except ValueError as e:
        # Specific exception handling
        logging.error(f"Validation error in fetch_data: {str(e)}")
        raise

    except ConnectionError as e:
        # Network error handling
        logging.error(f"Connection error: {str(e)}")
        raise DatabaseConnectionError("Failed to connect to database") from e

    except Exception as e:
        # Unexpected error handling (last resort)
        logging.exception("Unexpected error in fetch_data")
        raise DataServiceError(f"Data fetch failed: {str(e)}") from e
```

**Anti-Pattern Detection**:

```python
# ❌ UNACCEPTABLE - Generic/Mock Error Handling
def fetch_data(self, query: str) -> List[Dict]:
    """Fetch data with error handling."""
    try:
        # TODO: implement error handling properly
        return []
    except:  # Too generic
        pass  # Silent failure - unacceptable
```

**Validation Checklist**:
- [ ] Try-except blocks present
- [ ] Specific exception types caught
- [ ] Error messages descriptive
- [ ] Logging statements included
- [ ] Error propagation appropriate
- [ ] NO bare except clauses
- [ ] NO silent failures (pass in except)
- [ ] NO generic error messages

### Step 7: Test Case 6 - Async/Concurrent Implementation

**Command**:
```
/sc:implement "Add async/await support to DataService with connection pooling and concurrent request handling"
```

**Expected Behavior**:
- Real async implementation
- Real connection pooling
- Real concurrency handling
- NO sync code marked as async

**Async Implementation Validation**:

```bash
# Check async patterns
grep -A 10 "async def\|await\|asyncio" test-no-mocks/src/base_module.py
```

**Expected Implementation**:

```python
# ✅ ACCEPTABLE - Real Async
import asyncio
from typing import List, Dict
from contextlib import asynccontextmanager

class AsyncDataService:
    def __init__(self, pool_size: int = 10):
        self.pool: asyncio.Queue = asyncio.Queue(maxsize=pool_size)
        self._initialize_pool()

    def _initialize_pool(self):
        """Initialize connection pool."""
        for _ in range(self.pool.maxsize):
            # Real connection objects
            self.pool.put_nowait(self._create_connection())

    @asynccontextmanager
    async def _get_connection(self):
        """Get connection from pool."""
        conn = await self.pool.get()
        try:
            yield conn
        finally:
            await self.pool.put(conn)

    async def fetch_data(self, query: str) -> List[Dict]:
        """Async fetch with connection pooling."""
        async with self._get_connection() as conn:
            # Real async database query
            result = await conn.execute(query)
            return await result.fetchall()

    async def batch_fetch(self, queries: List[str]) -> List[List[Dict]]:
        """Concurrent batch fetching."""
        tasks = [self.fetch_data(q) for q in queries]
        return await asyncio.gather(*tasks)
```

**Anti-Pattern Detection**:

```python
# ❌ UNACCEPTABLE - Fake Async
async def fetch_data(self, query: str) -> List[Dict]:
    """Async fetch data."""
    # TODO: make this actually async
    return self._sync_fetch(query)  # Just wrapping sync code

async def batch_fetch(self, queries: List[str]) -> List[List[Dict]]:
    """Batch fetch."""
    # Mock concurrent execution
    results = []
    for q in queries:  # Sequential, not concurrent!
        results.append(await self.fetch_data(q))
    return results
```

**Validation Checklist**:
- [ ] Real async/await implementation
- [ ] Connection pooling implemented
- [ ] Concurrent execution (not sequential)
- [ ] Async context managers used
- [ ] Error handling in async context
- [ ] NO sync code in async wrapper
- [ ] NO sequential loops pretending to be concurrent

### Step 8: Automated Mock Detection Scan

**Comprehensive Mock Detection**:

```bash
# Create comprehensive mock detection script
cat > test-results/TC-006/detect_mocks.sh << 'EOF'
#!/bin/bash

echo "=== NO MOCKS Validation Report ==="
echo ""

PROJECT_DIR="test-no-mocks"
VIOLATIONS=0

# Pattern 1: TODO comments
echo "1. Checking for TODO comments..."
TODO_COUNT=$(grep -r -i "todo\|fixme" "$PROJECT_DIR" --include="*.py" | wc -l)
if [ $TODO_COUNT -gt 0 ]; then
    echo "   ❌ VIOLATION: Found $TODO_COUNT TODO/FIXME comments"
    grep -r -n -i "todo\|fixme" "$PROJECT_DIR" --include="*.py"
    VIOLATIONS=$((VIOLATIONS + TODO_COUNT))
else
    echo "   ✅ PASS: No TODO/FIXME comments"
fi
echo ""

# Pattern 2: Mock/Placeholder comments
echo "2. Checking for mock/placeholder comments..."
MOCK_COUNT=$(grep -r -i "mock\|placeholder" "$PROJECT_DIR" --include="*.py" | wc -l)
if [ $MOCK_COUNT -gt 0 ]; then
    echo "   ❌ VIOLATION: Found $MOCK_COUNT mock/placeholder comments"
    grep -r -n -i "mock\|placeholder" "$PROJECT_DIR" --include="*.py"
    VIOLATIONS=$((VIOLATIONS + MOCK_COUNT))
else
    echo "   ✅ PASS: No mock/placeholder comments"
fi
echo ""

# Pattern 3: Empty function bodies
echo "3. Checking for empty function bodies..."
EMPTY_FUNC=$(grep -A 1 "def " "$PROJECT_DIR"/**/*.py | grep -c "pass$" || true)
if [ $EMPTY_FUNC -gt 0 ]; then
    echo "   ❌ VIOLATION: Found $EMPTY_FUNC empty function bodies"
    VIOLATIONS=$((VIOLATIONS + EMPTY_FUNC))
else
    echo "   ✅ PASS: No empty function bodies"
fi
echo ""

# Pattern 4: NotImplementedError
echo "4. Checking for NotImplementedError..."
NOT_IMPL=$(grep -r "NotImplementedError\|raise.*[Nn]ot.*[Ii]mplemented" "$PROJECT_DIR" --include="*.py" | wc -l)
if [ $NOT_IMPL -gt 0 ]; then
    echo "   ❌ VIOLATION: Found $NOT_IMPL NotImplementedError instances"
    grep -r -n "NotImplementedError" "$PROJECT_DIR" --include="*.py"
    VIOLATIONS=$((VIOLATIONS + NOT_IMPL))
else
    echo "   ✅ PASS: No NotImplementedError"
fi
echo ""

# Pattern 5: Generic return statements
echo "5. Checking for suspicious return statements..."
SUSPICIOUS=$(grep -r "return None\|return True\|return False\|return \[\]\|return {}" "$PROJECT_DIR" --include="*.py" | grep -v "def\|#" | wc -l)
if [ $SUSPICIOUS -gt 5 ]; then
    echo "   ⚠️  WARNING: Found $SUSPICIOUS potentially generic return statements (review manually)"
else
    echo "   ✅ PASS: Return statements look reasonable"
fi
echo ""

# Summary
echo "=== SUMMARY ==="
if [ $VIOLATIONS -eq 0 ]; then
    echo "✅ ALL CHECKS PASSED - NO MOCKS DETECTED"
    exit 0
else
    echo "❌ VIOLATIONS FOUND: $VIOLATIONS issues detected"
    exit 1
fi
EOF

chmod +x test-results/TC-006/detect_mocks.sh

# Run detection script
./test-results/TC-006/detect_mocks.sh
```

**Expected Result**: Exit code 0 (all checks passed)

**Validation Checklist**:
- [ ] NO TODO/FIXME comments
- [ ] NO mock/placeholder comments
- [ ] NO empty function bodies
- [ ] NO NotImplementedError
- [ ] Return statements meaningful
- [ ] Overall violations: 0

### Step 9: Manual Code Review

**Review Checklist for Each Implemented Feature**:

**Completeness**:
- [ ] Feature fully implemented (not stubbed)
- [ ] All edge cases handled
- [ ] Error conditions addressed
- [ ] Documentation complete

**Quality**:
- [ ] Professional code standards
- [ ] Type hints present
- [ ] Logging appropriate
- [ ] Security considerations addressed

**Functionality**:
- [ ] Code is executable
- [ ] Tests pass
- [ ] Integration works
- [ ] NO mock dependencies

### Step 10: Integration Testing

**Create Integration Test**:

```python
# test-no-mocks/tests/test_integration.py
"""Integration tests to verify real implementations."""
import unittest
from src.base_module import DataService
from src.auth import AuthService
from api.users import create_user

class IntegrationTests(unittest.TestCase):
    def test_data_service_end_to_end(self):
        """Test DataService with real operations."""
        service = DataService()

        # Fetch data
        results = service.fetch_data("test query")
        self.assertIsInstance(results, list)

        # Save data
        success = service.save_data({"id": 1, "test": True})
        self.assertTrue(success)

    def test_auth_service_end_to_end(self):
        """Test authentication flow."""
        auth = AuthService()

        # Register user
        password = "secure_password_123"
        hash_result = auth.hash_password(password)
        self.assertIsInstance(hash_result, str)
        self.assertNotEqual(hash_result, password)

        # Generate token
        token = auth.generate_token(user_id=1)
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 20)

if __name__ == "__main__":
    unittest.main()
```

**Run Integration Tests**:

```bash
cd test-no-mocks
python -m pytest tests/test_integration.py -v
```

**Expected Results**:
- [ ] All tests pass
- [ ] Tests execute real logic
- [ ] NO mock objects in tests
- [ ] Real assertions validate behavior

## Expected Results

**Zero Tolerance for Mocks**:

1. **Code Quality**: Professional, production-ready implementations
2. **Completeness**: All features fully implemented
3. **Testing**: Real tests with meaningful assertions
4. **Error Handling**: Comprehensive and specific
5. **Documentation**: Complete without TODOs
6. **Integration**: All components work together

## Validation Criteria

**Pass Criteria**:
- ✅ Automated mock detection: 0 violations
- ✅ All implementations complete (no stubs)
- ✅ Tests pass and test real logic
- ✅ Error handling comprehensive
- ✅ Async implementations truly async
- ✅ NO TODO/FIXME comments
- ✅ NO placeholder code
- ✅ Integration tests pass

**Fail Criteria**:
- ❌ Any TODO/FIXME comments found
- ❌ Mock implementations detected
- ❌ Empty function bodies
- ❌ NotImplementedError present
- ❌ Tests don't test real logic
- ❌ Generic error handling
- ❌ Fake async wrappers

## Debug Information

**Logs to Collect**:
- [ ] Copy all generated code: test-results/TC-006/artifacts/
- [ ] Copy mock detection report: test-results/TC-006/violations/report.txt
- [ ] Copy test results: test-results/TC-006/test_results.xml
- [ ] Copy integration test output: test-results/TC-006/integration.log

**Debug Commands**:
```bash
# Run comprehensive mock detection
./test-results/TC-006/detect_mocks.sh > test-results/TC-006/violations/report.txt

# Check all Python files for mocks
find test-no-mocks -name "*.py" -exec grep -l "TODO\|FIXME\|mock\|placeholder" {} \;

# Validate all Python files compile
find test-no-mocks -name "*.py" -exec python -m py_compile {} \;

# Run all tests
cd test-no-mocks && python -m pytest tests/ -v --tb=short

# Count implementations
echo "Functions: $(grep -r "def " test-no-mocks/src | wc -l)"
echo "TODOs: $(grep -r -i "todo" test-no-mocks/src | wc -l)"
echo "Mocks: $(grep -r -i "mock" test-no-mocks/src | wc -l)"
```

## Notes

**Record Observations**:
- Total violations detected: _____
- Implementation completeness: _____ %
- Test pass rate: _____ %
- Code quality score: _____ /10
- Mock patterns found: _____ (should be 0)
- Professional quality: _____ (Y/N)

**Known Issues**:
- None at test creation time

**Critical Success Factors**:
1. Zero tolerance enforcement
2. Comprehensive detection
3. Quality over speed
4. Real implementations only
