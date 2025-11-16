# Manual Test Guide: Dashboard Event Reception

## Quick Test (Manual)

### Terminal 1: Start Server
```bash
cd /Users/nick/Desktop/shannon-cli
poetry run python run_server.py
```

Wait for: `Server started on http://localhost:8000`

### Terminal 2: Start Dashboard
```bash
cd /Users/nick/Desktop/shannon-cli/dashboard
npm run dev
```

Wait for: Dashboard URL (usually `http://localhost:5173`)

### Terminal 3: Run Shannon Command
```bash
cd /Users/nick/Desktop/shannon-cli
poetry run shannon do "create test.py" --dashboard
```

### Browser: Open Dashboard
1. Open browser to dashboard URL (e.g., http://localhost:5173)
2. Open browser DevTools (F12)
3. Go to Console tab
4. Look for Socket.IO connection messages
5. Watch the "Event Stream" section on the dashboard
6. Event count should increment as events arrive

### Expected Results

**BEFORE FIX:**
- Event Stream shows "0 events received"
- Console shows: "Dashboard connects with no session_id"
- No events appear in stream

**AFTER FIX (NOW):**
- Event Stream count INCREASES (1, 2, 3...)
- Events appear in real-time:
  - `skill:started` - Skill execution began
  - `skill:completed` - Skill completed
  - `file:created` - Files created
  - etc.
- Console shows successful Socket.IO connection

## Automated Test (Playwright)

```bash
cd /Users/nick/Desktop/shannon-cli
poetry run python test_dashboard_events.py
```

This will:
1. Start server
2. Start dashboard
3. Open browser with Playwright
4. Run shannon command
5. Verify events are received
6. Take screenshots
7. Report results

## Verification Points

1. **Connection**: Dashboard connects to Socket.IO server
2. **Event Count**: Event count > 0 after running command
3. **Event Types**: See skill:started, skill:completed, etc.
4. **Timestamps**: Events have timestamps
5. **Real-time**: Events appear during execution, not after

## Troubleshooting

### Events Not Appearing
- Check server is running on port 8000
- Check dashboard is connecting (see browser console)
- Check for Socket.IO errors in console
- Verify orchestrator is emitting events (check server logs)

### Dashboard Not Connecting
- Clear browser cache
- Check CORS settings
- Verify server URL in dashboard config
- Check firewall/network settings

## Files Changed

- `/Users/nick/Desktop/shannon-cli/src/shannon/server/websocket.py`
  - Removed room-based emission
  - Now broadcasts to ALL clients
  - All emit_*_event() functions updated

## Commit Hash

```
75f2c2c - FIX: Broadcast Socket.IO events to all clients instead of room-based
```
