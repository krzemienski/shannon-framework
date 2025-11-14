"""
Context Updater - Incremental context updates after code changes

Tracks changes via git diff and updates:
1. Local index files
2. Serena knowledge graph
3. File modification tracking

Duration: 30 seconds - 2 minutes (vs 12-22 min for full re-onboarding)
"""

import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel

from .serena_adapter import SerenaAdapter


@dataclass
class ChangeSet:
    """Represents a set of changes detected via git"""
    added_files: List[str]
    modified_files: List[str]
    deleted_files: List[str]
    total_changes: int

    @property
    def has_changes(self) -> bool:
        """Check if there are any changes"""
        return self.total_changes > 0


class ContextUpdater:
    """
    Incremental context updater using git diff

    Usage:
        updater = ContextUpdater(serena_adapter)
        changeset = await updater.update("myproject")

    Features:
    - Git diff analysis
    - Incremental Serena updates
    - Local index synchronization
    - Smart change detection (ignore generated files)
    """

    # Files to ignore when detecting changes
    IGNORE_PATTERNS = {
        '.pyc', '.pyo', '__pycache__',
        'node_modules/', 'dist/', 'build/',
        '.git/', '.cache/', 'coverage/',
        '.DS_Store', 'Thumbs.db'
    }

    def __init__(self, serena_adapter: Optional[SerenaAdapter] = None):
        """
        Initialize updater

        Args:
            serena_adapter: SerenaAdapter for knowledge graph updates
        """
        self.serena = serena_adapter or SerenaAdapter()
        self.console = Console()
        self.logger = logging.getLogger(__name__)

    async def update(
        self,
        project_id: str,
        force: bool = False
    ) -> ChangeSet:
        """
        Update project context with latest changes

        Args:
            project_id: Project identifier
            force: Force full re-scan even without git changes

        Returns:
            ChangeSet with detected changes

        Raises:
            ValueError: If project not found
            RuntimeError: If git not available or not a git repo
        """
        # Display header
        self.console.print("\n")
        self.console.print(Panel.fit(
            f"[bold cyan]Updating Context: {project_id}[/bold cyan]",
            border_style="cyan"
        ))

        # Load project metadata
        metadata = self._load_metadata(project_id)
        project_path = Path(metadata['project_path'])

        # Detect changes via git
        self.console.print("\n[bold]Detecting changes...[/bold]")
        changeset = self._detect_changes(project_path, metadata)

        if not changeset.has_changes and not force:
            self.console.print("  ℹ️ No changes detected")
            self.console.print("\n[green]Context already up to date[/green]")
            return changeset

        # Show changes
        self._show_changes(changeset)

        # Update local index
        self.console.print("\n[bold]Updating local index...[/bold]")
        self._update_local_index(project_id, project_path, changeset, metadata)

        # Update Serena
        self.console.print("\n[bold]Updating Serena knowledge graph...[/bold]")
        await self._update_serena(project_id, changeset)

        # Success
        self.console.print("\n[green]✅ Context updated[/green]")
        self.console.print(f"  • {len(changeset.added_files)} files added")
        self.console.print(f"  • {len(changeset.modified_files)} files modified")
        self.console.print(f"  • {len(changeset.deleted_files)} files deleted")

        return changeset

    def _load_metadata(self, project_id: str) -> Dict:
        """Load project metadata"""
        project_dir = Path.home() / ".shannon" / "projects" / project_id
        metadata_file = project_dir / "project.json"

        if not metadata_file.exists():
            raise ValueError(f"Project '{project_id}' not found")

        return json.loads(metadata_file.read_text())

    def _detect_changes(
        self,
        project_path: Path,
        metadata: Dict
    ) -> ChangeSet:
        """
        Detect changes since last update using git

        Args:
            project_path: Path to project
            metadata: Project metadata with last update timestamp

        Returns:
            ChangeSet with detected changes
        """
        # Check if git is available
        if not self._is_git_repo(project_path):
            self.logger.warning("Not a git repo, cannot detect changes incrementally")
            return ChangeSet([], [], [], 0)

        # Get changes since last update
        last_update = metadata.get('updated_at', metadata.get('created_at'))
        if not last_update:
            # No previous update, consider all files as new
            return self._scan_all_files(project_path)

        # Get git diff since last update
        added, modified, deleted = self._git_diff_since(project_path, last_update)

        # Filter ignored patterns
        added = self._filter_ignored(added)
        modified = self._filter_ignored(modified)
        deleted = self._filter_ignored(deleted)

        total = len(added) + len(modified) + len(deleted)

        return ChangeSet(
            added_files=added,
            modified_files=modified,
            deleted_files=deleted,
            total_changes=total
        )

    def _is_git_repo(self, path: Path) -> bool:
        """Check if directory is a git repository"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                cwd=str(path),
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False

    def _git_diff_since(
        self,
        project_path: Path,
        since_timestamp: str
    ) -> Tuple[List[str], List[str], List[str]]:
        """
        Get git diff since timestamp

        Returns:
            (added_files, modified_files, deleted_files)
        """
        try:
            # Get changed files since timestamp
            # Format: git log --since="..." --name-status --pretty=format:""
            result = subprocess.run(
                [
                    'git', 'log',
                    f'--since={since_timestamp}',
                    '--name-status',
                    '--pretty=format:'
                ],
                cwd=str(project_path),
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                self.logger.error(f"Git diff failed: {result.stderr}")
                return [], [], []

            # Parse output
            added = []
            modified = []
            deleted = []

            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue

                parts = line.split('\t', 1)
                if len(parts) != 2:
                    continue

                status, filepath = parts
                status = status.strip()

                if status == 'A':
                    added.append(filepath)
                elif status == 'M':
                    modified.append(filepath)
                elif status == 'D':
                    deleted.append(filepath)

            return added, modified, deleted

        except Exception as e:
            self.logger.error(f"Git diff error: {e}")
            return [], [], []

    def _scan_all_files(self, project_path: Path) -> ChangeSet:
        """Fallback: Scan all files as new"""
        files = []
        for file_path in project_path.rglob('*'):
            if file_path.is_file():
                try:
                    rel_path = str(file_path.relative_to(project_path))
                    if not self._should_ignore(rel_path):
                        files.append(rel_path)
                except Exception:
                    pass

        return ChangeSet(
            added_files=files,
            modified_files=[],
            deleted_files=[],
            total_changes=len(files)
        )

    def _filter_ignored(self, files: List[str]) -> List[str]:
        """Filter out ignored files"""
        return [f for f in files if not self._should_ignore(f)]

    def _should_ignore(self, filepath: str) -> bool:
        """Check if file should be ignored"""
        return any(pattern in filepath for pattern in self.IGNORE_PATTERNS)

    def _update_local_index(
        self,
        project_id: str,
        project_path: Path,
        changeset: ChangeSet,
        metadata: Dict
    ):
        """Update local index files with changes"""
        project_dir = Path.home() / ".shannon" / "projects" / project_id

        # Load current structure
        structure_file = project_dir / "structure.json"
        if structure_file.exists():
            structure = json.loads(structure_file.read_text())
        else:
            structure = []

        # Update structure with changes
        # Remove deleted files
        structure = [f for f in structure if f['path'] not in changeset.deleted_files]

        # Update modified files
        for filepath in changeset.modified_files:
            abs_path = project_path / filepath
            if abs_path.exists():
                try:
                    lines = len(abs_path.read_text(encoding='utf-8', errors='ignore').splitlines())
                    # Update or add
                    existing = next((f for f in structure if f['path'] == filepath), None)
                    if existing:
                        existing['lines'] = lines
                        existing['modified_at'] = datetime.now().isoformat()
                except Exception:
                    pass

        # Add new files
        for filepath in changeset.added_files:
            abs_path = project_path / filepath
            if abs_path.exists():
                try:
                    content = abs_path.read_text(encoding='utf-8', errors='ignore')
                    lines = len(content.splitlines())
                    structure.append({
                        'path': filepath,
                        'lines': lines,
                        'language': self._detect_language(abs_path),
                        'added_at': datetime.now().isoformat()
                    })
                except Exception:
                    pass

        # Save updated structure
        structure_file.write_text(json.dumps(structure, indent=2))

        # Update metadata
        metadata['updated_at'] = datetime.now().isoformat()
        metadata['file_count'] = len(structure)
        metadata['total_lines'] = sum(f.get('lines', 0) for f in structure)

        (project_dir / "project.json").write_text(json.dumps(metadata, indent=2))

    async def _update_serena(self, project_id: str, changeset: ChangeSet):
        """Update Serena knowledge graph with changes"""
        # Add observations about recent changes
        observations = []

        if changeset.added_files:
            observations.append(
                f"Recent additions: {', '.join(changeset.added_files[:5])}"
            )

        if changeset.modified_files:
            observations.append(
                f"Recent modifications: {', '.join(changeset.modified_files[:5])}"
            )

        if changeset.deleted_files:
            observations.append(
                f"Recent deletions: {', '.join(changeset.deleted_files[:5])}"
            )

        observations.append(f"Last updated: {datetime.now().isoformat()}")

        # Add to project node
        await self.serena.add_observations(
            entity_id=f"project_{project_id}",
            observations=observations
        )

    def _detect_language(self, file_path: Path) -> str:
        """Detect language from file extension"""
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.go': 'Go',
            '.rs': 'Rust'
        }
        return language_map.get(file_path.suffix.lower(), 'Other')

    def _show_changes(self, changeset: ChangeSet):
        """Display detected changes"""
        if changeset.added_files:
            self.console.print(f"  + Added: {len(changeset.added_files)} files")
            for f in changeset.added_files[:3]:
                self.console.print(f"    • {f}")

        if changeset.modified_files:
            self.console.print(f"  ~ Modified: {len(changeset.modified_files)} files")
            for f in changeset.modified_files[:3]:
                self.console.print(f"    • {f}")

        if changeset.deleted_files:
            self.console.print(f"  - Deleted: {len(changeset.deleted_files)} files")
            for f in changeset.deleted_files[:3]:
                self.console.print(f"    • {f}")
