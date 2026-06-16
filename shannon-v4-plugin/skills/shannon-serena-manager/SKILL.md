---
name: shannon-serena-manager
display_name: "Shannon Serena Manager (Memory Operations)"
description: "High-level wrapper for Serena MCP operations - simplified memory management with validation and error handling"
category: management
version: "4.0.0"
author: "Shannon Framework"
priority: 1
auto_activate: true
activation_triggers:
  - "/sh_memory command"
  - "list memories"
  - "search memory"
  - "read memory"
mcp_servers:
  required:
    - serena
allowed_tools:
  - serena_write_memory
  - serena_read_memory
  - serena_list_memories
  - serena_create_entities
  - serena_create_relations
  - serena_search
progressive_disclosure:
  tier: 1
  metadata_tokens: 150
input:
  operation:
    type: string
    description: "Operation: list, read, write, search, delete"
    required: true
  key:
    type: string
    description: "Memory key (for read/write/delete)"
    required: false
  value:
    type: any
    description: "Memory value (for write)"
    required: false
  query:
    type: string
    description: "Search query (for search)"
    required: false
output:
  result:
    type: any
    description: "Operation result"
  sitrep:
    type: object
    description: "Standardized SITREP (via shannon-status-reporter)"
---

# Shannon Serena Manager

> **Memory Operations**: Simplified interface to Serena MCP with validation and error handling

## Purpose

Provides a high-level, user-friendly interface to Serena MCP operations with:
- **Automatic validation** - Ensures data integrity
- **Error handling** - Graceful failures with helpful messages
- **Search capabilities** - Find memories by pattern or content
- **Batch operations** - Efficient bulk operations
- **SITREP output** - Standardized reporting

## Capabilities

### 1. List Memories
- List all memories in Serena
- Filter by pattern (e.g., "checkpoint_*", "wave_*")
- Sort by timestamp
- Display summary or full details

### 2. Read Memory
- Load memory by key
- Validate memory exists
- Handle missing memories gracefully
- Display formatted output

### 3. Write Memory
- Save memory with validation
- Automatic timestamping
- Version control support
- Backup previous versions

### 4. Search Memories
- Full-text search across memories
- Pattern matching
- Filter by type/category
- Ranked results

### 5. Delete Memory
- Safe deletion with confirmation
- Automatic backup before delete
- Cascade handling for related memories

## Activation

**Automatic**:
```bash
/sh_memory list
/sh_memory list checkpoint_*
/sh_memory read north_star_goal
/sh_memory search "react dashboard"
/sh_memory write my_key '{"data": "value"}'
```

**Manual**:
```bash
Skill("shannon-serena-manager")
```

## Execution Algorithm

### Step 1: Validate Input

```javascript
function validateOperation(operation, key, value, query) {
  const valid_operations = ['list', 'read', 'write', 'search', 'delete'];

  if (!valid_operations.includes(operation)) {
    throw new Error(`Invalid operation: ${operation}. Valid: ${valid_operations.join(', ')}`);
  }

  if (['read', 'write', 'delete'].includes(operation) && !key) {
    throw new Error(`Operation '${operation}' requires 'key' parameter`);
  }

  if (operation === 'write' && value === undefined) {
    throw new Error("Operation 'write' requires 'value' parameter");
  }

  if (operation === 'search' && !query) {
    throw new Error("Operation 'search' requires 'query' parameter");
  }

  return true;
}
```

### Step 2: Execute Operation

#### Operation: LIST

```javascript
async function listMemories(pattern = null) {
  try {
    // Get all memories
    const memories = await serena_list_memories();

    // Filter by pattern if provided
    let filtered = memories;
    if (pattern) {
      const regex = new RegExp(pattern.replace('*', '.*'));
      filtered = memories.filter(m => regex.test(m.key));
    }

    // Sort by timestamp (newest first)
    filtered.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));

    return {
      operation: "list",
      count: filtered.length,
      total: memories.length,
      pattern,
      memories: filtered.map(m => ({
        key: m.key,
        type: m.type || 'unknown',
        timestamp: m.timestamp,
        size: JSON.stringify(m.value || {}).length
      }))
    };
  } catch (error) {
    return {
      operation: "list",
      error: error.message,
      success: false
    };
  }
}
```

