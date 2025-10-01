# Test Case: PreCompact Hook Memory Optimization

**Test ID**: TC-005
**Priority**: High
**Category**: Performance/Memory Management
**Estimated Time**: 15 minutes

## Objective

Validate that Shannon's PreCompact hook correctly optimizes context before token-intensive operations, manages memory efficiently, and maintains quality while reducing token usage.

## Prerequisites

- [ ] Shannon project loaded in Claude Code
- [ ] Serena MCP configured and functional
- [ ] Large project or substantial context
- [ ] Test environment: /Users/nick/Documents/shannon

## Test Steps

### Step 1: Setup Large Context Test Environment

```bash
# Create project with substantial context
cd /Users/nick/Documents/shannon
mkdir -p test-precompact/{src,docs,tests,config}
mkdir -p test-results/TC-005/{artifacts,screenshots,logs,metrics}

# Create multiple files to build up context
for i in {1..10}; do
  cat > test-precompact/src/module_${i}.py << EOF
"""Module ${i} - Sample code for context testing."""
import logging
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)

class DataProcessor${i}:
    """Process data for module ${i}."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize processor with configuration."""
        self.config = config
        self.cache: Dict[str, Any] = {}
        logger.info("DataProcessor${i} initialized")

    def process_data(self, data: List[Dict]) -> List[Dict]:
        """Process input data and return results."""
        logger.info(f"Processing {len(data)} items")
        results = []
        for item in data:
            processed = self._transform_item(item)
            if processed:
                results.append(processed)
        logger.info(f"Processed {len(results)} items successfully")
        return results

    def _transform_item(self, item: Dict) -> Optional[Dict]:
        """Transform a single item."""
        if not self._validate_item(item):
            logger.warning(f"Invalid item: {item}")
            return None

        try:
            transformed = {
                "id": item.get("id"),
                "value": item.get("value", 0) * 2,
                "metadata": self._enrich_metadata(item)
            }
            return transformed
        except Exception as e:
            logger.error(f"Transform error: {str(e)}")
            return None

    def _validate_item(self, item: Dict) -> bool:
        """Validate item structure."""
        required_fields = ["id", "value"]
        return all(field in item for field in required_fields)

    def _enrich_metadata(self, item: Dict) -> Dict:
        """Enrich item metadata."""
        return {
            "timestamp": "2025-09-30T12:00:00Z",
            "processor": "DataProcessor${i}",
            "version": "1.0.0"
        }

    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            "size": len(self.cache),
            "hits": getattr(self, "_cache_hits", 0),
            "misses": getattr(self, "_cache_misses", 0)
        }
EOF
done

# Create documentation files
cat > test-precompact/docs/architecture.md << 'EOF'
# System Architecture

## Overview
This system processes data through multiple modules using a pipeline architecture.

## Components
- Module 1-10: Data processing modules
- Each module handles specific transformation logic
- Shared configuration and caching layer

## Data Flow
1. Input validation
2. Transformation pipeline
3. Metadata enrichment
4. Output generation

## Performance Considerations
- Caching reduces redundant processing
- Logging for observability
- Error handling for resilience
EOF

# Create config files
cat > test-precompact/config/settings.yaml << 'EOF'
app:
  name: "Test PreCompact Application"
  version: "1.0.0"
  environment: "test"

processing:
  batch_size: 100
  timeout: 30
  retry_attempts: 3

logging:
  level: "INFO"
  format: "json"
  output: "stdout"
EOF
```

**Expected**: Large project structure created with substantial context

### Step 2: Load Project and Build Context

**Commands**:
```
# Load project to build up context
/sh:load test-precompact/

# Analyze to increase context usage
/sh:analyze test-precompact/src/

# Read documentation to add more context
# (Internally: Read docs/architecture.md)
```

**Expected Behavior**:
- Project loaded successfully
- All 10 modules indexed
- Documentation read and understood
- Context usage increases to 40-60%

**Context State Validation**:
- [ ] Project structure understood
- [ ] All modules indexed by Serena
- [ ] Documentation context loaded
- [ ] Ready for token-intensive operation

### Step 3: Monitor Pre-Hook Context State

**Before executing token-intensive command, note baseline**:

```
# Estimate current context usage
# (Claude Code provides this in UI)

Expected baseline:
- Context usage: 40-60%
- Token count: ~8000-12000 tokens
- Memory entries: 10+ modules + docs
```

**Baseline Metrics**:
- [ ] Context usage percentage: _____ %
- [ ] Estimated token count: _____ tokens
- [ ] Memory entries: _____ count
- [ ] File count in context: _____ files

### Step 4: Execute Token-Intensive Command (Triggers PreCompact)

**Command**:
```
/sh:implement "Add comprehensive error handling, retry logic with exponential backoff, circuit breaker pattern, and detailed logging to all 10 modules"
```

**Expected Behavior**:
- PreCompact hook detects high token requirement
- Context optimization initiated automatically
- Optimization strategies applied
- Command proceeds with optimized context

