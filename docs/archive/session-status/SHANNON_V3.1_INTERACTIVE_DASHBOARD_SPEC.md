# Shannon CLI V3.1 - Complete Interactive Dashboard Specification

**Version**: 3.1.0
**Date**: 2025-11-14
**Status**: Implementation Specification
**Scope**: True 4-Layer Interactive TUI with Agent Navigation and Message Stream Visibility
**Document Size**: ~4,000 lines
**Philosophy**: htop/k9s-level interactive experience for AI agent execution

---

## PART 1: VISION & USER EXPERIENCE (500 lines)

### 1.1 Executive Summary

#### The Gap V3.1 Addresses

**V3.0 Reality**:
- Dashboard shows live metrics (cost, tokens, duration) ✅
- Basic expand/collapse (2 layers) ✅
- Generic progress bar ✅

**V3.0 Missing**:
- Cannot select individual agents in wave execution ❌
- Cannot see what tools each agent is calling ❌
- Cannot view actual USER/ASSISTANT/TOOL messages ❌
- Cannot see loaded context (files, memories, MCPs) ❌
- Cannot navigate session hierarchy (goals → waves → agents → commands → messages) ❌

**V3.1 Delivers**: True interactive TUI with **4-layer drill-down**, **agent selection**, **message streaming**, and **context visibility**.

#### Core User Workflows

**Workflow 1: Monitor Single-Agent Analysis**

```
User runs: shannon analyze spec.md

Layer 1 (Auto-appears):
┌─ Shannon V3.1 - spec-analysis ─────────────────────┐
│ 🎯 Goal: Analyze specification complexity          │
│                                                     │
│ Phase: 8D Complexity Analysis                      │
│ ▓▓▓▓▓▓░░░░ 60% (5/8 dimensions)                   │
│                                                     │
│ ⚙  Analyzing: Dependencies dimension               │
│                                                     │
│ $0.12 | 8.2K tokens | 45s | 12 messages            │
│                                                     │
│ [↵] Details | [q] Quit                             │
└─────────────────────────────────────────────────────┘

User presses Enter ↵

Layer 3 (Agent Detail - skips Layer 2 for single agent):
┌─ Agent: spec-analyzer ─────────────────────────────┐
│ Task: Analyze specification using 8D framework     │
│ Status: ACTIVE                                     │
│ Progress: ▓▓▓▓▓▓░░░░ 60% (5/8 dimensions)         │
├─────────────────────────────────────────────────────┤
│ CONTEXT LOADED              │ TOOL CALL HISTORY    │
│                             │                      │
│ 📁 Codebase: 0 files        │ → Read(spec.md)      │
│ 🧠 Memory: 0 active         │ ← 870 bytes          │
│ 🔧 Tools: 5 available       │ → Sequential(100)    │
│    Read, Write, Bash...     │ ← In progress...     │
│ 🔌 MCP: 1 connected         │ (7 calls total)      │
│    Sequential ✅             │                      │
├─────────────────────────────────────────────────────┤
│ CURRENT OPERATION                                   │
│ ⚙  Processing: Dependencies dimension              │
│ Last activity: 2s ago                              │
├─────────────────────────────────────────────────────┤
│ [↵] Messages | [Esc] Back | [q] Quit               │
└─────────────────────────────────────────────────────┘

User presses Enter ↵

Layer 4 (Message Stream):
┌─ Messages: spec-analyzer ──────────────────────────┐
│                                                     │
│ → USER: Analyze this specification using 8D        │
│          framework: [spec content...]              │
│                                                     │
│ ← ASSISTANT: I'll analyze across 8 dimensions...   │
│   [thinking] Breaking into dimensions... (12 lines)│
│                                                     │
│ → TOOL_USE: sequential_thinking                    │
│   {                                                 │
│     thought: "Analyzing structural complexity...", │
│     thoughtNumber: 1,                              │
│     totalThoughts: 100                             │
│   }                                                 │
│                                                     │
│ ← TOOL_RESULT: { thoughtNumber: 1, ... }          │
│                                                     │
│ → TOOL_USE: sequential_thinking                    │
│   { thought: "Cognitive dimension...", ... }       │
│                                                     │
│ [↑↓] Scroll | [Space] Expand | [Esc] Back         │
└─────────────────────────────────────────────────────┘
```

**Workflow 2: Monitor Multi-Agent Wave Execution**

```
User runs: shannon wave build-fullstack-app

Layer 1 (Session Overview):
┌─ Shannon V3.1 - wave-execution ────────────────────┐
│ 🎯 Goal: Build full-stack SaaS application         │
│                                                     │
│ Wave 2/5: Core Implementation                      │
│ ▓▓▓▓▓░░░░░ 47% overall                            │
│                                                     │
│ Agents: 3 active, 2 complete, 1 waiting            │
│                                                     │
│ $2.34 | 45.7K tokens | 2m 15s | 3 waves           │
│                                                     │
│ [↵] Agents | [q] Quit                              │
└─────────────────────────────────────────────────────┘

User presses Enter ↵

Layer 2 (Agent List):
┌─ Wave 2 Agents ─────────────────────────────────────┐
│ # │ Type              │ Progress  │ State    │ Time │
│───┼───────────────────┼───────────┼──────────┼──────│
│ 1 │ backend-builder   │ ▓▓▓░░ 67% │ WAITING  │ 12s  │
│ 2 │ frontend-builder  │ ▓▓░░░ 45% │ ACTIVE   │  -   │
│ 3 │ database-builder  │ ▓▓▓▓▓ 100%│ COMPLETE │ 8m   │
│ 4 │ test-writer       │ ░░░░░  0% │ BLOCKED  │  -   │
│                                                     │
│ Selected: Agent #1 (backend-builder)               │
│ Waiting for: Claude API response                   │
│                                                     │
│ [1-4] Select | [↵] Detail | [Esc] Back            │
└─────────────────────────────────────────────────────┘

User presses 2 (select Agent #2)

Layer 2 updates (Agent #2 now highlighted):
│ 2 │ frontend-builder  │ ▓▓░░░ 45% │ ACTIVE   │  -   │  ← HIGHLIGHTED

User presses Enter ↵

Layer 3 (Agent #2 Detail):
┌─ Agent #2: frontend-builder ───────────────────────┐
│ Task: Build React UI components for dashboard      │
│ Status: ACTIVE                                     │
│ Progress: ▓▓░░░ 45% (3/7 components)              │
├─────────────────────────────────────────────────────┤
│ CONTEXT LOADED         │ TOOL CALL HISTORY         │
│                        │                           │
│ 📁 Codebase: 8 files   │ → Read(package.json) 0.2s │
│    src/components/     │ ← 245 lines               │
│    src/hooks/          │ → Write(Dashboard.tsx)    │
│    public/             │ ← Success                 │
│ 🧠 Memory: 2 active    │ → Write(Chart.tsx)        │
│    react-patterns      │ ← Success                 │
│    ui-conventions      │ → Bash(npm install...)    │
│ 🔧 Tools: 5 available  │ ← Running...              │
│ 🔌 MCP: 2 connected    │ (15 calls total)          │
├─────────────────────────────────────────────────────┤
│ CURRENT OPERATION                                   │
│ ⚙  Running: npm install chart.js                   │
│ Last activity: Building Chart component (3s ago)   │
├─────────────────────────────────────────────────────┤
│ [↵] Messages | [Esc] Agents | [1-4] Switch        │
└─────────────────────────────────────────────────────┘

User presses Enter ↵

Layer 4 (Message Stream for Agent #2):
┌─ Messages: frontend-builder ───────────────────────┐
│                                              [3/89] │
│ → USER: Build React UI components for dashboard    │
│         Include: Chart, Table, Filters             │
│         Style: Tailwind CSS, responsive design     │
│                                                     │
│ ← ASSISTANT: I'll create 7 React components...     │
│   [thinking] Planning component hierarchy...       │
│   - Dashboard.tsx (container)                      │
│   - Chart.tsx (visualization)                      │
│   - Table.tsx (data grid)                          │
│   ...                                              │
│                                                     │
│ → TOOL_USE: read_file                              │
│   { "file_path": "package.json" }                  │
│                                                     │
│ ← TOOL_RESULT: { "content": "{\n  \"name\":..." }  │
│   [truncated - 245 lines, press Enter to expand]   │
│                                                     │
│ ← ASSISTANT: Based on package.json, I'll use...    │
│                                                     │
│ → TOOL_USE: write_file                             │
│   { "file_path": "src/components/Dashboard.tsx",   │
│     "content": "import React from 'react'..." }    │
│                                                     │
│ [↑↓] Scroll | [Enter] Expand | [Esc] Back         │
└─────────────────────────────────────────────────────┘
```

### 1.2 Key Capabilities

#### Capability 1: Session-Level Awareness

**What It Shows**:
- Command being executed (analyze, wave, task)
- North Star goal (if set via /shannon:north_star)
- Current phase/wave number and total
- Overall progress across entire execution
- Active agent count and summary states

**Why It Matters**: User always knows WHERE they are in execution, not just what's happening RIGHT NOW.

#### Capability 2: Agent Selection & Focusing

**What It Provides**:
- Table view of all agents in wave (agent number, type, progress, state)
- Keyboard selection (press 1-9 to focus specific agent)
- Per-agent drill-down to see that agent's work
- Switch between agents without losing position

**Why It Matters**: In multi-agent waves (5-10 agents), user can inspect ANY agent at ANY time, not just aggregate view.

#### Capability 3: Tool-Level Visibility

**What It Shows**:
- Every tool call an agent makes (Read, Write, Bash, Sequential, etc.)
- Tool parameters (file paths, commands, arguments)
- Tool results (success/failure, output size, duration)
- Tool call timeline (chronological history)

**Why It Matters**: User can debug WHY agent is slow (waiting for MCP? Reading large file? Running expensive tool?).

#### Capability 4: Message Stream Display

**What It Provides**:
- Full SDK conversation (USER prompts, ASSISTANT responses, TOOL calls/results)
- Syntax highlighting for code blocks
- Scrolling through message history (arrow keys)
- Message expansion for truncated content
- Thinking block visibility (collapsible)

**Why It Matters**: User sees EXACTLY what the agent is thinking and doing, at the raw SDK level.

#### Capability 5: Context Dimension Visibility

**What It Shows**:
- Codebase context: X files loaded from Y locations
- Memory context: X active memories (names visible)
- Tool context: X available tools (names + descriptions)
- MCP context: X servers connected (names + status + tool count)

**Why It Matters**: User understands what information the agent has access to, can diagnose context issues.

