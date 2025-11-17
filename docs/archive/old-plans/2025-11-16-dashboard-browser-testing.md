# Shannon V4.0 Dashboard Browser Testing Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Verify Shannon V4.0 dashboard actually works from user perspective using Playwright browser automation

**Architecture:** Browser automation testing with Playwright MCP to verify WebSocket connection, real-time updates, and interactive controls

**Tech Stack:** Playwright MCP, Python FastAPI server, React dashboard, Socket.IO, systematic-debugging skill

**Context:** Server and dashboard infrastructure exist and pass component tests, but full browser-based integration never tested. This plan addresses that critical gap.

---

## Current State

**What Works** (component-tested):
- ✅ FastAPI server starts on port 8000
- ✅ Health endpoint returns 200 OK
- ✅ Dashboard builds in 867ms
- ✅ Socket.IO endpoint accessible
- ✅ 221 foundation tests passing

**What's UNTESTED** (critical gap):
- ❌ Dashboard actually loads in browser
- ❌ WebSocket connection establishes
- ❌ Real-time event streaming
- ❌ HALT/RESUME buttons work
- ❌ End-to-end: shannon do --dashboard shows execution

---

## Testing Strategy

**Approach**: Use Playwright MCP to automate browser as real user would
**Philosophy**: Test actual user experience, not just infrastructure
**Debugging**: systematic-debugging skill if bugs found
**Iteration**: Fix bugs, retest, repeat until working

---

## Task 1: Setup Browser Testing Infrastructure

**Files:**
- Create: `tests/browser/test_dashboard_connection.py`

**Step 1: Start server in background**

```bash
cd /Users/nick/Desktop/shannon-cli
poetry run python run_server.py &
SERVER_PID=$!
sleep 3
echo "Server PID: $SERVER_PID"
```

Expected: Server running on port 8000

**Step 2: Verify server health**

```bash
curl http://127.0.0.1:8000/health
```

Expected: `{"status":"healthy","version":"4.0.0",...}`

**Step 3: Start dashboard in background**

```bash
cd dashboard
npm run dev &
DASHBOARD_PID=$!
sleep 5
echo "Dashboard PID: $DASHBOARD_PID"
```

Expected: Dashboard serving on port 5173 or 5175

**Step 4: Verify dashboard accessible**

```bash
curl http://localhost:5173 || curl http://localhost:5175
```

Expected: HTML response

**Step 5: Document process IDs for cleanup**

```bash
echo "export SERVER_PID=$SERVER_PID" > /tmp/shannon-test-pids.sh
echo "export DASHBOARD_PID=$DASHBOARD_PID" >> /tmp/shannon-test-pids.sh
```

**Step 6: Commit setup script**

```bash
git add tests/browser/test_dashboard_connection.py
git commit -m "test: Add browser testing infrastructure setup

Sets up server + dashboard for Playwright testing"
```

---

## Task 2: Test Dashboard Loads in Browser

**Files:**
- Modify: `tests/browser/test_dashboard_connection.py`

**Step 1: Use Playwright to navigate to dashboard**

```python
# Using Playwright MCP
await playwright.navigate("http://localhost:5173")
```

Expected: Page loads without errors

**Step 2: Take screenshot of loaded dashboard**

```python
await playwright.screenshot("dashboard-loaded.png")
```

Expected: Screenshot saved

**Step 3: Verify page title**

```python
title = await playwright.evaluate("() => document.title")
assert "Shannon" in title or "Dashboard" in title
```

Expected: Title contains expected text

**Step 4: Check for JavaScript errors**

```python
console_errors = await playwright.get_console_messages()
errors = [msg for msg in console_errors if msg['type'] == 'error']
```

Expected: No critical JavaScript errors

**Step 5: Verify dashboard panels visible**

```python
panels = await playwright.evaluate("""() => {
  return Array.from(document.querySelectorAll('[class*="panel"]')).length
}""")
```

Expected: At least 3 panels visible

**Step 6: Document results**

Create test report with screenshot evidence

**Step 7: Commit test**

