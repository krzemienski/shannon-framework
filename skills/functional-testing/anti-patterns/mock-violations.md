# NO MOCKS Violations - Comprehensive Anti-Pattern Catalog

## Purpose

This document catalogs **every way developers try to rationalize mock usage**.
Shannon's functional-testing skill MUST reject all of these patterns.

**Iron Law:** NO MOCKS EVER. No exceptions. No compromises.

---

## Violation Category 1: Direct Mock Usage

### Violation 1.1: unittest.mock

❌ **WRONG:**
```python
from unittest.mock import Mock, MagicMock, patch

@patch('myapp.database.connect')
def test_get_user(mock_connect):
    mock_connect.return_value = MockDB()
    user = get_user(1)
    assert user.id == 1
```

**Why This Is Wrong:**
- Tests the mock, not the real database
- Real database schema changes won't be caught
- Real connection errors won't be caught
- Real query performance won't be tested

✅ **RIGHT:**
```python
import psycopg2

def test_get_user():
    # Connect to REAL test database
    conn = psycopg2.connect(
        dbname="myapp_test",
        user="test_user",
        password="test_password"
    )

    # Insert REAL test data
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (id, name) VALUES (%s, %s)",
        (1, "Test User")
    )
    conn.commit()

    # Test REAL function with REAL database
    user = get_user(1)
    assert user.id == 1
    assert user.name == "Test User"

    # Cleanup REAL data
    cursor.execute("DELETE FROM users WHERE id = %s", (1,))
    conn.commit()
    conn.close()
```

---

### Violation 1.2: jest.mock()

❌ **WRONG:**
```javascript
jest.mock('./api', () => ({
  fetchUser: jest.fn().mockResolvedValue({
    id: 1,
    name: 'Test User'
  })
}));

test('displays user', async () => {
  const user = await fetchUser(1);
  expect(user.name).toBe('Test User');
});
```

✅ **RIGHT:**
```javascript
const fetch = require('node-fetch');

test('displays user', async () => {
  // Make REAL HTTP request to test API
  const response = await fetch('http://localhost:3000/api/users/1');
  const user = await response.json();

  expect(user).toHaveProperty('id');
  expect(user).toHaveProperty('name');
  expect(response.status).toBe(200);
});
```

---

### Violation 1.3: sinon.stub()

❌ **WRONG:**
```javascript
const sinon = require('sinon');

test('payment processing', () => {
  const stub = sinon.stub(stripe, 'charges').returns({
    create: sinon.stub().resolves({ status: 'succeeded' })
  });

  const result = processPayment(100);
  expect(result.status).toBe('succeeded');
});
```

✅ **RIGHT:**
```javascript
const stripe = require('stripe')(process.env.STRIPE_TEST_KEY);

test('payment processing', async () => {
  // Use REAL Stripe API in test mode
  const charge = await stripe.charges.create({
    amount: 100,
    currency: 'usd',
    source: 'tok_visa' // Stripe test token
  });

  expect(charge.status).toBe('succeeded');
  expect(charge.id).toMatch(/^ch_/);
});
```

---

## Violation Category 2: Fake Implementations

### Violation 2.1: Fake Classes

❌ **WRONG:**
```python
class FakeDatabase:
    def __init__(self):
        self.data = {}

    def insert(self, key, value):
        self.data[key] = value

    def query(self, key):
        return self.data.get(key)

def test_user_storage():
    db = FakeDatabase()
    db.insert('user:1', {'name': 'Test'})
    user = db.query('user:1')
    assert user['name'] == 'Test'
```

✅ **RIGHT:**
```python
import redis

def test_user_storage():
    # Connect to REAL Redis test instance
    r = redis.Redis(host='localhost', port=6379, db=15)

    # Use REAL Redis operations
    r.hset('user:1', mapping={'name': 'Test'})
    user = r.hgetall('user:1')

    assert user[b'name'] == b'Test'

    # Cleanup REAL data
    r.delete('user:1')
```

---

### Violation 2.2: Stub Functions

❌ **WRONG:**
```javascript
const stubAuth = () => ({ token: 'fake-token', userId: 1 });

test('authenticated request', () => {
  const auth = stubAuth();
  const result = makeRequest('/api/data', auth);
  expect(result).toBeDefined();
});
```