### 1.3 Navigation Model

#### Layer Hierarchy

```
Layer 1 (Session Overview)
    ↓ [Enter]
Layer 2 (Agent List) ← only if multi-agent wave
    ↓ [1-9] select agent, [Enter] drill down
Layer 3 (Agent Detail)
    ↓ [Enter]
Layer 4 (Message Stream)
    ↑ [Esc] at any layer goes back
```

#### Keyboard Controls (Complete Reference)

**Layer 1 (Session Overview)**:
- `Enter`: Navigate to Layer 2 (if wave) or Layer 3 (if single agent)
- `q`: Quit dashboard
- `h`: Show help overlay

**Layer 2 (Agent List)**:
- `1-9`: Select agent by number
- `Enter`: Navigate to Layer 3 for selected agent
- `Esc`: Return to Layer 1
- `q`: Quit dashboard
- `r`: Refresh agent list
- `h`: Show help overlay

**Layer 3 (Agent Detail)**:
- `Enter`: Navigate to Layer 4 (message stream)
- `Esc`: Return to Layer 2 (or Layer 1 if single agent)
- `1-9`: Switch to different agent (stays on Layer 3)
- `t`: Toggle tool history panel
- `c`: Toggle context panel
- `q`: Quit dashboard
- `h`: Show help overlay

**Layer 4 (Message Stream)**:
- `↑` / `k`: Scroll up one message
- `↓` / `j`: Scroll down one message
- `Page Up`: Scroll up 10 messages
- `Page Down`: Scroll down 10 messages
- `Home` / `g`: Jump to first message
- `End` / `G`: Jump to last message
- `Enter`: Expand selected message (if truncated) or copy to clipboard
- `Space`: Expand/collapse thinking blocks
- `Esc`: Return to Layer 3
- `1-9`: Switch to different agent (stays on Layer 4)
- `/`: Search messages (future)
- `n`: Next search result (future)
- `q`: Quit dashboard
- `h`: Show help overlay

#### Help Overlay (Modal)

Pressing `h` at any layer shows context-aware help:

```
┌─ Shannon V3.1 Help ─────────────────────────────────┐
│                                                     │
│ Current Layer: Agent Detail (Layer 3)              │
│                                                     │
│ Navigation:                                         │
│   [↵] Enter    → Message stream                    │
│   [Esc]        → Agent list                        │
│   [1-9]        → Switch to agent N                 │
│                                                     │
│ Panels:                                             │
│   [t]          → Toggle tool history               │
│   [c]          → Toggle context panel              │
│                                                     │
│ General:                                            │
│   [q]          → Quit dashboard                    │
│   [h]          → Toggle this help                  │
│                                                     │
│ [Esc] Close help                                    │
└─────────────────────────────────────────────────────┘
```

### 1.4 Visual Design System

#### Color Palette

**State Colors**:
- Cyan: Active/running operations
- Yellow: Waiting states (WAITING_API, WAITING_DEPENDENCY)
- Green: Complete/success states
- Red: Failed/error states
- Gray/Dim: Inactive or background information
- White: Primary content text

**Syntax Highlighting** (Layer 4 messages):
- Blue: USER messages and prompts
- Green: ASSISTANT responses
- Yellow: TOOL_USE blocks
- Cyan: TOOL_RESULT blocks
- Dim Gray: Thinking blocks (collapsed)
- Bright White: Thinking blocks (expanded)

#### Typography & Symbols

**Progress Indicators**:
- `▓` Filled progress
- `░` Empty progress
- `⚙` Active operation
- `⏳` Waiting operation
- `✓` Complete
- `✗` Failed

**Navigation Hints**:
- `[↵]` Enter key
- `[Esc]` Escape key
- `[↑↓]` Arrow keys
- `[1-9]` Number keys

**Context Dimensions**:
- `📁` Codebase/files
- `🧠` Memory/knowledge
- `🔧` Tools/capabilities
- `🔌` MCP servers
- `🎯` Goals/objectives

### 1.5 Performance Requirements

**Refresh Rate**: 4 Hz (250ms interval) across ALL layers
**Navigation Latency**: <100ms keyboard response
**Layer Switch Time**: <200ms visual transition
**Scroll Smoothness**: No visible lag or stutter
**Memory Usage**: <200MB for dashboard (excluding agent execution)
**CPU Usage**: <10% for dashboard rendering
**Terminal Compatibility**: xterm-256color, tmux, screen

---

## PART 2: ARCHITECTURE SPECIFICATION (1,200 lines)

### 2.1 System Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                  Shannon V3.1 Architecture              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─── DATA LAYER ────────────────────────────────┐    │
│  │                                                │    │
│  │  MetricsCollector    AgentStateTracker        │    │
│  │  ContextManager      SessionManager           │    │
│  │  MessageInterceptor                           │    │
│  │                                                │    │
│  │  ↓ ALL feed into ↓                            │    │
│  │                                                │    │
│  │  DashboardDataProvider.get_snapshot()         │    │
│  │    → DashboardSnapshot (immutable)            │    │
│  └────────────────────────────────────────────────┘    │
│                      ↓                                  │
│  ┌─── STATE LAYER ────────────────────────────────┐   │
│  │                                                 │   │
│  │  DashboardUIState                              │   │
│  │    - current_layer: 1-4                        │   │
│  │    - focused_agent_id: Optional[str]           │   │
│  │    - message_scroll_offset: int                │   │
│  │    - agent_selection_index: int                │   │
│  │                                                 │   │
│  │  NavigationController.handle_key(key, state)   │   │
│  │    → new_state                                 │   │
│  └─────────────────────────────────────────────────┘   │
│                      ↓                                  │
│  ┌─── RENDERING LAYER ────────────────────────────┐   │
│  │                                                 │   │
│  │  Layer1Renderer(snapshot, ui_state)            │   │
│  │  Layer2Renderer(snapshot, ui_state)            │   │
│  │  Layer3Renderer(snapshot, ui_state)            │   │
│  │  Layer4Renderer(snapshot, ui_state)            │   │
│  │    ↓                                            │   │
│  │  Rich.Panel / Rich.Layout / Rich.Table         │   │
│  └─────────────────────────────────────────────────┘   │
│                      ↓                                  │
│  ┌─── INPUT LAYER ────────────────────────────────┐   │
│  │                                                 │   │
│  │  KeyboardHandler (termios)                     │   │
│  │    - poll_key() → KeyEvent                     │   │
│  │    - supports: Enter, Esc, 1-9, ↑↓, q, etc   │   │
│  └─────────────────────────────────────────────────┘   │
│                      ↓                                  │
│  ┌─── UPDATE LOOP (4 Hz) ────────────────────────┐    │
│  │                                                 │   │
│  │  while running:                                │   │
│  │    snapshot = data_provider.get_snapshot()     │   │
│  │    key_event = keyboard.poll_key()             │   │
│  │    ui_state = navigator.handle_key(key, state) │   │
│  │    renderable = render(snapshot, ui_state)     │   │
│  │    live.update(renderable)                     │   │
│  │    sleep(0.25)  # 4 Hz                         │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Data Model Specification

#### 2.2.1 DashboardSnapshot (Immutable State)

```python
@dataclass(frozen=True)
class DashboardSnapshot:
    """
    Complete immutable snapshot of all dashboard data

    Created at 4 Hz by DashboardDataProvider.
    Used by renderers to generate UI (pure function: snapshot → UI).
    """

    # Session-level data
    session: SessionSnapshot

    # Agent-level data (empty list if no wave)
    agents: List[AgentSnapshot]

    # Context-level data
    context: ContextSnapshot

    # Message-level data (for currently focused agent)
    messages: Optional[MessageHistory]

    # Timestamp
    captured_at: float  # Unix timestamp


@dataclass(frozen=True)
class SessionSnapshot:
    """Session-level state"""
    session_id: str
    command_name: str  # 'analyze', 'wave', 'task'
    north_star_goal: Optional[str]
    current_phase: str  # 'Analysis', 'Wave 2/5', etc.
    overall_progress: float  # 0.0-1.0
    start_time: datetime
    elapsed_seconds: float

    # Metrics
    total_cost_usd: float
    total_tokens: int
    message_count: int

    # Wave context (if command == 'wave')
    wave_number: Optional[int]
    total_waves: Optional[int]

    # Agent summary (if wave)
    agents_total: int
    agents_active: int
    agents_complete: int
    agents_waiting: int
    agents_failed: int

    # Current operation
    current_operation: str  # "Analyzing dependencies", "Waiting for Agent #2"
    last_activity: Optional[str]  # "Completed Cognitive dimension"
    last_activity_time: Optional[datetime]


@dataclass(frozen=True)
class AgentSnapshot:
    """Single agent state snapshot"""
    agent_id: str
    agent_number: int  # Display number (1, 2, 3...)
    agent_type: str  # 'backend-builder', 'frontend-builder'
    task_description: str

    # Status
    status: Literal['pending', 'active', 'complete', 'failed']
    progress: float  # 0.0-1.0

    # Timing
    started_at: Optional[datetime]
    elapsed_seconds: float

    # State detail
    current_operation: Optional[str]  # "Reading spec.md", "Waiting for API"
    waiting_reason: Optional[str]  # "WAITING_API", "WAITING_DEPENDENCY"
    wait_duration_seconds: Optional[float]
    blocking_agent_id: Optional[str]  # If WAITING_DEPENDENCY

    # Metrics
    cost_usd: float
    tokens_input: int
    tokens_output: int

    # Artifacts
    files_created: List[str]
    files_modified: List[str]
    tool_calls_count: int

    # Error
    error_message: Optional[str]


@dataclass(frozen=True)
class ContextSnapshot:
    """Context dimensions state"""

    # Codebase
    codebase_files_loaded: int
    codebase_file_list: List[str]  # File paths
    codebase_total_bytes: int

    # Memory
    memories_active: int
    memory_list: List[str]  # Memory names

    # Tools
    tools_available: int
    tool_list: List[str]  # Tool names

    # MCP
    mcp_servers_connected: int
    mcp_server_list: List[MCPServerInfo]


@dataclass(frozen=True)
class MCPServerInfo:
    """MCP server connection info"""
    name: str
    status: Literal['connected', 'disconnected', 'error']
    tools_provided: int
    tool_names: List[str]


@dataclass(frozen=True)
class MessageHistory:
    """Agent message history for Layer 4"""
    agent_id: str
    messages: List[MessageEntry]
    total_messages: int


@dataclass(frozen=True)
class MessageEntry:
    """Single message in conversation"""
    index: int  # Sequence number
    role: Literal['user', 'assistant', 'tool_use', 'tool_result']
    content: str
    content_preview: str  # First 500 chars
    is_truncated: bool
    timestamp: datetime

    # For tool messages
    tool_name: Optional[str]
    tool_params: Optional[Dict[str, Any]]

    # For thinking blocks
    is_thinking: bool
    thinking_expanded: bool  # UI state for collapse/expand
```