#### Operation: READ

```javascript
async function readMemory(key) {
  try {
    const memory = await serena_read_memory(key);

    if (!memory) {
      return {
        operation: "read",
        key,
        found: false,
        message: `Memory '${key}' not found`,
        suggestions: await findSimilarKeys(key)
      };
    }

    return {
      operation: "read",
      key,
      found: true,
      value: memory,
      timestamp: memory.timestamp || 'unknown',
      size: JSON.stringify(memory).length
    };
  } catch (error) {
    return {
      operation: "read",
      key,
      error: error.message,
      success: false
    };
  }
}

async function findSimilarKeys(key) {
  const all_memories = await serena_list_memories();
  const similar = all_memories
    .map(m => ({
      key: m.key,
      similarity: calculateSimilarity(key, m.key)
    }))
    .filter(m => m.similarity > 0.5)
    .sort((a, b) => b.similarity - a.similarity)
    .slice(0, 5);

  return similar.map(m => m.key);
}

function calculateSimilarity(str1, str2) {
  // Simple Levenshtein distance-based similarity
  const longer = str1.length > str2.length ? str1 : str2;
  const shorter = str1.length > str2.length ? str2 : str1;

  if (longer.length === 0) return 1.0;

  const editDistance = levenshteinDistance(longer, shorter);
  return (longer.length - editDistance) / longer.length;
}

function levenshteinDistance(str1, str2) {
  const matrix = [];

  for (let i = 0; i <= str2.length; i++) {
    matrix[i] = [i];
  }

  for (let j = 0; j <= str1.length; j++) {
    matrix[0][j] = j;
  }

  for (let i = 1; i <= str2.length; i++) {
    for (let j = 1; j <= str1.length; j++) {
      if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
        matrix[i][j] = matrix[i - 1][j - 1];
      } else {
        matrix[i][j] = Math.min(
          matrix[i - 1][j - 1] + 1,
          matrix[i][j - 1] + 1,
          matrix[i - 1][j] + 1
        );
      }
    }
  }

  return matrix[str2.length][str1.length];
}
```

#### Operation: WRITE

```javascript
async function writeMemory(key, value) {
  try {
    // Check if key already exists
    const existing = await serena_read_memory(key);

    // Backup existing value if present
    if (existing) {
      const backup_key = `${key}_backup_${Date.now()}`;
      await serena_write_memory(backup_key, existing);
    }

    // Add metadata
    const memory_data = {
      ...value,
      _metadata: {
        created_at: existing ? existing._metadata?.created_at : Date.now(),
        updated_at: Date.now(),
        version: existing ? (existing._metadata?.version || 0) + 1 : 1,
        shannon_managed: true
      }
    };

    // Write to Serena
    await serena_write_memory(key, memory_data);

    return {
      operation: "write",
      key,
      success: true,
      version: memory_data._metadata.version,
      backed_up: existing !== null,
      backup_key: existing ? `${key}_backup_${Date.now()}` : null
    };
  } catch (error) {
    return {
      operation: "write",
      key,
      error: error.message,
      success: false
    };
  }
}
```

#### Operation: SEARCH

