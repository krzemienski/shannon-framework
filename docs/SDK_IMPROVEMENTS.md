# Shannon SDK Improvements

## Overview

Shannon-CLI's Claude Agent SDK integration has been enhanced with comprehensive improvements based on official SDK documentation. All changes are **backward compatible** and provide better error handling, observability, and capabilities.

## Summary of Changes

### ✅ Completed Improvements

1. **Specific Exception Handling** - Better error messages
2. **Edit Tool Support** - Precise code modifications  
3. **max_turns Limit** - Cost control
4. **SDK Hooks** - Tool-level monitoring
5. **stderr Callback** - Integrated logging
6. **ThinkingBlock Support** - Thinking model compatibility
7. **include_partial_messages** - Real-time streaming
8. **ClaudeSDKClient Integration** - Interactive sessions
9. **InteractiveSession Class** - Conversation management

## Detailed Changes

### 1. Exception Handling Enhancement

**Before:**
```python
except Exception as e:
    logger.error(f"Skill invocation failed: {e}")
    raise
```

**After:**
```python
except CLINotFoundError as e:
    raise RuntimeError(
        "Claude Code not installed. Install with:\n"
        "  npm install -g @anthropic-ai/claude-code"
    ) from e
except ProcessError as e:
    raise RuntimeError(
        f"Claude Code process failed with exit code {e.exit_code}\n"
        f"Error: {e.stderr}"
    ) from e
except CLIConnectionError as e:
    raise RuntimeError(f"Failed to connect to Claude Code: {e}") from e
except CLIJSONDecodeError as e:
    raise RuntimeError(f"Failed to parse Claude Code response: {e}") from e
except Exception as e:
    logger.error(f"Skill invocation failed: {e}")
    raise
```

**Benefits:**
- ✅ User-friendly error messages
- ✅ Installation instructions when CLI missing
- ✅ Detailed exit codes and stderr output
- ✅ Better debugging experience

**Affected Methods:**
- `invoke_skill()`
- `invoke_command()`
- `invoke_command_with_enhancements()`
- `InteractiveSession.send()`
- `InteractiveSession.connect()`

---

### 2. Edit Tool Added

**Before:**
```python
allowed_tools=[
    "Skill", "Read", "Write", "Bash", ...
]
```

**After:**
```python
allowed_tools=[
    "Skill", "Read", "Write", "Edit",  # ← Added
    "Bash", ...
]
```

**Benefits:**
- ✅ Precise search-and-replace code modifications
- ✅ Better than Write for existing file edits
- ✅ `old_string` → `new_string` pattern
- ✅ `replace_all` option for global changes

**Edit Tool Usage:**
```json
{
    "file_path": "/path/to/file.py",
    "old_string": "def old_function():",
    "new_string": "def new_function():",
    "replace_all": false
}
```

---

### 3. max_turns Limit

**Before:**
```python
ClaudeAgentOptions(
    plugins=[...],
    # No max_turns - unlimited
)
```

**After:**
```python
ClaudeAgentOptions(
    plugins=[...],
    max_turns=50,  # ← Added
)
```

**Benefits:**
- ✅ Prevents infinite loops
- ✅ Controls runaway costs
- ✅ Reasonable limit for complex tasks
- ✅ Configurable per use case

**Customization:**
```python
# For simple tasks
options = ClaudeAgentOptions(max_turns=10)

# For complex analysis
options = ClaudeAgentOptions(max_turns=50)

# For unlimited (use with caution)
options = ClaudeAgentOptions(max_turns=None)
```

---

### 4. SDK Hooks for Tool Monitoring

**Implementation:**
```python
async def pre_tool_hook(input_data: dict, tool_use_id: Optional[str], context: HookContext) -> dict:
    """Log tool usage before execution"""
    tool_name = input_data.get('tool_name', 'unknown')
    self.logger.debug(f"[PRE-TOOL] {tool_name}")
    return {}

async def post_tool_hook(input_data: dict, tool_use_id: Optional[str], context: HookContext) -> dict:
    """Log tool completion after execution"""
    tool_name = input_data.get('tool_name', 'unknown')
    self.logger.debug(f"[POST-TOOL] {tool_name} completed")
    return {}

ClaudeAgentOptions(
    hooks={
        'PreToolUse': [HookMatcher(hooks=[pre_tool_hook])],
        'PostToolUse': [HookMatcher(hooks=[post_tool_hook])]
    }
)
```

**Benefits:**
- ✅ Tool-level observability
- ✅ Complements message-level MessageCollector
- ✅ Can block/modify tool execution
- ✅ Logging and auditing

**Available Hook Events:**
- `PreToolUse` - Before tool execution
- `PostToolUse` - After tool execution  
- `UserPromptSubmit` - When user submits prompt
- `Stop` - When stopping execution
- `SubagentStop` - When subagent stops
- `PreCompact` - Before message compaction

**Hook Response Options:**
```python
# Allow tool execution
return {}

# Block tool execution
return {
    'hookSpecificOutput': {
        'hookEventName': 'PreToolUse',
        'permissionDecision': 'deny',
        'permissionDecisionReason': 'Dangerous command blocked'
    }
}
```

