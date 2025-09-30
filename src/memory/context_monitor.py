"""
Context Monitor and Manual Checkpoint System

Implements token usage tracking, alert system, and manual context management
for Shannon framework v2.1.

Features:
- Real-time token usage monitoring
- 4-level alert system (GREEN, YELLOW, ORANGE, RED)
- Manual checkpoint management
- Serena MCP memory key tracking
"""

import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class AlertLevel(Enum):
    """Context usage alert levels."""
    GREEN = "green"      # 0-60%
    YELLOW = "yellow"    # 60-75%
    ORANGE = "orange"    # 75-85%
    RED = "red"          # 85-95%
    CRITICAL = "critical"  # 95%+


@dataclass
class ContextSnapshot:
    """Snapshot of context state at a point in time."""

    timestamp: float
    tokens_used: int
    tokens_limit: int
    usage_percent: float
    alert_level: AlertLevel
    active_memories: List[str]
    serena_keys: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "timestamp": self.timestamp,
            "tokens_used": self.tokens_used,
            "tokens_limit": self.tokens_limit,
            "usage_percent": self.usage_percent,
            "alert_level": self.alert_level.value,
            "active_memories": self.active_memories,
            "serena_keys": self.serena_keys,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContextSnapshot":
        """Deserialize from dictionary."""
        return cls(
            timestamp=data["timestamp"],
            tokens_used=data["tokens_used"],
            tokens_limit=data["tokens_limit"],
            usage_percent=data["usage_percent"],
            alert_level=AlertLevel(data["alert_level"]),
            active_memories=data["active_memories"],
            serena_keys=data["serena_keys"],
            metadata=data.get("metadata", {})
        )


@dataclass
class Checkpoint:
    """Manual checkpoint with context preservation."""

    checkpoint_id: str
    timestamp: float
    description: str
    context_snapshot: ContextSnapshot
    serena_memory_keys: List[str]
    wave_state: Dict[str, Any]
    user_notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "checkpoint_id": self.checkpoint_id,
            "timestamp": self.timestamp,
            "description": self.description,
            "context_snapshot": self.context_snapshot.to_dict(),
            "serena_memory_keys": self.serena_memory_keys,
            "wave_state": self.wave_state,
            "user_notes": self.user_notes
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Checkpoint":
        """Deserialize from dictionary."""
        return cls(
            checkpoint_id=data["checkpoint_id"],
            timestamp=data["timestamp"],
            description=data["description"],
            context_snapshot=ContextSnapshot.from_dict(data["context_snapshot"]),
            serena_memory_keys=data["serena_memory_keys"],
            wave_state=data["wave_state"],
            user_notes=data.get("user_notes", "")
        )


