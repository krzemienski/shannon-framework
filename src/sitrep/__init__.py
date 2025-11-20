"""
Shannon Framework v4 - SITREP Protocol

Purpose: Military-style Situation Reports for standardized agent communication.

Components:
  - SITREP: Core data structure
  - SITREPTemplate: Formatting (markdown, text, compact)
  - SITREPGenerator: Creation helpers
  - SITREPValidator: Validation

SITREP Format:
  - Header: Agent, mission, timestamp, priority
  - Status: Overall status, completion percentage
  - Situation: Summary and task breakdown
  - Analysis: Findings, risks, metrics
  - Actions: Completed and next steps
  - Resources: Used and needed

Author: Shannon Framework Team
Version: 1.0.0
License: MIT
"""

from .models import (
    SITREP,
    Task,
    Finding,
    Risk,
    Metric,
    SITREPStatus,
    SITREPPriority,
    TaskStatus,
)
from .template import SITREPTemplate
from .generator import SITREPGenerator
from .validator import SITREPValidator, ValidationError

__all__ = [
    # Core model
    'SITREP',

    # Supporting models
    'Task',
    'Finding',
    'Risk',
    'Metric',

    # Enums
    'SITREPStatus',
    'SITREPPriority',
    'TaskStatus',

    # Template engine
    'SITREPTemplate',

    # Generator
    'SITREPGenerator',

    # Validator
    'SITREPValidator',
    'ValidationError',
]

__version__ = '1.0.0'


# Convenience functions

def create_sitrep(
    agent_name: str,
    mission: str,
    status: str = "GREEN",
    **kwargs
) -> SITREP:
    """
    Create a SITREP with minimal arguments.

    Args:
        agent_name: Name of reporting agent
        mission: Mission description
        status: Overall status (GREEN/YELLOW/RED/COMPLETE)
        **kwargs: Additional SITREP fields

    Returns:
        SITREP instance
    """
    return SITREPGenerator.create_simple(
        agent_name=agent_name,
        mission=mission,
        status=status,
        **kwargs
    )


def format_sitrep(sitrep: SITREP, format: str = "markdown") -> str:
    """
    Format SITREP as string.

    Args:
        sitrep: SITREP to format
        format: Output format (markdown, text, compact)

    Returns:
        Formatted string
    """
    if format == "markdown":
        return SITREPTemplate.render_markdown(sitrep)
    elif format == "text":
        return SITREPTemplate.render_text(sitrep)
    elif format == "compact":
        return SITREPTemplate.render_compact(sitrep)
    else:
        raise ValueError(f"Unknown format: {format}")


def validate_sitrep(sitrep: SITREP) -> bool:
    """
    Validate SITREP.

    Args:
        sitrep: SITREP to validate

    Returns:
        True if valid
    """
    validator = SITREPValidator()
    return validator.is_valid(sitrep)
