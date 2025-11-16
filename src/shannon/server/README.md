# Shannon Dashboard Server

WebSocket communication layer for Shannon v4.0 Dashboard with FastAPI and Socket.IO.

## Architecture

```
┌─────────────┐         ┌──────────────┐         ┌──────────────┐
│  Dashboard  │◄───────►│    Server    │◄───────►│ Orchestrator │
│   (React)   │  WS/HTTP│ FastAPI+SIO  │  Events │   (Python)   │
└─────────────┘         └──────────────┘         └──────────────┘
     │                         │                         │
     │                         ▼                         │
     │                  ┌──────────────┐                │
     │                  │ Skills       │◄───────────────┘
     │                  │ Registry     │
     │                  └──────────────┘
     │                         │
     └────────────────────────▼──────────────────────────┘
                        Real-time Events
```

## Components

### 1. FastAPI Application (`app.py`)

RESTful API endpoints for dashboard:

- **GET /health** - Server health check
- **GET /api/skills** - List all registered skills (with filters)
- **GET /api/skills/{name}** - Get skill details
- **GET /api/sessions** - List active execution sessions
- **GET /api/sessions/{session_id}** - Get session details
- **POST /api/sessions** - Create new execution session
- **DELETE /api/sessions/{session_id}** - Delete session

### 2. Socket.IO Integration (`websocket.py`)

Real-time WebSocket communication:

**Connection Handlers:**
- `connect` - Handle new dashboard connections
- `disconnect` - Handle disconnections
- `command` - Process commands from dashboard
- `ping` - Latency measurement
- `subscribe` - Subscribe to specific events/sessions

**Command Processing:**
- `HALT` - Pause execution
- `RESUME` - Resume execution
- `ROLLBACK` - Rollback N steps
- `REDIRECT` - Change execution path
- `DECISION` - Make decision at decision point
- `INJECT` - Inject new skill/command

**Event Emission (Server → Dashboard):**
- `skill:started` - Skill execution began
- `skill:completed` - Skill succeeded
- `skill:failed` - Skill failed
- `skill:progress` - Progress update
- `file:modified` - File changed
- `file:created` - File created
- `file:deleted` - File deleted
- `decision:point` - Decision required
- `decision:made` - Decision completed
- `validation:started` - Validation began
- `validation:result` - Validation results
- `agent:spawned` - New agent created
- `agent:progress` - Agent progress
- `agent:completed` - Agent finished
- `checkpoint:created` - Checkpoint saved
- `execution:halted` - Execution paused
- `execution:resumed` - Execution continued

## Usage

### Starting the Server

```bash
# Development mode with auto-reload
python run_server.py --reload

# Production mode
python run_server.py --host 0.0.0.0 --port 8000

# Custom configuration
python run_server.py --host 127.0.0.1 --port 5000 --log-level debug
```

### Connecting from Dashboard

```javascript
import io from 'socket.io-client';

// Connect to server
const socket = io('http://localhost:8000', {
  query: { session_id: 'session_abc' }
});

// Handle connection
socket.on('connected', (data) => {
  console.log('Connected:', data);
});

// Listen for events
socket.on('skill:started', (event) => {
  console.log('Skill started:', event.data);
});

// Send commands
socket.emit('command', {
  type: 'HALT',
  reason: 'User requested pause'
});

// Handle command results
socket.on('command:result', (result) => {
  if (result.success) {
    console.log('Command succeeded');
  }
});
```

### Emitting Events from Orchestrator

```python
from shannon.server.websocket import (
    emit_skill_event,
    emit_file_event,
    emit_decision_event
)

# Emit skill started event
await emit_skill_event('skill:started', {
    'skill_name': 'test_skill',
    'parameters': {'param1': 'value1'}
}, session_id='session_abc')

# Emit file modified event
await emit_file_event('file:modified', {
    'path': '/path/to/file.py',
    'changes': 'Added function',
    'lines_changed': 10
}, session_id='session_abc')

# Emit decision point
await emit_decision_event('decision:point', {
    'decision_id': 'decision_001',
    'question': 'Which approach?',
    'options': ['A', 'B', 'C'],
    'default': 'A'
}, session_id='session_abc')
```

### Handling Commands in Orchestrator