class ContextMonitor:
    """
    Monitor token usage and provide real-time alerts.

    Alert Levels:
    - GREEN (0-60%): Normal operation
    - YELLOW (60-75%): Resource optimization suggested
    - ORANGE (75-85%): Warning alerts active
    - RED (85-95%): Force efficiency modes
    - CRITICAL (95%+): Emergency protocols
    """

    def __init__(self, tokens_limit: int = 200000, storage_path: Optional[Path] = None):
        """
        Initialize context monitor.

        Args:
            tokens_limit: Maximum token budget
            storage_path: Path for persistent storage
        """
        self.tokens_limit = tokens_limit
        self.tokens_used = 0
        self.storage_path = storage_path or Path.home() / ".shannon" / "context"
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # Alert thresholds
        self.thresholds = {
            AlertLevel.GREEN: 0.60,
            AlertLevel.YELLOW: 0.75,
            AlertLevel.ORANGE: 0.85,
            AlertLevel.RED: 0.95
        }

        # Current state
        self.current_alert_level = AlertLevel.GREEN
        self.active_memories: Set[str] = set()
        self.serena_keys: Set[str] = set()

        # History
        self.usage_history: List[ContextSnapshot] = []
        self.alert_history: List[Tuple[float, AlertLevel, str]] = []

        # Callbacks for alert level changes
        self.alert_callbacks: Dict[AlertLevel, List[callable]] = {
            level: [] for level in AlertLevel
        }

    def update_usage(self, tokens_used: int):
        """
        Update token usage and check alert levels.

        Args:
            tokens_used: Current token count
        """
        self.tokens_used = tokens_used
        usage_percent = tokens_used / self.tokens_limit

        # Determine alert level
        new_level = self._calculate_alert_level(usage_percent)

        # Create snapshot
        snapshot = ContextSnapshot(
            timestamp=time.time(),
            tokens_used=tokens_used,
            tokens_limit=self.tokens_limit,
            usage_percent=usage_percent,
            alert_level=new_level,
            active_memories=list(self.active_memories),
            serena_keys=list(self.serena_keys)
        )
        self.usage_history.append(snapshot)

        # Check for alert level change
        if new_level != self.current_alert_level:
            self._trigger_alert_change(new_level)
            self.current_alert_level = new_level

    def _calculate_alert_level(self, usage_percent: float) -> AlertLevel:
        """
        Calculate alert level from usage percentage.

        Args:
            usage_percent: Token usage as percentage (0.0-1.0)

        Returns:
            Alert level
        """
        if usage_percent >= 0.95:
            return AlertLevel.CRITICAL
        elif usage_percent >= self.thresholds[AlertLevel.RED]:
            return AlertLevel.RED
        elif usage_percent >= self.thresholds[AlertLevel.ORANGE]:
            return AlertLevel.ORANGE
        elif usage_percent >= self.thresholds[AlertLevel.YELLOW]:
            return AlertLevel.YELLOW
        else:
            return AlertLevel.GREEN

    def _trigger_alert_change(self, new_level: AlertLevel):
        """
        Trigger callbacks for alert level change.

        Args:
            new_level: New alert level
        """
        timestamp = time.time()
        message = f"Alert level changed to {new_level.value} ({self.get_usage_percent():.1f}% usage)"

        self.alert_history.append((timestamp, new_level, message))

        # Execute registered callbacks
        for callback in self.alert_callbacks.get(new_level, []):
            try:
                callback(new_level, self.get_usage_percent())
            except Exception as e:
                print(f"Error in alert callback: {e}")

    def register_alert_callback(self, level: AlertLevel, callback: callable):
        """
        Register callback for specific alert level.

        Args:
            level: Alert level to trigger on
            callback: Function to call (receives level and usage_percent)
        """
        self.alert_callbacks[level].append(callback)

    def add_memory_reference(self, memory_key: str):
        """
        Track active memory reference.

        Args:
            memory_key: Memory identifier
        """
        self.active_memories.add(memory_key)

    def remove_memory_reference(self, memory_key: str):
        """
        Remove memory reference.

        Args:
            memory_key: Memory identifier
        """
        self.active_memories.discard(memory_key)

    def add_serena_key(self, serena_key: str):
        """
        Track Serena MCP memory key for context preservation.

        Args:
            serena_key: Serena memory key
        """
        self.serena_keys.add(serena_key)

    def get_usage_percent(self) -> float:
        """Get current usage percentage."""
        return (self.tokens_used / self.tokens_limit) * 100

    def get_remaining_tokens(self) -> int:
        """Get remaining token budget."""
        return max(0, self.tokens_limit - self.tokens_used)

    def get_current_snapshot(self) -> ContextSnapshot:
        """Get current context snapshot."""
        return ContextSnapshot(
            timestamp=time.time(),
            tokens_used=self.tokens_used,
            tokens_limit=self.tokens_limit,
            usage_percent=self.tokens_used / self.tokens_limit,
            alert_level=self.current_alert_level,
            active_memories=list(self.active_memories),
            serena_keys=list(self.serena_keys)
        )

    def get_recommendations(self) -> List[str]:
        """
        Get optimization recommendations based on current usage.

        Returns:
            List of recommendations
        """
        recommendations = []
        usage_percent = self.get_usage_percent()

        if self.current_alert_level == AlertLevel.CRITICAL:
            recommendations.extend([
                "CRITICAL: Emergency protocols activated",
                "Force enable --uc mode for all responses",
                "Defer all non-critical operations",
                "Consider manual checkpoint and context reset"
            ])
        elif self.current_alert_level == AlertLevel.RED:
            recommendations.extend([
                "Force efficiency modes active",
                "Block resource-intensive operations",
                "Enable --uc mode automatically",
                "Create checkpoint before proceeding"
            ])
        elif self.current_alert_level == AlertLevel.ORANGE:
            recommendations.extend([
                "Warning: Approaching capacity",
                "Defer non-critical operations",
                "Consider checkpoint creation",
                "Enable caching for repeated operations"
            ])
        elif self.current_alert_level == AlertLevel.YELLOW:
            recommendations.extend([
                "Resource optimization suggested",
                "Enable caching strategies",
                "Consider --uc mode for verbose operations"
            ])

        # Memory-specific recommendations
        if len(self.active_memories) > 10:
            recommendations.append(f"Consider consolidating {len(self.active_memories)} active memories")

        return recommendations

    def get_stats(self) -> Dict[str, Any]:
        """
        Get monitoring statistics.

        Returns:
            Statistics dictionary
        """
        return {
            "current": {
                "tokens_used": self.tokens_used,
                "tokens_limit": self.tokens_limit,
                "usage_percent": self.get_usage_percent(),
                "remaining": self.get_remaining_tokens(),
                "alert_level": self.current_alert_level.value
            },
            "memories": {
                "active_count": len(self.active_memories),
                "serena_keys_count": len(self.serena_keys)
            },
            "history": {
                "snapshots_count": len(self.usage_history),
                "alerts_count": len(self.alert_history),
                "alert_breakdown": self._count_alerts_by_level()
            }
        }

    def _count_alerts_by_level(self) -> Dict[str, int]:
        """Count alerts by level."""
        counts = {level.value: 0 for level in AlertLevel}
        for _, level, _ in self.alert_history:
            counts[level.value] += 1
        return counts

    def save_state(self):
        """Save monitoring state to disk."""
        state = {
            "tokens_limit": self.tokens_limit,
            "tokens_used": self.tokens_used,
            "current_alert_level": self.current_alert_level.value,
            "active_memories": list(self.active_memories),
            "serena_keys": list(self.serena_keys),
            "usage_history": [s.to_dict() for s in self.usage_history[-100:]],  # Last 100 snapshots
            "alert_history": [
                {"timestamp": t, "level": l.value, "message": m}
                for t, l, m in self.alert_history[-50:]  # Last 50 alerts
            ]
        }

        state_file = self.storage_path / "monitor_state.json"
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def load_state(self):
        """Load monitoring state from disk."""
        state_file = self.storage_path / "monitor_state.json"
        if not state_file.exists():
            return

        with open(state_file, 'r') as f:
            state = json.load(f)

        self.tokens_limit = state.get("tokens_limit", self.tokens_limit)
        self.tokens_used = state.get("tokens_used", 0)
        self.current_alert_level = AlertLevel(state.get("current_alert_level", "green"))
        self.active_memories = set(state.get("active_memories", []))
        self.serena_keys = set(state.get("serena_keys", []))

        # Restore history
        self.usage_history = [
            ContextSnapshot.from_dict(s) for s in state.get("usage_history", [])
        ]
        self.alert_history = [
            (item["timestamp"], AlertLevel(item["level"]), item["message"])
            for item in state.get("alert_history", [])
        ]


