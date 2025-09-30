"""
Time Travel Debugging Module

Provides state snapshot management with timeline tracking, rewind capabilities,
and branch management for debugging multi-agent systems.
"""

from .snapshot_manager import (
    SnapshotManager,
    Snapshot,
    SystemState,
    Timeline,
    SnapshotType,
    TimelineNavigator,
    BranchManager
)

__all__ = [
    'SnapshotManager',
    'Snapshot',
    'SystemState',
    'Timeline',
    'SnapshotType',
    'TimelineNavigator',
    'BranchManager'
]