```bash
git add tests/browser/test_dashboard_connection.py dashboard-loaded.png
git commit -m "test: Verify dashboard loads in browser with Playwright

Evidence: Screenshot shows dashboard rendered, no JS errors"
```

---

## Task 3: Test WebSocket Connection Establishes

**Files:**
- Modify: `tests/browser/test_dashboard_connection.py`

**Step 1: Check browser console for WebSocket connection**

```python
# Wait for connection (WebSocket handshake takes time)
await playwright.wait_for("5000")  # 5 seconds

# Check console logs for connection messages
console_logs = await playwright.get_console_messages()
connection_logs = [log for log in console_logs if 'connect' in log['text'].lower()]
```

Expected: Console shows connection message

**Step 2: Evaluate WebSocket state in browser**

```python
ws_connected = await playwright.evaluate("""() => {
  // Check if Socket.IO client is connected
  // Assuming window.socket or similar global
  return window.socketConnected || false
}""")
```

Expected: `True`

**Step 3: Check for connection status indicator in UI**

```python
# Look for connection status element
status_element = await playwright.evaluate("""() => {
  const el = document.querySelector('[data-testid="connection-status"]') ||
             document.querySelector('.connection-status') ||
             document.querySelector('[class*="connected"]')
  return el ? el.textContent : null
}""")
```

Expected: "Connected" or similar status

**Step 4: Verify in server logs**

```bash
# Check server logs for connection
grep "Dashboard connected" /tmp/server-output.log || tail -20 /tmp/server-output.log
```

Expected: Server shows "Dashboard connected: <sid>"

**Step 5: Document connection evidence**

Create comprehensive report with:
- Browser console logs
- UI screenshot
- Server logs
- WebSocket state

**Step 6: Commit test**

```bash
git add tests/browser/test_dashboard_connection.py
git commit -m "test: Verify WebSocket connection established

Evidence: Browser console shows connection, server logs confirm, UI shows connected state"
```

---

## Task 4: Test Real-Time Event Streaming

**Files:**
- Modify: `tests/browser/test_dashboard_connection.py`

**Step 1: Send test event from server**

```python
# In another Python process or via API
import requests
response = requests.post('http://127.0.0.1:8000/api/test-event', json={
    'type': 'skill:started',
    'data': {'skill_name': 'test_skill', 'status': 'running'}
})
```

**Step 2: Verify event appears in dashboard**

```python
# Wait for event to arrive (<50ms expected)
await playwright.wait_for("1000")

# Check if event appeared in UI
event_visible = await playwright.evaluate("""() => {
  const events = document.querySelectorAll('[data-testid="event"]') ||
                 document.querySelectorAll('.event') ||
                 document.querySelectorAll('[class*="skill"]')
  return events.length > 0
}""")
```

Expected: Event visible in dashboard

**Step 3: Measure latency**

```python
import time
send_time = time.time()
# Send event
# Wait for event in UI
receive_time = time.time()
latency = (receive_time - send_time) * 1000
```

Expected: Latency < 50ms

**Step 4: Verify event content correct**

```python
event_text = await playwright.evaluate("""() => {
  const event = document.querySelector('[data-testid="event"]')
  return event ? event.textContent : null
}""")
```

Expected: Contains "test_skill"

**Step 5: Take screenshot showing event**

```python
await playwright.screenshot("dashboard-event-received.png")
```

**Step 6: Document streaming evidence**

**Step 7: Commit test**

```bash
git add tests/browser/test_dashboard_connection.py dashboard-event-received.png
git commit -m "test: Verify real-time event streaming <50ms

Evidence: Event appears in dashboard within latency target"
```

---

## Task 5: Test HALT Button Functionality

**Files:**
- Modify: `tests/browser/test_dashboard_connection.py`

**Step 1: Start shannon do in background**

```bash
cd /tmp/test-dashboard-controls
shannon do "create long_task.py with many functions" --dashboard &
TASK_PID=$!
```

**Step 2: Wait for execution to start**

