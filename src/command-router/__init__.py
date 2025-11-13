"""
Shannon Framework v4 - Command Router

Purpose: Thin orchestration layer that coordinates all Shannon components.

Components:
  - CommandRouter: Main router
  - CommandContext: Execution context
  - CommandResult: Execution result

Commands:
  - ANALYZE_SPEC: Parse and analyze specification
  - CREATE_PLAN: Create execution plan
  - EXECUTE_PHASE: Execute single phase
  - EXECUTE_WAVE: Execute single wave
  - EXECUTE_FULL: Full end-to-end execution
  - CHECKPOINT: Create checkpoint
  - RESTORE: Restore from checkpoint
  - STATUS: Get current status
  - VALIDATE: Run validation gate

Execution Modes:
  - INTERACTIVE: User confirms each step
  - AUTO: Automatic execution
  - DRY_RUN: Plan only, don't execute

Author: Shannon Framework Team
Version: 1.0.0
License: MIT
"""

from .models import (
    CommandType,
    ExecutionMode,
    CommandContext,
    CommandResult,
)
from .router import CommandRouter

__all__ = [
    # Router
    'CommandRouter',

    # Models
    'CommandContext',
    'CommandResult',

    # Enums
    'CommandType',
    'ExecutionMode',
]

__version__ = '1.0.0'


# Convenience functions

def create_router(
    skills_dir: str = None,
    storage_backend: str = "local",
    serena_client=None
) -> CommandRouter:
    """
    Create command router.

    Args:
        skills_dir: Directory containing skill definitions
        storage_backend: Storage backend (local, serena, memory)
        serena_client: Serena MCP client

    Returns:
        CommandRouter instance
    """
    from pathlib import Path
    return CommandRouter(
        skills_dir=Path(skills_dir) if skills_dir else None,
        storage_backend=storage_backend,
        serena_client=serena_client
    )


def analyze_specification(
    spec_text: str,
    confidence_threshold: float = 0.90
) -> dict:
    """
    Quick specification analysis.

    Args:
        spec_text: Specification text
        confidence_threshold: Minimum confidence

    Returns:
        Analysis result dictionary
    """
    router = create_router()

    context = CommandContext(
        specification_text=spec_text,
        confidence_threshold=confidence_threshold
    )

    result = router.execute_command(CommandType.ANALYZE_SPEC, context)
    return result.to_dict()
