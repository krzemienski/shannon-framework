# Agent Tracking Architecture Analysis
**Date**: 2025-11-17
**Analysis During**: Phase 2.1 - Agent Event Discovery

## Problem Statement

Plan (NEXT_SESSION_V3_COMPLETION.md Phase 2) asks to integrate "agent tracking" into wave command, but systematic investigation reveals architectural confusion.

---

## Discovery: Two Separate Agent Systems

### System 1: V3 Agent Tracking (`src/shannon/agents/`)
- **Files**: state_tracker.py (546 lines), controller.py
- **Purpose**: Track individual agents during wave execution
- **Classes**: AgentStateTracker, AgentController, AgentState
- **Status Tracking**: pending → active → complete/failed
- **Features**: Progress%, cost, tokens, files created/modified, thinking blocks
- **Integration Point**: ContextAwareOrchestrator.agents (line 83)
- **Usage**: NEVER - not wired into any execution flow

### System 2: V4 Agent Pool (`src/shannon/orchestration/`)
- **Files**: agent_pool.py, orchestrator.py
- **Purpose**: Parallel agent execution with task queue
- **Classes**: AgentPool, Agent, AgentTask, AgentCoordinator
- **Roles**: RESEARCH, ANALYSIS, TESTING, VALIDATION, GIT, PLANNING
- **Features**: 8 parallel agents, task queue, role-based assignment
- **Integration Point**: ContextAwareOrchestrator.agent_pool (line 120)
- **Usage**: NEVER - created but not used in execution

---

## Discovery: Two Separate Orchestrators

### Orchestrator 1: V3 ContextAwareOrchestrator (`src/shannon/orchestrator.py`)
- **Purpose**: Integrate 8 V3 features (cache, cost, analytics, context, metrics, MCP, agents, agent_pool)
- **Used By**: shannon analyze, shannon wave
- **execute_analyze()**: ✅ FULLY IMPLEMENTED
  - Cache check → cost optimize → execute SDK → save cache → record analytics
  - Working, tested, integrated
- **execute_wave()**: ⚠️ STUB
  - Just calls `self.sdk_client.invoke_skill('wave-orchestration', prompt)`
  - Returns Framework result
  - Does NOT use agent_pool or agents
  - Does NOT spawn/track/coordinate anything

### Orchestrator 2: V4 Orchestration.Orchestrator (`src/shannon/orchestration/orchestrator.py`)
- **Purpose**: Execute multi-step plans with dashboard events
- **Used By**: shannon do  (v4_commands/do.py)
- **execute()**: Loops through plan.steps, executes skills sequentially
  - Emits: execution:started, skill:started, skill:completed, execution:completed
  - Has dashboard_client
  - Does NOT use AgentPool either!

---

## Discovery: Commands Using Different Systems

### shannon analyze → V3 ContextAwareOrchestrator
- ✅ Fully integrated
- Uses: cache, cost, analytics, metrics, MCP
- Does NOT use: agents or agent_pool

### shannon wave → V3 ContextAwareOrchestrator
- ⚠️ Partially integrated
- Uses: ContextAwareOrchestrator (initialized)
- Calls: Framework `/shannon:wave` skill (single call, returns result)
- Does NOT use: agents or agent_pool
- Returns: Summary only (agents_deployed: 1, no details)

### shannon do → V4 orchestration.Orchestrator
- ✅ Different system entirely
- Uses: orchestration.Orchestrator with ExecutionPlan
- Executes: plan.steps sequentially via SkillExecutor
- Emits: execution/skill events to dashboard
- Does NOT use: AgentPool (even though code exists)

---

## Agent Pool Implementation Status

**Code Exists**:
- ✅ agent_pool.py (440 lines, complete implementation)
- ✅ AgentPool class with all methods
- ✅ Dashboard AgentPool panel (dashboard/src/panels/AgentPool.tsx)
- ✅ Dashboard event handlers (agent:spawned, agent:progress, agent:completed)
- ✅ Tests (9/9 passing in Wave 1)

**Code Does NOT Exist**:
- ❌ Any execution code that calls agent_pool.create_agent()
- ❌ Any execution code that calls agent_pool.assign_task()
- ❌ Any execution code that emits agent:spawned events
- ❌ Integration between execution and AgentPool

**Agent 2 Delivered** (from AGENT2_MISSION_COMPLETE.md):
> "AgentPool ready for use... Dashboard ready to display agents"

**But NOT delivered**: The code that USES AgentPool during execution

---

## V3 Agent StateTracker vs V4 Agent Pool

**Are they redundant?**

**AgentStateTracker** (V3 agents/):
- Tracks state of individual agents (messages, cost, progress)
- Thread-safe with Lock
- Methods: register_agent(), mark_started/complete/failed(), update_progress()
- Purpose: Monitor agent execution
- get_active_agents(), get_wave_summary()

