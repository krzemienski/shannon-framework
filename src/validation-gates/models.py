"""
Shannon Framework v4 - Validation Gate Models

Data structures for validation gates and confidence scoring.
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class GateLevel(Enum):
    """Validation gate levels."""
    SPECIFICATION = "specification"  # Spec-level validation
    PHASE = "phase"                 # Phase-level validation
    WAVE = "wave"                   # Wave-level validation
    TASK = "task"                   # Task-level validation


class GateStatus(Enum):
    """Validation gate status."""
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    BYPASSED = "bypassed"


class ConfidenceLevel(Enum):
    """Confidence levels."""
    CRITICAL = "critical"   # < 0.70
    LOW = "low"            # 0.70 - 0.80
    MEDIUM = "medium"      # 0.80 - 0.90
    HIGH = "high"          # 0.90 - 0.95
    VERY_HIGH = "very_high"  # > 0.95


@dataclass
class ConfidenceScore:
    """Confidence score with breakdown."""
    overall: float  # 0.0 to 1.0

    # Component scores
    completeness: float = 0.0      # All required info present
    clarity: float = 0.0           # Clear and unambiguous
    feasibility: float = 0.0       # Technically feasible
    consistency: float = 0.0       # No contradictions
    testability: float = 0.0       # Can be validated

    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)
    confidence_level: Optional[ConfidenceLevel] = None

    def __post_init__(self):
        """Calculate confidence level from overall score."""
        if self.overall < 0.70:
            self.confidence_level = ConfidenceLevel.CRITICAL
        elif self.overall < 0.80:
            self.confidence_level = ConfidenceLevel.LOW
        elif self.overall < 0.90:
            self.confidence_level = ConfidenceLevel.MEDIUM
        elif self.overall < 0.95:
            self.confidence_level = ConfidenceLevel.HIGH
        else:
            self.confidence_level = ConfidenceLevel.VERY_HIGH

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'overall': self.overall,
            'completeness': self.completeness,
            'clarity': self.clarity,
            'feasibility': self.feasibility,
            'consistency': self.consistency,
            'testability': self.testability,
            'confidence_level': self.confidence_level.value if self.confidence_level else None,
            'timestamp': self.timestamp.isoformat(),
        }


@dataclass
class ValidationIssue:
    """Issue found during validation."""
    severity: str  # critical, high, medium, low
    category: str  # completeness, clarity, feasibility, etc.
    description: str
    recommendation: Optional[str] = None
    auto_fixable: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'severity': self.severity,
            'category': self.category,
            'description': self.description,
            'recommendation': self.recommendation,
            'auto_fixable': self.auto_fixable,
        }


@dataclass
class ValidationGateResult:
    """Result of validation gate check."""
    gate_level: GateLevel
    gate_id: str
    status: GateStatus

    # Scoring
    confidence_score: ConfidenceScore
    threshold: float  # Required threshold (e.g., 0.90)

    # Issues
    issues: List[ValidationIssue] = field(default_factory=list)

    # Recommendations
    recommendations: List[str] = field(default_factory=list)

    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)
    bypassed_reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def passed(self) -> bool:
        """Check if gate passed."""
        return (
            self.status == GateStatus.PASSED or
            self.status == GateStatus.BYPASSED
        )

    def get_critical_issues(self) -> List[ValidationIssue]:
        """Get critical issues."""
        return [i for i in self.issues if i.severity == "critical"]

    def get_high_issues(self) -> List[ValidationIssue]:
        """Get high severity issues."""
        return [i for i in self.issues if i.severity in ["critical", "high"]]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'gate_level': self.gate_level.value,
            'gate_id': self.gate_id,
            'status': self.status.value,
            'confidence_score': self.confidence_score.to_dict(),
            'threshold': self.threshold,
            'issues': [issue.to_dict() for issue in self.issues],
            'recommendations': self.recommendations,
            'timestamp': self.timestamp.isoformat(),
            'bypassed_reason': self.bypassed_reason,
            'metadata': self.metadata,
        }


@dataclass
class ValidationGate:
    """Validation gate configuration."""
    id: str
    level: GateLevel
    threshold: float = 0.90  # Default ≥90% confidence

    # Gate behavior
    allow_bypass: bool = False
    stop_on_failure: bool = True

    # Validation rules
    required_components: List[str] = field(default_factory=list)
    custom_validators: List[Any] = field(default_factory=list)

    # Metadata
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'level': self.level.value,
            'threshold': self.threshold,
            'allow_bypass': self.allow_bypass,
            'stop_on_failure': self.stop_on_failure,
            'required_components': self.required_components,
            'description': self.description,
            'metadata': self.metadata,
        }
