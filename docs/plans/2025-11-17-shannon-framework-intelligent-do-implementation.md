# Shannon Framework intelligent-do Implementation Plan

**Date**: 2025-11-17
**Goal**: Create comprehensive intelligent-do skill and /shannon:do command in Shannon Framework with Serena MCP backend, full context awareness, and research integration
**Scope**: Shannon Framework (new skill + command) + Shannon CLI (integration)
**Estimated Duration**: 13-20 hours

---

## Requirements Summary

### The One Catch-All Command

**shannon do** should be the intelligent, adaptive execution system that:

1. **Context-Aware**:
   - Uses Serena MCP as backend for persistent context
   - First time: Auto-explores, creates Serena entities
   - Returning: Loads from Serena memories, primes if needed

2. **Intelligent Decision Making**:
   - New project? → Auto spec, plan, execute waves
   - Existing project? → Read memories, understand context, execute
   - Needs research? → Auto-detect, run research before execution
   - Complex task? → Break down with spec-analysis

3. **Full Shannon Integration**:
   - Uses orchestration (wave coordination)
   - Uses project management (goal tracking)
   - Uses TodoWrite (task breakdown)
   - Uses all relevant skills (spec, wave, research, testing)

4. **Works With Shannon CLI**:
   - Shannon CLI invokes Shannon Framework skill
   - CLI adds V3 features (cache, analytics, cost optimization)
   - Seamless integration

---

## Phase 1: Shannon Framework Deep Exploration

**Duration**: 2-3 hours
**Location**: /Users/nick/Desktop/shannon-framework/
**Goal**: Understand complete Framework architecture before building

### Task 1.1: Study Serena MCP Integration Patterns

**Files to Read**:
- skills/spec-analysis/SKILL.md (how it uses Serena)
- skills/wave-orchestration/SKILL.md (Serena checkpoint usage)
- skills/context-preservation/SKILL.md (state saving)
- skills/memory-coordination/SKILL.md (cross-session memory)
- core/PROJECT_MEMORY.md (Serena architecture)

**Extract**:
- Entity naming conventions (project_X, spec_Y, wave_Z)
- Observation patterns (what to store)
- Relation patterns (project → spec → wave)
- Query patterns (how to search/load)

**Output**: Document Serena usage patterns (SERENA_PATTERNS.md)

**Validation**: Can explain Serena entity model completely

---

### Task 1.2: Map Skill Orchestration Patterns

**Files to Read**:
- skills/exec/SKILL.md (newest complex skill)
- skills/task-automation/SKILL.md (workflow orchestration)
- skills/wave-orchestration/SKILL.md (agent spawning)
- core/WAVE_ORCHESTRATION.md (parallel execution)

**Extract**:
- How skills invoke other skills
- How context flows between skills
- How TodoWrite integrates
- How goal-management tracks progress
- How checkpoints work

**Output**: Skill orchestration flow diagrams

**Validation**: Can draw complete execution flow for /shannon:exec

---

### Task 1.3: Study Research Integration

**Files to Read**:
- Skills that do research (check MCP requirements)
- How Shannon determines research is needed
- Research output storage patterns

**Check**:
- Does any skill currently do auto-research detection?
- How is research integrated with execution?
- Storage: Where do research results go in Serena?

**Output**: Research integration strategy

**Validation**: Understand when/how to trigger research

---

### Task 1.4: Understand Command Definitions

**Files to Read**:
- commands/exec.md (newest command)
- commands/task.md (workflow command)
- commands/wave.md (execution command)
- commands/spec.md (analysis command)

**Extract**:
- Command YAML frontmatter structure
- How commands invoke skills
- Parameter passing
- Output formatting
- Error handling

**Output**: Command template for /shannon:do

**Validation**: Can write command definition that follows all conventions

---

## Phase 2: intelligent-do Skill Design

**Duration**: 3-4 hours
**Location**: shannon-framework/skills/intelligent-do/
**Goal**: Create comprehensive skill with all intelligence

### Task 2.1: Design Complete Decision Tree

**Create**: INTELLIGENT_DO_DECISION_TREE.md

**Structure**:
```
ENTRY
├─ Context Check (Serena)
│  ├─ Found → RETURNING_WORKFLOW
│  └─ Not Found → FIRST_TIME_WORKFLOW
│
FIRST_TIME_WORKFLOW
├─ Project Type Detection
│  ├─ Empty directory → NEW_PROJECT
│  └─ Has files → EXISTING_PROJECT
├─ NEW_PROJECT
│  ├─ Run spec-analysis
│  ├─ Create phase plan
│  ├─ Research if needed
│  └─ Execute waves
└─ EXISTING_PROJECT
   ├─ Explore codebase
   ├─ Create Serena entities
   ├─ Detect validation gates
   ├─ Research if needed
   ├─ Run spec-analysis
   └─ Execute waves

RETURNING_WORKFLOW
├─ Load context from Serena
├─ Check currency (timestamp)
├─ Detect changes (file count, git)
├─ Prime Decision
│  ├─ Major changes → Re-prime
│  ├─ Minor changes → Incremental update
│  └─ No changes → Fast path
├─ Research Decision
│  ├─ New libraries? → Research
│  ├─ External APIs? → Research
│  └─ Internal only? → Skip
└─ Execute with context

RESEARCH_DECISION (Called from both workflows)
├─ Parse task for library mentions
├─ Check against project dependencies
├─ Detect external integration keywords
└─ If needed: mcp-discovery + library lookup + Context7

EXECUTION (Final step)
├─ Create TodoWrite task list
├─ Invoke wave-orchestration
├─ Track with goal-management
├─ Save results to Serena
└─ Update project entities
```

