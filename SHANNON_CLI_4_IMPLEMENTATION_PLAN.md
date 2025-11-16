# Shannon CLI v4.0: Complete Implementation Plan
## Building the Interactive Orchestration System

**Based On**: shannon-cli-4.md (2,503 lines, complete specification)
**Analysis**: SHANNON_CLI_4_GAP_ANALYSIS.md (100 ultrathink thoughts)
**Current State**: V3.5 executor modules (3,435 lines, reusable as skills)
**Target**: Full interactive orchestration system with skills framework
**Timeline**: 8-10 weeks (recommended: Hybrid Approach - Option B)
**Date**: 2025-11-15

---

## 🎯 Vision Statement

Transform Shannon CLI from a standalone executor into a **Quad Code-level interactive orchestration system** with:
- ✨ Skills framework (discover, compose, auto-generate)
- 🎛️ Real-time dashboard (6 panels, WebSocket streaming)
- 🎮 Interactive steering (HALT/RESUME/ROLLBACK in <100ms)
- 🧠 Specialized modes (do/debug/ultrathink/research)
- 🤖 Multi-agent coordination (parallel execution)
- 🔄 State management (time-travel debugging)

---

## 📐 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   Shannon CLI v4.0                      │
│            Interactive Orchestration System             │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ FRONTEND (React/TypeScript)                             │
├─────────────────────────────────────────────────────────┤
│ • Dashboard (6 panels)                                  │
│ • WebSocket client (Socket.io)                         │
│ • Interactive controls (HALT/RESUME/ROLLBACK/etc.)     │
│ • Real-time updates (<50ms latency)                    │
└─────────────────────────────────────────────────────────┘
                         ↕ WebSocket
┌─────────────────────────────────────────────────────────┐
│ BACKEND (Python - reuse existing + new infrastructure) │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ ┌─ SKILLS FRAMEWORK ────────────────────────────────┐  │
│ │ • Registry & Catalog (YAML skills)                 │  │
│ │ • Auto-Discovery Engine                            │  │
│ │ • Executor with Hooks (pre/post/error)             │  │
│ │ • Dependency Resolver                              │  │
│ │ • Dynamic Generator (pattern-based)                │  │
│ │ • Built-in Skills:                                 │  │
│ │   ├─ library_discovery (← LibraryDiscoverer)      │  │
│ │   ├─ validation (← ValidationOrchestrator)         │  │
│ │   ├─ git_ops (← GitManager)                        │  │
│ │   └─ prompt_enhance (← PromptEnhancer)             │  │
│ └───────────────────────────────────────────────────────┘  │
│                                                          │
│ ┌─ ORCHESTRATION ───────────────────────────────────┐  │
│ │ • Task Parser (intent → skills)                    │  │
│ │ • Execution Planner (skill selection/ordering)     │  │
│ │ • Agent Coordinator (multi-agent management)       │  │
│ │ • State Manager (checkpoints/rollback)             │  │
│ │ • Decision Engine (autonomous + human approval)    │  │
│ └───────────────────────────────────────────────────────┘  │
│                                                          │
│ ┌─ COMMUNICATION ───────────────────────────────────┐  │
│ │ • WebSocket Server (Socket.io/Python)              │  │
│ │ • Event Bus (pub/sub for system events)            │  │
│ │ • Command Queue (priority-based user commands)     │  │
│ │ • State Broadcaster (dashboard synchronization)    │  │
│ └───────────────────────────────────────────────────────┘  │
│                                                          │
│ ┌─ SPECIALIZED MODES ───────────────────────────────┐  │
│ │ • Debug Mode Engine (sequential + halts)           │  │
│ │ • Ultrathink Engine (500+ step reasoning)          │  │
│ │ • Research Orchestrator (Fire Crawl + Tavali)      │  │
│ │ • Hypothesis Generator & Evaluator                 │  │
│ └───────────────────────────────────────────────────────┘  │
│                                                          │
│ ┌─ COMMANDS (CLI Entry Points) ─────────────────────┐  │
│ │ • shannon do "task" (universal executor)           │  │
│ │ • shannon debug "task" (sequential analysis)       │  │
│ │ • shannon ultrathink "task" (deep reasoning)       │  │
│ │ • shannon research "topic" (knowledge gathering)   │  │
│ │ • shannon validate (comprehensive + skills)        │  │
│ └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 📅 10-Week Implementation Roadmap

### WEEK 1: Skills Framework Foundation

**Goal**: Basic skills can be defined, discovered, and executed

**Deliverables**:
- [ ] Skill schema definition (`schemas/skill.schema.json`)
- [ ] Skill registry (`src/shannon/skills/registry.py` - 500 lines)
- [ ] YAML/JSON loader (`src/shannon/skills/loader.py` - 400 lines)
- [ ] Basic skill executor (`src/shannon/skills/executor.py` - 600 lines)
- [ ] Simple hook system (`src/shannon/skills/hooks.py` - 300 lines)