```python
from shannon.server.websocket import conn_manager

# Register command handler
async def my_halt_handler():
    """Custom halt handler."""
    print("Execution halted!")
    # Pause orchestrator...

conn_manager.register_command_handler('HALT', my_halt_handler)

# Check execution state
state = await conn_manager.get_execution_state()
if state == ExecutionState.HALTED:
    # Wait for resume...
    pass
```

## Session Management

Sessions provide isolated execution contexts with room-based event routing:

```python
# Create session
POST /api/sessions
{
    "session_id": "session_abc",
    "skills": ["skill1", "skill2"],
    "metadata": {
        "user": "developer",
        "project": "my_project"
    }
}

# Multiple dashboards can connect to same session
# Events are broadcast to all connections in session room
```

## Performance

### Latency Targets

- **Event Emission:** <50ms
- **Command Processing:** <50ms
- **Connection Handling:** <100ms

### Testing Latency

```bash
# Run performance tests
pytest tests/server/test_websocket.py::TestPerformance -v

# Test with actual server
python -c "
import asyncio
import socketio
import time

async def test():
    sio = socketio.AsyncClient()
    await sio.connect('http://localhost:8000')

    start = time.perf_counter()
    await sio.emit('ping')
    await sio.wait()
    end = time.perf_counter()

    print(f'Latency: {(end-start)*1000:.2f}ms')

asyncio.run(test())
"
```

## Error Handling

All errors are logged and returned with structured responses:

```json
{
    "success": false,
    "error": "Error message",
    "timestamp": "2025-11-15T20:00:00.000Z"
}
```

## Testing

```bash
# Run all server tests
pytest tests/server/ -v

# Run specific test class
pytest tests/server/test_websocket.py::TestConnectionManager -v

# Run with coverage
pytest tests/server/ --cov=shannon.server --cov-report=html

# Performance tests only
pytest tests/server/test_websocket.py::TestPerformance -v
```

## Security Considerations

1. **CORS:** Configured for localhost development, restrict in production
2. **Authentication:** Add token-based auth for production
3. **Rate Limiting:** Implement command rate limits
4. **Input Validation:** All commands validated before processing
5. **Session Isolation:** Room-based separation prevents cross-session leaks

## Monitoring

### Connection Statistics

```python
from shannon.server.websocket import get_connection_stats

stats = await get_connection_stats()
# {
#     'total_connections': 5,
#     'sessions': {
#         'session_abc': 2,
#         'session_xyz': 3
#     },
#     'timestamp': '2025-11-15T20:00:00.000Z'
# }
```

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
    "status": "healthy",
    "version": "4.0.0",
    "timestamp": "2025-11-15T20:00:00.000Z",
    "active_sessions": 2,
    "connected_clients": 5
}
```

## Integration with Orchestrator

The server integrates with Shannon's orchestrator through event emission:

```python
# In orchestrator.py
from shannon.server.websocket import emit_skill_event

class ContextAwareOrchestrator:
    async def execute_skill(self, skill_name, params):
        # Emit start event
        await emit_skill_event('skill:started', {
            'skill_name': skill_name,
            'parameters': params
        }, session_id=self.session_id)

        try:
            # Execute skill...
            result = await skill.execute(params)

            # Emit completion
            await emit_skill_event('skill:completed', {
                'skill_name': skill_name,
                'result': result
            }, session_id=self.session_id)

        except Exception as e:
            # Emit failure
            await emit_skill_event('skill:failed', {
                'skill_name': skill_name,
                'error': str(e)
            }, session_id=self.session_id)
```

## Future Enhancements

- [ ] Authentication/Authorization
- [ ] Event filtering and subscriptions
- [ ] Persistent event history
- [ ] Command queuing and replay
- [ ] Metrics and analytics dashboard
- [ ] Multi-tenancy support
- [ ] WebRTC for direct peer communication
- [ ] GraphQL subscriptions alongside REST

## Troubleshooting

### Server won't start

```bash
# Check if port is in use
lsof -i :8000

# Try different port
python run_server.py --port 8001
```

### WebSocket connection fails

1. Check CORS settings in `app.py`
2. Verify Socket.IO client version compatibility
3. Check firewall settings
4. Enable debug logging: `--log-level debug`

### High latency

1. Check network conditions
2. Run performance tests
3. Enable profiling
4. Check for blocking operations in event handlers

## Documentation

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Socket.IO Docs](https://socket.io/docs/v4/)
- [Shannon Architecture](../../../docs/ARCHITECTURE.md)
- [Dashboard Integration](../../../docs/DASHBOARD.md)