class ManualCheckpointManager:
    """
    Manages manual checkpoints with context preservation.

    Critical for v2.1: Enables manual context management through
    explicit checkpoint creation and restoration.
    """

    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize checkpoint manager.

        Args:
            storage_path: Path for checkpoint storage
        """
        self.storage_path = storage_path or Path.home() / ".shannon" / "checkpoints"
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.checkpoints: Dict[str, Checkpoint] = {}
        self.load_checkpoints()

    def create_checkpoint(
        self,
        checkpoint_id: str,
        description: str,
        context_monitor: ContextMonitor,
        wave_state: Optional[Dict[str, Any]] = None,
        user_notes: str = ""
    ) -> Checkpoint:
        """
        Create manual checkpoint.

        Args:
            checkpoint_id: Unique checkpoint identifier
            description: Checkpoint description
            context_monitor: Context monitor instance
            wave_state: Optional wave execution state
            user_notes: Optional user notes

        Returns:
            Created checkpoint
        """
        snapshot = context_monitor.get_current_snapshot()

        checkpoint = Checkpoint(
            checkpoint_id=checkpoint_id,
            timestamp=time.time(),
            description=description,
            context_snapshot=snapshot,
            serena_memory_keys=list(context_monitor.serena_keys),
            wave_state=wave_state or {},
            user_notes=user_notes
        )

        self.checkpoints[checkpoint_id] = checkpoint
        self._save_checkpoint(checkpoint)

        return checkpoint

    def get_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """
        Retrieve checkpoint by ID.

        Args:
            checkpoint_id: Checkpoint identifier

        Returns:
            Checkpoint if found, None otherwise
        """
        return self.checkpoints.get(checkpoint_id)

    def list_checkpoints(self) -> List[Checkpoint]:
        """List all checkpoints sorted by timestamp."""
        return sorted(
            self.checkpoints.values(),
            key=lambda c: c.timestamp,
            reverse=True
        )

    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """
        Delete checkpoint.

        Args:
            checkpoint_id: Checkpoint identifier

        Returns:
            True if deleted, False if not found
        """
        if checkpoint_id in self.checkpoints:
            del self.checkpoints[checkpoint_id]
            checkpoint_file = self.storage_path / f"{checkpoint_id}.json"
            if checkpoint_file.exists():
                checkpoint_file.unlink()
            return True
        return False

    def get_restoration_instructions(self, checkpoint_id: str) -> Optional[str]:
        """
        Get instructions for restoring from checkpoint.

        Args:
            checkpoint_id: Checkpoint identifier

        Returns:
            Restoration instructions
        """
        checkpoint = self.get_checkpoint(checkpoint_id)
        if not checkpoint:
            return None

        instructions = f"""
