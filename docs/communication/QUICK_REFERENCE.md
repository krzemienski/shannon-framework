# Shannon Communication - Quick Reference

## Event Bus

### Emit Event
```python
await event_bus.emit(
    event_type=EventType.SKILL_STARTED,
    data={"skill_name": "test"},
    source="executor",
    correlation_id="exec-123"
)
```

### Subscribe
```python
# Specific event type
sub_id = await event_bus.subscribe(
    EventType.SKILL_STARTED,
    handler_function
)

# All events
sub_id = await event_bus.subscribe_all(handler_function)

# With filter
sub_id = await event_bus.subscribe(
    EventType.SKILL_STARTED,
    handler_function,
    filter_fn=lambda e: e.data.get("important")
)
```

### Unsubscribe
```python
await event_bus.unsubscribe(sub_id)
```

### History
```python
# Get all
history = event_bus.get_history()

# Get filtered
history = event_bus.get_history(
    event_type=EventType.SKILL_STARTED,
    limit=10,
    correlation_id="exec-123"
)
```

### WebSocket
```python
event_bus.register_websocket_handler(handler)
event_bus.unregister_websocket_handler(handler)
```

### Stats
```python
stats = event_bus.get_stats()
```

## Command Queue

### Enqueue
```python
command = await queue.enqueue(
    command_type=CommandType.HALT,
    data={"reason": "pause"},
    priority=1,  # 1=highest, 10=lowest
    source="websocket"
)
```

### Dequeue
```python
# Wait forever
command = await queue.dequeue()

# With timeout
command = await queue.dequeue(timeout=5.0)
```

### Complete
```python
# Success
await queue.complete_command(
    command,
    result={"status": "ok"}
)

# Failure
await queue.complete_command(
    command,
    error="Something went wrong"
)
```

### Cancel
```python
success = await queue.cancel_command(command_id)
```

### History
```python
# Get recent
history = queue.peek_history(limit=10)

# Get pending
pending = queue.peek_pending()

# Get by ID
command = queue.get_command_by_id(command_id)

# Get filtered
history = queue.peek_history(
    command_type=CommandType.HALT,
    status=CommandStatus.COMPLETED
)
```

### Stats
```python
stats = queue.get_stats()
```

## Event Types

```python
# Skills
EventType.SKILL_STARTED
EventType.SKILL_COMPLETED
EventType.SKILL_FAILED
EventType.SKILL_PROGRESS

# Files
EventType.FILE_MODIFIED
EventType.FILE_CREATED
EventType.FILE_DELETED
EventType.FILE_MOVED

# Decisions
EventType.DECISION_POINT
EventType.DECISION_MADE
EventType.DECISION_REQUIRED

# Validation
EventType.VALIDATION_STARTED
EventType.VALIDATION_RESULT
EventType.VALIDATION_FAILED

# Agents
EventType.AGENT_SPAWNED
EventType.AGENT_PROGRESS
EventType.AGENT_COMPLETED
EventType.AGENT_FAILED

# System
EventType.CHECKPOINT_CREATED
EventType.CHECKPOINT_RESTORED
EventType.EXECUTION_HALTED
EventType.EXECUTION_RESUMED
EventType.EXECUTION_STARTED
EventType.EXECUTION_COMPLETED

# Waves
EventType.WAVE_STARTED
EventType.WAVE_COMPLETED
EventType.WAVE_FAILED

# Errors
EventType.ERROR_OCCURRED
EventType.ERROR_RECOVERED
```

## Command Types

```python
CommandType.HALT        # Pause execution
CommandType.RESUME      # Resume execution
CommandType.ROLLBACK    # Rollback to checkpoint
CommandType.REDIRECT    # Change execution path
CommandType.DECISION    # Provide decision
CommandType.INJECT      # Inject code/data
CommandType.CHECKPOINT  # Create checkpoint
CommandType.CANCEL      # Cancel operation
CommandType.PRIORITY    # Change priority
```

## Command Status

```python
CommandStatus.PENDING     # Not yet processed
CommandStatus.PROCESSING  # Currently processing
CommandStatus.COMPLETED   # Successfully completed
CommandStatus.FAILED      # Failed with error
CommandStatus.CANCELLED   # Cancelled before processing
```

## Global Access

```python
from shannon.communication import get_event_bus, get_command_queue

event_bus = get_event_bus()
command_queue = get_command_queue()
```

## Integration Pattern

```python
class ShannonComponent:
    def __init__(self):
        self.event_bus = get_event_bus()
        self.command_queue = get_command_queue()

    async def run(self):
        # Emit events for state changes
        await self.event_bus.emit(
            EventType.EXECUTION_STARTED,
            data={"component": "example"},
            source="component"
        )

        # Process commands
        while not self.stopped:
            try:
                command = await self.command_queue.dequeue(timeout=1.0)
                await self.handle_command(command)
            except asyncio.TimeoutError:
                continue

    async def handle_command(self, command):
        # Process command
        result = await self.process(command)

        # Complete command
        await self.command_queue.complete_command(
            command,
            result=result
        )

        # Emit event
        await self.event_bus.emit(
            EventType.EXECUTION_COMPLETED,
            data={"result": result},
            source="component"
        )
```