✅ **RIGHT:**
```javascript
test('authenticated request', async () => {
  // Create REAL user and get REAL token
  const registerResponse = await fetch('http://localhost:3000/api/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email: 'test@example.com',
      password: 'SecurePass123!'
    })
  });

  const { token } = await registerResponse.json();

  // Make REAL authenticated request
  const dataResponse = await fetch('http://localhost:3000/api/data', {
    headers: { 'Authorization': `Bearer ${token}` }
  });

  expect(dataResponse.status).toBe(200);
  const data = await dataResponse.json();
  expect(data).toBeDefined();
});
```

---

### Violation 2.3: In-Memory Databases

❌ **WRONG:**
```python
from sqlalchemy import create_engine

def test_user_crud():
    # In-memory SQLite
    engine = create_engine('sqlite:///:memory:')
    # ... rest of test
```

**Why This Is Wrong:**
- SQLite behavior differs from PostgreSQL/MySQL
- No foreign key enforcement by default
- Different datetime handling
- Different string comparison
- Missing production constraints

✅ **RIGHT:**
```python
from sqlalchemy import create_engine

def test_user_crud():
    # REAL PostgreSQL test database
    engine = create_engine(
        'postgresql://test_user:test_password@localhost/myapp_test'
    )
    # ... rest of test with real database
```

---

## Violation Category 3: Rationalizations

### Violation 3.1: "But Mocks Are Faster!"

**The Rationalization:**
> "Mocks make tests run in milliseconds. Real systems take seconds. We need fast CI/CD."

**Why This Is Wrong:**
- Fast tests that don't catch bugs are worthless
- Real functional tests with proper setup run in 1-3 seconds
- Parallel execution makes real tests fast enough
- Cost of shipped bugs >> cost of 30 extra seconds in CI

**Shannon Response:**
```
❌ REJECTED: "Fast tests" rationalization

Real functional tests ARE fast:
- Database setup: ~100ms (Docker snapshot)
- API startup: ~200ms (test server)
- Browser launch: ~500ms (Puppeteer)
- Test execution: ~1-2s per scenario

Total: 2-3 seconds for comprehensive functional test

Mock test time: 50ms
Mock test value: ⚠️ ZERO (doesn't test production behavior)

Real test time: 2s
Real test value: ✅ FULL (validates actual system)

Use parallel execution if speed is critical:
- pytest -n 8 (run 8 tests in parallel)
- jest --maxWorkers=8
- Reduces suite time by 70-80%
```

---

### Violation 3.2: "But External APIs Are Expensive!"

**The Rationalization:**
> "We can't make real API calls to Stripe/Twilio/SendGrid in every test. It's too expensive."

**Why This Is Wrong:**
- Most services have free test modes
- Cost of bugs >> cost of API calls
- You're not testing production if you're not testing real integrations

**Shannon Response:**
```
❌ REJECTED: "Expensive API" rationalization

Real API solutions:
1. **Use Test Mode**: Stripe, Twilio, SendGrid all have free test APIs
2. **Use Staging Endpoints**: Most SaaS provides test environments
3. **Use Request Limits**: Only test critical paths (5-10 requests)
4. **Cache Responses**: First run uses real API, subsequent runs use recorded

Example (Stripe):
- Test mode is FREE
- Unlimited test charges
- Realistic responses
- Same API as production

Cost analysis:
- Stripe test mode: $0.00
- Production bug from mock: $50,000+ (downtime, lost sales, reputation)

Use REAL APIs in test mode.
```

---

### Violation 3.3: "But I Can't Control The Database!"

**The Rationalization:**
> "I don't have database access / It's shared / Schema changes break my local setup."

**Why This Is Wrong:**
- If you can't test against the database, you can't ship database code
- Docker solves this in 5 minutes
- Shared databases are an anti-pattern

**Shannon Response:**
```
❌ REJECTED: "Can't control database" rationalization

Solutions:
1. **Docker Compose**: Full database in 30 seconds
   ```yaml
   version: '3.8'
   services:
     test-db:
       image: postgres:15
       environment:
         POSTGRES_DB: myapp_test
         POSTGRES_USER: test_user
         POSTGRES_PASSWORD: test_password
       ports:
         - "5433:5432"
   ```

2. **Test Database Per Developer**: Never share test databases
   - dev1: myapp_test_dev1
   - dev2: myapp_test_dev2
   - CI: myapp_test_ci

3. **Migrations First**: Run migrations in test setup
   ```python
   def setup_test_db():
       subprocess.run(['alembic', 'upgrade', 'head'])
   ```

You MUST have database control to write database code.
```