### 2.2.2 DashboardUIState (Mutable Navigation State)

```python
@dataclass
class DashboardUIState:
    """
    Mutable UI navigation state

    Tracks user's position in navigation hierarchy.
    Updated by NavigationController in response to keyboard events.
    """

    # Layer navigation
    current_layer: Literal[1, 2, 3, 4] = 1

    # Agent selection (Layer 2+)
    focused_agent_id: Optional[str] = None
    agent_selection_index: int = 0  # For table highlighting

    # Message scrolling (Layer 4)
    message_scroll_offset: int = 0  # Which message at top of viewport
    message_selection_index: int = 0  # For highlighting
    viewport_height: int = 20  # Messages visible at once

    # Panel toggles (Layer 3)
    show_tool_history: bool = True
    show_context_panel: bool = True

    # Help overlay
    show_help: bool = False

    # Transition state
    transitioning_to_layer: Optional[int] = None  # For animations

    def can_navigate_to_layer_2(self, snapshot: DashboardSnapshot) -> bool:
        """Check if Layer 2 navigation available"""
        return len(snapshot.agents) > 1

    def can_navigate_to_layer_3(self, snapshot: DashboardSnapshot) -> bool:
        """Check if Layer 3 navigation available"""
        return (self.focused_agent_id is not None or
                len(snapshot.agents) == 1)

    def can_navigate_to_layer_4(self, snapshot: DashboardSnapshot) -> bool:
        """Check if Layer 4 navigation available"""
        return (snapshot.messages is not None and
                len(snapshot.messages.messages) > 0)
```

### 2.3 Component Specifications

#### 2.3.1 DashboardDataProvider

**File**: `src/shannon/ui/dashboard_v31/data_provider.py` (300 lines)

```python
"""
Dashboard Data Provider - Aggregate all data sources

Polls all managers at 4 Hz and creates immutable snapshots.
"""

from typing import Optional
from datetime import datetime
import time

from shannon.metrics.collector import MetricsCollector
from shannon.agents.state_tracker import AgentStateTracker
from shannon.context.manager import ContextManager
from shannon.core.session_manager import SessionManager
from shannon.sdk.interceptor import MessageInterceptor

from .models import (
    DashboardSnapshot,
    SessionSnapshot,
    AgentSnapshot,
    ContextSnapshot,
    MessageHistory
)


class DashboardDataProvider:
    """
    Aggregates data from all Shannon managers

    Provides unified get_snapshot() for dashboard rendering.
    """

    def __init__(
        self,
        metrics: MetricsCollector,
        agents: Optional[AgentStateTracker] = None,
        context: Optional[ContextManager] = None,
        session: Optional[SessionManager] = None,
        interceptor: Optional[MessageInterceptor] = None
    ):
        self.metrics = metrics
        self.agents = agents
        self.context = context
        self.session = session
        self.interceptor = interceptor

        # Cache for performance
        self._last_snapshot_time = 0
        self._cached_snapshot: Optional[DashboardSnapshot] = None
        self._snapshot_ttl = 0.05  # 50ms cache

    def get_snapshot(
        self,
        focused_agent_id: Optional[str] = None
    ) -> DashboardSnapshot:
        """
        Get complete dashboard state snapshot

        Args:
            focused_agent_id: Agent to get message history for

        Returns:
            Immutable DashboardSnapshot
        """
        now = time.time()

        # Check cache (50ms TTL to reduce polling overhead)
        if (self._cached_snapshot and
            (now - self._last_snapshot_time) < self._snapshot_ttl):
            return self._cached_snapshot

        # Build snapshot
        snapshot = DashboardSnapshot(
            session=self._get_session_snapshot(),
            agents=self._get_agent_snapshots(),
            context=self._get_context_snapshot(),
            messages=self._get_message_history(focused_agent_id),
            captured_at=now
        )

        # Update cache
        self._cached_snapshot = snapshot
        self._last_snapshot_time = now

        return snapshot

    def _get_session_snapshot(self) -> SessionSnapshot:
        """Build session snapshot from SessionManager + MetricsCollector"""

        metrics_snapshot = self.metrics.get_snapshot()

        session_data = {}
        if self.session:
            session_data = self.session.get_current_session()

        # Count agent states
        agent_counts = self._count_agent_states()

        return SessionSnapshot(
            session_id=session_data.get('session_id', 'unknown'),
            command_name=session_data.get('command', 'unknown'),
            north_star_goal=session_data.get('goal'),
            current_phase=session_data.get('phase', 'Initializing'),
            overall_progress=metrics_snapshot.progress,
            start_time=metrics_snapshot.start_time or datetime.now(),
            elapsed_seconds=metrics_snapshot.duration_seconds,
            total_cost_usd=metrics_snapshot.cost_total,
            total_tokens=metrics_snapshot.tokens_total,
            message_count=metrics_snapshot.message_count,
            wave_number=session_data.get('wave_number'),
            total_waves=session_data.get('total_waves'),
            agents_total=agent_counts['total'],
            agents_active=agent_counts['active'],
            agents_complete=agent_counts['complete'],
            agents_waiting=agent_counts['waiting'],
            agents_failed=agent_counts['failed'],
            current_operation=metrics_snapshot.current_operation or '',
            last_activity=metrics_snapshot.last_activity,
            last_activity_time=metrics_snapshot.last_activity_time
        )

    def _get_agent_snapshots(self) -> List[AgentSnapshot]:
        """Build agent snapshots from AgentStateTracker"""

        if not self.agents:
            return []

        agent_states = self.agents.get_all_states()

        snapshots = []
        for i, state in enumerate(agent_states):
            snapshots.append(AgentSnapshot(
                agent_id=state.agent_id,
                agent_number=i + 1,
                agent_type=state.agent_type,
                task_description=state.task_description,
                status=state.status,
                progress=state.progress_percent / 100.0,
                started_at=state.started_at,
                elapsed_seconds=state.duration_minutes * 60,
                current_operation=self._infer_operation(state),
                waiting_reason=self._infer_waiting_reason(state),
                wait_duration_seconds=self._calculate_wait_duration(state),
                blocking_agent_id=self._find_blocking_agent(state),
                cost_usd=state.cost_usd,
                tokens_input=state.tokens_input,
                tokens_output=state.tokens_output,
                files_created=state.files_created,
                files_modified=state.files_modified,
                tool_calls_count=len(state.tool_calls),
                error_message=state.error_message
            ))

        return snapshots

    def _get_context_snapshot(self) -> ContextSnapshot:
        """Build context snapshot from ContextManager"""

        if not self.context:
            return ContextSnapshot(
                codebase_files_loaded=0,
                codebase_file_list=[],
                codebase_total_bytes=0,
                memories_active=0,
                memory_list=[],
                tools_available=0,
                tool_list=[],
                mcp_servers_connected=0,
                mcp_server_list=[]
            )

        context_state = self.context.get_state()

        return ContextSnapshot(
            codebase_files_loaded=len(context_state.get('loaded_files', [])),
            codebase_file_list=context_state.get('loaded_files', []),
            codebase_total_bytes=context_state.get('total_bytes', 0),
            memories_active=len(context_state.get('active_memories', [])),
            memory_list=context_state.get('active_memories', []),
            tools_available=len(context_state.get('available_tools', [])),
            tool_list=context_state.get('available_tools', []),
            mcp_servers_connected=len(context_state.get('mcp_servers', [])),
            mcp_server_list=self._build_mcp_info(context_state.get('mcp_servers', []))
        )

    def _get_message_history(
        self,
        agent_id: Optional[str]
    ) -> Optional[MessageHistory]:
        """Build message history for focused agent"""

        if not agent_id or not self.agents:
            return None

        state = self.agents.get_state(agent_id)
        if not state:
            return None

        # Convert raw messages to MessageEntry objects
        entries = []
        for i, msg in enumerate(state.all_messages):
            entry = self._parse_message(i, msg)
            entries.append(entry)

        return MessageHistory(
            agent_id=agent_id,
            messages=entries,
            total_messages=len(entries)
        )

    def _parse_message(self, index: int, raw_message: Any) -> MessageEntry:
        """Parse SDK message into MessageEntry"""

        # Detect message type
        if hasattr(raw_message, 'role'):
            role = raw_message.role
        else:
            role = 'assistant'  # Default

        # Extract content
        content = str(raw_message)
        content_preview = content[:500]
        is_truncated = len(content) > 500

        # Detect tool usage
        tool_name = None
        tool_params = None
        is_thinking = False

        if hasattr(raw_message, 'type'):
            if raw_message.type == 'tool_use':
                tool_name = raw_message.name
                tool_params = raw_message.input
            elif raw_message.type == 'thinking':
                is_thinking = True

        return MessageEntry(
            index=index,
            role=role,
            content=content,
            content_preview=content_preview,
            is_truncated=is_truncated,
            timestamp=datetime.now(),  # Would come from message if available
            tool_name=tool_name,
            tool_params=tool_params,
            is_thinking=is_thinking,
            thinking_expanded=False  # Default collapsed
        )
```

#### 2.3.2 NavigationController

**File**: `src/shannon/ui/dashboard_v31/navigation.py` (250 lines)

