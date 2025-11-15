# Shannon Interactive Mode

## Overview

Shannon's interactive mode provides a **continuous conversation session** with Claude where context is preserved across multiple turns. Unlike regular shannon commands that create new sessions each time, interactive mode uses `ClaudeSDKClient` to maintain conversation state.

## Why Interactive Mode?

### Traditional (One-Shot) Commands
```bash
shannon analyze spec.md          # New session, no memory
shannon generate --task "API"    # New session, doesn't remember spec
```

Each command creates a **brand new session**. Claude doesn't remember previous interactions.

### Interactive Mode
```bash
shannon interactive

You: analyze spec.md
Claude: [analyzes spec with full details...]

You: what API endpoints did you find?
Claude: [remembers the spec analysis, lists endpoints]

You: generate code for the user endpoint
Claude: [remembers everything, generates relevant code]
```

Claude **remembers ALL previous turns** in the same session!

## Key Features

### 1. **Conversation Continuity**
- Multi-turn conversations where Claude remembers context
- Follow-up questions build on previous exchanges
- Natural conversation flow

### 2. **Real-Time Streaming**
- Character-by-character text streaming (enabled by default)
- See responses as Claude generates them
- Use `--no-partial` to disable

### 3. **Thinking Display**
- See Claude's reasoning process (for thinking-capable models)
- Use `--show-thinking` flag to enable
- Displayed in special panels

### 4. **Interactive Controls**
- `exit` or `quit` - End session
- `help` - Show available commands
- `interrupt` - Stop current operation
- `stats` - Show session statistics
- `Ctrl+C` - Interrupt long operations

## Usage

### Basic Interactive Session
```bash
shannon interactive
```

### With Thinking Display
```bash
shannon interactive --show-thinking
```

### Without Partial Messages (Full Blocks Only)
```bash
shannon interactive --no-partial
```

## Example Workflows

### Exploratory Analysis
```bash
shannon interactive

Turn 1 - You: List all Python files in this project
Turn 1 - Claude: [Lists files...]

Turn 2 - You: Which files handle user authentication?
Turn 2 - Claude: [Identifies auth files, remembers project structure]

Turn 3 - You: Show me the login flow
Turn 3 - Claude: [Explains login flow using knowledge from Turn 1 & 2]
```

### Iterative Development
```bash
shannon interactive

Turn 1 - You: @skill spec-analysis < analyze requirements.md
Turn 1 - Claude: [Performs 8D analysis...]

Turn 2 - You: What's the riskiest component?
Turn 2 - Claude: [Identifies risks based on analysis]

Turn 3 - You: Generate implementation for the authentication module
Turn 3 - Claude: [Generates code addressing identified risks]

Turn 4 - You: Add error handling for network failures
Turn 4 - Claude: [Updates code with error handling]
```

### Research & Learning
```bash
shannon interactive

Turn 1 - You: Explain how async/await works in Python
Turn 1 - Claude: [Explains async fundamentals]

Turn 2 - You: Show me an example with file I/O
Turn 2 - Claude: [Provides async file I/O example]

Turn 3 - You: How would I handle errors in that example?
Turn 3 - Claude: [Adds error handling to previous example]
```

## Architecture

### ClaudeSDKClient vs query()

**Traditional Commands** (`query()`):
```python
# Each call creates NEW session
async for msg in query(prompt="Task 1", options=...):
    process(msg)

# This is a DIFFERENT session - no memory
async for msg in query(prompt="Task 2", options=...):
    process(msg)
```

**Interactive Mode** (`ClaudeSDKClient`):
```python
# Single session maintained across multiple queries
async with ClaudeSDKClient(options=...) as client:
    # Turn 1
    await client.query("Task 1")
    async for msg in client.receive_response():
        process(msg)
    
    # Turn 2 - SAME session, remembers Task 1
    await client.query("Task 2")
    async for msg in client.receive_response():
        process(msg)
```

### Session Lifecycle

```
┌─────────────────────────────────────────┐
│ Start Interactive Session               │
│ shannon interactive                     │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ Connect to Claude                       │
│ ClaudeSDKClient.connect()              │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ Conversation Loop                       │
│                                         │
│  1. User sends message                  │
│  2. Claude processes (with context)     │
│  3. Streams response                    │
│  4. Updates conversation history        │
│  5. Repeat                             │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ Disconnect & Cleanup                    │
│ ClaudeSDKClient.disconnect()           │
└─────────────────────────────────────────┘
```

## Message Types

Interactive mode handles all Claude SDK message types:

### TextBlock
```python
if isinstance(msg, TextBlock):
    print(msg.text)  # Regular text response
```

### ThinkingBlock (with --show-thinking)
```python
if isinstance(msg, ThinkingBlock):
    print(f"Thinking: {msg.thinking}")  # Claude's reasoning process
```

### ToolUseBlock
```python
if isinstance(msg, ToolUseBlock):
    print(f"Using tool: {msg.name}")  # Tool invocation
```

