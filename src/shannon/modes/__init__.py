"""Shannon execution modes.

Provides different execution modes:
- DebugMode: Step-by-step execution with investigation
- UltrathinkMode: Deep reasoning with 500+ steps

Part of: Wave 7 & Wave 9
"""

from .debug_mode import (
    DebugSession,
    DebugModeEngine,
    DebugDepth,
    ExecutionState,
    DebugStep,
    Breakpoint
)

from .investigation import (
    InvestigationTools,
    InvestigationResult
)

from .ultrathink import (
    UltrathinkSession,
    ReasoningStep,
    Hypothesis
)

__all__ = [
    # Debug mode
    'DebugSession',
    'DebugModeEngine',
    'DebugDepth',
    'ExecutionState',
    'DebugStep',
    'Breakpoint',

    # Investigation
    'InvestigationTools',
    'InvestigationResult',

    # Ultrathink
    'UltrathinkSession',
    'ReasoningStep',
    'Hypothesis'
]
