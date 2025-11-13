"""
Shannon Framework v4 - Context Storage Backends

Storage backends for checkpoint persistence.
"""

import json
import hashlib
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
from .models import Checkpoint, CheckpointType, StorageBackend


class StorageError(Exception):
    """Exception raised for storage operations."""
    pass


class CheckpointStorage(ABC):
    """Abstract base class for checkpoint storage."""

    @abstractmethod
    def save_checkpoint(self, checkpoint: Checkpoint) -> bool:
        """Save checkpoint to storage."""
        pass

    @abstractmethod
    def load_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """Load checkpoint from storage."""
        pass

    @abstractmethod
    def list_checkpoints(self) -> List[str]:
        """List all checkpoint IDs."""
        pass

    @abstractmethod
    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """Delete checkpoint from storage."""
        pass

    @abstractmethod
    def checkpoint_exists(self, checkpoint_id: str) -> bool:
        """Check if checkpoint exists."""
        pass

    def calculate_checksum(self, data: Dict[str, Any]) -> str:
        """Calculate checksum for verification."""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()


class LocalStorage(CheckpointStorage):
    """
    Local filesystem storage backend.

    Stores checkpoints as JSON files in .shannon/checkpoints/
    """

    def __init__(self, base_dir: Path = None):
        """
        Initialize local storage.

        Args:
            base_dir: Base directory for storage (default: .shannon)
        """
        if base_dir is None:
            base_dir = Path.cwd() / '.shannon'

        self.base_dir = Path(base_dir)
        self.checkpoints_dir = self.base_dir / 'checkpoints'
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)

    def save_checkpoint(self, checkpoint: Checkpoint) -> bool:
        """Save checkpoint to local file."""
        try:
            checkpoint_data = checkpoint.to_dict()

            # Calculate checksum
            checkpoint.checksum = self.calculate_checksum(checkpoint_data)
            checkpoint_data['checksum'] = checkpoint.checksum

            # Save to file
            filepath = self.checkpoints_dir / f"{checkpoint.id}.json"
            with open(filepath, 'w') as f:
                json.dump(checkpoint_data, f, indent=2)

            checkpoint.storage_path = str(filepath)
            checkpoint.storage_backend = StorageBackend.LOCAL
            checkpoint.verified = True

            return True

        except Exception as e:
            raise StorageError(f"Failed to save checkpoint {checkpoint.id}: {e}")

    def load_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """Load checkpoint from local file."""
        try:
            filepath = self.checkpoints_dir / f"{checkpoint_id}.json"

            if not filepath.exists():
                return None

            with open(filepath, 'r') as f:
                checkpoint_data = json.load(f)

            # Verify checksum
            stored_checksum = checkpoint_data.pop('checksum', None)
            calculated_checksum = self.calculate_checksum(checkpoint_data)

            checkpoint = Checkpoint.from_dict(checkpoint_data)
            checkpoint.checksum = stored_checksum
            checkpoint.verified = (stored_checksum == calculated_checksum)

            if not checkpoint.verified:
                print(f"Warning: Checkpoint {checkpoint_id} failed checksum verification")

            return checkpoint

        except Exception as e:
            raise StorageError(f"Failed to load checkpoint {checkpoint_id}: {e}")

    def list_checkpoints(self) -> List[str]:
        """List all checkpoint IDs."""
        checkpoint_files = self.checkpoints_dir.glob('*.json')
        return [f.stem for f in checkpoint_files]

    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """Delete checkpoint file."""
        try:
            filepath = self.checkpoints_dir / f"{checkpoint_id}.json"
            if filepath.exists():
                filepath.unlink()
                return True
            return False
        except Exception as e:
            raise StorageError(f"Failed to delete checkpoint {checkpoint_id}: {e}")

    def checkpoint_exists(self, checkpoint_id: str) -> bool:
        """Check if checkpoint file exists."""
        filepath = self.checkpoints_dir / f"{checkpoint_id}.json"
        return filepath.exists()

    def get_checkpoint_path(self, checkpoint_id: str) -> Path:
        """Get file path for checkpoint."""
        return self.checkpoints_dir / f"{checkpoint_id}.json"