# Checkpoint Restoration: {checkpoint.checkpoint_id}

**Created**: {datetime.fromtimestamp(checkpoint.timestamp).isoformat()}
**Description**: {checkpoint.description}

## Context State
- Tokens Used: {checkpoint.context_snapshot.tokens_used:,} / {checkpoint.context_snapshot.tokens_limit:,}
- Usage: {checkpoint.context_snapshot.usage_percent:.1%}
- Alert Level: {checkpoint.context_snapshot.alert_level.value}

## Serena Memory Keys
To restore context, use these Serena MCP keys:
{chr(10).join(f'- {key}' for key in checkpoint.serena_memory_keys)}

## Wave State
{json.dumps(checkpoint.wave_state, indent=2)}

## User Notes
{checkpoint.user_notes}

## Restoration Commands
```python
# Load Serena memories
for key in {checkpoint.serena_memory_keys}:
    memory = serena.read_memory(key)
    # Process memory content

# Restore wave state (if applicable)
wave_state = {json.dumps(checkpoint.wave_state)}
```
"""
        return instructions

    def _save_checkpoint(self, checkpoint: Checkpoint):
        """Save checkpoint to disk."""
        checkpoint_file = self.storage_path / f"{checkpoint.checkpoint_id}.json"
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint.to_dict(), f, indent=2)

    def load_checkpoints(self):
        """Load all checkpoints from disk."""
        for checkpoint_file in self.storage_path.glob("*.json"):
            try:
                with open(checkpoint_file, 'r') as f:
                    data = json.load(f)
                checkpoint = Checkpoint.from_dict(data)
                self.checkpoints[checkpoint.checkpoint_id] = checkpoint
            except Exception as e:
                print(f"Error loading checkpoint {checkpoint_file}: {e}")


class SerenaReferenceTracker:
    """
    Tracks Serena MCP memory keys for context preservation.

    Critical for v2.1: Enables accurate context restoration by
    maintaining exact references to Serena memory storage.
    """

    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize reference tracker.

        Args:
            storage_path: Path for reference storage
        """
        self.storage_path = storage_path or Path.home() / ".shannon" / "serena_refs"
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # Track active references
        self.active_references: Dict[str, Dict[str, Any]] = {}
        self.reference_metadata: Dict[str, List[str]] = {}  # key -> [memory_keys]

    def register_reference(
        self,
        reference_key: str,
        serena_memory_keys: List[str],
        context: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Register Serena memory reference.

        Args:
            reference_key: Unique reference identifier
            serena_memory_keys: List of Serena memory keys
            context: Context description
            metadata: Optional metadata
        """
        self.active_references[reference_key] = {
            "serena_keys": serena_memory_keys,
            "context": context,
            "timestamp": time.time(),
            "metadata": metadata or {}
        }

        # Update reverse mapping
        for key in serena_memory_keys:
            if key not in self.reference_metadata:
                self.reference_metadata[key] = []
            self.reference_metadata[key].append(reference_key)

    def get_serena_keys(self, reference_key: str) -> List[str]:
        """
        Get Serena memory keys for reference.

        Args:
            reference_key: Reference identifier

        Returns:
            List of Serena memory keys
        """
        ref = self.active_references.get(reference_key)
        return ref["serena_keys"] if ref else []

    def get_all_serena_keys(self) -> Set[str]:
        """Get all active Serena memory keys."""
        all_keys = set()
        for ref in self.active_references.values():
            all_keys.update(ref["serena_keys"])
        return all_keys

    def remove_reference(self, reference_key: str):
        """
        Remove reference tracking.

        Args:
            reference_key: Reference identifier
        """
        if reference_key in self.active_references:
            del self.active_references[reference_key]

    def save_references(self):
        """Save references to disk."""
        state_file = self.storage_path / "references.json"
        with open(state_file, 'w') as f:
            json.dump({
                "active_references": self.active_references,
                "reference_metadata": self.reference_metadata
            }, f, indent=2)

    def load_references(self):
        """Load references from disk."""
        state_file = self.storage_path / "references.json"
        if not state_file.exists():
            return

        with open(state_file, 'r') as f:
            state = json.load(f)

        self.active_references = state.get("active_references", {})
        self.reference_metadata = state.get("reference_metadata", {})