**PreCompact Activation Detection**:
- [ ] No explicit "PreCompact activated" message (silent optimization)
- [ ] Command executes faster than expected
- [ ] Response quality maintained
- [ ] No context overflow errors

### Step 5: Validate PreCompact Optimization Strategies

**Strategy 1: Symbol-Enhanced Communication (--uc mode)**

**Expected Optimizations**:
- [ ] Symbols used in output (→, ✅, 🔍, etc.)
- [ ] Abbreviated terms (cfg, impl, perf, etc.)
- [ ] Concise explanations without verbosity
- [ ] 30-50% token reduction in communication

**Sample Optimized Output**:
```
Implementing enhancements across 10 modules:

Wave 1: Error Handling
→ auth/user_auth.py: try-except blocks ✅
→ api/endpoints.py: custom exceptions ✅
...

Wave 2: Retry Logic
→ exponential backoff impl ✅
→ max_retries cfg: 3 ✅
```

**Strategy 2: Selective Context Retention**

**Expected Behaviors**:
- [ ] Core module information retained
- [ ] Detailed documentation summarized
- [ ] Redundant file content deduplicated
- [ ] Focus on task-relevant context

**Strategy 3: MCP Query Optimization**

**Expected Behaviors**:
- [ ] Serena queries batched when possible
- [ ] Context7 queries targeted and specific
- [ ] Reduced round-trips to MCP servers
- [ ] Cached results reused

### Step 6: Validate Post-Hook Context State

**After PreCompact optimization**:

```
Expected post-optimization:
- Context usage: 50-70% (increased but optimized)
- Token count: ~10000-14000 (less than without optimization)
- Memory entries: Still accessible
- Quality: Maintained
```

**Post-Optimization Metrics**:
- [ ] Context usage percentage: _____ %
- [ ] Estimated token count: _____ tokens
- [ ] Memory entries still accessible: _____ (Y/N)
- [ ] Quality maintained: _____ (Y/N)

### Step 7: Validate Implementation Quality

**Quality Checklist (Despite Optimization)**:

**Completeness**:
- [ ] Error handling added to all 10 modules
- [ ] Retry logic implemented (not mocked)
- [ ] Circuit breaker pattern implemented
- [ ] Logging enhanced throughout
- [ ] NO placeholder implementations

**Code Quality**:
```bash
# Check implementations
grep -r "try:\|except" test-precompact/src/ | wc -l  # Should be substantial
grep -r "retry\|exponential" test-precompact/src/ | wc -l  # Should have retry logic
grep -r "circuit.*breaker\|CircuitBreaker" test-precompact/src/ | wc -l  # Should have pattern
```

**Expected Implementations**:
- [ ] Try-except blocks in critical sections
- [ ] Retry decorators or functions
- [ ] Circuit breaker class or utility
- [ ] Enhanced logging statements
- [ ] Real implementations, not TODOs

### Step 8: Validate Memory Access Post-Optimization

**Memory Integrity Validation**:

```
# Query Serena for module information
# Should still return accurate results despite optimization

Query: "What does DataProcessor3 do?"
Expected: Accurate description despite context optimization
```

**Memory Checklist**:
- [ ] Module information still accessible
- [ ] Function signatures retrievable
- [ ] Documentation still queryable
- [ ] Context relationships maintained
- [ ] No information loss

### Step 9: Compare With and Without PreCompact

**Scenario A: With PreCompact (Current Test)**

Metrics:
- Context usage: _____ %
- Response time: _____ seconds
- Token efficiency: _____ (estimated)
- Quality score: _____ /10

**Scenario B: Simulated Without PreCompact**

```
# Disable PreCompact (if flag available)
/sh:implement "..." --no-precompact

Expected without optimization:
- Context usage: 70-85% (higher)
- Response time: Slower or overflow
- Token usage: Higher
- Quality: Same (if no overflow)
```

**Comparative Metrics**:
- [ ] Token savings: _____ % reduction
- [ ] Context usage savings: _____ % lower
- [ ] Quality maintained: _____ (Y/N)
- [ ] Performance gain: _____ seconds faster

### Step 10: Validate PreCompact Hook Artifacts

**Hook Execution Metadata**:

```bash
# Check for PreCompact artifacts
ls -la .shannon/hooks/precompact/

# Check metrics
cat .shannon/hooks/precompact/metrics_*.json
```

**Expected Artifacts**:
- [ ] .shannon/hooks/precompact/ directory exists
- [ ] Metrics file created: metrics_TIMESTAMP.json
- [ ] Metrics include:
  - [ ] Optimization strategies applied
  - [ ] Token reduction achieved
  - [ ] Context compression ratio
  - [ ] Execution time
  - [ ] Quality score maintained