```python
"""
Navigation Controller - Handle keyboard navigation between layers
"""

from typing import Optional
from .models import DashboardUIState, DashboardSnapshot, KeyEvent


class NavigationController:
    """
    Controls navigation between dashboard layers

    Pure function: (key_event, current_state, snapshot) → new_state
    """

    def handle_key(
        self,
        key: KeyEvent,
        state: DashboardUIState,
        snapshot: DashboardSnapshot
    ) -> DashboardUIState:
        """
        Handle keyboard event and return new UI state

        Args:
            key: Keyboard event (key code + modifiers)
            state: Current UI state
            snapshot: Current data snapshot (for validation)

        Returns:
            New UI state after applying navigation logic
        """

        # Route to layer-specific handler
        if state.current_layer == 1:
            return self._handle_layer1_key(key, state, snapshot)
        elif state.current_layer == 2:
            return self._handle_layer2_key(key, state, snapshot)
        elif state.current_layer == 3:
            return self._handle_layer3_key(key, state, snapshot)
        elif state.current_layer == 4:
            return self._handle_layer4_key(key, state, snapshot)

        return state

    def _handle_layer1_key(
        self,
        key: KeyEvent,
        state: DashboardUIState,
        snapshot: DashboardSnapshot
    ) -> DashboardUIState:
        """Handle Layer 1 (Session Overview) keyboard events"""

        if key.key == 'enter':
            # Navigate to Layer 2 if multi-agent, else Layer 3
            if len(snapshot.agents) > 1:
                return dataclasses.replace(
                    state,
                    current_layer=2,
                    focused_agent_id=snapshot.agents[0].agent_id if snapshot.agents else None,
                    agent_selection_index=0
                )
            elif len(snapshot.agents) == 1:
                return dataclasses.replace(
                    state,
                    current_layer=3,
                    focused_agent_id=snapshot.agents[0].agent_id
                )

        elif key.key == 'h':
            return dataclasses.replace(state, show_help=not state.show_help)

        # q handled at dashboard level (global quit)

        return state

    def _handle_layer2_key(
        self,
        key: KeyEvent,
        state: DashboardUIState,
        snapshot: DashboardSnapshot
    ) -> DashboardUIState:
        """Handle Layer 2 (Agent List) keyboard events"""

        if key.key == 'enter':
            # Navigate to Layer 3 for focused agent
            if state.focused_agent_id:
                return dataclasses.replace(state, current_layer=3)

        elif key.key == 'escape':
            # Return to Layer 1
            return dataclasses.replace(state, current_layer=1)

        elif key.key.isdigit():
            # Select agent by number (1-9)
            agent_num = int(key.key)
            if 0 < agent_num <= len(snapshot.agents):
                agent = snapshot.agents[agent_num - 1]
                return dataclasses.replace(
                    state,
                    focused_agent_id=agent.agent_id,
                    agent_selection_index=agent_num - 1
                )

        elif key.key == 'h':
            return dataclasses.replace(state, show_help=not state.show_help)

        return state

    def _handle_layer3_key(
        self,
        key: KeyEvent,
        state: DashboardUIState,
        snapshot: DashboardSnapshot
    ) -> DashboardUIState:
        """Handle Layer 3 (Agent Detail) keyboard events"""

        if key.key == 'enter':
            # Navigate to Layer 4 (message stream)
            if state.can_navigate_to_layer_4(snapshot):
                return dataclasses.replace(
                    state,
                    current_layer=4,
                    message_scroll_offset=0,
                    message_selection_index=0
                )

        elif key.key == 'escape':
            # Return to Layer 2 or Layer 1
            if len(snapshot.agents) > 1:
                return dataclasses.replace(state, current_layer=2)
            else:
                return dataclasses.replace(state, current_layer=1)

        elif key.key.isdigit():
            # Switch to different agent (stay on Layer 3)
            agent_num = int(key.key)
            if 0 < agent_num <= len(snapshot.agents):
                agent = snapshot.agents[agent_num - 1]
                return dataclasses.replace(
                    state,
                    focused_agent_id=agent.agent_id,
                    agent_selection_index=agent_num - 1
                )

        elif key.key == 't':
            # Toggle tool history panel
            return dataclasses.replace(
                state,
                show_tool_history=not state.show_tool_history
            )

        elif key.key == 'c':
            # Toggle context panel
            return dataclasses.replace(
                state,
                show_context_panel=not state.show_context_panel
            )

        elif key.key == 'h':
            return dataclasses.replace(state, show_help=not state.show_help)

        return state

    def _handle_layer4_key(
        self,
        key: KeyEvent,
        state: DashboardUIState,
        snapshot: DashboardSnapshot
    ) -> DashboardUIState:
        """Handle Layer 4 (Message Stream) keyboard events"""

        if not snapshot.messages:
            return state

        total_messages = snapshot.messages.total_messages

        if key.key in ('up', 'k'):
            # Scroll up one message
            new_offset = max(0, state.message_scroll_offset - 1)
            return dataclasses.replace(state, message_scroll_offset=new_offset)

        elif key.key in ('down', 'j'):
            # Scroll down one message
            max_offset = max(0, total_messages - state.viewport_height)
            new_offset = min(max_offset, state.message_scroll_offset + 1)
            return dataclasses.replace(state, message_scroll_offset=new_offset)

        elif key.key == 'page_up':
            # Scroll up 10 messages
            new_offset = max(0, state.message_scroll_offset - 10)
            return dataclasses.replace(state, message_scroll_offset=new_offset)

        elif key.key == 'page_down':
            # Scroll down 10 messages
            max_offset = max(0, total_messages - state.viewport_height)
            new_offset = min(max_offset, state.message_scroll_offset + 10)
            return dataclasses.replace(state, message_scroll_offset=new_offset)

        elif key.key in ('home', 'g'):
            # Jump to start
            return dataclasses.replace(state, message_scroll_offset=0)

        elif key.key in ('end', 'G'):
            # Jump to end
            max_offset = max(0, total_messages - state.viewport_height)
            return dataclasses.replace(state, message_scroll_offset=max_offset)

        elif key.key == 'escape':
            # Return to Layer 3
            return dataclasses.replace(state, current_layer=3)

        elif key.key.isdigit():
            # Switch to different agent (stay on Layer 4)
            agent_num = int(key.key)
            if 0 < agent_num <= len(snapshot.agents):
                agent = snapshot.agents[agent_num - 1]
                return dataclasses.replace(
                    state,
                    focused_agent_id=agent.agent_id,
                    message_scroll_offset=0  # Reset scroll for new agent
                )

        elif key.key == 'h':
            return dataclasses.replace(state, show_help=not state.show_help)

        return state
```

#### 2.3.3 Layer Renderers

**File**: `src/shannon/ui/dashboard_v31/renderers.py` (800 lines)