**Testing**:
- [ ] Load skill from YAML
- [ ] Execute skill successfully
- [ ] Pre/post hooks trigger correctly
- [ ] Error hooks trigger on failure

**Skill Definitions to Create**:
```yaml
# skills/built-in/library_discovery.yaml
skill:
  name: library_discovery
  description: Discover npm/PyPI libraries
  execution:
    type: native
    module: shannon.executor.library_discoverer
    class: LibraryDiscoverer
    method: discover_for_feature
```

**Exit Criteria**:
- Can define skill in YAML
- Can load and execute skill
- Hooks work correctly

---

### WEEK 2: Auto-Discovery & Dependencies

**Goal**: Skills auto-discovered from multiple sources, dependencies resolved

**Deliverables**:
- [ ] Auto-discovery engine (`src/shannon/skills/discovery.py` - 800 lines)
  - Scans: .shannon/skills/, ~/.shannon/skills/
  - Parses: package.json scripts, Makefile targets
  - Queries: Connected MCPs for capabilities
- [ ] Dependency resolver (`src/shannon/skills/dependencies.py` - 400 lines)
  - Builds dependency graph
  - Detects circular dependencies (fails if found)
  - Determines execution order
  - Optimizes parallel execution opportunities
- [ ] Skill catalog persistence (`src/shannon/skills/catalog.py` - 300 lines)
  - Save/load from Memory MCP
  - Cache for performance
  - Invalidation on changes

**Testing**:
- [ ] Discovers skills from .shannon/skills/
- [ ] Resolves dependencies correctly
- [ ] Detects circular dependencies
- [ ] Builds valid execution order

**Exit Criteria**:
- Auto-discovery working from multiple sources
- Dependency resolution functional
- Catalog persists to Memory MCP

---

### WEEK 3: WebSocket Server & Event Streaming

**Goal**: Real-time communication infrastructure working

**Deliverables**:
- [ ] WebSocket server (`src/shannon/communication/websocket_server.py` - 800 lines)
  - Socket.io server
  - Connection management
  - Room/namespace support
  - Heartbeat/reconnection
- [ ] Event system (`src/shannon/communication/events.py` - 400 lines)
  - Event types defined
  - Event bus (pub/sub)
  - Event serialization
  - Rate limiting (prevent flooding)
- [ ] Command handler (`src/shannon/communication/commands.py` - 300 lines)
  - Receives commands from dashboard
  - Validates and routes
  - Priority queue
  - Response handling

**Event Types**:
```python
class EventType(Enum):
    SKILL_STARTED = "skill:started"
    SKILL_COMPLETED = "skill:completed"
    SKILL_FAILED = "skill:failed"
    FILE_MODIFIED = "file:modified"
    DECISION_POINT = "decision:point"
    VALIDATION_RESULT = "validation:result"
    AGENT_SPAWNED = "agent:spawned"
    AGENT_PROGRESS = "agent:progress"
    STATE_SNAPSHOT = "state:snapshot"
```

**Testing**:
- [ ] WebSocket connects/disconnects
- [ ] Events stream to clients
- [ ] Commands received from clients
- [ ] <50ms event latency

**Exit Criteria**:
- WebSocket server running
- Bidirectional communication working
- Event streaming validated

---

### WEEK 4: Dashboard Frontend (Core 3 Panels)

**Goal**: Basic dashboard showing real-time execution

**Technology**: React + TypeScript + Tailwind CSS

**Deliverables**:
- [ ] Dashboard app setup (`dashboard/` - new directory)
  - Create React App or Vite
  - TypeScript configuration
  - Socket.io client setup
- [ ] Panel 1: Execution Overview (`dashboard/src/panels/ExecutionOverview.tsx` - 400 lines)
  - Task name, status, progress bar
  - Timing (started, elapsed, ETA)
  - Controls: HALT, RESUME buttons
- [ ] Panel 2: Skills Orchestration (`dashboard/src/panels/SkillsView.tsx` - 600 lines)
  - Active/queued/completed skills
  - Per-skill status with progress
  - Actions: INSPECT, PAUSE
- [ ] Panel 3: File Changes (`dashboard/src/panels/FileDiff.tsx` - 800 lines)
  - Live diff with syntax highlighting
  - Actions: APPROVE, REVERT
  - File tree navigator
- [ ] WebSocket integration (`dashboard/src/services/websocket.ts` - 400 lines)
  - Connect to backend
  - Handle events
  - Send commands
  - State synchronization

**Testing**:
- [ ] Dashboard loads and connects
- [ ] Shows skill execution in real-time
- [ ] File changes display correctly
- [ ] HALT button stops execution

**Exit Criteria**:
- 3-panel dashboard functional
- Real-time updates working
- Basic controls (HALT/RESUME) working

---

### WEEK 5: shannon do Command + State Management

**Goal**: Universal task executor with rollback capability

**Deliverables**:
- [ ] shannon do command (`src/shannon/cli/commands/do.py` - 400 lines)
  - CLI interface with Click
  - Task parsing
  - Calls orchestration layer
  - Streams to WebSocket
