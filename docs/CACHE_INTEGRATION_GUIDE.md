# Shannon Cache System - Integration Guide

**For**: Wave 2+ Agents integrating with cache system
**Version**: 3.0.0
**Status**: Production-ready

---

## Quick Start

### Basic Usage

```python
from shannon.cache import CacheManager

# Initialize once at application startup
cache_manager = CacheManager()

# Use in your command/feature
def analyze_spec(spec_text: str, context: dict) -> dict:
    # Try cache first
    result = cache_manager.analysis.get(
        spec_text,
        context=context,
        model="sonnet",
        framework_version="3.0.0"
    )

    if result is None:
        # Cache miss - perform expensive operation
        result = perform_actual_analysis(spec_text, context)

        # Save to cache
        cache_manager.analysis.save(
            spec_text,
            result,
            context=context,
            model="sonnet",
            framework_version="3.0.0"
        )

    return result
```

---

## Cache Types

### 1. Analysis Cache

**Use for**: Expensive specification analysis operations

**Features**:
- Context-aware (includes project context in key)
- 7-day TTL
- SHA-256 hashing
- Tracks cost savings

**Integration**:
```python
# In shannon analyze command
result = cache_manager.analysis.get(
    spec_text=specification_content,
    context={
        'project_id': project.id,
        'tech_stack': project.tech_stack,
        'loaded_files': context_manager.loaded_files
    },
    model="sonnet[1m]",
    framework_version="3.0.0"
)

if result is None:
    # Perform analysis via SDK
    result = await analyze_with_sdk(spec_text)
    cache_manager.analysis.save(spec_text, result, context=context)
```

**Key Consideration**: Context MUST be included to avoid stale results when project changes.

---

### 2. Command Cache

**Use for**: Stable command results (prime, discover-skills, check-mcps)

**Features**:
- Version-based keys
- Command-specific TTLs (1-30 days)
- Execution time tracking
- Only caches approved commands

**Integration**:
```python
# In shannon prime command
result = cache_manager.command.get(
    'prime',
    framework_version='3.0.0'
)

if result is None:
    start_time = time.time()
    result = load_initial_instructions()
    execution_time = time.time() - start_time

    cache_manager.command.save(
        'prime',
        result,
        framework_version='3.0.0',
        execution_time=execution_time
    )
```

**Cacheable Commands**:
- `prime` (30-day TTL)
- `discover-skills` (7-day TTL)
- `check-mcps` (1-day TTL)

**Not Cacheable**: Dynamic commands (wave, analyze with args, etc.)

---

### 3. MCP Cache

**Use for**: MCP recommendations based on domain breakdown

**Features**:
- Deterministic signatures
- No TTL (stable mapping)
- Order-independent hashing
- Similarity search

**Integration**:
```python
# In MCP recommendation engine
domain_breakdown = {
    'Backend': 40.0,
    'Frontend': 30.0,
    'Analytics': 20.0,
    'DevOps': 10.0
}

mcps = cache_manager.mcp.get(domain_breakdown)

if mcps is None:
    mcps = compute_mcp_recommendations(domain_breakdown)
    cache_manager.mcp.save(domain_breakdown, mcps)
```

**Advanced**: Find similar cached domains
```python
similar = cache_manager.mcp.find_similar_domains(
    domain_breakdown,
    threshold=0.8  # 80% similarity
)

if similar:
    # Use recommendations from similar domain
    mcps = get_cached_recommendations(similar[0]['signature'])
```

---

## Manager Operations

### Statistics

```python
# Get comprehensive stats
stats = cache_manager.get_stats()

print(f"Hit rate: {stats['overall']['hit_rate_percent']:.1f}%")
print(f"Total savings: ${stats['overall']['total_savings_usd']:.2f}")
print(f"Cache size: {stats['overall']['total_size_mb']:.2f} MB")
```

### Health Monitoring

```python
# Check cache health
health = cache_manager.health_check()

if not health['healthy']:
    log.error(f"Cache issues: {health['issues']}")

if health['warnings']:
    log.warning(f"Cache warnings: {health['warnings']}")
```

### Maintenance

