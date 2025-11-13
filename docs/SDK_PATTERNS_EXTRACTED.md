# SDK Patterns Extracted from Official Docs

**Source**: 12 SDK documentation files (2,367 lines total)
**Date**: 2025-11-09
**Version**: claude-agent-sdk 0.1.6
**Status**: Complete extraction from verified official documentation

---

## CRITICAL REQUIREMENT #1: setting_sources

**From agent-sdk-skills.md lines 16, agent-sdk-overview.md line 41, agent-sdk-python-api-reference.md line 510**

### The Default Behavior

```python
# Default SDK behavior (setting_sources=None):
options = ClaudeAgentOptions()
# Result: NO filesystem loading
# - plugins = []
# - skills = []
# - commands = [] (only built-in)
# - CLAUDE.md NOT loaded
```

### The Required Configuration

```python
# To load plugins, skills, commands, CLAUDE.md:
options = ClaudeAgentOptions(
    setting_sources=["user", "project"],  # REQUIRED for filesystem loading
    plugins=[{"type": "local", "path": "./my-plugin"}]
)
# Result: Everything loads correctly
# - plugins loaded from path
# - skills from .claude/skills/ and ~/.claude/skills/
# - commands from .claude/commands/ and ~/.claude/commands/
# - CLAUDE.md loaded from project
```

### setting_sources Values

**From agent-sdk-python-api-reference.md lines 534-541:**

| Value | Location | Description |
|-------|----------|-------------|
| `"user"` | `~/.claude/settings.json` | Global user settings |
| `"project"` | `.claude/settings.json` | Project settings (version controlled) |
| `"local"` | `.claude/settings.local.json` | Local settings (gitignored) |

### Precedence (agent-sdk-python-api-reference.md lines 626-634)

When multiple sources loaded, settings merge with precedence:
1. Local settings (highest)
2. Project settings
3. User settings (lowest)

Programmatic options always override filesystem settings.

---

## CRITICAL REQUIREMENT #2: Message Type Checking

**From agent-sdk-python-api-reference.md lines 742-800**

### Message Type System

```python
# Message union type (line 749)
Message = UserMessage | AssistantMessage | SystemMessage | ResultMessage

# AssistantMessage dataclass (lines 767-771)
@dataclass
class AssistantMessage:
    content: list[ContentBlock]  # List of content blocks
    model: str

# SystemMessage dataclass (lines 777-782)
@dataclass
class SystemMessage:
    subtype: str  # 'init', 'completion', etc.
    data: dict[str, Any]

# ResultMessage dataclass (lines 788-800)
@dataclass
class ResultMessage:
    subtype: str
    duration_ms: int
    duration_api_ms: int
    is_error: bool
    num_turns: int
    session_id: str
    total_cost_usd: float | None = None
    usage: dict[str, Any] | None = None
    result: str | None = None
```

### WRONG Pattern (Old Skill)

```python
# ❌ WRONG - Messages don't have .type attribute
if message.type == 'assistant':
    print(message.content)  # content is list, not string!
```

### CORRECT Pattern

```python
# ✅ CORRECT - Use isinstance() checks
if isinstance(message, AssistantMessage):
    for block in message.content:  # Iterate content blocks
        if isinstance(block, TextBlock):
            print(block.text)  # Access text from block
```

---

## CRITICAL REQUIREMENT #3: Content Block Iteration

**From agent-sdk-python-api-reference.md lines 804-855**

### Content Block Type System

```python
# Content block union (line 809)
ContentBlock = TextBlock | ThinkingBlock | ToolUseBlock | ToolResultBlock

# TextBlock (lines 817-820)
@dataclass
class TextBlock:
    text: str

# ThinkingBlock (lines 826-831)
@dataclass
class ThinkingBlock:
    thinking: str
    signature: str

# ToolUseBlock (lines 837-843)
@dataclass
class ToolUseBlock:
    id: str
    name: str  # Tool name: "Write", "Bash", "Task", "Skill", etc.
    input: dict[str, Any]  # Tool parameters

# ToolResultBlock (lines 849-855)
@dataclass
class ToolResultBlock:
    tool_use_id: str
    content: str | list[dict[str, Any]] | None = None
    is_error: bool | None = None
```

### Text Extraction Pattern

```python
# From lines 76-94
text_parts = []

async for message in query(prompt="Hello", options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:  # content is list[ContentBlock]
            if isinstance(block, TextBlock):
                text_parts.append(block.text)

output = ''.join(text_parts)
```

