# Puppeteer Browser Test Examples

Complete examples of functional browser testing with Puppeteer MCP.

## Setup

```javascript
// test-setup.js
const puppeteer = require('puppeteer');

let browser;
let page;

beforeAll(async () => {
  // Launch REAL browser
  browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox']
  });
});

beforeEach(async () => {
  // New REAL page for each test
  page = await browser.newPage();
});

afterEach(async () => {
  // Close REAL page
  await page.close();
});

afterAll(async () => {
  // Close REAL browser
  await browser.close();
});
```

## Example 1: Complete Authentication Flow

```javascript
// ✅ CORRECT: Test real authentication with real database
describe('Authentication Flow', () => {
  test('User can register, login, and logout', async () => {
    // 1. REGISTRATION
    await page.goto('http://localhost:3000/register');
    await page.waitForSelector('[data-testid="register-form"]');

    const testEmail = `test-${Date.now()}@example.com`;
    await page.type('[data-testid="email"]', testEmail);
    await page.type('[data-testid="password"]', 'SecurePass123!');
    await page.type('[data-testid="password-confirm"]', 'SecurePass123!');
    await page.click('[data-testid="register-submit"]');

    // Wait for REAL database insert + redirect
    await page.waitForNavigation({ waitUntil: 'networkidle0' });
    expect(page.url()).toContain('/login');

    // 2. LOGIN
    await page.type('[data-testid="email"]', testEmail);
    await page.type('[data-testid="password"]', 'SecurePass123!');
    await page.click('[data-testid="login-submit"]');

    // Wait for REAL JWT creation + redirect
    await page.waitForNavigation({ waitUntil: 'networkidle0' });
    expect(page.url()).toContain('/dashboard');

    // Verify REAL session state
    const welcomeText = await page.$eval(
      '[data-testid="welcome"]',
      el => el.textContent
    );
    expect(welcomeText).toContain(testEmail);

    // 3. LOGOUT
    await page.click('[data-testid="user-menu"]');
    await page.click('[data-testid="logout"]');

    // Wait for REAL session destruction
    await page.waitForNavigation({ waitUntil: 'networkidle0' });
    expect(page.url()).toContain('/login');

    // Verify can't access protected route
    await page.goto('http://localhost:3000/dashboard');
    await page.waitForNavigation({ waitUntil: 'networkidle0' });
    expect(page.url()).toContain('/login');
  });
});
```

## Example 2: Form Validation with Real Backend

```javascript
// ✅ CORRECT: Test real validation errors from real API
describe('Form Validation', () => {
  test('Shows server-side validation errors', async () => {
    await page.goto('http://localhost:3000/tasks/new');

    // Try to submit empty form
    await page.click('[data-testid="save-task"]');

    // Wait for REAL API validation response
    await page.waitForSelector('[data-testid="error-title"]');

    const titleError = await page.$eval(
      '[data-testid="error-title"]',
      el => el.textContent
    );
    expect(titleError).toBe('Title is required');

    // Fill form with invalid data
    await page.type('[data-testid="task-title"]', 'ab'); // Too short
    await page.click('[data-testid="save-task"]');

    // Wait for REAL API validation
    await page.waitForSelector('[data-testid="error-title"]');

    const lengthError = await page.$eval(
      '[data-testid="error-title"]',
      el => el.textContent
    );
    expect(lengthError).toBe('Title must be at least 3 characters');
  });
});
```

## Example 3: Real-Time Updates with WebSocket

```javascript
// ✅ CORRECT: Test real WebSocket communication
describe('Real-Time Updates', () => {
  test('Tasks sync across browser tabs', async () => {
    // Create TWO real browser contexts
    const context1 = await browser.newContext();
    const context2 = await browser.newContext();
    const page1 = await context1.newPage();
    const page2 = await context2.newPage();

    // Both pages connect to REAL WebSocket server
    await page1.goto('http://localhost:3000/dashboard');
    await page2.goto('http://localhost:3000/dashboard');

    // Wait for REAL WebSocket connections
    await page1.waitForSelector('[data-testid="ws-connected"]');
    await page2.waitForSelector('[data-testid="ws-connected"]');

    // Page 1: Create task (REAL database insert + WebSocket broadcast)
    await page1.click('[data-testid="new-task"]');
    await page1.type('[data-testid="task-title"]', 'Shared Task');
    await page1.click('[data-testid="save-task"]');

    // Wait for REAL WebSocket message delivery to Page 2
    await page2.waitForSelector('[data-task-title="Shared Task"]', {
      timeout: 5000
    });

    // Verify REAL real-time sync
    const taskVisible = await page2.$('[data-task-title="Shared Task"]');
    expect(taskVisible).not.toBeNull();

    // Cleanup
    await context1.close();
    await context2.close();
  });
});
```

## Example 4: File Upload with Real Server