---

### Violation 3.4: "But Mocks Let Me Test Edge Cases!"

**The Rationalization:**
> "How can I test what happens when the API returns a 503? I can't force that in production."

**Why This Is Wrong:**
- You CAN trigger real errors
- Seed data creates edge cases
- Chaos engineering exists

**Shannon Response:**
```
❌ REJECTED: "Edge cases require mocks" rationalization

Real edge case testing:
1. **Seed Edge Case Data**: Insert real problematic data
   ```sql
   INSERT INTO users (email) VALUES
     ('invalid@@email.com'),  -- Double @
     (''),                     -- Empty string
     (NULL);                   -- NULL value
   ```

2. **Trigger Real Errors**: Use test endpoints
   ```javascript
   // Test 503 error
   await fetch('http://localhost:3000/test/trigger-503');

   // Then test recovery
   const response = await fetch('http://localhost:3000/api/data');
   expect(response.status).toBe(200);
   ```

3. **Network Simulation**: Use real network tools
   ```bash
   # Simulate slow network
   tc qdisc add dev eth0 root netem delay 1000ms

   # Run real tests under real slow conditions
   npm test
   ```

4. **Chaos Engineering**: Use tools like Chaos Monkey
   - Kill real services randomly
   - Test real recovery mechanisms

Edge cases are real. Test them with real systems.
```

---

### Violation 3.5: "But Unit Tests Are Best Practice!"

**The Rationalization:**
> "Every testing guide says to write unit tests. We need test pyramid. Mocks enable unit testing."

**Why This Is Wrong:**
- Unit tests test units
- You ship integrated systems
- Test pyramid is outdated (made for slow integration tests)

**Shannon Response:**
```
❌ REJECTED: "Unit tests are best practice" rationalization

Modern testing reality:
1. **You Ship Integration**: Your app is frontend + backend + database + APIs
   - Testing units in isolation proves nothing about production
   - Integration is where bugs live

2. **Test Pyramid Is Outdated**: Created when integration tests were slow (minutes)
   - Modern tools: Fast functional tests (2-3 seconds)
   - Puppeteer MCP, Docker, modern databases = fast integration

3. **Functional Tests ARE Best Practice**:
   - Google: 70% integration, 20% functional, 10% unit
   - Spotify: Functional-first testing
   - Netflix: Production testing (even more integrated)

4. **What To Test**:
   ❌ Internal functions (implementation details)
   ✅ User workflows (actual behavior)
   ✅ API contracts (real requests)
   ✅ Database operations (real queries)

The "best practice" is to test what users see and use.
That requires REAL systems, not mocks.
```

---

## Violation Category 4: Deceptive Names

### Violation 4.1: "Test Doubles"

**The Attempt:**
> "We're not using mocks, we're using test doubles. That's different."

**Shannon Response:**
```
❌ REJECTED: Test doubles = mocks with marketing

Test double is just fancy terminology for fake implementation.
- Stub = mock with hard-coded returns
- Fake = mock with simple implementation
- Spy = mock that records calls
- Dummy = mock that does nothing

All violate NO MOCKS. All forbidden.

Use REAL implementations ALWAYS.
```

---

### Violation 4.2: "Integration Tests" (with mocks)

**The Attempt:**
> "This IS an integration test! It tests how my function integrates with the mock."

**Shannon Response:**
```
❌ REJECTED: Integration requires REAL components

Your function + mock = NOT integration
Your function + real database = integration
Your function + real API = integration

Integration means REAL systems working together.
Mocks are isolated. Isolation ≠ Integration.
```

---

### Violation 4.3: "Functional Tests" (with stubs)

**The Attempt:**
> "These are functional tests - they test the function with stubbed dependencies."

**Shannon Response:**
```
❌ REJECTED: Functional = user-facing behavior with REAL systems

Functional testing definition:
- Tests complete USER WORKFLOWS
- Uses REAL browsers (Puppeteer)
- Uses REAL APIs (HTTP requests)
- Uses REAL databases (PostgreSQL/MySQL)

Your stubbed test:
- Tests FUNCTION in isolation
- Uses FAKE dependencies
- Proves NOTHING about production

Call it what it is: A unit test with mocks.
And those are forbidden.
```

---

## Violation Category 5: Conditional Test Logic

### Violation 5.1: Test Mode Checks

❌ **WRONG:**
```python
def create_user(email):
    if os.getenv('TESTING'):
        return User(id=1, email=email)  # Fake user

    # Real implementation
    return db.insert_user(email)
```