### Tool Tracking Pattern

```python
# Extract which tools Claude used
tools_used = []

async for message in query(prompt="...", options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                tools_used.append({
                    'tool': block.name,
                    'input': block.input,
                    'id': block.id
                })

print(f"Tools called: {[t['tool'] for t in tools_used]}")
```

---

## Plugin Loading Pattern

**From agent-sdk-plugins.md lines 9-27**

```python
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    options = ClaudeAgentOptions(
        plugins=[
            {"type": "local", "path": "./my-plugin"},
            {"type": "local", "path": "/absolute/path/to/plugin"}
        ],
        setting_sources=["user", "project"]  # REQUIRED!
    )

    async for message in query(prompt="Hello", options=options):
        pass
```

### Plugin Verification Pattern

**From agent-sdk-plugins.md lines 32-47**

```python
async for message in query(prompt="Hello", options=options):
    if isinstance(message, SystemMessage) and message.subtype == 'init':
        plugins = message.data.get('plugins', [])
        commands = message.data.get('slash_commands', [])
        print(f"Loaded: {len(plugins)} plugins")
        print(f"Commands: {commands}")
```

**Expected when working:**
- `plugins`: Non-empty list with plugin metadata
- `slash_commands`: Includes plugin commands (e.g., `/plugin-name:command`)

**When broken (missing setting_sources):**
- `plugins`: `[]` (empty)
- `slash_commands`: Only built-in commands

---

## query() vs ClaudeSDKClient

**From agent-sdk-python-api-reference.md lines 11-47**

### Comparison Table (lines 17-27)

| Feature | `query()` | `ClaudeSDKClient` |
|---------|-----------|-------------------|
| Session | New each time | Reuses same session |
| Conversation | Single exchange | Multiple in context |
| Interrupts | ❌ | ✅ |
| Hooks | ❌ | ✅ |
| Custom Tools | ❌ | ✅ |
| Continue Chat | ❌ | ✅ |

### When to Use query() (lines 29-36)

- One-off questions
- Independent tasks
- Simple automation
- Fresh start each time

### When to Use ClaudeSDKClient (lines 38-46)

- Continuing conversations
- Follow-up questions
- Interactive applications
- Response-driven logic
- Session control

---

## Complete Working Examples

### Example 1: Basic query() with Plugin

**From agent-sdk-plugins.md lines 10-27**

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./my-plugin"}],
        setting_sources=["user", "project"],  # Required!
        permission_mode="bypassPermissions"
    )

    async for message in query(prompt="Hello", options=options):
        print(message)

asyncio.run(main())
```

### Example 2: Text Extraction

**From agent-sdk-python-api-reference.md lines 76-94**

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock

async def get_response_text(prompt: str) -> str:
    text_parts = []

    async for message in query(prompt=prompt, options=ClaudeAgentOptions()):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    text_parts.append(block.text)

    return ''.join(text_parts)
```

### Example 3: Tool Usage Tracking

**From agent-sdk-python-api-reference.md (implied from ToolUseBlock definition)**

```python
from claude_agent_sdk import query, AssistantMessage, ToolUseBlock

tools_called = []

async for message in query(prompt="Create a Python file", options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                tools_called.append({
                    'tool': block.name,
                    'input': block.input,
                    'id': block.id
                })

print(f"Tools used: {[t['tool'] for t in tools_called]}")
```

### Example 4: Cost and Usage Tracking

**From agent-sdk-python-api-reference.md (ResultMessage pattern)**

```python
from claude_agent_sdk import query, ResultMessage

cost = 0.0
session_id = None

async for message in query(prompt="...", options=options):
    # Process messages...

    if isinstance(message, ResultMessage):
        cost = message.total_cost_usd or 0.0
        session_id = message.session_id
        duration_sec = message.duration_ms / 1000

        if message.usage:
            print(f"Tokens: {message.usage}")

        print(f"Cost: ${cost:.4f}")
        print(f"Duration: {duration_sec:.1f}s")
```

### Example 5: ClaudeSDKClient Continuous Conversation

**From agent-sdk-python-api-reference.md lines 268-305**

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient, AssistantMessage, TextBlock