```javascript
// ✅ CORRECT: Test real file upload
describe('File Upload', () => {
  test('Uploads and displays file', async () => {
    await page.goto('http://localhost:3000/tasks/new');

    // Create REAL test file
    const fs = require('fs');
    const testFilePath = '/tmp/test-attachment.txt';
    fs.writeFileSync(testFilePath, 'Test attachment content');

    // Upload REAL file
    const fileInput = await page.$('[data-testid="file-input"]');
    await fileInput.uploadFile(testFilePath);

    // Fill task details
    await page.type('[data-testid="task-title"]', 'Task with attachment');
    await page.click('[data-testid="save-task"]');

    // Wait for REAL file upload + database insert
    await page.waitForNavigation({ waitUntil: 'networkidle0' });

    // Verify REAL file was uploaded
    const attachment = await page.$('[data-testid="attachment"]');
    expect(attachment).not.toBeNull();

    const filename = await page.$eval(
      '[data-testid="attachment-name"]',
      el => el.textContent
    );
    expect(filename).toBe('test-attachment.txt');

    // Download and verify REAL file
    const [download] = await Promise.all([
      page.waitForEvent('download'),
      page.click('[data-testid="download-attachment"]')
    ]);
    const downloadPath = await download.path();
    const content = fs.readFileSync(downloadPath, 'utf-8');
    expect(content).toBe('Test attachment content');

    // Cleanup
    fs.unlinkSync(testFilePath);
  });
});
```

## Example 5: Infinite Scroll with Real Data

```javascript
// ✅ CORRECT: Test real infinite scroll with real database
describe('Infinite Scroll', () => {
  beforeEach(async () => {
    // Seed REAL database with test data
    const response = await fetch('http://localhost:3000/api/test/seed', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ taskCount: 50 })
    });
    expect(response.ok).toBe(true);
  });

  test('Loads more tasks on scroll', async () => {
    await page.goto('http://localhost:3000/tasks');

    // Wait for initial REAL data load
    await page.waitForSelector('[data-testid="task-list"]');

    // Count initial tasks
    const initialTasks = await page.$$('[data-testid^="task-"]');
    expect(initialTasks.length).toBe(20); // First page

    // Scroll to bottom (triggers REAL API call)
    await page.evaluate(() => {
      window.scrollTo(0, document.body.scrollHeight);
    });

    // Wait for REAL API response + DOM update
    await page.waitForFunction(
      () => document.querySelectorAll('[data-testid^="task-"]').length > 20,
      { timeout: 5000 }
    );

    // Verify REAL data loaded
    const updatedTasks = await page.$$('[data-testid^="task-"]');
    expect(updatedTasks.length).toBe(40); // Second page loaded
  });

  afterEach(async () => {
    // Cleanup REAL test data
    await fetch('http://localhost:3000/api/test/cleanup', {
      method: 'DELETE'
    });
  });
});
```

## Example 6: Drag and Drop with Real State Updates

```javascript
// ✅ CORRECT: Test real drag-and-drop with real database updates
describe('Drag and Drop', () => {
  test('Reorders tasks via drag and drop', async () => {
    await page.goto('http://localhost:3000/tasks');

    // Wait for REAL data load
    await page.waitForSelector('[data-testid="task-1"]');
    await page.waitForSelector('[data-testid="task-2"]');

    // Get initial order from REAL database
    const initialOrder = await page.$$eval(
      '[data-testid^="task-"]',
      tasks => tasks.map(t => t.dataset.testid)
    );
    expect(initialOrder).toEqual(['task-1', 'task-2', 'task-3']);

    // Perform REAL drag and drop
    const task1 = await page.$('[data-testid="task-1"]');
    const task3 = await page.$('[data-testid="task-3"]');

    const task1Box = await task1.boundingBox();
    const task3Box = await task3.boundingBox();

    await page.mouse.move(task1Box.x + task1Box.width / 2, task1Box.y + task1Box.height / 2);
    await page.mouse.down();
    await page.mouse.move(task3Box.x + task3Box.width / 2, task3Box.y + task3Box.height / 2);
    await page.mouse.up();

    // Wait for REAL database update + UI update
    await page.waitForTimeout(500);

    // Verify REAL order change
    const newOrder = await page.$$eval(
      '[data-testid^="task-"]',
      tasks => tasks.map(t => t.dataset.testid)
    );
    expect(newOrder).toEqual(['task-2', 'task-3', 'task-1']);

    // Verify persistence (reload page)
    await page.reload();
    await page.waitForSelector('[data-testid="task-2"]');

    const persistedOrder = await page.$$eval(
      '[data-testid^="task-"]',
      tasks => tasks.map(t => t.dataset.testid)
    );
    expect(persistedOrder).toEqual(['task-2', 'task-3', 'task-1']);
  });
});
```

## Common Patterns

### Wait for Network Requests

```javascript
// Wait for specific REAL API call
await page.waitForResponse(
  response => response.url().includes('/api/tasks') && response.status() === 200
);
```

### Intercept Requests (for debugging, not mocking)

```javascript
// Monitor REAL requests (don't mock them!)
page.on('request', request => {
  console.log('Request:', request.url());
});

page.on('response', response => {
  console.log('Response:', response.url(), response.status());
});
```

### Screenshot on Failure

```javascript
afterEach(async () => {
  if (global.testFailed) {
    await page.screenshot({
      path: `./screenshots/failure-${Date.now()}.png`
    });
  }
});
```

### Test with Different Viewports

```javascript
test('Works on mobile viewport', async () => {
  await page.setViewport({
    width: 375,
    height: 667,
    isMobile: true
  });

  await page.goto('http://localhost:3000');

  // Test REAL mobile behavior
  const menuButton = await page.$('[data-testid="mobile-menu"]');
  expect(menuButton).not.toBeNull();
});
```
