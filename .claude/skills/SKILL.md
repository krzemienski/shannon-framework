---
name: testing-claude-plugins-with-python-sdk
description: Use when working with Claude Agents SDK (Python) - covers plugin loading, session management, streaming messages, monitoring long-running operations, and real-time progress tracking. Essential for testing Claude Code plugins, building autonomous agents, or programmatic Claude Code interaction.
---

# Testing Claude Plugins With Python SDK

## Overview

Complete reference for Claude Agents SDK (Python) covering plugin loading, session management, message streaming, and monitoring long-running operations.

**Use this skill when**:
- Loading Claude Code plugins programmatically
- Testing plugin functionality via SDK
- Building autonomous agents with SDK
- Monitoring long-running Claude operations
- Streaming real-time progress from Claude
- Managing sessions and resumption

## Quick Start (5 Minutes)

### 1. Install SDK

```bash
pip install claude-agent-sdk
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 2. Basic Query

```python
from claude_agent_sdk import query

async for message in query(prompt="Hello Claude"):
    if message.type == 'assistant':
        print(message.content)
```

### 3. Load Plugin

```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="/my-plugin:command",
    options=ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./my-plugin"}]
    )
):
    print(message)
```

---

## Complete SDK Reference

### 1. Plugin Loading

**Purpose**: Load Claude Code plugins programmatically to test or extend functionality

**Configuration**:

```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    plugins=[
        {"type": "local", "path": "./my-plugin"},           # Relative path
        {"type": "local", "path": "/absolute/path/plugin"}  # Absolute path
    ]
)
```

**Requirements**:
- Path must point to plugin root directory (containing `.claude-plugin/plugin.json`)
- Plugin must have valid `plugin.json` manifest
- Can load multiple plugins simultaneously

**Verification**:

```python
async for message in query(prompt="test", options=options):
    if message.type == 'system' and message.subtype == 'init':
        print("Loaded plugins:", message.plugins)
        print("Available commands:", message.slash_commands)
```

**Example**: Loading Shannon Framework plugin

```python
options = ClaudeAgentOptions(
    plugins=[{"type": "local", "path": "./shannon-plugin"}]
)

async for msg in query(prompt="/sh_spec 'Build React app'", options=options):
    # Shannon plugin's /sh_spec command executes
    pass
```

---

### 2. Session Management

**Purpose**: Resume conversations, maintain context across multiple queries

**Starting Session**:

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

session_id = None

async with ClaudeSDKClient(options=options) as client:
    await client.query("First question")

    async for msg in client.receive_messages():
        if msg.type == 'system' and msg.subtype == 'init':
            session_id = msg.session_id  # Capture session ID
            print(f"Session: {session_id}")
```

**Resuming Session**:

```python
# Continue same conversation
async with ClaudeSDKClient(options=options) as client:
    await client.query(
        "Follow-up question",
        resume=session_id  # Resume previous session
    )

    async for msg in client.receive_messages():
        # Claude has full context from previous session
        pass
```

**Forking Session**:

```python
# Explore alternative without modifying original
await client.query(
    "Try different approach",
    resume=session_id,
    fork_session=True  # Create branch
)
```

**Use Cases**:
- **Resume**: Continue long-running work across restarts
- **Fork**: Try alternatives without losing original path
- **Testing**: Create session, test behavior, resume to verify state

---

### 3. Message Streaming and Types

**Purpose**: Monitor real-time progress, parse different message types

**Message Types**:

```python
from claude_agent_sdk import (
    SystemMessage,    # Init, completion events
    AssistantMessage, # Claude's responses
    ToolCallMessage,  # Tool execution requests
    ToolResultMessage,# Tool execution results
    ErrorMessage      # Errors and failures
)
```

**Streaming Pattern**:

```python
async for message in query(prompt="Long task", options=options):

    if message.type == 'system':
        # System events (init, completion)
        if message.subtype == 'init':
            print(f"Session: {message.session_id}")
            print(f"Model: {message.model}")
        elif message.subtype == 'completion':
            print("Task complete")

    elif message.type == 'assistant':
        # Claude's text responses
        print(f"Claude: {message.content}")

    elif message.type == 'tool_call':
        # Tool about to execute
        print(f"Calling tool: {message.tool_name}")
        print(f"Input: {message.input}")

    elif message.type == 'tool_result':
        # Tool completed
        print(f"Tool {message.tool_name} completed")
        print(f"Result: {message.result}")

    elif message.type == 'error':
        # Errors
        print(f"Error: {message.error.message}")
```

**Real-Time Monitoring**:

```python
import time

start_time = time.time()
tool_calls = []

async for message in query(prompt="Complex task", options=options):
    elapsed = time.time() - start_time

    if message.type == 'tool_call':
        tool_calls.append({
            'tool': message.tool_name,
            'timestamp': elapsed,
            'input': message.input
        })
        print(f"[{elapsed:.1f}s] Tool: {message.tool_name}")

    elif message.type == 'assistant':
        print(f"[{elapsed:.1f}s] Progress: {message.content[:80]}...")

print(f"Total time: {elapsed:.1f}s")
print(f"Tool calls: {len(tool_calls)}")
```

---

### 4. Long-Running Operations

**Purpose**: Monitor operations that take minutes/hours (builds, analyses, multi-step workflows)

**Progress Tracking Pattern**:

```python
import asyncio
from datetime import datetime

async def monitor_long_operation(prompt: str, options: ClaudeAgentOptions):
    """
    Monitor long-running operation with progress updates
    """
    start = datetime.now()
    messages_received = 0
    tools_executed = 0
    current_activity = "Starting..."

    print(f"Started: {start.strftime('%H:%M:%S')}")
    print("-" * 80)

    async for message in query(prompt=prompt, options=options):
        messages_received += 1

        if message.type == 'tool_call':
            tools_executed += 1
            current_activity = f"Tool: {message.tool_name}"

            elapsed = (datetime.now() - start).total_seconds()
            print(f"[{elapsed:6.1f}s] {current_activity}")

        elif message.type == 'assistant':
            # Update current activity from message
            preview = message.content[:60]
            if preview:
                current_activity = preview
                elapsed = (datetime.now() - start).total_seconds()
                print(f"[{elapsed:6.1f}s] {current_activity}...")

    total_time = (datetime.now() - start).total_seconds()

    print("-" * 80)
    print(f"Completed: {datetime.now().strftime('%H:%M:%S')}")
    print(f"Duration: {total_time/60:.1f} minutes")
    print(f"Messages: {messages_received}")
    print(f"Tools: {tools_executed}")

# Usage
await monitor_long_operation(
    "/plugin:complex-command with long execution",
    options
)
```

**Timeout Handling**:

```python
async def with_timeout(prompt: str, timeout_seconds: int = 600):
    """Execute with timeout (default 10 minutes)"""

    try:
        async with asyncio.timeout(timeout_seconds):
            async for msg in query(prompt=prompt, options=options):
                # Process messages
                pass
    except asyncio.TimeoutError:
        print(f"Operation timed out after {timeout_seconds}s")
        # Handle timeout
```

---

### 5. Permissions and Safety

**Purpose**: Control what plugins can do, prevent dangerous operations

**Permission Modes**:

```python
options = ClaudeAgentOptions(
    permission_mode="default"       # Prompt for confirmations
    # OR
    permission_mode="acceptEdits"   # Auto-approve file edits
    # OR
    permission_mode="bypassPermissions"  # Skip all checks (dangerous)
)
```

**Custom Permission Logic**:

```python
async def permission_callback(tool_name: str, tool_input: dict) -> dict:
    """
    Custom permission logic for fine-grained control

    Returns:
        {"behavior": "allow"} - Allow operation
        {"behavior": "deny", "message": "reason"} - Block operation
        {"behavior": "ask", "message": "confirm?"} - Prompt user
    """

    # Block dangerous bash commands
    if tool_name == 'Bash':
        command = tool_input.get('command', '')
        if 'rm -rf' in command or 'dd if=' in command:
            return {
                "behavior": "deny",
                "message": "Dangerous command blocked"
            }

    # Require confirmation for file writes to important files
    if tool_name in ['Write', 'Edit']:
        file_path = tool_input.get('file_path', '')
        if 'config' in file_path.lower() or '.env' in file_path:
            return {
                "behavior": "ask",
                "message": f"Modify {file_path}?"
            }

    # Allow everything else
    return {"behavior": "allow"}

# Use custom permissions
options = ClaudeAgentOptions(
    can_use_tool=permission_callback,
    allowed_tools=["Read", "Write", "Bash"]
)
```

**Restricting Tools**:

```python
# Whitelist approach (only these tools)
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Grep", "Glob"]  # Read-only
)

# Blacklist approach (everything except these)
options = ClaudeAgentOptions(
    disallowed_tools=["Bash"]  # Everything except Bash
)
```

---

### 6. Parsing and Validating Output

**Purpose**: Extract structured data from Claude's text responses

**Pattern Matching**:

```python
import re

def extract_value(text: str, pattern: str) -> str:
    """Extract value using regex pattern"""
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

# Example: Extract complexity score
output = "Complexity: 0.68 (COMPLEX)"
complexity = extract_value(output, r'Complexity:\s*([0-9.]+)')
# Returns: "0.68"

# Example: Extract all file paths
files = re.findall(r'Created:\s*(.+\.(?:py|js|md))', output)
# Returns: list of file paths
```

**Structured Extraction**:

```python
def parse_plugin_output(messages: list) -> dict:
    """
    Parse plugin command output into structured data

    Args:
        messages: List of assistant messages from SDK

    Returns:
        Extracted data as dict
    """
    output = ''.join(msg.content for msg in messages if msg.type == 'assistant')

    result = {}

    # Extract key-value pairs
    # Pattern: "Key: Value"
    for line in output.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            result[key.strip()] = value.strip()

    # Extract lists
    # Pattern: "- Item"
    list_items = re.findall(r'^\s*-\s*(.+)$', output, re.MULTILINE)
    if list_items:
        result['items'] = list_items

    return result
```

**Validation Without Pytest**:

```python
def validate_output(output: str, expected: dict) -> bool:
    """
    Validate output contains expected elements

    Returns: True if all validations pass
    """
    checks_passed = 0
    checks_total = 0

    # Check 1: Contains required text
    for required in expected.get('contains', []):
        checks_total += 1
        if required in output:
            print(f"  ✅ Contains: '{required}'")
            checks_passed += 1
        else:
            print(f"  ❌ Missing: '{required}'")

    # Check 2: Numeric ranges
    for key, (min_val, max_val) in expected.get('ranges', {}).items():
        checks_total += 1
        value = extract_value(output, rf'{key}:\s*([0-9.]+)')

        if value:
            value = float(value)
            if min_val <= value <= max_val:
                print(f"  ✅ {key}: {value} in [{min_val}, {max_val}]")
                checks_passed += 1
            else:
                print(f"  ❌ {key}: {value} outside [{min_val}, {max_val}]")
        else:
            print(f"  ❌ {key}: not found in output")

    print(f"\nValidation: {checks_passed}/{checks_total} checks passed")
    return checks_passed == checks_total

# Usage
expected = {
    'contains': ['Success', 'Complete'],
    'ranges': {'Score': (0.5, 0.8), 'Count': (1, 10)}
}

valid = validate_output(output, expected)
```

---

### 7. Configuration Options

**Complete ClaudeAgentOptions**:

```python
from claude_agent_sdk import ClaudeAgentOptions
from pathlib import Path

options = ClaudeAgentOptions(
    # Model selection
    model="claude-sonnet-4-5",  # or "haiku", "opus", "inherit"

    # Tools
    allowed_tools=["Read", "Write", "Edit", "Bash"],
    disallowed_tools=[],  # Empty means allow all (unless allowed_tools set)

    # Permissions
    permission_mode="acceptEdits",  # "default", "acceptEdits", "bypassPermissions"
    can_use_tool=custom_permission_callback,  # Optional callback

    # Plugins
    plugins=[
        {"type": "local", "path": "./plugin1"},
        {"type": "local", "path": "/abs/path/plugin2"}
    ],

    # System prompt
    system_prompt="You are a helpful assistant.",
    # Or preset:
    # system_prompt={"type": "preset", "preset": "claude_code", "append": "Extra instructions"},

    # Working directory
    cwd=str(Path("/path/to/project")),

    # Budget limits
    max_budget_usd=5.0,          # Stop after spending $5
    max_thinking_tokens=10000,   # Limit extended thinking
    max_turns=10,                # Maximum conversation turns

    # MCP servers
    mcp_servers={
        "custom": {
            "command": "python",
            "args": ["-m", "my_mcp_server"]
        }
    },

    # Settings
    setting_sources=["user", "project", "local"],  # Load from filesystem

    # Session
    fork_session="previous_session_id",  # Resume from session

    # Streaming
    include_partial_messages=True,  # Get partial updates during streaming
)
```

---

### 8. Error Handling

**Purpose**: Handle SDK errors gracefully

**Error Types**:

```python
from claude_agent_sdk import (
    ClaudeSDKError,        # Base exception
    CLINotFoundError,      # Claude Code CLI not installed
    CLIConnectionError,    # Connection failed
    ProcessError,          # Process execution failed
    CLIJSONDecodeError,    # JSON parsing failed
    MessageParseError      # Message format invalid
)
```

**Error Handling Pattern**:

```python
import asyncio

async def safe_query(prompt: str, options: ClaudeAgentOptions):
    """
    Execute query with comprehensive error handling
    """
    try:
        messages = []

        async for msg in query(prompt=prompt, options=options):
            messages.append(msg)

        return messages

    except CLINotFoundError:
        print("❌ Claude Code CLI not installed")
        print("   Install: npm install -g @anthropic-ai/claude-code")
        return None

    except CLIConnectionError as e:
        print(f"❌ Connection failed: {e}")
        print("   Check Claude Code is running")
        return None

    except ProcessError as e:
        print(f"❌ Process failed (exit code: {e.exit_code})")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return None

    except asyncio.TimeoutError:
        print("❌ Operation timed out")
        return None

    except ClaudeSDKError as e:
        print(f"❌ SDK error: {e}")
        return None

# Usage with timeout
try:
    async with asyncio.timeout(600):  # 10 minute timeout
        result = await safe_query(prompt, options)
except asyncio.TimeoutError:
    print("Operation exceeded 10 minutes")
```

---

### 9. Monitoring and Progress Tracking

**Purpose**: Track progress of long-running operations in real-time

**Progress Tracking Pattern**:

```python
class ProgressMonitor:
    """Monitor and report progress from SDK messages"""

    def __init__(self):
        self.start_time = time.time()
        self.tool_count = 0
        self.message_count = 0
        self.current_activity = "Initializing..."

    def update(self, message):
        """Update from SDK message"""
        self.message_count += 1
        elapsed = time.time() - self.start_time

        if message.type == 'tool_call':
            self.tool_count += 1
            self.current_activity = f"Tool: {message.tool_name}"
            self.report_progress(elapsed)

        elif message.type == 'assistant' and message.content:
            # Update from assistant message
            preview = message.content[:60]
            if preview and preview != self.current_activity:
                self.current_activity = preview
                self.report_progress(elapsed)

    def report_progress(self, elapsed: float):
        """Print progress update"""
        print(f"[{elapsed:6.1f}s] {self.current_activity}")
        print(f"         Tools: {self.tool_count} | Messages: {self.message_count}")

# Usage
monitor = ProgressMonitor()

async for message in query(prompt="Long analysis task", options=options):
    monitor.update(message)
```

**Checkpoint Pattern** (for very long operations):

