# ADR-001: SDK Message Interception Strategy

**Date**: 2025-01-13
**Status**: Accepted
**Context**: Shannon CLI V3.0 Architecture Phase

---

## Context

Shannon CLI V3.0 requires real-time visibility into Shannon Framework operations for:
- Live metrics dashboard (cost, tokens, progress)
- Agent state tracking (parallel wave execution)
- Context usage monitoring (file references, patterns)
- Cost optimization (model selection, budget enforcement)
- Analytics recording (historical tracking)

The Claude Agent SDK provides an async iterator interface:

```python
async for msg in query(prompt, options):
    # Messages stream in real-time
    # AssistantMessage, ToolUseBlock, SystemMessage, etc.
    pass
```

**Challenge**: How do we intercept this message stream to extract metrics, track state, and collect data WITHOUT:
1. Breaking the async iteration contract
2. Adding latency to message delivery
3. Losing messages
4. Blocking the UI thread
5. Requiring changes to SDK or Shannon Framework

---

## Decision

Use a **Transparent Async Wrapper Pattern** with **Parallel Message Collectors**.

### Architecture

```python
class MessageInterceptor:
    """
    Transparent wrapper around SDK query() that:
    1. Yields all messages unchanged (maintains API contract)
    2. Asynchronously processes messages in parallel
    3. Updates live dashboard without blocking
    4. Routes messages to appropriate handlers
    """

    async def intercept(
        self,
        query_iterator: AsyncIterator[Message],
        collectors: List[MessageCollector]
    ) -> AsyncIterator[Message]:
        """
        Intercept messages while maintaining streaming behavior
        """

        async for msg in query_iterator:
            # Non-blocking: Fire collectors in background
            for collector in collectors:
                # Each collector processes asynchronously
                asyncio.create_task(collector.process(msg))

            # Yield immediately - no latency added
            yield msg


class MessageCollector(ABC):
    """Base interface for all collectors"""

    @abstractmethod
    async def process(self, msg: Message) -> None:
        """Process message asynchronously"""
        pass
```

### Collectors

```python
# Metrics collection
class MetricsCollector(MessageCollector):
    async def process(self, msg: Message):
        # Extract cost, tokens, timing
        # Update live dashboard
        pass

# Agent state tracking
class AgentStateCollector(MessageCollector):
    async def process(self, msg: Message):
        # Track agent progress
        # Identify tool calls
        # Update agent state
        pass

# Context usage tracking
class ContextCollector(MessageCollector):
    async def process(self, msg: Message):
        # Extract file references
        # Track context effectiveness
        pass
```

### Integration

```python
# In ShannonSDKClient
async def invoke_skill(self, skill_name: str, prompt: str):
    # Original SDK call
    query_iterator = query(prompt, self.base_options)

    # V3 Enhancement: Wrap with interceptor
    if self.enable_v3_features:
        interceptor = MessageInterceptor()
        collectors = [
            MetricsCollector(self.metrics_dashboard),
            AgentStateCollector(self.agent_tracker),
            ContextCollector(self.context_manager)
        ]
        query_iterator = interceptor.intercept(query_iterator, collectors)

    # Caller receives transparent async iterator
    async for msg in query_iterator:
        yield msg
```

---

## Rationale

### Why This Approach?

1. **Zero Latency**
   - Messages yielded immediately
   - Collectors run in background (asyncio.create_task)
   - No blocking on collection logic

2. **Non-Breaking**
   - Caller receives identical AsyncIterator interface
   - Works with existing V2 code
   - Can be disabled via feature flag

3. **Extensible**
   - Easy to add new collectors
   - Each collector is independent
   - No coordination required between collectors

4. **Error Isolation**
   - Collector failures don't affect message stream
   - Each collector wrapped in try/except
   - Errors logged but don't break iteration

5. **Observable**
   - All messages visible to all collectors
   - Multiple collectors can process same stream
   - No message loss or duplication

---

## Alternatives Considered

### Alternative 1: Monkey-Patching SDK

**Approach**: Patch the `query()` function to inject collection logic

```python
original_query = claude_agent_sdk.query

def patched_query(prompt, options):
    async for msg in original_query(prompt, options):
        # Inject collection here
        collect_metrics(msg)
        yield msg

claude_agent_sdk.query = patched_query
```

**Pros**:
- No wrapper needed
- Transparent to caller

**Cons**:
- **Rejected**: Too fragile, breaks on SDK updates
- Hard to test
- Difficult to disable
- Violates least surprise principle

### Alternative 2: SDK Modification

**Approach**: Fork Claude Agent SDK and add hooks

```python
# In forked SDK
async def query(prompt, options, message_hook=None):
    async for msg in _internal_query(prompt, options):
        if message_hook:
            await message_hook(msg)
        yield msg
```

**Pros**:
- Clean integration
- First-class support

**Cons**:
- **Rejected**: Requires maintaining SDK fork
- Can't use official SDK
- Updates delayed
- Contribution might not be accepted

