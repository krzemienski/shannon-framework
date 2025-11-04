# Example: Querying Wave History

**Scenario**: User asks "Show me all waves for the current project and their status"

**Context**: Project has 3 completed waves and 1 in-progress wave stored in Serena MCP

---

## Without Memory Coordination Skill

**Agent Behavior**:
```
Agent: "Let me check the wave history..."

[Attempts read_graph() - loads entire knowledge graph]
[Manually filters for entities with "wave" in name]
[Inconsistent naming: finds "wave1", "Wave_2", "waveThree", "current_wave"]
[No timestamp information, no status]
[Missing relations - can't determine order]

Agent: "I found 4 wave-related entities but cannot determine their order or status reliably."
```

**Problems**:
- ❌ read_graph() loaded 500+ entities (inefficient)
- ❌ Inconsistent naming prevented reliable filtering
- ❌ No timestamps or status information
- ❌ Cannot determine wave order or progression
- ❌ Wasted 2000+ tokens loading irrelevant entities

---

## With Memory Coordination Skill

**Agent Behavior**:
```
Agent: "Using memory-coordination protocol to query wave history..."

Step 1: Map query to search pattern
  Intent: "All waves"
  Protocol: search_nodes("shannon/waves/")

Step 2: Execute targeted search
  search_nodes("shannon/waves/")

  Returns (4 entities):
  - shannon/waves/wave_20250103_140000
  - shannon/waves/wave_20250103_160000
  - shannon/waves/wave_20250104_090000
  - shannon/waves/wave_20250104_113000

Step 3: Fetch wave details
  open_nodes([
    "shannon/waves/wave_20250103_140000",
    "shannon/waves/wave_20250103_160000",
    "shannon/waves/wave_20250104_090000",
    "shannon/waves/wave_20250104_113000"
  ])

Step 4: Parse observations
  Wave 1 (shannon/waves/wave_20250103_140000):
    - created: 2025-01-03T14:00:00Z
    - wave_number: 1
    - phase: Phase 2 - Architecture & Design
    - status: complete
    - agents: 8
    - duration: 2h 15m
    - deliverables: Architecture diagrams, API specs, DB schemas
    - validation_gate: ✅ Design approved

  Wave 2 (shannon/waves/wave_20250103_160000):
    - created: 2025-01-03T16:00:00Z
    - wave_number: 2
    - phase: Phase 3 - Implementation (Frontend)
    - status: complete
    - agents: 5
    - duration: 3h 45m
    - deliverables: React components, routing, state management
    - validation_gate: ✅ Functional tests passing

  Wave 3 (shannon/waves/wave_20250104_090000):
    - created: 2025-01-04T09:00:00Z
    - wave_number: 3
    - phase: Phase 3 - Implementation (Backend)
    - status: complete
    - agents: 6
    - duration: 4h 20m
    - deliverables: API endpoints, auth, middleware
    - validation_gate: ✅ API tests passing

  Wave 4 (shannon/waves/wave_20250104_113000):
    - created: 2025-01-04T11:30:00Z
    - wave_number: 4
    - phase: Phase 4 - Integration & Testing
    - status: in_progress
    - agents: 8
    - current_progress: 60%
    - estimated_completion: 2025-01-04T16:00:00Z

Step 5: Format output
```