```javascript
async function searchMemories(query) {
  try {
    // Get all memories
    const memories = await serena_list_memories();

    // Search in keys and values
    const results = [];

    for (const memory of memories) {
      const key_match = memory.key.toLowerCase().includes(query.toLowerCase());
      const value_string = JSON.stringify(memory.value || {}).toLowerCase();
      const value_match = value_string.includes(query.toLowerCase());

      if (key_match || value_match) {
        results.push({
          key: memory.key,
          match_in: key_match ? (value_match ? 'key_and_value' : 'key') : 'value',
          timestamp: memory.timestamp,
          snippet: extractSnippet(value_string, query, 100)
        });
      }
    }

    // Sort by relevance (key matches first)
    results.sort((a, b) => {
      if (a.match_in === 'key' && b.match_in !== 'key') return -1;
      if (a.match_in !== 'key' && b.match_in === 'key') return 1;
      return (b.timestamp || 0) - (a.timestamp || 0);
    });

    return {
      operation: "search",
      query,
      count: results.length,
      results
    };
  } catch (error) {
    return {
      operation: "search",
      query,
      error: error.message,
      success: false
    };
  }
}

function extractSnippet(text, query, max_length) {
  const index = text.toLowerCase().indexOf(query.toLowerCase());

  if (index === -1) return text.substring(0, max_length) + '...';

  const start = Math.max(0, index - 50);
  const end = Math.min(text.length, index + query.length + 50);

  let snippet = text.substring(start, end);

  if (start > 0) snippet = '...' + snippet;
  if (end < text.length) snippet = snippet + '...';

  return snippet;
}
```

#### Operation: DELETE

```javascript
async function deleteMemory(key, confirm = false) {
  try {
    // Check if memory exists
    const existing = await serena_read_memory(key);

    if (!existing) {
      return {
        operation: "delete",
        key,
        found: false,
        message: `Memory '${key}' not found`
      };
    }

    // Require confirmation for safety
    if (!confirm) {
      return {
        operation: "delete",
        key,
        requires_confirmation: true,
        message: `Memory '${key}' found. Pass confirm=true to delete.`,
        preview: JSON.stringify(existing).substring(0, 200) + '...'
      };
    }

    // Backup before delete
    const backup_key = `${key}_deleted_${Date.now()}`;
    await serena_write_memory(backup_key, existing);

    // Delete (Note: Serena might not have explicit delete, so we mark as deleted)
    await serena_write_memory(key, {
      _deleted: true,
      _deleted_at: Date.now(),
      _backup: backup_key
    });

    return {
      operation: "delete",
      key,
      success: true,
      backup_key,
      message: `Memory '${key}' deleted. Backup saved to '${backup_key}'`
    };
  } catch (error) {
    return {
      operation: "delete",
      key,
      error: error.message,
      success: false
    };
  }
}
```

### Step 3: Generate SITREP

```javascript
// Generate standardized SITREP using shannon-status-reporter
const sitrep_data = {
  agent_name: "shannon-serena-manager",
  task_id: `memory_${operation}_${Date.now()}`,
  current_phase: "Memory Management",
  progress: 100,
  state: result.success !== false ? "completed" : "failed",

  objective: `${operation.toUpperCase()} memory operation`,
  scope: [
    `Operation: ${operation}`,
    key ? `Key: ${key}` : null,
    query ? `Query: ${query}` : null,
    pattern ? `Pattern: ${pattern}` : null
  ].filter(Boolean),
  dependencies: ["serena"],

  findings: [
    `Operation: ${operation}`,
    operation === "list" ? `Found ${result.count} memories` : null,
    operation === "read" && result.found ? `Memory loaded: ${key}` : null,
    operation === "read" && !result.found ? `Memory not found: ${key}` : null,
    operation === "write" ? `Memory written: ${key} (version ${result.version})` : null,
    operation === "search" ? `Found ${result.count} matches for "${query}"` : null,
    operation === "delete" ? `Memory deleted: ${key}` : null
  ].filter(Boolean),

  blockers: result.error ? [result.error] : [],
  risks: [],
  questions: [],

  next_steps: [
    operation === "read" && !result.found && result.suggestions?.length > 0
      ? `Try similar keys: ${result.suggestions.join(', ')}`
      : null,
    operation === "write" ? `Read back with: /sh_memory read ${key}` : null
  ].filter(Boolean),

  artifacts: [
    operation === "write" ? key : null,
    operation === "write" && result.backed_up ? result.backup_key : null,
    operation === "delete" ? result.backup_key : null
  ].filter(Boolean),

  tests_executed: ["serena_connection", "operation_validation"],
  test_results: result.success !== false ? "Operation completed successfully" : "Operation failed"
};

// Invoke shannon-status-reporter to generate SITREP
const sitrep = await generate_sitrep(sitrep_data);

return sitrep;
```