- [ ] Orchestration layer (`src/shannon/orchestration/` - 2,000 lines)
  - Task parser (intent → skills mapping)
  - Execution planner (skill selection/ordering)
  - Skill invoker (execute with events)
  - Error handling
- [ ] State manager (`src/shannon/orchestration/state_manager.py` - 600 lines)
  - Create checkpoints before each skill
  - Snapshot: filesystem, git state, execution context
  - Restore: Rollback to any checkpoint
  - Verification: Ensure restored correctly
- [ ] ROLLBACK functionality
  - Dashboard button
  - WebSocket command
  - State restoration
  - Event notification

**Testing**:
- [ ] shannon do "simple task" completes successfully
- [ ] Skills execute in order
- [ ] Can HALT mid-execution
- [ ] Can ROLLBACK to previous step
- [ ] State correctly restored

**Exit Criteria**:
- shannon do command working
- State snapshots created
- Rollback functional

---

### WEEK 6: Agent Coordination

**Goal**: Multi-agent parallel execution

**Deliverables**:
- [ ] Agent coordinator (`src/shannon/orchestration/agent_coordinator.py` - 700 lines)
  - Agent pool (8 active / 50 max)
  - Role assignment (Research, Analysis, Testing, etc.)
  - Dependency tracking (agents wait for dependencies)
  - Progress monitoring
  - Lifecycle management (spawn/terminate)
- [ ] Agent types implementation:
  - ResearchAgent (Fire Crawl execution)
  - AnalysisAgent (code analysis)
  - TestingAgent (run tests)
  - ValidationAgent (validate results)
  - GitAgent (git operations)
  - MonitoringAgent (system health)
- [ ] Dashboard Panel 3: Sub-Agent Activity (`dashboard/src/panels/AgentPool.tsx` - 500 lines)
  - List active agents
  - Progress bars per agent
  - Actions: INSPECT, SPAWN, TERMINATE

**Testing**:
- [ ] Spawn multiple agents
- [ ] Agents execute in parallel
- [ ] Dependencies handled correctly
- [ ] Dashboard shows agent status
- [ ] Can terminate agent mid-execution

**Exit Criteria**:
- Multi-agent execution working
- Parallel skills execution functional
- Agent pool visible in dashboard

---

### WEEK 7: shannon debug Command

**Goal**: Sequential analysis mode with halt points

**Deliverables**:
- [ ] Debug mode engine (`src/shannon/modes/debug_mode.py` - 1,500 lines)
  - Sequential execution
  - Automatic halts at decision points
  - Depth levels (standard/detailed/ultra/trace)
  - Investigation tools:
    - inspect state
    - show reasoning
    - list alternatives
    - test hypothesis
    - inject constraint
    - explain decision
- [ ] shannon debug command (`src/shannon/cli/commands/debug.py` - 300 lines)
  - CLI interface
  - Depth level selection
  - Resume from step
  - Focus area filtering
- [ ] Debug dashboard view (`dashboard/src/views/DebugMode.tsx` - 800 lines)
  - Step-by-step visualization
  - Reasoning chain display
  - Investigation tool UI
  - State inspector

**Testing**:
- [ ] Debug mode halts at decision points
- [ ] Can inspect state while halted
- [ ] Investigation tools work
- [ ] Can inject constraints
- [ ] Can continue execution

**Exit Criteria**:
- shannon debug command working
- Halts at decision points
- Investigation tools functional

---

### WEEK 8: Decision Engine & Full Dashboard

**Goal**: Human-in-the-loop decision making, complete dashboard

**Deliverables**:
- [ ] Decision engine (`src/shannon/orchestration/decision_engine.py` - 400 lines)
  - Decision point detection
  - Option generation (with pros/cons/confidence)
  - User presentation via WebSocket
  - Timeout handling (auto-decide after N seconds)
  - History tracking
- [ ] Dashboard Panel 4: Decision Points (`dashboard/src/panels/Decisions.tsx` - 400 lines)
  - Show context and question
  - Display options with details
  - Capture user selection
  - Show recommendation
- [ ] Dashboard Panel 5: Validation Stream (`dashboard/src/panels/Validation.tsx` - 400 lines)
  - Live test output
  - Code quality metrics
  - Performance results
  - Actions: PAUSE TESTS, VIEW FAILURES
- [ ] Complete steering controls:
  - REDIRECT with re-planning
  - Context injection UI
  - APPROVE/OVERRIDE for decisions

**Testing**:
- [ ] Decision points presented to user
- [ ] User can select options
- [ ] Execution continues with chosen option
- [ ] Validation streams to dashboard
- [ ] All steering controls work

**Exit Criteria**:
- All 6 dashboard panels working
- Decision points functional
- Complete steering control

---

### WEEK 9: shannon ultrathink & shannon research Commands

**Goal**: Deep reasoning and knowledge gathering modes

