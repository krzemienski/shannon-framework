"""
Shannon CLI V3.0 - Analytics Module

SQLite-based analytics system for historical tracking, trends, and insights.

Main components:
- AnalyticsDatabase: SQLite database with CRUD operations
- TrendAnalyzer: Complexity trends, domain evolution, timeline accuracy
- InsightsGenerator: ML-powered recommendations and actionable suggestions

Usage:
    from shannon.analytics import AnalyticsDatabase, TrendAnalyzer, InsightsGenerator

    # Initialize database
    db = AnalyticsDatabase()

    # Record session
    db.record_session(
        session_id="analysis_20250113_194500",
        analysis_result={
            'complexity_score': 0.60,
            'interpretation': 'complex',
            'timeline_days': 50,
            'estimated_cost': 45.0,
            'dimensions': {...},
            'domains': {...}
        }
    )

    # Analyze trends
    analyzer = TrendAnalyzer(db)
    trends = analyzer.get_complexity_trends(months=6)

    # Generate insights
    insights_gen = InsightsGenerator(db, analyzer)
    insights = insights_gen.generate_all_insights()
"""

from .database import AnalyticsDatabase
from .trends import TrendAnalyzer, ComplexityTrend, TimelineAccuracy, CostAnalysis
from .insights import InsightsGenerator, Insight

__all__ = [
    'AnalyticsDatabase',
    'TrendAnalyzer',
    'InsightsGenerator',
    'ComplexityTrend',
    'TimelineAccuracy',
    'CostAnalysis',
    'Insight',
]
