"""
Shannon Context Management System

Complete context management for existing codebases:
- Onboarding: Index existing codebase (12-22 min)
- Priming: Quick context reload (10-30 sec)
- Updating: Incremental updates via git diff (30 sec - 2 min)
- Smart Loading: Task-specific relevance-based loading (90% relevance with 10% of codebase)

Storage Architecture:
- Hot (in-memory): Current session context
- Warm (local files): ~/.shannon/projects/{name}/
- Cold (Serena MCP): Knowledge graph for semantic search

Usage:
    from shannon.context import ContextManager

    # Initialize manager
    manager = ContextManager()

    # Onboard new project
    await manager.onboard_project("/path/to/project", "myproject")

    # Prime for session
    await manager.prime_project("myproject")

    # Load context for task
    context = await manager.load_for_task("Add authentication", "myproject")

    # Update after changes
    await manager.update_project("myproject")
"""

from .serena_adapter import (
    SerenaAdapter,
    SerenaNode,
    SerenaRelation
)
from .onboarder import (
    CodebaseOnboarder,
    DiscoveryResult,
    AnalysisResult
)
from .primer import (
    ContextPrimer,
    ProjectContext,
    QuickPrimer,
    MCPStatus
)
from .updater import (
    ContextUpdater,
    ChangeSet
)
from .loader import (
    SmartContextLoader,
    LoadedContext,
    ContextLoadingStrategy
)
from .manager import (
    ContextManager,
    SessionContext
)

# Version
__version__ = "3.0.0"

# Public API
__all__ = [
    # Main manager
    'ContextManager',
    'SessionContext',

    # Components
    'SerenaAdapter',
    'CodebaseOnboarder',
    'ContextPrimer',
    'ContextUpdater',
    'SmartContextLoader',

    # Data classes
    'SerenaNode',
    'SerenaRelation',
    'DiscoveryResult',
    'AnalysisResult',
    'ProjectContext',
    'MCPStatus',
    'ChangeSet',
    'LoadedContext',

    # Utilities
    'QuickPrimer',
    'ContextLoadingStrategy',

    # Convenience functions
    'onboard',
    'prime',
    'update',
    'load_for_task',
    'list_projects'
]


# Convenience functions for quick usage

_global_manager = None


def get_manager() -> ContextManager:
    """Get or create global context manager"""
    global _global_manager
    if _global_manager is None:
        _global_manager = ContextManager()
    return _global_manager


async def onboard(project_path: str, project_id: str = None):
    """
    Convenience function to onboard a project

    Args:
        project_path: Path to project root
        project_id: Optional project ID

    Returns:
        Onboarding result

    Example:
        await onboard("/path/to/project", "myproject")
    """
    manager = get_manager()
    return await manager.onboard_project(project_path, project_id)


async def prime(project_id: str, load_files: bool = True):
    """
    Convenience function to prime a project

    Args:
        project_id: Project identifier
        load_files: Whether to load critical files

    Returns:
        ProjectContext

    Example:
        context = await prime("myproject")
    """
    manager = get_manager()
    return await manager.prime_project(project_id, load_files)


async def update(project_id: str = None, force: bool = False):
    """
    Convenience function to update a project

    Args:
        project_id: Project identifier (defaults to current)
        force: Force full re-scan

    Returns:
        ChangeSet

    Example:
        changes = await update("myproject")
    """
    manager = get_manager()
    return await manager.update_project(project_id, force)


async def load_for_task(task: str, project_id: str = None):
    """
    Convenience function to load context for a task

    Args:
        task: Task description
        project_id: Project identifier (defaults to current)

    Returns:
        LoadedContext

    Example:
        context = await load_for_task("Add JWT authentication")
    """
    manager = get_manager()
    return await manager.load_for_task(task, project_id)


def list_projects():
    """
    Convenience function to list all projects

    Returns:
        List of project metadata dictionaries

    Example:
        projects = list_projects()
        for project in projects:
            print(project['project_id'])
    """
    manager = get_manager()
    return manager.list_projects()


# Module initialization
import logging

logger = logging.getLogger(__name__)
logger.debug("Shannon context management system initialized")
