"""
Shannon Reflection Module
========================

Serena MCP-powered reflection system for continuous learning and improvement.

Key Components:
- ReflectionEngine: 5-stage reflection orchestrator
- WaveReflectionHooks: Integration hooks for wave boundaries
- ReflectionContext: Context dataclass for reflection inputs
- ReflectionResult: Result dataclass for reflection outputs

Usage:
    from shannon.reflection import ReflectionEngine, WaveReflectionHooks

    # For wave orchestration
    hooks = WaveReflectionHooks(mcp_available=True)
    pre_result = await hooks.pre_wave_hook(wave_context)

    # For standalone reflection
    engine = ReflectionEngine(mcp_available=True)
    result = await engine.reflect(reflection_context)
"""

from .serena_hooks import (
    ReflectionEngine,
    WaveReflectionHooks,
    ReflectionContext,
    ReflectionResult,
    ReflectionPoint
)

__all__ = [
    "ReflectionEngine",
    "WaveReflectionHooks",
    "ReflectionContext",
    "ReflectionResult",
    "ReflectionPoint"
]

__version__ = "2.1.0"