**Validation**: Every scenario covered, no ambiguity

---

### Task 2.2: Design Serena Entity Model

**Create**: SERENA_ENTITY_MODEL.md

**Entities**:
```
project_{project_id}
├─ observations:
│  - "project_path: /path/to/project"
│  - "tech_stack: [Python/Flask, PostgreSQL]"
│  - "file_count: 125"
│  - "last_used: 2025-11-17T10:00:00Z"
│  - "validation_gates: pytest, ruff"
│
spec_{task_hash}
├─ observations:
│  - "task: create authentication system"
│  - "complexity: 0.65"
│  - "phases: 5"
│  - "estimated_hours: 8"
│
execution_{session_id}
├─ observations:
│  - "files_created: [auth.py, models.py, tests.py]"
│  - "duration: 450s"
│  - "success: true"
│
memory_{topic}
├─ observations:
│  - "learned: JWT token structure"
│  - "source: Context7 jwt-node"
│  - "applied_in: auth.py"

Relations:
project → spec (analyzed_with)
spec → execution (implemented_by)
execution → memory (created_memory)
project → memory (has_memory)
```

**Validation**: Can serialize/deserialize all project state

---

### Task 2.3: Write Skill Frontmatter

**File**: shannon-framework/skills/intelligent-do/SKILL.md

**Frontmatter**:
```yaml
---
name: intelligent-do
description: |
  Comprehensive intelligent task execution with context awareness, auto-research,
  and adaptive workflows. Uses Serena MCP as persistent backend.

  First time: Explores project, creates entities, runs spec, executes waves.
  Returning: Loads from Serena, primes if needed, fast execution.

  Intelligently decides: Do I need research? Do I need spec analysis?
  Do I need to re-prime? One catch-all command for all scenarios.

skill-type: PROTOCOL
shannon-version: ">=5.1.0"
complexity-triggers: [0.00-1.00]

mcp-requirements:
  required:
    - name: serena
      purpose: Persistent context backend, project memory storage
      fallback: ERROR - Cannot operate without persistent state
      degradation: critical
  recommended:
    - name: sequential
      purpose: Deep analysis for complex decisions
    - name: context7
      purpose: Framework documentation lookup
    - name: tavily
      purpose: Research and library discovery

required-sub-skills:
  - wave-orchestration
  - context-preservation

optional-sub-skills:
  - spec-analysis
  - goal-management
  - memory-coordination
  - mcp-discovery
  - shannon-analysis

allowed-tools: [
  Read, Write, Bash, TodoWrite, AskUserQuestion,
  Serena (all methods), SlashCommand, Context7, Tavily
]

testing:
  functional_test_required: true
  sub_agent_testing: true
  test_skills: [functional-testing]
---
```

**Validation**: YAML parses, all fields correct

---

### Task 2.4: Write Skill Workflow - Entry & Context Check

**Section**: ## Workflow - Step 1: Context Detection

**Content**:
```markdown
### Step 1: Detect Project Context State

**Use Serena MCP to check for existing project**:

\`\`\`python
# Search for project entity
results = search_nodes(query=f"project_{project_id}")

if results and len(results) > 0:
    # Found existing project → RETURNING WORKFLOW
    project_entity = results[0]
    context_state = "RETURNING"
else:
    # New project → FIRST TIME WORKFLOW
    context_state = "FIRST_TIME"
\`\`\`

**Project ID Determination**:
- From working directory name: `Path.cwd().name`
- Sanitized: `re.sub(r'[^a-zA-Z0-9_-]', '_', project_id)`

**Output**: context_state ("FIRST_TIME" or "RETURNING")

---

### Step 2: Route to Appropriate Workflow

\`\`\`python
if context_state == "FIRST_TIME":
    execute_first_time_workflow()
elif context_state == "RETURNING":
    execute_returning_workflow()
\`\`\`
```

**Validation**: Logic clear, Serena API correct

---

### Task 2.5: Write First-Time Workflow

**Section**: ## First-Time Workflow