**Deliverables**:
- [ ] Ultrathink engine (`src/shannon/modes/ultrathink.py` - 1,800 lines)
  - 500+ step reasoning (Sequential MCP)
  - Problem decomposition
  - Hypothesis generation (3+ hypotheses)
  - Multi-hypothesis evaluation
  - Comparison matrix
  - Decision tree visualization
  - Research orchestration integration
- [ ] Research orchestrator (`src/shannon/research/orchestrator.py` - 1,200 lines)
  - Fire Crawl integration
  - Tavali integration
  - Web search coordination
  - Knowledge synthesis
  - Pattern extraction
  - Best practices compilation
- [ ] shannon ultrathink command (`src/shannon/cli/commands/ultrathink.py` - 200 lines)
- [ ] shannon research command (`src/shannon/cli/commands/research.py` - 200 lines)
- [ ] Ultrathink dashboard view (`dashboard/src/views/Ultrathink.tsx` - 1,000 lines)
  - Reasoning tree visualization
  - Hypothesis comparison matrix
  - Research progress tracking
  - Decision tree display

**Testing**:
- [ ] Ultrathink generates 500+ thoughts
- [ ] Multiple hypotheses created
- [ ] Comparison matrix accurate
- [ ] Research finds relevant sources
- [ ] Knowledge synthesized correctly

**Exit Criteria**:
- shannon ultrathink working
- shannon research working
- Deep analysis before execution proven

---

### WEEK 10: Dynamic Skills, Pattern Detection, Polish

**Goal**: Self-improving system, production ready

**Deliverables**:
- [ ] Pattern detector (`src/shannon/skills/pattern_detector.py` - 600 lines)
  - Command history analysis (last 1000 commands)
  - Repeated sequence detection (≥3 occurrences)
  - Automation value scoring
  - Suggestion generation
- [ ] Dynamic skill generator (`src/shannon/skills/generator.py` - 700 lines)
  - Analyze command patterns
  - Extract parameters and variations
  - Determine dependencies
  - Generate YAML skill definition
  - User notification with ACCEPT/DECLINE
- [ ] Performance monitoring (`src/shannon/skills/performance.py` - 300 lines)
  - Track: Execution time, success rate, usage count
  - Per-skill metrics
  - Optimization suggestions
  - Dashboard metrics panel
- [ ] Polish & Refinement:
  - Error messages improvement
  - Dashboard UX refinement
  - Performance optimization
  - Documentation completion
  - Tutorial creation

**Testing**:
- [ ] Pattern detection finds repeated commands
- [ ] Dynamic skill creation works
- [ ] Generated skills execute correctly
- [ ] Performance metrics accurate
- [ ] Full system end-to-end tested

**Exit Criteria**:
- Dynamic skill creation working
- Pattern detection functional
- System performant and stable
- Ready for beta release

---

## 🗂️ File Structure (New)

```
shannon-cli/
├── src/shannon/
│   ├── skills/                    # NEW: Skills Framework
│   │   ├── __init__.py
│   │   ├── registry.py           # Skill registry (500 lines)
│   │   ├── loader.py             # YAML/JSON loader (400 lines)
│   │   ├── executor.py           # Skill executor (1,000 lines)
│   │   ├── hooks.py              # Hook system (600 lines)
│   │   ├── discovery.py          # Auto-discovery (800 lines)
│   │   ├── dependencies.py       # Dependency resolver (400 lines)
│   │   ├── catalog.py            # Catalog persistence (300 lines)
│   │   ├── pattern_detector.py  # Pattern detection (600 lines)
│   │   ├── generator.py          # Dynamic generation (700 lines)
│   │   └── performance.py        # Performance tracking (300 lines)
│   │
│   ├── orchestration/            # NEW: Orchestration Layer
│   │   ├── __init__.py
│   │   ├── task_parser.py        # Intent parsing (500 lines)
│   │   ├── planner.py            # Execution planning (800 lines)
│   │   ├── agent_coordinator.py  # Multi-agent (700 lines)
│   │   ├── state_manager.py      # Snapshots/rollback (600 lines)
│   │   └── decision_engine.py    # Decision making (400 lines)
│   │
│   ├── communication/            # NEW: Communication Layer
│   │   ├── __init__.py
│   │   ├── websocket_server.py   # Socket.io server (800 lines)
│   │   ├── events.py             # Event bus (400 lines)
│   │   ├── commands.py           # Command queue (300 lines)
│   │   └── broadcaster.py        # State broadcasting (400 lines)
│   │
│   ├── modes/                    # NEW: Specialized Modes
│   │   ├── __init__.py
│   │   ├── debug_mode.py         # Debug engine (1,500 lines)
│   │   ├── ultrathink.py         # Ultrathink engine (1,800 lines)
│   │   └── investigation.py      # Investigation tools (400 lines)
│   │
│   ├── research/                 # NEW: Research Layer
│   │   ├── __init__.py
│   │   ├── orchestrator.py       # Research orchestration (1,200 lines)
│   │   ├── fire_crawl.py         # Fire Crawl integration (400 lines)
│   │   ├── tavali.py             # Tavali integration (300 lines)
│   │   ├── web_search.py         # Web research (300 lines)
│   │   └── synthesizer.py        # Knowledge synthesis (400 lines)
│   │
│   ├── cli/commands/             # UPDATED: New Commands
│   │   ├── do.py                 # NEW: shannon do (400 lines)
│   │   ├── debug.py              # NEW: shannon debug (300 lines)
│   │   ├── ultrathink.py         # NEW: shannon ultrathink (200 lines)
│   │   ├── research.py           # NEW: shannon research (200 lines)
│   │   ├── validate.py           # UPDATED: Add skills testing (300 lines)
│   │   └── exec.py               # KEEP: May deprecate later
│   │
│   └── executor/                 # EXISTING: Becomes Built-in Skills
│       └── (Keep all existing files as skill implementations)
│
├── dashboard/                     # NEW: React Dashboard
│   ├── package.json
│   ├── tsconfig.json
│   ├── src/
│   │   ├── App.tsx               # Main app (200 lines)
│   │   ├── panels/               # Dashboard panels
│   │   │   ├── ExecutionOverview.tsx  (400 lines)
│   │   │   ├── SkillsView.tsx         (600 lines)
│   │   │   ├── AgentPool.tsx          (500 lines)
│   │   │   ├── FileDiff.tsx           (800 lines)
│   │   │   ├── Decisions.tsx          (400 lines)
│   │   │   └── Validation.tsx         (400 lines)
│   │   ├── services/
│   │   │   └── websocket.ts      # WebSocket client (400 lines)
│   │   ├── store/               # State management
│   │   │   └── index.ts          # Zustand store (600 lines)
│   │   └── components/          # Shared components
│   │       └── (various)         (1,200 lines)
│   └── public/
│
├── skills/                       # NEW: Skill Definitions
│   ├── built-in/                # Built-in skills (YAML)
│   │   ├── library_discovery.yaml
│   │   ├── validation_orchestrator.yaml
│   │   ├── git_operations.yaml
│   │   ├── prompt_enhancement.yaml
│   │   └── (more built-ins)
│   └── README.md                # Skill development guide
│
└── schemas/                     # NEW: Schemas
    └── skill.schema.json        # Skill definition schema
```

