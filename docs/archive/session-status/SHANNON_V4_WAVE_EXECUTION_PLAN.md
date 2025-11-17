# Shannon CLI v4.0: Wave-Based Execution Plan
## Interactive Orchestration System (Python-Based)

**Created**: 2025-11-15
**Based On**: shannon-cli-4.md (2,503 lines, complete specification)
**Ultrathink**: 100+ sequential thoughts completed
**Architecture**: Hybrid Python (backend) + React (dashboard)
**Timeline**: 10 waves / 8-10 weeks
**Current Assets**: 3,435 lines (executor modules) → Reuse as built-in skills

---

## 🎯 Vision & Scope

**Transform Shannon CLI into Quad Code-level interactive orchestration system**:
- ✨ Skills framework (auto-discovery, hooks, composability)
- 🎛️ Real-time dashboard (6 panels, WebSocket <50ms latency)
- 🎮 Interactive steering (HALT/RESUME/ROLLBACK <100ms)
- 🧠 Specialized modes (do/debug/ultrathink/research)
- 🤖 Multi-agent coordination (8 agents, parallel execution)
- 🔄 State management (time-travel debugging)

**Technology Stack**:
- **Backend**: Python 3.10+ (FastAPI, python-socketio, asyncio)
- **Frontend**: React + TypeScript (Vite, Tailwind CSS, Socket.io-client)
- **Communication**: WebSocket bidirectional streaming
- **State**: Python asyncio + React Zustand
- **Skills**: YAML definitions + Python implementations

**Reuse Strategy**:
- Keep all 3,435 lines of executor modules
- Wrap as built-in skills (YAML wrappers)
- Add new infrastructure around them

---

## 📊 Architecture Layers

```
┌─────────────────────────────────────────────────────┐
│ FRONTEND (React + TypeScript)                       │
│ • Dashboard (6 panels)                              │
│ • WebSocket client                                  │
│ • Interactive controls                              │
└─────────────────────────────────────────────────────┘
                      ↕ WebSocket
┌─────────────────────────────────────────────────────┐
│ BACKEND (Python)                                    │
│                                                      │
│ ┌─ Skills Framework (NEW) ──────────────────────┐  │
│ │ Registry, Loader, Executor, Hooks, Discovery   │  │
│ │ Built-in Skills (wrap existing modules)        │  │
│ └────────────────────────────────────────────────┘  │
│                                                      │
│ ┌─ Orchestration (NEW) ─────────────────────────┐  │
│ │ Task Parser, Planner, Agent Coordinator,       │  │
│ │ State Manager, Decision Engine                 │  │
│ └────────────────────────────────────────────────┘  │
│                                                      │
│ ┌─ Communication (NEW) ─────────────────────────┐  │
│ │ FastAPI + WebSocket Server, Event Bus,         │  │
│ │ Command Queue, State Broadcaster               │  │
│ └────────────────────────────────────────────────┘  │
│                                                      │
│ ┌─ Modes (NEW) ─────────────────────────────────┐  │
│ │ Debug Mode, Ultrathink, Research Orchestrator  │  │
│ └────────────────────────────────────────────────┘  │
│                                                      │
│ ┌─ Executor Modules (EXISTING - Keep!) ─────────┐  │
│ │ LibraryDiscoverer, ValidationOrchestrator,     │  │
│ │ GitManager, PromptEnhancer, etc.               │  │
│ └────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 🌊 WAVE 0: Foundation & Project Setup

**Duration**: 2-3 days
**Prerequisite**: None
**Goal**: Project structure ready for implementation

### Tasks:

**Task 0.1: Project Structure**
```bash
# Create new directory structure
shannon-cli/
├── src/shannon/
│   ├── skills/           # NEW
│   ├── orchestration/    # NEW
│   ├── communication/    # NEW
│   ├── modes/            # NEW
│   ├── research/         # NEW
│   ├── server/           # NEW
│   └── executor/         # EXISTING (keep)
├── dashboard/            # NEW (React app)
├── skills/               # NEW (skill definitions)
│   └── built-in/
├── schemas/              # NEW
└── tests/                # NEW (comprehensive)
```

**Task 0.2: Dependencies Setup**
```toml
# Add to pyproject.toml
[tool.poetry.dependencies]
fastapi = "^0.109.0"
python-socketio = "^5.11.0"
pyyaml = "^6.0.1"
jsonschema = "^4.21.0"
networkx = "^3.2.1"
uvicorn = "^0.27.0"
```

**Task 0.3: Schemas**
- Create `schemas/skill.schema.json` (complete skill definition schema)
- Create `schemas/execution_plan.schema.json`
- Create `schemas/checkpoint.schema.json`

**Task 0.4: Base Models**
```python
# src/shannon/skills/models.py
@dataclass
class Skill:
    name: str
    version: str
    description: str
    parameters: List[Parameter]
    dependencies: List[str]
    hooks: Hooks
    execution: Execution
    metadata: SkillMetadata

@dataclass
class SkillResult:
    success: bool
    data: Any
    duration: float
    error: Optional[str] = None
