"""
Time Travel Snapshot Manager

Implements state snapshot management with timeline tracking, rewind capabilities,
and branch management for debugging multi-agent systems.

Key Features:
- Complete state capture (agents, memory, context, random state)
- Timeline navigation with rewind functionality
- Branch management for alternate timelines
- Async snapshot creation for minimal disruption
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple, Callable, Coroutine
from datetime import datetime
from enum import Enum
import json
import pickle
import asyncio
import random
import hashlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class SnapshotType(Enum):
    """Types of snapshots"""
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    CHECKPOINT = "checkpoint"
    BRANCH_POINT = "branch_point"


@dataclass
class SystemState:
    """Complete system state at a point in time"""
    agents: Dict[str, Any]
    memory: Dict[str, Any]
    context: Dict[str, Any]
    random_state: Tuple[Any, ...]
    metadata: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "agents": self.agents,
            "memory": self.memory,
            "context": self.context,
            "random_state": self.random_state,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SystemState':
        """Create from dictionary"""
        return cls(
            agents=data["agents"],
            memory=data["memory"],
            context=data["context"],
            random_state=tuple(data["random_state"]),
            metadata=data["metadata"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )


@dataclass
class Snapshot:
    """Single snapshot of system state"""
    snapshot_id: str
    timeline_id: str
    parent_id: Optional[str]
    state: SystemState
    snapshot_type: SnapshotType
    description: str
    tags: Set[str] = field(default_factory=set)
    size_bytes: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Calculate size after initialization"""
        if self.size_bytes == 0:
            # Estimate size from pickled state
            pickled = pickle.dumps(self.state)
            self.size_bytes = len(pickled)


@dataclass
class Timeline:
    """Timeline containing sequence of snapshots"""
    timeline_id: str
    name: str
    description: str
    parent_timeline_id: Optional[str]
    branch_point_id: Optional[str]
    snapshots: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True