**New Lines**: ~16,000 lines total across all new files

---

## 🔧 Technology Stack

### Backend (Python)

**Existing**:
- Python 3.10+
- Claude Agent SDK
- Click (CLI)
- Pydantic (models)
- Rich (TUI - keep for fallback)

**New**:
- python-socketio (WebSocket server)
- aiofiles (async file operations)
- PyYAML (skill definitions)
- jsonschema (skill validation)
- networkx (dependency graphs)

### Frontend (NEW)

**Framework**:
- React 18+ (or Vue 3 if preferred)
- TypeScript (type safety)
- Vite (build tool)

**Libraries**:
- Socket.io-client (WebSocket)
- Zustand or Redux (state management)
- React Router (navigation)
- Tailwind CSS (styling)
- Monaco Editor (code diff display)
- Recharts (metrics visualization)
- Framer Motion (animations)

---

## 🧪 Testing Strategy

### Week 1-2 (Skills Framework)
- Unit tests: Skill loading, execution, hooks
- Integration tests: Multi-skill workflows
- Test skills: Create sample skills in YAML

### Week 3-4 (Communication & Dashboard)
- E2E tests: Playwright tests for dashboard
- WebSocket tests: Connection, events, commands
- Latency tests: Measure <50ms requirement

### Week 5-6 (Orchestration & Agents)
- Orchestration tests: shannon do end-to-end
- Rollback tests: State restoration verification
- Agent tests: Multi-agent coordination

### Week 7-8 (Debug & Decision)
- Debug mode tests: Halt/investigate/continue
- Decision engine tests: Option presentation/selection
- Full UI tests: All 6 panels

### Week 9-10 (Advanced Modes & Polish)
- Ultrathink tests: 500+ step reasoning
- Research tests: Fire Crawl/Tavali integration
- Performance tests: Load testing, stress testing
- Security tests: WebSocket security, input validation

---

## 🎬 Quick Start Implementation (Week 1 Details)

### Day 1-2: Skill Schema & Registry

**File**: `schemas/skill.schema.json`
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["name", "version", "description", "execution"],
  "properties": {
    "name": {"type": "string", "pattern": "^[a-z][a-z0-9_]*$"},
    "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
    "description": {"type": "string"},
    "category": {"type": "string"},
    "parameters": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "type"],
        "properties": {
          "name": {"type": "string"},
          "type": {"enum": ["string", "integer", "boolean", "array", "object"]},
          "required": {"type": "boolean"},
          "default": {},
          "validation": {"type": "string"}
        }
      }
    },
    "dependencies": {
      "type": "array",
      "items": {"type": "string"}
    },
    "hooks": {
      "type": "object",
      "properties": {
        "pre": {"type": "array", "items": {"type": "string"}},
        "post": {"type": "array", "items": {"type": "string"}},
        "error": {"type": "array", "items": {"type": "string"}}
      }
    },
    "execution": {
      "type": "object",
      "required": ["type"],
      "properties": {
        "type": {"enum": ["script", "mcp", "composite", "native"]},
        "script": {"type": "string"},
        "mcp": {"type": "string"},
        "module": {"type": "string"},
        "class": {"type": "string"},
        "method": {"type": "string"},
        "timeout": {"type": "integer"},
        "retry": {"type": "integer"}
      }
    }
  }
}
```

**File**: `src/shannon/skills/registry.py`
```python
from typing import Dict, List, Optional
from pathlib import Path
import yaml
import jsonschema