class SerenaStorage(CheckpointStorage):
    """
    Serena MCP storage backend.

    Uses Serena MCP for context preservation with zero-context-loss.
    Falls back to local storage if Serena unavailable.
    """

    def __init__(self, serena_client=None, fallback_storage: CheckpointStorage = None):
        """
        Initialize Serena storage.

        Args:
            serena_client: Serena MCP client instance
            fallback_storage: Fallback storage (default: LocalStorage)
        """
        self.serena_client = serena_client
        self.fallback_storage = fallback_storage or LocalStorage()
        self.serena_available = self._check_serena_available()

    def _check_serena_available(self) -> bool:
        """Check if Serena MCP is available."""
        if not self.serena_client:
            return False

        try:
            # Simple health check
            # In real implementation, would call Serena's health endpoint
            return True
        except Exception:
            return False

    def save_checkpoint(self, checkpoint: Checkpoint) -> bool:
        """Save checkpoint to Serena or fallback."""
        if self.serena_available:
            try:
                return self._save_to_serena(checkpoint)
            except Exception as e:
                print(f"Warning: Serena save failed, using fallback: {e}")
                self.serena_available = False

        # Use fallback
        return self.fallback_storage.save_checkpoint(checkpoint)

    def load_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """Load checkpoint from Serena or fallback."""
        if self.serena_available:
            try:
                checkpoint = self._load_from_serena(checkpoint_id)
                if checkpoint:
                    return checkpoint
            except Exception as e:
                print(f"Warning: Serena load failed, using fallback: {e}")
                self.serena_available = False

        # Use fallback
        return self.fallback_storage.load_checkpoint(checkpoint_id)

    def list_checkpoints(self) -> List[str]:
        """List checkpoints from Serena or fallback."""
        if self.serena_available:
            try:
                return self._list_serena_checkpoints()
            except Exception:
                self.serena_available = False

        return self.fallback_storage.list_checkpoints()

    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """Delete checkpoint from Serena or fallback."""
        if self.serena_available:
            try:
                return self._delete_from_serena(checkpoint_id)
            except Exception:
                self.serena_available = False

        return self.fallback_storage.delete_checkpoint(checkpoint_id)

    def checkpoint_exists(self, checkpoint_id: str) -> bool:
        """Check if checkpoint exists in Serena or fallback."""
        if self.serena_available:
            try:
                return self._serena_checkpoint_exists(checkpoint_id)
            except Exception:
                self.serena_available = False

        return self.fallback_storage.checkpoint_exists(checkpoint_id)

    def _save_to_serena(self, checkpoint: Checkpoint) -> bool:
        """Save checkpoint to Serena MCP."""
        # In real implementation, would use Serena MCP API
        # For now, this is a placeholder that demonstrates the interface

        checkpoint_data = checkpoint.to_dict()

        # Calculate checksum
        checkpoint.checksum = self.calculate_checksum(checkpoint_data)
        checkpoint_data['checksum'] = checkpoint.checksum

        # Serena API call (placeholder)
        # self.serena_client.store_context(
        #     context_id=checkpoint.id,
        #     context_type="checkpoint",
        #     data=checkpoint_data
        # )

        checkpoint.storage_backend = StorageBackend.SERENA
        checkpoint.verified = True

        # Also save to fallback for redundancy
        self.fallback_storage.save_checkpoint(checkpoint)

        return True

    def _load_from_serena(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """Load checkpoint from Serena MCP."""
        # Serena API call (placeholder)
        # checkpoint_data = self.serena_client.retrieve_context(
        #     context_id=checkpoint_id,
        #     context_type="checkpoint"
        # )

        # For now, return None to trigger fallback
        return None

    def _list_serena_checkpoints(self) -> List[str]:
        """List checkpoints from Serena."""
        # Serena API call (placeholder)
        # return self.serena_client.list_contexts(context_type="checkpoint")

        # Use fallback
        return self.fallback_storage.list_checkpoints()

    def _delete_from_serena(self, checkpoint_id: str) -> bool:
        """Delete checkpoint from Serena."""
        # Serena API call (placeholder)
        # return self.serena_client.delete_context(
        #     context_id=checkpoint_id,
        #     context_type="checkpoint"
        # )

        # Use fallback
        return self.fallback_storage.delete_checkpoint(checkpoint_id)

    def _serena_checkpoint_exists(self, checkpoint_id: str) -> bool:
        """Check if checkpoint exists in Serena."""
        # Serena API call (placeholder)
        # return self.serena_client.context_exists(
        #     context_id=checkpoint_id,
        #     context_type="checkpoint"
        # )

        # Use fallback
        return self.fallback_storage.checkpoint_exists(checkpoint_id)


class MemoryStorage(CheckpointStorage):
    """
    In-memory storage backend.

    For testing and temporary checkpoints.
    """

    def __init__(self):
        """Initialize memory storage."""
        self.checkpoints: Dict[str, Checkpoint] = {}

    def save_checkpoint(self, checkpoint: Checkpoint) -> bool:
        """Save checkpoint to memory."""
        checkpoint_data = checkpoint.to_dict()
        checkpoint.checksum = self.calculate_checksum(checkpoint_data)
        checkpoint.storage_backend = StorageBackend.MEMORY
        checkpoint.verified = True

        self.checkpoints[checkpoint.id] = checkpoint
        return True

    def load_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """Load checkpoint from memory."""
        return self.checkpoints.get(checkpoint_id)

    def list_checkpoints(self) -> List[str]:
        """List all checkpoint IDs in memory."""
        return list(self.checkpoints.keys())

    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """Delete checkpoint from memory."""
        if checkpoint_id in self.checkpoints:
            del self.checkpoints[checkpoint_id]
            return True
        return False

    def checkpoint_exists(self, checkpoint_id: str) -> bool:
        """Check if checkpoint exists in memory."""
        return checkpoint_id in self.checkpoints

    def clear(self):
        """Clear all checkpoints from memory."""
        self.checkpoints = {}
