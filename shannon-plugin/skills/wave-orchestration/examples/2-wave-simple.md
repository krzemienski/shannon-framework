# Example: 2-Wave Simple Project

**Project**: Task Management Web App (Simple)

**8D Complexity Score**: 0.45 (Moderate)

**Phase Plan**: 3 phases → 2 waves

---

## Input: Phase Plan

```json
{
  "project": "Task Management Web App",
  "complexity_score": 0.45,
  "phases": [
    {
      "id": 1,
      "name": "Architecture Design",
      "dependencies": [],
      "estimated_time": "10 minutes",
      "deliverables": ["System architecture", "API contracts", "DB schema"]
    },
    {
      "id": 2,
      "name": "Core Implementation",
      "dependencies": [1],
      "estimated_time": "15 minutes",
      "deliverables": ["React UI", "Express API", "PostgreSQL schema"],
      "parallelizable": true,
      "sub_phases": [
        {"name": "React UI", "agent_type": "frontend-builder"},
        {"name": "Express API", "agent_type": "backend-builder"},
        {"name": "PostgreSQL Schema", "agent_type": "database-builder"}
      ]
    },
    {
      "id": 3,
      "name": "Testing",
      "dependencies": [2],
      "estimated_time": "10 minutes",
      "deliverables": ["Puppeteer tests"],
      "parallelizable": false
    }
  ]
}
```

---

## Step 1: Dependency Analysis

```python
dependency_graph = {
    1: {
        "name": "Architecture Design",
        "depends_on": [],
        "blocks": [2],
        "estimated_time": 10
    },
    2: {
        "name": "Core Implementation",
        "depends_on": [1],
        "blocks": [3],
        "estimated_time": 15
    },
    3: {
        "name": "Testing",
        "depends_on": [2],
        "blocks": [],
        "estimated_time": 10
    }
}

# Validation: No circular dependencies ✅
# Critical path: 1 → 2 → 3 (35 minutes sequential)
```

---

## Step 2: Wave Structure Generation

```python
waves = [
    {
        "wave_number": 1,
        "wave_name": "Architecture",
        "phases": [1],
        "parallel": False,  # Single phase
        "estimated_time": 10,
        "dependencies": []
    },
    {
        "wave_number": 2,
        "wave_name": "Core Implementation",
        "phases": [2],  # Sub-phases: React, Express, PostgreSQL
        "parallel": True,  # 3 sub-phases can run parallel
        "estimated_time": 15,
        "dependencies": [1]
    }
    # Note: Phase 3 (Testing) deferred to next session or separate execution
    # In production: would be Wave 3 after user validates Wave 2
]
```

---

## Step 3: Agent Allocation

```python
# Complexity: 0.45 (Moderate)
# Rule: 2-3 agents maximum

# Wave 1: Architecture Design
wave_1_agents = 1  # Single architect agent

# Wave 2: Core Implementation
wave_2_agents = 3  # 1 per sub-phase (React, Express, PostgreSQL)

agent_allocation = {
    "wave_1": {
        "agents": 1,
        "assignments": [
            {
                "agent_type": "architect",
                "task": "Design system architecture, API contracts, DB schema"
            }
        ]
    },
    "wave_2": {
        "agents": 3,
        "assignments": [
            {
                "agent_type": "frontend-builder",
                "task": "Build React UI components"
            },
            {
                "agent_type": "backend-builder",
                "task": "Build Express API endpoints"
            },
            {
                "agent_type": "database-builder",
                "task": "Create PostgreSQL schema"
            }
        ]
    }
}
```

---

## Step 4: Synthesis Checkpoints

```python
checkpoints = [
    {
        "checkpoint_id": "wave_1_checkpoint",
        "location": "After architecture design",
        "validation_criteria": [
            "Architecture document created",
            "API contracts defined",
            "Database schema designed",
            "User validates architecture"
        ],
        "serena_keys": ["wave_1_complete", "architecture_complete"],
        "user_validation_required": True
    },
    {
        "checkpoint_id": "wave_2_checkpoint",
        "location": "After core implementation",
        "validation_criteria": [
            "All 3 agents completed successfully",
            "React UI components built",
            "Express API endpoints implemented",
            "PostgreSQL schema created",
            "No integration conflicts"
        ],
        "serena_keys": [
            "wave_2_complete",
            "wave_2_frontend_results",
            "wave_2_backend_results",
            "wave_2_database_results"
        ],
        "user_validation_required": True
    }
]
```

