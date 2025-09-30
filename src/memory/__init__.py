"""
Shannon Framework Memory System

Multi-tier memory management with context monitoring and manual checkpoint system.

Key Components:
- MemoryTierManager: 5-tier memory hierarchy with automatic transitions
- ContextMonitor: Real-time token usage tracking with 4-level alerts
- ManualCheckpointManager: Manual context preservation and restoration
- SerenaReferenceTracker: Serena MCP key tracking for context continuity

Usage:
    from shannon.memory import (
        MemoryTierManager,
        MemoryTier,
        ContextMonitor,
        AlertLevel,
        ManualCheckpointManager,
        SerenaReferenceTracker
    )

    # Initialize components
    tier_manager = MemoryTierManager()
    context_monitor = ContextMonitor(tokens_limit=200000)
    checkpoint_manager = ManualCheckpointManager()
    serena_tracker = SerenaReferenceTracker()

    # Start tier management
    await tier_manager.start()

    # Store memory
    tier_manager.store("analysis_results", {"findings": "..."})

    # Monitor context
    context_monitor.update_usage(50000)
    if context_monitor.current_alert_level == AlertLevel.YELLOW:
        print("Optimization recommended")

    # Create checkpoint
    checkpoint = checkpoint_manager.create_checkpoint(
        checkpoint_id="wave_2_complete",
        description="Wave 2 analysis complete",
        context_monitor=context_monitor,
        wave_state={"wave": 2, "status": "complete"}
    )

    # Track Serena references
    serena_tracker.register_reference(
        reference_key="analysis_session",
        serena_memory_keys=["memory_key_1", "memory_key_2"],
        context="Wave 2 analysis session"
    )
"""

from .tier_manager import (
    MemoryTier,
    CompressionType,
    MemoryItem,
    MemoryTierManager,
    SemanticCompressor,
    ASTCompressor,
    HolographicCompressor,
    ArchiveCompressor
)

from .context_monitor import (
    AlertLevel,
    ContextSnapshot,
    Checkpoint,
    ContextMonitor,
    ManualCheckpointManager,
    SerenaReferenceTracker
)

__all__ = [
    # Tier Management
    "MemoryTier",
    "CompressionType",
    "MemoryItem",
    "MemoryTierManager",
    "SemanticCompressor",
    "ASTCompressor",
    "HolographicCompressor",
    "ArchiveCompressor",

    # Context Monitoring
    "AlertLevel",
    "ContextSnapshot",
    "Checkpoint",
    "ContextMonitor",
    "ManualCheckpointManager",
    "SerenaReferenceTracker",
]

__version__ = "2.1.0"