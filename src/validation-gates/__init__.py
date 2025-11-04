"""
Shannon Framework v4 - Validation Gate System

Purpose: Confidence-based validation gates to prevent wrong-direction work.

Components:
  - ValidationGateValidator: Main validator
  - ValidationGate: Gate configuration
  - ConfidenceScore: Multi-component scoring
  - ValidationIssue: Issue tracking

Gate Levels:
  - SPECIFICATION: Validate spec before implementation (≥90%)
  - PHASE: Validate phase completion (≥90%)
  - WAVE: Validate wave execution (≥90%)
  - TASK: Validate individual tasks

Confidence Components:
  - Completeness: All required information present
  - Clarity: Clear and unambiguous
  - Feasibility: Technically achievable
  - Consistency: No contradictions
  - Testability: Can be validated

Confidence Levels:
  - CRITICAL: < 70% (stop immediately)
  - LOW: 70-80% (major revision needed)
  - MEDIUM: 80-90% (acceptable but improvable)
  - HIGH: 90-95% (good confidence)
  - VERY_HIGH: > 95% (excellent confidence)

Author: Shannon Framework Team
Version: 1.0.0
License: MIT
"""

from .models import (
    ValidationGate,
    ValidationGateResult,
    ValidationIssue,
    ConfidenceScore,
    GateLevel,
    GateStatus,
    ConfidenceLevel,
)
from .validator import ValidationGateValidator

__all__ = [
    # Validator
    'ValidationGateValidator',

    # Models
    'ValidationGate',
    'ValidationGateResult',
    'ValidationIssue',
    'ConfidenceScore',

    # Enums
    'GateLevel',
    'GateStatus',
    'ConfidenceLevel',
]

__version__ = '1.0.0'


# Convenience functions

def create_gate(
    gate_id: str,
    level: str,
    threshold: float = 0.90,
    allow_bypass: bool = False,
    stop_on_failure: bool = True
) -> ValidationGate:
    """
    Create validation gate.

    Args:
        gate_id: Gate identifier
        level: Gate level (specification, phase, wave, task)
        threshold: Minimum confidence threshold (0.0-1.0)
        allow_bypass: Allow manual bypass
        stop_on_failure: Stop execution on failure

    Returns:
        ValidationGate instance
    """
    return ValidationGate(
        id=gate_id,
        level=GateLevel[level.upper()],
        threshold=threshold,
        allow_bypass=allow_bypass,
        stop_on_failure=stop_on_failure
    )


def validate_confidence(
    confidence: float,
    threshold: float = 0.90
) -> bool:
    """
    Quick confidence check.

    Args:
        confidence: Confidence score (0.0-1.0)
        threshold: Minimum threshold

    Returns:
        True if confidence >= threshold
    """
    return confidence >= threshold


def get_confidence_level(confidence: float) -> str:
    """
    Get confidence level from score.

    Args:
        confidence: Confidence score (0.0-1.0)

    Returns:
        Confidence level string
    """
    if confidence < 0.70:
        return "CRITICAL"
    elif confidence < 0.80:
        return "LOW"
    elif confidence < 0.90:
        return "MEDIUM"
    elif confidence < 0.95:
        return "HIGH"
    else:
        return "VERY_HIGH"
