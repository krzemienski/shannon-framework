"""
Shannon CLI Data Models

Pydantic v2 models for Shannon Framework data structures.
All models include comprehensive validation to enforce Shannon requirements.

Created for: Wave 1 - Foundation & Infrastructure
Component: Data & Storage Specialist
"""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class ComplexityBand(str, Enum):
    """
    Complexity interpretation bands for Shannon 8D scores.

    Bands:
        TRIVIAL: 0.00-0.25 - Minimal complexity
        SIMPLE: 0.25-0.40 - Low complexity
        MODERATE: 0.40-0.60 - Medium complexity
        COMPLEX: 0.60-0.75 - High complexity
        HIGH: 0.75-0.85 - Very high complexity
        CRITICAL: 0.85-1.00 - Extreme complexity
    """

    TRIVIAL = "trivial"        # 0.00-0.25
    SIMPLE = "simple"          # 0.25-0.40
    MODERATE = "moderate"      # 0.40-0.60
    COMPLEX = "complex"        # 0.60-0.75
    HIGH = "high"              # 0.75-0.85
    CRITICAL = "critical"      # 0.85-1.00


class DimensionScore(BaseModel):
    """
    Score for one of the 8 Shannon complexity dimensions.

    Dimensions:
        - structural: Code organization complexity
        - cognitive: Understanding difficulty
        - coordination: Team/component coordination needs
        - temporal: Time-based dependencies
        - technical: Technical stack complexity
        - scale: Size and scope impact
        - uncertainty: Unknown factors and risks
        - dependencies: External dependencies impact

    Attributes:
        dimension: Name of the dimension
        score: Normalized score (0.0-1.0)
        weight: Weight in total calculation (e.g., 0.20 for 20%)
        contribution: Calculated as score × weight
        details: Additional calculation metadata
    """

    dimension: str = Field(
        description="Dimension name (structural, cognitive, coordination, temporal, technical, scale, uncertainty, dependencies)"
    )

    score: float = Field(
        ge=0.0,
        le=1.0,
        description="Dimension score 0.0-1.0"
    )

    weight: float = Field(
        description="Weight in total calculation (e.g., 0.20 for 20%)"
    )

    contribution: float = Field(
        description="score × weight (contribution to total complexity)"
    )

    details: Dict[str, Any] = Field(
        default_factory=dict,
        description="Calculation details (file_count, regex matches, etc.)"
    )

    @model_validator(mode='after')
    def validate_contribution(self) -> 'DimensionScore':
        """
        Verify contribution = score × weight within tolerance.

        Raises:
            ValueError: If contribution doesn't match score × weight
        """
        expected_contribution = self.score * self.weight
        if abs(self.contribution - expected_contribution) > 0.001:
            raise ValueError(
                f"Contribution {self.contribution} != score×weight "
                f"({self.score}×{self.weight}={expected_contribution})"
            )
        return self


class MCPRecommendation(BaseModel):
    """
    MCP (Model Context Protocol) server recommendation.

    Tiered recommendation system:
        Tier 1: Mandatory - Core functionality
        Tier 2: Primary - Essential features
        Tier 3: Secondary - Enhanced functionality
        Tier 4: Optional - Nice-to-have additions

    Attributes:
        name: MCP server name
        tier: Recommendation tier (1-4)
        purpose: Why this MCP is recommended
        priority: REQUIRED, RECOMMENDED, or OPTIONAL
        usage: Optional usage guidance
        fallback: Optional fallback strategy if unavailable
    """

    name: str = Field(
        description="MCP server name (e.g., 'filesystem', 'github', 'serena')"
    )

    tier: int = Field(
        ge=1,
        le=4,
        description="1=Mandatory, 2=Primary, 3=Secondary, 4=Optional"
    )

    purpose: str = Field(
        description="Why this MCP is recommended for the project"
    )

    priority: str = Field(
        description="REQUIRED, RECOMMENDED, or OPTIONAL"
    )

    usage: Optional[str] = Field(
        default=None,
        description="How to use this MCP in the project"
    )

    fallback: Optional[str] = Field(
        default=None,
        description="Fallback strategy if MCP unavailable"
    )


class Phase(BaseModel):
    """
    One of exactly 5 implementation phases in Shannon execution.

    Shannon requirement: All projects must have exactly 5 phases.

    Attributes:
        phase_number: Phase number (1-5)
        phase_name: Descriptive phase name
        objectives: List of phase objectives
        deliverables: List of expected deliverables
        validation_gate: List of validation criteria
        duration_percent: Percentage of total timeline
        duration_estimate: Human-readable duration estimate
    """

    phase_number: int = Field(
        ge=1,
        le=5,
        description="Phase number (1-5)"
    )

    phase_name: str = Field(
        description="Descriptive name for this phase"
    )

    objectives: List[str] = Field(
        description="Phase objectives to accomplish"
    )

    deliverables: List[str] = Field(
        description="Concrete deliverables expected from this phase"
    )

    validation_gate: List[str] = Field(
        description="Validation criteria that must pass to complete phase"
    )

    duration_percent: int = Field(
        description="Percentage of total project timeline"
    )

    duration_estimate: str = Field(
        description="Human-readable duration (e.g., '2-3 days', '1 week')"
    )