```python
async def with_checkpoints(prompt: str, checkpoint_interval: int = 300):
    """
    Monitor operation with periodic checkpoints

    Args:
        checkpoint_interval: Seconds between checkpoints (default 5 min)
    """
    last_checkpoint = time.time()
    checkpoint_data = []

    async for message in query(prompt=prompt, options=options):
        # Collect messages
        checkpoint_data.append(message)

        # Checkpoint every N seconds
        if time.time() - last_checkpoint > checkpoint_interval:
            # Save checkpoint
            with open(f'checkpoint_{int(time.time())}.json', 'w') as f:
                json.dump([m.dict() for m in checkpoint_data], f)

            print(f"💾 Checkpoint saved ({len(checkpoint_data)} messages)")
            last_checkpoint = time.time()
```

---

### 10. Testing Plugin Commands

**Purpose**: Validate plugin behavior programmatically

**Basic Test Pattern**:

```python
async def test_plugin_command(
    plugin_path: str,
    command: str,
    expected_patterns: list
) -> bool:
    """
    Test plugin command execution

    Args:
        plugin_path: Path to plugin directory
        command: Command to execute (e.g., "/plugin:cmd arg")
        expected_patterns: List of patterns that should appear in output

    Returns:
        True if all patterns found
    """
    print(f"Testing: {command}")

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": plugin_path}]
    )

    messages = []
    async for msg in query(prompt=command, options=options):
        if msg.type == 'assistant':
            messages.append(msg.content)

    output = ''.join(messages)

    # Validate
    checks_passed = 0
    for pattern in expected_patterns:
        if pattern in output:
            print(f"  ✅ Found: '{pattern}'")
            checks_passed += 1
        else:
            print(f"  ❌ Missing: '{pattern}'")

    success = checks_passed == len(expected_patterns)
    print(f"  Result: {checks_passed}/{len(expected_patterns)} checks passed")

    return success

# Usage
passed = await test_plugin_command(
    plugin_path="./my-plugin",
    command="/my-plugin:analyze",
    expected_patterns=["Analysis complete", "Results:", "Success"]
)
```

**Executable Test Script** (no pytest):

```python
#!/usr/bin/env python3
"""
Test plugin functionality
Run: python test_my_plugin.py
"""

import sys
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    print("=" * 80)
    print("PLUGIN TEST")
    print("=" * 80)

    # Test 1
    print("\nTest 1: Basic command execution")

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./my-plugin"}]
    )

    messages = []
    async for msg in query(prompt="/my-plugin:test", options=options):
        if msg.type == 'assistant':
            messages.append(msg.content)

    output = ''.join(messages)

    # Validate
    if "expected text" in output:
        print("  ✅ Test 1 passed")
        test1_passed = True
    else:
        print("  ❌ Test 1 failed")
        test1_passed = False

    # Summary
    print("\n" + "=" * 80)
    if test1_passed:
        print("✅ ALL TESTS PASSED")
        return 0
    else:
        print("❌ TESTS FAILED")
        return 1

if __name__ == '__main__':
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
```

---

### 11. Capturing Tool Usage

**Purpose**: Monitor which tools plugins invoke, validate tool calls

**Tool Tracking**:

```python
class ToolTracker:
    """Track all tool calls during operation"""

    def __init__(self):
        self.tools = []

    def record(self, message):
        """Record tool call"""
        if message.type == 'tool_call':
            self.tools.append({
                'tool': message.tool_name,
                'input': message.input,
                'timestamp': time.time()
            })
        elif message.type == 'tool_result':
            # Match to previous tool_call and add result
            if self.tools and self.tools[-1]['tool'] == message.tool_name:
                self.tools[-1]['result'] = message.result
                self.tools[-1]['success'] = True

    def summary(self):
        """Print tool usage summary"""
        print(f"Total tools called: {len(self.tools)}")

        # Group by tool name
        from collections import Counter
        tool_counts = Counter(t['tool'] for t in self.tools)

        print("Tool usage:")
        for tool, count in tool_counts.most_common():
            print(f"  {tool}: {count}x")

        return self.tools

# Usage
tracker = ToolTracker()

async for message in query(prompt="Complex task", options=options):
    tracker.record(message)

tools_used = tracker.summary()
```

