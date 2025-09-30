# Memory System API Reference

Complete API documentation for Shannon Framework memory management components.

## Table of Contents
- [MemoryTierManager](#memorytier manager)
- [ContextMonitor](#contextmonitor)
- [ManualCheckpointManager](#manualcheckpointmanager)
- [SerenaReferenceTracker](#serenare ferencetracker)

---

## MemoryTierManager

5-tier memory hierarchy with automatic transitions and intelligent compression.

### Memory Tiers

- **Working**: 0-1min, no compression, instant access
- **Hot**: 1min-1hr, 5:1 semantic compression, 10ms access
- **Warm**: 1hr-24hr, 10:1 AST compression, 20ms access
- **Cold**: 24hr-7d, 50:1 holographic compression, 50ms access
- **Archive**: >7d, 100:1 archive compression, 100ms access

### Class Definition

```python
class MemoryTierManager:
    def __init__(self, storage_path: Optional[Path] = None)
```

**Parameters:**
- `storage_path` (Optional[Path]): Path for persistent storage (default: `~/.shannon/memory`)

**Automatic Features:**
- Time-based tier transitions
- Intelligent compression
- Access pattern tracking
- Automatic cleanup

### Methods

#### start() / stop()

Start/stop automatic tier management.

```python
async def start(self)
async def stop(self)
```

**Example:**
```python
manager = MemoryTierManager()
await manager.start()

# ... use manager ...

await manager.stop()
```

#### store()

Store new memory item in Working tier.

```python
def store(
    self,
    key: str,
    content: Any,
    metadata: Optional[Dict[str, Any]] = None
) -> MemoryItem
```

**Parameters:**
- `key` (str): Unique memory identifier
- `content` (Any): Content to store (any JSON-serializable type)
- `metadata` (Optional[Dict]): Additional metadata

**Returns:**
- `MemoryItem`: Created memory item with metadata

**Example:**
```python
# Store analysis results
item = manager.store(
    key="analysis_results_2024",
    content={
        'files_analyzed': 150,
        'issues_found': 23,
        'recommendations': [...]
    },
    metadata={'project': 'auth_refactor', 'version': '2.1'}
)

print(f"Stored in tier: {item.tier.value}")
print(f"Size: {item.original_size} bytes")
```

#### retrieve()

Retrieve memory item by key.

```python
def retrieve(
    self,
    key: str
) -> Optional[Any]
```

**Parameters:**
- `key` (str): Memory identifier

**Returns:**
- `Any`: Content if found, None otherwise

**Features:**
- Automatic decompression
- Access tracking
- Usage statistics

**Example:**
```python
# Retrieve stored data
content = manager.retrieve("analysis_results_2024")
if content:
    print(f"Files analyzed: {content['files_analyzed']}")
else:
    print("Memory not found")
```

#### get_item()

Get full memory item with metadata.

```python
def get_item(
    self,
    key: str
) -> Optional[MemoryItem]
```

**Returns:**
- `MemoryItem`: Full item with all metadata

**Example:**
```python
item = manager.get_item("analysis_results_2024")
if item:
    print(f"Tier: {item.tier.value}")
    print(f"Created: {datetime.fromtimestamp(item.created_at)}")
    print(f"Accessed: {item.access_count} times")
    print(f"Compressed: {item.compressed}")
    if item.compressed:
        print(f"Compression: {item.compression_type.value}")
        ratio = item.original_size / item.compressed_size
        print(f"Ratio: {ratio:.1f}:1")
```

#### transition_item()

Manually transition item to specific tier.

```python
async def transition_item(
    self,
    key: str,
    target_tier: MemoryTier
) -> bool
```

**Parameters:**
- `key` (str): Memory identifier
- `target_tier` (MemoryTier): Target tier

**Returns:**
- `bool`: True if transitioned, False if not found

**Example:**
```python
from shannon.memory import MemoryTier

# Force immediate archival
success = await manager.transition_item(
    key="old_analysis",
    target_tier=MemoryTier.ARCHIVE
)

if success:
    print("Transitioned to archive")
```

#### delete()

Delete memory item.

```python
def delete(
    self,
    key: str
) -> bool
```

**Returns:**
- `bool`: True if deleted, False if not found

**Example:**
```python
if manager.delete("temp_analysis"):
    print("Memory deleted")
```

#### get_tier_stats()

Get statistics for all tiers.

```python
def get_tier_stats(self) -> Dict[str, Any]
```

**Returns:**
- `Dict`: Comprehensive tier statistics
  - `tiers`: Per-tier statistics
  - `global_stats`: Overall statistics
  - `avg_compression_ratio`: Average compression achieved

**Example:**
```python
stats = manager.get_tier_stats()

print("\nTier Statistics:")
for tier_name, tier_stats in stats['tiers'].items():
    print(f"\n{tier_name.upper()}:")
    print(f"  Items: {tier_stats['count']}")
    print(f"  Size: {tier_stats['total_size'] / 1024:.1f} KB")
    print(f"  Compression: {tier_stats['compression_ratio']:.1f}:1")
    print(f"  Avg Access: {tier_stats['avg_access_count']:.1f}")

print(f"\nGlobal avg compression: {stats['avg_compression_ratio']:.1f}:1")
print(f"Total transitions: {stats['global_stats']['transitions']}")
```

#### list_keys()

List all keys, optionally filtered by tier.

```python
def list_keys(
    self,
    tier: Optional[MemoryTier] = None
) -> List[str]
```

**Parameters:**
- `tier` (Optional[MemoryTier]): Optional tier filter

**Returns:**
- `List[str]`: Memory keys

**Example:**
```python
# All keys
all_keys = manager.list_keys()
print(f"Total memories: {len(all_keys)}")

# Working tier only
working_keys = manager.list_keys(MemoryTier.WORKING)
print(f"Active memories: {len(working_keys)}")

# Archive tier
archived_keys = manager.list_keys(MemoryTier.ARCHIVE)
print(f"Archived memories: {len(archived_keys)}")
```

#### save_to_disk() / load_from_disk()

Persist/restore memory state.

```python
def save_to_disk(self)
def load_from_disk(self)
```

**Example:**
```python
# Save before shutdown
manager.save_to_disk()

# Restore on startup
new_manager = MemoryTierManager()
new_manager.load_from_disk()
```

---

## ContextMonitor

Real-time token usage monitoring with 4-level alert system.

### Alert Levels

- **GREEN (0-60%)**: Normal operation
- **YELLOW (60-75%)**: Resource optimization suggested
- **ORANGE (75-85%)**: Warning alerts active
- **RED (85-95%)**: Force efficiency modes
- **CRITICAL (95%+)**: Emergency protocols

### Class Definition

```python
class ContextMonitor:
    def __init__(
        self,
        tokens_limit: int = 200000,
        storage_path: Optional[Path] = None
    )
```

**Parameters:**
- `tokens_limit` (int): Maximum token budget (default: 200000)
- `storage_path` (Optional[Path]): Storage path (default: `~/.shannon/context`)

### Methods

#### update_usage()

Update token usage and check alert levels.

```python
def update_usage(
    self,
    tokens_used: int
)
```

**Parameters:**
- `tokens_used` (int): Current token count

**Side Effects:**
- Creates usage snapshot
- Triggers alert callbacks if level changes
- Updates alert history

**Example:**
```python
monitor = ContextMonitor(tokens_limit=200000)

# Update periodically
monitor.update_usage(50000)  # 25% - GREEN
monitor.update_usage(130000)  # 65% - YELLOW
monitor.update_usage(170000)  # 85% - ORANGE
```

#### register_alert_callback()

Register callback for specific alert level.

```python
def register_alert_callback(
    self,
    level: AlertLevel,
    callback: callable
)
```

**Parameters:**
- `level` (AlertLevel): Alert level to trigger on
- `callback` (callable): Function receiving `(level, usage_percent)`

**Example:**
```python
from shannon.memory import AlertLevel

def on_yellow_alert(level, usage_percent):
    print(f"⚠️ Yellow alert: {usage_percent:.1f}% usage")
    print("Enabling caching strategies")

def on_red_alert(level, usage_percent):
    print(f"🚨 Red alert: {usage_percent:.1f}% usage")
    print("Forcing efficiency modes")

monitor.register_alert_callback(AlertLevel.YELLOW, on_yellow_alert)
monitor.register_alert_callback(AlertLevel.RED, on_red_alert)
```

#### add_memory_reference() / remove_memory_reference()

Track active memory references.

```python
def add_memory_reference(self, memory_key: str)
def remove_memory_reference(self, memory_key: str)
```

**Example:**
```python
# Track memory usage
monitor.add_memory_reference("wave_2_results")
monitor.add_memory_reference("analysis_cache")

# Release when done
monitor.remove_memory_reference("wave_2_results")
```

#### add_serena_key()

Track Serena MCP memory key for context preservation.

```python
def add_serena_key(
    self,
    serena_key: str
)
```

**Example:**
```python
# Track Serena integration
monitor.add_serena_key("wave_2_core_implementation_synthesis")
monitor.add_serena_key("project_architecture_analysis")
```

#### get_recommendations()

Get optimization recommendations based on current usage.

```python
def get_recommendations(self) -> List[str]
```

**Returns:**
- `List[str]`: Actionable recommendations

**Example:**
```python
recommendations = monitor.get_recommendations()
for rec in recommendations:
    print(f"💡 {rec}")

# Example output at ORANGE level:
# 💡 Warning: Approaching capacity
# 💡 Defer non-critical operations
# 💡 Consider checkpoint creation
# 💡 Enable caching for repeated operations
```

#### get_current_snapshot()

Get current context snapshot.

```python
def get_current_snapshot(self) -> ContextSnapshot
```

**Returns:**
- `ContextSnapshot`: Current state snapshot

**Example:**
```python
snapshot = monitor.get_current_snapshot()
print(f"Tokens: {snapshot.tokens_used:,} / {snapshot.tokens_limit:,}")
print(f"Usage: {snapshot.usage_percent:.1%}")
print(f"Alert: {snapshot.alert_level.value}")
print(f"Active memories: {len(snapshot.active_memories)}")
print(f"Serena keys: {len(snapshot.serena_keys)}")
```

#### get_stats()

Get monitoring statistics.

```python
def get_stats(self) -> Dict[str, Any]
```

**Returns:**
- `Dict`: Comprehensive statistics
  - `current`: Current state
  - `memories`: Memory tracking
  - `history`: Historical data

**Example:**
```python
stats = monitor.get_stats()

print("\nCurrent Status:")
print(f"  Tokens Used: {stats['current']['tokens_used']:,}")
print(f"  Usage: {stats['current']['usage_percent']:.1f}%")
print(f"  Remaining: {stats['current']['remaining']:,}")
print(f"  Alert: {stats['current']['alert_level']}")

print("\nMemory Tracking:")
print(f"  Active: {stats['memories']['active_count']}")
print(f"  Serena Keys: {stats['memories']['serena_keys_count']}")

print("\nHistory:")
print(f"  Snapshots: {stats['history']['snapshots_count']}")
print(f"  Total Alerts: {stats['history']['alerts_count']}")
for level, count in stats['history']['alert_breakdown'].items():
    if count > 0:
        print(f"    {level}: {count}")
```

---

## ManualCheckpointManager

Manual checkpoint management with context preservation (v2.1 critical feature).

### Class Definition

```python
class ManualCheckpointManager:
    def __init__(self, storage_path: Optional[Path] = None)
```

**Parameters:**
- `storage_path` (Optional[Path]): Checkpoint storage (default: `~/.shannon/checkpoints`)

### Methods

#### create_checkpoint()

Create manual checkpoint with full context preservation.

```python
def create_checkpoint(
    self,
    checkpoint_id: str,
    description: str,
    context_monitor: ContextMonitor,
    wave_state: Optional[Dict[str, Any]] = None,
    user_notes: str = ""
) -> Checkpoint
```

**Parameters:**
- `checkpoint_id` (str): Unique checkpoint identifier
- `description` (str): Checkpoint description
- `context_monitor` (ContextMonitor): Context monitor instance
- `wave_state` (Optional[Dict]): Optional wave execution state
- `user_notes` (str): Optional user notes

**Returns:**
- `Checkpoint`: Created checkpoint with full state

**Example:**
```python
manager = ManualCheckpointManager()

checkpoint = manager.create_checkpoint(
    checkpoint_id="wave_2_complete",
    description="Wave 2 core implementation complete",
    context_monitor=monitor,
    wave_state={
        'wave_id': 'wave_2',
        'phase': 'implementation',
        'agents_completed': 5
    },
    user_notes="All core features implemented, memory system functional"
)

print(f"Checkpoint created: {checkpoint.checkpoint_id}")
print(f"Serena keys preserved: {len(checkpoint.serena_memory_keys)}")
```

#### get_checkpoint()

Retrieve checkpoint by ID.

```python
def get_checkpoint(
    self,
    checkpoint_id: str
) -> Optional[Checkpoint]
```

**Returns:**
- `Checkpoint`: Checkpoint if found, None otherwise

**Example:**
```python
checkpoint = manager.get_checkpoint("wave_2_complete")
if checkpoint:
    print(f"Description: {checkpoint.description}")
    print(f"Created: {datetime.fromtimestamp(checkpoint.timestamp)}")
    print(f"Token usage: {checkpoint.context_snapshot.usage_percent:.1%}")
```

#### list_checkpoints()

List all checkpoints sorted by timestamp.

```python
def list_checkpoints(self) -> List[Checkpoint]
```

**Returns:**
- `List[Checkpoint]`: All checkpoints (newest first)

**Example:**
```python
checkpoints = manager.list_checkpoints()

print("\nAvailable Checkpoints:")
for cp in checkpoints:
    created = datetime.fromtimestamp(cp.timestamp)
    print(f"\n{cp.checkpoint_id}")
    print(f"  Created: {created.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Description: {cp.description}")
    print(f"  Token usage: {cp.context_snapshot.usage_percent:.1%}")
    print(f"  Serena keys: {len(cp.serena_memory_keys)}")
```

#### delete_checkpoint()

Delete checkpoint.

```python
def delete_checkpoint(
    self,
    checkpoint_id: str
) -> bool
```

**Returns:**
- `bool`: True if deleted, False if not found

**Example:**
```python
if manager.delete_checkpoint("old_checkpoint"):
    print("Checkpoint deleted")
```

#### get_restoration_instructions()

Get instructions for restoring from checkpoint.

```python
def get_restoration_instructions(
    self,
    checkpoint_id: str
) -> Optional[str]
```

**Returns:**
- `str`: Markdown-formatted restoration instructions

**Example:**
```python
instructions = manager.get_restoration_instructions("wave_2_complete")
print(instructions)

# Output includes:
# - Checkpoint metadata
# - Context state at checkpoint
# - Serena memory keys to restore
# - Wave state information
# - Restoration commands
```

---

## SerenaReferenceTracker

Tracks Serena MCP memory keys for accurate context preservation (v2.1 critical feature).

### Class Definition

```python
class SerenaReferenceTracker:
    def __init__(self, storage_path: Optional[Path] = None)
```

**Parameters:**
- `storage_path` (Optional[Path]): Storage path (default: `~/.shannon/serena_refs`)

### Methods

#### register_reference()

Register Serena memory reference.

```python
def register_reference(
    self,
    reference_key: str,
    serena_memory_keys: List[str],
    context: str,
    metadata: Optional[Dict[str, Any]] = None
)
```

**Parameters:**
- `reference_key` (str): Unique reference identifier
- `serena_memory_keys` (List[str]): Serena memory keys
- `context` (str): Context description
- `metadata` (Optional[Dict]): Additional metadata

**Example:**
```python
tracker = SerenaReferenceTracker()

tracker.register_reference(
    reference_key="wave_2_implementation",
    serena_memory_keys=[
        "wave_2_core_implementation_synthesis",
        "orchestrator_implementation_details",
        "memory_system_architecture"
    ],
    context="Wave 2 core implementation memories",
    metadata={'wave_id': 'wave_2', 'phase': 'implementation'}
)
```

#### get_serena_keys()

Get Serena memory keys for reference.

```python
def get_serena_keys(
    self,
    reference_key: str
) -> List[str]
```

**Returns:**
- `List[str]`: Serena memory keys

**Example:**
```python
keys = tracker.get_serena_keys("wave_2_implementation")
print(f"Serena keys: {len(keys)}")
for key in keys:
    print(f"  - {key}")
```

#### get_all_serena_keys()

Get all active Serena memory keys.

```python
def get_all_serena_keys(self) -> Set[str]
```

**Returns:**
- `Set[str]`: All active Serena keys

**Example:**
```python
all_keys = tracker.get_all_serena_keys()
print(f"Total Serena keys tracked: {len(all_keys)}")
```

#### remove_reference()

Remove reference tracking.

```python
def remove_reference(
    self,
    reference_key: str
)
```

**Example:**
```python
tracker.remove_reference("old_wave_reference")
```

---

## Complete Usage Example

```python
import asyncio
from pathlib import Path
from shannon.memory import (
    MemoryTierManager,
    ContextMonitor,
    ManualCheckpointManager,
    SerenaReferenceTracker,
    AlertLevel,
    MemoryTier
)

async def main():
    # Initialize memory system
    memory_manager = MemoryTierManager()
    await memory_manager.start()

    # Store analysis results
    memory_manager.store(
        key="wave_2_analysis",
        content={'files': 150, 'issues': 23},
        metadata={'phase': 'analysis'}
    )

    # Initialize context monitoring
    monitor = ContextMonitor(tokens_limit=200000)

    # Register alert callbacks
    def on_yellow(level, usage):
        print(f"⚠️ {usage:.1f}% - Optimizing")

    monitor.register_alert_callback(AlertLevel.YELLOW, on_yellow)

    # Simulate token usage
    monitor.update_usage(50000)
    monitor.add_memory_reference("wave_2_analysis")

    # Create checkpoint
    checkpoint_manager = ManualCheckpointManager()
    checkpoint = checkpoint_manager.create_checkpoint(
        checkpoint_id="milestone_1",
        description="Analysis phase complete",
        context_monitor=monitor,
        user_notes="Ready for implementation"
    )

    # Track Serena references
    tracker = SerenaReferenceTracker()
    tracker.register_reference(
        reference_key="analysis_phase",
        serena_memory_keys=["analysis_results", "code_metrics"],
        context="Analysis phase memories"
    )

    # Get statistics
    tier_stats = memory_manager.get_tier_stats()
    context_stats = monitor.get_stats()

    print(f"\nMemory: {tier_stats['global_stats']['transitions']} transitions")
    print(f"Context: {context_stats['current']['usage_percent']:.1f}% usage")
    print(f"Checkpoint: {checkpoint.checkpoint_id} created")

    # Cleanup
    await memory_manager.stop()

if __name__ == "__main__":
    asyncio.run(main())
```