"""
Example 2: Manual Checkpoint Management
========================================

Demonstrates manual context management through checkpoint creation and restoration.
Shows how to preserve context across sessions using Serena memory references.
"""

import asyncio
import sys
import time
from pathlib import Path

# Add Shannon to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from memory.context_monitor import (
    ContextMonitor,
    ManualCheckpointManager,
    SerenaReferenceTracker,
    AlertLevel
)


async def simulate_work(monitor: ContextMonitor, tokens: int):
    """Simulate work that consumes tokens."""
    monitor.update_usage(monitor.tokens_used + tokens)
    await asyncio.sleep(0.1)  # Simulate processing


async def main():
    """Demonstrate manual checkpoint management."""

    print("="*70)
    print("Shannon Framework v2.1 - Manual Checkpoint Management")
    print("="*70)
    print()

    # ========================================================================
    # STEP 1: Initialize context monitoring
    # ========================================================================
    monitor = ContextMonitor(tokens_limit=200000)
    checkpoint_mgr = ManualCheckpointManager()
    serena_tracker = SerenaReferenceTracker()

    print("Initialized:")
    print(f"  Token Limit: {monitor.tokens_limit:,}")
    print(f"  Initial Usage: {monitor.tokens_used:,}")
    print()

    # ========================================================================
    # STEP 2: Simulate progressive work with monitoring
    # ========================================================================
    print("Phase 1: Initial Analysis")
    print("-" * 70)

    # Register alert callback
    def alert_handler(level: AlertLevel, usage: float):
        print(f"  🚨 Alert: {level.value} ({usage:.1f}% usage)")

    monitor.register_alert_callback(AlertLevel.YELLOW, alert_handler)
    monitor.register_alert_callback(AlertLevel.ORANGE, alert_handler)
    monitor.register_alert_callback(AlertLevel.RED, alert_handler)

    # Simulate initial analysis work
    await simulate_work(monitor, 50000)
    monitor.add_memory_reference("analysis_results")
    monitor.add_serena_key("serena/analysis/auth_system")

    print(f"  Tokens Used: {monitor.tokens_used:,} ({monitor.get_usage_percent():.1f}%)")
    print(f"  Alert Level: {monitor.current_alert_level.value}")
    print(f"  Active Memories: {len(monitor.active_memories)}")
    print()

    # ========================================================================
    # STEP 3: Create first checkpoint
    # ========================================================================
    print("Creating Checkpoint #1: after_analysis")
    print("-" * 70)

    wave_state = {
        'phase': 'analysis',
        'completed_tasks': ['code_review', 'dependency_analysis'],
        'pending_tasks': ['implementation', 'testing']
    }

    checkpoint1 = checkpoint_mgr.create_checkpoint(
        checkpoint_id="after_analysis",
        description="Completed initial analysis phase",
        context_monitor=monitor,
        wave_state=wave_state,
        user_notes="All security vulnerabilities identified"
    )

    print(f"  Checkpoint ID: {checkpoint1.checkpoint_id}")
    print(f"  Timestamp: {checkpoint1.timestamp}")
    print(f"  Token Snapshot: {checkpoint1.context_snapshot.tokens_used:,}")
    print(f"  Serena Keys: {len(checkpoint1.serena_memory_keys)}")
    print()

    # ========================================================================
    # STEP 4: Continue work - hit YELLOW zone
    # ========================================================================
    print("Phase 2: Implementation")
    print("-" * 70)

    await simulate_work(monitor, 80000)  # Now at 130K tokens
    monitor.add_memory_reference("implementation_plan")
    monitor.add_serena_key("serena/impl/auth_refactor")

    print(f"  Tokens Used: {monitor.tokens_used:,} ({monitor.get_usage_percent():.1f}%)")
    print(f"  Alert Level: {monitor.current_alert_level.value}")
    print()

    # Show recommendations
    recommendations = monitor.get_recommendations()
    if recommendations:
        print("  Recommendations:")
        for rec in recommendations:
            print(f"    • {rec}")
        print()

    # ========================================================================
    # STEP 5: Create second checkpoint at critical point
    # ========================================================================
    print("Creating Checkpoint #2: before_risky_changes")
    print("-" * 70)

    wave_state['phase'] = 'implementation'
    wave_state['completed_tasks'].extend(['auth_module', 'token_handler'])

    checkpoint2 = checkpoint_mgr.create_checkpoint(
        checkpoint_id="before_risky_changes",
        description="Before production database migration",
        context_monitor=monitor,
        wave_state=wave_state,
        user_notes="⚠️ CRITICAL: Production changes ahead"
    )

    print(f"  Checkpoint ID: {checkpoint2.checkpoint_id}")
    print(f"  Usage at Checkpoint: {checkpoint2.context_snapshot.usage_percent:.1%}")
    print()

    # ========================================================================
    # STEP 6: Simulate hitting ORANGE/RED zones
    # ========================================================================
    print("Phase 3: Heavy Testing (approaching limits)")
    print("-" * 70)

    await simulate_work(monitor, 50000)  # Now at 180K tokens

    print(f"  Tokens Used: {monitor.tokens_used:,} ({monitor.get_usage_percent():.1f}%)")
    print(f"  Alert Level: {monitor.current_alert_level.value}")
    print(f"  Remaining: {monitor.get_remaining_tokens():,} tokens")
    print()

    # ========================================================================
    # STEP 7: List all checkpoints
    # ========================================================================
    print("All Available Checkpoints:")
    print("-" * 70)

    checkpoints = checkpoint_mgr.list_checkpoints()
    for cp in checkpoints:
        print(f"  [{cp.checkpoint_id}]")
        print(f"    Description: {cp.description}")
        print(f"    Tokens: {cp.context_snapshot.tokens_used:,} ({cp.context_snapshot.usage_percent:.1%})")
        print(f"    Alert: {cp.context_snapshot.alert_level.value}")
        print()

    # ========================================================================
    # STEP 8: Show restoration instructions
    # ========================================================================
    print("Restoration Instructions for 'before_risky_changes':")
    print("-" * 70)

    instructions = checkpoint_mgr.get_restoration_instructions("before_risky_changes")
    print(instructions)

    # ========================================================================
    # STEP 9: Display monitoring stats
    # ========================================================================
    print()
    print("Final Monitoring Statistics:")
    print("-" * 70)

    stats = monitor.get_stats()
    print(f"Current State:")
    print(f"  Tokens Used: {stats['current']['tokens_used']:,}")
    print(f"  Usage: {stats['current']['usage_percent']:.1f}%")
    print(f"  Alert Level: {stats['current']['alert_level']}")
    print()
    print(f"Memory:")
    print(f"  Active Memories: {stats['memories']['active_count']}")
    print(f"  Serena Keys: {stats['memories']['serena_keys_count']}")
    print()
    print(f"History:")
    print(f"  Snapshots: {stats['history']['snapshots_count']}")
    print(f"  Alerts: {stats['history']['alerts_count']}")

    print()
    print("="*70)
    print("Example Complete!")
    print("="*70)