**Validation**: Verify expected tools were called

```python
def validate_tools_used(tools: list, expected_tools: set) -> bool:
    """Validate expected tools were called"""
    actual_tools = {t['tool'] for t in tools}

    missing = expected_tools - actual_tools
    unexpected = actual_tools - expected_tools

    if not missing and not unexpected:
        print(f"✅ Tools match expected: {expected_tools}")
        return True
    else:
        if missing:
            print(f"❌ Missing tools: {missing}")
        if unexpected:
            print(f"⚠️  Unexpected tools: {unexpected}")
        return False
```

---

### 12. Working Directory and File Operations

**Purpose**: Control where plugin operates, validate file changes

**Set Working Directory**:

```python
options = ClaudeAgentOptions(
    cwd="/path/to/project",  # All file operations relative to this
    allowed_tools=["Read", "Write", "Edit"]
)
```

**Validate File Changes**:

```python
import os
from pathlib import Path

def capture_file_state(directory: str) -> dict:
    """Capture file tree state"""
    files = {}
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            filepath = Path(root) / filename
            files[str(filepath)] = filepath.stat().st_mtime
    return files

# Before operation
before = capture_file_state("./project")

# Run plugin
async for msg in query(prompt="/plugin:create-files", options=options):
    pass

# After operation
after = capture_file_state("./project")

# Compare
new_files = set(after.keys()) - set(before.keys())
modified = {f for f in before if f in after and after[f] != before[f]}

print(f"New files: {len(new_files)}")
for f in new_files:
    print(f"  + {f}")

print(f"Modified: {len(modified)}")
for f in modified:
    print(f"  ~ {f}")
```

---

### 13. Cost Tracking

**Purpose**: Monitor API costs during testing

**Token Usage Tracking**:

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

async with ClaudeSDKClient(options=options) as client:
    await client.query("Analyze this project")

    total_tokens = 0

    async for msg in client.receive_messages():
        # Token count in system completion message
        if msg.type == 'system' and msg.subtype == 'completion':
            if hasattr(msg, 'usage'):
                total_tokens = msg.usage.get('total_tokens', 0)
                print(f"Total tokens: {total_tokens:,}")

# Estimate cost (rough)
cost_per_million = 3.0  # $3 per million tokens for Sonnet
estimated_cost = (total_tokens / 1_000_000) * cost_per_million
print(f"Estimated cost: ${estimated_cost:.4f}")
```

**Budget Control**:

```python
class BudgetController:
    """Track and limit spending during tests"""

    def __init__(self, budget_usd: float = 10.0):
        self.budget = budget_usd
        self.spent = 0.0

    def can_run(self, estimated_cost: float) -> bool:
        """Check if test can run within budget"""
        if self.spent + estimated_cost > self.budget:
            print(f"⊘ Budget exceeded: ${self.spent:.2f} / ${self.budget:.2f}")
            return False
        return True

    def record(self, cost: float):
        """Record cost after test"""
        self.spent += cost
        print(f"💰 Cost: ${cost:.2f} | Total: ${self.spent:.2f} / ${self.budget:.2f}")

# Usage
budget = BudgetController(budget_usd=10.0)

if budget.can_run(estimated_cost=0.50):
    # Run test
    result = await run_test()
    budget.record(0.45)  # Actual cost
```

---

### 14. Subagents in SDK

**Purpose**: Define specialized agents for delegation

**Basic Subagent Definition**:

```python
from claude_agent_sdk import AgentDefinition

options = ClaudeAgentOptions(
    agents={
        "analyzer": AgentDefinition(
            description="Code analysis specialist",
            prompt="You analyze code for issues. Be thorough.",
            tools=["Read", "Grep"],
            model="sonnet"
        ),
        "builder": AgentDefinition(
            description="Code implementation specialist",
            prompt="You build features. Write clean code.",
            tools=["Read", "Write", "Edit"],
            model="sonnet"
        )
    }
)