**Why This Is Wrong:**
- Production code should NEVER know about tests
- Test mode = different behavior = not testing production
- Conditional logic creates untested code paths

✅ **RIGHT:**
```python
def create_user(email):
    # SAME code in test and production
    return db.insert_user(email)

# In test:
def test_create_user():
    # Use REAL database (test instance)
    conn = connect_test_db()
    user = create_user('test@example.com')
    assert user.email == 'test@example.com'
```

---

### Violation 5.2: Mock Injection

❌ **WRONG:**
```python
class UserService:
    def __init__(self, db=None):
        self.db = db or RealDatabase()  # Allow mock injection

# In test:
mock_db = MockDatabase()
service = UserService(db=mock_db)
```

✅ **RIGHT:**
```python
class UserService:
    def __init__(self, db):
        self.db = db  # Always requires real DB

# In test:
test_db = RealDatabase(config='test_config')
service = UserService(db=test_db)
```

---

## Violation Category 6: Time/Randomness Mocking

### Violation 6.1: Fake Timers

❌ **WRONG:**
```javascript
jest.useFakeTimers();
jest.setSystemTime(new Date('2024-01-01'));

test('creates timestamp', () => {
  const task = createTask('Test');
  expect(task.createdAt).toEqual(new Date('2024-01-01'));
});
```

✅ **RIGHT:**
```javascript
// Parameterize time
function createTask(title, createdAt = new Date()) {
  return { title, createdAt };
}

test('creates timestamp', () => {
  const testDate = new Date('2024-01-01');
  const task = createTask('Test', testDate);
  expect(task.createdAt).toEqual(testDate);
});
```

---

### Violation 6.2: Seeded Random

❌ **WRONG:**
```python
import random
random.seed(42)  # Make random deterministic

def test_random_selection():
    result = select_random_item([1, 2, 3])
    assert result == 2  # Will always be 2 with seed 42
```

✅ **RIGHT:**
```python
def test_random_selection():
    items = [1, 2, 3]
    result = select_random_item(items)

    # Assert on REAL random behavior
    assert result in items

    # Test distribution over multiple runs
    results = [select_random_item(items) for _ in range(100)]
    assert all(r in items for r in results)
    assert len(set(results)) > 1  # Not always same value
```

---

## Detection Patterns

Shannon's functional-testing skill automatically detects these patterns:

### Red Flag Imports
```python
from unittest.mock import Mock, MagicMock, patch
import mock
from jest import mock as jest_mock
import sinon
from doubles import *
```

### Red Flag Variable Names
```python
mock_db
fake_api
stub_function
test_double
mock_*
fake_*
stub_*
```

### Red Flag Function Patterns
```python
@patch('...')
jest.mock('...')
sinon.stub(...)
createStub(...)
```

### Red Flag Classes
```python
class FakeDatabase
class MockAPI
class StubService
class TestDouble
```

### Red Flag Conditional Logic
```python
if os.getenv('TESTING'):
if config.TEST_MODE:
if __debug__:
```

---

## Enforcement Checklist

Before accepting ANY test, verify:

☐ NO mock imports (`unittest.mock`, `jest.mock`, `sinon`, etc.)
☐ NO stub functions created
☐ NO fake classes defined
☐ NO test doubles terminology
☐ NO in-memory databases (for integration tests)
☐ NO hard-coded responses
☐ NO conditional test logic
☐ NO time mocking
☐ REAL browser launched (for UI tests)
☐ REAL HTTP requests made (for API tests)
☐ REAL database queries (for persistence tests)
☐ REAL cleanup of real resources

---

## Summary

**The Shannon NO MOCKS Iron Law:**

Every mock, stub, fake, or test double is a potential production bug.

Test with REAL systems:
- ✅ Real browsers (Puppeteer MCP)
- ✅ Real databases (PostgreSQL, MySQL, D1)
- ✅ Real APIs (test mode, staging)
- ✅ Real workflows (user journeys)

ZERO exceptions. ZERO compromises. ZERO mocks.

---

## See Also

- `../SKILL.md` - Main functional-testing skill
- `../references/TESTING_PHILOSOPHY.md` - Complete NO MOCKS philosophy
- `../examples/puppeteer-browser-test.md` - Real browser test example
- `/shannon-plugin/core/TESTING_PHILOSOPHY.md` - Core Shannon testing principles