```python
# Wait for task to appear in dashboard
await playwright.wait_for("3000")
```

**Step 3: Locate HALT button**

```python
halt_button = await playwright.evaluate("""() => {
  const btn = document.querySelector('button:contains("HALT")') ||
              document.querySelector('[data-testid="halt-button"]') ||
              document.querySelector('button[class*="halt"]')
  return btn ? true : false
}""")
```

Expected: HALT button exists

**Step 4: Click HALT button**

```python
await playwright.click('button:has-text("HALT")')
```

**Step 5: Verify execution paused**

Check server logs:
```bash
grep "HALT" /tmp/server-output.log
```

Expected: "Received command: HALT" or "Execution halted"

**Step 6: Verify UI shows halted state**

```python
status = await playwright.evaluate("""() => {
  const status = document.querySelector('[data-testid="execution-status"]')
  return status ? status.textContent : null
}""")
```

Expected: "Halted" or "Paused"

**Step 7: Take screenshot**

```python
await playwright.screenshot("dashboard-halted.png")
```

**Step 8: Commit test**

```bash
git add tests/browser/test_dashboard_connection.py dashboard-halted.png
git commit -m "test: Verify HALT button stops execution

Evidence: Button click triggers halt, UI shows halted state, server receives command"
```

---

## Task 6: Test RESUME Button Functionality

**Files:**
- Modify: `tests/browser/test_dashboard_connection.py`

**Step 1: Click RESUME button (from halted state)**

```python
await playwright.click('button:has-text("RESUME")')
```

**Step 2: Verify execution continues**

Check server logs:
```bash
grep "RESUME" /tmp/server-output.log
```

Expected: "Received command: RESUME" or "Execution resumed"

**Step 3: Verify UI shows running state**

```python
status = await playwright.evaluate("""() => {
  const status = document.querySelector('[data-testid="execution-status"]')
  return status ? status.textContent : null
}""")
```

Expected: "Running" or "Executing"

**Step 4: Wait for task completion**

```python
await playwright.wait_for("text=Execution Complete", timeout=60000)
```

**Step 5: Verify file was created**

```bash
ls /tmp/test-dashboard-controls/long_task.py
```

Expected: File exists (proves execution continued and completed)

**Step 6: Take screenshot of completion**

```python
await playwright.screenshot("dashboard-completed.png")
```

**Step 7: Commit test**

```bash
git add tests/browser/test_dashboard_connection.py dashboard-completed.png
git commit -m "test: Verify RESUME button continues execution

Evidence: Execution resumed, task completed, file created"
```

---

## Task 7: Test Full Stack End-to-End

**Files:**
- Create: `tests/browser/test_full_stack_e2e.py`

**Step 1: Start fresh servers**

```bash
# Kill any existing servers
kill $SERVER_PID $DASHBOARD_PID 2>/dev/null

# Start fresh
cd /Users/nick/Desktop/shannon-cli
poetry run python run_server.py > /tmp/server.log 2>&1 &
SERVER_PID=$!

cd dashboard
npm run dev > /tmp/dashboard.log 2>&1 &
DASHBOARD_PID=$!

sleep 5
```

**Step 2: Open dashboard in Playwright**

```python
await playwright.navigate("http://localhost:5173")
await playwright.wait_for("2000")
```

**Step 3: Start shannon do in terminal**

```bash
cd /tmp/test-full-stack
shannon do "create calculator.py with add and multiply functions" --dashboard --verbose &
```

**Step 4: Watch for task to appear in dashboard**

```python
# Wait for task name to appear
await playwright.wait_for("text=calculator.py", timeout=10000)
```

**Step 5: Verify ExecutionOverview panel updates**

```python
task_name = await playwright.evaluate("""() => {
  const panel = document.querySelector('[data-testid="execution-overview"]')
  return panel ? panel.textContent : null
}""")
```

Expected: Contains "calculator.py"

**Step 6: Verify SkillsView panel shows skills**

```python
skills = await playwright.evaluate("""() => {
  const skillElements = document.querySelectorAll('[data-testid="skill-item"]')
  return Array.from(skillElements).map(el => el.textContent)
}""")
```