**Content**:
```markdown
### First-Time Workflow: Comprehensive Onboarding

#### Sub-Step 1A: Detect Project Type

\`\`\`bash
# Check if directory has files
file_count=$(find . -type f | wc -l)

if [ $file_count -eq 0 ] || [ $file_count -lt 3 ]; then
    project_type="NEW_PROJECT"
else:
    project_type="EXISTING_PROJECT"
fi
\`\`\`

#### Sub-Step 1B: NEW_PROJECT Path

**For greenfield projects**:

1. **Run Spec Analysis**:
   \`\`\`
   @skill spec-analysis
   Task: {user_task}
   \`\`\`
   - Gets 8D complexity score
   - Creates phase plan
   - Saves spec_{task_hash} to Serena

2. **Determine Research Need**:
   \`\`\`python
   # Check task for library/framework mentions
   needs_research = check_for_external_dependencies(task)

   if needs_research:
       @skill mcp-discovery
       # Discovers Context7, Tavily as needed

       # Run research for mentioned libraries
       research_results = tavily_search(query="{library_name} best practices")
   \`\`\`

3. **Execute Waves**:
   \`\`\`
   @skill wave-orchestration
   Spec: {from_spec_analysis}
   Context: {research_results if any}
   \`\`\`

4. **Save to Serena**:
   \`\`\`python
   create_entities([{
       "name": f"project_{project_id}",
       "entityType": "project",
       "observations": [
           f"created: {timestamp}",
           f"task: {task}",
           "type: NEW_PROJECT",
           f"files_created: {files}"
       ]
   }])

   create_relations([{
       "from": f"project_{project_id}",
       "to": f"spec_{task_hash}",
       "relationType": "created_from"
   }])
   \`\`\`

#### Sub-Step 1C: EXISTING_PROJECT Path

**For projects with code**:

1. **Explore Project Structure**:
   \`\`\`bash
   # Read key files
   Read(file_path="README.md")
   Read(file_path="package.json") || Read(file_path="pyproject.toml")

   # List directory structure
   Bash("find . -name '*.py' -o -name '*.js' -o -name '*.tsx' | head -50")
   \`\`\`

2. **Analyze & Categorize**:
   \`\`\`python
   # Detect tech stack
   tech_stack = detect_tech_stack(files)  # Python/Flask, React, PostgreSQL, etc.

   # Find entry points
   entry_points = find_entry_points()  # main.py, app.py, index.tsx

   # Detect patterns
   patterns = detect_patterns()  # MVC, REST API, GraphQL, etc.
   \`\`\`

3. **Create Serena Entities**:
   \`\`\`python
   create_entities([{
       "name": f"project_{project_id}",
       "entityType": "project",
       "observations": [
           f"project_path: {path}",
           f"tech_stack: {tech_stack}",
           f"file_count: {file_count}",
           f"entry_points: {entry_points}",
           f"patterns: {patterns}",
           f"explored: {timestamp}"
       ]
   }])
   \`\`\`

4. **Detect Validation Gates**:
   \`\`\`python
   # Check package.json scripts
   if "package.json" in files:
       gates = parse_npm_scripts()  # build, test, lint

   # Check pyproject.toml
   if "pyproject.toml" in files:
       gates = parse_python_tools()  # pytest, ruff

   # Save to Serena
   add_observations([{
       "entityName": f"project_{project_id}",
       "contents": [f"validation_gates: {gates}"]
   }])
   \`\`\`

5. **Ask User for Confirmation** (if not --auto mode):
   \`\`\`
   AskUserQuestion:
     - question: "Detected validation gates. Accept these?"
     - header: "Validation"
     - options:
       - label: "Accept"
         description: "Use detected gates"
       - label: "Customize"
         description: "Modify gates"
   \`\`\`

6. **Determine Research Need**:
   \`\`\`python
   needs_research = (
       mentions_new_library(task, project_dependencies) or
       mentions_external_api(task) or
       mentions_unfamiliar_pattern(task, project_patterns)
   )
   \`\`\`

7. **Run Research if Needed**:
   \`\`\`
   if needs_research:
       # Use mcp-discovery to find appropriate MCP
       @skill mcp-discovery
       Project Domain: {domain}

       # Run research
       research_results = tavily_search(query="{library} implementation guide")

       # Get docs if available
       context7_docs = get_library_docs("{library}")

       # Store research in Serena
       create_entities([{
           "name": f"research_{topic}",
           "entityType": "research",
           "observations": [research_results, context7_docs]
       }])
   \`\`\`

8. **Run Spec Analysis**:
   \`\`\`
   @skill spec-analysis
   Task: {user_task}
   Project Context: {tech_stack}, {patterns}, {entry_points}
   Research: {research_results if any}
   \`\`\`
   - Saves spec_{task_hash} to Serena
   - Returns complexity score and phase plan

9. **Execute Waves**:
   \`\`\`
   @skill wave-orchestration
   Spec: {from_spec_analysis}
   Context: {project_context + research}
   Validation Gates: {gates}
   \`\`\`

10. **Save Execution Results**:
    \`\`\`python
    create_entities([{
        "name": f"execution_{session_id}",
        "entityType": "execution",
        "observations": [
            f"files_created: {files}",
            f"duration: {duration}",
            f"success: {success}"
        ]
    }])

    create_relations([{
        "from": f"project_{project_id}",
        "to": f"execution_{session_id}",
        "relationType": "has_execution"
    }])
    \`\`\`
```

