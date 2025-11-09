"""Pydantic data models for Shannon CLI"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime


class ComplexityBand(str, Enum):
    """Complexity interpretation bands"""

    TRIVIAL = "trivial"  # 0.00-0.25
    SIMPLE = "simple"  # 0.25-0.40
    MODERATE = "moderate"  # 0.40-0.60
    COMPLEX = "complex"  # 0.60-0.75
    HIGH = "high"  # 0.75-0.85
    CRITICAL = "critical"  # 0.85-1.00


class DimensionScore(BaseModel):
    """Score for one complexity dimension"""

    dimension: str
    score: float = Field(ge=0.0, le=1.0, description="Dimension score 0.0-1.0")
    weight: float = Field(description="Weight in total calculation")
    contribution: float = Field(description="score * weight")
    details: Dict[str, Any] = Field(default_factory=dict)


class MCPRecommendation(BaseModel):
    """MCP server recommendation"""

    name: str
    tier: int = Field(
        ge=1, le=4, description="1=Mandatory, 2=Primary, 3=Secondary, 4=Optional"
    )
    purpose: str
    priority: str  # REQUIRED, RECOMMENDED, OPTIONAL
    usage: Optional[str] = None
    fallback: Optional[str] = None


class Phase(BaseModel):
    """One of 5 implementation phases"""

    phase_number: int = Field(ge=1, le=5)
    phase_name: str
    objectives: List[str]
    deliverables: List[str]
    validation_gate: List[str]
    duration_percent: int
    duration_estimate: str


class AnalysisResult(BaseModel):
    """Complete specification analysis result"""

    analysis_id: str
    complexity_score: float = Field(ge=0.10, le=0.95)
    interpretation: ComplexityBand
    dimension_scores: Dict[str, DimensionScore]
    domain_percentages: Dict[str, int]
    mcp_recommendations: List[MCPRecommendation]
    phase_plan: List[Phase]
    execution_strategy: str
    timeline_estimate: str
    analyzed_at: datetime = Field(default_factory=datetime.now)

    @field_validator("domain_percentages")
    @classmethod
    def domains_must_sum_to_100(cls, v: Dict[str, int]) -> Dict[str, int]:
        """Enforce Shannon requirement: domains sum to exactly 100%"""
        total = sum(v.values())
        if total != 100:
            raise ValueError(f"Domain percentages must sum to 100%, got {total}%")
        return v

    @field_validator("phase_plan")
    @classmethod
    def must_have_5_phases(cls, v: List[Phase]) -> List[Phase]:
        """Enforce Shannon requirement: exactly 5 phases"""
        if len(v) != 5:
            raise ValueError(f"Must have exactly 5 phases, got {len(v)}")
        return v

    def to_dict(self) -> Dict:
        """Serialize for JSON storage"""
        return self.model_dump()


class WaveTask(BaseModel):
    """Single task within a wave"""

    task_id: str
    name: str
    agent_type: str
    description: str
    dependencies: List[str] = Field(default_factory=list)
    estimated_minutes: int
    deliverables: List[str] = Field(default_factory=list)


class Wave(BaseModel):
    """Wave containing multiple parallel tasks"""

    wave_number: int
    wave_name: str
    tasks: List[WaveTask]
    parallel: bool = True
    depends_on: List[int] = Field(default_factory=list)


class WaveResult(BaseModel):
    """Results after wave execution"""

    wave_number: int
    wave_name: str
    agents_deployed: int
    execution_time_minutes: float
    files_created: List[str]
    components_built: List[str]
    decisions_made: List[str]
    tests_created: int
    no_mocks_confirmed: bool
    quality_metrics: Dict[str, Any]
    completed_at: datetime = Field(default_factory=datetime.now)
