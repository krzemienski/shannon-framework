"""
Shannon Framework v4 - Context Manager Models

Data structures for context preservation and session management.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path


class CheckpointType(Enum):
    """Types of checkpoints."""
    MANUAL = "manual"           # User-initiated
    AUTO = "auto"               # Automatic periodic
    PRE_WAVE = "pre_wave"       # Before wave execution
    POST_WAVE = "post_wave"     # After wave completion
    PRE_PHASE = "pre_phase"     # Before phase start
    POST_PHASE = "post_phase"   # After phase completion
    ERROR = "error"             # On error/failure


class StorageBackend(Enum):
    """Storage backend types."""
    SERENA = "serena"           # Serena MCP (preferred)
    LOCAL = "local"             # Local filesystem
    MEMORY = "memory"           # In-memory only


@dataclass
class ContextData:
    """Context data to preserve."""
    # Specification
    specification: Optional[Dict[str, Any]] = None

    # Active skills
    active_skills: List[str] = field(default_factory=list)
    skill_states: Dict[str, Any] = field(default_factory=dict)

    # Execution state
    current_phase: Optional[int] = None
    current_wave: Optional[int] = None
    completed_phases: List[int] = field(default_factory=list)
    completed_waves: List[int] = field(default_factory=list)

    # Tasks and progress
    task_states: Dict[str, Any] = field(default_factory=dict)
    execution_history: List[Dict[str, Any]] = field(default_factory=list)

    # SITREPs
    sitreps: List[Dict[str, Any]] = field(default_factory=list)

    # Files and artifacts
    generated_files: List[str] = field(default_factory=list)
    artifacts: Dict[str, str] = field(default_factory=dict)

    # Metrics
    metrics: Dict[str, Any] = field(default_factory=dict)

    # Custom data
    custom: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'specification': self.specification,
            'active_skills': self.active_skills,
            'skill_states': self.skill_states,
            'current_phase': self.current_phase,
            'current_wave': self.current_wave,
            'completed_phases': self.completed_phases,
            'completed_waves': self.completed_waves,
            'task_states': self.task_states,
            'execution_history': self.execution_history,
            'sitreps': self.sitreps,
            'generated_files': self.generated_files,
            'artifacts': self.artifacts,
            'metrics': self.metrics,
            'custom': self.custom,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextData':
        """Create from dictionary."""
        return cls(
            specification=data.get('specification'),
            active_skills=data.get('active_skills', []),
            skill_states=data.get('skill_states', {}),
            current_phase=data.get('current_phase'),
            current_wave=data.get('current_wave'),
            completed_phases=data.get('completed_phases', []),
            completed_waves=data.get('completed_waves', []),
            task_states=data.get('task_states', {}),
            execution_history=data.get('execution_history', []),
            sitreps=data.get('sitreps', []),
            generated_files=data.get('generated_files', []),
            artifacts=data.get('artifacts', {}),
            metrics=data.get('metrics', {}),
            custom=data.get('custom', {}),
        )


@dataclass
class Checkpoint:
    """Checkpoint containing saved context."""
    id: str
    checkpoint_type: CheckpointType
    timestamp: datetime
    context: ContextData

    # Metadata
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    parent_checkpoint: Optional[str] = None

    # Storage
    storage_backend: StorageBackend = StorageBackend.LOCAL
    storage_path: Optional[str] = None

    # Verification
    checksum: Optional[str] = None
    verified: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'checkpoint_type': self.checkpoint_type.value,
            'timestamp': self.timestamp.isoformat(),
            'context': self.context.to_dict(),
            'description': self.description,
            'tags': self.tags,
            'parent_checkpoint': self.parent_checkpoint,
            'storage_backend': self.storage_backend.value,
            'storage_path': self.storage_path,
            'checksum': self.checksum,
            'verified': self.verified,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Checkpoint':
        """Create from dictionary."""
        return cls(
            id=data['id'],
            checkpoint_type=CheckpointType(data['checkpoint_type']),
            timestamp=datetime.fromisoformat(data['timestamp']),
            context=ContextData.from_dict(data['context']),
            description=data.get('description'),
            tags=data.get('tags', []),
            parent_checkpoint=data.get('parent_checkpoint'),
            storage_backend=StorageBackend(data.get('storage_backend', 'local')),
            storage_path=data.get('storage_path'),
            checksum=data.get('checksum'),
            verified=data.get('verified', False),
        )


@dataclass
class Session:
    """Session containing multiple checkpoints."""
    id: str
    name: str
    created_at: datetime
    updated_at: datetime

    # Checkpoints
    checkpoints: List[str] = field(default_factory=list)  # Checkpoint IDs
    current_checkpoint: Optional[str] = None

    # Session metadata
    specification_title: Optional[str] = None
    total_phases: int = 0
    completed_phases: int = 0

    # Storage
    storage_backend: StorageBackend = StorageBackend.LOCAL
    storage_path: Optional[Path] = None

    # Session state
    active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'checkpoints': self.checkpoints,
            'current_checkpoint': self.current_checkpoint,
            'specification_title': self.specification_title,
            'total_phases': self.total_phases,
            'completed_phases': self.completed_phases,
            'storage_backend': self.storage_backend.value,
            'storage_path': str(self.storage_path) if self.storage_path else None,
            'active': self.active,
            'metadata': self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Session':
        """Create from dictionary."""
        storage_path = data.get('storage_path')
        if storage_path:
            storage_path = Path(storage_path)

        return cls(
            id=data['id'],
            name=data['name'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            checkpoints=data.get('checkpoints', []),
            current_checkpoint=data.get('current_checkpoint'),
            specification_title=data.get('specification_title'),
            total_phases=data.get('total_phases', 0),
            completed_phases=data.get('completed_phases', 0),
            storage_backend=StorageBackend(data.get('storage_backend', 'local')),
            storage_path=storage_path,
            active=data.get('active', True),
            metadata=data.get('metadata', {}),
        )


@dataclass
class RestoreResult:
    """Result of context restoration."""
    success: bool
    checkpoint: Optional[Checkpoint] = None
    context: Optional[ContextData] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    restored_files: List[str] = field(default_factory=list)
