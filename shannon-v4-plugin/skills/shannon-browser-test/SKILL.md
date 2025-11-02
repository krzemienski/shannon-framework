---
name: shannon-browser-test
display_name: "Shannon Browser Testing (NO MOCKS)"
description: "Real browser testing with Puppeteer/Playwright. NO MOCKS - tests actual user flows in real browsers"
category: testing
version: "4.0.0"
priority: 1
auto_activate: true
activation_condition: "domain_analysis.frontend >= 20% OR testing_phase_active"
mcp_servers:
  required: [serena, puppeteer]
  recommended: [playwright]
allowed_tools: [puppeteer_navigate, puppeteer_click, puppeteer_screenshot, puppeteer_type, puppeteer_evaluate, Write, Read]
---

# Shannon Browser Testing (NO MOCKS)

> **Real Browser Testing**: Puppeteer/Playwright for functional E2E tests

## Philosophy: NO MOCKS

Shannon enforces **functional testing only**:

✅ **DO**:
- Real browsers (Puppeteer, Playwright)
- Real user interactions (click, type, navigate)
- Real network requests
- Real DOM rendering
- Real JavaScript execution

❌ **DON'T**:
- Jest mocks
- Enzyme shallow rendering
- Testing Library fake timers
- Mock fetch/axios
- JSDOM (unless production uses it)

**Why**: Mocks test your mocks, not production behavior

## Capabilities

- Full browser automation
- User flow testing
- Screenshot comparison
- Performance metrics
- Network interception (observation, not mocking)
- Cross-browser testing
- Mobile viewport simulation

## Patterns

**Basic Test Structure**:
```typescript
import puppeteer from 'puppeteer';

describe('User Authentication Flow', () => {
  let browser, page;

  beforeAll(async () => {
    browser = await puppeteer.launch();
    page = await browser.newPage();
  });

  afterAll(async () => {
    await browser.close();
  });

  test('should login successfully', async () => {
    // Navigate
    await page.goto('http://localhost:3000/login');

    // Interact
    await page.type('#email', 'user@example.com');
    await page.type('#password', 'password123');
    await page.click('button[type="submit"]');

    // Verify
    await page.waitForNavigation();
    const url = page.url();
    expect(url).toBe('http://localhost:3000/dashboard');

    // Screenshot for evidence
    await page.screenshot({ path: 'login-success.png' });
  });
});
```

**Form Submission**:
```typescript
test('should submit form and display success', async () => {
  await page.goto('http://localhost:3000/contact');

  // Fill form
  await page.type('#name', 'John Doe');
  await page.type('#email', 'john@example.com');
  await page.type('#message', 'Test message');

  // Submit
  await page.click('button[type="submit"]');

  // Wait for success message
  await page.waitForSelector('.success-message');
  const successText = await page.$eval('.success-message', el => el.textContent);
  expect(successText).toContain('Message sent successfully');
});
```

**API Integration**:
```typescript
test('should load data from real API', async () => {
  // Observe network requests (not mock)
  page.on('response', response => {
    if (response.url().includes('/api/users')) {
      console.log('API called:', response.status());
    }
  });

  await page.goto('http://localhost:3000/users');

  // Wait for data to load
  await page.waitForSelector('.user-list .user-item');

  // Verify data rendered
  const userCount = await page.$$eval('.user-item', items => items.length);
  expect(userCount).toBeGreaterThan(0);
});
```

**Screenshot Comparison**:
```typescript
test('should match visual baseline', async () => {
  await page.goto('http://localhost:3000/dashboard');
  await page.waitForSelector('.dashboard-loaded');

  const screenshot = await page.screenshot();

  // Compare with baseline (use pixelmatch or similar)
  expect(screenshot).toMatchImageSnapshot();
});
```

## Best Practices

**Test Real User Flows**:
```
❌ Bad: Test individual functions in isolation
✅ Good: Test complete user journeys end-to-end
```

**Use Real Data**:
```
❌ Bad: Mock API responses with fake data
✅ Good: Use real test database with seed data
```

**Verify Actual Output**:
```
❌ Bad: Verify function was called with params
✅ Good: Verify UI displays correct result
```

**Test Production Behavior**:
```
❌ Bad: Test with mocked environment
✅ Good: Test against real backend (test environment)
```

## Integration

**Puppeteer MCP**:
```bash
# Navigate
puppeteer_navigate "http://localhost:3000"

# Click element
puppeteer_click "button.submit"

# Take screenshot
puppeteer_screenshot "test-evidence.png"

# Evaluate JS
puppeteer_evaluate "document.title"
```

**Test Workflow**:
```
1. Start test database (Docker)
2. Seed with test data
3. Start application server
4. Run Puppeteer tests against real app
5. Verify functional behavior
6. Collect screenshots as evidence
7. Teardown
```

## Performance Testing

**Metrics Collection**:
```typescript
test('should load dashboard in under 2 seconds', async () => {
  const startTime = Date.now();

  await page.goto('http://localhost:3000/dashboard');
  await page.waitForSelector('.dashboard-loaded');

  const loadTime = Date.now() - startTime;
  expect(loadTime).toBeLessThan(2000);

  // Collect performance metrics
  const metrics = await page.metrics();
  console.log('Performance:', metrics);
});
```

## Evidence-Based Validation

Every test MUST produce evidence:
- Screenshots of success states
- Network request logs
- Console output logs
- Performance metrics
- Error screenshots on failure

## Learn More

📚 **Full Patterns**: [resources/TESTING_PATTERNS.md](./resources/TESTING_PATTERNS.md)
🎯 **Real-World Examples**: [resources/EXAMPLES.md](./resources/EXAMPLES.md)

---

**Shannon V4** - Functional Testing, Zero Mocks 🚀