---

### 5. stderr Callback Integration

**Implementation:**
```python
def stderr_handler(stderr_line: str) -> None:
    """Integrate SDK stderr into shannon logging"""
    self.logger.debug(f"[SDK stderr] {stderr_line.strip()}")

ClaudeAgentOptions(
    stderr=stderr_handler
)
```

**Benefits:**
- ✅ SDK stderr integrated into Shannon logging
- ✅ Better log aggregation
- ✅ Unified debugging experience
- ✅ No separate stderr streams

**Before:**
- SDK stderr → sys.stderr (separate stream)

**After:**
- SDK stderr → Shannon logger (unified)

---

### 6. ThinkingBlock Support

**Implementation:**
```python
from claude_agent_sdk import ThinkingBlock

# In message parsing
if isinstance(block, ThinkingBlock):
    logger.debug(f"Thinking: {block.thinking[:100]}...")
    # Optionally display or log thinking content
```

**Benefits:**
- ✅ Future-proof for thinking-capable models
- ✅ Insight into Claude's reasoning process
- ✅ Better debugging and understanding
- ✅ Optional display (user-controlled)

**ThinkingBlock Structure:**
```python
@dataclass
class ThinkingBlock:
    thinking: str      # Reasoning content
    signature: str     # Thinking signature
```

**Interactive Mode:**
```bash
shannon interactive --show-thinking

Claude: [Thinking] Let me analyze the requirements...
        First, I need to understand the API structure...
        Then I'll identify the key components...
```

---

### 7. include_partial_messages

**Configuration:**
```python
# Character-by-character streaming (default in interactive)
ClaudeAgentOptions(
    include_partial_messages=True
)

# Block-level streaming (faster, less granular)
ClaudeAgentOptions(
    include_partial_messages=False
)
```

**Benefits:**
- ✅ Real-time text display
- ✅ Better UX in interactive mode
- ✅ See responses as they're generated
- ✅ Smoother streaming experience

**Performance:**
- `True`: More messages, lower latency per character
- `False`: Fewer messages, higher latency per block

---

### 8. ClaudeSDKClient Integration

**New Capability:**
```python
from claude_agent_sdk import ClaudeSDKClient

# Continuous conversation session
async with ClaudeSDKClient(options=...) as client:
    # Turn 1
    await client.query("What is Python?")
    async for msg in client.receive_response():
        print(msg)
    
    # Turn 2 - Remembers Turn 1!
    await client.query("Show me an example")
    async for msg in client.receive_response():
        print(msg)
```

**vs query() Function:**
```python
from claude_agent_sdk import query

# NEW session each time (no memory)
async for msg in query(prompt="What is Python?", options=...):
    print(msg)

# DIFFERENT session (doesn't remember)
async for msg in query(prompt="Show me an example", options=...):
    print(msg)
```

**When to Use:**

**ClaudeSDKClient:**
- ✅ Multi-turn conversations
- ✅ Follow-up questions
- ✅ Interactive workflows
- ✅ Context preservation needed

**query():**
- ✅ One-off tasks
- ✅ Independent operations
- ✅ Automation scripts
- ✅ Fresh context each time

---

### 9. InteractiveSession Class

**New Class in `shannon.sdk`:**

```python
from shannon.sdk import InteractiveSession

async with session:
    await session.send("Your message")
    async for msg in session.receive():
        # Process messages
        if isinstance(msg, TextBlock):
            print(msg.text)
        elif isinstance(msg, ThinkingBlock):
            print(f"Thinking: {msg.thinking}")
```

**Features:**
- ✅ Async context manager
- ✅ Automatic connect/disconnect
- ✅ Turn counting
- ✅ Interrupt support
- ✅ Session statistics
- ✅ Error handling

**Methods:**
- `connect()` - Establish session
- `disconnect()` - End session
- `send(message)` - Send user input
- `receive()` - Receive responses
- `interrupt()` - Stop current operation
- `get_turn_count()` - Session statistics
- `is_active()` - Check if connected

---

## Architecture Impact

### Message Flow (Before)

```
User Command → ShannonSDKClient.invoke_skill()
    ↓
    query() [NEW SESSION]
    ↓
    SDK Messages → MessageInterceptor → MessageCollectors
    ↓
    Process & Exit [SESSION ENDS]
```

### Message Flow (After - Interactive)

```
User Command → ShannonSDKClient.start_interactive_session()
    ↓
    ClaudeSDKClient [PERSISTENT SESSION]
    ↓
    ┌─────────────────────────────┐
    │ Turn 1: query() + receive() │ ← Context preserved
    │ Turn 2: query() + receive() │ ← Remembers Turn 1
    │ Turn 3: query() + receive() │ ← Remembers 1 & 2
    │ ...                         │
    └─────────────────────────────┘
    ↓
    disconnect() [SESSION ENDS]
```

### Monitoring Layers