# Main agent can delegate to subagents
async for msg in query(
    prompt="Analyze then build feature X",
    options=options
):
    # Main agent may use Task tool to delegate to analyzer or builder
    pass
```

**Monitoring Subagent Activity**:

```python
async for message in query(prompt="Complex task", options=options):
    if message.type == 'tool_call' and message.tool_name == 'Task':
        # Subagent delegation happening
        subagent = message.input.get('subagent_type')
        print(f"🔄 Delegating to: {subagent}")

    elif message.type == 'tool_result' and message.tool_name == 'Task':
        # Subagent completed
        print(f"✅ Subagent completed")
```

---

### 15. Common Patterns

**Pattern 1: Test and Capture**

```python
async def test_and_capture(prompt: str, plugin_path: str) -> dict:
    """Execute plugin command and capture complete state"""

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": plugin_path}]
    )

    result = {
        'messages': [],
        'tools_called': [],
        'duration_seconds': 0,
        'success': False
    }

    start = time.time()

    try:
        async for msg in query(prompt=prompt, options=options):
            if msg.type == 'assistant':
                result['messages'].append(msg.content)
            elif msg.type == 'tool_call':
                result['tools_called'].append(msg.tool_name)

        result['success'] = True

    except Exception as e:
        result['error'] = str(e)

    result['duration_seconds'] = time.time() - start

    return result
```

**Pattern 2: Batch Testing**

```python
async def batch_test(test_cases: list) -> dict:
    """Run multiple tests and aggregate results"""

    results = {
        'total': len(test_cases),
        'passed': 0,
        'failed': 0,
        'tests': []
    }

    for test in test_cases:
        print(f"\nRunning: {test['name']}")

        passed = await test_plugin_command(
            plugin_path=test['plugin'],
            command=test['command'],
            expected_patterns=test['expected']
        )

        results['tests'].append({
            'name': test['name'],
            'passed': passed
        })

        if passed:
            results['passed'] += 1
        else:
            results['failed'] += 1

    print(f"\n{'='*80}")
    print(f"Summary: {results['passed']}/{results['total']} passed")
    print(f"{'='*80}")

    return results
```

**Pattern 3: Iterative Testing**

```python
def test_fix_retest_loop(test_fn, max_iterations: int = 5):
    """
    Run test, identify failures, allow fixes, retest

    Use for plugin development/debugging
    """
    for iteration in range(1, max_iterations + 1):
        print(f"\n{'='*80}")
        print(f"Iteration {iteration}")
        print(f"{'='*80}")

        passed = asyncio.run(test_fn())

        if passed:
            print(f"\n✅ Tests passed on iteration {iteration}")
            return True
        else:
            print(f"\n❌ Tests failed on iteration {iteration}")

            if iteration < max_iterations:
                input("\nFix the plugin, then press Enter to retest...")
            else:
                print(f"\nMax iterations ({max_iterations}) reached")
                return False
```

---

### 16. Real-World Examples

**Example 1: Test Plugin Loads Correctly**

```python
#!/usr/bin/env python3
import sys
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def test_plugin_loads():
    """Verify plugin loads without errors"""

    print("Test: Plugin loads correctly")

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./my-plugin"}]
    )

    # Simple query to trigger plugin loading
    async for msg in query(prompt="hello", options=options):
        if msg.type == 'system' and msg.subtype == 'init':
            if msg.plugins and len(msg.plugins) > 0:
                print(f"✅ Plugin loaded: {msg.plugins}")
                return 0

    print("❌ Plugin did not load")
    return 1

if __name__ == '__main__':
    sys.exit(asyncio.run(test_plugin_loads()))
```

**Example 2: Test Command Produces Expected Output**

```python
async def test_command_output():
    """Test plugin command produces expected results"""

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./my-plugin"}]
    )

    # Execute command
    messages = []
    async for msg in query(prompt="/my-plugin:analyze test.txt", options=options):
        if msg.type == 'assistant':
            messages.append(msg.content)

    output = ''.join(messages)

    # Validate output
    required_elements = [
        "Analysis complete",
        "Lines:",
        "Characters:"
    ]

    checks_passed = sum(1 for elem in required_elements if elem in output)

    if checks_passed == len(required_elements):
        print(f"✅ All {len(required_elements)} checks passed")
        return 0
    else:
        print(f"❌ Only {checks_passed}/{len(required_elements)} checks passed")
        print(f"Output: {output[:200]}...")
        return 1