```python
# Clear expired entries (safe - preserves fresh data)
counts = cache_manager.clear_expired()

# LRU eviction (if approaching size limit)
if cache_manager.check_size_limit():
    evicted = cache_manager.evict_lru()

# Full clear (use sparingly)
counts = cache_manager.clear_all()
```

---

## Integration Checklist

For each command/feature using cache:

- [ ] Import `CacheManager` from `shannon.cache`
- [ ] Initialize manager (or use shared instance)
- [ ] Implement cache-first pattern:
  1. Try `cache.get()`
  2. If miss, perform operation
  3. Save with `cache.save()`
- [ ] Include all relevant context in cache key
- [ ] Track execution time for command cache
- [ ] Handle cache misses gracefully
- [ ] Log cache hits/misses for debugging

---

## Best Practices

### 1. Cache Key Stability

**DO**:
```python
# Include deterministic context
context = {
    'project_id': project.id,
    'tech_stack': sorted(project.tech_stack),  # Sorted for consistency
    'loaded_files': sorted(files.keys())       # Sorted keys
}
```

**DON'T**:
```python
# Include timestamps or random data
context = {
    'timestamp': datetime.now(),  # ❌ Changes every time
    'random_id': uuid.uuid4()     # ❌ Never hits cache
}
```

### 2. Context Completeness

**DO**: Include context that affects results
```python
# Analysis depends on project files
cache_manager.analysis.get(spec, context=project_context)
```

**DON'T**: Omit context when it matters
```python
# ❌ Results differ based on project, but context omitted
cache_manager.analysis.get(spec, context=None)
```

### 3. Cache Invalidation

**Trust TTL**: Let automatic expiration handle most cases
```python
# Analysis cache expires after 7 days automatically
# No manual invalidation needed
```

**Manual Clear**: Only when necessary
```python
# User explicitly requests re-analysis
if force_recompute:
    cache_manager.analysis.clear()
    result = perform_analysis()
    cache_manager.analysis.save(...)
```

### 4. Performance

**Batch Operations**: Use manager for multiple cache types
```python
# ✅ Single manager instance
manager = CacheManager()
analysis_result = manager.analysis.get(...)
command_result = manager.command.get(...)
mcp_result = manager.mcp.get(...)
```

**Avoid**: Creating multiple managers
```python
# ❌ Inefficient - multiple stat file reads
manager1 = CacheManager()
result1 = manager1.analysis.get(...)

manager2 = CacheManager()
result2 = manager2.command.get(...)
```

---

## Error Handling

### Graceful Degradation

```python
try:
    result = cache_manager.analysis.get(spec, context=context)
    if result is None:
        result = perform_analysis(spec)
        cache_manager.analysis.save(spec, result, context=context)
except Exception as e:
    # Cache failure should not break functionality
    log.warning(f"Cache error: {e}")
    result = perform_analysis(spec)  # Fallback to direct execution
```

### Corruption Recovery

Cache system auto-recovers from corruption:
- Detects invalid JSON
- Deletes corrupted files
- Returns None (cache miss)
- Logs warning

No special handling needed in your code.

---

## Testing Guidelines

### Test Cache Integration

```python
def test_analyze_with_cache(tmp_path):
    """Test analysis uses cache correctly."""
    # Use temp directory for tests
    manager = CacheManager(base_dir=tmp_path)

    spec = "Test specification"
    context = {'project_id': 'test'}

    # First call - cache miss
    result1 = analyze_spec(spec, context, cache=manager)
    assert result1 is not None

    # Second call - cache hit
    result2 = analyze_spec(spec, context, cache=manager)
    assert result2 == result1
    assert result2.get('_cache_hit') is True

    # Different context - cache miss
    different_context = {'project_id': 'different'}
    result3 = analyze_spec(spec, different_context, cache=manager)
    assert result3.get('_cache_hit') is not True
```

### NO MOCKS

Follow Shannon philosophy - test with real cache I/O:
```python
# ✅ Real file operations
with tempfile.TemporaryDirectory() as tmpdir:
    manager = CacheManager(base_dir=Path(tmpdir))
    # Test with actual cache files

# ❌ Mocked cache
with patch('CacheManager.get') as mock_get:  # Don't do this
    mock_get.return_value = {...}
```

---

## Performance Monitoring

### Log Cache Performance

