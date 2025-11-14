"""
Shannon CLI V3.0 - Analytics Trends

Complexity trend calculations, domain evolution analysis,
timeline accuracy metrics, and cost analysis.
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import math
import statistics


@dataclass
class ComplexityTrend:
    """Complexity trend over time."""
    month: str
    avg_complexity: float
    session_count: int
    interpretation: str  # trending up/down/stable


@dataclass
class TimelineAccuracy:
    """Timeline estimation accuracy metrics."""
    overall_multiplier: float
    by_complexity: Dict[str, float]
    sample_size: int
    confidence: str  # high/medium/low


@dataclass
class CostAnalysis:
    """Cost analysis breakdown."""
    total_cost: float
    avg_cost_per_session: float
    by_complexity_band: Dict[str, float]
    total_savings: float
    savings_breakdown: Dict[str, float]


class TrendAnalyzer:
    """
    Analyzes trends from analytics database.

    Provides:
    - Complexity trends over time
    - Domain evolution patterns
    - Timeline accuracy analysis
    - Cost analysis by complexity band
    """

    def __init__(self, db):
        """
        Initialize trend analyzer.

        Args:
            db: AnalyticsDatabase instance
        """
        self.db = db

    # ===== Complexity Trends =====

    def get_complexity_trends(self, months: int = 6) -> List[ComplexityTrend]:
        """
        Get complexity trends over time.

        Args:
            months: Number of months to analyze

        Returns:
            List of ComplexityTrend objects showing monthly averages
        """
        cutoff = datetime.now() - timedelta(days=months * 30)

        with self.db._get_connection() as conn:
            rows = conn.execute("""
                SELECT
                    strftime('%Y-%m', created_at) as month,
                    AVG(complexity_score) as avg_complexity,
                    COUNT(*) as session_count
                FROM sessions
                WHERE created_at >= ?
                GROUP BY month
                ORDER BY month
            """, (cutoff,)).fetchall()

        trends = []
        for i, row in enumerate(rows):
            # Determine trend direction
            if i > 0:
                prev_avg = rows[i - 1]['avg_complexity']
                curr_avg = row['avg_complexity']

                if curr_avg > prev_avg * 1.1:
                    interpretation = "trending_up"
                elif curr_avg < prev_avg * 0.9:
                    interpretation = "trending_down"
                else:
                    interpretation = "stable"
            else:
                interpretation = "stable"

            trends.append(ComplexityTrend(
                month=row['month'],
                avg_complexity=row['avg_complexity'],
                session_count=row['session_count'],
                interpretation=interpretation
            ))

        return trends

    def get_complexity_distribution(self) -> Dict[str, int]:
        """
        Get distribution of sessions by complexity interpretation.

        Returns:
            Dict mapping interpretation to count
            Example: {'simple': 10, 'moderate': 15, 'complex': 5}
        """
        with self.db._get_connection() as conn:
            rows = conn.execute("""
                SELECT interpretation, COUNT(*) as count
                FROM sessions
                GROUP BY interpretation
            """).fetchall()

        return {row['interpretation']: row['count'] for row in rows}

    # ===== Domain Evolution =====

    def get_domain_distribution(self) -> Dict[str, Dict[str, Any]]:
        """
        Get typical domain distribution with statistics.

        Returns:
            Dict mapping domain to stats (avg, stddev, count)
            Example: {
                'Frontend': {'avg': 35.5, 'stddev': 5.2, 'count': 20},
                'Backend': {'avg': 30.0, 'stddev': 8.1, 'count': 20}
            }
        """
        with self.db._get_connection() as conn:
            rows = conn.execute("""
                SELECT
                    domain,
                    AVG(percentage) as avg_percentage,
                    COUNT(*) as count
                FROM domains
                GROUP BY domain
            """).fetchall()

            result = {}
            for row in rows:
                domain = row['domain']

                # Get all percentages for this domain to calculate stddev
                percentages = conn.execute("""
                    SELECT percentage FROM domains WHERE domain = ?
                """, (domain,)).fetchall()

                percentage_values = [p['percentage'] for p in percentages]

                stddev = (
                    statistics.stdev(percentage_values)
                    if len(percentage_values) > 1
                    else 0.0
                )

                result[domain] = {
                    'avg': row['avg_percentage'],
                    'stddev': stddev,
                    'count': row['count']
                }

        return result

    def get_domain_trends(
        self,
        domain: str,
        months: int = 6
    ) -> List[Dict[str, Any]]:
        """
        Get trend for specific domain over time.

        Args:
            domain: Domain name to analyze
            months: Number of months to analyze

        Returns:
            List of dicts with month, avg_percentage, session_count
        """
        cutoff = datetime.now() - timedelta(days=months * 30)

        with self.db._get_connection() as conn:
            rows = conn.execute("""
                SELECT
                    strftime('%Y-%m', s.created_at) as month,
                    AVG(d.percentage) as avg_percentage,
                    COUNT(*) as session_count
                FROM domains d
                JOIN sessions s ON d.session_id = s.session_id
                WHERE d.domain = ? AND s.created_at >= ?
                GROUP BY month
                ORDER BY month
            """, (domain, cutoff)).fetchall()

        return [dict(row) for row in rows]

    # ===== Timeline Accuracy =====

    def get_timeline_accuracy(self) -> TimelineAccuracy:
        """
        Analyze timeline estimation accuracy.

        Returns:
            TimelineAccuracy with multiplier to apply to estimates
        """
        with self.db._get_connection() as conn:
            rows = conn.execute("""
                SELECT
                    timeline_days as estimated,
                    actual_timeline_days as actual,
                    complexity_score,
                    interpretation
                FROM sessions
                WHERE actual_timeline_days IS NOT NULL
            """).fetchall()

        if not rows:
            return TimelineAccuracy(
                overall_multiplier=1.0,
                by_complexity={},
                sample_size=0,
                confidence='low'
            )

        # Calculate average ratio: actual / estimated
        ratios = [
            row['actual'] / row['estimated']
            for row in rows
            if row['estimated'] > 0
        ]

        if not ratios:
            return TimelineAccuracy(
                overall_multiplier=1.0,
                by_complexity={},
                sample_size=0,
                confidence='low'
            )

        avg_ratio = statistics.mean(ratios)

        # By complexity band
        by_complexity = {}
        for band in ['simple', 'moderate', 'complex']:
            band_rows = [
                r for r in rows
                if r['interpretation'] == band
            ]

            if band_rows:
                band_ratios = [
                    r['actual'] / r['estimated']
                    for r in band_rows
                    if r['estimated'] > 0
                ]

                if band_ratios:
                    by_complexity[band] = statistics.mean(band_ratios)

        # Determine confidence level
        if len(ratios) >= 10:
            confidence = 'high'
        elif len(ratios) >= 5:
            confidence = 'medium'
        else:
            confidence = 'low'

        return TimelineAccuracy(
            overall_multiplier=avg_ratio,
            by_complexity=by_complexity,
            sample_size=len(ratios),
            confidence=confidence
        )

    # ===== Cost Analysis =====

    def get_cost_analysis(self) -> CostAnalysis:
        """
        Analyze costs with breakdown by complexity.

        Returns:
            CostAnalysis with total costs, averages, and savings
        """
        with self.db._get_connection() as conn:
            # Total cost
            total = conn.execute("""
                SELECT SUM(cost_total_usd) as total FROM sessions
            """).fetchone()

            total_cost = total['total'] if total and total['total'] else 0.0

            # Average cost per session
            avg = conn.execute("""
                SELECT AVG(cost_total_usd) as avg FROM sessions
            """).fetchone()

            avg_cost = avg['avg'] if avg and avg['avg'] else 0.0

            # Cost by complexity band
            by_band = conn.execute("""
                SELECT
                    interpretation,
                    AVG(cost_total_usd) as avg_cost
                FROM sessions
                GROUP BY interpretation
            """).fetchall()

            by_complexity_band = {
                row['interpretation']: row['avg_cost']
                for row in by_band
            }

            # Total savings
            savings = conn.execute("""
                SELECT SUM(amount_usd) as total FROM cost_savings
            """).fetchone()

            total_savings = savings['total'] if savings and savings['total'] else 0.0

            # Savings breakdown by type
            savings_breakdown_rows = conn.execute("""
                SELECT
                    saving_type,
                    SUM(amount_usd) as total
                FROM cost_savings
                GROUP BY saving_type
            """).fetchall()

            savings_breakdown = {
                row['saving_type']: row['total']
                for row in savings_breakdown_rows
            }

        return CostAnalysis(
            total_cost=total_cost,
            avg_cost_per_session=avg_cost,
            by_complexity_band=by_complexity_band,
            total_savings=total_savings,
            savings_breakdown=savings_breakdown
        )

    def get_wave_performance(self) -> Dict[str, Any]:
        """
        Analyze wave execution performance.

        Returns:
            Dict with average speedup, agent counts, costs
        """
        with self.db._get_connection() as conn:
            stats = conn.execute("""
                SELECT
                    AVG(speedup_factor) as avg_speedup,
                    AVG(agent_count) as avg_agents,
                    AVG(cost_usd) as avg_cost,
                    AVG(duration_minutes) as avg_duration,
                    COUNT(*) as total_waves
                FROM wave_executions
                WHERE speedup_factor IS NOT NULL
            """).fetchone()

            if not stats or stats['total_waves'] == 0:
                return {
                    'avg_speedup': 0.0,
                    'avg_agents': 0.0,
                    'avg_cost': 0.0,
                    'avg_duration': 0.0,
                    'total_waves': 0
                }

            return dict(stats)

    # ===== MCP Usage Analysis =====

    def get_mcp_usage_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Analyze MCP usage patterns.

        Returns:
            Dict mapping MCP name to usage stats
            Example: {
                'serena': {
                    'recommended': 10,
                    'installed': 8,
                    'used': 7,
                    'install_rate': 0.8,
                    'usage_rate': 0.875
                }
            }
        """
        with self.db._get_connection() as conn:
            rows = conn.execute("""
                SELECT
                    mcp_name,
                    COUNT(*) as recommended_count,
                    SUM(CASE WHEN installed THEN 1 ELSE 0 END) as installed_count,
                    SUM(CASE WHEN used THEN 1 ELSE 0 END) as used_count
                FROM mcp_usage
                GROUP BY mcp_name
            """).fetchall()

        result = {}
        for row in rows:
            recommended = row['recommended_count']
            installed = row['installed_count']
            used = row['used_count']

            result[row['mcp_name']] = {
                'recommended': recommended,
                'installed': installed,
                'used': used,
                'install_rate': installed / recommended if recommended > 0 else 0.0,
                'usage_rate': used / installed if installed > 0 else 0.0
            }

        return result
