"""Shannon Orchestration - State Manager

Manages execution state through checkpoints for rollback capability.

The StateManager provides:
- Checkpoint creation before critical operations
- File system snapshots (only changed files)
- Git state capture
- Execution context preservation
- Rollback to any checkpoint
- Verification after restoration

Checkpoints are lightweight and only store:
- Changed files (not entire filesystem)
- Git state (HEAD, branch, status)
- Execution context (variables, results)
- Skill stack (execution history)

Example:
    manager = StateManager(project_root)

    # Create checkpoint
    checkpoint = await manager.create_checkpoint("before_code_gen")

    # ... do work ...

    # Rollback if needed
    await manager.restore_checkpoint(checkpoint.id)
"""

import asyncio
import hashlib
import json
import logging
import shutil
import subprocess
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Set

logger = logging.getLogger(__name__)


@dataclass
class GitState:
    """Captured git repository state"""
    branch: str
    commit: str
    status: str
    staged_files: List[str] = field(default_factory=list)
    modified_files: List[str] = field(default_factory=list)
    untracked_files: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'branch': self.branch,
            'commit': self.commit,
            'status': self.status,
            'staged_files': self.staged_files,
            'modified_files': self.modified_files,
            'untracked_files': self.untracked_files
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GitState':
        """Create from dictionary"""
        return cls(
            branch=data['branch'],
            commit=data['commit'],
            status=data['status'],
            staged_files=data.get('staged_files', []),
            modified_files=data.get('modified_files', []),
            untracked_files=data.get('untracked_files', [])
        )