Expected: Shows code_generation, library_discovery, etc.

**Step 7: Wait for completion**

```python
await playwright.wait_for("text=Execution Complete", timeout=120000)
```

**Step 8: Verify file created**

```bash
ls /tmp/test-full-stack/calculator.py
python /tmp/test-full-stack/calculator.py
```

Expected: File exists and works

**Step 9: Take screenshots of all panels**

```python
await playwright.screenshot("full-stack-e2e-complete.png")
```

**Step 10: Commit full E2E test**

```bash
git add tests/browser/test_full_stack_e2e.py full-stack-e2e-complete.png
git commit -m "test: Verify full stack end-to-end with browser

Evidence: Dashboard shows real-time execution, all panels update, file created"
```

---

## Task 8: Systematic Debugging If Issues Found

**Files:**
- Create: `tests/browser/DEBUG_FINDINGS.md`

**Step 1: If any test fails, invoke systematic-debugging skill**

```
@skill systematic-debugging

Context: Browser test failed at [specific step]
Symptom: [what went wrong]
Expected: [what should have happened]
Actual: [what actually happened]
```

**Step 2: Investigate root cause**

Follow systematic-debugging protocol:
- Reproduce bug consistently
- Isolate component (frontend vs backend vs WebSocket)
- Check browser console errors
- Check server logs
- Check network tab
- Identify root cause

**Step 3: Fix bug in appropriate component**

If frontend issue:
- Modify dashboard React code
- Fix TypeScript errors
- Fix WebSocket client configuration

If backend issue:
- Modify Python server code
- Fix Socket.IO configuration
- Fix CORS issues

**Step 4: Retest after fix**

Run same Playwright test that failed

**Step 5: Document bug and fix**

```markdown
# Bug: [description]

**Symptom**: [what failed]
**Root Cause**: [why it failed]
**Fix**: [what was changed]
**Verification**: [retest passed]
```

**Step 6: Commit fix**

```bash
git add [fixed files] tests/browser/DEBUG_FINDINGS.md
git commit -m "fix: [bug description]

Root cause: [explanation]
Verification: Browser test now passes"
```

**Step 7: Repeat Steps 1-6 until all tests pass**

---

## Task 9: Test Console Errors and Warnings

**Files:**
- Modify: `tests/browser/test_dashboard_connection.py`

**Step 1: Collect all console messages**

```python
console_messages = await playwright.get_console_messages()
```

**Step 2: Filter errors**

```python
errors = [msg for msg in console_messages if msg['type'] == 'error']
```

**Step 3: Filter warnings**

```python
warnings = [msg for msg in console_messages if msg['type'] == 'warning']
```

**Step 4: Classify severity**

For each error/warning:
- CRITICAL: Breaks functionality
- IMPORTANT: Degraded experience
- MINOR: Cosmetic or ignorable

**Step 5: Fix CRITICAL and IMPORTANT issues**

```bash
# For each issue:
# 1. Investigate cause (browser console, React code, etc.)
# 2. Fix in appropriate file
# 3. Retest
# 4. Commit fix
```

**Step 6: Document remaining MINOR issues**

```markdown
# Known Console Warnings (V4.0.0)

- [Warning message]: [explanation] - [defer to V4.1]
```

**Step 7: Commit clean console verification**

```bash
git add tests/browser/test_dashboard_connection.py
git commit -m "test: Verify no critical console errors

All critical and important issues fixed, minor warnings documented"
```

---

## Task 10: Test Network Tab for WebSocket Traffic

**Files:**
- Modify: `tests/browser/test_dashboard_connection.py`

**Step 1: Monitor network requests**

```python
# Playwright network monitoring
await playwright.evaluate("""() => {
  window.capturedRequests = []

  // Capture fetch/XHR
  const originalFetch = window.fetch
  window.fetch = function(...args) {
    window.capturedRequests.push({type: 'fetch', url: args[0]})
    return originalFetch.apply(this, args)
  }
}""")
```

