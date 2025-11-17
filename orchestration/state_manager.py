"""
State Manager - Handles execution state snapshots and rollback

Provides snapshot functionality for rollback operations.
"""

import time
import copy
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class StateSnapshot:
    """Represents a snapshot of execution state at a point in time"""

    def __init__(self, wave_index: int, execution_history: List[Dict], waves_state: List[Dict]):
        self.wave_index = wave_index
        self.execution_history = copy.deepcopy(execution_history)
        self.waves_state = copy.deepcopy(waves_state)
        self.timestamp = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "wave_index": self.wave_index,
            "execution_history_length": len(self.execution_history),
            "waves_count": len(self.waves_state),
            "timestamp": self.timestamp
        }


class StateManager:
    """
    Manages execution state snapshots for rollback capability.

    Features:
    - create_snapshot(): Save current execution state
    - get_snapshot(n): Get snapshot from N steps ago
    - rollback(n): Restore state from N steps ago
    """

    def __init__(self):
        self.snapshots: List[StateSnapshot] = []
        self.max_snapshots = 100  # Keep last 100 snapshots

    def create_snapshot(self, wave_index: int, execution_history: List[Dict],
                       waves: List[Any]) -> StateSnapshot:
        """
        Create a snapshot of current execution state.

        Args:
            wave_index: Current wave index being executed
            execution_history: List of execution history records
            waves: List of Wave objects

        Returns:
            StateSnapshot object
        """
        # Convert waves to serializable format
        waves_state = [w.to_dict() for w in waves]

        snapshot = StateSnapshot(wave_index, execution_history, waves_state)
        self.snapshots.append(snapshot)

        # Trim old snapshots if exceeding max
        if len(self.snapshots) > self.max_snapshots:
            self.snapshots = self.snapshots[-self.max_snapshots:]

        logger.info(f"Created snapshot at wave {wave_index} (total snapshots: {len(self.snapshots)})")
        return snapshot

    def get_snapshot(self, steps_back: int) -> Optional[StateSnapshot]:
        """
        Get snapshot from N steps back.

        Args:
            steps_back: Number of steps to go back (1 = previous snapshot)

        Returns:
            StateSnapshot if found, None otherwise
        """
        if steps_back < 1 or steps_back > len(self.snapshots):
            logger.warning(f"Cannot get snapshot {steps_back} steps back (only {len(self.snapshots)} available)")
            return None

        # Get snapshot from the end (most recent) going backward
        index = len(self.snapshots) - steps_back
        return self.snapshots[index]

    def get_rollback_state(self, steps_back: int) -> Optional[Dict[str, Any]]:
        """
        Get the state to rollback to.

        Args:
            steps_back: Number of steps to rollback

        Returns:
            Dict with wave_index, execution_history, and waves_state
        """
        snapshot = self.get_snapshot(steps_back)
        if snapshot is None:
            return None

        return {
            "wave_index": snapshot.wave_index,
            "execution_history": copy.deepcopy(snapshot.execution_history),
            "waves_state": copy.deepcopy(snapshot.waves_state),
            "snapshot_timestamp": snapshot.timestamp
        }

    def clear_snapshots(self) -> None:
        """Clear all snapshots"""
        self.snapshots.clear()
        logger.info("Cleared all snapshots")

    def get_snapshot_count(self) -> int:
        """Get total number of snapshots"""
        return len(self.snapshots)

    def list_snapshots(self) -> List[Dict[str, Any]]:
        """List all snapshots with basic info"""
        return [
            {
                "index": i,
                "wave_index": snapshot.wave_index,
                "timestamp": snapshot.timestamp,
                "execution_history_length": len(snapshot.execution_history)
            }
            for i, snapshot in enumerate(self.snapshots)
        ]
