# Shannon Framework - Wave Execution Flow

## 5-Phase Wave Execution

```
┌─────────────────────────────────────────────────────────────────┐
│                    WAVE ORCHESTRATION FLOW                      │
└─────────────────────────────────────────────────────────────────┘

Phase 1: DISCOVERY
┌─────────────────────────────────────────────────────────────────┐
│  Objective: Understand problem space and requirements           │
│                                                                  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐                   │
│  │ Research  │  │ Context   │  │ Scope     │                   │
│  │  Agent    │  │ Analyzer  │  │ Evaluator │                   │
│  └───────────┘  └───────────┘  └───────────┘                   │
│       │              │              │                           │
│       └──────────────┼──────────────┘                           │
│                      ▼                                          │
│          ┌──────────────────────┐                               │
│          │  Problem Definition  │                               │
│          │  Constraints Map     │                               │
│          │  Success Criteria    │                               │
│          └──────────────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
                       │
                       ▼ Reflection Gate
                       │
Phase 2: ANALYSIS
┌─────────────────────────────────────────────────────────────────┐
│  Objective: Deep investigation and complexity assessment        │
│                                                                  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐                   │
│  │ Technical │  │ Dependency│  │ Risk      │                   │
│  │ Analyzer  │  │ Mapper    │  │ Assessor  │                   │
│  └───────────┘  └───────────┘  └───────────┘                   │
│       │              │              │                           │
│       └──────────────┼──────────────┘                           │
│                      ▼                                          │
│          ┌──────────────────────┐                               │
│          │  Complexity Scores   │                               │
│          │  Dependencies Graph  │                               │
│          │  Risk Assessment     │                               │
│          └──────────────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
                       │
                       ▼ Reflection Gate
                       │
Phase 3: SYNTHESIS
┌─────────────────────────────────────────────────────────────────┐
│  Objective: Integrate findings and design solution              │
│                                                                  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐                   │
│  │ Solution  │  │ Strategy  │  │ Resource  │                   │
│  │ Designer  │  │ Planner   │  │ Allocator │                   │
│  └───────────┘  └───────────┘  └───────────┘                   │
│       │              │              │                           │
│       └──────────────┼──────────────┘                           │
│                      ▼                                          │
│          ┌──────────────────────┐                               │
│          │  Implementation Plan │                               │
│          │  Agent Allocation    │                               │
│          │  Success Metrics     │                               │
│          └──────────────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
                       │
                       ▼ Reflection Gate
                       │
Phase 4: IMPLEMENTATION
┌─────────────────────────────────────────────────────────────────┐
│  Objective: Execute solution with parallel coordination         │
│                                                                  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐   │
│  │ Builder   │  │ Optimizer │  │ Integrator│  │ Tester    │   │
│  │  Agent    │  │  Agent    │  │  Agent    │  │  Agent    │   │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘   │
│       │              │              │              │           │
│       └──────────────┼──────────────┼──────────────┘           │
│                      ▼              ▼                           │
│          ┌──────────────────────────────┐                       │
│          │  Code Implementation         │                       │
│          │  Configuration Updates       │                       │
│          │  Integration Complete        │                       │
│          └──────────────────────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
                       │
                       ▼ Reflection Gate
                       │
Phase 5: VALIDATION
┌─────────────────────────────────────────────────────────────────┐
│  Objective: Verify correctness and performance                  │
│                                                                  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐                   │
│  │ Quality   │  │ Performance│ │ Security  │                   │
│  │ Validator │  │ Tester    │  │ Auditor   │                   │
│  └───────────┘  └───────────┘  └───────────┘                   │
│       │              │              │                           │
│       └──────────────┼──────────────┘                           │
│                      ▼                                          │
│          ┌──────────────────────┐                               │
│          │  Test Results        │                               │
│          │  Performance Metrics │                               │
│          │  Validation Report   │                               │
│          └──────────────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
                       │
                       ▼
              ┌───────────────┐
              │  Wave Result  │
              └───────────────┘
```

## Agent Spawning Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT LIFECYCLE                               │
└─────────────────────────────────────────────────────────────────┘

Step 1: Agent Creation
┌──────────────────┐
│  WaveOrchestrator│──────▶ Analyze complexity
│                  │──────▶ Select strategy
│                  │──────▶ Estimate agent count
└──────────────────┘
         │
         ▼
┌──────────────────┐
│   AgentSpawner   │
│                  │
│  ┌────────────┐  │
│  │ Semaphore  │  │◀──── Concurrency control
│  │ (max=10)   │  │      (max_concurrent_agents)
│  └────────────┘  │
└──────────────────┘
         │
         ▼
Step 2: Agent Initialization
┌──────────────────────────────────────┐
│ agent = AgentClass(                  │
│   agent_id = "Type_Counter_Timestamp"│
│   capabilities = {Analysis, ...}     │
│   config = {...}                     │
│ )                                    │
└──────────────────────────────────────┘
         │
         ▼
┌──────────────────┐
│ agent.initialize()│──────▶ Setup resources
│                  │──────▶ Load configuration
│                  │──────▶ State = READY
└──────────────────┘
         │
         ▼
