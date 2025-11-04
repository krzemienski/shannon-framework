# Example: 85% Confidence → CLARIFY

## Scenario
User requests implementation of real-time notifications using WebSocket.

## Input
```
User: "Add real-time notification system using WebSocket.
       Users should get instant alerts for new messages, likes, and comments."
```

## Confidence Check Process

### Check 1: No Duplicate Implementations (25%)
**Action**: Search codebase for existing WebSocket/notification code

```bash
grep -r "websocket\|socket\.io\|notification" src/
```

**Result**:
- ✅ No existing WebSocket server found
- ✅ No Socket.io dependency in package.json
- ✅ Notification feature doesn't exist

**Score**: 25/25 ✅ PASS

**Evidence**: "No duplicate implementation found. Fresh feature."

---

### Check 2: Architecture Compliance (25%)
**Action**: Verify WebSocket approach fits system architecture

**Analysis**:
1. Read: `src/server.js`
   - Current: Express HTTP server on port 3000
   - Can upgrade: HTTP server can attach Socket.io

2. Read: `src/app.js`
   - Pattern: Middleware-based architecture
   - Compatible: Socket.io middleware pattern exists

3. Proposed approach:
   ```javascript
   // In src/server.js
   const http = require('http')
   const { Server } = require('socket.io')

   const httpServer = http.createServer(app)
   const io = new Server(httpServer)

   // Socket.io namespace for notifications
   const notificationNamespace = io.of('/notifications')
   ```

**Result**: ✅ Architecture compliant - Socket.io integrates with Express HTTP server

**Score**: 25/25 ✅ PASS

**Rationale**: "Socket.io server upgrade pattern compatible with Express architecture"

---

### Check 3: Official Docs Verified (20%)
**Action**: Consult Socket.io official documentation

**Verification**:
1. Source: https://socket.io/docs/v4/
2. Version check: package.json would use "socket.io": "^4.6.0" (latest stable)
3. Syntax verification:
   ```javascript
   // Correct Socket.io 4.x syntax
   io.on('connection', (socket) => {
     socket.emit('notification', { message: 'Hello' })
     socket.on('disconnect', () => { /* cleanup */ })
   })
   ```

4. Key patterns verified:
   - Server initialization: `new Server(httpServer, options)`
   - Event emission: `socket.emit(eventName, data)`
   - Room management: `socket.join(roomName)`
   - Namespace isolation: `io.of('/namespace')`

**Result**: ✅ Official docs consulted, syntax confirmed

**Score**: 20/20 ✅ PASS

**Source**: "https://socket.io/docs/v4/server-initialization/"

---

### Check 4: Working OSS Referenced (15%)
**Action**: Research production Socket.io notification implementations

**Issue**: ❌ No OSS research conducted

**What's missing**:
- No GitHub search for "socket.io notifications" OR "real-time notification system"
- No review of production implementations (Slack clones, Discord clones, chat apps)
- No analysis of proven patterns:
  - Room-based notifications (user-specific rooms)
  - Broadcast strategies (emit vs broadcast vs volatile)
  - Reconnection handling
  - Notification queuing for offline users
  - Read/unread status synchronization

**Suggested OSS to research**:
1. `socketio/socket.io-chat-example` (Socket.io official, 1k+ stars)
2. `socketio/socket.io-redis-adapter` (Scalable multi-server setup)
3. Real-world apps: Slack clones, Discord clones with notification systems

**Expected learnings**:
- Room management: One room per user (e.g., `user:${userId}`)
- Notification payload structure: `{ type, title, body, timestamp, read: false }`
- Acknowledgments: Use `socket.emit('notification', data, (ack) => {})` for delivery confirmation
- Persistent storage: Save notifications to DB, emit to online users, queue for offline

**Result**: ❌ FAIL - No OSS researched

**Score**: 0/15 ❌ FAIL

**Reason**: "No production OSS implementations referenced. Need proven patterns."

---

### Check 5: Root Cause Identified (15%)
**Action**: Determine if applicable (N/A for new features)

**Analysis**: This is a new feature request, not a fix or improvement.

**Result**: ⚠️ N/A - Not applicable to new feature implementations

**Score**: 15/15 ⚠️ SKIP (not applicable)

**Note**: "Root cause check applies only to fixes/improvements, not new features"

---

## Confidence Score Calculation

```javascript
total_points = duplicate_check.points +     // 25
               architecture_check.points +   // 25
               docs_check.points +           // 20
               oss_check.points +            //  0  ❌
               root_cause_check.points       // 15 (N/A)

total_points = 25 + 25 + 20 + 0 + 15 = 85

confidence_score = 85 / 100.0 = 0.85 (85%)
```

## Decision Threshold

