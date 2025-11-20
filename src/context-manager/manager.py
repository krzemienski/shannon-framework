"""
Shannon Framework v4 - Context Manager

Manages context preservation with checkpoint/restore capabilities.
"""

import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime
from pathlib import Path

from .models import (
    Checkpoint, CheckpointType, ContextData, RestoreResult,
    Session, StorageBackend
)
from .storage import (
    CheckpointStorage, LocalStorage, SerenaStorage, MemoryStorage,
    StorageError
)


class ContextManager:
    """
    Manages context preservation and restoration.

    Features:
    - Create checkpoints at key execution points
    - Restore context from checkpoints
    - Serena MCP integration with local fallback
    - Checkpoint verification and validation
    """

    def __init__(
        self,
        storage_backend: str = "local",
        serena_client=None,
        base_dir: Path = None
    ):
        """
        Initialize context manager.

        Args:
            storage_backend: Backend type (local, serena, memory)
            serena_client: Serena MCP client (for serena backend)
            base_dir: Base directory for local storage
        """
        self.storage = self._init_storage(storage_backend, serena_client, base_dir)
        self.current_context = ContextData()
        self.current_checkpoint: Optional[Checkpoint] = None

    def _init_storage(
        self,
        backend: str,
        serena_client,
        base_dir: Path
    ) -> CheckpointStorage:
        """Initialize storage backend."""
        if backend == "serena":
            return SerenaStorage(serena_client=serena_client)
        elif backend == "memory":
            return MemoryStorage()
        else:  # local
            return LocalStorage(base_dir=base_dir)

    def create_checkpoint(
        self,
        checkpoint_type: CheckpointType = CheckpointType.MANUAL,
        description: str = None,
        tags: List[str] = None
    ) -> Checkpoint:
        """
        Create checkpoint from current context.

        Args:
            checkpoint_type: Type of checkpoint
            description: Optional description
            tags: Optional tags

        Returns:
            Created checkpoint
        """
        checkpoint_id = f"checkpoint_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

        checkpoint = Checkpoint(
            id=checkpoint_id,
            checkpoint_type=checkpoint_type,
            timestamp=datetime.now(),
            context=self.current_context,
            description=description,
            tags=tags or [],
            parent_checkpoint=self.current_checkpoint.id if self.current_checkpoint else None
        )

        # Save to storage
        self.storage.save_checkpoint(checkpoint)

        # Update current checkpoint
        self.current_checkpoint = checkpoint

        return checkpoint

    def restore_checkpoint(self, checkpoint_id: str) -> RestoreResult:
        """
        Restore context from checkpoint.

        Args:
            checkpoint_id: ID of checkpoint to restore

        Returns:
            RestoreResult with success status and details
        """
        result = RestoreResult(success=False)

        try:
            # Load checkpoint
            checkpoint = self.storage.load_checkpoint(checkpoint_id)
            if not checkpoint:
                result.errors.append(f"Checkpoint '{checkpoint_id}' not found")
                return result

            # Verify checkpoint
            if not checkpoint.verified:
                result.warnings.append(f"Checkpoint verification failed - data may be corrupted")

            # Restore context
            self.current_context = checkpoint.context
            self.current_checkpoint = checkpoint

            result.success = True
            result.checkpoint = checkpoint
            result.context = checkpoint.context

            # Track what was restored
            if checkpoint.context.generated_files:
                result.restored_files = checkpoint.context.generated_files

        except StorageError as e:
            result.errors.append(f"Storage error: {e}")
        except Exception as e:
            result.errors.append(f"Unexpected error: {e}")

        return result

    def list_checkpoints(self, tags: List[str] = None) -> List[str]:
        """
        List available checkpoints.

        Args:
            tags: Optional tag filter

        Returns:
            List of checkpoint IDs
        """
        checkpoint_ids = self.storage.list_checkpoints()

        # Filter by tags if requested
        if tags:
            filtered = []
            for cp_id in checkpoint_ids:
                cp = self.storage.load_checkpoint(cp_id)
                if cp and any(tag in cp.tags for tag in tags):
                    filtered.append(cp_id)
            return filtered

        return checkpoint_ids

    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """
        Delete checkpoint.

        Args:
            checkpoint_id: ID of checkpoint to delete

        Returns:
            True if deleted successfully
        """
        return self.storage.delete_checkpoint(checkpoint_id)

    def get_checkpoint_info(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """
        Get checkpoint information.

        Args:
            checkpoint_id: Checkpoint ID

        Returns:
            Checkpoint info dictionary or None
        """
        checkpoint = self.storage.load_checkpoint(checkpoint_id)
        if not checkpoint:
            return None

        return {
            'id': checkpoint.id,
            'type': checkpoint.checkpoint_type.value,
            'timestamp': checkpoint.timestamp.isoformat(),
            'description': checkpoint.description,
            'tags': checkpoint.tags,
            'verified': checkpoint.verified,
            'phase': checkpoint.context.current_phase,
            'wave': checkpoint.context.current_wave,
            'active_skills': checkpoint.context.active_skills,
            'task_count': len(checkpoint.context.task_states),
        }

    def update_context(self, **kwargs):
        """
        Update current context with new data.

        Args:
            **kwargs: Context fields to update
        """
        for key, value in kwargs.items():
            if hasattr(self.current_context, key):
                setattr(self.current_context, key, value)

    def get_context(self) -> ContextData:
        """Get current context."""
        return self.current_context

    def auto_checkpoint(self, checkpoint_type: CheckpointType, description: str = None):
        """
        Create automatic checkpoint.

        Args:
            checkpoint_type: Type of auto checkpoint
            description: Optional description
        """
        return self.create_checkpoint(
            checkpoint_type=checkpoint_type,
            description=description,
            tags=['auto']
        )


class SessionManager:
    """
    Manages sessions containing multiple checkpoints.

    A session represents a complete execution from spec to completion.
    """

    def __init__(
        self,
        storage_backend: str = "local",
        serena_client=None,
        base_dir: Path = None
    ):
        """
        Initialize session manager.

        Args:
            storage_backend: Backend type
            serena_client: Serena MCP client
            base_dir: Base directory for storage
        """
        if base_dir is None:
            base_dir = Path.cwd() / '.shannon'

        self.base_dir = Path(base_dir)
        self.sessions_dir = self.base_dir / 'sessions'
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

        self.storage_backend = storage_backend
        self.serena_client = serena_client

        self.current_session: Optional[Session] = None
        self.context_manager: Optional[ContextManager] = None

    def create_session(
        self,
        name: str,
        specification_title: str = None,
        total_phases: int = 0
    ) -> Session:
        """
        Create new session.

        Args:
            name: Session name
            specification_title: Title of specification
            total_phases: Total number of phases

        Returns:
            Created session
        """
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        session_dir = self.sessions_dir / session_id

        session = Session(
            id=session_id,
            name=name,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            specification_title=specification_title,
            total_phases=total_phases,
            storage_path=session_dir
        )

        # Create session directory
        session_dir.mkdir(parents=True, exist_ok=True)

        # Save session metadata
        self._save_session(session)

        # Initialize context manager for this session
        self.current_session = session
        self.context_manager = ContextManager(
            storage_backend=self.storage_backend,
            serena_client=self.serena_client,
            base_dir=session_dir
        )

        return session

    def load_session(self, session_id: str) -> Session:
        """
        Load existing session.

        Args:
            session_id: Session ID to load

        Returns:
            Loaded session
        """
        session_file = self.sessions_dir / session_id / 'session.json'

        if not session_file.exists():
            raise ValueError(f"Session '{session_id}' not found")

        import json
        with open(session_file, 'r') as f:
            session_data = json.load(f)

        session = Session.from_dict(session_data)

        # Initialize context manager
        self.current_session = session
        self.context_manager = ContextManager(
            storage_backend=self.storage_backend,
            serena_client=self.serena_client,
            base_dir=session.storage_path
        )

        return session

    def checkpoint_session(
        self,
        checkpoint_type: CheckpointType = CheckpointType.MANUAL,
        description: str = None
    ) -> Checkpoint:
        """
        Create checkpoint in current session.

        Args:
            checkpoint_type: Type of checkpoint
            description: Optional description

        Returns:
            Created checkpoint
        """
        if not self.current_session:
            raise ValueError("No active session")

        checkpoint = self.context_manager.create_checkpoint(
            checkpoint_type=checkpoint_type,
            description=description
        )

        # Add to session
        self.current_session.checkpoints.append(checkpoint.id)
        self.current_session.current_checkpoint = checkpoint.id
        self.current_session.updated_at = datetime.now()

        # Update session progress from context
        context = self.context_manager.get_context()
        self.current_session.completed_phases = len(context.completed_phases)

        # Save session
        self._save_session(self.current_session)

        return checkpoint

    def restore_session_checkpoint(self, checkpoint_id: str) -> RestoreResult:
        """
        Restore checkpoint in current session.

        Args:
            checkpoint_id: Checkpoint ID to restore

        Returns:
            RestoreResult
        """
        if not self.current_session:
            raise ValueError("No active session")

        result = self.context_manager.restore_checkpoint(checkpoint_id)

        if result.success:
            self.current_session.current_checkpoint = checkpoint_id
            self.current_session.updated_at = datetime.now()
            self._save_session(self.current_session)

        return result

    def list_sessions(self, active_only: bool = False) -> List[Dict[str, Any]]:
        """
        List all sessions.

        Args:
            active_only: Only include active sessions

        Returns:
            List of session info dictionaries
        """
        sessions = []

        for session_dir in self.sessions_dir.iterdir():
            if not session_dir.is_dir():
                continue

            session_file = session_dir / 'session.json'
            if not session_file.exists():
                continue

            import json
            with open(session_file, 'r') as f:
                session_data = json.load(f)

            session = Session.from_dict(session_data)

            if active_only and not session.active:
                continue

            sessions.append({
                'id': session.id,
                'name': session.name,
                'specification_title': session.specification_title,
                'created_at': session.created_at.isoformat(),
                'updated_at': session.updated_at.isoformat(),
                'checkpoint_count': len(session.checkpoints),
                'progress': f"{session.completed_phases}/{session.total_phases}" if session.total_phases > 0 else "N/A",
                'active': session.active,
            })

        # Sort by updated_at descending
        sessions.sort(key=lambda s: s['updated_at'], reverse=True)

        return sessions

    def close_session(self):
        """Close current session."""
        if self.current_session:
            self.current_session.active = False
            self.current_session.updated_at = datetime.now()
            self._save_session(self.current_session)

            self.current_session = None
            self.context_manager = None

    def _save_session(self, session: Session):
        """Save session metadata to file."""
        import json
        session_file = session.storage_path / 'session.json'

        with open(session_file, 'w') as f:
            json.dump(session.to_dict(), f, indent=2)