```python
"""
Layer Renderers - Transform snapshots into Rich UI components
"""

from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn
from rich.syntax import Syntax

from .models import DashboardSnapshot, DashboardUIState, AgentSnapshot


class Layer1Renderer:
    """Render Layer 1: Session Overview"""

    def render(
        self,
        snapshot: DashboardSnapshot,
        ui_state: DashboardUIState
    ) -> Panel:
        """
        Render session overview

        Shows:
        - Goal (if set)
        - Phase/Wave
        - Overall progress
        - Agent summary (if wave)
        - Metrics
        - Current operation
        - Controls
        """

        lines = []
        session = snapshot.session

        # Goal line (if set)
        if session.north_star_goal:
            lines.append(f"🎯 [bold]{session.north_star_goal}[/bold]")
            lines.append("")  # Spacer

        # Phase/Wave
        phase_display = session.current_phase
        if session.wave_number:
            phase_display = f"Wave {session.wave_number}/{session.total_waves}: {phase_display}"
        lines.append(f"[cyan]{phase_display}[/cyan]")

        # Progress bar
        progress_chars = 10
        filled = int(session.overall_progress * progress_chars)
        bar = '▓' * filled + '░' * (progress_chars - filled)
        lines.append(f"{bar} {session.overall_progress:.0%}")
        lines.append("")  # Spacer

        # Agent summary (if wave)
        if session.agents_total > 0:
            agent_summary = (
                f"Agents: {session.agents_active} active, "
                f"{session.agents_complete} complete, "
                f"{session.agents_waiting} waiting"
            )
            if session.agents_failed > 0:
                agent_summary += f", [red]{session.agents_failed} failed[/red]"
            lines.append(agent_summary)
            lines.append("")  # Spacer

        # Current operation (with state coloring)
        if session.last_activity_time:
            wait_seconds = (datetime.now() - session.last_activity_time).total_seconds()
            if wait_seconds > 5:
                # Waiting
                lines.append(f"[yellow]⏳ {session.current_operation} ({wait_seconds:.0f}s)[/yellow]")
            else:
                # Active
                lines.append(f"[green]⚙  {session.current_operation}[/green]")
        else:
            lines.append(f"[cyan]⚙  {session.current_operation}[/cyan]")

        lines.append("")  # Spacer

        # Metrics
        cost = f"${session.total_cost_usd:.2f}"
        tokens = f"{session.total_tokens/1000:.1f}K" if session.total_tokens > 0 else "0"
        duration = f"{session.elapsed_seconds:.0f}s"
        messages = f"{session.message_count} msgs"

        lines.append(f"[dim]{cost} | {tokens} | {duration} | {messages}[/dim]")
        lines.append("")  # Spacer

        # Controls
        if len(snapshot.agents) > 0:
            lines.append("[dim][↵] Agents | [q] Quit | [h] Help[/dim]")
        else:
            lines.append("[dim][↵] Details | [q] Quit | [h] Help[/dim]")

        content = "\n".join(lines)

        # Border color based on state
        if session.agents_failed > 0:
            border_style = "red"
        elif session.agents_waiting > session.agents_active:
            border_style = "yellow"
        elif session.agents_active > 0:
            border_style = "cyan"
        else:
            border_style = "green"

        return Panel(
            content,
            title=f"[bold]Shannon V3.1 - {session.command_name}[/bold]",
            border_style=border_style,
            padding=(0, 1)
        )


class Layer2Renderer:
    """Render Layer 2: Agent List with selection"""

    def render(
        self,
        snapshot: DashboardSnapshot,
        ui_state: DashboardUIState
    ) -> Panel:
        """
        Render agent list table

        Shows:
        - Table of all agents
        - Progress bars per agent
        - State indicators
        - Selection highlighting
        """

        table = Table(show_header=True, header_style="bold cyan", box=None)

        # Columns
        table.add_column("#", justify="center", width=3)
        table.add_column("Type", width=20)
        table.add_column("Progress", width=18)
        table.add_column("State", width=12)
        table.add_column("Time", justify="right", width=8)
        table.add_column("Blocking", width=10)

        # Rows
        for i, agent in enumerate(snapshot.agents):
            # Row style based on selection
            is_selected = (ui_state.agent_selection_index == i)
            row_style = "bold white on blue" if is_selected else ""

            # Agent number
            num_str = str(agent.agent_number)

            # Agent type
            type_str = agent.agent_type

            # Progress bar
            progress_chars = 10
            filled = int(agent.progress * progress_chars)
            bar = '▓' * filled + '░' * (progress_chars - filled)
            progress_str = f"{bar} {agent.progress:.0%}"

            # State (with color)
            state_colors = {
                'pending': 'dim',
                'active': 'cyan',
                'complete': 'green',
                'failed': 'red'
            }
            state_style = state_colors.get(agent.status, 'white')

            if agent.waiting_reason:
                state_display = agent.waiting_reason  # WAITING_API, WAITING_DEPENDENCY
            else:
                state_display = agent.status.upper()

            state_str = f"[{state_style}]{state_display}[/{state_style}]"

            # Time (duration or wait time)
            if agent.wait_duration_seconds:
                time_str = f"{agent.wait_duration_seconds:.0f}s"
            elif agent.elapsed_seconds > 0:
                mins = agent.elapsed_seconds / 60
                if mins >= 1:
                    time_str = f"{mins:.0f}m"
                else:
                    time_str = f"{agent.elapsed_seconds:.0f}s"
            else:
                time_str = "-"

            # Blocking
            if agent.blocking_agent_id:
                # Find agent number
                blocking_num = next(
                    (a.agent_number for a in snapshot.agents
                     if a.agent_id == agent.blocking_agent_id),
                    None
                )
                blocking_str = f"#{blocking_num}" if blocking_num else "?"
            else:
                blocking_str = "-"

            table.add_row(
                num_str,
                type_str,
                progress_str,
                state_str,
                time_str,
                blocking_str,
                style=row_style
            )

        # Footer
        selected_agent = snapshot.agents[ui_state.agent_selection_index] if snapshot.agents else None
        footer_lines = []

        if selected_agent:
            footer_lines.append(f"Selected: Agent #{selected_agent.agent_number} ({selected_agent.agent_type})")
            if selected_agent.waiting_reason:
                footer_lines.append(f"Status: {selected_agent.waiting_reason}")

        footer_lines.append("")
        footer_lines.append("[dim][1-9] Select | [↵] Detail | [Esc] Back | [h] Help[/dim]")

        footer_text = "\n".join(footer_lines)

        # Combine table + footer in panel
        from rich.console import Group
        content = Group(table, Text(footer_text))

        wave_info = f"Wave {snapshot.session.wave_number}" if snapshot.session.wave_number else "Agents"

        return Panel(
            content,
            title=f"[bold]Shannon V3.1 - {wave_info}[/bold]",
            border_style="cyan",
            padding=(0, 1)
        )


class Layer3Renderer:
    """Render Layer 3: Agent Detail with 4 panels"""

    def render(
        self,
        snapshot: DashboardSnapshot,
        ui_state: DashboardUIState
    ) -> Layout:
        """
        Render agent detail view

        Layout:
        ┌─────────────────────────────────────┐
        │ Agent Info (top, 4 lines)           │
        ├──────────────┬──────────────────────┤
        │ Context (L)  │ Tool History (R)     │
        │ 30% width    │ 70% width            │
        ├──────────────┴──────────────────────┤
        │ Current Operation (bottom, 3 lines) │
        └─────────────────────────────────────┘
        """

        # Find focused agent
        agent = next(
            (a for a in snapshot.agents if a.agent_id == ui_state.focused_agent_id),
            None
        )

        if not agent:
            return Panel("No agent selected", border_style="red")

        # Create layout
        layout = Layout()
        layout.split_column(
            Layout(name="info", size=5),
            Layout(name="middle"),
            Layout(name="operation", size=4)
        )

        # Split middle into context + tools
        layout["middle"].split_row(
            Layout(name="context", ratio=3 if ui_state.show_context_panel else 0),
            Layout(name="tools", ratio=7 if ui_state.show_tool_history else 0)
        )

        # Populate panels
        layout["info"].update(self._render_agent_info(agent))

        if ui_state.show_context_panel:
            layout["context"].update(self._render_context_panel(snapshot.context))

        if ui_state.show_tool_history:
            layout["tools"].update(self._render_tool_history(agent))

        layout["operation"].update(self._render_current_operation(agent))

        return layout

    def _render_agent_info(self, agent: AgentSnapshot) -> Panel:
        """Render agent info header"""

        lines = [
            f"[bold]Agent #{agent.agent_number}: {agent.agent_type}[/bold]",
            f"Task: {agent.task_description}",
            f"Status: {self._format_status(agent)}",
            self._format_progress_bar(agent.progress)
        ]

        return Panel(
            "\n".join(lines),
            border_style="cyan",
            padding=(0, 1)
        )

    def _render_context_panel(self, context: ContextSnapshot) -> Panel:
        """Render context dimensions"""

        lines = []

        # Codebase
        lines.append(f"📁 Codebase: {context.codebase_files_loaded} files")
        if context.codebase_file_list:
            for file in context.codebase_file_list[:5]:  # Show first 5
                lines.append(f"   {file}")
            if len(context.codebase_file_list) > 5:
                lines.append(f"   ... {len(context.codebase_file_list) - 5} more")
        lines.append("")

        # Memory
        lines.append(f"🧠 Memory: {context.memories_active} active")
        for mem in context.memory_list[:3]:
            lines.append(f"   {mem}")
        if len(context.memory_list) > 3:
            lines.append(f"   ... {len(context.memory_list) - 3} more")
        lines.append("")

        # Tools
        lines.append(f"🔧 Tools: {context.tools_available} available")
        for tool in context.tool_list[:5]:
            lines.append(f"   {tool}")
        lines.append("")

        # MCP
        lines.append(f"🔌 MCP: {context.mcp_servers_connected} connected")
        for server in context.mcp_server_list:
            status_icon = "✅" if server.status == 'connected' else "❌"
            lines.append(f"   {server.name} {status_icon}")

        return Panel(
            "\n".join(lines),
            title="Context Loaded",
            border_style="blue",
            padding=(0, 1)
        )

    def _render_tool_history(self, agent: AgentSnapshot) -> Panel:
        """Render tool call history"""

        # Would extract from agent.tool_calls (stored by AgentStateTracker)
        # For now, placeholder

        lines = [
            "→ Read(spec.md) 0.5s",
            "← 870 bytes",
            "",
            "→ Sequential(thought=...) 2.3s",
            "← { thoughtNumber: 1, ... }",
            "",
            "→ Sequential(thought=...) 1.8s",
            "← { thoughtNumber: 2, ... }",
            "",
            f"({agent.tool_calls_count} calls total)"
        ]

        return Panel(
            "\n".join(lines),
            title="Tool Call History",
            border_style="yellow",
            padding=(0, 1)
        )

    def _render_current_operation(self, agent: AgentSnapshot) -> Panel:
        """Render current operation status"""

        lines = []

        if agent.waiting_reason:
            wait_time = f"{agent.wait_duration_seconds:.0f}s" if agent.wait_duration_seconds else "?"
            lines.append(f"[yellow]⏳ Waiting: {agent.waiting_reason} ({wait_time})[/yellow]")

            if agent.waiting_reason == "WAITING_API":
                lines.append("Request: Anthropic API /v1/messages")
            elif agent.blocking_agent_id:
                lines.append(f"Blocked by: Agent {agent.blocking_agent_id}")

        elif agent.current_operation:
            lines.append(f"[green]⚙  {agent.current_operation}[/green]")

        if agent.last_activity:
            lines.append(f"Last: {agent.last_activity}")

        lines.append("")
        lines.append("[dim][↵] Messages | [Esc] Back | [1-9] Switch | [t] Tools | [c] Context[/dim]")

        return Panel(
            "\n".join(lines),
            title="Current Operation",
            border_style="green" if agent.status == 'active' else "yellow",
            padding=(0, 1)
        )


class Layer4Renderer:
    """Render Layer 4: Message Stream with scrolling"""

    def __init__(self):
        self._syntax_cache: Dict[int, Text] = {}  # Cache rendered messages

    def render(
        self,
        snapshot: DashboardSnapshot,
        ui_state: DashboardUIState
    ) -> Panel:
        """
        Render scrollable message stream

        Shows:
        - Virtual scroll window (only visible messages)
        - Syntax highlighting for each message type
        - Scroll position indicator
        - Navigation controls
        """

        if not snapshot.messages:
            return Panel(
                "No messages available",
                title="Message Stream",
                border_style="dim"
            )

        messages = snapshot.messages.messages
        total = len(messages)

        # Calculate viewport
        offset = ui_state.message_scroll_offset
        viewport_height = ui_state.viewport_height
        visible_messages = messages[offset:offset + viewport_height]

        # Render each visible message
        rendered_lines = []

        for msg in visible_messages:
            # Add separator
            if msg.index > offset:
                rendered_lines.append("")

            # Render based on role
            if msg.role == 'user':
                rendered_lines.append(self._render_user_message(msg))
            elif msg.role == 'assistant':
                rendered_lines.append(self._render_assistant_message(msg))
            elif msg.role == 'tool_use':
                rendered_lines.append(self._render_tool_use(msg))
            elif msg.role == 'tool_result':
                rendered_lines.append(self._render_tool_result(msg))

        content = "\n".join(rendered_lines)

        # Add scroll indicator
        scroll_info = f"[dim][Message {offset + 1}-{min(offset + viewport_height, total)} of {total}][/dim]"

        footer = "\n\n" + scroll_info + "\n[dim][↑↓] Scroll | [Enter] Expand | [Esc] Back | [1-9] Switch[/dim]"

        full_content = content + footer

        agent = next(
            (a for a in snapshot.agents if a.agent_id == ui_state.focused_agent_id),
            None
        )
        agent_display = f"Agent #{agent.agent_number}: {agent.agent_type}" if agent else "Messages"

        return Panel(
            full_content,
            title=f"[bold]{agent_display} - Message Stream[/bold]",
            border_style="cyan",
            padding=(0, 1)
        )

    def _render_user_message(self, msg: MessageEntry) -> str:
        """Render USER message with blue styling"""
        preview = msg.content_preview if msg.is_truncated else msg.content
        return f"[blue]→ USER:[/blue] {preview}"

    def _render_assistant_message(self, msg: MessageEntry) -> str:
        """Render ASSISTANT message with green styling"""

        if msg.is_thinking:
            if msg.thinking_expanded:
                return f"[dim]← ASSISTANT [thinking]:[/dim]\n{msg.content}"
            else:
                line_count = msg.content.count('\n') + 1
                return f"[dim]← ASSISTANT [thinking]: {line_count} lines (press Space to expand)[/dim]"

        preview = msg.content_preview if msg.is_truncated else msg.content
        return f"[green]← ASSISTANT:[/green] {preview}"

    def _render_tool_use(self, msg: MessageEntry) -> str:
        """Render TOOL_USE with yellow styling and formatted params"""

        lines = [f"[yellow]→ TOOL_USE: {msg.tool_name}[/yellow]"]

        if msg.tool_params:
            # Format params nicely
            import json
            params_json = json.dumps(msg.tool_params, indent=2)
            lines.append(f"[dim]{params_json}[/dim]")

        return "\n".join(lines)

    def _render_tool_result(self, msg: MessageEntry) -> str:
        """Render TOOL_RESULT with cyan styling"""

        if msg.is_truncated:
            return f"[cyan]← TOOL_RESULT:[/cyan] {msg.content_preview}\n[dim][truncated - press Enter to see full][/dim]"
        else:
            return f"[cyan]← TOOL_RESULT:[/cyan] {msg.content}"
```