class SkillRegistry:
    """Central registry for all skills"""

    def __init__(self, schema_path: Path):
        self.schema = self._load_schema(schema_path)
        self.skills: Dict[str, Skill] = {}
        self.catalog_path: Optional[Path] = None

    def register(self, skill_def: Dict) -> None:
        """Register a skill from definition"""
        # Validate against schema
        jsonschema.validate(skill_def, self.schema)

        # Create Skill object
        skill = Skill.from_dict(skill_def)

        # Check for conflicts
        if skill.name in self.skills:
            raise ValueError(f"Skill '{skill.name}' already registered")

        # Add to registry
        self.skills[skill.name] = skill

    def get(self, name: str) -> Optional[Skill]:
        """Get skill by name"""
        return self.skills.get(name)

    def list_all(self) -> List[Skill]:
        """List all registered skills"""
        return list(self.skills.values())

    def find_by_category(self, category: str) -> List[Skill]:
        """Find skills by category"""
        return [s for s in self.skills.values() if s.category == category]
```

### Day 3-4: Skill Loader & Basic Executor

**File**: `src/shannon/skills/loader.py`
```python
import yaml
from pathlib import Path
from typing import List

class SkillLoader:
    """Load skills from YAML/JSON files"""

    def __init__(self, registry: SkillRegistry):
        self.registry = registry

    def load_from_file(self, skill_file: Path) -> Skill:
        """Load single skill from file"""
        with open(skill_file) as f:
            if skill_file.suffix == '.yaml' or skill_file.suffix == '.yml':
                skill_def = yaml.safe_load(f)
            elif skill_file.suffix == '.json':
                skill_def = json.load(f)
            else:
                raise ValueError(f"Unsupported file type: {skill_file.suffix}")

        # Register skill
        self.registry.register(skill_def)

        return self.registry.get(skill_def['name'])

    def load_from_directory(self, skills_dir: Path) -> List[Skill]:
        """Load all skills from directory"""
        skills = []
        for skill_file in skills_dir.glob('**/*.yaml'):
            try:
                skill = self.load_from_file(skill_file)
                skills.append(skill)
            except Exception as e:
                logger.error(f"Failed to load {skill_file}: {e}")

        return skills
```

**File**: `src/shannon/skills/executor.py`
```python
class SkillExecutor:
    """Execute skills with hooks"""

    async def execute(
        self,
        skill: Skill,
        parameters: Dict,
        context: ExecutionContext
    ) -> SkillResult:
        """Execute skill with full hook support"""

        # Create checkpoint for rollback
        checkpoint = await context.state_manager.create_checkpoint()

        try:
            # Execute PRE-hooks
            for hook_name in skill.hooks.pre:
                await self._execute_hook(hook_name, parameters, context)

            # Execute MAIN skill
            result = await self._execute_main(skill, parameters, context)

            # Execute POST-hooks (on success)
            for hook_name in skill.hooks.post:
                await self._execute_hook(hook_name, parameters, context)

            return SkillResult(success=True, data=result)

        except Exception as e:
            # Execute ERROR-hooks
            for hook_name in skill.hooks.error:
                await self._execute_hook(hook_name, parameters, context)

            # Rollback to checkpoint
            await context.state_manager.restore_checkpoint(checkpoint)

            return SkillResult(success=False, error=str(e))
```

### Day 5: First Skill Definitions

**File**: `skills/built-in/library_discovery.yaml`
```yaml
skill:
  name: library_discovery
  version: 1.0.0
  description: Discover and recommend open-source libraries
  category: research

  parameters:
    - name: feature_description
      type: string
      required: true
      description: Feature or functionality needed

    - name: category
      type: string
      required: false
      default: "general"
      description: Category for better search

  execution:
    type: native
    module: shannon.executor.library_discoverer
    class: LibraryDiscoverer
    method: discover_for_feature
    timeout: 30
    retry: 2

  hooks:
    post:
      - cache_results_in_serena

  metadata:
    author: Shannon Framework
    auto_generated: false
```

**File**: `skills/built-in/validation_orchestrator.yaml`
```yaml
skill:
  name: validation_orchestrator
  version: 1.0.0
  description: 3-tier validation (static, tests, functional)
  category: validation

  parameters:
    - name: changes
      type: object
      required: true
      description: Changes to validate

  execution:
    type: native
    module: shannon.executor.validator
    class: ValidationOrchestrator
    method: validate_all_tiers
    timeout: 300

  hooks:
    pre:
      - ensure_test_environment
    post:
      - save_validation_report
    error:
      - collect_failure_logs