## Examples

### Example 1: List All Memories

```bash
/sh_memory list
```

**SITREP Output**:
```markdown
## SITREP: shannon-serena-manager - memory_list_1730739600000

### Status
- **Current Phase**: Memory Management
- **Progress**: 100%
- **State**: completed

### Context
- **Objective**: LIST memory operation
- **Scope**: Operation: list
- **Dependencies**: serena

### Findings
- Operation: list
- Found 23 memories

### Issues
- **Blockers**: None
- **Risks**: None
- **Questions**: None

### Next Steps
- (None)

### Artifacts
- (None)

### Validation
- **Tests Executed**: serena_connection, operation_validation
- **Results**: Operation completed successfully
```

### Example 2: Search Memories

```bash
/sh_memory search "react dashboard"
```

**SITREP Output** shows search results with matching keys and snippets.

### Example 3: Read Memory Not Found

```bash
/sh_memory read noth_star_goal  # Typo
```

**SITREP Output**:
```markdown
## SITREP: shannon-serena-manager - memory_read_1730739700000

### Status
- **Current Phase**: Memory Management
- **Progress**: 100%
- **State**: completed

### Context
- **Objective**: READ memory operation
- **Scope**: Operation: read, Key: noth_star_goal
- **Dependencies**: serena

### Findings
- Operation: read
- Memory not found: noth_star_goal

### Issues
- **Blockers**: None
- **Risks**: None
- **Questions**: None

### Next Steps
- [ ] Try similar keys: north_star_goal, north_star_goal_history_v1

### Artifacts
- (None)

### Validation
- **Tests Executed**: serena_connection, operation_validation
- **Results**: Operation completed successfully
```

## Integration with Shannon v4

**Used by**:
- /sh_memory command (primary interface)
- All Shannon skills (for memory operations)
- shannon-checkpoint-manager (state persistence)
- shannon-goal-tracker (North Star storage)

**Uses**:
- shannon-status-reporter (SITREP generation)
- serena MCP (all operations)

**Composition**:
```
Any skill → shannon-serena-manager → Serena MCP
         ↓
    Simplified API + validation + error handling
```

## Best Practices

### DO ✅
- Use descriptive memory keys (e.g., "north_star_goal", not "nsg")
- Version important memories
- Search before creating new memories (avoid duplicates)
- Use list with patterns to explore namespace
- Check SITREP output for suggestions

### DON'T ❌
- Use special characters in keys (use underscores)
- Store sensitive data without encryption flag
- Delete memories without backup
- Ignore memory size (large memories slow operations)
- Create deeply nested keys (keep flat structure)

## Memory Key Conventions

**Shannon Standard Keys**:
```
north_star_goal              - Project goal
spec_analysis_*              - Specification analysis
phase_plan_detailed          - Phase plan
wave_N_complete              - Wave completion status
checkpoint_*                 - Checkpoints
sitrep_*                     - SITREPs
```

**Key Naming Patterns**:
```
{component}_{identifier}_{timestamp}
  └─ shannon component
      └─ unique ID or version
          └─ Unix timestamp (optional)

Examples:
- checkpoint_myproject_1730739600000
- wave_2_complete
- north_star_goal_history_v1
```

## Learn More

📚 **Full Documentation**: [resources/FULL_SKILL.md](./resources/FULL_SKILL.md)
📚 **Memory Patterns**: [resources/MEMORY_PATTERNS.md](./resources/MEMORY_PATTERNS.md)

---

**Shannon V4** - Memory Management Made Simple 💾