**AgentPool** (V4 orchestration/):
- Manages pool of agents with task queue
- Async with asyncio.Lock
- Methods: create_agent(), assign_task(), complete_task()
- Purpose: Coordinate parallel execution
- get_active_agents(), get_agent_stats()

**Relationship**:
- AgentPool CREATES/MANAGES agents (execution layer)
- AgentStateTracker MONITORS agents (observability layer)
- They should work TOGETHER:
  - AgentPool spawns agent → AgentStateTracker registers it
  - AgentPool assigns task → AgentStateTracker marks started
  - AgentPool completes task → AgentStateTracker marks complete
  - Dashboard queries AgentStateTracker for display

**Current Reality**: Neither is wired into execution, so they don't work together

---

## What shannon wave ACTUALLY Does

**Current Implementation** (commands.py lines 628-810):
```python
def wave(request: str, ...):
    # Initialize V3 ContextAwareOrchestrator
    orchestrator = ContextAwareOrchestrator(config)

    # MCP pre-check
    if orchestrator.mcp:
        await orchestrator.mcp.pre_wave_check()

    # Call Framework skill
    messages = []
    async for msg in client.invoke_command('/shannon:wave', request):
        messages.append(msg)
        # Display messages

    # Parse result
    wave_result = parser.extract_wave_result(messages)

    # Save result
    session.write_memory(f"wave_{wave_number}_complete", wave_result)

    # Display result
    ui.display_wave_result(wave_result)
```

**What it doesn't do**:
- Spawn agents via agent_pool
- Track agents via agents (AgentStateTracker)
- Emit agent events to dashboard
- Coordinate parallel execution
- Do anything with the 1,326 + 440 lines of agent code

**Framework returns**: Just a summary (agents_deployed: 1, files_created: [])

---

## What SHOULD Happen (Best Guess from Code)

**Option A: Shannon Framework Should Return Agent Details**
- Framework spawns agents internally
- Returns detailed results per agent
- CLI parses and displays
- **Reality**: Framework returns summary only

**Option B: CLI Should Spawn Agents Using AgentPool**
- Parse wave request into tasks
- Create AgentTask for each
- agent_pool.submit_task() for parallel execution
- Track with AgentStateTracker
- Emit events to dashboard
- **Reality**: No task parsing logic, no agent spawning code

**Option C: AgentPool Is For Future Feature**
- Built for V4 but not yet wired up
- Tests prove it works
- Waiting for parallel wave coordinator
- **Reality**: Most likely - infrastructure exists, integration missing

---

## Conclusion

**AgentPool and AgentStateTracker are**:
- ✅ Implemented (1,766 lines of code)
- ✅ Tested (9/9 tests passing)
- ✅ In ContextAwareOrchestrator (initialized)
- ✅ Dashboard ready (panel + event handlers)
- ❌ NOT USED by any command (wave, do, analyze)
- ❌ NOT INTEGRATED into execution flow
- ❌ NO CODE spawns agents
- ❌ NO CODE emits agent events

**They are**: **Infrastructure without integration** - like a car engine not connected to wheels

---

## Recommendation for V3 Completion

**Phase 2 (Agent Tracking) Status**:
- CANNOT implement as planned
- Plan assumes Framework emits agent events → Framework doesn't
- Plan assumes agent tracking hooks exist → They don't
- Infrastructure exists but execution layer missing

**Options**:
1. **Skip Phase 2**: Move to Phase 3 (Context Management) - achievable
2. **Build integration**: Write task parser + agent spawner (estimate: 8-10 hours, not 3-4)
3. **Minimal stub**: Make wave-agents show pool stats (30 min)

**Recommended**: Option 3 (minimal stub) then Phase 3
- wave-agents command: Query orchestrator.agent_pool.get_agent_stats()
- Shows: "0 agents active (AgentPool ready but not used by wave)"
- Honest about current state
- Can expand when parallel execution added

---

## Technical Debt Identified

1. **Duplicate Systems**: AgentStateTracker vs AgentPool overlap
2. **Unused Code**: 1,766 lines of agent code never executed
3. **Architectural Confusion**: V3 vs V4, two orchestrators, unclear boundaries
4. **Missing Integration**: Agent spawning/coordination layer doesn't exist
5. **Plan Misalignment**: V3 plan assumes features that require V4 parallel execution

---

**Next Actions**:
1. Document this analysis
2. Implement minimal wave-agents stub (show pool stats)
3. Proceed to Phase 3 (Context Management) - clear path
4. Note in completion: "Agent tracking infrastructure built, parallel execution integration pending"
