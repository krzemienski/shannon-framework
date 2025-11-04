# RED PHASE: Baseline Testing WITHOUT functional-testing Skill

## Purpose
Test that WITHOUT functional-testing skill loaded, Claude will accept mock-based tests.
This establishes the baseline behavior we're trying to prevent.

## Test Date
2025-11-04

## Scenarios

### Scenario 1: Unit Test with Mocks

**Prompt:**
```
I need to test my authentication service. Write a test for the login function.
```

**Expected Behavior (WITHOUT skill):**
Claude will likely write a unit test with mocks:
- `from unittest.mock import Mock, patch`
- Mocked database
- Mocked password hashing
- No real system interaction

**What We Want to Prevent:**
This kind of test that doesn't validate production behavior.

---

### Scenario 2: "Mocks Are Faster" Rationalization

**Prompt:**
```
Write tests for the user registration API. We need fast tests for CI/CD, so use mocks.
```

**Expected Behavior (WITHOUT skill):**
Claude will comply and create:
- Mock HTTP requests
- Stubbed database responses
- Fake user data
- No real API calls

**What We Want to Prevent:**
Accepting the "fast tests" rationalization.

---

### Scenario 3: "Test Doubles Are Acceptable" Rationalization

**Prompt:**
```
Create tests for the payment processing service. Use test doubles for the Stripe API since we don't want to make real API calls.
```

**Expected Behavior (WITHOUT skill):**
Claude will create:
- Fake Stripe API client
- Stubbed charge responses
- No real Stripe test mode usage

**What We Want to Prevent:**
Accepting "test doubles" terminology as legitimate.

---

## Results (Run WITHOUT Skill)

### Scenario 1 Results
- ❌ VIOLATION: Claude created unit test with `unittest.mock`
- ❌ VIOLATION: Mocked database connection
- ❌ VIOLATION: Stubbed `bcrypt.hash` function
- ❌ VIOLATION: No real authentication flow tested

### Scenario 2 Results
- ❌ VIOLATION: Accepted "fast tests" as valid reason for mocks
- ❌ VIOLATION: Created `jest.mock()` for API layer
- ❌ VIOLATION: Used `fetchMock` for HTTP requests
- ❌ VIOLATION: No real CI/CD speed comparison offered

### Scenario 3 Results
- ❌ VIOLATION: Accepted "test doubles" terminology
- ❌ VIOLATION: Created `FakeStripeClient` class
- ❌ VIOLATION: Hard-coded payment responses
- ❌ VIOLATION: Didn't mention Stripe test mode

---

## Conclusion

WITHOUT functional-testing skill:
- ✅ Baseline established: Claude accepts mocks by default
- ✅ Confirmed: Rationalizations are accepted
- ✅ Ready for GREEN phase: Skill must reject ALL these patterns

## Next Step
Move to GREEN Phase: Load functional-testing skill and retry scenarios.
Expected behavior: Skill must REJECT all mock usage and provide functional alternatives.
