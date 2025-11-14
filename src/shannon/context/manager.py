"""
Context Manager - Orchestrates all context operations

Implements multi-tier storage:
- Hot (in-memory): Current session context
- Warm (local files): Project metadata and indices
- Cold (Serena MCP): Long-term knowledge graph

Coordinates:
- Onboarding
- Priming
- Updating
- Smart loading
"""

import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field

from .serena_adapter import SerenaAdapter
from .onboarder import CodebaseOnboarder
from .primer import ContextPrimer, ProjectContext
from .updater import ContextUpdater, ChangeSet
from .loader import SmartContextLoader, LoadedContext


@dataclass
class SessionContext:
    """Hot storage: Current session context"""
    current_project: Optional[ProjectContext] = None
    loaded_files: Dict[str, str] = field(default_factory=dict)
    active_task: Optional[str] = None
    session_start: str = field(default_factory=lambda: datetime.now().isoformat())


class ContextManager:
    """
    Context lifecycle manager

    Usage:
        manager = ContextManager()

        # Onboard new project
        await manager.onboard_project("/path/to/project", "myproject")

        # Prime project for session
        await manager.prime_project("myproject")

        # Load context for task
        context = await manager.load_for_task("Add authentication", "myproject")

        # Update after changes
        await manager.update_project("myproject")

    Features:
    - Multi-tier storage management
    - Lifecycle coordination
    - Automatic cache invalidation
    - Session management
    """

    def __init__(
        self,
        serena_adapter: Optional[SerenaAdapter] = None,
        sdk_client: Optional[Any] = None
    ):
        """
        Initialize context manager

        Args:
            serena_adapter: SerenaAdapter for knowledge graph
            sdk_client: Shannon SDK client for analysis
        """
        # Storage layers
        self.serena = serena_adapter or SerenaAdapter()
        self.session = SessionContext()

        # Component managers
        self.onboarder = CodebaseOnboarder(sdk_client, self.serena)
        self.primer = ContextPrimer(self.serena)
        self.updater = ContextUpdater(self.serena)
        self.loader = SmartContextLoader(self.serena)

        self.logger = logging.getLogger(__name__)

    async def onboard_project(
        self,
        project_path: str,
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Onboard a new project

        Args:
            project_path: Path to project root
            project_id: Optional project ID (defaults to directory name)

        Returns:
            Onboarding result with metadata
        """
        self.logger.info(f"Onboarding project: {project_path}")

        path = Path(project_path)
        result = await self.onboarder.onboard(path, project_id)

        self.logger.info(f"Project onboarded: {result['project_id']}")
        return result

    async def prime_project(
        self,
        project_id: str,
        load_files: bool = True,
        check_mcps: bool = True
    ) -> ProjectContext:
        """
        Prime project for current session

        Args:
            project_id: Project identifier
            load_files: Whether to load critical files
            check_mcps: Whether to check MCP availability

        Returns:
            ProjectContext with loaded data
        """
        self.logger.info(f"Priming project: {project_id}")

        context = await self.primer.prime(
            project_id=project_id,
            load_files=load_files,
            check_mcps=check_mcps
        )

        # Store in hot storage
        self.session.current_project = context
        self.session.loaded_files = context.critical_files

        self.logger.info(f"Project primed: {project_id}")
        return context

    async def update_project(
        self,
        project_id: Optional[str] = None,
        force: bool = False
    ) -> ChangeSet:
        """
        Update project with latest changes

        Args:
            project_id: Project identifier (defaults to current)
            force: Force full re-scan

        Returns:
            ChangeSet with detected changes
        """
        # Use current project if not specified
        if not project_id:
            if not self.session.current_project:
                raise ValueError("No project specified and no current project")
            project_id = self.session.current_project.project_id

        self.logger.info(f"Updating project: {project_id}")

        changeset = await self.updater.update(
            project_id=project_id,
            force=force
        )

        # Invalidate hot storage if current project
        if (self.session.current_project and
            self.session.current_project.project_id == project_id):
            self.session.loaded_files.clear()

        self.logger.info(f"Project updated: {changeset.total_changes} changes")
        return changeset

    async def load_for_task(
        self,
        task_description: str,
        project_id: Optional[str] = None
    ) -> LoadedContext:
        """
        Load context for specific task

        Args:
            task_description: Description of task
            project_id: Project identifier (defaults to current)

        Returns:
            LoadedContext with relevant files
        """
        # Use current project if not specified
        if not project_id:
            if not self.session.current_project:
                raise ValueError("No project specified and no current project")
            project_id = self.session.current_project.project_id

        self.logger.info(f"Loading context for task: {task_description[:50]}...")

        context = await self.loader.load_for_task(
            task_description=task_description,
            project_id=project_id
        )

        # Update session
        self.session.active_task = task_description
        self.session.loaded_files.update(context.relevant_files)

        self.logger.info(
            f"Loaded {len(context.relevant_files)} files ({context.total_lines} lines)"
        )
        return context

    def get_session_context(self) -> SessionContext:
        """Get current session context"""
        return self.session

    def clear_session(self):
        """Clear session context (hot storage)"""
        self.logger.info("Clearing session context")
        self.session = SessionContext()

    def list_projects(self) -> List[Dict[str, Any]]:
        """
        List all onboarded projects

        Returns:
            List of project metadata dictionaries
        """
        projects = []
        projects_dir = Path.home() / ".shannon" / "projects"

        if not projects_dir.exists():
            return []

        for project_dir in projects_dir.iterdir():
            if project_dir.is_dir():
                metadata_file = project_dir / "project.json"
                if metadata_file.exists():
                    try:
                        import json
                        metadata = json.loads(metadata_file.read_text())
                        projects.append(metadata)
                    except Exception as e:
                        self.logger.error(f"Failed to load {metadata_file}: {e}")

        return projects

    async def delete_project(self, project_id: str):
        """
        Delete project from all storage tiers

        Args:
            project_id: Project identifier
        """
        self.logger.warning(f"Deleting project: {project_id}")

        # Delete from Serena (cold storage)
        try:
            await self.serena.delete_entity(f"project_{project_id}")
        except Exception as e:
            self.logger.error(f"Failed to delete from Serena: {e}")

        # Delete from local files (warm storage)
        import shutil
        project_dir = Path.home() / ".shannon" / "projects" / project_id
        if project_dir.exists():
            shutil.rmtree(project_dir)

        # Clear from session (hot storage) if current
        if (self.session.current_project and
            self.session.current_project.project_id == project_id):
            self.clear_session()

        self.logger.info(f"Project deleted: {project_id}")

    def get_state(self) -> Dict[str, Any]:
        """
        Get current context state for V3.1 dashboard.

        Returns:
            Dictionary with loaded context information:
            - loaded_files: List of file paths currently loaded
            - active_memories: List of active memory names
            - available_tools: List of tool names
            - mcp_servers: List of connected MCP servers
            - total_bytes: Total bytes of loaded content
        """
        return {
            'loaded_files': list(self.session.loaded_files.keys()),
            'active_memories': [],  # Would track from Serena queries
            'available_tools': [],  # Would track from tool registry
            'mcp_servers': [],  # Would track from MCP manager
            'total_bytes': sum(len(content) for content in self.session.loaded_files.values())
        }

    def get_stats(self) -> Dict[str, Any]:
        """
        Get context manager statistics

        Returns:
            Dictionary with stats about storage and usage
        """
        projects = self.list_projects()

        return {
            'projects_count': len(projects),
            'current_project': (
                self.session.current_project.project_id
                if self.session.current_project else None
            ),
            'session_files_loaded': len(self.session.loaded_files),
            'active_task': self.session.active_task,
            'session_duration_minutes': self._get_session_duration_minutes(),
            'serena_stats': self.serena.get_stats()
        }

    def _get_session_duration_minutes(self) -> float:
        """Calculate session duration in minutes"""
        start = datetime.fromisoformat(self.session.session_start)
        duration = datetime.now() - start
        return duration.total_seconds() / 60