# ============================================================================
# EXPECTED OUTPUT:
# ============================================================================
"""
======================================================================
Shannon Framework v2.1 - Manual Checkpoint Management
======================================================================

Initialized:
  Token Limit: 200,000
  Initial Usage: 0

Phase 1: Initial Analysis
----------------------------------------------------------------------
  Tokens Used: 50,000 (25.0% usage)
  Alert Level: green
  Active Memories: 1

Creating Checkpoint #1: after_analysis
----------------------------------------------------------------------
  Checkpoint ID: after_analysis
  Timestamp: 1704134567.123
  Token Snapshot: 50,000
  Serena Keys: 1

Phase 2: Implementation
----------------------------------------------------------------------
  🚨 Alert: yellow (65.0% usage)
  Tokens Used: 130,000 (65.0% usage)
  Alert Level: yellow

  Recommendations:
    • Resource optimization suggested
    • Enable caching strategies
    • Consider --uc mode for verbose operations

Creating Checkpoint #2: before_risky_changes
----------------------------------------------------------------------
  Checkpoint ID: before_risky_changes
  Usage at Checkpoint: 65.0%

Phase 3: Heavy Testing (approaching limits)
----------------------------------------------------------------------
  🚨 Alert: red (90.0% usage)
  Tokens Used: 180,000 (90.0% usage)
  Alert Level: red
  Remaining: 20,000 tokens

All Available Checkpoints:
----------------------------------------------------------------------
  [before_risky_changes]
    Description: Before production database migration
    Tokens: 130,000 (65.0%)
    Alert: yellow

  [after_analysis]
    Description: Completed initial analysis phase
    Tokens: 50,000 (25.0%)
    Alert: green

======================================================================
Example Complete!
======================================================================
"""


if __name__ == '__main__':
    asyncio.run(main())