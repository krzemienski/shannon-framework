# SHANNON CLI - TECHNICAL SPECIFICATION V2.0

**Version**: 2.0.0 (Complete Architectural Redesign)
**Date**: 2025-11-13
**Specification Type**: Thin Wrapper Over Shannon Framework
**Architecture**: SDK-Based Delegation (NOT Reimplementation)

---

## CRITICAL ARCHITECTURE CHANGE

**V1.0 (WRONG)**: Reimplemented Shannon Framework algorithms in Python (6,918 lines)
**V2.0 (CORRECT)**: Thin wrapper that invokes Shannon Framework via SDK (3,000 lines)

**Key Insight**: Shannon Framework already has all algorithms (18 skills, 11,045 lines). Shannon CLI should DELEGATE, not REIMPLEMENT.

---

## EXECUTIVE SUMMARY

### What Shannon CLI Actually Is

Shannon CLI is a **standalone Python executable** that provides:
1. **Programmatic API** - Call Shannon Framework from Python scripts/CI/CD
2. **Beautiful Terminal UI** - Rich progress bars, spinners, tables
3. **Session Persistence** - Resume capability with local file storage
4. **JSON Output** - Machine-readable for automation
5. **Progress Visibility** - Show what's happening under the hood
6. **Exit Codes** - Proper CI/CD integration

### What Shannon CLI Is NOT

❌ NOT a reimplementation of 8D complexity analysis
❌ NOT a reimplementation of wave orchestration
❌ NOT a reimplementation of domain detection
❌ NOT a reimplementation of ANY Shannon Framework algorithm

### How It Works

```
User runs: shannon analyze spec.md
    ↓
Shannon CLI (Python Click app)
    ↓
Claude Agent SDK query() with Shannon plugin loaded
    ↓
Agent executes: @skill spec-analysis [spec text]
    ↓
Shannon Framework skill executes (1,786 line algorithm)
    ↓
Results stream back to CLI with progress
    ↓
CLI displays with Rich UI + saves to session
```

**Code Reduction**: 6,918 lines → 3,000 lines (57% reduction)
**Algorithm Reuse**: 100% (zero duplication)
**Maintenance**: Framework updates → CLI gets them automatically

---

## ARCHITECTURE OVERVIEW

### Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 1: CLI INTERFACE (~500 lines)                   │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Click Commands + Rich Terminal UI              │   │
│  │  • shannon analyze                              │   │
│  │  • shannon wave                                 │   │
│  │  • shannon status                               │   │
│  └─────────────────────────────────────────────────┘   │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│  LAYER 2: SDK ORCHESTRATION (~800 lines)                │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │ SDKClient    │ │ProgressUI    │ │MessageParser │   │
│  │• Load plugin │ │• Spinners    │ │• Extract     │   │
│  │• Invoke skill│ │• Progress    │ │• Parse       │   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│  LAYER 3: SHANNON FRAMEWORK (via SDK)                   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │ spec-analysis│ │wave-orchestr.│ │Other 16 skill│   │
│  │ (1,786 lines)│ │ (1,611 lines)│ │ (7,648 lines)│   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
│  Plugin loaded via: plugins=[{path: shannon-framework}] │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  LAYER 4: SESSION STORAGE (~700 lines)                  │
│  SessionManager + Config + Logger                       │
│  ~/.shannon/sessions/{id}/*.json                        │
└─────────────────────────────────────────────────────────┘
```

**Total**: ~3,000 lines (CLI-specific code only)
**Delegates**: ~11,000 lines (Shannon Framework skills/core)

---

## COMPONENT SPECIFICATIONS

### Component 1: ShannonSDKClient (~200 lines)

**File**: `src/shannon/sdk/client.py`

**Purpose**: Wrapper around claude_agent_sdk that loads Shannon Framework

**Class Structure**:
```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition
from pathlib import Path

class ShannonSDKClient:
    """Client for invoking Shannon Framework via SDK"""

    def __init__(
        self,
        shannon_framework_path: Path = None,
        session_id: str = None
    ):
        # Locate Shannon Framework
        self.framework_path = shannon_framework_path or self._find_framework()

        # Base options for all SDK calls
        self.base_options = ClaudeAgentOptions(
            plugins=[{
                "type": "local",
                "path": str(self.framework_path)
            }],
            setting_sources=["user", "project"],  # Load skills
            allowed_tools=["Skill", "Read", "Write", "Bash", "Task", "SlashCommand"],
            cwd=str(Path.cwd()),
            model="claude-sonnet-4.5"
        )

    async def invoke_skill(
        self,
        skill_name: str,
        prompt: str,
        progress_callback=None
    ) -> dict:
        """
        Invoke a Shannon Framework skill

        Args:
            skill_name: e.g., 'spec-analysis', 'wave-orchestration'
            prompt: Skill-specific prompt
            progress_callback: Optional callback for progress updates

        Returns:
            Parsed skill result as dict
        """
        messages = []

        async for msg in query(
            prompt=f"@skill {skill_name}\n\n{prompt}",
            options=self.base_options
        ):
            messages.append(msg)

            # Call progress callback
            if progress_callback:
                progress_callback(msg)

        # Extract result from messages
        return self._extract_result(messages)

    async def invoke_command(
        self,
        command: str,
        args: str = "",
        progress_callback=None
    ) -> dict:
        """
        Invoke a Shannon Framework command

        Args:
            command: e.g., '/shannon:spec', '/shannon:wave'
            args: Command arguments

        Returns:
            Parsed command result
        """
        async for msg in query(
            prompt=f"{command} {args}",
            options=self.base_options
        ):
            if progress_callback:
                progress_callback(msg)

        return self._extract_result(messages)
```

**Key Methods**:
- `invoke_skill()`: Run Shannon skill, stream progress
- `invoke_command()`: Run Shannon command
- `_extract_result()`: Parse SDK messages for results
- `_find_framework()`: Locate Shannon Framework directory

---

### Component 2: ProgressUI (~200 lines)

**File**: `src/shannon/ui/progress.py`

**Purpose**: Rich terminal UI showing real-time progress

**Features**:
```python
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.table import Table

class ProgressUI:
    """Real-time progress display for Shannon operations"""

    def __init__(self):
        self.console = Console()
        self.current_operation = None

    def track_skill_execution(self, skill_name: str, messages):
        """
        Show progress while skill executes

        Displays:
        - Spinner during execution
        - Dimension calculations as they happen
        - Tool calls made by skill
        - Final results
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task(
                f"Running {skill_name} skill...",
                total=None
            )

            for msg in messages:
                # Update progress based on message type
                if isinstance(msg, ToolUseBlock):
                    progress.update(task, description=f"Tool: {msg.name}")

                if isinstance(msg, TextBlock):
                    # Parse for progress indicators
                    if "structural" in msg.text.lower():
                        progress.update(task, description="Calculating structural...")

    def display_analysis_result(self, result: dict):
        """Display 8D analysis with Rich tables"""
        # Create beautiful table showing dimensions
        table = Table(title="8D Complexity Analysis")
        table.add_column("Dimension", style="cyan")
        table.add_column("Score", style="magenta")
        table.add_column("Weight", style="green")
        table.add_column("Contribution", style="yellow")

        for dim_name, dim_data in result['dimension_scores'].items():
            table.add_row(
                dim_name.capitalize(),
                f"{dim_data['score']:.3f}",
                f"{dim_data['weight']:.0%}",
                f"{dim_data['contribution']:.4f}"
            )

        self.console.print(table)
```

**Display Modes**:
- Spinners for long operations
- Progress bars for multi-step processes
- Tables for results
- Color-coded output
- Live updates during execution

---

### Component 3: MessageParser (~150 lines)

**File**: `src/shannon/sdk/message_parser.py`

**Purpose**: Parse Claude Agent SDK messages and extract meaningful info

**Class Structure**:
```python
from claude_agent_sdk import AssistantMessage, ToolUseBlock, TextBlock, ResultMessage

class MessageParser:
    """Parse SDK messages for results and progress"""

    def extract_skill_result(self, messages: list) -> dict:
        """
        Extract result from spec-analysis skill execution

        Parses AssistantMessage content for:
        - Complexity score
        - Dimension scores
        - Domain percentages
        - MCP recommendations
        - Phase plan

        Returns structured dict matching AnalysisResult model
        """
        for msg in reversed(messages):  # Start from end
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        # Parse text for structured data
                        # Look for "Complexity: 0.68"
                        # Look for dimension tables
                        # Extract JSON if present
                        return self._parse_analysis_text(block.text)

    def extract_progress_indicators(self, msg) -> dict:
        """
        Extract progress info from streaming message

        Returns:
        - current_step: "Calculating structural..."
        - tool_used: "Read", "Skill", etc.
        - progress_percent: 0-100
        """
        if isinstance(msg, ToolUseBlock):
            return {
                'type': 'tool_use',
                'tool': msg.name,
                'operation': msg.input.get('description', '')
            }

        if isinstance(msg, TextBlock):
            # Parse for progress keywords
            text = msg.text.lower()
            if "calculating" in text:
                return {'type': 'progress', 'step': msg.text}

    def extract_tool_calls(self, messages: list) -> list:
        """Get all tool calls made during execution"""
        tools = []
        for msg in messages:
            if isinstance(msg, ToolUseBlock):
                tools.append({
                    'name': msg.name,
                    'input': msg.input
                })
        return tools
```

**Methods**:
- `extract_skill_result()`: Parse final result
- `extract_progress_indicators()`: Real-time progress
- `extract_tool_calls()`: Show tools used
- `extract_wave_results()`: Parse wave execution

---

### Component 4: CLI Commands (~300 lines)

**File**: `src/shannon/cli/commands.py`

**Commands**:

```python
import click
from shannon.sdk.client import ShannonSDKClient
from shannon.ui.progress import ProgressUI
from shannon.core.session_manager import SessionManager

@click.group()
def cli():
    """Shannon Framework - Standalone CLI"""
    pass

@cli.command()
@click.argument('spec_file', type=click.Path(exists=True))
@click.option('--json', is_flag=True, help='Output JSON')
@click.option('--session-id', help='Session ID for persistence')
def analyze(spec_file, json, session_id):
    """
    Analyze specification using Shannon Framework's 8D algorithm

    Delegates to spec-analysis skill via SDK
    """
    # Initialize
    session = SessionManager(session_id or generate_session_id())
    client = ShannonSDKClient()
    ui = ProgressUI()

    # Read spec
    spec_text = Path(spec_file).read_text()

    # Invoke framework skill with progress tracking
    ui.console.print("[bold]Shannon Specification Analysis[/bold]")

    result = None
    async for msg in client.invoke_skill('spec-analysis', spec_text):
        # Show progress
        ui.track_skill_execution('spec-analysis', [msg])

        # Parse final result
        if is_final_message(msg):
            result = parser.extract_skill_result(messages)

    # Save session
    session.write_memory('spec_analysis', result)

    # Display
    if json:
        print(json.dumps(result, indent=2))
    else:
        ui.display_analysis_result(result)

    # Exit
    sys.exit(0)

@cli.command()
@click.argument('request')
@click.option('--session-id', help='Session ID to resume')
def wave(request, session_id):
    """
    Execute wave-based implementation

    Delegates to wave-orchestration skill via SDK
    """
    # Load previous analysis
    session = SessionManager(session_id or get_latest_session())
    analysis = session.read_memory('spec_analysis')

    if not analysis:
        click.echo("Error: Run 'shannon analyze' first", err=True)
        sys.exit(1)

    # Invoke wave orchestration
    client = ShannonSDKClient()
    ui = ProgressUI()

    async for msg in client.invoke_command('/shannon:wave', request):
        ui.track_wave_execution(msg)

    sys.exit(0)

@cli.command()
@click.option('--session-id', help='Session ID')
def status(session_id):
    """Show current session status"""
    session = SessionManager(session_id or get_latest_session())

    # Read session files (no SDK needed)
    analysis = session.read_memory('spec_analysis')
    waves = session.list_memories_matching('wave_*_complete')

    # Display with Rich
    table = Table(title="Session Status")
    table.add_row("Complexity", f"{analysis['complexity_score']:.3f}")
    table.add_row("Waves Complete", f"{len(waves)}/6")
    # ...

    console.print(table)
    sys.exit(0)
```

---

## SDK INTEGRATION SPECIFICATION

### Shannon Framework Plugin Loading

**Every SDK call must include**:
```python
ClaudeAgentOptions(
    plugins=[{
        "type": "local",
        "path": "/Users/nick/Desktop/shannon-framework"  # Or auto-detect
    }],
    setting_sources=["user", "project"],  # Required for skills
    allowed_tools=["Skill", "Read", "Write", "Bash", "Task", "SlashCommand"]
)
```

### Skill Invocation Pattern

**Pattern 1: Via Skill Tool**
```python
prompt = f"@skill spec-analysis\n\nAnalyze this spec: {spec_text}"
async for msg in query(prompt, options):
    # Process messages
```

**Pattern 2: Via Command**
```python
prompt = f"/shannon:spec @{spec_file}"
async for msg in query(prompt, options):
    # Process messages
```

Both work - skills are more direct, commands may have additional logic.

### Message Streaming and Progress

**SDK returns messages in order**:
1. `SystemMessage(subtype='init')` - Initialization, shows loaded plugins
2. `AssistantMessage` - Claude's response with ToolUseBlocks
3. `ToolUseBlock` - When Claude uses tools (Read, Skill, etc.)
4. `TextBlock` - Text content from Claude
5. `ResultMessage` - Final result with costs

**Progress extraction**:
```python
for msg in messages:
    if isinstance(msg, ToolUseBlock):
        if msg.name == "Skill":
            print(f"Invoking skill: {msg.input['skill']}")
        elif msg.name == "Read":
            print(f"Reading: {msg.input['file_path']}")

    if isinstance(msg, TextBlock):
        # Parse for progress indicators
        if "Calculating" in msg.text:
            print(f"Progress: {msg.text}")
```

---

## COMPONENTS TO BUILD

### Keep from Waves 1-2 (Reuse ~1,800 lines)

1. **ShannonConfig** (192 lines) - ✅ Keep as-is
2. **ShannonLogger** (551 lines) - ✅ Keep as-is
3. **SessionManager** (506 lines) - ✅ Keep as-is
4. **Pydantic Models** (588 lines) - ✅ Keep for type safety

### Build New (~1,200 lines)

5. **ShannonSDKClient** (~200 lines) - NEW
   - SDK wrapper with Shannon plugin loading
   - Skill/command invocation
   - Message streaming

6. **ProgressUI** (~200 lines) - NEW
   - Rich spinners, progress bars, tables
   - Real-time updates during execution

7. **MessageParser** (~150 lines) - NEW
   - Parse SDK messages
   - Extract results from skill outputs
   - Extract progress indicators

8. **OutputFormatter** (~200 lines) - NEW
   - JSON output mode
   - Markdown output mode
   - Rich table formatting

9. **CLI Commands** (~300 lines) - NEW
   - Click command definitions
   - Argument parsing
   - Exit code handling

10. **ResultExtractor** (~150 lines) - NEW
    - Parse spec-analysis skill output
    - Parse wave-orchestration skill output
    - Convert to Pydantic models

### Delete from Waves 2-3 (~5,118 lines)

❌ Delete entire src/shannon/core/ directory except session_manager.py:
- spec_analyzer.py (~800 lines)
- domain_detector.py (~424 lines)
- mcp_recommender.py (~363 lines)
- phase_planner.py (~510 lines)
- timeline_estimator.py (~245 lines)
- wave_planner.py (~251 lines)
- wave_coordinator.py (~438 lines)
- progress_tracker.py (~431 lines)

❌ Delete src/shannon/sdk/ except client.py:
- agent_factory.py (~266 lines)
- prompt_builder.py (~218 lines)
- templates/ (~716 lines)

**Reason**: All this logic exists in Shannon Framework. We don't need to reimplement it.

---

## IMPLEMENTATION WAVES (REVISED)

### Wave 1: Foundation (KEEP - Already Complete) ✅
- Config, Logger, SessionManager, Models
- **Status**: Done, no changes needed

### Wave 2: SDK Integration (REPLACE Current Wave 2)
**Duration**: 6 hours
**Tasks**:
1. Implement ShannonSDKClient with plugin loading
2. Implement MessageParser for SDK message extraction
3. Test skill invocation (functional test with real SDK)
4. Verify Shannon Framework loads and skills accessible

**Deliverables**:
- Working SDK client that can invoke spec-analysis skill
- Message parser extracting results
- Functional test proving integration works

### Wave 3: CLI Commands (REPLACE Current Wave 3)
**Duration**: 8 hours
**Tasks**:
1. Implement `shannon analyze` command
2. Implement `shannon wave` command
3. Implement `shannon status` command
4. Implement `shannon resume` command
5. Add argument parsing and validation

**Deliverables**:
- 4 working CLI commands
- Proper exit codes
- Help text and documentation

### Wave 4: Progress UI (NEW)
**Duration**: 6 hours
**Tasks**:
1. Implement ProgressUI with Rich spinners
2. Add progress tracking for skill execution
3. Add table formatting for results
4. Add live updates during wave execution

**Deliverables**:
- Beautiful terminal output
- Real-time progress visibility
- Rich tables and spinners

### Wave 5: Output Formatting (NEW)
**Duration**: 4 hours
**Tasks**:
1. JSON output mode
2. Markdown output mode
3. ResultExtractor for parsing skill outputs
4. Format converters

**Deliverables**:
- Multiple output formats
- Automation-friendly JSON
- Human-friendly Rich tables

### Wave 6: Functional Testing (KEEP Concept, Update Tests)
**Duration**: 6 hours
**Tasks**:
1. Shell script testing (NO pytest)
2. Test `shannon analyze` end-to-end
3. Test `shannon wave` with real Shannon Framework
4. Validate session persistence
5. Verify progress tracking displays correctly

**Deliverables**:
- Functional shell script tests
- End-to-end validation
- NO pytest (per spec requirement)

---

## SUCCESS CRITERIA (REVISED)

### Functional Criteria

1. ✅ **Shannon Framework Integration**: All commands invoke framework skills/commands successfully
2. ✅ **Progress Visibility**: User sees real-time updates (spinners, tool calls, dimension calculations)
3. ✅ **Session Persistence**: Can save and resume sessions
4. ✅ **Beautiful Output**: Rich terminal UI with tables, colors, spinners
5. ✅ **JSON Mode**: `--json` flag outputs machine-readable JSON
6. ✅ **Exit Codes**: Proper codes for CI/CD (0=success, 1=error)
7. ✅ **NO Algorithm Duplication**: Zero reimplementation of framework logic
8. ✅ **Functional Testing**: Shell scripts validate end-to-end (NO pytest)

### Quantitative Metrics

- **Code Size**: ≤ 3,000 lines (vs original spec's 6,918)
- **Algorithm Duplication**: 0% (all delegated to framework)
- **Test Coverage**: 100% via shell scripts
- **SDK Integration**: 100% (all commands use framework)
- **Framework Leverage**: 18/18 skills accessible, 15/15 commands usable

---

## FILE STRUCTURE (REVISED)

```
shannon-cli/
├── pyproject.toml                    # Poetry config (keep)
├── README.md                         # Update for new architecture
├── TECHNICAL_SPEC_V2.md             # THIS FILE
├── src/
│   └── shannon/
│       ├── __init__.py
│       ├── config.py                # ✅ Keep (192 lines)
│       ├── logger.py                # ✅ Keep (551 lines)
│       ├── cli/
│       │   ├── commands.py          # ✅ Rebuild (~300 lines)
│       │   └── output.py            # ✅ Rebuild (~100 lines)
│       ├── sdk/
│       │   ├── client.py            # ✅ NEW (~200 lines)
│       │   └── message_parser.py    # ✅ NEW (~150 lines)
│       ├── ui/
│       │   ├── progress.py          # ✅ NEW (~200 lines)
│       │   └── formatters.py        # ✅ NEW (~200 lines)
│       ├── storage/
│       │   ├── models.py            # ✅ Keep (588 lines)
│       │   └── session_manager.py   # ✅ Keep (506 lines)
│       └── core/
│           └── (DELETE ALL except session_manager moved to storage)
└── tests/
    └── functional/                  # Shell scripts (Wave 6)
        ├── test_analyze.sh
        ├── test_wave.sh
        └── test_session.sh
```

**Total Production Code**: ~2,987 lines
- Kept from Waves 1-2: 1,837 lines
- New for SDK integration: 1,150 lines

**Deleted**: ~5,118 lines (reimplemented algorithms)

---

## TESTING STRATEGY (Shell Scripts Only)

### Test 1: Basic Analysis

**File**: `tests/functional/test_analyze_basic.sh`

```bash
#!/bin/bash

# Test shannon analyze command

SPEC_FILE="fixtures/simple_todo.md"
SESSION_ID="test_$(date +%s)"

# Run analysis
shannon analyze "$SPEC_FILE" --session-id "$SESSION_ID" --json > result.json

# Validate
COMPLEXITY=$(jq -r '.complexity_score' result.json)

# Check in range [0.25, 0.40] for simple todo
if (( $(echo "$COMPLEXITY >= 0.25 && $COMPLEXITY <= 0.40" | bc -l) )); then
    echo "✅ Complexity in expected range: $COMPLEXITY"
else
    echo "❌ Complexity out of range: $COMPLEXITY"
    exit 1
fi

# Check session file created
if [ -f "~/.shannon/sessions/$SESSION_ID/spec_analysis.json" ]; then
    echo "✅ Session file created"
else
    echo "❌ Session file not found"
    exit 1
fi

echo "✅ Test passed"
exit 0
```

### Test 2: Wave Execution

```bash
#!/bin/bash

# Test shannon wave command

# First analyze
shannon analyze fixtures/moderate.md --session-id wave_test

# Then run wave
shannon wave "Implement the system" --session-id wave_test 2>&1 | tee wave_output.log

# Check for wave execution indicators
grep -q "Wave 1:" wave_output.log || exit 1
grep -q "agents" wave_output.log || exit 1

echo "✅ Wave execution test passed"
```

**NO PYTEST** - All testing via shell scripts that run actual CLI commands.

---

## NEXT STEPS

### Immediate Actions

1. ✅ **Delete** reimplemented algorithm code (~5,118 lines)
2. ⏭️ **Implement** ShannonSDKClient with Shannon plugin loading
3. ⏭️ **Test** skill invocation functionally (prove it works)
4. ⏭️ **Implement** CLI commands as thin wrappers
5. ⏭️ **Implement** ProgressUI with Rich
6. ⏭️ **Validate** end-to-end with shell scripts

### Timeline (Revised)

- Wave 1: ✅ Complete (foundation)
- Wave 2: 6 hours (SDK integration)
- Wave 3: 8 hours (CLI commands)
- Wave 4: 6 hours (Progress UI)
- Wave 5: 4 hours (Output formatting)
- Wave 6: 6 hours (Functional testing)

**Total**: 30 hours (vs original 72.5 hours)
**Savings**: 59% faster due to framework delegation

---

## VALIDATION

Shannon CLI v2.0 succeeds when:

✅ Can invoke ALL 18 Shannon Framework skills via SDK
✅ Can run ALL 15 Shannon commands via SDK
✅ Shows real-time progress with Rich UI
✅ Outputs JSON for automation (`--json` flag)
✅ Saves sessions locally (resume capability)
✅ Proper exit codes (0=success, non-zero=error)
✅ Zero algorithm duplication (100% delegation)
✅ Functional shell script tests (NO pytest)
✅ Code size ≤ 3,000 lines
✅ Works standalone (no Claude Code UI needed)

---

**Specification Status**: DRAFT v2.0 - Ready for review and implementation