```

---

## 🔄 Migration Strategy for Existing Code

### Executor Modules → Built-in Skills

**Step 1**: Keep all Python modules as-is
**Step 2**: Create YAML wrappers in `skills/built-in/`
**Step 3**: Skills Framework calls existing Python code
**Step 4**: No code rewrite needed initially

**Example Flow**:
```
User: shannon do "find authentication libraries"
  ↓
shannon do command parses intent
  ↓
Skills Framework resolves to: library_discovery skill
  ↓
Skill executor loads: skills/built-in/library_discovery.yaml
  ↓
Executes: LibraryDiscoverer.discover_for_feature("authentication")
  ↓
Returns: List of libraries (FastAPI-users, django-allauth, etc.)
```

**Benefit**: Existing code becomes instantly usable through new architecture!

### shannon exec Command

**Options**:
1. **Keep as alias**: `shannon exec` → `shannon do` (backward compatibility)
2. **Deprecate**: Remove in V4.0, migrate users to `shannon do`
3. **Repurpose**: Use for simple tasks, `shannon do` for complex

**Recommendation**: Keep as alias for backward compatibility

---

## 🚀 Accelerated Timeline (Parallel Development)

If multiple developers available:

**Team Structure**:
- **Dev 1**: Skills Framework (Weeks 1-2)
- **Dev 2**: WebSocket + Backend Communication (Week 3)
- **Dev 3**: React Dashboard Frontend (Weeks 3-4)
- **Dev 4**: Orchestration Layer (Week 5)
- **Integration**: Weeks 6-8
- **Specialized Modes**: Weeks 9-10

**Parallel Timeline**: 6-8 weeks (vs 10 weeks sequential)

---

## 📊 Success Metrics (from Spec)

### Skills Framework
- [ ] Skill Discovery Rate: ≥95% of available skills found
- [ ] Hook Reliability: 100% hook triggering
- [ ] Dynamic Creation Success: ≥80% of suggested skills useful
- [ ] Skill Execution Speed: <5s average overhead
- [ ] Dependency Resolution: 100% successful

### Interactive Steering
- [ ] Halt Response Time: <100ms
- [ ] Rollback Reliability: 100% state restoration
- [ ] Dashboard Latency: <50ms event streaming
- [ ] Decision Point Handling: 100% user input captured
- [ ] Redirect Success: ≥90% successful re-planning

### Overall System
- [ ] Task Success Rate: ≥85% completed successfully
- [ ] User Intervention Rate: <20% (most tasks auto)
- [ ] Time to Completion: 10-20 min average
- [ ] System Uptime: ≥99.9%
- [ ] User Satisfaction: ≥8/10 rating

---

## 🎯 MVP Definition (Minimum Viable Product)

**If timeline constrained, deliver MVP first:**

**MVP Scope** (6 weeks):
1. ✅ Skills Framework (registry, loader, executor, hooks)
2. ✅ shannon do command (basic orchestration)
3. ✅ WebSocket communication
4. ✅ Dashboard (3 panels: Overview, Skills, Files)
5. ✅ Basic controls (HALT/RESUME)
6. ✅ Wrap existing modules as 4 built-in skills

**Defer to V4.1**:
- Agent coordination (multi-agent parallel)
- Debug mode (sequential analysis)
- Ultrathink mode (500+ reasoning)
- Research orchestrator
- Dynamic skill generation
- Full 6-panel dashboard

**MVP Value**: Users can define skills, orchestrate tasks, monitor in real-time, HALT execution

---

## 🚦 Implementation Checkpoints

### Checkpoint 1 (End of Week 2): Skills Framework
- [ ] Can define skill in YAML
- [ ] Can load skill from file
- [ ] Can execute skill with hooks
- [ ] Can resolve dependencies
- [ ] Can discover skills from .shannon/skills/

**Demo**: Load and execute library_discovery skill

### Checkpoint 2 (End of Week 4): Dashboard + Communication
- [ ] WebSocket server running
- [ ] Dashboard connects and shows execution
- [ ] Events stream to dashboard
- [ ] Can HALT execution from dashboard

**Demo**: Run task, watch in dashboard, click HALT button

### Checkpoint 3 (End of Week 6): Orchestration
- [ ] shannon do command working
- [ ] Multi-skill orchestration
- [ ] State snapshots created
- [ ] Can ROLLBACK to previous state

**Demo**: shannon do "complex task", rollback mid-execution

### Checkpoint 4 (End of Week 8): Full Interactive
- [ ] All 6 panels working
- [ ] Decision points presented
- [ ] Full steering control
- [ ] Agent coordination functional

**Demo**: Complex task with agents, decisions, file changes - full interactivity

### Checkpoint 5 (End of Week 10): Complete System
- [ ] All commands working (do/debug/ultrathink/research/validate)
- [ ] Dynamic skill creation
- [ ] Production ready
- [ ] Documentation complete

**Demo**: Full workflow demonstrating all capabilities

---

## ⚠️ Risks & Mitigation

### Risk 1: WebSocket Performance
**Concern**: <50ms latency requirement may be challenging
**Mitigation**: Use Socket.io with binary serialization, benchmark early (Week 3)

### Risk 2: State Snapshots Overhead
**Concern**: Creating checkpoints every skill may slow execution
**Mitigation**: Async snapshots, optimize for common cases, make configurable

### Risk 3: Technology Stack Mismatch
**Concern**: Spec wants TypeScript, we built Python backend
**Mitigation**: Python backend + React frontend (hybrid), TypeScript only for dashboard

### Risk 4: Complexity of Skills Framework
**Concern**: Dependency resolution, hook execution may have edge cases
**Mitigation**: Comprehensive testing, start simple, add complexity gradually

### Risk 5: Dashboard Development Effort
**Concern**: 5,000 lines of React could take longer
**Mitigation**: Use UI component library (shadcn/ui), start with 3 panels (MVP)

---

## 💰 Effort Estimation

### By Role (Assuming parallel work):

**Backend Engineer** (6 weeks):
- Skills Framework: 2 weeks
- Orchestration Layer: 2 weeks
- Specialized Modes: 2 weeks

**Frontend Engineer** (4 weeks):
- Dashboard Setup: 1 week
- Core Panels (3): 2 weeks
- Full Dashboard (6 panels): 1 week

**Full-Stack Engineer** (4 weeks):
- WebSocket Communication: 1 week
- Agent Coordination: 1 week
- Integration: 2 weeks

**Total**: 14 person-weeks = ~3.5 person-months

**If solo developer**: 10 weeks sequential

---

## 📚 Documentation Requirements

### User Documentation
- [ ] Getting Started Guide
- [ ] Skills Development Tutorial
- [ ] Dashboard User Guide
- [ ] Command Reference (do/debug/ultrathink/research/validate)
- [ ] Troubleshooting Guide

### Developer Documentation
- [ ] Architecture Overview
- [ ] Skills Framework API
- [ ] WebSocket Protocol Specification
- [ ] Dashboard Component Guide
- [ ] Contributing Guidelines

### Tutorials
- [ ] Creating Your First Skill
- [ ] Building Composite Skills
- [ ] Using Debug Mode
- [ ] Research Orchestration
- [ ] Dashboard Customization

---

## 🎁 Deliverables by Week

| Week | Deliverable | Value | Demo |
|------|-------------|-------|------|
| 1 | Skill registry + loader | Can define skills | Load YAML skill |
| 2 | Auto-discovery + deps | Skills discovered | Auto-find skills |
| 3 | WebSocket server | Real-time events | Event streaming |
| 4 | Basic dashboard | Visual monitoring | See execution live |
| 5 | shannon do command | Orchestration | Multi-skill task |
| 6 | Agent coordination | Parallel execution | 3 agents running |
| 7 | shannon debug | Investigation | Halt and inspect |
| 8 | Full dashboard | Complete steering | All controls work |
| 9 | Ultrathink + research | Deep analysis | 500-step reasoning |
| 10 | Dynamic skills + polish | Self-improving | Auto-create skill |

---

## 🔑 Critical Success Factors

1. **Start with Skills Framework** - Everything builds on this foundation
2. **Test Early** - WebSocket latency must be proven Week 3
3. **Incremental Delivery** - Working features each week
4. **Reuse Existing Code** - Don't throw away 3,435 lines
5. **Dashboard is Key** - Visual feedback drives user value
6. **State Management** - Rollback capability critical for trust
7. **Documentation** - Users need clear skill development guide

---

## 🎯 Recommendation: START WITH WEEK 1

**Immediate Next Steps** (Week 1, Days 1-5):

**Day 1**:
- [ ] Create `schemas/skill.schema.json`
- [ ] Create `src/shannon/skills/__init__.py`
- [ ] Create `src/shannon/skills/models.py` (Skill, SkillResult classes)

**Day 2**:
- [ ] Implement `src/shannon/skills/registry.py` (500 lines)
- [ ] Write tests for registry
- [ ] Test: Register skill from dict

**Day 3**:
- [ ] Implement `src/shannon/skills/loader.py` (400 lines)
- [ ] Write tests for loader
- [ ] Test: Load skill from YAML file

**Day 4**:
- [ ] Implement `src/shannon/skills/executor.py` (600 lines)
- [ ] Implement `src/shannon/skills/hooks.py` (300 lines)
- [ ] Write tests for execution

**Day 5**:
- [ ] Create `skills/built-in/library_discovery.yaml`
- [ ] Create `skills/built-in/validation_orchestrator.yaml`
- [ ] Test: Execute library_discovery skill
- [ ] Verify: Hooks execute correctly

**Week 1 Exit**: Can define skills in YAML and execute them with hooks!

---

**Status**: Ready to begin implementation
**Next**: Await user approval on Option A/B/C/D, then start Week 1