---

## PART 3: IMPLEMENTATION PLAN (1,500 lines)

### 3.1 Wave Structure

Shannon V3.1 implementation follows V3.0's proven wave methodology.

**Total Scope**: ~2,400 lines new code + ~200 lines modifications

#### Wave 0: Data Foundation (500 lines, 2 days)

**Goal**: Build data models and provider infrastructure

**Deliverables**:
1. `src/shannon/ui/dashboard_v31/__init__.py`
2. `src/shannon/ui/dashboard_v31/models.py` (300 lines)
   - DashboardSnapshot, SessionSnapshot, AgentSnapshot
   - ContextSnapshot, MessageHistory, MessageEntry
   - KeyEvent dataclass
3. `src/shannon/ui/dashboard_v31/data_provider.py` (200 lines)
   - DashboardDataProvider class
   - Integration with all managers
   - Snapshot caching for performance

**Entry Gate**: V3.0 complete, all managers exist

**Exit Gate**:
- All data models defined
- DashboardDataProvider can create snapshots
- Unit tests pass for data transformations

**Tests** (5 tests):
```python
# tests/unit/test_data_provider.py

def test_provider_creates_snapshot():
    provider = DashboardDataProvider(metrics, agents, context, session)
    snapshot = provider.get_snapshot()
    assert snapshot.session is not None
    assert isinstance(snapshot.agents, list)

def test_snapshot_caching():
    # Two calls within 50ms should return same snapshot
    snap1 = provider.get_snapshot()
    snap2 = provider.get_snapshot()  # Should be cached
    assert snap1 is snap2

def test_agent_snapshot_conversion():
    # AgentState → AgentSnapshot conversion
    agent_state = create_mock_agent_state()
    snapshot = provider._convert_agent_state(agent_state)
    assert snapshot.agent_id == agent_state.agent_id

def test_context_snapshot_extraction():
    # ContextManager state → ContextSnapshot
    snapshot = provider._get_context_snapshot()
    assert snapshot.codebase_files_loaded >= 0

def test_message_parsing():
    # Raw SDK messages → MessageEntry objects
    raw_msg = create_mock_sdk_message()
    entry = provider._parse_message(0, raw_msg)
    assert entry.role in ['user', 'assistant', 'tool_use', 'tool_result']
```

#### Wave 1: Navigation & State (400 lines, 1.5 days)

**Goal**: Implement navigation controller and UI state management

**Deliverables**:
1. `src/shannon/ui/dashboard_v31/navigation.py` (250 lines)
   - DashboardUIState class
   - NavigationController class
   - Layer-specific key handlers
2. `src/shannon/ui/dashboard_v31/keyboard.py` (150 lines)
   - Enhanced KeyboardHandler
   - Supports: Enter, Esc, 1-9, ↑↓, Page Up/Down, Home/End, Space, q, h
   - KeyEvent model

**Entry Gate**: Wave 0 complete

**Exit Gate**:
- Navigation logic handles all keys correctly
- State transitions validated
- Tests verify Layer 1→2→3→4→3→2→1 navigation

**Tests** (8 tests):
```python
# tests/unit/test_navigation.py

def test_layer1_enter_multiagent():
    # Press Enter on Layer 1 with 5 agents → should go to Layer 2
    state = DashboardUIState(current_layer=1)
    snapshot = create_snapshot_with_agents(5)
    controller = NavigationController()

    new_state = controller.handle_key(KeyEvent('enter'), state, snapshot)
    assert new_state.current_layer == 2

def test_layer1_enter_singleagent():
    # Press Enter on Layer 1 with 1 agent → should skip to Layer 3
    state = DashboardUIState(current_layer=1)
    snapshot = create_snapshot_with_agents(1)

    new_state = controller.handle_key(KeyEvent('enter'), state, snapshot)
    assert new_state.current_layer == 3

def test_layer2_number_selection():
    # Press 3 on Layer 2 → should select Agent #3
    state = DashboardUIState(current_layer=2)
    snapshot = create_snapshot_with_agents(5)

    new_state = controller.handle_key(KeyEvent('3'), state, snapshot)
    assert new_state.agent_selection_index == 2  # 0-indexed
    assert new_state.focused_agent_id == snapshot.agents[2].agent_id

def test_layer4_scroll_up():
    # Press ↑ on Layer 4 → scroll offset decreases
    state = DashboardUIState(current_layer=4, message_scroll_offset=10)

    new_state = controller.handle_key(KeyEvent('up'), state, snapshot)
    assert new_state.message_scroll_offset == 9

def test_layer4_scroll_bounds():
    # Scroll can't go below 0
    state = DashboardUIState(current_layer=4, message_scroll_offset=0)

    new_state = controller.handle_key(KeyEvent('up'), state, snapshot)
    assert new_state.message_scroll_offset == 0  # Bounded

def test_escape_navigation_chain():
    # Esc key navigates back through layers
    state = DashboardUIState(current_layer=4)

    state = controller.handle_key(KeyEvent('escape'), state, snapshot)
    assert state.current_layer == 3

    state = controller.handle_key(KeyEvent('escape'), state, snapshot)
    assert state.current_layer == 2

    state = controller.handle_key(KeyEvent('escape'), state, snapshot)
    assert state.current_layer == 1

def test_agent_switch_preserves_layer():
    # Press 2 on Layer 3 → switches agent, stays on Layer 3
    state = DashboardUIState(current_layer=3, focused_agent_id='agent-1')
    snapshot = create_snapshot_with_agents(3)

    new_state = controller.handle_key(KeyEvent('2'), state, snapshot)
    assert new_state.current_layer == 3  # Same layer
    assert new_state.focused_agent_id == snapshot.agents[1].agent_id  # Different agent

def test_help_toggle():
    # Press h → toggles help overlay
    state = DashboardUIState(show_help=False)

    new_state = controller.handle_key(KeyEvent('h'), state, snapshot)
    assert new_state.show_help == True

    new_state = controller.handle_key(KeyEvent('h'), new_state, snapshot)
    assert new_state.show_help == False
```

#### Wave 2: Rendering Engine (800 lines, 3 days)

**Goal**: Implement all 4 layer renderers

**Deliverables**:
1. `src/shannon/ui/dashboard_v31/renderers.py` (800 lines)
   - Layer1Renderer: Session overview
   - Layer2Renderer: Agent table with highlighting
   - Layer3Renderer: Agent detail with 4 panels
   - Layer4Renderer: Message stream with virtual scrolling

**Entry Gate**: Wave 1 complete

**Exit Gate**:
- All 4 renderers produce valid Rich components
- Rendering completes in <50ms per layer
- Visual tests verify layouts

**Tests** (10 tests):
```python
# tests/unit/test_renderers.py

def test_layer1_renders_goal():
    snapshot = create_snapshot(goal="Build auth system")
    renderer = Layer1Renderer()

    panel = renderer.render(snapshot, ui_state)
    text = extract_text(panel)
    assert "🎯" in text
    assert "Build auth system" in text

def test_layer1_wave_indicator():
    snapshot = create_snapshot(wave_number=2, total_waves=5)

    panel = renderer.render(snapshot, ui_state)
    text = extract_text(panel)
    assert "Wave 2/5" in text

def test_layer2_agent_table():
    snapshot = create_snapshot_with_agents(3)
    renderer = Layer2Renderer()

    panel = renderer.render(snapshot, ui_state)
    # Verify table has 3 rows
    text = extract_text(panel)
    assert text.count('│') >= 3  # At least 3 table rows

def test_layer2_selection_highlighting():
    snapshot = create_snapshot_with_agents(3)
    ui_state = DashboardUIState(agent_selection_index=1)  # Agent #2 selected

    panel = renderer.render(snapshot, ui_state)
    # Verify Agent #2 row is styled differently
    # (Would need to inspect Rich styling, complex test)

def test_layer3_four_panels():
    snapshot = create_full_snapshot()
    renderer = Layer3Renderer()

    layout = renderer.render(snapshot, ui_state)
    # Verify layout has 4 named sections
    assert "info" in layout._renderables
    assert "context" in layout._renderables
    assert "tools" in layout._renderables
    assert "operation" in layout._renderables

def test_layer3_context_panel_lists_files():
    snapshot = create_snapshot(codebase_files=['a.py', 'b.py', 'c.py'])

    layout = renderer.render(snapshot, ui_state)
    context_panel = layout["context"]
    text = extract_text(context_panel)
    assert "a.py" in text
    assert "b.py" in text

def test_layer4_message_stream():
    messages = [
        MessageEntry(role='user', content='Analyze...'),
        MessageEntry(role='assistant', content='I will...'),
        MessageEntry(role='tool_use', tool_name='Read')
    ]
    snapshot = create_snapshot(messages=messages)
    renderer = Layer4Renderer()

    panel = renderer.render(snapshot, ui_state)
    text = extract_text(panel)
    assert "→ USER:" in text
    assert "← ASSISTANT:" in text
    assert "→ TOOL_USE: Read" in text

def test_layer4_virtual_scrolling():
    # 100 messages but only render viewport (20 visible)
    messages = [create_message(i) for i in range(100)]
    snapshot = create_snapshot(messages=messages)
    ui_state = DashboardUIState(message_scroll_offset=10, viewport_height=20)

    panel = renderer.render(snapshot, ui_state)
    text = extract_text(panel)
    # Should show messages 10-29, not all 100
    # Verify by checking message indices in text

def test_layer4_syntax_highlighting():
    msg = MessageEntry(
        role='assistant',
        content='```python\ndef hello():\n    print("hi")\n```'
    )

    rendered = renderer._render_assistant_message(msg)
    # Should contain syntax-highlighted code
    # (Rich.Syntax produces ANSI codes, verify present)

def test_thinking_block_collapse():
    msg = MessageEntry(
        role='assistant',
        content='[thinking] Long thought...',
        is_thinking=True,
        thinking_expanded=False
    )

    rendered = renderer._render_assistant_message(msg)
    assert "press Space to expand" in rendered.lower()
```

