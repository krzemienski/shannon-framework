"""
Shannon Framework v4 - Context & Session Manager

Purpose: Context preservation with checkpoint/restore and session management.

Components:
  - ContextManager: Checkpoint/restore operations
  - SessionManager: Session lifecycle management
  - Storage: Serena MCP + local fallback
  - Models: Checkpoint, Session, ContextData

Checkpoint Types:
  - MANUAL: User-initiated
  - AUTO: Automatic periodic
  - PRE_WAVE/POST_WAVE: Wave boundaries
  - PRE_PHASE/POST_PHASE: Phase boundaries
  - ERROR: On failure

Storage Backends:
  - Serena MCP: Zero-context-loss preservation (preferred)
  - Local: Filesystem fallback (.shannon/checkpoints/)
  - Memory: Testing/temporary

Author: Shannon Framework Team
Version: 1.0.0
License: MIT
"""

from .models import (
    Checkpoint,
    CheckpointType,
    ContextData,
    Session,
    StorageBackend,
    RestoreResult,
)
from .storage import (
    CheckpointStorage,
    LocalStorage,
    SerenaStorage,
    MemoryStorage,
    StorageError,
)
from .manager import (
    ContextManager,
    SessionManager,
)

__all__ = [
    # Managers
    'ContextManager',
    'SessionManager',

    # Models
    'Checkpoint',
    'CheckpointType',
    'ContextData',
    'Session',
    'StorageBackend',
    'RestoreResult',

    # Storage
    'CheckpointStorage',
    'LocalStorage',
    'SerenaStorage',
    'MemoryStorage',
    'StorageError',
]

__version__ = '1.0.0'


# Convenience functions

def create_context_manager(
    backend: str = "local",
    serena_client=None
) -> ContextManager:
    """
    Create context manager with specified backend.

    Args:
        backend: Storage backend (local, serena, memory)
        serena_client: Serena MCP client (for serena backend)

    Returns:
        ContextManager instance
    """
    return ContextManager(
        storage_backend=backend,
        serena_client=serena_client
    )


def create_session_manager(
    backend: str = "local",
    serena_client=None
) -> SessionManager:
    """
    Create session manager with specified backend.

    Args:
        backend: Storage backend (local, serena, memory)
        serena_client: Serena MCP client

    Returns:
        SessionManager instance
    """
    return SessionManager(
        storage_backend=backend,
        serena_client=serena_client
    )