### Alternative 3: Message Buffering

**Approach**: Buffer all messages, process, then replay

```python
async def intercept(query_iterator):
    messages = []

    # Collect all messages first
    async for msg in query_iterator:
        messages.append(msg)

    # Process
    for msg in messages:
        await process(msg)

    # Replay
    for msg in messages:
        yield msg
```

**Pros**:
- Simple implementation
- Sequential processing

**Cons**:
- **Rejected**: Adds latency (must wait for all messages)
- Breaks streaming UX
- Memory overhead for long operations
- Defeats purpose of async streaming

### Alternative 4: Sync Collectors

**Approach**: Process synchronously in iteration loop

```python
async def intercept(query_iterator, collectors):
    async for msg in query_iterator:
        # Process synchronously
        for collector in collectors:
            await collector.process(msg)  # Wait for each

        yield msg
```

**Pros**:
- Simple
- Sequential processing
- No background tasks

**Cons**:
- **Rejected**: Adds latency (must wait for all collectors)
- Slow collectors block message delivery
- UI freezes during collection
- Defeats purpose of streaming

---

## Consequences

### Positive

1. **Performance**
   - Zero added latency to message delivery
   - Collectors run in parallel
   - UI remains responsive

2. **Maintainability**
   - Clean separation of concerns
   - Easy to add/remove collectors
   - No SDK coupling

3. **Reliability**
   - No message loss
   - Error isolation
   - Can disable if needed

4. **Testability**
   - Can test collectors independently
   - Can test interceptor without collectors
   - Functional tests validate real behavior

### Negative

1. **Complexity**
   - Async coordination more complex than sync
   - Background tasks need lifecycle management
   - Potential for race conditions in collectors (mitigated with locks)

2. **Error Handling**
   - Collector errors happen in background
   - Need explicit error propagation
   - Logging becomes more important

3. **Debugging**
   - Parallel execution harder to debug
   - Need async-aware debugging tools
   - Message ordering not guaranteed in collectors

### Mitigations

**Complexity**:
- Clear interfaces (MessageCollector ABC)
- Comprehensive documentation
- Example collectors as reference

**Error Handling**:
```python
async def process_safely(collector, msg):
    try:
        await collector.process(msg)
    except Exception as e:
        logger.error(f"Collector {collector.__class__.__name__} failed: {e}")
        # Don't propagate - isolate errors
```

**Debugging**:
- Add debug logging at interception points
- Collector metrics (messages processed, errors)
- Optional sync mode for debugging

---

## Implementation Notes

### Collector Lifecycle

```python
class MessageInterceptor:
    def __init__(self):
        self.active_tasks: List[asyncio.Task] = []

    async def intercept(self, query_iterator, collectors):
        try:
            async for msg in query_iterator:
                # Create tasks
                for collector in collectors:
                    task = asyncio.create_task(
                        self._process_safely(collector, msg)
                    )
                    self.active_tasks.append(task)

                yield msg
        finally:
            # Wait for all collectors to finish
            if self.active_tasks:
                await asyncio.gather(*self.active_tasks, return_exceptions=True)
```

### Performance Characteristics

- **Latency**: <1ms per message (async overhead only)
- **Memory**: O(n) where n = number of messages (temporary task list)
- **CPU**: Parallel collector execution (scales with cores)
- **Throughput**: Limited by SDK, not interceptor

### Testing Strategy

```python
async def test_interception_preserves_messages():
    """Verify all messages pass through unchanged"""

    messages = []
    async def mock_query():
        yield AssistantMessage(...)
        yield SystemMessage(...)
        yield ResultMessage(...)

    async for msg in interceptor.intercept(mock_query(), collectors=[]):
        messages.append(msg)

    assert len(messages) == 3
    # Verify message integrity
```

```python
async def test_collector_receives_all_messages():
    """Verify collectors see all messages"""

    collector = MetricsCollector()

    async for msg in interceptor.intercept(query_stream, [collector]):
        pass

    assert collector.message_count == expected_count
```

---

## Related Decisions

- **ADR-002**: Context-Aware Cache Keys (depends on ContextCollector)
- **ADR-003**: Agent State Tracking (depends on AgentStateCollector)
- **ADR-004**: Live Metrics Dashboard (depends on MetricsCollector)

---

## References

- Claude Agent SDK documentation
- AsyncIO documentation (create_task, gather)
- Shannon CLI V2 message parsing (existing code)
- Python async/await best practices

---

## Status History

- **2025-01-13**: Proposed and accepted
- **Context**: Architecture phase for Shannon CLI V3.0
- **Decision**: Transparent async wrapper with parallel collectors
- **Implementation**: Phase 1 (Weeks 1-2)

---

**This decision is foundational to all V3 features.** Every subsystem (metrics, agents, context, analytics) depends on message interception working correctly without breaking the SDK contract.