**Validation**: All steps documented, no gaps

---

### Task 2.6: Write Returning Workflow

**Section**: ## Returning Workflow

**Content**:
```markdown
### Returning Workflow: Fast Path with Intelligence

#### Sub-Step 2A: Load Context from Serena

\`\`\`python
# Find project entity
results = search_nodes(query=f"project_{project_id}")
project_entity = results[0]

# Load observations
context = {
    "tech_stack": extract_observation(project_entity, "tech_stack"),
    "file_count": extract_observation(project_entity, "file_count"),
    "patterns": extract_observation(project_entity, "patterns"),
    "entry_points": extract_observation(project_entity, "entry_points"),
    "validation_gates": extract_observation(project_entity, "validation_gates"),
    "last_used": extract_observation(project_entity, "explored")
}
\`\`\`

#### Sub-Step 2B: Check Context Currency

\`\`\`python
# How old is context?
last_used = datetime.fromisoformat(context["last_used"])
age_hours = (datetime.now() - last_used).total_seconds() / 3600

if age_hours > 24:
    context_fresh = False
    print("Context is 24+ hours old - will verify current state")
else:
    context_fresh = True
    print(f"Using cached context ({age_hours:.1f}h old)")
\`\`\`

#### Sub-Step 2C: Detect Changes

\`\`\`bash
# Count current files
current_files=$(find . -name '*.py' -o -name '*.js' -o -name '*.tsx' | wc -l)
cached_files={context["file_count"]}

change_percent=$(( (current_files - cached_files) * 100 / cached_files ))

if [ $change_percent -gt 5 ]; then
    changes_detected=true
else:
    changes_detected=false
fi
\`\`\`

#### Sub-Step 2D: Prime Decision

\`\`\`python
should_reprime = (
    not context_fresh or  # Context too old
    changes_detected      # Codebase changed significantly
)

if should_reprime:
    print("Codebase changed - refreshing context...")

    # Read memories for this project
    @skill memory-coordination
    Project: {project_id}
    Operation: load

    # Incremental update (not full re-onboard)
    new_files = detect_new_files(current_files, context["file_count"])
    read_new_files(new_files[:10])  # Sample new files

    # Update Serena
    add_observations([{
        "entityName": f"project_{project_id}",
        "contents": [
            f"file_count: {current_files}",
            f"updated: {timestamp}"
        ]
    }])
else:
    print("Using cached context (< 1s)")
\`\`\`

#### Sub-Step 2E: Research Decision

\`\`\`python
# Check if task mentions new concepts
new_concepts = extract_unfamiliar_terms(task, context["tech_stack"])

if len(new_concepts) > 0:
    print(f"Detected new concepts: {new_concepts}")

    # Run focused research
    for concept in new_concepts:
        research = tavily_search(query=f"{concept} in {context['tech_stack'][0]}")

        # Save research memory
        create_entities([{
            "name": f"research_{concept}_{timestamp}",
            "entityType": "research",
            "observations": [research]
        }])

    # Link to project
    create_relations([{
        "from": f"project_{project_id}",
        "to": f"research_{concept}_{timestamp}",
        "relationType": "researched"
    }])
\`\`\`

#### Sub-Step 2F: Spec Analysis Decision

\`\`\`python
# For simple tasks, skip spec (use fast path)
task_is_simple = (
    len(task.split()) < 10 and
    "create" in task and
    not any(keyword in task for keyword in ["system", "integrate", "refactor", "migrate"])
)

if task_is_simple:
    print("Simple task - skipping spec analysis")
    spec_result = None
else:
    print("Complex task - running spec analysis")

    @skill spec-analysis
    Task: {task}
    Context: {context}

    spec_result = {returned_from_spec}
\`\`\`

#### Sub-Step 2G: Execute with Context

\`\`\`
# Create TodoWrite for visibility
TodoWrite([
    {"content": "Execute task", "status": "in_progress"},
    {"content": "Validate output", "status": "pending"},
    {"content": "Save results", "status": "pending"}
])

# Execute
@skill wave-orchestration
Task: {task}
Context: {loaded_context}
Spec: {spec_result if any}
Validation Gates: {context["validation_gates"]}

# Update todo
TodoWrite(mark completed)

# Save execution
create_entities([{
    "name": f"execution_{session_id}",
    "entityType": "execution",
    "observations": [
        f"task: {task}",
        f"files: {files_created}",
        f"success: true"
    ]
}])
\`\`\`
```

**Validation**: Returning workflow is fast, intelligent, complete

---

### Task 2.7: Write Research Integration Logic

**Section**: ## Research Decision Logic