**Agent Response**:
```
# Wave History for Project

## Completed Waves (3)

### Wave 1: Phase 2 - Architecture & Design ✅
- **Started**: 2025-01-03 14:00
- **Duration**: 2h 15m
- **Agents**: 8
- **Status**: COMPLETE
- **Deliverables**: Architecture diagrams, API specs, DB schemas
- **Validation**: ✅ Design approved, patterns established

### Wave 2: Phase 3 - Implementation (Frontend) ✅
- **Started**: 2025-01-03 16:00
- **Duration**: 3h 45m
- **Agents**: 5
- **Status**: COMPLETE
- **Deliverables**: React components, routing, state management
- **Validation**: ✅ Functional tests passing (Puppeteer)

### Wave 3: Phase 3 - Implementation (Backend) ✅
- **Started**: 2025-01-04 09:00
- **Duration**: 4h 20m
- **Agents**: 6
- **Status**: COMPLETE
- **Deliverables**: API endpoints, authentication, middleware
- **Validation**: ✅ API tests passing (real HTTP)

## Active Waves (1)

### Wave 4: Phase 4 - Integration & Testing 🔄
- **Started**: 2025-01-04 11:30
- **Duration**: ~4h 30m (estimated)
- **Agents**: 8
- **Status**: IN PROGRESS (60% complete)
- **Current Focus**: Frontend-backend integration, E2E testing
- **Estimated Completion**: 2025-01-04 16:00

## Summary
- **Total Waves**: 4
- **Completed**: 3 (75%)
- **In Progress**: 1 (25%)
- **Total Time**: 10h 20m (completed) + ~1h 50m (active)
- **Phase Progress**: Phase 2 ✅, Phase 3 ✅, Phase 4 🔄
```

**Benefits**:
- ✅ Efficient query (search_nodes with namespace prefix)
- ✅ Complete information (timestamps, status, deliverables)
- ✅ Clear progression (wave order, phase tracking)
- ✅ Validation status visible (gates passed/pending)
- ✅ Minimal tokens (~200 vs 2000+ without skill)

---

## Protocol Applied

**Memory Coordination Protocols Used**:

1. **Namespace Search**: `search_nodes("shannon/waves/")` instead of `read_graph()`
   - Targeted query (only waves)
   - Fast execution (<1 second)
   - Token efficient (200 tokens vs 2000+)

2. **Standardized Entity Naming**: `shannon/waves/wave_[timestamp]`
   - Consistent format enables reliable sorting
   - Timestamp in name provides chronological order
   - No ambiguity (all waves follow same pattern)

3. **Structured Observations**: All waves have consistent observation format
   - type, created, wave_number, phase, status, agents, duration, deliverables, validation_gate
   - Enables programmatic parsing
   - Complete context without missing information

4. **Relations Preserved**: Can query wave -> spec relation if needed
   - `open_nodes(["shannon/waves/wave_20250103_140000"])` includes relation to parent spec
   - Enables "show me the spec that spawned Wave 1" queries
   - Context lineage intact

---

## Comparison

| Metric | Without Skill | With Skill |
|--------|---------------|------------|
| Query Method | read_graph() | search_nodes("shannon/waves/") |
| Entities Loaded | 500+ | 4 |
| Tokens Used | ~2000 | ~200 |
| Query Time | 3-5 seconds | <1 second |
| Data Completeness | Inconsistent | Complete |
| Ordering | Manual/broken | Timestamp-based |
| Success Rate | 60% | 100% |

---

## Code Example

**With Memory Coordination Skill**:
```javascript
// Step 1: Query all waves
const waves = await search_nodes("shannon/waves/");

// Step 2: Get detailed information
const waveDetails = await open_nodes(waves.map(w => w.name));

// Step 3: Parse and format
const waveHistory = waveDetails.map(wave => {
  const obs = parseObservations(wave.observations);
  return {
    name: wave.name,
    waveNumber: obs.wave_number,
    created: obs.created,
    phase: obs.phase,
    status: obs.status,
    agents: obs.agents,
    duration: obs.duration,
    deliverables: obs.deliverables,
    validationGate: obs.validation_gate
  };
});

// Step 4: Sort by wave number
waveHistory.sort((a, b) => a.waveNumber - b.waveNumber);

// Step 5: Format output
return formatWaveHistory(waveHistory);
```

**Result**: Complete, accurate wave history in <1 second

---

## Validation

**Verify Memory Coordination Applied**:
- ✅ Used search_nodes("shannon/waves/") not read_graph()
- ✅ All entities have shannon/waves/ prefix
- ✅ Entity names follow standard format (wave_[timestamp])
- ✅ Observations structured with timestamps
- ✅ Can trace wave -> spec relations if needed
- ✅ Query executed efficiently (<200 tokens)
- ✅ No manual filtering required (namespace prefix did the work)

**Result**: Memory Coordination Protocol successfully applied ✅
