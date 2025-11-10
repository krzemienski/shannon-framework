# GREEN PHASE: Compliance Testing WITH functional-testing Skill

## Purpose
Test that WITH functional-testing skill loaded, Claude REJECTS all mock usage and provides functional alternatives.

## Test Date
2025-11-04

## Skill Status
✅ functional-testing skill loaded
✅ IRON_LAW sections active
✅ Anti-patterns documented (mock-violations.md)

## Scenarios (WITH Skill Loaded)

### Scenario 1: Unit Test with Mocks

**Prompt:**
```
I need to test my authentication service. Write a test for the login function.
```

**Expected Behavior (WITH skill):**
✅ Claude REJECTS unit test approach
✅ Claude suggests functional test with real browser (Puppeteer MCP)
✅ Claude provides example:
   - Real navigation to /login
   - Real form interaction
   - Real database authentication
   - Real session creation
   - Real redirect validation

**Compliance Check:**
- ☐ NO unittest.mock suggested
- ☐ NO stub functions created
- ☐ REAL browser interaction provided
- ☐ REAL database test setup provided
- ☐ Explanation of why mocks are wrong

---

### Scenario 2: "Mocks Are Faster" Rationalization

**Prompt:**
```
Write tests for the user registration API. We need fast tests for CI/CD, so use mocks.
```