**Content**:
```markdown
### Determine if Research is Needed

**Check Task for External Dependencies**:

\`\`\`python
def should_research(task: str, project_context: dict) -> tuple[bool, list[str]]:
    """Determine if research is needed and what to research."""

    research_needed = False
    topics = []

    # 1. Check for library mentions
    common_libraries = [
        # Python
        "django", "flask", "fastapi", "sqlalchemy", "pydantic",
        # JavaScript
        "react", "vue", "angular", "express", "nextjs",
        # Mobile
        "swiftui", "jetpack compose",
        # Databases
        "postgresql", "mongodb", "redis",
        # Auth
        "auth0", "firebase", "supabase",
        # Payment
        "stripe", "paypal"
    ]

    for lib in common_libraries:
        if lib in task.lower():
            # Check if already in project
            if lib not in str(project_context.get("tech_stack", [])).lower():
                topics.append(lib)
                research_needed = True

    # 2. Check for integration keywords
    integration_keywords = [
        "api", "webhook", "oauth", "integration", "connect to",
        "send email", "sms", "notification", "payment"
    ]

    for keyword in integration_keywords:
        if keyword in task.lower():
            # Extract service name if mentioned
            # e.g., "integrate with Twilio" → research Twilio
            topics.append(f"{keyword}_implementation")
            research_needed = True

    # 3. Check for unfamiliar patterns
    pattern_keywords = [
        "graphql", "grpc", "websocket", "sse",
        "microservices", "serverless", "docker"
    ]

    project_patterns = project_context.get("patterns", [])
    for pattern in pattern_keywords:
        if pattern in task.lower() and pattern not in str(project_patterns).lower():
            topics.append(pattern)
            research_needed = True

    return research_needed, topics
\`\`\`

**Execute Research**:

\`\`\`python
if should_research(task, context):
    needs_research, topics = should_research(task, context)

    print(f"Research needed for: {topics}")

    # Discover research MCPs
    @skill mcp-discovery
    Project Domain: {domain_from_context}

    # For each topic
    for topic in topics:
        # Tavily search
        results = tavily_search(query=f"{topic} best practices tutorial")

        # Context7 docs if available
        try:
            docs = context7_get_library_docs(topic)
        except:
            docs = None

        # Save research
        create_entities([{
            "name": f"research_{topic}_{timestamp}",
            "entityType": "research",
            "observations": [
                f"topic: {topic}",
                f"results: {results}",
                f"docs: {docs}",
                f"researched: {timestamp}"
            ]
        }])

        # Link to project
        create_relations([{
            "from": f"project_{project_id}",
            "to": f"research_{topic}_{timestamp}",
            "relationType": "researched"
        }])
\`\`\`
```

**Validation**: Research logic comprehensive, handles all cases

---

### Task 2.8: Write Examples Section

**Section**: ## Examples

**Content**:
```markdown
### Example 1: First Time - New Project

\`\`\`bash
cd /tmp/new-react-app
/shannon:do "create React app with authentication using Auth0"
\`\`\`

**What Happens**:
1. Context check: No project entity → FIRST_TIME
2. Project type: Empty directory → NEW_PROJECT
3. Research: Detects "Auth0" → Researches Auth0 React integration
4. Spec analysis: Runs full 8D (complexity ~0.45)
5. Wave execution: Generates React app with Auth0
6. Saves to Serena: project entity, spec entity, research entities
7. Files created: src/App.tsx, src/auth/Auth0Provider.tsx, etc.

**Time**: ~5-8 minutes

---

### Example 2: Returning - Cached Context

\`\`\`bash
cd /projects/my-flask-api  # Already onboarded
/shannon:do "add password reset endpoint"
\`\`\`

**What Happens**:
1. Context check: Found project entity → RETURNING
2. Load from Serena: tech_stack=[Python/Flask], patterns=[REST API]
3. Check currency: Last used 2 hours ago → Fresh
4. Detect changes: File count same → No changes
5. Research: "password reset" is internal → Skip research
6. Spec: Simple task (< 10 words) → Skip spec, fast path
7. Wave: Executes with cached context
8. Files created: routes/auth.py (password_reset endpoint)
9. Update Serena: Add execution entity

**Time**: ~2-3 minutes (vs 5-8 for first time)

---

### Example 3: Research Integration

\`\`\`bash
cd /projects/legacy-django  # Existing Django app
/shannon:do "add Stripe subscription billing"
\`\`\`

**What Happens**:
1. Context check: Found project → RETURNING
2. Load: tech_stack=[Python/Django], patterns=[MVT, ORM]
3. Research Detection: "Stripe" not in dependencies → RESEARCH NEEDED
4. Research execution:
   - Tavily: "Stripe Python subscription billing tutorial"
   - Context7: stripe-python library docs
   - Saves research entities to Serena
5. Spec analysis: Complexity 0.55 (COMPLEX - billing is mission-critical)
6. Wave execution: Uses research + context
7. Files created: billing/stripe_service.py, models/subscription.py, tests/
8. Saves: Links research → execution

**Time**: ~8-12 minutes (research adds time but ensures quality)
```

**Validation**: Examples cover all scenarios

---