class SnapshotManager:
    """
    Manages state snapshots with timeline tracking.

    Provides complete state capture including agents, memory, context,
    and random state for deterministic replay and debugging.
    """

    def __init__(
        self,
        storage_path: Optional[Path] = None,
        auto_snapshot_interval: Optional[int] = None
    ):
        """
        Initialize snapshot manager.

        Args:
            storage_path: Path for persistent snapshot storage
            auto_snapshot_interval: Interval in seconds for automatic snapshots
        """
        self.storage_path = storage_path
        self.auto_snapshot_interval = auto_snapshot_interval

        self.snapshots: Dict[str, Snapshot] = {}
        self.timelines: Dict[str, Timeline] = {}
        self.current_timeline_id: Optional[str] = None
        self.current_snapshot_id: Optional[str] = None

        self._auto_snapshot_task: Optional[asyncio.Task] = None
        self._snapshot_lock = asyncio.Lock()

        # Create default timeline
        self._create_timeline("main", "Main timeline", None, None)

    def _create_timeline(
        self,
        timeline_id: str,
        name: str,
        parent_timeline_id: Optional[str],
        branch_point_id: Optional[str]
    ) -> Timeline:
        """Create a new timeline"""
        timeline = Timeline(
            timeline_id=timeline_id,
            name=name,
            description=f"Timeline: {name}",
            parent_timeline_id=parent_timeline_id,
            branch_point_id=branch_point_id
        )

        self.timelines[timeline_id] = timeline

        if self.current_timeline_id is None:
            self.current_timeline_id = timeline_id

        logger.info(f"Created timeline: {name} ({timeline_id})")
        return timeline

    async def create_snapshot(
        self,
        state: SystemState,
        description: str = "",
        snapshot_type: SnapshotType = SnapshotType.MANUAL,
        tags: Optional[Set[str]] = None
    ) -> Snapshot:
        """
        Create a snapshot of current system state.

        Args:
            state: System state to capture
            description: Human-readable description
            snapshot_type: Type of snapshot
            tags: Optional tags for categorization

        Returns:
            Created snapshot
        """
        async with self._snapshot_lock:
            # Generate snapshot ID
            state_hash = hashlib.sha256(
                pickle.dumps(state)
            ).hexdigest()[:16]
            snapshot_id = f"snap_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{state_hash}"

            # Create snapshot
            snapshot = Snapshot(
                snapshot_id=snapshot_id,
                timeline_id=self.current_timeline_id,
                parent_id=self.current_snapshot_id,
                state=state,
                snapshot_type=snapshot_type,
                description=description or f"{snapshot_type.value} snapshot",
                tags=tags or set()
            )

            # Store snapshot
            self.snapshots[snapshot_id] = snapshot

            # Add to timeline
            if self.current_timeline_id:
                timeline = self.timelines[self.current_timeline_id]
                timeline.snapshots.append(snapshot_id)

            # Update current snapshot
            self.current_snapshot_id = snapshot_id

            logger.info(
                f"Created snapshot: {snapshot_id} "
                f"({snapshot.size_bytes} bytes, {snapshot_type.value})"
            )

            # Persist if storage path configured
            if self.storage_path:
                await self._persist_snapshot(snapshot)

            return snapshot

    async def capture_complete_state(
        self,
        agents: Optional[Dict[str, Any]] = None,
        memory: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        include_random_state: bool = True
    ) -> SystemState:
        """
        Capture complete system state.

        Args:
            agents: Agent states to capture
            memory: Memory states to capture
            context: Context to capture
            include_random_state: Whether to capture random state

        Returns:
            SystemState object
        """
        # Capture random state for deterministic replay
        random_state = None
        if include_random_state:
            random_state = random.getstate()

        # Build metadata
        metadata = {
            "capture_method": "complete",
            "components": [],
            "python_version": None  # Would capture actual version in production
        }

        if agents is not None:
            metadata["components"].append("agents")
        if memory is not None:
            metadata["components"].append("memory")
        if context is not None:
            metadata["components"].append("context")
        if random_state is not None:
            metadata["components"].append("random_state")

        return SystemState(
            agents=agents or {},
            memory=memory or {},
            context=context or {},
            random_state=random_state or tuple(),
            metadata=metadata
        )

    def get_snapshot(self, snapshot_id: str) -> Optional[Snapshot]:
        """Retrieve snapshot by ID"""
        return self.snapshots.get(snapshot_id)

    def list_snapshots(
        self,
        timeline_id: Optional[str] = None,
        snapshot_type: Optional[SnapshotType] = None,
        tags: Optional[Set[str]] = None
    ) -> List[Snapshot]:
        """
        List snapshots with optional filtering.

        Args:
            timeline_id: Filter by timeline
            snapshot_type: Filter by type
            tags: Filter by tags (any match)

        Returns:
            List of matching snapshots
        """
        snapshots = list(self.snapshots.values())

        if timeline_id:
            snapshots = [s for s in snapshots if s.timeline_id == timeline_id]

        if snapshot_type:
            snapshots = [s for s in snapshots if s.snapshot_type == snapshot_type]

        if tags:
            snapshots = [s for s in snapshots if s.tags & tags]

        return sorted(snapshots, key=lambda s: s.created_at)

    def get_timeline_history(self, timeline_id: Optional[str] = None) -> List[Snapshot]:
        """Get chronological history of snapshots in timeline"""
        timeline_id = timeline_id or self.current_timeline_id
        if not timeline_id or timeline_id not in self.timelines:
            return []

        timeline = self.timelines[timeline_id]
        return [
            self.snapshots[sid]
            for sid in timeline.snapshots
            if sid in self.snapshots
        ]

    async def _persist_snapshot(self, snapshot: Snapshot):
        """Persist snapshot to storage"""
        if not self.storage_path:
            return

        snapshot_dir = self.storage_path / snapshot.timeline_id
        snapshot_dir.mkdir(parents=True, exist_ok=True)

        snapshot_file = snapshot_dir / f"{snapshot.snapshot_id}.pkl"

        # Save snapshot
        with open(snapshot_file, 'wb') as f:
            pickle.dump(snapshot, f)

        logger.debug(f"Persisted snapshot: {snapshot_file}")

    async def start_auto_snapshot(
        self,
        state_getter: Callable[[], Coroutine[Any, Any, SystemState]]
    ):
        """
        Start automatic snapshot creation.

        Args:
            state_getter: Async function that returns current SystemState
        """
        if self.auto_snapshot_interval is None:
            return

        if self._auto_snapshot_task is not None:
            logger.warning("Auto-snapshot already running")
            return

        async def auto_snapshot_loop():
            while True:
                try:
                    await asyncio.sleep(self.auto_snapshot_interval)

                    # Get current state
                    state = await state_getter()

                    # Create automatic snapshot
                    await self.create_snapshot(
                        state=state,
                        description="Automatic checkpoint",
                        snapshot_type=SnapshotType.AUTOMATIC,
                        tags={"auto"}
                    )

                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error(f"Error in auto-snapshot: {e}")

        self._auto_snapshot_task = asyncio.create_task(auto_snapshot_loop())
        logger.info(
            f"Started auto-snapshot with interval: {self.auto_snapshot_interval}s"
        )

    async def stop_auto_snapshot(self):
        """Stop automatic snapshot creation"""
        if self._auto_snapshot_task:
            self._auto_snapshot_task.cancel()
            try:
                await self._auto_snapshot_task
            except asyncio.CancelledError:
                pass
            self._auto_snapshot_task = None
            logger.info("Stopped auto-snapshot")


