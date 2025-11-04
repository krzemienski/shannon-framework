"""
Shannon Framework v4 - Skill Registry

Purpose: Skill discovery, registration, lifecycle management, and auto-activation.

Components:
  - SkillRegistry: Central registry for skill management
  - SkillManager: High-level lifecycle and orchestration
  - SkillLoader: Progressive loading (3 levels)
  - Models: Skill data structures

Progressive Disclosure:
  Level 1: Frontmatter only (~50 tokens/skill)
  Level 2: Full SKILL.md (~500 lines)
  Level 3: All references/* (unlimited)

Author: Shannon Framework Team
Version: 1.0.0
License: MIT
"""

from .models import (
    Skill,
    SkillMetadata,
    SkillContent,
    SkillReferences,
    SkillType,
    LoadLevel,
    ActivationTrigger,
    MCPDependency,
    SubSkillRequirement,
)
from .loader import SkillLoader, SkillLoadError
from .registry import SkillRegistry, SkillRegistryError
from .manager import SkillManager

__all__ = [
    # Core classes
    'SkillRegistry',
    'SkillManager',
    'SkillLoader',

    # Models
    'Skill',
    'SkillMetadata',
    'SkillContent',
    'SkillReferences',

    # Enums
    'SkillType',
    'LoadLevel',

    # Dependencies
    'ActivationTrigger',
    'MCPDependency',
    'SubSkillRequirement',

    # Exceptions
    'SkillLoadError',
    'SkillRegistryError',
]

__version__ = '1.0.0'