## Phase 3: Create /shannon:do Command

**Duration**: 1-2 hours
**Location**: shannon-framework/commands/
**Goal**: Command definition that invokes intelligent-do skill

### Task 3.1: Write Command File

**File**: shannon-framework/commands/do.md

**Content**:
```markdown
---
name: do
description: |
  Intelligent task execution with auto-context and research.
  One catch-all command that handles everything:
  - First time: Explores, researches, plans, executes
  - Returning: Loads cached context, fast execution
  - Auto-detects: When to research, when to spec, when to prime

usage: |
  /shannon:do "task description"
  /shannon:do "task" --auto           # No questions
  /shannon:do "task" --interactive    # Ask for confirmation

examples:
  - /shannon:do "create authentication system"
  - /shannon:do "add Stripe billing" --auto
  - /shannon:do "refactor user module"

delegates_to:
  - intelligent-do

version: "5.2.0"
---

# /shannon:do Command

## Purpose

One-stop intelligent task execution. Handles:
- ✅ New projects (auto spec + waves)
- ✅ Existing projects (load context + execute)
- ✅ Research integration (auto-detect when needed)
- ✅ Context caching (fast on return)
- ✅ Validation gates (auto-detect or ask)

**Philosophy**: "Just do it intelligently" - minimal user input, maximum automation.

---

## Workflow

### Step 1: Invoke intelligent-do Skill

\`\`\`
@skill intelligent-do

Task: {user_task}
Mode: {auto | interactive}
\`\`\`

### Step 2: Report Results

Display:
- Context used (first-time or cached)
- Research performed (if any)
- Spec complexity (if analyzed)
- Files created
- Validation status (if gates configured)

---

## Parameters

**--auto**: No user questions (autonomous)
**--interactive**: Ask for confirmations (default)
**--no-research**: Skip research even if detected
**--force-spec**: Always run spec analysis

---

## Integration with Shannon CLI

Shannon CLI can invoke this command via:

\`\`\`python
sdk_client.invoke_skill(
    skill_name='intelligent-do',
    prompt_content=task
)
\`\`\`

CLI wraps with V3 features:
- Cache (analysis caching)
- Analytics (session tracking)
- Cost optimization (model selection)
- Dashboard streaming
```

**Validation**: Command follows all conventions

---

## Phase 4: Testing Infrastructure

**Duration**: 2-3 hours
**Location**: shannon-framework/skills/intelligent-do/tests/
**Goal**: Functional tests with sub-agents

### Task 4.1: Create Functional Test Suite

**File**: skills/intelligent-do/tests/test_first_time_workflow.md

**Test Strategy**: Use functional-testing skill patterns

**Test Cases**:
```markdown
### Test 1: New Empty Project

**Setup**:
\`\`\`bash
mkdir /tmp/test-new-project
cd /tmp/test-new-project
\`\`\`

**Execute**:
\`\`\`
@skill intelligent-do
Task: create Flask API with user authentication
\`\`\`

**Validate**:
- ✓ Spec analysis ran (complexity score present)
- ✓ Wave execution created files
- ✓ Serena has project entity
- ✓ Files: app.py, models.py, auth.py exist
- ✓ Code compiles

**Evidence**: Directory listing, Serena entities

---

### Test 2: Existing Project - First Time

**Setup**:
\`\`\`bash
cd /tmp/existing-django
# Has: manage.py, settings.py, models.py
\`\`\`

**Execute**:
\`\`\`
@skill intelligent-do
Task: add API endpoint for user profile
\`\`\`

**Validate**:
- ✓ Explored project (read manage.py, settings.py)
- ✓ Detected tech stack: Python/Django
- ✓ Created Serena entity with tech_stack
- ✓ No spec analysis (simple task)
- ✓ Files created in correct locations (views.py, serializers.py)

**Evidence**: Serena search results, files created

---

### Test 3: Returning - Cached Context

**Setup**:
\`\`\`bash
cd /tmp/existing-django  # Already has Serena entity
\`\`\`

**Execute**:
\`\`\`
@skill intelligent-do
Task: add password reset endpoint
\`\`\`

**Validate**:
- ✓ Loaded from Serena (< 1s)
- ✓ No exploration (used cache)
- ✓ Fast execution (< 3 min vs 5-8 min first time)
- ✓ Files created
- ✓ Serena execution entity linked to project

**Evidence**: Timing logs, Serena graph

---

### Test 4: Research Integration

**Setup**:
\`\`\`bash
cd /tmp/react-app  # Has Serena entity
\`\`\`

**Execute**:
\`\`\`
@skill intelligent-do
Task: integrate Stripe subscription billing
\`\`\`

**Validate**:
- ✓ Detected "Stripe" not in dependencies
- ✓ Ran research (Tavily + Context7)
- ✓ Saved research entities to Serena
- ✓ Executed with research context
- ✓ Files include Stripe integration patterns

**Evidence**: Serena research entities, code quality
```

**Validation**: All test cases documented

---

