"""
Functional tests for Pydantic data models
NO MOCKS - Testing real model validation
"""

import pytest
from datetime import datetime


def test_analysis_result_domain_validation():
    """
    FUNCTIONAL TEST: AnalysisResult validates domain percentages
    Should reject if domains don't sum to 100%
    """
    from shannon.storage.models import (
        AnalysisResult,
        ComplexityBand,
        DimensionScore,
        Phase,
        MCPRecommendation,
    )

    # Valid domain percentages (sum to 100%)
    valid_analysis = AnalysisResult(
        analysis_id="test_valid",
        complexity_score=0.50,
        interpretation=ComplexityBand.MODERATE,
        dimension_scores={},
        domain_percentages={"Frontend": 60, "Backend": 40},  # Sums to 100
        mcp_recommendations=[],
        phase_plan=[
            Phase(
                phase_number=i,
                phase_name=f"Phase {i}",
                objectives=["test"],
                deliverables=["test"],
                validation_gate=["test"],
                duration_percent=20,
                duration_estimate="1 day",
            )
            for i in range(1, 6)
        ],
        execution_strategy="sequential",
        timeline_estimate="1 day",
    )
    assert valid_analysis.analysis_id == "test_valid"

    # Invalid domain percentages (sum to 90% only)
    with pytest.raises(ValueError, match="sum to 100%"):
        AnalysisResult(
            analysis_id="test_invalid",
            complexity_score=0.50,
            interpretation=ComplexityBand.MODERATE,
            dimension_scores={},
            domain_percentages={"Frontend": 50, "Backend": 40},  # Only 90%
            mcp_recommendations=[],
            phase_plan=[
                Phase(
                    phase_number=i,
                    phase_name=f"Phase {i}",
                    objectives=["test"],
                    deliverables=["test"],
                    validation_gate=["test"],
                    duration_percent=20,
                    duration_estimate="1 day",
                )
                for i in range(1, 6)
            ],
            execution_strategy="sequential",
            timeline_estimate="1 day",
        )


def test_complexity_score_range_validation():
    """Score must be in [0.10, 0.95] range"""
    from shannon.storage.models import (
        AnalysisResult,
        ComplexityBand,
        Phase,
    )

    # Too high
    with pytest.raises(ValueError):
        AnalysisResult(
            analysis_id="test_high",
            complexity_score=1.05,  # Too high
            interpretation=ComplexityBand.CRITICAL,
            dimension_scores={},
            domain_percentages={"Frontend": 100},
            mcp_recommendations=[],
            phase_plan=[
                Phase(
                    phase_number=i,
                    phase_name=f"Phase {i}",
                    objectives=["test"],
                    deliverables=["test"],
                    validation_gate=["test"],
                    duration_percent=20,
                    duration_estimate="1 day",
                )
                for i in range(1, 6)
            ],
            execution_strategy="sequential",
            timeline_estimate="1 day",
        )

    # Too low
    with pytest.raises(ValueError):
        AnalysisResult(
            analysis_id="test_low",
            complexity_score=0.05,  # Too low
            interpretation=ComplexityBand.TRIVIAL,
            dimension_scores={},
            domain_percentages={"Frontend": 100},
            mcp_recommendations=[],
            phase_plan=[
                Phase(
                    phase_number=i,
                    phase_name=f"Phase {i}",
                    objectives=["test"],
                    deliverables=["test"],
                    validation_gate=["test"],
                    duration_percent=20,
                    duration_estimate="1 day",
                )
                for i in range(1, 6)
            ],
            execution_strategy="sequential",
            timeline_estimate="1 day",
        )


def test_phase_count_validation():
    """Must have exactly 5 phases"""
    from shannon.storage.models import (
        AnalysisResult,
        ComplexityBand,
        Phase,
    )

    # Only 3 phases (should fail)
    with pytest.raises(ValueError, match="exactly 5 phases"):
        AnalysisResult(
            analysis_id="test_phases",
            complexity_score=0.50,
            interpretation=ComplexityBand.MODERATE,
            dimension_scores={},
            domain_percentages={"Frontend": 100},
            mcp_recommendations=[],
            phase_plan=[
                Phase(
                    phase_number=i,
                    phase_name=f"Phase {i}",
                    objectives=["test"],
                    deliverables=["test"],
                    validation_gate=["test"],
                    duration_percent=33,
                    duration_estimate="1 day",
                )
                for i in range(1, 4)  # Only 3 phases
            ],
            execution_strategy="sequential",
            timeline_estimate="1 day",
        )


def test_dimension_score_range():
    """DimensionScore must have score in [0.0, 1.0] range"""
    from shannon.storage.models import DimensionScore

    # Valid score
    dim = DimensionScore(
        dimension="structural",
        score=0.50,
        weight=0.20,
        contribution=0.10,
        details={},
    )
    assert dim.score == 0.50

    # Invalid score (too high)
    with pytest.raises(ValueError):
        DimensionScore(
            dimension="structural",
            score=1.50,  # Too high
            weight=0.20,
            contribution=0.30,
            details={},
        )


def test_mcp_recommendation_tier_validation():
    """MCP tier must be in [1, 4] range"""
    from shannon.storage.models import MCPRecommendation

    # Valid tier
    mcp = MCPRecommendation(
        name="Serena MCP",
        tier=1,
        purpose="Context preservation",
        priority="REQUIRED",
    )
    assert mcp.tier == 1

    # Invalid tier (too high)
    with pytest.raises(ValueError):
        MCPRecommendation(
            name="Invalid MCP",
            tier=5,  # Invalid (must be 1-4)
            purpose="Test",
            priority="OPTIONAL",
        )