Step 3: Agent Execution
┌──────────────────────────────────────┐
│  async with semaphore:               │
│    result = await agent.run(task)    │
│                                      │
│  State transitions:                  │
│  READY → EXECUTING → COMPLETED       │
│                                      │
│  Metrics tracked:                    │
│  • Execution time                    │
│  • Memory usage                      │
│  • Success/failure count             │
│  • Error traces                      │
└──────────────────────────────────────┘
         │
         ▼
Step 4: Result Collection
┌──────────────────────────────────────┐
│  AgentResult {                       │
│    agent_id: str                     │
│    agent_type: str                   │
│    success: bool                     │
│    output: Any                       │
│    metrics: AgentMetrics             │
│    error_message: Optional[str]      │
│  }                                   │
└──────────────────────────────────────┘
         │
         ▼
Step 5: Agent Cleanup
┌──────────────────┐
│ cleanup_agent()  │──────▶ Cancel if executing
│                  │──────▶ Release resources
│                  │──────▶ Remove from pool
└──────────────────┘
```

## Reflection Points

```
┌─────────────────────────────────────────────────────────────────┐
│                 REFLECTION SYSTEM ARCHITECTURE                   │
└─────────────────────────────────────────────────────────────────┘

Phase Boundary Reflection:
┌──────────────┐
│ Phase N End  │
└──────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Reflection Agent                    │
│                                      │
│  Questions:                          │
│  • Did we achieve phase objectives?  │
│  • What insights were gained?        │
│  • What risks were identified?       │
│  • Should we continue or replan?     │
│                                      │
│  Outputs:                            │
│  • Quality score (0.0-1.0)           │
│  • Confidence level (0.0-1.0)        │
│  • Recommendations                   │
│  • Next phase adjustments            │
└──────────────────────────────────────┘
       │
       ├──▶ Quality ≥ 0.7 ────▶ Continue to next phase
       │
       └──▶ Quality < 0.7 ────▶ Replan or iterate current phase

Wave-Level Reflection:
┌──────────────────────────────────────┐
│  Wave Completion Analysis            │
│                                      │
│  Metrics:                            │
│  • Success rate per phase            │
│  • Total execution time              │
│  • Resource utilization              │
│  • Agent efficiency                  │
│                                      │
│  Learning:                           │
│  • Pattern extraction                │
│  • Strategy effectiveness            │
│  • Error patterns                    │
│  • Optimization opportunities        │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Memory System Storage               │
│  • Success patterns → HOT tier       │
│  • Error patterns → WARM tier        │
│  • Historical data → COLD tier       │
└──────────────────────────────────────┘
```

## Parallel vs Sequential Execution

```
Parallel Execution (Default):
┌─────────────────────────────────────────────────────────────┐
│  Phase: IMPLEMENTATION                                       │
│  parallel_execution: true                                    │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Agent 1  │  │ Agent 2  │  │ Agent 3  │  │ Agent N  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│       ║              ║              ║              ║        │
│       ║              ║              ║              ║        │
│       ▼              ▼              ▼              ▼        │
│  ┌────────────────────────────────────────────────────┐    │
│  │       asyncio.gather() - Concurrent Execution      │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  Duration: max(agent_timeout)                               │
└─────────────────────────────────────────────────────────────┘

Sequential Execution (Dependency Chain):
┌─────────────────────────────────────────────────────────────┐
│  Phase: DISCOVERY                                            │
│  parallel_execution: false                                   │
│                                                              │
│  ┌──────────┐                                               │
│  │ Agent 1  │                                               │
│  └──────────┘                                               │
│       │                                                      │
│       ▼                                                      │
│  ┌──────────┐                                               │
│  │ Agent 2  │                                               │
│  └──────────┘                                               │
│       │                                                      │
│       ▼                                                      │
│  ┌──────────┐                                               │
│  │ Agent N  │                                               │
│  └──────────┘                                               │
│                                                              │
│  Duration: sum(all agent_timeouts)                          │
└─────────────────────────────────────────────────────────────┘
```

## Error Handling and Retry Logic

```
┌─────────────────────────────────────────────────────────────┐
│                  ERROR RECOVERY FLOW                         │
└─────────────────────────────────────────────────────────────┘

Agent Execution:
┌──────────────┐
│ agent.run()  │
└──────────────┘
       │
       ├──▶ Success ────▶ Continue
       │
       └──▶ Exception
              │
              ▼
       ┌────────────┐
       │ Log error  │
       │ Increment  │
       │  retries   │
       └────────────┘
              │
              ├──▶ retries < retry_limit ────▶ Retry execution
              │
              └──▶ retries ≥ retry_limit
                     │
                     ▼
              ┌────────────────┐
              │ Mark as FAILED │
              │ Record error   │
              └────────────────┘
                     │
                     ▼
Wave-level decision:
┌────────────────────────────────────┐
│ validation_level == PRODUCTION?    │
│                                    │
│ YES → Abort wave immediately       │
│ NO  → Continue with best effort    │
└────────────────────────────────────┘
```