class AnalysisResult(BaseModel):
    """
    Complete Shannon 8D specification analysis result.

    CRITICAL VALIDATIONS:
        1. Must have exactly 8 dimensions in dimension_scores
        2. Domain percentages must sum to exactly 100%
        3. Must have exactly 5 phases in phase_plan

    Attributes:
        analysis_id: Unique identifier (format: spec_analysis_YYYYMMDD_HHMMSS)
        complexity_score: Weighted total complexity (0.10-0.95)
        interpretation: Complexity band classification
        dimension_scores: All 8 dimension scores
        domain_percentages: Domain breakdown (must sum to 100%)
        mcp_recommendations: Tiered MCP server recommendations
        phase_plan: 5-phase implementation plan
        execution_strategy: 'sequential' or 'wave-based'
        timeline_estimate: Human-readable timeline
        analyzed_at: Analysis timestamp
    """

    analysis_id: str = Field(
        description="Unique ID (format: spec_analysis_YYYYMMDD_HHMMSS)"
    )

    complexity_score: float = Field(
        ge=0.10,
        le=0.95,
        description="Weighted total complexity (0.10-0.95)"
    )

    interpretation: ComplexityBand = Field(
        description="Complexity band classification"
    )

    dimension_scores: Dict[str, DimensionScore] = Field(
        description="All 8 dimension scores (structural, cognitive, coordination, temporal, technical, scale, uncertainty, dependencies)"
    )

    domain_percentages: Dict[str, int] = Field(
        description="Domain percentages (Frontend, Backend, Infrastructure, etc.) MUST sum to 100%"
    )

    mcp_recommendations: List[MCPRecommendation] = Field(
        description="Tiered MCP server recommendations"
    )

    phase_plan: List[Phase] = Field(
        description="5-phase implementation plan (MUST have exactly 5 phases)"
    )

    execution_strategy: str = Field(
        description="'sequential' or 'wave-based'"
    )

    timeline_estimate: str = Field(
        description="Human-readable timeline (e.g., '2-4 days', '1-2 weeks')"
    )

    analyzed_at: datetime = Field(
        default_factory=datetime.now,
        description="Analysis timestamp"
    )

    @field_validator('domain_percentages')
    @classmethod
    def domains_must_sum_to_100(cls, v: Dict[str, int]) -> Dict[str, int]:
        """
        CRITICAL VALIDATION: Domain percentages MUST sum to exactly 100%.

        Shannon requirement from spec-analysis/SKILL.md:999-1005

        Args:
            v: Domain percentages dictionary

        Returns:
            Validated domain percentages

        Raises:
            ValueError: If domains don't sum to exactly 100%
        """
        total = sum(v.values())
        if total != 100:
            raise ValueError(
                f"Domain percentages must sum to 100%, got {total}%. "
                f"Domains: {v}"
            )
        return v

    @field_validator('phase_plan')
    @classmethod
    def must_have_5_phases(cls, v: List[Phase]) -> List[Phase]:
        """
        CRITICAL VALIDATION: Must have exactly 5 phases.

        Shannon requirement from spec-analysis/SKILL.md:1007-1009

        Args:
            v: List of Phase objects

        Returns:
            Validated phase list

        Raises:
            ValueError: If not exactly 5 phases
        """
        if len(v) != 5:
            raise ValueError(
                f"Must have exactly 5 phases, got {len(v)}"
            )
        return v

    @field_validator('dimension_scores')
    @classmethod
    def must_have_8_dimensions(cls, v: Dict[str, DimensionScore]) -> Dict[str, DimensionScore]:
        """
        CRITICAL VALIDATION: Must have all 8 Shannon dimensions.

        Required dimensions:
            - structural
            - cognitive
            - coordination
            - temporal
            - technical
            - scale
            - uncertainty
            - dependencies

        Args:
            v: Dictionary of dimension scores

        Returns:
            Validated dimension scores

        Raises:
            ValueError: If not exactly 8 dimensions or missing/extra dimensions
        """
        required_dimensions = {
            'structural', 'cognitive', 'coordination', 'temporal',
            'technical', 'scale', 'uncertainty', 'dependencies'
        }

        actual_dimensions = set(v.keys())

        if actual_dimensions != required_dimensions:
            missing = required_dimensions - actual_dimensions
            extra = actual_dimensions - required_dimensions
            raise ValueError(
                f"Must have exactly 8 dimensions. "
                f"Missing: {missing}, Extra: {extra}"
            )

        return v

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize to dictionary for JSON storage.

        Returns:
            Dictionary representation of the analysis result
        """
        return self.model_dump()


class WaveTask(BaseModel):
    """
    Single task within a wave execution.

    Tasks can be executed in parallel within a wave but may have
    dependencies on other tasks in the same or previous waves.

    Attributes:
        task_id: Unique task identifier
        name: Human-readable task name
        agent_type: Type of agent to execute this task
        description: Detailed task description
        dependencies: List of task IDs this task depends on
        estimated_minutes: Estimated execution time
        deliverables: Expected outputs from this task
    """

    task_id: str = Field(
        description="Unique task identifier (e.g., 'wave_1_task_1')"
    )

    name: str = Field(
        description="Human-readable task name"
    )

    agent_type: str = Field(
        description="Agent type to execute task (e.g., 'data-storage-specialist', 'test-engineer')"
    )

    description: str = Field(
        description="Detailed task description and requirements"
    )

    dependencies: List[str] = Field(
        default_factory=list,
        description="List of task IDs this task depends on"
    )

    estimated_minutes: int = Field(
        description="Estimated execution time in minutes"
    )

    deliverables: List[str] = Field(
        default_factory=list,
        description="Expected deliverable files or components"
    )


class Wave(BaseModel):
    """
    Wave containing multiple parallel tasks.

    Waves organize work into parallelizable batches. Tasks within a wave
    can execute concurrently, but waves execute sequentially.

    Attributes:
        wave_number: Wave number in sequence
        wave_name: Descriptive wave name
        tasks: List of tasks in this wave
        parallel: Whether tasks can execute in parallel
        depends_on: List of wave numbers this wave depends on
    """

    wave_number: int = Field(
        description="Wave number in execution sequence"
    )

    wave_name: str = Field(
        description="Descriptive name for this wave"
    )

    tasks: List[WaveTask] = Field(
        description="Tasks to execute in this wave"
    )

    parallel: bool = Field(
        default=True,
        description="Whether tasks can execute in parallel"
    )

    depends_on: List[int] = Field(
        default_factory=list,
        description="List of wave numbers this wave depends on"
    )


class SessionMetadata(BaseModel):
    """
    Session metadata for tracking execution state.

    Stored in ~/.shannon/sessions/{session_id}/session.json

    Attributes:
        session_id: Unique session identifier
        created_at: Session creation timestamp
        updated_at: Last update timestamp
        project_path: Path to analyzed project (if applicable)
        current_phase: Current execution phase (if started)
        current_wave: Current wave number (if wave-based execution)
        status: Session status
        tags: Optional tags for categorization
    """

    session_id: str = Field(
        description="Unique session identifier"
    )

    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Session creation timestamp"
    )

    updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Last update timestamp"
    )

    project_path: Optional[Path] = Field(
        default=None,
        description="Path to analyzed project (if applicable)"
    )

    current_phase: Optional[int] = Field(
        default=None,
        description="Current execution phase (1-5)"
    )

    current_wave: Optional[int] = Field(
        default=None,
        description="Current wave number (for wave-based execution)"
    )

    status: str = Field(
        default="active",
        description="Session status (active, paused, complete, error)"
    )

    tags: List[str] = Field(
        default_factory=list,
        description="Optional tags for categorization"
    )

    @model_validator(mode='after')
    def update_timestamp(self) -> 'SessionMetadata':
        """Update the updated_at timestamp whenever the model is modified."""
        self.updated_at = datetime.now()
        return self


class WaveResult(BaseModel):
    """
    Results after wave execution completion.

    Stored after each wave completes to track progress and quality metrics.

    Attributes:
        wave_number: Wave number that was executed
        wave_name: Wave name
        agents_deployed: Number of agents used
        execution_time_minutes: Actual execution time
        files_created: List of files created
        components_built: List of components built
        decisions_made: Key decisions made during execution
        tests_created: Number of tests created
        no_mocks_confirmed: Whether NO MOCKS rule was followed
        quality_metrics: Additional quality metrics
    """

    wave_number: int = Field(
        description="Wave number that was executed"
    )

    wave_name: str = Field(
        description="Wave name"
    )

    agents_deployed: int = Field(
        description="Number of agents used in this wave"
    )

    execution_time_minutes: float = Field(
        description="Actual execution time in minutes"
    )

    files_created: List[str] = Field(
        default_factory=list,
        description="List of files created during wave"
    )

    components_built: List[str] = Field(
        default_factory=list,
        description="List of components/modules built"
    )

    decisions_made: List[str] = Field(
        default_factory=list,
        description="Key architectural/implementation decisions"
    )

    tests_created: int = Field(
        default=0,
        description="Number of test files/cases created"
    )

    no_mocks_confirmed: bool = Field(
        default=True,
        description="Confirmation that NO MOCKS rule was followed"
    )

    quality_metrics: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional quality metrics (coverage, type hints, etc.)"
    )


# Export all models
__all__ = [
    'ComplexityBand',
    'DimensionScore',
    'MCPRecommendation',
    'Phase',
    'AnalysisResult',
    'WaveTask',
    'Wave',
    'SessionMetadata',
    'WaveResult',
]