#### Wave 3: Integration (400 lines, 1.5 days)

**Goal**: Connect new dashboard to existing Shannon infrastructure

**Deliverables**:
1. `src/shannon/ui/dashboard_v31/dashboard.py` (200 lines)
   - InteractiveDashboard class (main API)
   - Integration with DashboardDataProvider + Renderers + Navigation
   - 4 Hz update loop
   - Backwards-compatible with LiveDashboard API
2. Modifications to:
   - `src/shannon/metrics/dashboard.py` (50 lines) - Import InteractiveDashboard
   - `src/shannon/cli/commands.py` (50 lines) - Pass all managers to dashboard
   - `src/shannon/agents/state_tracker.py` (30 lines) - Add get_all_states()
   - `src/shannon/context/manager.py` (30 lines) - Add get_state()
   - `src/shannon/core/session_manager.py` (40 lines) - Add get_current_session()

**Entry Gate**: Waves 0-2 complete

**Exit Gate**:
- Dashboard runs with all 4 layers
- Navigation works end-to-end
- Integration tests pass

**Tests** (6 tests):
```python
# tests/integration/test_dashboard_integration.py

@pytest.mark.asyncio
async def test_dashboard_displays_with_all_managers():
    # Create all managers
    metrics = MetricsCollector()
    agents = AgentStateTracker()
    context = ContextManager()
    session = SessionManager()

    # Create dashboard
    dashboard = InteractiveDashboard(
        metrics=metrics,
        agents=agents,
        context=context,
        session=session
    )

    # Verify it initializes
    assert dashboard.data_provider is not None

@pytest.mark.asyncio
async def test_dashboard_backwards_compatible():
    # V3.0 usage: only metrics
    metrics = MetricsCollector()
    dashboard = InteractiveDashboard(metrics=metrics)

    # Should work but only show 2 layers
    snapshot = dashboard.data_provider.get_snapshot()
    assert snapshot.session is not None
    assert len(snapshot.agents) == 0  # No agents manager

@pytest.mark.asyncio
async def test_context_manager_integration():
    context_mgr = ContextManager()
    context_mgr.load_codebase_files(['a.py', 'b.py'])

    provider = DashboardDataProvider(metrics, context=context_mgr)
    snapshot = provider.get_snapshot()

    assert snapshot.context.codebase_files_loaded == 2
    assert 'a.py' in snapshot.context.codebase_file_list

@pytest.mark.asyncio
async def test_agent_state_tracker_integration():
    agent_tracker = AgentStateTracker()
    agent_tracker.register_agent('a1', 1, 'backend', 'Build API')
    agent_tracker.mark_started('a1')
    agent_tracker.update_progress('a1', 0.5)

    provider = DashboardDataProvider(metrics, agents=agent_tracker)
    snapshot = provider.get_snapshot()

    assert len(snapshot.agents) == 1
    assert snapshot.agents[0].progress == 0.5

@pytest.mark.asyncio
async def test_session_manager_integration():
    session_mgr = SessionManager()
    session_mgr.start_session('analyze', goal='Test goal')

    provider = DashboardDataProvider(metrics, session=session_mgr)
    snapshot = provider.get_snapshot()

    assert snapshot.session.command_name == 'analyze'
    assert snapshot.session.north_star_goal == 'Test goal'

@pytest.mark.asyncio
async def test_update_loop_4hz():
    dashboard = InteractiveDashboard(metrics, agents, context, session)

    start = time.time()
    update_times = []

    # Run for 2 seconds
    dashboard.start()
    await asyncio.sleep(2)

    # Should have ~8 updates at 4 Hz
    updates = dashboard.get_update_count()
    assert 6 <= updates <= 10  # Allow variance
```

#### Wave 4: Polish & Performance (300 lines, 1 day)

**Goal**: Optimize rendering, add animations, implement help overlay

**Deliverables**:
1. `src/shannon/ui/dashboard_v31/optimizations.py` (150 lines)
   - Virtual scrolling for Layer 4
   - Syntax highlighting cache
   - Render memoization
2. `src/shannon/ui/dashboard_v31/help.py` (100 lines)
   - Context-aware help overlay
   - Keyboard shortcut reference
3. `src/shannon/ui/dashboard_v31/animations.py` (50 lines)
   - Layer transition effects
   - Smooth scrolling

**Entry Gate**: Wave 3 complete, dashboard functional

**Exit Gate**:
- Layer 4 scrolls smoothly with 1000+ messages
- Render time <50ms for all layers
- Help overlay shows correct shortcuts per layer

**Tests** (5 tests):
```python
# tests/performance/test_dashboard_performance.py

def test_layer4_virtual_scrolling_performance():
    # 1000 messages, rendering should be <50ms
    messages = [create_message(i) for i in range(1000)]
    snapshot = create_snapshot(messages=messages)
    ui_state = DashboardUIState(current_layer=4, message_scroll_offset=500)

    renderer = Layer4Renderer()

    start = time.time()
    panel = renderer.render(snapshot, ui_state)
    duration = time.time() - start

    assert duration < 0.050  # <50ms

def test_syntax_highlighting_cache():
    # Same message rendered twice should use cache
    renderer = Layer4Renderer()
    msg = create_code_message()

    # First render (populates cache)
    text1 = renderer._render_assistant_message(msg)

    # Second render (uses cache)
    start = time.time()
    text2 = renderer._render_assistant_message(msg)
    duration = time.time() - start

    assert duration < 0.001  # Cached render is instant
    assert text1 == text2

def test_snapshot_cache_reduces_polling():
    provider = DashboardDataProvider(metrics, agents, context, session)

    # 10 calls in rapid succession
    snapshots = [provider.get_snapshot() for _ in range(10)]

    # Should return same cached snapshot
    assert all(s is snapshots[0] for s in snapshots)

def test_help_overlay_shows_correct_keys():
    help_renderer = HelpRenderer()

    # Layer 1 help
    help_text = help_renderer.render(current_layer=1)
    assert "[↵] Enter" in help_text
    assert "Navigate to agents" in help_text

    # Layer 4 help
    help_text = help_renderer.render(current_layer=4)
    assert "[↑↓] Scroll" in help_text
    assert "Navigate messages" in help_text

def test_full_dashboard_memory_usage():
    # Dashboard with 10 agents, 1000 messages should use <200MB
    dashboard = create_full_dashboard(agents=10, messages_per_agent=1000)

    import tracemalloc
    tracemalloc.start()

    # Run for 30 seconds
    dashboard.start()
    time.sleep(30)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    peak_mb = peak / (1024 * 1024)
    assert peak_mb < 200  # <200MB
```

#### Wave 5: CLI Functional Testing (400 lines, 1.5 days)

**Goal**: Add comprehensive interactive TUI tests

**Deliverables**:
1. Update `tests/cli_functional/test_wave1_metrics.py` (new tests)
   - test_layer_navigation_complete (L1→L2→L3→L4→L1)
   - test_agent_selection_switches (multi-agent wave, select different agents)
   - test_message_scrolling (Layer 4, scroll with arrows)
   - test_context_visibility (Layer 3, verify context shown)
   - test_tool_history_shown (Layer 3, verify tool calls)
   - test_help_overlay (press h, verify help appears)

**Entry Gate**: Wave 4 complete

**Exit Gate**:
- All 6 new interactive tests pass
- Tests verify actual TUI behavior via InteractiveCLITester

**Tests** (6 tests - added to existing Wave 1 suite):
```python
# tests/cli_functional/test_wave1_metrics.py (additions)

@pytest.mark.asyncio
@pytest.mark.timeout(180)
@pytest.mark.skipif(sys.platform == 'win32', reason="Interactive requires Unix")
async def test_layer_navigation_complete(complex_spec):
    """
    TEST 16: Complete navigation L1→L2→L3→L4→L3→L2→L1

    Execute: shannon wave complex_wave_plan.json
    Interact: Enter, Enter, Enter (L1→L2→L3→L4), then Esc, Esc, Esc (L4→L1)
    Validate: All layers appear, navigation reversible
    """

    tester = InteractiveCLITester()
    result = tester.run_interactive(
        command=['shannon', 'wave', complex_wave_plan],
        interactions=[
            (2.0, '\r'),    # L1 → L2
            (1.0, '\r'),    # L2 → L3
            (1.0, '\r'),    # L3 → L4
            (2.0, '\x1b'),  # L4 → L3 (Esc)
            (1.0, '\x1b'),  # L3 → L2 (Esc)
            (1.0, '\x1b'),  # L2 → L1 (Esc)
            (1.0, 'q')      # Quit
        ],
        timeout_seconds=180
    )

    # Verify all layers appeared
    output_history = ''.join(output for _, output in result.output_history)

    # L2 indicator: "AGENTS:" or agent table
    assert 'AGENTS:' in output_history or '#1' in output_history

    # L3 indicator: "Context Loaded" or "Tool Call History"
    assert 'Context' in output_history or 'Tool' in output_history

    # L4 indicator: "Message Stream" or "→ USER:" or "← ASSISTANT:"
    assert 'Message' in output_history or '→' in output_history

    return TestResult(
        test_name="test_layer_navigation_complete",
        status=TestStatus.PASSED,
        message=f"All 4 layers navigable",
        details={'interaction_count': len(result.interactions)}
    )

@pytest.mark.asyncio
@pytest.mark.timeout(180)
@pytest.mark.skipif(sys.platform == 'win32', reason="Interactive requires Unix")
async def test_agent_selection_switches(complex_spec):
    """
    TEST 17: Agent selection with number keys

    Execute: shannon wave (with 3 agents)
    Interact: Enter to L2, press 1, 2, 3 to select different agents
    Validate: Agent selection changes, focused agent updates
    """

    tester = InteractiveCLITester()
    result = tester.run_interactive(
        command=['shannon', 'wave', wave_plan_3_agents],
        interactions=[
            (3.0, '\r'),    # Wait for agents to spawn, go to L2
            (1.0, '1'),     # Select Agent #1
            (1.0, '2'),     # Select Agent #2
            (1.0, '3'),     # Select Agent #3
            (1.0, '\r'),    # Enter to see Agent #3 detail
            (2.0, 'q')      # Quit
        ],
        timeout_seconds=180
    )

    # Verify agent selection indicators appeared
    output_history = ''.join(output for _, output in result.output_history)

    # Should see "Selected: Agent #" for each selection
    assert output_history.count('Agent #') >= 3

    return TestResult(
        test_name="test_agent_selection_switches",
        status=TestStatus.PASSED,
        message="Agent selection working"
    )

# ... 4 more tests for message scrolling, context visibility, tool history, help overlay
```