```javascript
if (0.85 >= 0.90) {
  decision = "PROCEED"  // ❌ FALSE
} else if (0.85 >= 0.70) {
  decision = "CLARIFY"  // ✅ TRUE
} else {
  decision = "STOP"
}

// Result: CLARIFY ⚠️
```

## Output Report

```json
{
  "feature": "websocket_real_time_notifications",
  "timestamp": "2025-11-04T10:45:00Z",
  "confidence_score": 0.85,
  "decision": "CLARIFY",
  "checks": [
    {
      "name": "duplicate",
      "points": 25,
      "max": 25,
      "passed": true,
      "evidence": "No existing WebSocket/notification implementation found"
    },
    {
      "name": "architecture",
      "points": 25,
      "max": 25,
      "passed": true,
      "rationale": "Socket.io server upgrade compatible with Express HTTP server"
    },
    {
      "name": "docs",
      "points": 20,
      "max": 20,
      "passed": true,
      "source": "https://socket.io/docs/v4/server-initialization/",
      "verification": "Socket.io 4.x syntax verified (emit, rooms, namespaces)"
    },
    {
      "name": "oss",
      "points": 0,
      "max": 15,
      "passed": false,
      "examples": [],
      "reason": "No production OSS implementations researched"
    },
    {
      "name": "root_cause",
      "points": 15,
      "max": 15,
      "passed": null,
      "note": "N/A - new feature, root cause check not applicable"
    }
  ],
  "missing_checks": [
    {
      "name": "oss",
      "missing_points": 15,
      "recommendation": "Research Socket.io notification patterns from production apps"
    }
  ],
  "action": "Request OSS examples before proceeding (need 90% confidence)",
  "next_steps": [
    "User: Provide working Socket.io notification example from GitHub",
    "Suggested repos:",
    "  - socketio/socket.io-chat-example (official example)",
    "  - slack-clone or discord-clone with notifications",
    "  - Real-world apps using room-based notification delivery",
    "Agent: Review OSS patterns:",
    "  - Room management (user-specific rooms)",
    "  - Notification payload structure",
    "  - Reconnection handling",
    "  - Offline user notification queuing",
    "Agent: Re-run confidence check after OSS research (expect 100%)"
  ]
}
```

## User Response

**Agent to User**:
```
🔍 Confidence Check Complete: 85% (CLARIFY)

I've validated your WebSocket notification request:

✅ No duplicate implementations (25/25)
✅ Architecture compliant (25/25)
✅ Official Socket.io docs verified (20/20)
❌ Working OSS not researched (0/15)
⚠️  Root cause N/A (new feature)

**Decision: CLARIFY ⚠️**

Before proceeding, please provide a working OSS reference for Socket.io
real-time notifications (GitHub repo with production-quality implementation).

This will help us:
- Learn proven room management patterns
- Understand reconnection handling
- See notification queuing for offline users
- Validate notification payload structure

**Suggested repos to review:**
- socketio/socket.io-chat-example (official)
- Slack/Discord clone implementations with notifications

Once OSS researched, confidence will reach 100% and we can proceed.

**Why this matters:** OSS research prevents reinventing solved problems
(race conditions, edge cases, reconnection logic). 15-30 min research
saves weeks of debugging.

**Current confidence: 85% → Need 90% to proceed**
```

## Expected Flow After Clarification

**User provides OSS reference**:
```
User: "Check out socket.io-chat-example and this Discord clone:
       github.com/discord-clone/notifications (2k stars)"
```

**Agent re-runs confidence check**:
1. **OSS Check (15/15)**:
   - Researched: socket.io-chat-example, discord-clone/notifications
   - Learnings:
     - Room pattern: `socket.join(`user:${userId}`)` for user-specific rooms
     - Emit pattern: `io.to(`user:${userId}`).emit('notification', payload)`
     - Reconnection: Socket.io handles automatically with connection state
     - Persistence: Save to DB first, then emit (ensures offline users get notifications)
   - Result: ✅ PASS

2. **New confidence score**: 100/100 = 1.00 (100%)

3. **New decision**: PROCEED ✅

**Agent proceeds to implementation** with confidence, using learned OSS patterns.

---

## Key Takeaway

**85% confidence = CLARIFY, not PROCEED**

Even though 4/5 checks passed, the missing OSS research (15 points) puts us below
the 90% threshold. This prevents wrong-direction work:

- ❌ Without OSS: Risk reinventing wheel, missing edge cases, inefficient patterns
- ✅ With OSS: Learn from production code, proven patterns, battle-tested

**Result**: 15-30 minutes OSS research prevents 2+ weeks of debugging custom code.

**ROI**: (2 weeks × 40 hours/week × 60 min/hour) / 30 min = 160x token savings