class TimelineNavigator:
    """Handles timeline navigation and rewind operations"""

    def __init__(self, snapshot_manager: SnapshotManager):
        self.snapshot_manager = snapshot_manager

    async def rewind_to_snapshot(
        self,
        snapshot_id: str,
        restore_random_state: bool = True
    ) -> SystemState:
        """
        Rewind to a specific snapshot.

        Args:
            snapshot_id: ID of snapshot to rewind to
            restore_random_state: Whether to restore random state

        Returns:
            System state at that snapshot

        Raises:
            KeyError: If snapshot not found
        """
        snapshot = self.snapshot_manager.get_snapshot(snapshot_id)
        if not snapshot:
            raise KeyError(f"Snapshot not found: {snapshot_id}")

        # Restore random state if requested
        if restore_random_state and snapshot.state.random_state:
            random.setstate(snapshot.state.random_state)

        # Update current snapshot pointer
        self.snapshot_manager.current_snapshot_id = snapshot_id

        logger.info(f"Rewound to snapshot: {snapshot_id}")

        return snapshot.state

    async def rewind_steps(self, steps: int) -> Optional[SystemState]:
        """
        Rewind by a specific number of steps in current timeline.

        Args:
            steps: Number of steps to rewind (positive integer)

        Returns:
            System state after rewind, or None if not enough history
        """
        history = self.snapshot_manager.get_timeline_history()

        if not history:
            logger.warning("No timeline history available")
            return None

        # Find current snapshot index
        current_id = self.snapshot_manager.current_snapshot_id
        try:
            current_idx = next(
                i for i, s in enumerate(history)
                if s.snapshot_id == current_id
            )
        except StopIteration:
            current_idx = len(history) - 1

        # Calculate target index
        target_idx = max(0, current_idx - steps)

        if target_idx == current_idx:
            logger.info("Already at earliest snapshot")
            return history[target_idx].state

        target_snapshot = history[target_idx]
        return await self.rewind_to_snapshot(target_snapshot.snapshot_id)

    async def fast_forward_steps(self, steps: int) -> Optional[SystemState]:
        """
        Fast forward by a specific number of steps in current timeline.

        Args:
            steps: Number of steps to advance (positive integer)

        Returns:
            System state after advancement, or None if at end
        """
        history = self.snapshot_manager.get_timeline_history()

        if not history:
            logger.warning("No timeline history available")
            return None

        # Find current snapshot index
        current_id = self.snapshot_manager.current_snapshot_id
        try:
            current_idx = next(
                i for i, s in enumerate(history)
                if s.snapshot_id == current_id
            )
        except StopIteration:
            current_idx = 0

        # Calculate target index
        target_idx = min(len(history) - 1, current_idx + steps)

        if target_idx == current_idx:
            logger.info("Already at latest snapshot")
            return history[target_idx].state

        target_snapshot = history[target_idx]
        return await self.rewind_to_snapshot(target_snapshot.snapshot_id)

    def get_timeline_position(self) -> Tuple[int, int]:
        """
        Get current position in timeline.

        Returns:
            Tuple of (current_index, total_snapshots)
        """
        history = self.snapshot_manager.get_timeline_history()

        if not history:
            return (0, 0)

        current_id = self.snapshot_manager.current_snapshot_id
        try:
            current_idx = next(
                i for i, s in enumerate(history)
                if s.snapshot_id == current_id
            )
            return (current_idx + 1, len(history))
        except StopIteration:
            return (len(history), len(history))