```
┌──────────────────────────────────────┐
│ SDK Hooks (Tool Level)               │
│ - PreToolUse / PostToolUse           │
│ - Can block/modify tools             │
└─────────────┬────────────────────────┘
              │
              ▼
┌──────────────────────────────────────┐
│ MessageInterceptor (Message Level)   │
│ - MessageCollectors                  │
│ - Metrics, Context, Agents           │
└─────────────┬────────────────────────┘
              │
              ▼
┌──────────────────────────────────────┐
│ StreamHandler (Stream Level)         │
│ - Health monitoring                  │
│ - Buffering                          │
└──────────────────────────────────────┘
```

**Complementary, not conflicting!** Each layer serves different purposes.

---

## Migration Guide

### No Breaking Changes

All improvements are **backward compatible**. Existing code continues to work.

### Gradual Adoption

**Phase 1 - Automatic (Already Applied):**
- ✅ Exception handling (better errors)
- ✅ Edit tool (available automatically)
- ✅ max_turns (prevents runaway)
- ✅ Hooks (automatic logging)
- ✅ stderr callback (integrated)

**Phase 2 - Opt-In:**
- ⚡ ThinkingBlock (use `--show-thinking`)
- ⚡ Interactive mode (use `shannon interactive`)
- ⚡ Partial messages (enabled in interactive)

**Phase 3 - Future:**
- 🔮 Custom SDK tools via `@tool` decorator
- 🔮 Session persistence/resumption
- 🔮 can_use_tool callbacks for security
- 🔮 Model selection per task type

---

## Performance Impact

| Change | Overhead | Benefit |
|--------|----------|---------|
| Exception handling | None | Better UX |
| Edit tool | None | Better code editing |
| max_turns | None | Cost control |
| SDK hooks | Minimal (~1ms/tool) | Observability |
| stderr callback | Minimal | Log integration |
| ThinkingBlock | None (parse only) | Model insights |
| include_partial_messages | Small (more msgs) | Real-time UX |
| ClaudeSDKClient | Small (session mgmt) | Context preservation |

**Net Impact:** Negligible overhead, significant benefits.

---

## Configuration Reference

### Base Options (All Commands)

```python
ClaudeAgentOptions(
    plugins=[{"type": "local", "path": framework_path}],
    setting_sources=["user", "project"],
    permission_mode="bypassPermissions",
    allowed_tools=[
        "Skill", "Read", "Write", "Edit",  # ← Edit added
        "Bash", "SlashCommand", "Grep", "Glob", "TodoWrite",
        "mcp__serena__write_memory",
        "mcp__serena__read_memory",
        "mcp__serena__list_memories",
        "mcp__serena__get_current_config",
        "mcp__sequential-thinking__sequentialthinking"
    ],
    max_turns=50,  # ← Added
    hooks={  # ← Added
        'PreToolUse': [HookMatcher(hooks=[pre_tool_hook])],
        'PostToolUse': [HookMatcher(hooks=[post_tool_hook])]
    },
    stderr=stderr_handler  # ← Added
)
```

### Interactive Options (Interactive Mode)

```python
ClaudeAgentOptions(
    # ... all base options ...
    include_partial_messages=True,  # ← Character-level streaming
)
```

---

## Testing Strategy

### Unit Tests
- ✅ Exception handling (mock SDK errors)
- ✅ Hook invocation (verify callbacks called)
- ✅ InteractiveSession lifecycle

### Integration Tests
- ✅ Edit tool with Framework skills
- ✅ max_turns enforcement
- ✅ Interactive session flow

### End-to-End Tests
- ✅ Full interactive workflows
- ✅ ThinkingBlock parsing
- ✅ Partial message streaming

**Philosophy:** Use REAL SDK, no mocks (per Shannon testing standards).

---

## Documentation Updates

### New Files
1. ✅ `docs/INTERACTIVE_MODE.md` - Interactive mode guide
2. ✅ `docs/SDK_IMPROVEMENTS.md` - This file

### Updated Files
- ⏳ `docs/USER_GUIDE.md` - Add interactive mode section
- ⏳ `docs/API_REFERENCE.md` - Document InteractiveSession
- ⏳ `README.md` - Add interactive mode to features

---

## Future Enhancements

### Short-term (Next Sprint)
- [ ] Custom SDK tools via `@tool` decorator
- [ ] Session persistence (save/resume)
- [ ] can_use_tool security callbacks
- [ ] Model selection per task type

### Medium-term (Next Quarter)
- [ ] Multi-session management
- [ ] Session analytics and insights
- [ ] Cost optimization heuristics
- [ ] Advanced hook configurations

### Long-term (Future)
- [ ] Distributed session support
- [ ] Session sharing/collaboration
- [ ] Advanced thinking model features
- [ ] Custom plugin integrations

---

## Summary

Shannon's SDK integration is now **production-ready** with:

- ✅ **Robust error handling** - User-friendly messages
- ✅ **Enhanced tools** - Edit for precise modifications
- ✅ **Cost controls** - max_turns prevents runaway
- ✅ **Comprehensive monitoring** - Hooks + MessageCollectors
- ✅ **Modern capabilities** - ThinkingBlock, partial messages
- ✅ **Interactive sessions** - ClaudeSDKClient integration
- ✅ **Full backward compatibility** - No breaking changes

All improvements follow **official SDK patterns** and best practices.