---

## Execution

### Wave 1: Architecture Design (Single Agent)

```markdown
## Spawning Wave 1: Architecture Design

**Wave Configuration**:
- Agents: 1
- Type: Single agent (no parallelization)
- Dependencies: None
- Estimated Time: 10 minutes

**Agent Assignment**:
Agent 1 (architect): Design system architecture, API contracts, DB schema

**Spawning 1 agent**:
<invoke name="Task">
  <parameter name="subagent_type">architect</parameter>
  <parameter name="description">Design task management system architecture</parameter>
  <parameter name="prompt">
    [Context loading protocol]

    YOUR TASK: Design complete architecture for task management web app
    - System architecture (React + Express + PostgreSQL)
    - API contracts (REST endpoints for task CRUD)
    - Database schema (tasks, users tables)

    DELIVERABLES:
    - Architecture document in Serena
    - API contract definitions
    - Database schema

    SAVE: write_memory("architecture_complete", {...})
  </parameter>
</invoke>

**Expected Duration**: 10 minutes
```

**Wave 1 Results**:
```json
{
  "wave_number": 1,
  "execution_time": 8,
  "deliverables": {
    "architecture_document": "Created",
    "api_contracts": "5 endpoints defined",
    "database_schema": "2 tables designed"
  },
  "user_validation": "Approved"
}
```

---

### Wave 2: Core Implementation (Parallel - 3 Agents)

```markdown
## Spawning Wave 2: Core Implementation

**Wave Configuration**:
- Agents: 3
- Type: Fully Parallel
- Dependencies: wave_1_complete
- Estimated Time: max(15, 15, 15) = 15 minutes

**Context Loaded**:
✓ spec_analysis
✓ phase_plan_detailed
✓ wave_1_complete
✓ architecture_complete

**Agent Assignments**:
1. frontend-builder: React UI components
2. backend-builder: Express API endpoints
3. database-builder: PostgreSQL schema

**Spawning 3 agents in PARALLEL** (ONE message):
<function_calls>
  <invoke name="Task">
    <parameter name="subagent_type">frontend-builder</parameter>
    <parameter name="description">Build React UI components</parameter>
    <parameter name="prompt">
      [Context loading protocol]

      YOUR TASK: Build React UI components for task management
      - TaskCard component
      - TaskList component
      - TaskForm component

      DELIVERABLES:
      - src/components/TaskCard.tsx
      - src/components/TaskList.tsx
      - src/components/TaskForm.tsx

      SAVE: write_memory("wave_2_frontend_results", {...})
    </parameter>
  </invoke>

  <invoke name="Task">
    <parameter name="subagent_type">backend-builder</parameter>
    <parameter name="description">Build Express API endpoints</parameter>
    <parameter name="prompt">
      [Context loading protocol]

      YOUR TASK: Build Express REST API
      - GET /api/tasks
      - POST /api/tasks
      - PUT /api/tasks/:id
      - DELETE /api/tasks/:id

      DELIVERABLES:
      - src/routes/tasks.js
      - src/controllers/taskController.js

      SAVE: write_memory("wave_2_backend_results", {...})
    </parameter>
  </invoke>

  <invoke name="Task">
    <parameter name="subagent_type">database-builder</parameter>
    <parameter name="description">Create PostgreSQL schema</parameter>
    <parameter name="prompt">
      [Context loading protocol]

      YOUR TASK: Create PostgreSQL database schema
      - tasks table (id, title, description, status, created_at)
      - users table (id, username, email, created_at)

      DELIVERABLES:
      - migrations/001_create_tasks.sql
      - migrations/002_create_users.sql

      SAVE: write_memory("wave_2_database_results", {...})
    </parameter>
  </invoke>
</function_calls>

**Execution**: All 3 agents run SIMULTANEOUSLY
**Expected Duration**: 15 minutes (not 45 minutes sequential)
```