```python
import logging

logger = logging.getLogger(__name__)

def analyze_with_monitoring(spec, context):
    start = time.time()
    result = cache_manager.analysis.get(spec, context=context)
    elapsed = time.time() - start

    if result is None:
        logger.info("Cache MISS - performing analysis")
        result = perform_analysis(spec)
        cache_manager.analysis.save(spec, result, context=context)
    else:
        logger.info(f"Cache HIT - saved {elapsed:.3f}s")

    return result
```

### Track Hit Rates

```python
# Periodic stats logging
stats = cache_manager.get_stats()

logger.info(f"Cache performance - Overall hit rate: {stats['overall']['hit_rate_percent']:.1f}%")
logger.info(f"Cost savings: ${stats['overall']['total_savings_usd']:.2f}")
```

---

## Common Patterns

### Pattern 1: Optional Cache

```python
def process_with_optional_cache(data, use_cache=True, cache_manager=None):
    """Process data with optional caching."""
    if use_cache and cache_manager:
        result = cache_manager.analysis.get(data)
        if result:
            return result

    # Perform processing
    result = expensive_processing(data)

    if use_cache and cache_manager:
        cache_manager.analysis.save(data, result)

    return result
```

### Pattern 2: Fallback Chain

```python
def get_recommendations_with_fallback(domains):
    """Try cache → similarity search → compute."""
    # Try exact match
    mcps = cache_manager.mcp.get(domains)
    if mcps:
        return mcps

    # Try similar domains
    similar = cache_manager.mcp.find_similar_domains(domains, threshold=0.9)
    if similar:
        return get_recommendations_for_signature(similar[0]['signature'])

    # Compute fresh
    mcps = compute_recommendations(domains)
    cache_manager.mcp.save(domains, mcps)
    return mcps
```

### Pattern 3: Batch Processing

```python
def process_multiple_specs(specs, context):
    """Process multiple specs efficiently."""
    results = []

    for spec in specs:
        # Try cache for each
        result = cache_manager.analysis.get(spec, context=context)

        if result is None:
            # Batch compute if needed
            uncached_specs.append(spec)

    # Process uncached in batch
    if uncached_specs:
        batch_results = batch_analyze(uncached_specs)
        for spec, result in zip(uncached_specs, batch_results):
            cache_manager.analysis.save(spec, result, context=context)
            results.append(result)

    return results
```

---

## Troubleshooting

### Cache Not Hitting

**Issue**: Expected cache hit but getting miss

**Check**:
1. Context matches exactly (sorted keys, deterministic values)
2. Framework version matches
3. Model string matches
4. Entry not expired (check TTL)

**Debug**:
```python
key1 = cache_manager.analysis.compute_key(spec, context1)
key2 = cache_manager.analysis.compute_key(spec, context2)

print(f"Key 1: {key1}")
print(f"Key 2: {key2}")
print(f"Match: {key1 == key2}")
```

### Cache Files Growing

**Issue**: Cache directory getting large

**Solution**:
```python
# Check size
size_mb = cache_manager.get_total_size_mb()
print(f"Total cache: {size_mb:.2f} MB")

# Evict old entries
if size_mb > 400:
    evicted = cache_manager.evict_lru(target_mb=300)
    print(f"Evicted {evicted} entries")
```

### Stats Not Updating

**Issue**: Statistics seem stale

**Check**:
```python
# Ensure using same manager instance
# Stats persist in files, so should survive restarts

# Force reload
manager = CacheManager()
stats = manager.get_stats()
```

---

## Migration Guide

### From No Cache to Cache

1. Add cache manager initialization:
```python
# At module/class level
cache_manager = CacheManager()
```

2. Wrap expensive operations:
```python
# Before
result = expensive_operation()

# After
result = cache_manager.analysis.get(key)
if result is None:
    result = expensive_operation()
    cache_manager.analysis.save(key, result)
```

3. Test thoroughly with real operations

---

## Support

**Questions**: Contact Wave 1, Agent 2 (Cache Architect)
**Issues**: Check `CACHE_IMPLEMENTATION_SUMMARY.md`
**Tests**: See `tests/cache/test_cache_system.py`
**Demo**: Run `examples/cache_demo.py`

---

**Integration Status**: READY
**Quality**: PRODUCTION-READY
**Performance**: OPTIMIZED