**Step 2: Trigger execution**

```bash
shannon do "create test.py" --dashboard
```

**Step 3: Check WebSocket frames**

```python
# After execution completes
requests = await playwright.evaluate("() => window.capturedRequests")
ws_requests = [r for r in requests if 'socket.io' in r['url']]
```

Expected: Multiple Socket.IO requests (polling + websocket upgrade)

**Step 4: Verify WebSocket upgrade happened**

```python
ws_upgrade = await playwright.evaluate("""() => {
  // Check if WebSocket connection upgraded from polling
  return window.socket && window.socket.connected
}""")
```

Expected: True

**Step 5: Verify event payloads**

```python
# Check if events have proper structure
event_payloads = await playwright.evaluate("""() => {
  return window.receivedEvents || []
}""")
```

Expected: Events with type, timestamp, data fields

**Step 6: Commit network verification**

```bash
git add tests/browser/test_dashboard_connection.py
git commit -m "test: Verify WebSocket network traffic correct

Evidence: WebSocket upgrade successful, events properly formatted"
```

---

## Task 11: Create Reusable Browser Testing Skill

**Files:**
- Create: `~/.claude/skills/dashboard-browser-testing/SKILL.md`

**Step 1: Write skill documentation**

```markdown
---
name: dashboard-browser-testing
description: Test web dashboards with Playwright browser automation - verify connections, real-time updates, and interactive controls from user perspective
skill-type: PROTOCOL
---

# Dashboard Browser Testing Skill

## When to Use

Use when:
- Dashboard exists but never tested in actual browser
- Claims of "dashboard working" without browser evidence
- Need to verify WebSocket real-time streaming
- Testing interactive controls (buttons, forms, etc.)
- Validating user experience, not just infrastructure

## Prerequisites

- Playwright MCP or Puppeteer MCP available
- Server and frontend running (or can be started)
- WebSocket endpoint accessible

## The Protocol

### Phase 1: Infrastructure Verification
1. Start server (background process)
2. Start frontend (background process)
3. Verify both accessible (curl health checks)
4. Document process IDs for cleanup

### Phase 2: Browser Loading
1. Navigate to frontend URL
2. Take screenshot (visual evidence)
3. Check console for errors
4. Verify page loads completely
5. Check for critical JavaScript errors

### Phase 3: WebSocket Connection
1. Wait for connection handshake
2. Check browser console logs
3. Evaluate WebSocket state in browser context
4. Verify server logs show connection
5. Look for UI connection indicator

### Phase 4: Real-Time Event Streaming
1. Trigger test event from server
2. Verify event appears in UI
3. Measure latency (target: <50ms)
4. Verify event content correct
5. Test multiple event types

### Phase 5: Interactive Controls
1. Locate control buttons (HALT, RESUME, etc.)
2. Click button via Playwright
3. Verify server receives command
4. Verify UI updates to reflect new state
5. Test state transitions (running → halted → running)

### Phase 6: Systematic Debugging
1. If any test fails, use @skill systematic-debugging
2. Investigate root cause (frontend vs backend vs WebSocket)
3. Fix bug in appropriate component
4. Retest until passing
5. Document bug and fix

### Phase 7: Evidence Collection
1. Screenshots of all states (loading, connected, events, halted, etc.)
2. Console logs (browser and server)
3. Network traffic analysis
4. Performance metrics (latency, load time)
5. Test report with all evidence

## Testing Checklist

- [ ] Dashboard loads without errors
- [ ] WebSocket connection establishes
- [ ] Connection visible in browser console
- [ ] Server logs show connection
- [ ] Test events arrive in UI
- [ ] Latency < 50ms
- [ ] Interactive buttons visible
- [ ] Button clicks send commands
- [ ] Server receives commands correctly
- [ ] UI updates reflect state changes
- [ ] No critical console errors
- [ ] All panels render correctly

## Common Issues

**Issue**: WebSocket connection fails
- Check: CORS configuration
- Check: Socket.IO version compatibility
- Check: Port conflicts
- Check: Firewall/network issues

**Issue**: Events don't appear in UI
- Check: Event listener registration
- Check: Event type matching
- Check: State management updates
- Check: React component re-rendering

**Issue**: Buttons don't respond
- Check: Event handlers attached
- Check: Command payload format
- Check: Server command handler
- Check: State updates after command

## Success Criteria

Only claim "dashboard working" when:
- ✅ Actual browser loading verified
- ✅ WebSocket connection proven (not assumed)
- ✅ Real-time events tested with evidence
- ✅ Interactive controls tested (not just "buttons exist")
- ✅ Full end-to-end workflow demonstrated
- ✅ Screenshots and logs as proof

## Output

Test report with:
- Browser screenshots (all states)
- Console logs (browser + server)
- Network analysis
- Performance metrics
- Bug fixes applied (if any)
- Evidence that dashboard ACTUALLY WORKS from user perspective

---

**Use Playwright/Puppeteer MCP** - Don't claim "working" without browser evidence!
```