**Wave 2 Results**:
```json
{
  "wave_number": 2,
  "agents_deployed": 3,
  "execution_time": 14,
  "sequential_time_hypothetical": 42,
  "speedup": "3.0x",
  "deliverables": {
    "frontend": {
      "files_created": 3,
      "components": ["TaskCard", "TaskList", "TaskForm"]
    },
    "backend": {
      "files_created": 2,
      "endpoints": ["GET /tasks", "POST /tasks", "PUT /tasks/:id", "DELETE /tasks/:id"]
    },
    "database": {
      "files_created": 2,
      "tables": ["tasks", "users"]
    }
  },
  "integration_status": "All components integrate cleanly",
  "user_validation": "Approved"
}
```

---

## Performance Analysis

### Parallelization Metrics

```python
# Wave 2 Performance
agents = 3
execution_times = [12, 14, 13]  # minutes per agent (actual)

sequential_time = sum(execution_times)  # 12 + 14 + 13 = 39 minutes
parallel_time = max(execution_times)    # max(12, 14, 13) = 14 minutes

speedup = sequential_time / parallel_time  # 39 / 14 = 2.79x
efficiency = speedup / agents              # 2.79 / 3 = 93%

print(f"Wave 2: {agents} agents in {parallel_time} minutes")
print(f"Sequential would be {sequential_time} minutes")
print(f"Speedup: {speedup:.2f}x faster")
print(f"Efficiency: {efficiency:.0%} (excellent!)")
```

**Results**:
- **2.79x speedup** (close to 3x ideal for 3 agents)
- **93% efficiency** (excellent parallelization)
- **14 minutes** actual vs **39 minutes** sequential
- **25 minutes saved** through parallelization

### Overall Project Performance

```python
total_time_parallel = 8 + 14  # Wave 1 + Wave 2 = 22 minutes
total_time_sequential = 8 + 39  # Architecture + Sequential impl = 47 minutes

overall_speedup = total_time_sequential / total_time_parallel
# 47 / 22 = 2.14x faster overall

time_saved = total_time_sequential - total_time_parallel
# 47 - 22 = 25 minutes saved
```

**Overall Impact**:
- **2.14x overall speedup** for the project
- **25 minutes saved** (53% time reduction)
- **Moderate complexity** (0.45) achieved **good parallelization**

---

## Lessons Learned

### What Worked Well

✅ **Clear dependency structure**: Architecture → Implementation → Testing
✅ **Independent sub-phases**: React, Express, PostgreSQL had no inter-dependencies
✅ **Appropriate wave size**: 3 agents manageable for moderate complexity
✅ **Clean synthesis**: Easy to aggregate 3 agent results
✅ **User validation**: Clear checkpoints between waves

### Optimization Opportunities

- Could have combined Architecture with 1 implementation agent (if experienced)
- Testing phase could be added as Wave 3 for complete workflow
- Token budget was under-utilized (could support more agents if needed)

### Key Takeaways

1. Even **moderate complexity** (0.45) benefits from wave orchestration
2. **2-3 agents** sweet spot for moderate projects
3. **Parallelization efficiency** high (93%) when phases truly independent
4. **User validation** critical between waves for quality
5. **Context loading** ensures all agents aligned on architecture

---

## Next Wave (If Continuing)

### Wave 3: Testing (Not Executed in Example)

```python
wave_3 = {
    "wave_number": 3,
    "wave_name": "Testing",
    "agents": 1,
    "dependencies": ["wave_2_complete"],
    "agent_assignment": {
        "agent_type": "testing-specialist",
        "task": "Create Puppeteer functional tests",
        "deliverables": [
            "tests/functional/taskManagement.test.js",
            "Puppeteer tests for all user flows"
        ]
    },
    "estimated_time": 10
}
```

This example demonstrates simple but effective wave orchestration for a moderate complexity project.