@dataclass
class Checkpoint:
    """Execution checkpoint for rollback"""
    id: str
    label: str
    timestamp: datetime
    skill_stack: List[str]                    # Skills executed so far
    file_snapshots: Dict[str, str]            # path -> content hash
    file_contents: Dict[str, str]             # path -> actual content
    git_state: GitState
    execution_context: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'id': self.id,
            'label': self.label,
            'timestamp': self.timestamp.isoformat(),
            'skill_stack': self.skill_stack,
            'file_snapshots': self.file_snapshots,
            # Don't serialize file_contents - save separately for space
            'git_state': self.git_state.to_dict(),
            'execution_context': self.execution_context,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Checkpoint':
        """Create from dictionary"""
        return cls(
            id=data['id'],
            label=data['label'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            skill_stack=data['skill_stack'],
            file_snapshots=data['file_snapshots'],
            file_contents={},  # Loaded separately
            git_state=GitState.from_dict(data['git_state']),
            execution_context=data['execution_context'],
            metadata=data.get('metadata', {})
        )


class StateManagerError(Exception):
    """Base exception for state manager errors"""
    pass


class CheckpointNotFoundError(StateManagerError):
    """Raised when checkpoint doesn't exist"""
    pass


class RestoreError(StateManagerError):
    """Raised when restore fails"""
    pass


class StateManager:
    """
    Manages execution state and checkpoints for rollback.

    The StateManager enables safe experimentation by:
    1. Creating checkpoints before risky operations
    2. Capturing only changed files (not entire filesystem)
    3. Recording git state for version control awareness
    4. Preserving execution context across rollbacks
    5. Verifying restoration integrity

    Thread-safe and designed for async execution.

    Usage:
        manager = StateManager(project_root)

        # Create checkpoint
        checkpoint = await manager.create_checkpoint("initial")

        # Do work...

        # Restore if needed
        await manager.restore_checkpoint(checkpoint.id)

        # Verify restoration
        is_valid = await manager.verify_checkpoint(checkpoint.id)
    """

    def __init__(
        self,
        project_root: Path,
        checkpoint_dir: Optional[Path] = None
    ):
        """
        Initialize state manager.

        Args:
            project_root: Root directory of project
            checkpoint_dir: Directory to store checkpoints (default: .shannon/checkpoints)
        """
        self.project_root = Path(project_root).resolve()
        self.checkpoint_dir = checkpoint_dir or (self.project_root / '.shannon' / 'checkpoints')
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

        # In-memory tracking
        self.checkpoints: Dict[str, Checkpoint] = {}
        self.current_skill_stack: List[str] = []
        self.execution_context: Dict[str, Any] = {}
        self.tracked_files: Set[str] = set()  # Files we're tracking changes for

        # Lock for thread safety
        self.lock = asyncio.Lock()

        logger.info(f"StateManager initialized: {self.project_root}")

    async def create_checkpoint(
        self,
        label: str,
        skill_name: Optional[str] = None
    ) -> Checkpoint:
        """
        Create checkpoint of current state.

        Args:
            label: Human-readable checkpoint label
            skill_name: Optional skill name to add to stack

        Returns:
            Created checkpoint

        Raises:
            StateManagerError: If checkpoint creation fails
        """
        async with self.lock:
            checkpoint_id = str(uuid.uuid4())

            logger.info(f"Creating checkpoint: {label} (id={checkpoint_id})")

            try:
                # Update skill stack
                if skill_name:
                    self.current_skill_stack.append(skill_name)

                # Snapshot changed files
                file_snapshots, file_contents = await self._snapshot_files()

                # Snapshot git state
                git_state = await self._snapshot_git()

                # Create checkpoint
                checkpoint = Checkpoint(
                    id=checkpoint_id,
                    label=label,
                    timestamp=datetime.now(),
                    skill_stack=self.current_skill_stack.copy(),
                    file_snapshots=file_snapshots,
                    file_contents=file_contents,
                    git_state=git_state,
                    execution_context=self.execution_context.copy(),
                    metadata={
                        'project_root': str(self.project_root),
                        'tracked_files_count': len(self.tracked_files)
                    }
                )

                # Save checkpoint to disk
                await self._save_checkpoint(checkpoint)

                # Store in memory
                self.checkpoints[checkpoint_id] = checkpoint

                logger.info(
                    f"Checkpoint created: {len(file_snapshots)} files, "
                    f"stack depth={len(checkpoint.skill_stack)}"
                )

                return checkpoint

            except Exception as e:
                logger.error(f"Failed to create checkpoint: {e}", exc_info=True)
                raise StateManagerError(f"Checkpoint creation failed: {e}") from e

    async def restore_checkpoint(self, checkpoint_id: str) -> bool:
        """
        Restore state to checkpoint.

        Args:
            checkpoint_id: ID of checkpoint to restore

        Returns:
            True if restore successful

        Raises:
            CheckpointNotFoundError: If checkpoint doesn't exist
            RestoreError: If restore fails
        """
        async with self.lock:
            logger.info(f"Restoring checkpoint: {checkpoint_id}")

            # Load checkpoint
            checkpoint = await self._load_checkpoint(checkpoint_id)

            try:
                # Restore files
                await self._restore_files(checkpoint)

                # Restore git state
                await self._restore_git(checkpoint.git_state)

                # Restore execution state
                self.current_skill_stack = checkpoint.skill_stack.copy()
                self.execution_context = checkpoint.execution_context.copy()

                logger.info(f"Checkpoint restored successfully: {checkpoint.label}")

                return True

            except Exception as e:
                logger.error(f"Failed to restore checkpoint: {e}", exc_info=True)
                raise RestoreError(f"Checkpoint restore failed: {e}") from e

    async def verify_checkpoint(self, checkpoint_id: str) -> bool:
        """
        Verify current state matches checkpoint.

        Args:
            checkpoint_id: ID of checkpoint to verify against

        Returns:
            True if state matches checkpoint

        Raises:
            CheckpointNotFoundError: If checkpoint doesn't exist
        """
        checkpoint = await self._load_checkpoint(checkpoint_id)

        # Verify files
        current_snapshots, _ = await self._snapshot_files()

        # Compare snapshots
        if current_snapshots != checkpoint.file_snapshots:
            logger.warning("File snapshots don't match")
            return False

        # Verify git state
        current_git = await self._snapshot_git()
        if current_git.commit != checkpoint.git_state.commit:
            logger.warning("Git state doesn't match")
            return False

        logger.info("Checkpoint verification passed")
        return True

    async def list_checkpoints(self) -> List[Checkpoint]:
        """
        List all available checkpoints.

        Returns:
            List of checkpoints, newest first
        """
        async with self.lock:
            # Load from disk if not in memory
            checkpoint_files = list(self.checkpoint_dir.glob("*.json"))

            checkpoints = []
            for cp_file in checkpoint_files:
                cp_id = cp_file.stem
                if cp_id not in self.checkpoints:
                    try:
                        checkpoint = await self._load_checkpoint(cp_id)
                        self.checkpoints[cp_id] = checkpoint
                    except Exception as e:
                        logger.warning(f"Failed to load checkpoint {cp_id}: {e}")
                        continue

            checkpoints = list(self.checkpoints.values())
            checkpoints.sort(key=lambda cp: cp.timestamp, reverse=True)

            return checkpoints

    async def delete_checkpoint(self, checkpoint_id: str):
        """
        Delete checkpoint.

        Args:
            checkpoint_id: ID of checkpoint to delete

        Raises:
            CheckpointNotFoundError: If checkpoint doesn't exist
        """
        async with self.lock:
            if checkpoint_id not in self.checkpoints:
                # Try to load from disk
                await self._load_checkpoint(checkpoint_id)

            # Delete from disk
            checkpoint_file = self.checkpoint_dir / f"{checkpoint_id}.json"
            contents_file = self.checkpoint_dir / f"{checkpoint_id}_contents.json"

            if checkpoint_file.exists():
                checkpoint_file.unlink()
            if contents_file.exists():
                contents_file.unlink()

            # Remove from memory
            if checkpoint_id in self.checkpoints:
                del self.checkpoints[checkpoint_id]

            logger.info(f"Checkpoint deleted: {checkpoint_id}")

    def add_tracked_file(self, file_path: Path):
        """
        Add file to tracking list.

        Args:
            file_path: Path to file to track
        """
        rel_path = self._get_relative_path(file_path)
        self.tracked_files.add(str(rel_path))

    def update_context(self, key: str, value: Any):
        """
        Update execution context.

        Args:
            key: Context key
            value: Context value
        """
        self.execution_context[key] = value

    # Private methods

    async def _snapshot_files(self) -> tuple[Dict[str, str], Dict[str, str]]:
        """
        Snapshot tracked files.

        Returns:
            Tuple of (file_snapshots, file_contents)
            - file_snapshots: path -> content hash
            - file_contents: path -> actual content
        """
        snapshots = {}
        contents = {}

        # If no files tracked, track common changed files
        if not self.tracked_files:
            await self._discover_changed_files()

        for rel_path_str in self.tracked_files:
            file_path = self.project_root / rel_path_str

            if not file_path.exists():
                # File was deleted
                snapshots[rel_path_str] = "DELETED"
                contents[rel_path_str] = ""
                continue

            try:
                # Read content
                content = file_path.read_text(encoding='utf-8')

                # Hash content
                content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]

                snapshots[rel_path_str] = content_hash
                contents[rel_path_str] = content

            except Exception as e:
                logger.warning(f"Failed to snapshot {rel_path_str}: {e}")

        return snapshots, contents

    async def _discover_changed_files(self):
        """Discover files that have changed (via git)"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if not line:
                        continue

                    # Parse git status format
                    status = line[:2]
                    file_path = line[3:]

                    self.tracked_files.add(file_path)

        except Exception as e:
            logger.debug(f"Git discovery failed: {e}")

    async def _snapshot_git(self) -> GitState:
        """
        Snapshot git repository state.

        Returns:
            GitState object
        """
        try:
            # Get current branch
            branch_result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=10
            )
            branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"

            # Get current commit
            commit_result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=10
            )
            commit = commit_result.stdout.strip() if commit_result.returncode == 0 else "unknown"

            # Get status
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=10
            )
            status = status_result.stdout.strip() if status_result.returncode == 0 else ""

            # Parse status into files
            staged = []
            modified = []
            untracked = []

            for line in status.split('\n'):
                if not line:
                    continue

                status_code = line[:2]
                file_path = line[3:]

                if status_code[0] in ('A', 'M', 'D'):
                    staged.append(file_path)
                elif status_code[1] in ('M', 'D'):
                    modified.append(file_path)
                elif status_code == '??':
                    untracked.append(file_path)

            return GitState(
                branch=branch,
                commit=commit,
                status=status,
                staged_files=staged,
                modified_files=modified,
                untracked_files=untracked
            )

        except Exception as e:
            logger.warning(f"Failed to snapshot git state: {e}")
            return GitState(
                branch="unknown",
                commit="unknown",
                status="error"
            )

    async def _restore_files(self, checkpoint: Checkpoint):
        """
        Restore files from checkpoint.

        Args:
            checkpoint: Checkpoint to restore from
        """
        for rel_path, content in checkpoint.file_contents.items():
            file_path = self.project_root / rel_path

            if content == "" and checkpoint.file_snapshots.get(rel_path) == "DELETED":
                # File should be deleted
                if file_path.exists():
                    file_path.unlink()
                    logger.debug(f"Deleted: {rel_path}")
            else:
                # Restore file content
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(content, encoding='utf-8')
                logger.debug(f"Restored: {rel_path}")

    async def _restore_git(self, git_state: GitState):
        """
        Restore git state (best effort).

        Args:
            git_state: Git state to restore
        """
        try:
            # Reset to commit
            subprocess.run(
                ['git', 'reset', '--hard', git_state.commit],
                cwd=self.project_root,
                capture_output=True,
                timeout=30
            )

            # Checkout branch
            subprocess.run(
                ['git', 'checkout', git_state.branch],
                cwd=self.project_root,
                capture_output=True,
                timeout=30
            )

            logger.info(f"Git restored to {git_state.branch}@{git_state.commit[:8]}")

        except Exception as e:
            logger.warning(f"Failed to restore git state: {e}")

    async def _save_checkpoint(self, checkpoint: Checkpoint):
        """Save checkpoint to disk"""
        checkpoint_file = self.checkpoint_dir / f"{checkpoint.id}.json"
        contents_file = self.checkpoint_dir / f"{checkpoint.id}_contents.json"

        # Save metadata
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint.to_dict(), f, indent=2)

        # Save file contents separately (can be large)
        with open(contents_file, 'w') as f:
            json.dump(checkpoint.file_contents, f, indent=2)

    async def _load_checkpoint(self, checkpoint_id: str) -> Checkpoint:
        """Load checkpoint from disk"""
        checkpoint_file = self.checkpoint_dir / f"{checkpoint_id}.json"

        if not checkpoint_file.exists():
            raise CheckpointNotFoundError(f"Checkpoint not found: {checkpoint_id}")

        # Load metadata
        with open(checkpoint_file, 'r') as f:
            data = json.load(f)

        checkpoint = Checkpoint.from_dict(data)

        # Load file contents
        contents_file = self.checkpoint_dir / f"{checkpoint_id}_contents.json"
        if contents_file.exists():
            with open(contents_file, 'r') as f:
                checkpoint.file_contents = json.load(f)

        return checkpoint

    def _get_relative_path(self, file_path: Path) -> Path:
        """Get path relative to project root"""
        try:
            return file_path.relative_to(self.project_root)
        except ValueError:
            # File is outside project root
            return file_path