async def main():
    async with ClaudeSDKClient() as client:
        # First question
        await client.query("What's the capital of France?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

        # Follow-up - Claude remembers context!
        await client.query("What's the population of that city?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

asyncio.run(main())
```

### Example 6: Hook Integration

**From agent-sdk-python-api-reference.md lines 979-1029**

```python
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher, HookContext
from typing import Any

async def validate_bash_command(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    """Validate and block dangerous bash commands."""
    if input_data['tool_name'] == 'Bash':
        command = input_data['tool_input'].get('command', '')
        if 'rm -rf /' in command:
            return {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'permissionDecision': 'deny',
                    'permissionDecisionReason': 'Dangerous command blocked'
                }
            }
    return {}

options = ClaudeAgentOptions(
    hooks={
        'PreToolUse': [
            HookMatcher(matcher='Bash', hooks=[validate_bash_command])
        ]
    },
    allowed_tools=["Bash", "Read", "Write"]
)

async for message in query(prompt="...", options=options):
    print(message)
```

### Example 7: Custom Tools

**From agent-sdk-custom-tools.md lines 20-40**

```python
from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeAgentOptions

@tool("get_weather", "Get temperature for location",
      {"latitude": float, "longitude": float})
async def get_weather(args: dict[str, Any]) -> dict[str, Any]:
    temp = 72  # Mock implementation
    return {
        "content": [{
            "type": "text",
            "text": f"Temperature: {temp}°F"
        }]
    }

server = create_sdk_mcp_server(
    name="weather",
    version="1.0.0",
    tools=[get_weather]
)

options = ClaudeAgentOptions(
    mcp_servers={"weather": server},
    allowed_tools=["mcp__weather__get_weather"]
)
```

### Example 8: Session Management

**From agent-sdk-sessions.md lines 10-24**

```python
from claude_agent_sdk import query, ClaudeAgentOptions

session_id = None

async for message in query(
    prompt="Help me build a web application",
    options=ClaudeAgentOptions(model="claude-sonnet-4-5")
):
    if hasattr(message, 'subtype') and message.subtype == 'init':
        session_id = message.data.get('session_id')
        print(f"Session: {session_id}")

# Later, resume session:
async for message in query(
    prompt="Continue implementing authentication",
    options=ClaudeAgentOptions(resume=session_id)
):
    print(message)
```

---

## Common Error Patterns

### Error 1: Missing setting_sources

**Symptom:**
```python
# plugins: [] (empty)
# commands: ['/compact', '/clear', ...] (built-in only)
# Shannon commands missing
```

**Cause:**
```python
options = ClaudeAgentOptions(
    plugins=[{"type": "local", "path": "./shannon-plugin"}]
    # Missing: setting_sources!
)
```

**Fix:**
```python
options = ClaudeAgentOptions(
    plugins=[{"type": "local", "path": "./shannon-plugin"}],
    setting_sources=["user", "project"]  # Add this!
)
```

### Error 2: Using .type Attribute

**Symptom:**
```python
AttributeError: 'AssistantMessage' object has no attribute 'type'
```

**Cause:**
```python
if message.type == 'assistant':  # Wrong!
    ...
```

**Fix:**
```python
if isinstance(message, AssistantMessage):  # Correct!
    ...
```

### Error 3: Not Iterating Content Blocks

**Symptom:**
```python
TypeError: 'list' object has no attribute 'text'
```

**Cause:**
```python
if isinstance(message, AssistantMessage):
    print(message.content)  # content is list, not string!
```

**Fix:**
```python
if isinstance(message, AssistantMessage):
    for block in message.content:  # Iterate blocks
        if isinstance(block, TextBlock):
            print(block.text)  # Get text from block
```

### Error 4: API Key Not Set

**Symptom:**
```python
CLIConnectionError: Authentication failed
```

**Cause:**
```python
from claude_agent_sdk import query  # API key not set

async for message in query(prompt="Hello"):
    ...
```

**Fix:**
```python
import os
os.environ['ANTHROPIC_API_KEY'] = "sk-ant-..."  # Set BEFORE import

from claude_agent_sdk import query

async for message in query(prompt="Hello"):
    ...
```

---

## Permission Modes

**From agent-sdk-python-api-reference.md lines 656-667**

```python
PermissionMode = Literal[
    "default",           # Standard permission behavior
    "acceptEdits",       # Auto-accept file edits
    "plan",              # Planning mode - no execution
    "bypassPermissions"  # Bypass all permission checks (testing)
]
```

### Testing Pattern

```python
# For automated testing - bypass permission prompts
options = ClaudeAgentOptions(
    permission_mode="bypassPermissions",
    allowed_tools=["Read", "Write", "Bash"]
)
```

---

## Tool Names and allowedTools

**From agent-sdk-python-api-reference.md lines 456, tool schemas throughout**

### Built-in Tools

```python
options = ClaudeAgentOptions(
    allowed_tools=[
        "Read",           # Read files
        "Write",          # Write files
        "Edit",           # Edit files
        "Bash",           # Execute shell commands
        "Glob",           # File pattern matching
        "Grep",           # Content search
        "Task",           # Spawn subagents
        "Skill",          # Invoke skills (requires setting_sources!)
        "TodoWrite",      # Manage todos
        "WebFetch",       # Fetch URLs
        "WebSearch",      # Search web
        # ... more tools
    ]
)
```

### MCP Tool Naming

```python
# MCP tools follow pattern: mcp__{server}__{tool}
allowed_tools=[
    "mcp__weather__get_weather",
    "mcp__github__create_issue"
]
```

---

## Message Flow Patterns

### Pattern 1: Init → Messages → Result

```python
async for message in query(prompt="...", options=options):
    # First message: SystemMessage with subtype='init'
    if isinstance(message, SystemMessage) and message.subtype == 'init':
        print(f"Session: {message.data['session_id']}")
        print(f"Plugins: {message.data['plugins']}")

    # Content messages: AssistantMessage with content blocks
    elif isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(block.text)
            elif isinstance(block, ToolUseBlock):
                print(f"Using: {block.name}")

    # Final message: ResultMessage with cost/usage
    elif isinstance(message, ResultMessage):
        print(f"Cost: ${message.total_cost_usd:.4f}")
        print(f"Duration: {message.duration_ms}ms")
```

### Pattern 2: Progress Monitoring

**From agent-sdk-python-api-reference.md lines 1637-1681**

```python
async for message in client.receive_messages():
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                print(f"🔨 Using: {block.name}")
            elif isinstance(block, ToolResultBlock):
                print(f"✅ Completed")
            elif isinstance(block, TextBlock):
                print(f"💭 Claude: {block.text[:100]}")
```

---

## ClaudeAgentOptions Complete Configuration

**From agent-sdk-python-api-reference.md lines 449-481**

```python
@dataclass
class ClaudeAgentOptions:
    # Tool Control
    allowed_tools: list[str] = field(default_factory=list)
    disallowed_tools: list[str] = field(default_factory=list)

    # System Prompt
    system_prompt: str | SystemPromptPreset | None = None

    # MCP Servers
    mcp_servers: dict[str, McpServerConfig] | str | Path = field(default_factory=dict)

    # Permissions
    permission_mode: PermissionMode | None = None
    can_use_tool: CanUseTool | None = None

    # Session Management
    continue_conversation: bool = False
    resume: str | None = None
    max_turns: int | None = None

    # Model Selection
    model: str | None = None

    # Working Directory
    cwd: str | Path | None = None
    add_dirs: list[str | Path] = field(default_factory=list)

    # Settings Loading (CRITICAL!)
    settings: str | None = None
    setting_sources: list[SettingSource] | None = None  # Required for plugins/skills!

    # Environment
    env: dict[str, str] = field(default_factory=dict)
    extra_args: dict[str, str | None] = field(default_factory=dict)

    # Advanced
    max_buffer_size: int | None = None
    stderr: Callable[[str], None] | None = None
    hooks: dict[HookEvent, list[HookMatcher]] | None = None
    user: str | None = None
    include_partial_messages: bool = False
    fork_session: bool = False

    # Programmatic Configuration
    agents: dict[str, AgentDefinition] | None = None
    plugins: list[SdkPluginConfig] = field(default_factory=list)
```

---

## SystemPromptPreset Pattern

**From agent-sdk-python-api-reference.md lines 512-521, agent-sdk-modifying-prompts.md**

```python
# Use Claude Code's system prompt
options = ClaudeAgentOptions(
    system_prompt={
        "type": "preset",
        "preset": "claude_code"
    },
    setting_sources=["project"]  # Required to load CLAUDE.md!
)

# Extend Claude Code's prompt
options = ClaudeAgentOptions(
    system_prompt={
        "type": "preset",
        "preset": "claude_code",
        "append": "Additional custom instructions here."
    }
)

# Custom system prompt (replace entirely)
options = ClaudeAgentOptions(
    system_prompt="You are a specialized assistant for..."
)
```

---

## Error Handling Patterns

**From agent-sdk-python-api-reference.md lines 857-916, 1710-1729**

```python
from claude_agent_sdk import (
    query,
    CLINotFoundError,
    ProcessError,
    CLIJSONDecodeError
)

try:
    async for message in query(prompt="Hello"):
        print(message)

except CLINotFoundError as e:
    print(f"CLI not found: {e}")
    print("Install: npm install -g @anthropic-ai/claude-code")

except ProcessError as e:
    print(f"Process failed: exit code {e.exit_code}")
    print(f"Stderr: {e.stderr}")

except CLIJSONDecodeError as e:
    print(f"JSON parse error: {e.line}")
    print(f"Original error: {e.original_error}")
```

---

## Subagent Patterns

**From agent-sdk-subagents.md lines 14-30**

```python
# Programmatic subagent definition
options = ClaudeAgentOptions(
    agents={
        'code-reviewer': {
            'description': 'Expert code review specialist',
            'prompt': 'You are a code reviewer focused on security and performance...',
            'tools': ['Read', 'Grep', 'Glob'],
            'model': 'sonnet'
        },
        'test-writer': {
            'description': 'Test automation expert',
            'prompt': 'You write comprehensive test suites...',
            'tools': ['Read', 'Write'],
            'model': 'haiku'
        }
    }
)

# Claude will spawn these agents via Task tool when appropriate
async for message in query(
    prompt="Review and test the authentication module",
    options=options
):
    print(message)
```

---

## Complete Test Template

**Synthesis of all patterns into production-ready test script:**

```python
#!/usr/bin/env python3
"""
Complete SDK test pattern - all verified patterns from official docs

Tests Shannon plugin loading and command execution via Claude Agents SDK.
"""

import os
import sys
import asyncio
from pathlib import Path

# STEP 1: Set API key BEFORE importing SDK
os.environ['ANTHROPIC_API_KEY'] = "sk-ant-..."

# STEP 2: Import SDK types
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    SystemMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    ToolResultBlock
)

async def test_shannon_plugin():
    """Test Shannon plugin via SDK with all correct patterns."""

    print("=" * 80)
    print("Testing Shannon Plugin via Claude Agents SDK")
    print("=" * 80)

    # STEP 3: Configure options with ALL requirements
    options = ClaudeAgentOptions(
        # Plugin loading
        plugins=[{"type": "local", "path": "./shannon-plugin"}],

        # CRITICAL: Required for filesystem loading
        setting_sources=["user", "project"],

        # Permissions for testing
        permission_mode="bypassPermissions",

        # Tools allowed
        allowed_tools=["Skill", "Read", "Write", "Bash", "TodoWrite"],

        # Working directory
        cwd=str(Path.cwd())
    )

    # STEP 4: Read specification
    spec_file = Path("docs/ref/prd-creator-spec.md")
    spec_text = spec_file.read_text()

    print(f"\nSpec: {spec_file.name} ({len(spec_text):,} bytes)")
    print("Executing: /shannon:spec\n")

    # STEP 5: Execute command and track everything
    text_output = []
    tools_used = []
    skills_invoked = []
    cost = 0.0
    session_id = None
    plugins_loaded = []

    async for message in query(prompt=f'/shannon:spec "{spec_text}"', options=options):
        # Handle SystemMessage (init)
        if isinstance(message, SystemMessage):
            if message.subtype == 'init':
                session_id = message.data.get('session_id')
                plugins_loaded = message.data.get('plugins', [])
                commands = message.data.get('slash_commands', [])

                print(f"Session: {session_id}")
                print(f"Plugins loaded: {len(plugins_loaded)}")
                print(f"Commands available: {len(commands)}")

                # Verify Shannon loaded
                shannon_commands = [c for c in commands if c.startswith('/shannon:')]
                print(f"Shannon commands: {len(shannon_commands)}")
                print()

        # Handle AssistantMessage (content)
        elif isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    text_output.append(block.text)
                    print(".", end="", flush=True)

                elif isinstance(block, ToolUseBlock):
                    tools_used.append(block.name)
                    if block.name == "Skill":
                        skill_name = block.input.get('skill', 'unknown')
                        skills_invoked.append(skill_name)

        # Handle ResultMessage (final)
        elif isinstance(message, ResultMessage):
            cost = message.total_cost_usd or 0.0
            duration_sec = message.duration_ms / 1000

            print(f"\n\n{'='*80}")
            print(f"Execution Complete")
            print(f"{'='*80}")
            print(f"Duration: {duration_sec:.1f}s")
            print(f"Cost: ${cost:.4f}")
            print(f"Tools used: {len(tools_used)} ({len(set(tools_used))} unique)")
            print(f"Skills invoked: {skills_invoked}")

    # STEP 6: Validate results
    output = ''.join(text_output)

    print(f"\n{'='*80}")
    print("Validation")
    print(f"{'='*80}")

    checks = [
        ("Plugin loaded", len(plugins_loaded) > 0),
        ("Shannon commands available", len(shannon_commands) > 0),
        ("Has output", len(output) > 0),
        ("Contains 'Complexity'", "Complexity" in output),
        ("Contains 'Domain'", "Domain" in output),
        ("Skills invoked", len(skills_invoked) > 0),
        ("spec-analysis used", "spec-analysis" in skills_invoked)
    ]

    passed = 0
    for name, result in checks:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
        if result:
            passed += 1

    print(f"\n{passed}/{len(checks)} checks passed")

    # Return exit code
    return 0 if passed == len(checks) else 1

if __name__ == '__main__':
    sys.exit(asyncio.run(test_shannon_plugin()))
```

---

## Quick Reference: Most Common Patterns

### 1. Basic Query with Plugin

```python
options = ClaudeAgentOptions(
    plugins=[{"type": "local", "path": "./plugin"}],
    setting_sources=["user", "project"],  # Required!
    permission_mode="bypassPermissions"
)

async for message in query(prompt="/command", options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(block.text)
```

### 2. Extract Text Response

```python
text = []
async for message in query(prompt="...", options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                text.append(block.text)

output = ''.join(text)
```

### 3. Track Cost

```python
cost = 0.0
async for message in query(prompt="...", options=options):
    if isinstance(message, ResultMessage):
        cost = message.total_cost_usd or 0.0
print(f"${cost:.4f}")
```

### 4. Track Tools Used

```python
tools = []
async for message in query(prompt="...", options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                tools.append(block.name)
print(f"Tools: {tools}")
```

### 5. Verify Plugin Loaded

```python
async for message in query(prompt="...", options=options):
    if isinstance(message, SystemMessage) and message.subtype == 'init':
        plugins = message.data.get('plugins', [])
        if len(plugins) == 0:
            print("❌ Plugin not loaded - check setting_sources!")
        else:
            print(f"✅ Loaded: {plugins}")
```

---

## References to Line Numbers in Source Docs

### agent-sdk-python-api-reference.md (1,847 lines)
- Lines 11-47: query() vs ClaudeSDKClient comparison
- Lines 54-95: query() function definition and example
- Lines 219-373: ClaudeSDKClient class and examples
- Lines 449-511: ClaudeAgentOptions complete definition
- Lines 510: setting_sources definition ⭐ CRITICAL
- Lines 529-635: SettingSource, precedence, examples
- Lines 656-667: PermissionMode types
- Lines 742-800: Message types (AssistantMessage, SystemMessage, ResultMessage)
- Lines 804-855: Content block types
- Lines 857-916: Error types
- Lines 979-1029: Hook example

### agent-sdk-skills.md (65 lines)
- Line 16: setting_sources requirement ⭐ CRITICAL
- Lines 22-40: Configuration example
- Lines 54-65: Troubleshooting (missing setting_sources)

### agent-sdk-plugins.md (117 lines)
- Lines 9-27: Loading pattern
- Lines 32-47: Verification pattern
- Lines 68-108: Complete example

### agent-sdk-overview.md (41 lines)
- Line 41: setting_sources requirement ⭐ CRITICAL
- Lines 33-40: Claude Code feature support

### agent-sdk-modifying-prompts.md (21 lines)
- Line 8: CLAUDE.md requires setting_sources
- Line 21: claude_code preset doesn't auto-load CLAUDE.md

---

## SDK Version Information

**Package**: claude-agent-sdk
**Version**: 0.1.6 (latest as of 2025-11-09)
**Install**: `pip install claude-agent-sdk`
**Docs**: https://code.claude.com/docs/agent-sdk

---

**EXTRACTION COMPLETE - All patterns documented with source references**
