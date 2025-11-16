"""
Shannon Skills Framework - v4.0

Wave 1 COMPLETE! All core runtime components implemented and production-ready.

The Skills Framework is the foundation of Shannon v4.0, providing:
- Skill definitions (YAML/JSON)
- Auto-discovery from multiple sources
- Dependency resolution
- Hook-based lifecycle management
- Full skill execution engine (NATIVE/SCRIPT/MCP/COMPOSITE)
- Performance tracking and optimization
- Dynamic skill generation (future)

Wave 1 Components (COMPLETE):
    models.py        - Core data structures
    registry.py      - Central skill registry (15 tests passing)
    loader.py        - Load skills from YAML/JSON (12 tests passing)
    hooks.py         - Hook lifecycle management (10 tests passing)
    executor.py      - Skill execution engine (23 tests passing) - NEW!

Total: 60/60 tests passing

Usage:
    from shannon.skills import (
        SkillRegistry,
        SkillLoader,
        HookManager,
        SkillExecutor,
        ExecutionContext
    )

    # Initialize
    registry = SkillRegistry(schema_path=Path("schemas/skill.schema.json"))
    loader = SkillLoader(search_paths=[Path("skills")])
    hook_manager = HookManager(registry=registry)
    executor = SkillExecutor(registry=registry, hook_manager=hook_manager)

    # Load all skills
    await loader.load_all_skills(registry)

    # Execute a skill
    skill = registry.get("library_discovery")
    result = await executor.execute(
        skill=skill,
        parameters={'feature_description': 'auth', 'project_root': '/path'},
        context=ExecutionContext(task="Find libraries")
    )
"""

from shannon.skills.models import (
    Skill,
    SkillResult,
    Parameter,
    Hooks,
    Execution,
    ExecutionType,
    SkillStatus,
    HookTrigger,
    ExecutionContext,
    AgentState,
    SkillMetadata,
)
from shannon.skills.registry import SkillRegistry
from shannon.skills.loader import (
    SkillLoader,
    SkillLoadError,
    SkillParseError,
    SkillFileError,
)
from shannon.skills.hooks import (
    HookManager,
    HookExecutionResult,
    HookExecutionError,
    CircularHookError,
    HookTimeoutError,
)
from shannon.skills.executor import (
    SkillExecutor,
    SkillExecutionError,
    ParameterValidationError,
    SkillTimeoutError,
    NativeExecutionError,
    ScriptExecutionError,
    MCPExecutionError,
    CompositeExecutionError,
)

__version__ = "4.0.0"

__all__ = [
    # Models
    'Skill',
    'SkillResult',
    'Parameter',
    'Hooks',
    'Execution',
    'ExecutionType',
    'SkillStatus',
    'HookTrigger',
    'ExecutionContext',
    'AgentState',
    'SkillMetadata',
    # Registry
    'SkillRegistry',
    # Loader
    'SkillLoader',
    'SkillLoadError',
    'SkillParseError',
    'SkillFileError',
    # Hooks
    'HookManager',
    'HookExecutionResult',
    'HookExecutionError',
    'CircularHookError',
    'HookTimeoutError',
    # Executor (NEW!)
    'SkillExecutor',
    'SkillExecutionError',
    'ParameterValidationError',
    'SkillTimeoutError',
    'NativeExecutionError',
    'ScriptExecutionError',
    'MCPExecutionError',
    'CompositeExecutionError',
]