class BranchManager:
    """Manages timeline branches and alternate timelines"""

    def __init__(self, snapshot_manager: SnapshotManager):
        self.snapshot_manager = snapshot_manager

    async def create_branch(
        self,
        branch_name: str,
        from_snapshot_id: Optional[str] = None,
        description: str = ""
    ) -> Timeline:
        """
        Create a new timeline branch from a snapshot.

        Args:
            branch_name: Name for the new branch
            from_snapshot_id: Snapshot to branch from (None = current)
            description: Description of the branch

        Returns:
            Created timeline
        """
        # Use current snapshot if not specified
        branch_point_id = from_snapshot_id or self.snapshot_manager.current_snapshot_id

        if not branch_point_id:
            raise ValueError("No snapshot to branch from")

        # Get parent timeline
        branch_point = self.snapshot_manager.get_snapshot(branch_point_id)
        if not branch_point:
            raise KeyError(f"Branch point snapshot not found: {branch_point_id}")

        parent_timeline_id = branch_point.timeline_id

        # Generate timeline ID
        timeline_id = f"branch_{branch_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Create timeline
        timeline = self.snapshot_manager._create_timeline(
            timeline_id=timeline_id,
            name=branch_name,
            parent_timeline_id=parent_timeline_id,
            branch_point_id=branch_point_id
        )

        # Mark branch point
        branch_point.tags.add("branch_point")
        branch_point.snapshot_type = SnapshotType.BRANCH_POINT

        # Switch to new timeline
        self.snapshot_manager.current_timeline_id = timeline_id

        logger.info(
            f"Created branch '{branch_name}' from snapshot {branch_point_id}"
        )

        return timeline

    def switch_timeline(self, timeline_id: str):
        """Switch to a different timeline"""
        if timeline_id not in self.snapshot_manager.timelines:
            raise KeyError(f"Timeline not found: {timeline_id}")

        self.snapshot_manager.current_timeline_id = timeline_id

        # Update current snapshot to latest in timeline
        timeline = self.snapshot_manager.timelines[timeline_id]
        if timeline.snapshots:
            self.snapshot_manager.current_snapshot_id = timeline.snapshots[-1]

        logger.info(f"Switched to timeline: {timeline_id}")

    def list_branches(self) -> List[Timeline]:
        """List all timeline branches"""
        return [
            t for t in self.snapshot_manager.timelines.values()
            if t.parent_timeline_id is not None
        ]

    def get_branch_tree(self) -> Dict[str, List[str]]:
        """
        Get tree structure of timeline branches.

        Returns:
            Dict mapping parent timeline IDs to child timeline IDs
        """
        tree: Dict[str, List[str]] = {}

        for timeline in self.snapshot_manager.timelines.values():
            if timeline.parent_timeline_id:
                if timeline.parent_timeline_id not in tree:
                    tree[timeline.parent_timeline_id] = []
                tree[timeline.parent_timeline_id].append(timeline.timeline_id)

        return tree