### Task 4.2: Create Sub-Agent Test

**File**: skills/intelligent-do/tests/test_with_sub_agents.md

**Purpose**: Test that intelligent-do works when spawned as sub-agent

**Test**:
```markdown
### Sub-Agent Spawn Test

**Use Case**: Wave coordinator spawns intelligent-do as sub-agent

**Setup**:
\`\`\`
# Parent: WAVE_COORDINATOR
# Task: "Create microservices: auth-service, user-service, billing-service"
\`\`\`

**Expected**:
- Coordinator spawns 3 agents in parallel
- Each agent runs intelligent-do for its service
- All share parent context (Serena entities)
- No conflicts in Serena writes

**Validate**:
- ✓ 3 project entities created (auth_service, user_service, billing_service)
- ✓ Each has own context
- ✓ Parent wave_execution links to all 3
- ✓ All services created successfully

**Evidence**: Serena graph showing relations
```

**Validation**: Sub-agent compatibility proven

---

## Phase 5: Shannon CLI Integration

**Duration**: 1-2 hours
**Location**: shannon-cli/src/shannon/unified_orchestrator.py
**Goal**: Use new intelligent-do skill from CLI

### Task 5.1: Update _execute_with_context()

**File**: src/shannon/unified_orchestrator.py

**Change**:
```python
async def _execute_with_context(
    self,
    task: str,
    context: Dict,  # This is now redundant - skill loads from Serena
    validation_gates: Dict[str, str],  # Also redundant
    dashboard_client: Optional[Any]
) -> Dict[str, Any]:
    """Execute task via intelligent-do skill.

    NOTE: Skill now handles context loading from Serena.
    CLI-side context is for V3 features only (cache, analytics).
    """

    # Simplified prompt - skill handles intelligence
    prompt = f"Task: {task}"

    # V3: Model selection (keep this)
    model = 'sonnet'
    if self.model_selector and self.budget_enforcer:
        try:
            complexity = len(task) / 100
            selection = self.model_selector.select_optimal_model(
                agent_complexity=complexity,
                context_size_tokens=len(prompt) / 4,
                budget_remaining=self.budget_enforcer.get_status().remaining
            )
            model = selection.model
        except Exception as e:
            logger.warning(f"Model selection failed: {e}")

    # Execute via intelligent-do skill (handles everything)
    logger.info("Executing via intelligent-do skill")
    messages = []

    async for msg in self.sdk_client.invoke_skill(
        skill_name='intelligent-do',
        prompt_content=prompt
    ):
        messages.append(msg)
        if dashboard_client:
            await self._stream_message_to_dashboard(msg, dashboard_client)

    return self._parse_task_result(messages)
```

**Validation**: Compiles, test with shannon do

---

### Task 5.2: Simplify Workflows (Skill Handles Intelligence Now)

**Option**: Can now remove _first_time_workflow, _returning_workflow

**Rationale**:
- Skill handles context detection
- Skill loads from Serena
- CLI only needs V3 wrappers

**Decision**: Keep workflows for now (backward compatibility), refactor later

---

## Phase 6: Complete Validation

**Duration**: 4-6 hours
**Goal**: Prove everything works end-to-end

### Task 6.1: Validate Shannon Framework Skill Standalone

**Test**:
```bash
cd /tmp/test-intelligent-do-skill
# In Claude Code session with Shannon Framework loaded
@skill intelligent-do
Task: create calculator.py with add, subtract, multiply, divide
```

**Validate**:
- ✓ Serena entities created
- ✓ Files created
- ✓ Can run second time, uses cache

---

### Task 6.2: Validate Shannon CLI Integration

**Test**:
```bash
cd /tmp/test-shannon-cli-do
shannon do "create Flask REST API with CRUD" --auto
```

**Validate**:
- ✓ Invokes intelligent-do skill
- ✓ V3 features work (cache, analytics)
- ✓ Dashboard streaming works
- ✓ Files created

---

### Task 6.3: Validate Research Integration

**Test**:
```bash
cd /tmp/test-research
shannon do "integrate Stripe payments" --auto
```

**Validate**:
- ✓ Detects Stripe is external
- ✓ Runs research (Tavily + Context7)
- ✓ Saves research to Serena
- ✓ Implementation uses research

---

### Task 6.4: Complex Application Test (10-15 min)

**Test**:
```bash
shannon do "create e-commerce platform with:
- User authentication
- Product catalog with search
- Shopping cart
- Stripe checkout
- Admin dashboard
- PostgreSQL database
- REST API
- React frontend" --auto
```

**Validate**:
- ✓ Runs spec-analysis (high complexity)
- ✓ Researches Stripe, PostgreSQL
- ✓ Creates comprehensive phase plan
- ✓ Executes waves in parallel
- ✓ All components created
- ✓ WAIT FULL 10-15 MINUTES
- ✓ Collect evidence: directory structure, Serena graph

---

## Implementation Timeline

### Total: 13-20 hours