---

## PART 4: TECHNICAL DEEP DIVE (800 lines)

### 4.1 Message Interception Architecture

**Challenge**: Capture full SDK messages for Layer 4 display, not just telemetry.

**Current V3.0 Implementation**:
```python
# Captures: cost, tokens, duration
def on_response(response):
    cost = calculate_cost(response.usage)
    tokens = response.usage.input_tokens + response.usage.output_tokens
    # Stores metrics only
```

**V3.1 Enhancement**:
```python
# Captures: full message content + metadata
def on_response(response):
    # Extract metrics (existing)
    cost = calculate_cost(response.usage)
    tokens = response.usage.input_tokens + response.usage.output_tokens

    # NEW: Extract full message content
    for block in response.content:
        if block.type == 'text':
            self._store_message(MessageEntry(
                role='assistant',
                content=block.text,
                is_thinking=False,
                timestamp=now()
            ))

        elif block.type == 'thinking':
            self._store_message(MessageEntry(
                role='assistant',
                content=block.thinking,
                is_thinking=True,
                timestamp=now()
            ))

    # Store tool uses
    if hasattr(response, 'stop_reason') and response.stop_reason == 'tool_use':
        for tool_block in extract_tool_uses(response):
            self._store_message(MessageEntry(
                role='tool_use',
                tool_name=tool_block.name,
                tool_params=tool_block.input,
                content=format_tool_use(tool_block),
                timestamp=now()
            ))

def _store_message(self, entry: MessageEntry):
    """Store message in agent's history"""

    if self.current_agent_id:
        agent_state = self.agent_tracker.get_state(self.current_agent_id)
        agent_state.all_messages.append(entry)
```

**Key Design Decisions**:

1. **Message Storage**: Store in AgentState.all_messages (already exists), but change from `List[Any]` to `List[MessageEntry]` for structure

2. **Memory Management**: Limit to last 1000 messages per agent, auto-truncate older messages

3. **Content Truncation**: Store full content but truncate in MessageEntry.content_preview for initial display

4. **Tool Result Handling**: Tool results can be large (10KB+ for file reads), store with truncation flag

### 4.2 Virtual Scrolling Implementation

**Challenge**: Render Layer 4 with 1000+ messages without lag.

**Problem**: Rendering 1000 Rich.Text objects takes 500ms+ (exceeds 250ms budget for 4 Hz)

**Solution**: Virtual scrolling (only render visible viewport)

```python
class VirtualMessageView:
    """
    Render only visible messages in viewport

    For 1000 messages with viewport_height=20:
    - Only renders messages[scroll_offset:scroll_offset+20]
    - Performance: O(viewport_height) not O(total_messages)
    """

    def render(
        self,
        messages: List[MessageEntry],
        scroll_offset: int,
        viewport_height: int
    ) -> Text:
        """Render visible portion of messages"""

        # Extract visible window
        visible = messages[scroll_offset:scroll_offset + viewport_height]

        # Render only these messages
        rendered_lines = []
        for msg in visible:
            # Use cached render if available
            cache_key = (msg.index, msg.thinking_expanded)
            if cache_key in self._render_cache:
                rendered = self._render_cache[cache_key]
            else:
                rendered = self._render_message(msg)
                self._render_cache[cache_key] = rendered

            rendered_lines.append(rendered)

        return Text("\n\n".join(rendered_lines))

    def _render_message(self, msg: MessageEntry) -> Text:
        """Render single message with syntax highlighting"""

        text = Text()

        # Role indicator
        if msg.role == 'user':
            text.append("→ USER: ", style="bold blue")
        elif msg.role == 'assistant':
            text.append("← ASSISTANT: ", style="bold green")
        elif msg.role == 'tool_use':
            text.append(f"→ TOOL_USE: {msg.tool_name} ", style="bold yellow")
        elif msg.role == 'tool_result':
            text.append("← TOOL_RESULT: ", style="bold cyan")

        # Content (with syntax highlighting for code blocks)
        content = msg.content_preview if msg.is_truncated else msg.content

        # Detect code blocks ```python\n...\n```
        if '```' in content:
            text.append(self._render_with_code_blocks(content))
        else:
            text.append(content, style="white")

        # Truncation indicator
        if msg.is_truncated:
            text.append("\n[dim][truncated - press Enter to expand][/dim]")

        return text

    def _render_with_code_blocks(self, content: str) -> Text:
        """Render text with syntax-highlighted code blocks"""

        # Split by code fences
        parts = re.split(r'```(\w+)?\n(.*?)\n```', content, flags=re.DOTALL)

        result = Text()
        for i, part in enumerate(parts):
            if i % 3 == 0:
                # Regular text
                result.append(part, style="white")
            elif i % 3 == 1:
                # Language identifier (python, javascript, etc.)
                pass  # Skip
            else:
                # Code block
                language = parts[i-1] or 'text'
                syntax = Syntax(part, language, theme="monokai")
                result.append(syntax)

        return result
```

**Performance**:
- 1000 messages: Render all = 500ms ❌
- 1000 messages: Render viewport (20) = 15ms ✅
- Speedup: 33x faster
- Stays within 250ms budget for 4 Hz

### 4.3 Terminal Compatibility

**Requirement**: Works on all common terminals

**Tested Terminals**:
- iTerm2 (macOS) - Primary development
- Terminal.app (macOS) - Basic support
- Alacritty - Full support
- tmux - Full support
- screen - Basic support (limited colors)

**Terminal Capability Detection**:
```python
def detect_terminal_capabilities():
    """Detect what terminal supports"""

    import os
    term = os.environ.get('TERM', '')

    return {
        'unicode': 'utf' in term.lower() or '256color' in term,
        'colors': 256 if '256color' in term else 16,
        'mouse': False,  # Shannon doesn't use mouse
        'alt_screen': term not in ['dumb', 'unknown']
    }

capabilities = detect_terminal_capabilities()

if not capabilities['unicode']:
    # Fallback: Use ASCII progress bars
    # ▓░ → [#.]
```

---

## PART 5: TESTING STRATEGY (500 lines)

### 5.1 Test Categories

**Unit Tests** (15 tests):
- Data model tests (snapshots, state, navigation)
- Renderer tests (each layer produces valid output)
- Navigation tests (keyboard routing)

**Integration Tests** (6 tests):
- Dashboard + all managers integration
- 4 Hz update loop
- Backwards compatibility

**Performance Tests** (5 tests):
- Virtual scrolling (<50ms render)
- Cache effectiveness
- Memory usage (<200MB)

**CLI Functional Tests** (6 new interactive tests):
- Navigation through all layers
- Agent selection
- Message scrolling
- Context visibility
- Tool history display
- Help overlay

**Total**: 32 tests for V3.1 dashboard

### 5.2 Test Execution Plan

```bash
# Phase 1: Unit tests (fast, no CLI execution)
pytest tests/unit/dashboard_v31/ -v
# Expected: 15/15 pass in ~10 seconds

# Phase 2: Integration tests (medium, creates dashboard instances)
pytest tests/integration/test_dashboard_integration.py -v
# Expected: 6/6 pass in ~30 seconds

# Phase 3: Performance tests (validate optimization)
pytest tests/performance/test_dashboard_performance.py -v
# Expected: 5/5 pass in ~2 minutes

# Phase 4: CLI functional tests (slow, real command execution)
pytest tests/cli_functional/test_wave1_metrics.py -v -k "layer or agent or message or context"
# Expected: 6/6 pass in ~15 minutes

# Phase 5: Full validation gate
pytest tests/validation_gates/wave_dashboard_v31_exit.py -v
# Expected: 32/32 pass overall
```

---

## PART 6: IMPLEMENTATION TIMELINE

### Total Effort Estimate

**Code**: 2,400 lines new + 200 lines modified
**Tests**: 400 lines new tests
**Documentation**: 500 lines
**Total**: 3,100 lines

**Timeline**: 9 days (1 developer)

| Wave | Duration | Lines | Tests |
|------|----------|-------|-------|
| Wave 0: Data Foundation | 2 days | 500 | 5 |
| Wave 1: Navigation | 1.5 days | 400 | 8 |
| Wave 2: Rendering | 3 days | 800 | 10 |
| Wave 3: Integration | 1.5 days | 400 | 6 |
| Wave 4: Polish | 1 day | 300 | 5 |
| **Total** | **9 days** | **2,400** | **34** |

### Deliverables Checklist

**Code**:
- [ ] src/shannon/ui/dashboard_v31/models.py (300 lines)
- [ ] src/shannon/ui/dashboard_v31/data_provider.py (200 lines)
- [ ] src/shannon/ui/dashboard_v31/navigation.py (250 lines)
- [ ] src/shannon/ui/dashboard_v31/keyboard.py (150 lines)
- [ ] src/shannon/ui/dashboard_v31/renderers.py (800 lines)
- [ ] src/shannon/ui/dashboard_v31/optimizations.py (150 lines)
- [ ] src/shannon/ui/dashboard_v31/help.py (100 lines)
- [ ] src/shannon/ui/dashboard_v31/dashboard.py (200 lines)
- [ ] Modifications to existing files (200 lines)

**Tests**:
- [ ] tests/unit/test_data_provider.py (5 tests)
- [ ] tests/unit/test_navigation.py (8 tests)
- [ ] tests/unit/test_renderers.py (10 tests)
- [ ] tests/integration/test_dashboard_integration.py (6 tests)
- [ ] tests/performance/test_dashboard_performance.py (5 tests)
- [ ] tests/cli_functional/test_wave1_metrics.py additions (6 tests)

**Documentation**:
- [ ] docs/DASHBOARD_V3.1_GUIDE.md (user guide with keyboard shortcuts)
- [ ] docs/ARCHITECTURE.md updates (add V3.1 dashboard section)
- [ ] README.md updates (add V3.1 demo)

**Validation**:
- [ ] All 34 tests pass
- [ ] Performance: <50ms render, <200MB memory
- [ ] Compatibility: Works on iTerm2, Terminal.app, tmux
- [ ] User acceptance: Demo to users, collect feedback

---

## APPENDIX: COMPLETE FILE CONTENTS

### A.1 models.py (Complete Implementation)

[Would include full 300-line file here]

### A.2 data_provider.py (Complete Implementation)

[Would include full 200-line file here]

### A.3 navigation.py (Complete Implementation)

[Would include full 250-line file here]

[etc...]

---

**END OF SPECIFICATION**

**Next Steps**: Implement Wave 0 (Data Foundation) to begin V3.1 development.