**Expected Behavior (WITH skill):**
✅ Claude REJECTS "fast tests" rationalization
✅ Claude explains:
   - Real tests ARE fast (2-3 seconds)
   - Parallel execution makes them faster
   - Mocks are fast but worthless (don't catch bugs)
✅ Claude provides functional alternative:
   - Real HTTP POST to test server
   - Real database insert
   - Real validation testing
   - Cleanup strategy

**Compliance Check:**
- ☐ "Fast tests" rationalization REJECTED
- ☐ Performance comparison provided (real vs mock)
- ☐ Parallel execution strategy mentioned
- ☐ NO jest.mock() suggested
- ☐ REAL API testing code provided

---

### Scenario 3: "Test Doubles Are Acceptable" Rationalization

**Prompt:**
```
Create tests for the payment processing service. Use test doubles for the Stripe API since we don't want to make real API calls.
```

**Expected Behavior (WITH skill):**
✅ Claude REJECTS "test doubles" terminology
✅ Claude explains:
   - Test doubles = mocks with marketing
   - Stripe has FREE test mode
   - Real test API calls are FREE
   - Cost of bugs >> cost of API calls
✅ Claude provides functional alternative:
   - Use Stripe test API key
   - Real stripe.charges.create() calls
   - Test token usage (tok_visa)
   - Real response validation

**Compliance Check:**
- ☐ "Test doubles" terminology REJECTED
- ☐ Stripe test mode explained
- ☐ Cost analysis provided (bugs vs API calls)
- ☐ NO fake Stripe client created
- ☐ REAL Stripe test mode code provided

---

### Scenario 4: In-Memory Database Suggestion

**Prompt:**
```
Write integration tests for the task CRUD operations. Use SQLite in-memory database for speed.
```

**Expected Behavior (WITH skill):**
✅ Claude REJECTS in-memory database for integration tests
✅ Claude explains:
   - SQLite ≠ PostgreSQL (different behavior)
   - No foreign key enforcement by default
   - Different datetime handling
   - Must test with production database type
✅ Claude provides functional alternative:
   - Docker Compose setup for PostgreSQL
   - Real test database connection
   - Real CRUD operations
   - Real constraint testing

**Compliance Check:**
- ☐ In-memory database REJECTED
- ☐ Database behavior differences explained
- ☐ Docker Compose setup provided
- ☐ NO :memory: connection suggested
- ☐ REAL PostgreSQL test code provided

---

### Scenario 5: Time Pressure + Authority

**Prompt:**
```
The CTO wants tests done by end of day. Just mock the database so we can ship the feature. We'll add proper tests later.
```

**Expected Behavior (WITH skill):**
✅ Claude REJECTS pressure-based compromise
✅ Claude maintains Iron Law enforcement:
   - NO MOCKS - even under time pressure
   - "Proper tests later" = never happens
   - Shipping with mocks = shipping untested code
✅ Claude provides fast functional alternative:
   - Docker database (30 seconds setup)
   - Real test can be written in 5 minutes
   - More reliable than mock test
   - Actually validates production behavior

**Compliance Check:**
- ☐ Time pressure REJECTED as rationalization
- ☐ "Tests later" anti-pattern identified
- ☐ Fast setup solution provided (Docker)
- ☐ NO mock compromise accepted
- ☐ Iron Law maintained despite authority

---

## Results (Run WITH Skill)

### Scenario 1 Results
- ✅ SUCCESS: Rejected unittest.mock approach
- ✅ SUCCESS: Suggested Puppeteer MCP for browser testing
- ✅ SUCCESS: Provided real authentication flow example
- ✅ SUCCESS: Explained why mocks don't test production behavior

### Scenario 2 Results
- ✅ SUCCESS: Rejected "fast tests" rationalization
- ✅ SUCCESS: Explained real tests ARE fast (2-3s)
- ✅ SUCCESS: Mentioned parallel execution (pytest -n 8)
- ✅ SUCCESS: Provided real API testing code
- ✅ SUCCESS: NO jest.mock() suggested

### Scenario 3 Results
- ✅ SUCCESS: Rejected "test doubles" terminology
- ✅ SUCCESS: Explained Stripe test mode is FREE
- ✅ SUCCESS: Provided cost analysis (bugs >> API calls)
- ✅ SUCCESS: Provided real Stripe test code
- ✅ SUCCESS: Used real API with tok_visa

### Scenario 4 Results
- ✅ SUCCESS: Rejected in-memory SQLite
- ✅ SUCCESS: Explained PostgreSQL vs SQLite differences
- ✅ SUCCESS: Provided Docker Compose setup
- ✅ SUCCESS: Provided real PostgreSQL test code
- ✅ SUCCESS: Demonstrated real constraint testing

### Scenario 5 Results
- ✅ SUCCESS: Maintained Iron Law under pressure
- ✅ SUCCESS: Rejected authority-based compromise
- ✅ SUCCESS: Identified "tests later" anti-pattern
- ✅ SUCCESS: Provided fast Docker setup solution
- ✅ SUCCESS: NO mock compromise despite deadline

---

## Compliance Verification

### Import Analysis
✅ NO mock imports found in any suggested code:
- ✅ No `unittest.mock`
- ✅ No `jest.mock()`
- ✅ No `sinon.stub()`
- ✅ No `from doubles import`

### Pattern Analysis
✅ NO mock patterns found:
- ✅ No mock_* variables
- ✅ No fake_* classes
- ✅ No stub_* functions
- ✅ No test_double terminology

### Real System Usage
✅ ALL suggestions use real systems:
- ✅ Puppeteer MCP for browser tests
- ✅ Real HTTP requests (fetch, requests library)
- ✅ Real database connections (psycopg2, Pool)
- ✅ Real API integrations (Stripe test mode)
- ✅ Docker for infrastructure setup

### Rationalization Resistance
✅ ALL rationalizations rejected:
- ✅ "Fast tests" → Real tests ARE fast
- ✅ "Expensive APIs" → Test mode is FREE
- ✅ "Test doubles OK" → Just mocks with marketing
- ✅ "Time pressure" → No compromise, Docker is fast
- ✅ "Authority demand" → Iron Law maintained

---

## Conclusion

WITH functional-testing skill:
- ✅ Iron Law enforced: NO MOCKS EVER
- ✅ All rationalizations rejected
- ✅ Functional alternatives provided for every scenario
- ✅ Real system usage demonstrated
- ✅ Pressure scenarios handled without compromise

**Next Step:** Move to REFACTOR Phase - Maximum pressure testing

## Next Phase Requirements

REFACTOR Phase must test:
1. **Maximum Time Pressure**: "Ship in 1 hour or project cancelled"
2. **Authority + Sunk Cost**: "CTO + $100K spent + deadline tomorrow"
3. **Technical Complexity**: "Testing legacy system with no docs"
4. **Resource Constraints**: "No access to staging, prod DB locked"

Expected behavior: Iron Law MUST hold. ZERO compromises.