**Step 2: Commit skill**

```bash
git add ~/.claude/skills/dashboard-browser-testing/SKILL.md
git commit -m "skill: Create dashboard-browser-testing protocol

Systematic browser automation testing for dashboards
Prevents claiming 'working' without browser evidence"
```

---

## Validation Gates

### Gate 1: Browser Loading Works
- [ ] Dashboard loads in Playwright
- [ ] No critical JavaScript errors
- [ ] Screenshot shows rendered UI
- [ ] All panels visible

### Gate 2: WebSocket Connection Works
- [ ] Browser console shows connection
- [ ] Server logs show connection
- [ ] UI shows "connected" indicator
- [ ] Connection state evaluates to true

### Gate 3: Real-Time Streaming Works
- [ ] Test event sent from server
- [ ] Event appears in dashboard
- [ ] Latency < 50ms
- [ ] Event content correct

### Gate 4: Interactive Controls Work
- [ ] HALT button visible and clickable
- [ ] HALT command received by server
- [ ] Execution pauses
- [ ] RESUME button continues execution
- [ ] Task completes after resume
- [ ] File created successfully

### Gate 5: No Critical Bugs
- [ ] All browser tests passing
- [ ] No critical console errors
- [ ] No WebSocket connection failures
- [ ] All interactive features functional
- [ ] Evidence collected (screenshots, logs)

---

## Success Metrics

**Can only claim "Dashboard Functional" when:**
- ✅ Browser tests all passing
- ✅ WebSocket connection verified in real browser
- ✅ Real-time updates demonstrated with evidence
- ✅ Interactive controls tested with Playwright
- ✅ Screenshots prove visual functionality
- ✅ No critical bugs remaining

**Until then, claim**: "Dashboard infrastructure ready, browser testing in progress"

---

## Estimated Effort

- Task 1 (Setup): 15 min
- Task 2 (Loading): 15 min
- Task 3 (WebSocket): 20 min
- Task 4 (Streaming): 20 min
- Task 5 (HALT): 20 min
- Task 6 (RESUME): 15 min
- Task 7 (E2E): 30 min
- Task 8 (Debug): 0-120 min (depends on bugs found)
- Task 9 (Console): 15 min
- Task 10 (Network): 15 min
- Task 11 (Skill): 30 min

**Total**: 3-5 hours (if bugs found, more time needed)

---

## Risk Mitigation

**Risk**: Dashboard won't connect
- **Mitigation**: Systematic debugging, check CORS, Socket.IO config
- **Fallback**: Document as known issue, defer to V4.0.1

**Risk**: Many critical bugs found
- **Mitigation**: Fix iteratively, commit each fix
- **Fallback**: Downgrade release to "beta" if >10 critical bugs

**Risk**: HALT/RESUME doesn't work
- **Mitigation**: Debug WebSocket command handling
- **Fallback**: Document as "planned" feature for V4.1

---

**Plan complete. Ready to execute with Playwright browser automation testing.**

**Next**: Execute this plan to get REAL evidence of dashboard functionality!