### ResultMessage
```python
if isinstance(msg, ResultMessage):
    print(f"Cost: ${msg.total_cost_usd}")  # Final stats
    print(f"Duration: {msg.duration_ms}ms")
```

## Configuration

### SDK Options (Automatic)
Interactive mode automatically configures:

- ✅ `include_partial_messages=True` - Character-by-character streaming
- ✅ `max_turns=50` - Prevent runaway costs
- ✅ `hooks` - Tool-level monitoring
- ✅ `stderr` callback - Integrated logging
- ✅ All Shannon Framework skills available
- ✅ MCP tools (Serena, Sequential Thinking)

### Custom Configuration
Extend via `ShannonSDKClient`:

```python
from shannon.sdk import ShannonSDKClient

client = ShannonSDKClient()
session = await client.start_interactive_session(
    enable_partial_messages=True,
    enable_thinking_display=True
)

async with session:
    await session.send("Your message")
    async for msg in session.receive():
        process(msg)
```

## Advanced Features

### Interrupts
Stop long-running operations:

```bash
You: count from 1 to 1000 slowly

[Claude starts counting...]

You: interrupt

[Operation stops]

You: just say hello instead

Claude: Hello!
```

### Session Statistics
```bash
You: stats

Session Statistics:
  Turns: 5
  Active: True
```

### Error Handling

Interactive mode provides detailed error messages:

```
❌ Claude Code CLI not found
   Install with: npm install -g @anthropic-ai/claude-code

❌ Process failed with exit code 1
   Error: [detailed stderr output]

❌ Connection failed
   [connection details]
```

## Performance

### Streaming Performance
- **Partial messages**: Character-by-character display (~instant)
- **Full blocks**: Wait for complete blocks (~1-2s latency)

### Memory Usage
- Session maintains conversation history in memory
- Use `exit` to free resources when done
- Long sessions may accumulate significant context

### Cost Tracking
Every turn shows cost:
```
Cost: $0.0045, Duration: 1234ms
```

## Best Practices

### ✅ DO
- Use interactive mode for exploratory workflows
- Take advantage of context preservation
- Use natural follow-up questions
- Monitor costs with `stats` command
- Exit sessions when done to free resources

### ❌ DON'T
- Use interactive mode for simple one-off tasks (use regular commands)
- Create multiple concurrent interactive sessions (high cost)
- Keep sessions open indefinitely (memory growth)
- Skip monitoring costs on long sessions

## Comparison with Other Modes

| Feature | Interactive | Regular Commands | Dashboard |
|---------|-------------|------------------|-----------|
| **Context Memory** | ✅ Yes | ❌ No | ❌ No |
| **Multi-turn** | ✅ Yes | ❌ No | ⚠️ Limited |
| **Streaming** | ✅ Character-level | ✅ Block-level | ✅ Real-time |
| **Cost per task** | Higher (context) | Lower (single) | Varies |
| **Use case** | Exploration | Automation | Monitoring |

## Examples

### Code Review Session
```bash
shannon interactive

You: Read the auth module and identify security issues
Claude: [Analyzes auth code...]

You: Show me the password hashing implementation
Claude: [Shows specific code, remembers review context]

You: Is bcrypt properly configured?
Claude: [Checks bcrypt config based on code shown]

You: Generate fixes for the issues you found
Claude: [Creates fixes addressing all identified issues]
```

### Learning Session
```bash
shannon interactive --show-thinking

You: Explain dependency injection
Claude: [Explains DI concept]
[Thinking: User needs practical understanding...]

You: Show me an example in Python
Claude: [Provides Python DI example]

You: How would I test that code?
Claude: [Shows test examples using DI pattern]
```

## Troubleshooting

### Session Won't Start
```bash
# Check Claude Code installation
npm list -g @anthropic-ai/claude-code

# Reinstall if needed
npm install -g @anthropic-ai/claude-code
```

### Slow Responses
```bash
# Disable partial messages
shannon interactive --no-partial

# Or check network connection
ping api.anthropic.com
```

### Memory Issues
```bash
# Exit and restart session periodically
You: exit

# Start new session
shannon interactive
```

## Integration with Shannon Framework

Interactive mode has full access to Shannon Framework skills:

```bash
You: @skill spec-analysis < analyze requirements.md
You: @skill task-decomposition "build authentication system"
You: /shannon:wave orchestrate the implementation
```

All skills maintain context across turns!

## Summary

Interactive mode transforms Shannon from a task executor into a **conversational coding partner**:

- 🧠 **Remembers context** - Follow-up questions work naturally
- ⚡ **Real-time streaming** - See responses as they're generated
- 🔍 **Thinking display** - Understand Claude's reasoning
- 🛠️ **Full tool access** - All Shannon skills and MCP tools
- 🎯 **Interrupt support** - Stop and redirect mid-execution

Perfect for:
- Exploratory development
- Learning and research
- Iterative refinement
- Complex multi-step tasks
- Code review and analysis