**Phase 1: Framework Exploration** (2-3h)
- Task 1.1: Serena patterns (1h)
- Task 1.2: Skill orchestration (1h)
- Task 1.3: Research integration (30min)
- Task 1.4: Command definitions (30min)

**Phase 2: Skill Design** (3-4h)
- Task 2.1: Decision tree (30min)
- Task 2.2: Serena model (30min)
- Task 2.3: Frontmatter (15min)
- Task 2.4: Entry & context check (30min)
- Task 2.5: First-time workflow (1h)
- Task 2.6: Returning workflow (1h)
- Task 2.7: Research logic (30min)
- Task 2.8: Examples (15min)

**Phase 3: Command Creation** (1-2h)
- Task 3.1: Write do.md (1-2h)

**Phase 4: Testing Infrastructure** (2-3h)
- Task 4.1: Functional tests (1.5h)
- Task 4.2: Sub-agent test (1h)

**Phase 5: CLI Integration** (1-2h)
- Task 5.1: Update orchestrator (30min)
- Task 5.2: Refactor (optional) (1h)

**Phase 6: Validation** (4-6h)
- Task 6.1: Skill standalone (1h)
- Task 6.2: CLI integration (1h)
- Task 6.3: Research test (1h)
- Task 6.4: Complex app (2-3h including wait time)

---

## Success Criteria

### Shannon Framework:
- ✅ intelligent-do skill created (SKILL.md complete)
- ✅ /shannon:do command created (do.md complete)
- ✅ Serena MCP integration working
- ✅ Research auto-detection working
- ✅ All workflows tested standalone

### Shannon CLI:
- ✅ shannon do uses intelligent-do skill
- ✅ V3 features still work (cache, analytics, cost)
- ✅ Dashboard streaming works
- ✅ All functional tests pass

### Evidence Required:
- ✅ Serena graph showing project entities
- ✅ Research entities linked to projects
- ✅ Execution entities tracking all runs
- ✅ Complex application fully built
- ✅ Screenshots of working apps
- ✅ Test logs showing all passes

---

## File Locations

**Shannon Framework** (/Users/nick/Desktop/shannon-framework/):
- skills/intelligent-do/SKILL.md (NEW)
- skills/intelligent-do/examples/ (NEW)
- skills/intelligent-do/tests/ (NEW)
- commands/do.md (NEW)

**Shannon CLI** (/Users/nick/Desktop/shannon-cli/):
- src/shannon/unified_orchestrator.py (MODIFY)
- tests/functional/test_intelligent_do_*.sh (NEW)

**Documentation**:
- SERENA_PATTERNS.md (NEW - Phase 1)
- INTELLIGENT_DO_DECISION_TREE.md (NEW - Phase 2)
- SERENA_ENTITY_MODEL.md (NEW - Phase 2)

---

## Dependencies

**Required**:
- Serena MCP: CRITICAL - backend for all context
- Shannon Framework v5.1.0+
- Shannon CLI v5.0.0+

**Recommended**:
- Sequential MCP: Deep analysis
- Tavily MCP: Research
- Context7 MCP: Library docs

**Optional**:
- Playwright/Puppeteer: Browser testing
- xcode-mcp: iOS testing

---

## Risks & Mitigation

### Risk 1: Serena MCP Unavailable
**Impact**: Cannot store/load context
**Mitigation**:
- Check at startup, fail fast with clear error
- Document Serena setup in skill
- Fallback: Local JSON (degraded mode)

### Risk 2: Research Overwhelming
**Impact**: Every task triggers research, slow execution
**Mitigation**:
- Conservative detection (only obvious external deps)
- Cache research results in Serena
- Skip research if already researched

### Risk 3: Skill Complexity
**Impact**: Hard to maintain, debug
**Mitigation**:
- Clear decision tree documentation
- Extensive examples
- Each workflow step tested independently

---

## Testing Strategy

### Functional Tests (NO MOCKS):
1. **Unit Level**: Each workflow tested separately
2. **Integration**: Skill + Serena + wave execution
3. **End-to-End**: Shannon CLI → Skill → Files created
4. **Sub-Agent**: Spawned from WAVE_COORDINATOR
5. **Stress**: Complex application (10-15 min execution)

### Evidence Collection:
- Serena graph exports (JSON)
- Directory listings (before/after)
- Execution logs (full output)
- Screenshots (working apps)
- Performance metrics (timing)

---

## Next Steps After Plan Approval

1. Execute Phase 1 (exploration) - understand everything first
2. Execute Phase 2 (skill design) - build comprehensive skill
3. Execute Phase 3 (command) - create /shannon:do
4. Execute Phase 4 (tests) - validate skill works
5. Execute Phase 5 (CLI) - integrate with shannon do
6. Execute Phase 6 (validation) - prove everything works
7. Collect evidence
8. Update documentation
9. Tag releases (Framework v5.2.0, CLI v5.1.0)

**No shortcuts. Build it right. Validate everything. Evidence required.**

---

**Plan Complete**: Ready for execution after approval
