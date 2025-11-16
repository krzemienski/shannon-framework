"""
Shannon Skills Framework

The Skills Framework is the foundation of Shannon v4.0, providing:
- Skill definitions (YAML/JSON)
- Auto-discovery from multiple sources
- Dependency resolution
- Hook-based lifecycle management
- Performance tracking and optimization
- Dynamic skill generation

Architecture:
    registry.py      - Central skill registry
    loader.py        - Load skills from YAML/JSON
    executor.py      - Execute skills with hooks
    hooks.py         - Hook management
    discovery.py     - Auto-discovery engine
    dependencies.py  - Dependency resolution
    catalog.py       - Skill catalog persistence
    pattern_detector.py - Pattern detection
    generator.py     - Dynamic skill generation
    performance.py   - Performance monitoring
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

__version__ = "4.0.0"

__all__ = [
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
]
