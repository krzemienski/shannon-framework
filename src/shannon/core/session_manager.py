"""Session management and context storage"""

from pathlib import Path
from typing import Optional, Dict, Any, List
import json
from datetime import datetime


class SessionManager:
    """
    File-based session storage (replaces Serena MCP)

    Storage: ~/.shannon/sessions/{session_id}/
    Format: Individual JSON files per memory key

    API compatibility with Serena MCP:
    - write_memory(key, data) → Save JSON
    - read_memory(key) → Load JSON
    - list_memories() → List all keys
    - has_memory(key) → Check exists
    """

    def __init__(self, session_id: str):
        """
        Initialize session manager

        Args:
            session_id: Unique session identifier
        """
        self.session_id = session_id
        self.session_dir = Path.home() / ".shannon" / "sessions" / session_id
        self.session_dir.mkdir(parents=True, exist_ok=True)

        # Metadata file
        self.metadata_file = self.session_dir / "session.json"
        self._load_or_create_metadata()

    def _load_or_create_metadata(self):
        """Load existing metadata or create new"""
        if self.metadata_file.exists():
            with open(self.metadata_file) as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {
                "session_id": self.session_id,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "project_name": None,
                "keys": [],
            }
            self._save_metadata()

    def _save_metadata(self):
        """Persist metadata"""
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def write_memory(self, key: str, data: Dict[str, Any]) -> None:
        """
        Save data to session storage

        Args:
            key: Memory key (e.g., 'spec_analysis', 'wave_1_complete')
            data: JSON-serializable data

        Storage: {session_dir}/{key}.json
        """
        memory_file = self.session_dir / f"{key}.json"

        with open(memory_file, "w") as f:
            json.dump(data, f, indent=2)

        # Update metadata
        self.metadata["updated_at"] = datetime.now().isoformat()
        if key not in self.metadata["keys"]:
            self.metadata["keys"].append(key)
        self._save_metadata()

    def read_memory(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Load data from session storage

        Args:
            key: Memory key

        Returns:
            Data dict or None if not found
        """
        memory_file = self.session_dir / f"{key}.json"

        if not memory_file.exists():
            return None

        with open(memory_file) as f:
            return json.load(f)

    def list_memories(self) -> List[str]:
        """List all memory keys in session"""
        return self.metadata.get("keys", [])

    def has_memory(self, key: str) -> bool:
        """Check if memory key exists"""
        return (self.session_dir / f"{key}.json").exists()

    @staticmethod
    def list_all_sessions() -> List[str]:
        """List all session IDs"""
        sessions_dir = Path.home() / ".shannon" / "sessions"
        if not sessions_dir.exists():
            return []
        return [d.name for d in sessions_dir.iterdir() if d.is_dir()]