**Sample Metrics JSON**:
```json
{
  "hook": "PreCompact",
  "timestamp": "2025-09-30T14:30:22Z",
  "trigger": "high_token_operation",
  "context_before": {
    "usage_percent": 55,
    "estimated_tokens": 11000
  },
  "optimizations": [
    {
      "strategy": "symbol_communication",
      "token_reduction": 2200,
      "reduction_percent": 20
    },
    {
      "strategy": "selective_retention",
      "token_reduction": 1650,
      "reduction_percent": 15
    },
    {
      "strategy": "mcp_query_optimization",
      "token_reduction": 550,
      "reduction_percent": 5
    }
  ],
  "context_after": {
    "usage_percent": 62,
    "estimated_tokens": 12500
  },
  "performance": {
    "optimization_time_ms": 150,
    "total_execution_time_s": 45
  },
  "quality": {
    "maintained": true,
    "score": 9.2
  }
}
```

### Step 11: Validate Adaptive Threshold Behavior

**Test Different Context Levels**:

**Low Context (20-40%)**:
```
# With low context, PreCompact may not activate
Expected: Normal execution without optimization
```

**Medium Context (40-60%)**:
```
# Medium context triggers light optimization
Expected: Selective optimizations applied
```

**High Context (60-80%)**:
```
# High context triggers aggressive optimization
Expected: All optimization strategies applied
```

**Critical Context (80-95%)**:
```
# Critical level triggers maximum optimization
Expected: Emergency compression, force --uc mode
```

**Threshold Validation**:
- [ ] No optimization at low context levels
- [ ] Proportional optimization at medium levels
- [ ] Aggressive optimization at high levels
- [ ] Emergency protocols at critical levels

### Step 12: Validate Quality Preservation

**Quality Metrics**:

**Implementation Completeness**:
- [ ] All requested features implemented
- [ ] NO mocks or placeholders
- [ ] Error handling comprehensive
- [ ] Retry logic functional
- [ ] Circuit breaker operational

**Code Quality**:
- [ ] Professional code standards maintained
- [ ] Type hints preserved
- [ ] Documentation adequate
- [ ] Logging appropriate
- [ ] Error messages clear

**Functional Correctness**:
```bash
# Run syntax checks
python -m py_compile test-precompact/src/module_*.py

# Expected: All files compile without syntax errors
```

**Quality Validation**:
- [ ] Syntax valid (all files compile)
- [ ] Logic complete (not stubbed)
- [ ] Patterns correct (retry, circuit breaker)
- [ ] Integration works (modules still compatible)

## Expected Results

**Successful PreCompact Hook Execution**:

1. **Automatic Activation**: Hook triggered by high token requirement
2. **Optimization Applied**: Context compressed 30-50%
3. **Quality Maintained**: Implementation complete and correct
4. **Performance Gain**: Faster execution, no overflow
5. **Artifacts Generated**: Metrics and logs created
6. **Memory Intact**: Serena context still accessible
7. **Adaptive Behavior**: Optimization level matches context state

## Validation Criteria

**Pass Criteria**:
- ✅ PreCompact hook activated automatically
- ✅ Token reduction: 30-50%
- ✅ Context usage optimized (no overflow)
- ✅ Quality maintained (>90% score)
- ✅ Implementation complete (NO MOCKS)
- ✅ Memory access preserved
- ✅ Metrics artifacts generated
- ✅ Adaptive thresholds working

**Fail Criteria**:
- ❌ Context overflow despite optimization
- ❌ Quality degradation (mocks, incomplete code)
- ❌ Memory corruption or loss
- ❌ Hook not activated when needed
- ❌ No measurable token reduction
- ❌ Artifacts not generated

## Debug Information

**Logs to Collect**:
- [ ] Copy implementation output: test-results/TC-005/implement_output.md
- [ ] Copy all modified files: test-results/TC-005/artifacts/
- [ ] Copy PreCompact metrics: test-results/TC-005/metrics/metrics_*.json
- [ ] Copy context snapshots: test-results/TC-005/context_*.json
- [ ] Screenshots: test-results/TC-005/screenshots/

**Debug Commands**:
```bash
# Check PreCompact artifacts
ls -la .shannon/hooks/precompact/
cat .shannon/hooks/precompact/metrics_*.json | jq .

# Verify implementations complete
grep -r "TODO\|FIXME\|mock\|placeholder" test-precompact/src/

# Count error handling additions
grep -r "try:\|except" test-precompact/src/ | wc -l

# Check circuit breaker implementation
grep -r "circuit.*breaker\|CircuitBreaker" test-precompact/src/

# Validate retry logic
grep -r "@retry\|def.*retry\|exponential" test-precompact/src/

# Test syntax
for f in test-precompact/src/*.py; do python -m py_compile "$f" || echo "Error in $f"; done
```

## Notes

**Record Observations**:
- PreCompact activated: _____ (Y/N)
- Context usage before: _____ %
- Context usage after: _____ %
- Token reduction: _____ %
- Optimization strategies used: _____
- Quality score: _____ /10
- Memory access working: _____ (Y/N)
- Execution time: _____ seconds
- Artifacts generated: _____ (Y/N)

**Known Issues**:
- None at test creation time

**Edge Cases to Test**:
1. PreCompact at critical threshold (95%+ context)
2. Multiple PreCompact activations in session
3. PreCompact with all MCP servers active
4. PreCompact failure and recovery
5. PreCompact with wave orchestration
