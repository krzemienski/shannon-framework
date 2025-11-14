"""
Shannon CLI V3.0 - Analytics Insights

ML-powered recommendations, pattern matching for insights,
comparison to industry averages, and actionable suggestions.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Insight:
    """Actionable insight from analytics."""
    type: str  # timeline_accuracy, mcp_usage, cost_optimization, domain_pattern
    severity: str  # low, medium, high
    title: str
    description: str
    recommendation: str
    data: Dict[str, Any]


class InsightsGenerator:
    """
    Generate actionable insights from analytics data.

    Insights types:
    - Timeline accuracy adjustments
    - Cost optimization opportunities
    - MCP usage recommendations
    - Domain-specific patterns
    """

    def __init__(self, db, trend_analyzer):
        """
        Initialize insights generator.

        Args:
            db: AnalyticsDatabase instance
            trend_analyzer: TrendAnalyzer instance
        """
        self.db = db
        self.trend_analyzer = trend_analyzer

    def generate_all_insights(self) -> List[Insight]:
        """
        Generate all available insights.

        Returns:
            List of Insight objects ordered by severity
        """
        insights = []

        # Timeline accuracy insight
        timeline_insight = self._timeline_accuracy_insight()
        if timeline_insight:
            insights.append(timeline_insight)

        # MCP usage insight
        mcp_insight = self._mcp_usage_insight()
        if mcp_insight:
            insights.append(mcp_insight)

        # Cost optimization insight
        cost_insight = self._cost_optimization_insight()
        if cost_insight:
            insights.append(cost_insight)

        # Domain pattern insight
        domain_insight = self._domain_pattern_insight()
        if domain_insight:
            insights.append(domain_insight)

        # Complexity trend insight
        complexity_insight = self._complexity_trend_insight()
        if complexity_insight:
            insights.append(complexity_insight)

        # Wave performance insight
        wave_insight = self._wave_performance_insight()
        if wave_insight:
            insights.append(wave_insight)

        # Sort by severity (high -> medium -> low)
        severity_order = {'high': 0, 'medium': 1, 'low': 2}
        insights.sort(key=lambda x: severity_order.get(x.severity, 3))

        return insights

    def _timeline_accuracy_insight(self) -> Optional[Insight]:
        """
        Analyze timeline estimation accuracy.

        Returns insight if user consistently over/under estimates.
        """
        accuracy = self.trend_analyzer.get_timeline_accuracy()

        if accuracy.confidence == 'low':
            return None  # Not enough data

        multiplier = accuracy.overall_multiplier

        # Only generate insight if significantly off
        if abs(multiplier - 1.0) < 0.10:
            return None  # Estimates are accurate

        if multiplier > 1.10:
            # User underestimates
            severity = 'high' if multiplier > 1.5 else 'medium'

            return Insight(
                type='timeline_accuracy',
                severity=severity,
                title='Timeline Estimates Too Optimistic',
                description=(
                    f"Your projects typically take {multiplier:.1f}x longer "
                    f"than estimated. Consider multiplying estimates by {multiplier:.2f}."
                ),
                recommendation=(
                    f"Apply {multiplier:.2f}x multiplier to timeline estimates"
                ),
                data={
                    'multiplier': multiplier,
                    'by_complexity': accuracy.by_complexity,
                    'sample_size': accuracy.sample_size,
                    'confidence': accuracy.confidence
                }
            )
        else:
            # User overestimates
            return Insight(
                type='timeline_accuracy',
                severity='low',
                title='Timeline Estimates Conservative',
                description=(
                    f"Your projects typically complete {1/multiplier:.1f}x faster "
                    f"than estimated. You may be overestimating."
                ),
                recommendation=(
                    f"Consider using {multiplier:.2f}x multiplier (more aggressive estimates)"
                ),
                data={
                    'multiplier': multiplier,
                    'by_complexity': accuracy.by_complexity,
                    'sample_size': accuracy.sample_size,
                    'confidence': accuracy.confidence
                }
            )

    def _mcp_usage_insight(self) -> Optional[Insight]:
        """
        Analyze MCP usage patterns.

        Returns insight if user is under-utilizing MCPs.
        """
        stats = self.trend_analyzer.get_mcp_usage_stats()

        if not stats:
            return None

        underutilized = []

        for mcp_name, mcp_stats in stats.items():
            # Check if recommended often but rarely installed
            if (mcp_stats['recommended'] >= 3 and
                mcp_stats['install_rate'] < 0.5):
                underutilized.append({
                    'mcp': mcp_name,
                    'recommended': mcp_stats['recommended'],
                    'installed': mcp_stats['installed'],
                    'rate': mcp_stats['install_rate']
                })

        if not underutilized:
            return None

        return Insight(
            type='mcp_usage',
            severity='medium',
            title='Underutilized MCPs',
            description=(
                f"You're not installing {len(underutilized)} frequently "
                f"recommended MCPs. This may be limiting Shannon's capabilities."
            ),
            recommendation=(
                f"Consider installing: {', '.join(m['mcp'] for m in underutilized[:3])}"
            ),
            data={'underutilized': underutilized}
        )

    def _cost_optimization_insight(self) -> Optional[Insight]:
        """
        Analyze cost patterns and savings.

        Returns insight if significant cost optimization opportunities exist.
        """
        analysis = self.trend_analyzer.get_cost_analysis()

        # Check if savings rate is low
        if analysis.total_cost > 0:
            savings_rate = analysis.total_savings / analysis.total_cost
        else:
            savings_rate = 0.0

        # Expected savings rate: 20-30% with good optimization
        if savings_rate < 0.15 and analysis.total_cost > 10.0:
            return Insight(
                type='cost_optimization',
                severity='medium',
                title='Low Cost Optimization',
                description=(
                    f"Only {savings_rate*100:.1f}% of costs are being saved through "
                    f"optimization. Industry average is 25-30%."
                ),
                recommendation=(
                    "Enable caching and context management for better cost savings. "
                    "Use 'shannon onboard' to build context cache."
                ),
                data={
                    'total_cost': analysis.total_cost,
                    'total_savings': analysis.total_savings,
                    'savings_rate': savings_rate,
                    'savings_breakdown': analysis.savings_breakdown
                }
            )

        return None

    def _domain_pattern_insight(self) -> Optional[Insight]:
        """
        Analyze domain distribution patterns.

        Returns insight if domain distribution is unusual.
        """
        distribution = self.trend_analyzer.get_domain_distribution()

        if not distribution:
            return None

        # Check for extremely skewed distributions
        max_domain = max(distribution.items(), key=lambda x: x[1]['avg'])
        max_name, max_stats = max_domain

        if max_stats['avg'] > 70 and max_stats['count'] >= 5:
            # One domain dominates
            return Insight(
                type='domain_pattern',
                severity='low',
                title='Domain Concentration',
                description=(
                    f"{max_name} represents {max_stats['avg']:.0f}% of your projects. "
                    f"This specialization may benefit from domain-specific MCPs."
                ),
                recommendation=(
                    f"Consider using domain-specific MCPs for {max_name} development"
                ),
                data={
                    'dominant_domain': max_name,
                    'percentage': max_stats['avg'],
                    'all_domains': distribution
                }
            )

        return None

    def _complexity_trend_insight(self) -> Optional[Insight]:
        """
        Analyze complexity trends over time.

        Returns insight if complexity is trending significantly.
        """
        trends = self.trend_analyzer.get_complexity_trends(months=6)

        if len(trends) < 3:
            return None  # Need at least 3 months of data

        # Check last 3 months for consistent trend
        recent = trends[-3:]
        trending_up = all(t.interpretation == 'trending_up' for t in recent)
        trending_down = all(t.interpretation == 'trending_down' for t in recent)

        if trending_up:
            return Insight(
                type='complexity_trend',
                severity='medium',
                title='Project Complexity Increasing',
                description=(
                    "Your project complexity has been trending up for 3 months. "
                    "This may indicate scope creep or increasing technical debt."
                ),
                recommendation=(
                    "Review project scope and consider breaking into smaller components"
                ),
                data={'trends': [t.__dict__ for t in recent]}
            )

        if trending_down:
            return Insight(
                type='complexity_trend',
                severity='low',
                title='Project Complexity Decreasing',
                description=(
                    "Your project complexity has been trending down. "
                    "This suggests better planning or simpler requirements."
                ),
                recommendation=(
                    "Continue current planning approach"
                ),
                data={'trends': [t.__dict__ for t in recent]}
            )

        return None

    def _wave_performance_insight(self) -> Optional[Insight]:
        """
        Analyze wave execution performance.

        Returns insight if wave execution could be improved.
        """
        perf = self.trend_analyzer.get_wave_performance()

        if perf['total_waves'] < 3:
            return None  # Need more data

        avg_speedup = perf['avg_speedup']

        # Expected speedup: 2.0-2.5x for well-structured waves
        if avg_speedup < 1.5:
            return Insight(
                type='wave_performance',
                severity='medium',
                title='Low Wave Speedup',
                description=(
                    f"Your waves achieve only {avg_speedup:.1f}x speedup on average. "
                    f"Expected is 2.0-2.5x with good parallelization."
                ),
                recommendation=(
                    "Review wave planning to ensure better task parallelization. "
                    "Consider breaking tasks into more independent units."
                ),
                data=perf
            )

        if avg_speedup > 2.5:
            return Insight(
                type='wave_performance',
                severity='low',
                title='Excellent Wave Performance',
                description=(
                    f"Your waves achieve {avg_speedup:.1f}x speedup on average. "
                    f"This is excellent parallelization."
                ),
                recommendation=(
                    "Continue current wave planning approach"
                ),
                data=perf
            )

        return None