```

**Skills Required**: None (manual setup)

**Exit Criteria**:
- [ ] Directory structure created
- [ ] Dependencies installed
- [ ] Schemas defined
- [ ] Base models implemented

---

## 🌊 WAVE 1: Skills Framework Core

**Duration**: Week 1-2 (5 working days)
**Dependencies**: Wave 0
**Goal**: Can define skills in YAML and execute with hooks

### Agent Assignments:

**Agent 1-A: SkillRegistry Implementation**
- **Skill**: python-expert
- **File**: `src/shannon/skills/registry.py` (500 lines)
- **Responsibilities**:
  - Skill registration with validation
  - Conflict detection
  - Query methods (get, list, find_by_category)
  - Thread-safe access (asyncio.Lock)
- **Tests**: `tests/skills/test_registry.py`
- **Exit**: Can register skills from dict

**Agent 1-B: SkillLoader Implementation**
- **Skill**: python-expert
- **File**: `src/shannon/skills/loader.py` (400 lines)
- **Responsibilities**:
  - Load from YAML/JSON files
  - Schema validation (jsonschema)
  - Error handling for malformed files
  - Batch loading from directory
- **Tests**: `tests/skills/test_loader.py`
- **Exit**: Can load skills from YAML

**Agent 1-C: HookManager Implementation**
- **Skill**: python-expert
- **File**: `src/shannon/skills/hooks.py` (600 lines)
- **Responsibilities**:
  - Execute pre/post/error hooks
  - Hook dependency resolution
  - Error handling (pre-fail=abort, post-fail=warn, error-fail=log)
  - Hook chaining support
- **Tests**: `tests/skills/test_hooks.py`
- **Exit**: Hooks execute correctly

**Agent 1-D: SkillExecutor Implementation**
- **Skill**: python-expert
- **File**: `src/shannon/skills/executor.py` (1,000 lines)
- **Responsibilities**:
  - Execute native Python skills (import + call)
  - Execute script skills (subprocess)
  - Execute MCP skills (via MCP calls)
  - Execute composite skills (orchestrate multiple)
  - Timeout handling
  - Retry logic
  - Result aggregation
- **Tests**: `tests/skills/test_executor.py`
- **Exit**: Can execute all skill types

**Agent 1-E: Built-in Skill Definitions**
- **Skill**: technical-writer
- **Files**: `skills/built-in/*.yaml` (4 files)
- **Create**:
  1. `library_discovery.yaml` (wraps LibraryDiscoverer)
  2. `validation_orchestrator.yaml` (wraps ValidationOrchestrator)
  3. `git_operations.yaml` (wraps GitManager)
  4. `prompt_enhancement.yaml` (wraps PromptEnhancer)
- **Exit**: 4 skills defined and loadable

### Wave 1 Integration Test:

```python
# tests/wave1_integration.py
async def test_wave1_complete():
    # Load skill from YAML
    loader = SkillLoader(registry)
    skill = loader.load_from_file('skills/built-in/library_discovery.yaml')

    # Execute with hooks
    executor = SkillExecutor(registry)
    result = await executor.execute(
        skill,
        parameters={'feature_description': 'authentication', 'category': 'auth'}
    )

    # Verify
    assert result.success
    assert len(result.data) > 0  # Found libraries
    assert 'fastapi-users' in [lib.name for lib in result.data]
```

**Exit Criteria**:
- [ ] Can load skills from YAML
- [ ] Can execute skills (native Python type)
- [ ] Hooks execute in correct order
- [ ] All 4 built-in skills work
- [ ] Integration test passes

**Estimated Lines**: ~2,500 new lines

---

## 🌊 WAVE 2: Auto-Discovery & Dependencies

**Duration**: Week 2 (3 working days)
**Dependencies**: Wave 1
**Goal**: Skills auto-discovered, dependencies resolved

### Agent Assignments:

**Agent 2-A: Discovery Engine**
- **Skill**: python-expert
- **File**: `src/shannon/skills/discovery.py` (800 lines)
- **Responsibilities**:
  - Scan `.shannon/skills/` recursively
  - Scan `~/.shannon/skills/` (user global)
  - Parse `package.json` scripts as skills
  - Parse `Makefile` targets as skills
  - Query MCPs for capabilities (mcp-exec)
  - Load from Memory MCP cache
- **Discovery Strategy**:
  ```python
  async def discover_all(self) -> List[Skill]:
      skills = []

      # 1. Built-in skills
      skills.extend(await self.load_built_in())

      # 2. Project skills (.shannon/skills/)
      skills.extend(await self.scan_directory('.shannon/skills'))

      # 3. User global skills (~/.shannon/skills/)
      skills.extend(await self.scan_directory(Path.home() / '.shannon/skills'))

      # 4. Package.json scripts
      skills.extend(await self.parse_package_json())

      # 5. Makefile targets
      skills.extend(await self.parse_makefile())

      # 6. MCP skills
      skills.extend(await self.query_mcps())

      # 7. Memory MCP cache
      skills.extend(await self.load_from_memory())

      return skills
  ```
- **Tests**: `tests/skills/test_discovery.py`
- **Exit**: Discovers skills from all sources

**Agent 2-B: Dependency Resolver**
- **Skill**: python-expert
- **File**: `src/shannon/skills/dependencies.py` (400 lines)
- **Responsibilities**:
  - Build dependency graph (networkx.DiGraph)
  - Detect circular dependencies
  - Topological sort for execution order
  - Identify parallel execution opportunities
  - Validate all dependencies available
- **Algorithm**:
  ```python
  import networkx as nx

  def resolve_dependencies(self, skills: List[Skill]) -> List[List[Skill]]:
      # Build graph
      G = nx.DiGraph()
      for skill in skills:
          G.add_node(skill.name)
          for dep in skill.dependencies:
              G.add_edge(dep, skill.name)

      # Check for cycles
      if not nx.is_directed_acyclic_graph(G):
          cycles = list(nx.simple_cycles(G))
          raise CircularDependencyError(cycles)

      # Topological sort
      ordered = list(nx.topological_sort(G))

      # Group by level (parallelizable)
      levels = []
      for level in nx.topological_generations(G):
          levels.append([skills_by_name[n] for n in level])

      return levels  # [[skill1, skill2], [skill3], ...]
  ```
- **Tests**: `tests/skills/test_dependencies.py`
- **Exit**: Dependencies resolved, execution order determined

**Agent 2-C: Catalog Persistence**
- **Skill**: python-expert
- **File**: `src/shannon/skills/catalog.py` (300 lines)
- **Responsibilities**:
  - Save discovered skills to Memory MCP
  - Cache for 7 days
  - Invalidate on skill file changes
  - Quick load on subsequent runs
- **Integration**:
  ```python
  async def save_to_memory(self, skills: List[Skill]):
      catalog = {
          'skills': [s.to_dict() for s in skills],
          'discovered_at': datetime.now().isoformat(),
          'version': '1.0.0'
      }

      await memory_mcp.create_entities([{
          'name': 'skill_catalog',
          'entityType': 'catalog',
          'observations': [json.dumps(catalog)]
      }])
  ```
- **Tests**: `tests/skills/test_catalog.py`
- **Exit**: Catalog persists and loads

### Wave 2 Integration Test:

```python
async def test_wave2_complete():
    # Discover all skills
    discovery = DiscoveryEngine(registry)
    skills = await discovery.discover_all()

    # Should find built-in + any custom
    assert len(skills) >= 4  # At least our 4 built-ins

    # Resolve dependencies
    resolver = DependencyResolver()
    execution_order = resolver.resolve_dependencies(skills)

    # Verify no circular deps
    assert all(isinstance(level, list) for level in execution_order)

    # Save catalog
    catalog = SkillCatalog()
    await catalog.save_to_memory(skills)

    # Reload (should be cached)
    reloaded = await catalog.load_from_memory()
    assert len(reloaded) == len(skills)
```

**Exit Criteria**:
- [ ] Discovers skills from 7 sources
- [ ] Dependency resolution works (no cycles)
- [ ] Catalog persists to Memory MCP
- [ ] Integration test passes

**Estimated Lines**: ~1,500 new lines

---

## 🌊 WAVE 3: WebSocket Communication Infrastructure

**Duration**: Week 3 (4 working days)
**Dependencies**: Wave 0
**Goal**: Real-time bidirectional streaming working

### Agent Assignments:

**Agent 3-A: FastAPI WebSocket Server**
- **Skill**: fastapi-expert, python-expert
- **File**: `src/shannon/server/app.py` (400 lines)
- **Responsibilities**:
  - FastAPI application setup
  - CORS configuration
  - Health check endpoint
  - Static file serving (for React dashboard)
- **Implementation**:
  ```python
  from fastapi import FastAPI
  from fastapi.middleware.cors import CORSMiddleware
  from fastapi.staticfiles import StaticFiles

  app = FastAPI(title="Shannon Dashboard Server")

  # CORS for dev
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:3000"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"]
  )

  @app.get("/health")
  async def health():
      return {"status": "healthy", "version": "4.0.0"}

  # Serve React dashboard (production)
  app.mount("/", StaticFiles(directory="dashboard/dist", html=True))
  ```

**Agent 3-B: Socket.IO Integration**
- **Skill**: python-expert
- **File**: `src/shannon/server/websocket.py` (800 lines)
- **Responsibilities**:
  - python-socketio server setup
  - Event handlers (connect, disconnect, command)
  - Room management (per execution session)
  - Error handling and reconnection
- **Implementation**:
  ```python
  import socketio

  sio = socketio.AsyncServer(
      async_mode='asgi',
      cors_allowed_origins='*',
      logger=True,
      engineio_logger=True
  )

  @sio.event
  async def connect(sid, environ):
      logger.info(f"Dashboard connected: {sid}")
      await sio.emit('connected', {'server_version': '4.0.0'}, to=sid)

  @sio.event
  async def command(sid, data):
      """Handle dashboard commands: HALT, RESUME, ROLLBACK, etc."""
      cmd_type = data.get('type')

      if cmd_type == 'HALT':
          await orchestrator.halt_execution()
      elif cmd_type == 'RESUME':
          await orchestrator.resume_execution()
      elif cmd_type == 'ROLLBACK':
          steps = data.get('steps', 1)
          await orchestrator.rollback(steps)
      elif cmd_type == 'DECISION':
          decision_id = data['decision_id']
          selected = data['selected_option']
          await orchestrator.handle_decision(decision_id, selected)

  # Mount to FastAPI
  from socketio import ASGIApp
  socket_app = ASGIApp(sio, app)
  ```

**Agent 3-C: Event Bus**
- **Skill**: python-expert
- **File**: `src/shannon/communication/events.py` (400 lines)
- **Responsibilities**:
  - Pub/sub event system
  - Event types enum
  - Event serialization
  - Rate limiting (prevent flooding)
- **Events**:
  ```python
  class EventType(Enum):
      # Skill events
      SKILL_STARTED = "skill:started"
      SKILL_COMPLETED = "skill:completed"
      SKILL_FAILED = "skill:failed"

      # File events
      FILE_MODIFIED = "file:modified"
      FILE_CREATED = "file:created"
      FILE_DELETED = "file:deleted"

      # Decision events
      DECISION_POINT = "decision:point"
      DECISION_MADE = "decision:made"

      # Validation events
      VALIDATION_STARTED = "validation:started"
      VALIDATION_RESULT = "validation:result"

      # Agent events
      AGENT_SPAWNED = "agent:spawned"
      AGENT_PROGRESS = "agent:progress"
      AGENT_COMPLETED = "agent:completed"

      # System events
      CHECKPOINT_CREATED = "checkpoint:created"
      EXECUTION_HALTED = "execution:halted"
      EXECUTION_RESUMED = "execution:resumed"

  class EventBus:
      async def emit(self, event_type: EventType, data: Dict):
          # Serialize event
          event = {
              'type': event_type.value,
              'timestamp': datetime.now().isoformat(),
              'data': data
          }

          # Send to WebSocket
          await sio.emit(event_type.value, event)

          # Log
          logger.debug(f"Event: {event_type.value}")
  ```

**Agent 3-D: Command Queue**
- **Skill**: python-expert
- **File**: `src/shannon/communication/command_queue.py` (300 lines)
- **Responsibilities**:
  - Priority queue for commands
  - Command validation
  - Rate limiting
  - Command history
- **Implementation**:
  ```python
  from asyncio import PriorityQueue

  class CommandQueue:
      def __init__(self):
          self.queue = PriorityQueue()
          self.history = []

      async def enqueue(self, command: Command, priority: int = 5):
          await self.queue.put((priority, command))
          self.history.append(command)

      async def dequeue(self) -> Command:
          _, command = await self.queue.get()
          return command
  ```

### Wave 3 Integration Test:

```python
async def test_wave3_complete():
    # Start server
    server = DashboardServer()
    await server.start()

    # Connect client
    client = socketio.AsyncClient()
    await client.connect('http://localhost:8000')

    # Test event emission
    await server.events.emit(EventType.SKILL_STARTED, {'skill': 'test'})

    # Verify client receives (within 50ms)
    event = await client.receive(timeout=0.05)
    assert event['type'] == 'skill:started'

    # Test command
    await client.emit('command', {'type': 'HALT'})

    # Verify handled
    assert server.orchestrator.halted == True
```

**Exit Criteria**:
- [ ] WebSocket server running
- [ ] Can connect from client
- [ ] Events stream to dashboard
- [ ] Commands received from dashboard
- [ ] <50ms event latency measured

**Estimated Lines**: ~1,900 new lines

---

## 🌊 WAVE 4: Dashboard Frontend (Core 3 Panels)

**Duration**: Week 4 (5 working days)
**Dependencies**: Wave 3
**Goal**: Visual dashboard showing real-time execution

### Agent Assignments:

**Agent 4-A: Dashboard App Setup**
- **Skill**: react-expert, typescript-expert
- **Directory**: `dashboard/` (Vite + React + TypeScript)
- **Setup**:
  ```bash
  cd shannon-cli
  npm create vite@latest dashboard -- --template react-ts
  cd dashboard
  npm install socket.io-client zustand tailwindcss
  npm install -D @types/node
  ```
- **Structure**:
  ```
  dashboard/
  ├── src/
  │   ├── App.tsx
  │   ├── hooks/
  │   │   └── useSocket.ts
  │   ├── store/
  │   │   └── dashboardStore.ts
  │   ├── panels/
  │   │   ├── ExecutionOverview.tsx
  │   │   ├── SkillsView.tsx
  │   │   └── FileDiff.tsx
  │   ├── components/
  │   │   └── (shared)
  │   └── types/
  │       └── events.ts
  ```

**Agent 4-B: WebSocket Client Hook**
- **Skill**: react-expert, typescript-expert
- **File**: `dashboard/src/hooks/useSocket.ts` (200 lines)
- **Implementation**:
  ```typescript
  import { useEffect, useState } from 'react';
  import { io, Socket } from 'socket.io-client';

  export function useSocket(url: string) {
      const [socket, setSocket] = useState<Socket | null>(null);
      const [events, setEvents] = useState<any[]>([]);

      useEffect(() => {
          const s = io(url);

          s.on('connect', () => console.log('Connected'));

          // Listen to all event types
          s.onAny((eventName, data) => {
              setEvents(prev => [...prev, { type: eventName, data, timestamp: Date.now() }]);
          });

          setSocket(s);

          return () => s.disconnect();
      }, [url]);

      const sendCommand = (type: string, params?: any) => {
          socket?.emit('command', { type, ...params });
      };

      return { socket, events, sendCommand };
  }
  ```

**Agent 4-C: Panel 1 - Execution Overview**
- **Skill**: react-expert, typescript-expert, tailwind-expert
- **File**: `dashboard/src/panels/ExecutionOverview.tsx` (400 lines)
- **Features**:
  - Task name and description
  - Status indicator (running, paused, completed, failed)
  - Progress bar (percentage)
  - Timing (started, elapsed, ETA)
  - Controls: HALT, RESUME buttons
- **UI**:
  ```tsx
  export function ExecutionOverview({ events, onHalt, onResume }) {
      const execution = useExecutionState(events);

      return (
          <div className="border rounded-lg p-4">
              <h2 className="text-xl font-bold">{execution.task}</h2>
              <div className="mt-2">
                  <StatusBadge status={execution.status} />
                  <ProgressBar value={execution.progress} />
              </div>

              <div className="mt-4 flex gap-2">
                  <Button onClick={onHalt} variant="danger">⏸ HALT</Button>
                  <Button onClick={onResume} variant="primary">▶ RESUME</Button>
                  <Button onClick={onRollback}>🔄 ROLLBACK</Button>
              </div>

              <div className="mt-4 text-sm text-gray-600">
                  <div>Started: {execution.startTime}</div>
                  <div>Elapsed: {execution.elapsed}</div>
                  <div>ETA: {execution.eta}</div>
              </div>
          </div>
      );
  }
  ```

**Agent 4-D: Panel 2 - Skills View**
- **Skill**: react-expert, typescript-expert
- **File**: `dashboard/src/panels/SkillsView.tsx` (600 lines)
- **Features**:
  - List of skills: Active, Queued, Completed, Failed
  - Per-skill: Name, status, duration, progress
  - Hooks status (pre/post/error)
  - Actions: INSPECT skill details, PAUSE skill
- **UI**: Table/list with real-time updates

**Agent 4-E: Panel 3 - File Diff**
- **Skill**: react-expert, typescript-expert
- **File**: `dashboard/src/panels/FileDiff.tsx` (800 lines)
- **Features**:
  - File tree navigator
  - Live diff display (Monaco Editor or react-diff-viewer)
  - Syntax highlighting
  - Actions: APPROVE, REVERT, EDIT
- **Library**: `react-diff-viewer-continued` or Monaco Editor
- **UI**: Side-by-side diff with approve/revert buttons

### Wave 4 Integration Test:

```bash
# Start backend
cd shannon-cli
poetry run python -m shannon.server.app

# Start frontend (separate terminal)
cd dashboard
npm run dev

# Open browser: http://localhost:3000
# Should see 3 panels, connect to WebSocket
```

**Exit Criteria**:
- [ ] Dashboard loads and connects to backend
- [ ] Shows execution in real-time
- [ ] HALT button stops execution
- [ ] Skills list updates live
- [ ] File diffs display correctly

**Estimated Lines**: ~2,000 new lines (dashboard)

---

## 🌊 WAVE 5: shannon do Command + Orchestration

**Duration**: Week 5 (5 working days)
**Dependencies**: Waves 1, 2, 3
**Goal**: Universal task executor working end-to-end

### Agent Assignments:

**Agent 5-A: Task Parser**
- **Skill**: python-expert
- **File**: `src/shannon/orchestration/task_parser.py` (500 lines)
- **Responsibilities**:
  - Parse natural language task
  - Extract intent (goal, domain, type, keywords)
  - Use Claude SDK for understanding
  - Map intent to skills
- **Implementation**:
  ```python
  class TaskParser:
      async def parse(self, task: str) -> ParsedTask:
          # Use Claude to understand
          response = await self.claude.messages.create(
              model="claude-sonnet-4",
              messages=[{
                  "role": "user",
                  "content": f"Parse this task into structured intent:\n\nTask: {task}\n\nExtract: goal, domain, type (fix/feature/refactor), keywords"
              }]
          )

          # Extract structured data
          intent = self.extract_intent(response.content[0].text)

          # Map to skills
          candidate_skills = await self.skill_registry.find_for_domain(intent.domain)

          return ParsedTask(
              original=task,
              intent=intent,
              candidate_skills=candidate_skills
          )
  ```

**Agent 5-B: Execution Planner**
- **Skill**: python-expert
- **File**: `src/shannon/orchestration/planner.py` (800 lines)
- **Responsibilities**:
  - Select skills for task
  - Order skills (dependencies)
  - Add checkpoints
  - Estimate duration
  - Detect decision points
- **Planning Algorithm**:
  ```python
  class ExecutionPlanner:
      async def create_plan(self, parsed_task: ParsedTask) -> ExecutionPlan:
          # 1. Select skills
          selected = await self.select_skills(parsed_task.candidate_skills, parsed_task.intent)

          # 2. Research if needed
          if self.needs_research(parsed_task.intent):
              research_skill = self.skill_registry.get('research_orchestrator')
              selected.insert(0, research_skill)

          # 3. Resolve dependencies
          ordered = self.dependency_resolver.resolve(selected)

          # 4. Add checkpoints (before each skill)
          with_checkpoints = self.add_checkpoints(ordered)

          # 5. Detect decision points
          decision_points = self.detect_decisions(with_checkpoints)

          # 6. Estimate duration
          duration = sum(skill.estimated_duration for skill in selected)

          return ExecutionPlan(
              task=parsed_task,
              skills=with_checkpoints,
              decision_points=decision_points,
              estimated_duration=duration,
              parallel_opportunities=self.find_parallel_ops(ordered)
          )
  ```

**Agent 5-C: State Manager (Checkpoints & Rollback)**
- **Skill**: python-expert
- **File**: `src/shannon/orchestration/state_manager.py` (600 lines)
- **Responsibilities**:
  - Create checkpoints before skills
  - Snapshot: files, git, context, agents
  - Restore to any checkpoint
  - Verify restoration
- **Implementation**: (See Thought 4 above)

**Agent 5-D: shannon do Command**
- **Skill**: python-expert
- **File**: `src/shannon/cli/commands/do.py` (400 lines)
- **Responsibilities**:
  - CLI interface (Click)
  - Start WebSocket server
  - Parse and plan task
  - Execute with orchestrator
  - Stream to dashboard
- **CLI**:
  ```python
  @click.command()
  @click.argument('task')
  @click.option('--dashboard/--no-dashboard', default=True)
  @click.option('--checkpoints/--no-checkpoints', default=True)
  @click.option('--interactive/--auto', default=True)
  async def do(task: str, dashboard: bool, checkpoints: bool, interactive: bool):
      """Universal task executor with skills orchestration"""

      # Start WebSocket server if dashboard enabled
      if dashboard:
          server = await start_dashboard_server()

      # Parse task
      parsed = await task_parser.parse(task)

      # Create plan
      plan = await execution_planner.create_plan(parsed)

      # Execute
      orchestrator = Orchestrator(
          plan=plan,
          checkpoints=checkpoints,
          interactive=interactive,
          events=event_bus
      )

      result = await orchestrator.execute()

      # Report
      if result.success:
          click.echo(f"✅ Task completed successfully")
      else:
          click.echo(f"❌ Task failed: {result.error}")
  ```

### Wave 5 Integration Test:

```bash
# Test shannon do
shannon do "create utils.py with helper functions"

# Expected:
# 1. Dashboard opens in browser
# 2. Shows task parsing → planning → execution
# 3. Skills execute with checkpoints
# 4. Can HALT mid-execution
# 5. Can ROLLBACK to previous checkpoint
# 6. Completes successfully
```

**Exit Criteria**:
- [ ] shannon do command exists
- [ ] Parses task correctly
- [ ] Creates execution plan
- [ ] Executes skills in order
- [ ] Dashboard shows execution
- [ ] Checkpoints created
- [ ] Can HALT/RESUME
- [ ] Integration test passes

**Estimated Lines**: ~2,300 new lines (backend)

---

## 🌊 WAVE 6: Agent Coordination & Parallel Execution

**Duration**: Week 6 (4 working days)
**Dependencies**: Wave 5
**Goal**: Multi-agent parallel execution working

### Agent Assignments:

**Agent 6-A: Agent Pool Manager**
- **Skill**: python-expert
- **File**: `src/shannon/orchestration/agent_pool.py` (700 lines)
- **Responsibilities**:
  - Manage agent pool (8 active / 50 max)
  - Spawn agents with roles
  - Track agent status
  - Coordinate dependencies
  - Terminate agents
- **Implementation**: (See Thought 7 above)

**Agent 6-B: Agent Types**
- **Skill**: python-expert
- **Files**: `src/shannon/orchestration/agents/*.py` (800 lines total)
- **Types**:
  1. ResearchAgent - Fire Crawl execution
  2. AnalysisAgent - Code analysis
  3. TestingAgent - Run tests
  4. ValidationAgent - Validate results
  5. GitAgent - Git operations
  6. PlanningAgent - Task planning
  7. MonitoringAgent - System health
  8. GenericAgent - General tasks

**Agent 6-C: Dashboard Agent Panel**
- **Skill**: react-expert, typescript-expert
- **File**: `dashboard/src/panels/AgentPool.tsx` (500 lines)
- **Features**:
  - List active agents (8/50)
  - Per-agent: Role, task, progress bar, duration
  - Actions: INSPECT, SPAWN, TERMINATE
- **UI**: Real-time agent status cards

**Agent 6-D: Parallel Execution Integration**
- **Skill**: python-expert
- **File**: Update `src/shannon/orchestration/planner.py`
- **Add**: Parallel execution optimization
- **Implementation**:
  ```python
  async def execute_plan(self, plan: ExecutionPlan):
      for level in plan.skill_levels:
          # Execute all skills in this level in parallel
          if len(level) > 1:
              # Spawn agent per skill
              agents = [
                  await self.agent_pool.spawn(
                      role=self.determine_role(skill),
                      task=f"Execute {skill.name}"
                  )
                  for skill in level
              ]

              # Execute in parallel
              results = await asyncio.gather(*[
                  self.execute_skill_with_agent(skill, agent)
                  for skill, agent in zip(level, agents)
              ])
          else:
              # Single skill, execute directly
              result = await self.execute_skill(level[0])
  ```

### Wave 6 Integration Test:

```python
async def test_wave6_parallel():
    # Task requiring parallel skills
    result = await shannon_do("analyze codebase and run all tests")

    # Should spawn:
    # - AnalysisAgent (code analysis)
    # - TestingAgent (run tests)
    # Both execute in parallel

    assert len(result.agents_spawned) == 2
    assert result.parallel_duration < result.sequential_duration
```

**Exit Criteria**:
- [ ] Can spawn multiple agents
- [ ] Agents execute in parallel
- [ ] Dashboard shows agent status
- [ ] Can inspect/terminate agents
- [ ] Parallel execution faster than sequential

**Estimated Lines**: ~2,000 new lines

---

## 🌊 WAVE 7: shannon debug Mode

**Duration**: Week 7 (5 working days)
**Dependencies**: Wave 5
**Goal**: Sequential analysis mode with halt points

### Agent Assignments:

**Agent 7-A: Debug Mode Engine**
- **Skill**: python-expert
- **File**: `src/shannon/modes/debug_mode.py` (1,500 lines)
- **Responsibilities**:
  - Sequential execution (one skill at a time)
  - Automatic halts (before skill, after skill, on decision)
  - Depth levels (standard/detailed/ultra/trace)
  - Investigation tools
  - Step tracking
- **Implementation**: (See Thought 13 above)

**Agent 7-B: Investigation Tools**
- **Skill**: python-expert
- **File**: `src/shannon/modes/investigation.py` (400 lines)
- **Tools**:
  ```python
  class InvestigationTools:
      async def inspect_state(self) -> Dict:
          """Show complete execution state"""
          return {
              'current_step': self.step_count,
              'skill_stack': self.skill_stack,
              'context': self.context.to_dict(),
              'checkpoints': len(self.checkpoints),
              'agents': [a.to_dict() for a in self.agents]
          }

      async def show_reasoning(self) -> str:
          """Display full reasoning for current decision"""
          return self.current_reasoning_chain

      async def list_alternatives(self) -> List[Alternative]:
          """Show other options that were considered"""
          return self.alternatives_considered

      async def test_hypothesis(self, hypothesis: str) -> SimulationResult:
          """Simulate alternative approach"""
          return await self.simulator.simulate(hypothesis)

      async def inject_constraint(self, constraint: str):
          """Add new requirement to execution"""
          self.context.constraints.append(constraint)
          await self.replan_with_constraint(constraint)
  ```

**Agent 7-C: shannon debug Command**
- **Skill**: python-expert
- **File**: `src/shannon/cli/commands/debug.py` (300 lines)
- **CLI**:
  ```python
  @click.command()
  @click.argument('task')
  @click.option('--depth', type=click.Choice(['standard', 'detailed', 'ultra', 'trace']), default='detailed')
  @click.option('--focus', help='Focus area (e.g., memory_management)')
  @click.option('--resume-from', help='Resume from step number')
  async def debug(task: str, depth: str, focus: str, resume_from: int):
      """Sequential analysis mode with halt points"""

      engine = DebugModeEngine(depth=depth, focus=focus)

      if resume_from:
          await engine.resume_from_step(resume_from)

      result = await engine.execute_with_debugging(task)
  ```

**Agent 7-D: Debug Dashboard View**
- **Skill**: react-expert, typescript-expert
- **File**: `dashboard/src/views/DebugMode.tsx` (800 lines)
- **Features**:
  - Step-by-step visualization
  - Reasoning chain display
  - Investigation tool UI (buttons for each tool)
  - State inspector panel
  - Halt/Continue controls

### Wave 7 Integration Test:

```bash
# Run in debug mode
shannon debug "optimize database queries" --depth detailed

# Expected:
# 1. Dashboard shows debug view
# 2. Halts before each major step
# 3. Shows reasoning
# 4. Can inspect state
# 5. Can inject constraints
# 6. Can continue/rollback
```

**Exit Criteria**:
- [ ] shannon debug command exists
- [ ] Halts at decision points
- [ ] Investigation tools work
- [ ] Depth levels control verbosity
- [ ] Dashboard debug view functional

**Estimated Lines**: ~3,000 new lines

---

## 🌊 WAVE 8: Decision Engine & Complete Dashboard

**Duration**: Week 8 (5 working days)
**Dependencies**: Wave 4, 5
**Goal**: Full 6-panel dashboard with all steering controls

### Agent Assignments:

**Agent 8-A: Decision Engine**
- **Skill**: python-expert
- **File**: `src/shannon/orchestration/decision_engine.py` (400 lines)
- **Responsibilities**:
  - Detect decision points (uncertainty, multiple approaches, high impact)
  - Generate options with pros/cons
  - Calculate confidence per option
  - Present to user via dashboard
  - Handle user selection
  - Auto-select on timeout
- **Implementation**: (See Thought 5 above)

**Agent 8-B: Panel 5 - Decision Points**
- **Skill**: react-expert, typescript-expert
- **File**: `dashboard/src/panels/Decisions.tsx` (400 lines)
- **Features**:
  - Show context and question
  - Display options with details (pros/cons/confidence/impact)
  - Recommendation highlighting
  - Countdown timer for auto-select
  - User selection buttons
- **UI**: Decision card with option buttons

**Agent 8-C: Panel 6 - Validation Stream**
- **Skill**: react-expert, typescript-expert
- **File**: `dashboard/src/panels/Validation.tsx` (400 lines)
- **Features**:
  - Live test output streaming
  - Code quality metrics
  - Performance results
  - Actions: PAUSE TESTS, VIEW FAILURES
- **UI**: Test results with real-time updates

**Agent 8-D: Complete Steering Controls**
- **Skill**: react-expert, python-expert
- **Add**:
  - REDIRECT with re-planning UI
  - Context injection modal
  - APPROVE/OVERRIDE for decisions
  - All controls <100ms response
- **Backend**: Update command handlers
- **Frontend**: Add control UIs

### Wave 8 Integration Test:

```bash
# Complex task with decisions
shannon do "refactor authentication system"

# Expected:
# 1. All 6 panels visible
# 2. Decision point presented: "Refactor now or create follow-up?"
# 3. User selects option
# 4. Execution continues with choice
# 5. Can REDIRECT mid-execution
# 6. Validation streams in real-time
```

**Exit Criteria**:
- [ ] All 6 dashboard panels working
- [ ] Decision points presented
- [ ] User can select options
- [ ] All steering controls functional
- [ ] <100ms response time measured

**Estimated Lines**: ~1,200 new lines

---

## 🌊 WAVE 9: Research & Ultrathink Modes

**Duration**: Week 9 (5 working days)
**Dependencies**: Wave 5, 8
**Goal**: Deep analysis and knowledge gathering modes

### Agent Assignments:

**Agent 9-A: Research Orchestrator**
- **Skill**: python-expert
- **File**: `src/shannon/research/orchestrator.py` (1,200 lines)
- **Responsibilities**:
  - Coordinate Fire Crawl, Tavali, Web research
  - Parallel research execution
  - Knowledge synthesis
  - Pattern extraction
  - Best practices compilation
- **Implementation**:
  ```python
  class ResearchOrchestrator:
      async def research(self, topic: str, depth: str = 'standard') -> ResearchResult:
          # Parallel research
          fire_crawl_task = self.fire_crawl(topic)
          web_research_task = self.web_research(topic)

          results = await asyncio.gather(fire_crawl_task, web_research_task)

          # Tavali synthesis
          synthesis = await self.tavali_synthesize(results)

          return ResearchResult(
              topic=topic,
              sources=results,
              patterns=synthesis.patterns,
              best_practices=synthesis.best_practices,
              anti_patterns=synthesis.anti_patterns,
              code_examples=synthesis.code_examples
          )
  ```

**Agent 9-B: Ultrathink Engine**
- **Skill**: python-expert
- **File**: `src/shannon/modes/ultrathink.py` (1,800 lines)
- **Responsibilities**:
  - 500+ step reasoning via Sequential MCP
  - Problem decomposition (100 steps)
  - Research integration (150 steps)
  - Hypothesis generation (150 steps)
  - Evaluation & planning (100 steps)
- **Implementation**: (See Thought 14 above)

**Agent 9-C: Commands**
- **Skill**: python-expert
- **Files**:
  - `src/shannon/cli/commands/research.py` (200 lines)
  - `src/shannon/cli/commands/ultrathink.py` (200 lines)
- **Features**:
  - CLI interfaces
  - Integration with engines
  - Output formatting
  - Optional: --then-execute flag

**Agent 9-D: Dashboard Views**
- **Skill**: react-expert, typescript-expert
- **Files**:
  - `dashboard/src/views/Ultrathink.tsx` (1,000 lines)
  - `dashboard/src/views/Research.tsx` (600 lines)
- **Features**:
  - Reasoning tree visualization
  - Hypothesis comparison matrix
  - Research progress tracking
  - Interactive exploration

### Wave 9 Integration Test:

```bash
# Test research
shannon research "React server components best practices"
# Expected: Fire Crawl + Web research → Knowledge synthesis

# Test ultrathink
shannon ultrathink "redesign database schema" --then-execute
# Expected: 500+ steps → Hypotheses → Plan → Option to execute
```

**Exit Criteria**:
- [ ] shannon research finds knowledge
- [ ] shannon ultrathink generates hypotheses
- [ ] 500+ reasoning steps complete
- [ ] Dashboard visualizations working

**Estimated Lines**: ~3,000 new lines

---

## 🌊 WAVE 10: Dynamic Skills & Production Polish

**Duration**: Week 10 (5 working days)
**Dependencies**: All previous waves
**Goal**: Self-improving system, production ready

### Agent Assignments:

**Agent 10-A: Pattern Detector**
- **Skill**: python-expert
- **File**: `src/shannon/skills/pattern_detector.py` (600 lines)
- **Responsibilities**:
  - Analyze command history (last 1000 commands)
  - Detect repeated sequences (≥3 occurrences)
  - Calculate automation value score
  - Suggest composite skill creation
- **Algorithm**:
  ```python
  class PatternDetector:
      async def detect_patterns(self) -> List[Pattern]:
          # Load command history
          history = await self.load_history(limit=1000)

          # Find sequences
          sequences = self.find_sequences(history, min_length=2)

          # Filter by frequency (≥3 occurrences)
          frequent = [s for s in sequences if s.count >= 3]

          # Score automation value
          scored = [
              (seq, self.calculate_automation_value(seq))
              for seq in frequent
          ]

          # Sort by value
          scored.sort(key=lambda x: x[1], reverse=True)

          return [Pattern(sequence=seq, score=score) for seq, score in scored]
  ```

**Agent 10-B: Dynamic Skill Generator**
- **Skill**: python-expert
- **File**: `src/shannon/skills/generator.py` (700 lines)
- **Responsibilities**:
  - Analyze command pattern
  - Extract parameters and variations
  - Determine dependencies
  - Generate YAML skill definition
  - User notification (ACCEPT/DECLINE/CUSTOMIZE)
- **Generation**:
  ```python
  async def generate_from_pattern(self, pattern: Pattern) -> GeneratedSkill:
      # Analyze pattern
      params = self.extract_parameters(pattern.sequence)
      deps = self.determine_dependencies(pattern.sequence)

      # Generate YAML
      skill_def = {
          'skill': {
              'name': self.generate_name(pattern),
              'version': '1.0.0',
              'auto_generated': True,
              'description': self.generate_description(pattern),
              'parameters': params,
              'dependencies': deps,
              'execution': {
                  'type': 'composite',
                  'skills': pattern.sequence
              }
          }
      }

      # Present to user
      approval = await self.request_approval(skill_def)

      if approval:
          await self.save_skill(skill_def)

      return GeneratedSkill(definition=skill_def, approved=approval)
  ```

**Agent 10-C: Performance Monitoring**
- **Skill**: python-expert
- **File**: `src/shannon/skills/performance.py` (300 lines)
- **Responsibilities**:
  - Track per-skill metrics (duration, success rate, usage count)
  - Identify slow skills
  - Optimization suggestions
  - Dashboard metrics panel
- **Metrics**:
  ```python
  @dataclass
  class SkillMetrics:
      skill_name: str
      total_executions: int
      successful: int
      failed: int
      success_rate: float
      avg_duration: float
      max_duration: float
      min_duration: float
      last_used: datetime
  ```

**Agent 10-D: Production Polish**
- **Skills**: python-expert, react-expert
- **Tasks**:
  1. Error message improvements
  2. Dashboard UX refinement (loading states, transitions)
  3. Performance optimization (caching, memoization)
  4. Logging improvements
  5. Configuration options
  6. Help text updates
  7. Tutorial creation

**Agent 10-E: Documentation**
- **Skill**: technical-writer
- **Files**:
  - `docs/SKILLS_DEVELOPMENT_GUIDE.md` (comprehensive skill creation guide)
  - `docs/DASHBOARD_USER_GUIDE.md` (how to use dashboard)
  - `docs/COMMAND_REFERENCE.md` (all commands with examples)
  - `docs/ARCHITECTURE.md` (system architecture)
  - Update `README.md` with V4.0 features

### Wave 10 Integration Test:

```bash
# Full system test
shannon do "implement user profile page" --interactive

# Expected:
# 1. Task parsed
# 2. Skills discovered
# 3. Execution plan created
# 4. Research conducted (if needed)
# 5. Skills execute with checkpoints
# 6. Dashboard shows all panels
# 7. Decision points presented
# 8. Agents coordinate
# 9. Validation runs
# 10. Git commit created
# 11. Pattern recorded for future skill generation
```

**Exit Criteria**:
- [ ] Pattern detection finds repeated commands
- [ ] Dynamic skill creation working
- [ ] Performance metrics accurate
- [ ] Documentation complete
- [ ] Full E2E test passes
- [ ] Ready for release

**Estimated Lines**: ~1,600 new lines

---

## 📦 Complete File Manifest (New Files)

### Backend (Python) - ~12,000 new lines

**Skills Framework** (~5,500 lines):
- `src/shannon/skills/models.py` (300)
- `src/shannon/skills/registry.py` (500)
- `src/shannon/skills/loader.py` (400)
- `src/shannon/skills/executor.py` (1,000)
- `src/shannon/skills/hooks.py` (600)
- `src/shannon/skills/discovery.py` (800)
- `src/shannon/skills/dependencies.py` (400)
- `src/shannon/skills/catalog.py` (300)
- `src/shannon/skills/pattern_detector.py` (600)
- `src/shannon/skills/generator.py` (700)
- `src/shannon/skills/performance.py` (300)

**Orchestration** (~3,400 lines):
- `src/shannon/orchestration/task_parser.py` (500)
- `src/shannon/orchestration/planner.py` (800)
- `src/shannon/orchestration/state_manager.py` (600)
- `src/shannon/orchestration/decision_engine.py` (400)
- `src/shannon/orchestration/agent_pool.py` (700)
- `src/shannon/orchestration/agents/` (800 - various agent types)

**Communication** (~1,900 lines):
- `src/shannon/server/app.py` (400)
- `src/shannon/server/websocket.py` (800)
- `src/shannon/communication/events.py` (400)
- `src/shannon/communication/command_queue.py` (300)

**Modes** (~3,700 lines):
- `src/shannon/modes/debug_mode.py` (1,500)
- `src/shannon/modes/ultrathink.py` (1,800)
- `src/shannon/modes/investigation.py` (400)

**Research** (~1,200 lines):
- `src/shannon/research/orchestrator.py` (1,200)

**Commands** (~1,500 lines):
- `src/shannon/cli/commands/do.py` (400)
- `src/shannon/cli/commands/debug.py` (300)
- `src/shannon/cli/commands/ultrathink.py` (200)
- `src/shannon/cli/commands/research.py` (200)
- `src/shannon/cli/commands/validate.py` (300 - enhanced)
- Update `src/shannon/cli/commands/__init__.py` (100)

### Frontend (React/TypeScript) - ~5,300 new lines

**Dashboard Core** (~1,200 lines):
- `dashboard/src/App.tsx` (200)
- `dashboard/src/hooks/useSocket.ts` (200)
- `dashboard/src/store/dashboardStore.ts` (600)
- `dashboard/src/types/events.ts` (200)

**Panels** (~3,100 lines):
- `dashboard/src/panels/ExecutionOverview.tsx` (400)
- `dashboard/src/panels/SkillsView.tsx` (600)
- `dashboard/src/panels/AgentPool.tsx` (500)
- `dashboard/src/panels/FileDiff.tsx` (800)
- `dashboard/src/panels/Decisions.tsx` (400)
- `dashboard/src/panels/Validation.tsx` (400)

**Views** (~1,600 lines):
- `dashboard/src/views/DebugMode.tsx` (800)
- `dashboard/src/views/Ultrathink.tsx` (800)

**Components** (~400 lines):
- `dashboard/src/components/` (shared components)

### Configuration & Schemas (~800 lines)

**Skill Definitions** (~400 lines):
- `skills/built-in/library_discovery.yaml`
- `skills/built-in/validation_orchestrator.yaml`
- `skills/built-in/git_operations.yaml`
- `skills/built-in/prompt_enhancement.yaml`
- `skills/built-in/research_orchestrator.yaml`
- `skills/built-in/code_analysis.yaml`
- `skills/built-in/test_runner.yaml`
- `skills/built-in/file_operations.yaml`

**Schemas** (~400 lines):
- `schemas/skill.schema.json`
- `schemas/execution_plan.schema.json`
- `schemas/checkpoint.schema.json`
- `schemas/decision_point.schema.json`

### Tests (~3,000 lines)

- `tests/skills/` (1,000 lines)
- `tests/orchestration/` (800 lines)
- `tests/communication/` (400 lines)
- `tests/modes/` (600 lines)
- `tests/integration/` (200 lines)

**Total New Code**: ~21,000 lines

---

## 🎯 Skill Invocations Per Wave

### Wave 0:
- **Manual setup** (no skills, just structure)

### Wave 1:
- **python-expert** (5 agents)
- **technical-writer** (1 agent - YAML definitions)

### Wave 2:
- **python-expert** (3 agents)

### Wave 3:
- **python-expert** (2 agents)
- **fastapi-expert** (1 agent)

### Wave 4:
- **react-expert** (3 agents)
- **typescript-expert** (3 agents)
- **tailwind-expert** (2 agents)

### Wave 5:
- **python-expert** (4 agents)

### Wave 6:
- **python-expert** (3 agents)
- **react-expert** (1 agent)
- **typescript-expert** (1 agent)

### Wave 7:
- **python-expert** (3 agents)
- **react-expert** (1 agent)
- **typescript-expert** (1 agent)

### Wave 8:
- **python-expert** (1 agent)
- **react-expert** (3 agents)
- **typescript-expert** (3 agents)

### Wave 9:
- **python-expert** (2 agents)
- **react-expert** (1 agent)
- **typescript-expert** (1 agent)

### Wave 10:
- **python-expert** (3 agents)
- **react-expert** (1 agent)
- **technical-writer** (1 agent - documentation)

**Total Agent Invocations**: ~45 agents across 10 waves

---

## 🔧 Technical Implementation Details

### WebSocket Protocol

**Events (Backend → Dashboard)**:
```typescript
// Event format
interface SocketEvent {
    type: string;  // "skill:started", "decision:point", etc.
    timestamp: string;
    data: any;
}

// Examples
{
    type: "skill:started",
    timestamp: "2025-11-15T22:30:45.123Z",
    data: {
        skill_name: "library_discovery",
        parameters: { feature: "auth" }
    }
}

{
    type: "decision:point",
    timestamp: "2025-11-15T22:31:12.456Z",
    data: {
        id: "decision_1",
        question: "Should I refactor authentication?",
        options: [
            { label: "Yes, refactor now", pros: [...], cons: [...], confidence: 0.82 },
            { label: "No, just fix bug", pros: [...], cons: [...], confidence: 0.91 }
        ],
        recommended: 1,
        timeout_seconds: 30
    }
}
```

**Commands (Dashboard → Backend)**:
```typescript
// Command format
interface DashboardCommand {
    type: 'HALT' | 'RESUME' | 'ROLLBACK' | 'REDIRECT' | 'DECISION' | 'INJECT';
    params?: any;
}

// Examples
{ type: "HALT" }
{ type: "ROLLBACK", params: { steps: 5 } }
{ type: "DECISION", params: { decision_id: "decision_1", selected: 1 } }
{ type: "INJECT", params: { constraint: "Use async/await pattern" } }
```

### State Checkpoint Format

```python
@dataclass
class Checkpoint:
    id: str  # UUID
    label: str  # Human-readable (skill name)
    timestamp: datetime

    # Execution state
    skill_stack: List[str]  # Skills executed so far
    current_skill: Optional[str]
    next_skills: List[str]

    # File system
    file_snapshots: Dict[str, str]  # path → content (only changed files)
    file_hashes: Dict[str, str]  # path → SHA256 (for verification)

    # Git state
    git_branch: str
    git_commit: str
    git_stash_id: Optional[str]  # If we used git stash

    # Context
    execution_context: Dict[str, Any]
    decision_history: List[Decision]

    # Agents
    agent_states: List[AgentState]

    # Metadata
    rollback_count: int = 0  # How many times rolled back to this
    restored_from: Optional[str] = None  # If restored, from which checkpoint

def create_checkpoint(label: str) -> Checkpoint:
    """Create checkpoint of current state"""
    return Checkpoint(
        id=str(uuid.uuid4()),
        label=label,
        timestamp=datetime.now(),
        skill_stack=current_skill_stack.copy(),
        file_snapshots=snapshot_changed_files(),
        git_commit=get_current_commit(),
        execution_context=context.copy(),
        agent_states=[a.snapshot() for a in agents]
    )

async def restore_checkpoint(checkpoint: Checkpoint):
    """Restore to checkpoint state"""
    # Restore files
    for path, content in checkpoint.file_snapshots.items():
        await write_file(path, content)

    # Restore git if needed
    if checkpoint.git_commit != get_current_commit():
        await git_reset_hard(checkpoint.git_commit)

    # Restore context
    context.update(checkpoint.execution_context)

    # Restore agents
    for agent_state in checkpoint.agent_states:
        await restore_agent(agent_state)

    # Verify
    verify_restoration(checkpoint)
```

### Skill Definition Examples

**Composite Skill**:
```yaml
# skills/built-in/test_and_commit.yaml
skill:
  name: test_and_commit
  version: 1.0.0
  description: Run all tests and commit if passing
  category: workflow

  execution:
    type: composite
    skills:
      - skill: validation_orchestrator
        parameters:
          tiers: [1, 2, 3]
        on_failure: halt

      - skill: git_operations
        method: commit_changes
        parameters:
          message: "feat: ${task_summary}"
        on_failure: rollback

  hooks:
    pre:
      - ensure_clean_git_state
    post:
      - notify_success
    error:
      - alert_failure
      - rollback_changes
```

**MCP Skill**:
```yaml
# skills/built-in/fire_crawl_research.yaml
skill:
  name: fire_crawl_research
  version: 1.0.0
  description: Deep crawl documentation with Fire Crawl MCP
  category: research

  parameters:
    - name: url
      type: string
      required: true
    - name: max_pages
      type: integer
      default: 50

  execution:
    type: mcp
    mcp_server: firecrawl
    mcp_tool: firecrawl_crawl
    timeout: 120

  hooks:
    post:
      - cache_results_in_memory
      - extract_knowledge_with_tavali
```

---

## 📋 Dependencies Installation Order

### Python Backend

```bash
# Wave 0
poetry add fastapi python-socketio pyyaml jsonschema networkx uvicorn

# Wave 3 (additional)
poetry add python-multipart aiofiles websockets

# Wave 9 (research)
poetry add beautifulsoup4 lxml  # For web parsing if needed
```

### Frontend Dashboard

```bash
# Wave 4
cd dashboard
npm install socket.io-client zustand react-router-dom
npm install tailwindcss postcss autoprefixer
npm install lucide-react  # Icons
npm install react-diff-viewer-continued  # Diff display
npm install @monaco-editor/react  # Code editor
npm install recharts  # Charts for metrics

# Dev dependencies
npm install -D @types/node @types/react
```

---

## ✅ Exit Criteria by Wave

### Wave 0: Foundation
- [ ] Project structure created
- [ ] All dependencies installed
- [ ] Schemas defined
- [ ] Base models implemented
- [ ] Tests directory setup

### Wave 1: Skills Framework
- [ ] Can load skills from YAML
- [ ] Can execute skills
- [ ] Hooks execute correctly
- [ ] 4 built-in skills defined
- [ ] Integration test passes

### Wave 2: Discovery & Dependencies
- [ ] Discovers skills from all sources
- [ ] Resolves dependencies (no cycles)
- [ ] Catalog persists to Memory MCP
- [ ] Quick reload from cache

### Wave 3: WebSocket
- [ ] Server running on port 8000
- [ ] Client can connect
- [ ] Events stream <50ms latency
- [ ] Commands received correctly

### Wave 4: Dashboard Core
- [ ] Dashboard loads at localhost:3000
- [ ] Shows 3 panels
- [ ] HALT/RESUME buttons work
- [ ] Real-time updates visible

### Wave 5: shannon do
- [ ] Command exists
- [ ] Parses tasks correctly
- [ ] Orchestrates skills
- [ ] Checkpoints created
- [ ] Can HALT/ROLLBACK

### Wave 6: Agents
- [ ] Can spawn agents
- [ ] Parallel execution works
- [ ] Agent panel shows status
- [ ] Performance improvement measured

### Wave 7: Debug Mode
- [ ] shannon debug exists
- [ ] Halts at decision points
- [ ] Investigation tools work
- [ ] Debug view functional

### Wave 8: Full Dashboard
- [ ] All 6 panels visible
- [ ] Decision points presented
- [ ] All controls functional
- [ ] <100ms response time

### Wave 9: Advanced Modes
- [ ] shannon ultrathink generates hypotheses
- [ ] shannon research synthesizes knowledge
- [ ] 500+ step reasoning works
- [ ] Research orchestration functional

### Wave 10: Complete
- [ ] Pattern detection working
- [ ] Dynamic skill creation functional
- [ ] Performance optimized
- [ ] Documentation complete
- [ ] Production ready

---

## 🚀 Quick Start (Day 1 Instructions)

**When approved, start immediately with**:

```bash
# 1. Create structure
mkdir -p src/shannon/{skills,orchestration,communication,modes,research,server}
mkdir -p skills/built-in
mkdir -p schemas
mkdir -p tests/skills

# 2. Install dependencies
poetry add fastapi python-socketio pyyaml jsonschema networkx uvicorn[standard]

# 3. Create first schema
cat > schemas/skill.schema.json << 'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["name", "version", "description", "execution"],
  "properties": {
    "name": {"type": "string"},
    "version": {"type": "string"},
    "description": {"type": "string"},
    "execution": {
      "type": "object",
      "required": ["type"],
      "properties": {
        "type": {"enum": ["native", "script", "mcp", "composite"]}
      }
    }
  }
}
EOF

# 4. Create first model
cat > src/shannon/skills/models.py << 'EOF'
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

@dataclass
class Skill:
    name: str
    version: str
    description: str
    # ... (complete implementation)
EOF

# 5. Invoke first agent
shannon wave --spec "SHANNON_V4_WAVE_EXECUTION_PLAN.md" --wave 1 --agent A
```

---

## 📊 Success Metrics (Measurable)

### Week 2 (After Wave 1):
- [ ] Can load ≥4 skills from YAML
- [ ] Skill execution success rate: 100%
- [ ] Hook execution success rate: 100%

### Week 4 (After Wave 4):
- [ ] Dashboard connects: 100% success
- [ ] Event latency: <50ms average
- [ ] Dashboard panels: 3/6 working

### Week 6 (After Wave 6):
- [ ] Agent spawn success: 100%
- [ ] Parallel speedup: ≥1.5x for independent skills
- [ ] Agent pool: 8 active agents demonstrated

### Week 8 (After Wave 8):
- [ ] HALT response time: <100ms
- [ ] Rollback success rate: 100%
- [ ] Decision points: User input captured 100%
- [ ] Dashboard panels: 6/6 working

### Week 10 (Complete):
- [ ] Pattern detection: ≥90% accuracy
- [ ] Dynamic skill generation: ≥80% useful
- [ ] Task success rate: ≥85%
- [ ] User intervention: <20% of tasks
- [ ] System uptime: ≥99.9%

---

## 🎓 Contextual Knowledge Requirements

### For Skills Framework (Waves 1-2):
- **Read**: shannon-cli-4.md lines 45-260 (Skills framework specification)
- **Read**: Existing `src/shannon/executor/*.py` (understand current modules)
- **Context7**: Pull Python YAML, jsonschema, networkx docs
- **Memory**: Load any previous skill framework implementations

### For WebSocket/Dashboard (Waves 3-4):
- **Read**: shannon-cli-4.md lines 1670-1975 (Dashboard architecture)
- **Context7**: Pull FastAPI, python-socketio, React, Socket.io-client docs
- **Memory**: Load any WebSocket patterns from previous work

### For Orchestration (Waves 5-6):
- **Read**: shannon-cli-4.md lines 502-615 (shannon do execution flow)
- **Read**: shannon-cli-4.md lines 1816-1848 (Agent coordination)
- **Context7**: Pull Python asyncio docs
- **Memory**: Load orchestration patterns

### For Specialized Modes (Waves 7-9):
- **Read**: shannon-cli-4.md lines 685-1597 (Debug & Ultrathink specifications)
- **Context7**: Pull Sequential MCP documentation
- **Memory**: Load debugging patterns

### For Dynamic Skills (Wave 10):
- **Read**: shannon-cli-4.md lines 218-260 (Dynamic skill creation)
- **Context7**: Pull pattern detection algorithms
- **Memory**: Load ML/pattern recognition approaches

---

## 🎬 Execution Command

**To start this plan**:

```bash
# Option 1: Execute all waves sequentially
shannon wave --plan "SHANNON_V4_WAVE_EXECUTION_PLAN.md" --execute-all

# Option 2: Execute specific wave
shannon wave --plan "SHANNON_V4_WAVE_EXECUTION_PLAN.md" --wave 1

# Option 3: Execute specific agent in wave
shannon wave --plan "SHANNON_V4_WAVE_EXECUTION_PLAN.md" --wave 1 --agent A
```

**With context priming**:
```bash
# Prime context first, then execute
/prime --deep
shannon wave --plan "SHANNON_V4_WAVE_EXECUTION_PLAN.md" --execute-all
```

---

## 🎯 MVP vs Full Release

### MVP (After Wave 6) - 6 weeks

**Includes**:
- ✅ Skills Framework (define, discover, execute with hooks)
- ✅ shannon do command (orchestrate tasks)
- ✅ Dashboard (3 panels: Overview, Skills, Files)
- ✅ WebSocket communication
- ✅ Basic steering (HALT/RESUME)
- ✅ Agent coordination

**Deferred to V4.1**:
- Debug mode
- Ultrathink mode
- Research orchestrator
- Dynamic skill generation
- Full 6-panel dashboard

**MVP Value**: Working interactive orchestration system!

### Full Release (After Wave 10) - 10 weeks

**Everything** from spec including advanced modes and self-improvement

---

## 💾 Checkpoint Strategy

**After each wave**:
```bash
# Create checkpoint
git add -A
git commit -m "Wave X complete: [description]"
git tag "v4.0-wave-X"

# Save state to Serena
/checkpoint create "wave-X-complete"

# Document completion
echo "Wave X: COMPLETE" >> WAVES_PROGRESS.md
```

**Rollback if needed**:
```bash
# Rollback to previous wave
git reset --hard v4.0-wave-X
/checkpoint restore "wave-X-complete"
```

---

## 📈 Progress Tracking

**Use TodoWrite after each wave to track**:

Wave 1 Todos:
- [ ] SkillRegistry implemented
- [ ] SkillLoader implemented
- [ ] HookManager implemented
- [ ] SkillExecutor implemented
- [ ] 4 built-in skills defined
- [ ] Integration test passes

(Repeat for all waves)

---

## ⚠️ Risks & Mitigation

### Risk 1: WebSocket Latency
- **Target**: <50ms event streaming
- **Mitigation**: Benchmark in Wave 3, optimize serialization, use binary if needed

### Risk 2: State Snapshot Size
- **Concern**: Large checkpoints slow rollback
- **Mitigation**: Only snapshot changed files, use git stash for large changes

### Risk 3: React Dashboard Complexity
- **Concern**: 5,000 lines may take longer
- **Mitigation**: Use UI library (shadcn/ui), start with 3 panels (MVP)

### Risk 4: Agent Coordination Bugs
- **Concern**: Race conditions, deadlocks
- **Mitigation**: Extensive testing, use asyncio primitives correctly, timeouts

---

## 🏁 Final Deliverables

### Code
- [ ] ~21,000 lines new code (backend + frontend)
- [ ] 3,435 lines existing code (reused as skills)
- [ ] All code tested and documented

### Documentation
- [ ] Skills Development Guide
- [ ] Dashboard User Guide
- [ ] Command Reference
- [ ] Architecture Documentation
- [ ] API Documentation (WebSocket protocol)

### Testing
- [ ] Unit tests for all modules
- [ ] Integration tests for each wave
- [ ] E2E test for full workflow
- [ ] Performance benchmarks
- [ ] Load testing results

### Deployment
- [ ] Production build scripts
- [ ] Docker container (optional)
- [ ] Installation guide
- [ ] Troubleshooting guide

---

**Status**: Plan complete and ready for execution
**Start**: Awaiting user approval, then begin Wave 0
**Timeline**: 8-10 weeks to full release, 6 weeks to MVP

