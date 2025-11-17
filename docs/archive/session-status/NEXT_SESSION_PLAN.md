# Next Session: Testing & Proving (6 Hours)

**Goal**: PROVE what works, FIX what doesn't
**Current**: 20% proven, 80% unverified
**Target**: 90% proven functional

---

## Current Honest Status

**PROVEN WORKING** (Ran tests myself):
- ✅ Wave 1: Skills Framework (integration test passed)
- ✅ Wave 2: Discovery & Dependencies (integration test passed)

**UNVERIFIED** (Code exists, not tested):
- ⚠️ Wave 3: Communication
- ⚠️ Wave 4: Dashboard
- ⚠️ Wave 5: shannon do
- ⚠️ Waves 6-10: Advanced features

---

## 6-Hour Testing Plan

### HOUR 1-2: Run All Existing Tests

**Task**: Execute every test file and document REAL results

```bash
# Run all skills tests
poetry run pytest tests/skills/ -v

# Expected files:
- tests/skills/test_registry.py
- tests/skills/test_loader.py
- tests/skills/test_executor.py
- tests/skills/test_hooks.py
- tests/skills/test_dependencies.py
- tests/skills/test_discovery.py
- tests/skills/test_catalog.py

# Run server tests
poetry run pytest tests/server/ -v

# Run all integration tests
python3 tests/wave1_integration_test.py
python3 tests/wave2_integration_test.py
python3 tests/wave3_integration_test.py (if exists)
```

**Document**:
- Actual pass/fail counts
- Which tests actually run
- Which tests are broken
- Real test coverage

**Exit**: Know exactly what's tested and working

---

### HOUR 3: Fix shannon do to Actually Work

**Current Issue**: Flow completes but no files created

**Test**:
```bash
cd /tmp/test_project
shannon do "create calculator.py with add function"

# Verify:
ls calculator.py  # Does file exist?
cat calculator.py  # Does it have add function?
git log  # Was commit created?
```

**Fix If Needed**:
- Ensure skills actually execute (not just return)
- Ensure file operations happen
- Ensure git commits work
- Test until file is actually created

**Exit**: shannon do creates real files

---

### HOUR 4: Test Server WebSocket

**Test**:
```bash
# Terminal 1
poetry run python run_server.py

# Terminal 2 - Test with curl or simple client
curl http://localhost:8000/health

# Create simple WebSocket test client
python3 -c "
import socketio
sio = socketio.Client()
sio.connect('http://localhost:8000')
print('Connected:', sio.connected)
sio.disconnect()
"
```

**Verify**:
- Server starts without errors
- Health endpoint responds
- WebSocket accepts connections
- Events can be received
- Commands can be sent

**Exit**: WebSocket proven working

---

### HOUR 5: Test Dashboard Integration

**Test**:
```bash
# Terminal 1: Server
poetry run python run_server.py

# Terminal 2: Dashboard
cd dashboard
npm run dev

# Browser: http://localhost:5173
# Check browser console for WebSocket connection
# Verify: "Connected to Shannon server" message
```

**Verify**:
- Dashboard loads in browser
- WebSocket connection established
- No console errors
- Can see connection status

**Exit**: Dashboard connects to server

---

### HOUR 6: Full Stack Integration

**Test Complete Workflow**:
```bash
# Terminal 1: Server with logging
poetry run python run_server.py

# Terminal 2: Dashboard
cd dashboard && npm run dev

# Terminal 3: Execute task
shannon do "create simple test.py file" --dashboard

# Verify:
# - Dashboard shows task progress
# - Events stream in real-time
# - Execution completes
# - File is created
# - Git commit happens
```

**Document**:
- Screenshot of dashboard showing execution
- Log of events received
- Proof file was created
- Git log showing commit

**Exit**: End-to-end workflow proven with evidence

---

## Expected Outcomes

### After Hour 2:
- Know exact test pass/fail counts
- Know what's actually tested
- Have list of broken tests to fix

### After Hour 4:
- shannon do creates real files
- Skills execute successfully
- Can use for actual work

### After Hour 6:
- Full stack proven working
- Dashboard + server connected
- Real-time execution visible
- Can claim 90% functional with proof

---

## Success Criteria

**Can Only Claim "Functional" When**:
- ✅ Tests actually run (not agent claims)
- ✅ shannon do creates real files
- ✅ Dashboard connects to server
- ✅ Full workflow works end-to-end
- ✅ Evidence provided (screenshots, logs, files created)

**Until Then**:
- Claim: "Infrastructure complete, foundation working"
- Don't claim: "95% functional" without proof

---

## Honest Starting Point for Next Session

**PROVEN** (20%):
- Wave 1 & 2: Integration tests passed

**UNPROVEN** (80%):
- Everything else

**Realistic Goal**: Prove 70% more (reach 90% proven)
**Timeline**: 6 focused hours of testing

**Approach**: Test first, fix second, claim last