```

**Example 3: Monitor Long-Running Plugin Operation**

```python
async def test_long_operation():
    """Monitor plugin through long operation"""

    import time

    start = time.time()
    tool_count = 0

    print("Starting long operation...")

    async for msg in query(
        prompt="/plugin:build-project spec.md",
        options=ClaudeAgentOptions(
            plugins=[{"type": "local", "path": "./plugin"}]
        )
    ):
        elapsed = time.time() - start

        if msg.type == 'tool_call':
            tool_count += 1
            print(f"[{elapsed:6.1f}s] Tool {tool_count}: {msg.tool_name}")

        elif msg.type == 'assistant':
            preview = msg.content[:60]
            if preview:
                print(f"[{elapsed:6.1f}s] {preview}...")

    total_time = time.time() - start
    print(f"\nCompleted in {total_time/60:.1f} minutes")
    print(f"Tools used: {tool_count}")
```

---

## Common Issues

**Issue 1: Plugin Not Found**
```
Error: Plugin not loaded
```
**Solution**: Verify path points to directory containing `.claude-plugin/plugin.json`

**Issue 2: Command Not Recognized**
```
Error: Unknown command /plugin:cmd
```
**Solution**: Use correct namespace format: `plugin-name:command-name`

**Issue 3: Permission Denied**
```
Error: Permission denied for tool
```
**Solution**: Check `permission_mode` or add tool to `allowed_tools`

**Issue 4: Timeout on Long Operations**
```
Error: asyncio.TimeoutError
```
**Solution**: Wrap in `asyncio.timeout()` with appropriate duration

**Issue 5: Can't Extract Data from Output**
```
Error: Pattern not found
```
**Solution**: Print full output, adjust regex patterns, handle format variations

---

## SDK vs CLI Differences

**SDK Advantages**:
- ✅ Programmatic control (loops, conditions, automation)
- ✅ Capture and parse all messages
- ✅ Monitor real-time progress
- ✅ Automated testing possible
- ✅ Integration into pipelines

**SDK Limitations**:
- ❌ Some hooks may not fire (hooks are Claude Code-specific)
- ❌ Different session model than interactive Claude Code
- ❌ Text parsing required (no structured JSON API)

---

## Quick Reference

| Task | Code Pattern |
|------|--------------|
| **Load plugin** | `options=ClaudeAgentOptions(plugins=[{"type": "local", "path": "./plugin"}])` |
| **Execute command** | `async for msg in query(prompt="/plugin:cmd", options=options)` |
| **Monitor progress** | Track `tool_call` and `assistant` messages with timestamps |
| **Validate output** | Regex patterns, string contains checks |
| **Handle errors** | Try/except with SDK-specific exceptions |
| **Track tools** | Monitor `tool_call` and `tool_result` messages |
| **Timeout** | `async with asyncio.timeout(seconds)` |
| **Resume session** | `await client.query("...", resume=session_id)` |

---

## Dependencies

**Required**:
- `claude-agent-sdk` (Python package)
- Claude Code CLI (required by SDK)
- `ANTHROPIC_API_KEY` environment variable

**Optional**:
- `asyncio` (standard library, for timeout/gather)
- `re` (standard library, for pattern matching)

---

## References

- **Official SDK Docs**: https://docs.claude.com/en/docs/agent-sdk/python
- **Plugin Loading**: https://docs.claude.com/en/docs/agent-sdk/plugins
- **Session Management**: https://docs.claude.com/en/docs/agent-sdk/sessions
- **Python API Reference**: https://docs.claude.com/en/docs/agent-sdk/python

---

**This skill provides general SDK knowledge. For specific testing scenarios, combine with domain knowledge and validation requirements.**
