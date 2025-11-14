"""
Shannon CLI V3.0 - Sample Data Generator

Generate realistic sample analytics data for development and testing.

Usage:
    python -m shannon.analytics.sample_data [--sessions N] [--db-path PATH]

Example:
    python -m shannon.analytics.sample_data --sessions 50
"""

import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(src_path))

from shannon.analytics import AnalyticsDatabase, TrendAnalyzer, InsightsGenerator


def generate_sample_sessions(db: AnalyticsDatabase, count: int = 30):
    """
    Generate sample analysis sessions with realistic data.

    Args:
        db: AnalyticsDatabase instance
        count: Number of sessions to generate
    """
    print(f"Generating {count} sample sessions...")

    # Domain pools
    domains = ['Frontend', 'Backend', 'Analytics', 'DevOps', 'CLI', 'UI', 'Mobile', 'API']
    interpretations = ['simple', 'moderate', 'complex']
    mcp_names = ['serena', 'context7', 'sequential', 'sqlite', 'github', 'tavily', 'pypi']

    base_date = datetime.now()

    for i in range(count):
        # Generate complexity score with some variation
        complexity = round(random.uniform(0.15, 0.95), 2)

        # Determine interpretation
        if complexity < 0.35:
            interpretation = 'simple'
        elif complexity < 0.65:
            interpretation = 'moderate'
        else:
            interpretation = 'complex'

        # Generate 8 dimensions that sum to complexity
        dimensions = {
            'structural': {
                'score': round(random.uniform(0.3, 0.8), 2),
                'weight': 0.20,
                'contribution': 0.0
            },
            'cognitive': {
                'score': round(random.uniform(0.3, 0.9), 2),
                'weight': 0.15,
                'contribution': 0.0
            },
            'coordination': {
                'score': round(random.uniform(0.2, 1.0), 2),
                'weight': 0.15,
                'contribution': 0.0
            },
            'temporal': {
                'score': round(random.uniform(0.1, 0.6), 2),
                'weight': 0.10,
                'contribution': 0.0
            },
            'technical': {
                'score': round(random.uniform(0.4, 0.95), 2),
                'weight': 0.15,
                'contribution': 0.0
            },
            'scale': {
                'score': round(random.uniform(0.2, 0.7), 2),
                'weight': 0.10,
                'contribution': 0.0
            },
            'uncertainty': {
                'score': round(random.uniform(0.05, 0.5), 2),
                'weight': 0.10,
                'contribution': 0.0
            },
            'dependencies': {
                'score': round(random.uniform(0.1, 0.6), 2),
                'weight': 0.05,
                'contribution': 0.0
            }
        }

        # Calculate contributions
        for dim_name, dim_data in dimensions.items():
            dim_data['contribution'] = round(dim_data['score'] * dim_data['weight'], 3)

        # Generate domain distribution (must sum to 100)
        num_domains = random.randint(3, 6)
        selected_domains = random.sample(domains, num_domains)

        # Generate random percentages that sum to 100
        percentages = [random.randint(5, 40) for _ in range(num_domains)]
        total = sum(percentages)
        normalized = {
            domain: int((p / total) * 100)
            for domain, p in zip(selected_domains, percentages)
        }

        # Adjust to ensure sum is exactly 100
        diff = 100 - sum(normalized.values())
        if diff != 0:
            normalized[selected_domains[0]] += diff

        # Generate timeline and cost
        if interpretation == 'simple':
            timeline_days = random.randint(5, 20)
            cost = round(random.uniform(5.0, 25.0), 2)
        elif interpretation == 'moderate':
            timeline_days = random.randint(15, 40)
            cost = round(random.uniform(20.0, 60.0), 2)
        else:
            timeline_days = random.randint(35, 80)
            cost = round(random.uniform(50.0, 150.0), 2)

        # Create session
        session_id = f"sample_session_{i:04d}"
        project_id = f"project_{random.choice(['A', 'B', 'C', 'D'])}"

        analysis_result = {
            'spec_hash': f"hash_{random.randint(100000, 999999)}",
            'complexity_score': complexity,
            'interpretation': interpretation,
            'timeline_days': timeline_days,
            'estimated_cost': cost,
            'dimensions': dimensions,
            'domains': normalized
        }

        # Record session with varying dates
        db.record_session(
            session_id=session_id,
            analysis_result=analysis_result,
            has_context=random.choice([True, False]),
            project_id=project_id
        )

        # Update created_at to spread over last 6 months
        days_ago = random.randint(0, 180)
        target_date = base_date - timedelta(days=days_ago)

        with db._get_connection() as conn:
            conn.execute("""
                UPDATE sessions
                SET created_at = ?
                WHERE session_id = ?
            """, (target_date, session_id))

        # Some sessions have actual timelines (60% completion rate)
        if random.random() < 0.6:
            # Actual timelines are typically 0.8x to 1.5x estimate
            multiplier = random.uniform(0.8, 1.5)
            actual = int(timeline_days * multiplier)
            db.update_session_actual_timeline(session_id, actual)

        # Record waves for some sessions (40% use waves)
        if random.random() < 0.4:
            num_waves = random.randint(2, 4)
            for wave_num in range(1, num_waves + 1):
                db.record_wave(
                    session_id=session_id,
                    wave_number=wave_num,
                    agent_count=random.randint(2, 5),
                    duration_minutes=round(random.uniform(20.0, 90.0), 1),
                    cost_usd=round(random.uniform(3.0, 25.0), 2),
                    speedup_factor=round(random.uniform(1.5, 3.0), 2)
                )

        # Record MCP usage
        num_mcps = random.randint(2, 5)
        for mcp in random.sample(mcp_names, num_mcps):
            installed = random.random() < 0.7  # 70% install rate
            used = installed and (random.random() < 0.8)  # 80% usage if installed

            db.record_mcp_usage(
                session_id=session_id,
                mcp_name=mcp,
                installed=installed,
                used=used
            )

        # Record cost savings
        if random.random() < 0.5:
            db.record_cost_saving(
                session_id=session_id,
                saving_type='cache_hit',
                amount_usd=round(random.uniform(1.0, 10.0), 2)
            )

        if random.random() < 0.3:
            db.record_cost_saving(
                session_id=session_id,
                saving_type='model_optimization',
                amount_usd=round(random.uniform(2.0, 15.0), 2)
            )

        if i % 10 == 0:
            print(f"  Generated {i+1}/{count} sessions...")

    print(f"✓ Generated {count} sample sessions")


def print_summary(db: AnalyticsDatabase):
    """Print summary statistics of generated data."""
    print("\n" + "="*60)
    print("DATABASE SUMMARY")
    print("="*60)

    total_sessions = db.get_total_sessions()
    total_cost = db.get_total_cost()

    print(f"\nSessions: {total_sessions}")
    print(f"Total Cost: ${total_cost:.2f}")

    # Complexity distribution
    print("\nComplexity Distribution:")
    with db._get_connection() as conn:
        dist = conn.execute("""
            SELECT interpretation, COUNT(*) as count
            FROM sessions
            GROUP BY interpretation
        """).fetchall()

        for row in dist:
            print(f"  {row['interpretation'].capitalize()}: {row['count']}")

    # Domain analysis
    analyzer = TrendAnalyzer(db)
    distribution = analyzer.get_domain_distribution()

    print("\nTop Domains:")
    sorted_domains = sorted(
        distribution.items(),
        key=lambda x: x[1]['avg'],
        reverse=True
    )[:5]

    for domain, stats in sorted_domains:
        print(f"  {domain}: {stats['avg']:.1f}% avg ({stats['count']} sessions)")

    # Generate insights
    print("\n" + "="*60)
    print("INSIGHTS")
    print("="*60)

    insights_gen = InsightsGenerator(db, analyzer)
    insights = insights_gen.generate_all_insights()

    if insights:
        for insight in insights:
            print(f"\n[{insight.severity.upper()}] {insight.title}")
            print(f"  {insight.description}")
            print(f"  → {insight.recommendation}")
    else:
        print("\nNo insights generated (need more data)")

    print("\n" + "="*60)


def main():
    """Main entry point for sample data generation."""
    parser = argparse.ArgumentParser(
        description="Generate sample analytics data for Shannon CLI development"
    )
    parser.add_argument(
        '--sessions',
        type=int,
        default=30,
        help='Number of sessions to generate (default: 30)'
    )
    parser.add_argument(
        '--db-path',
        type=Path,
        default=None,
        help='Database path (default: ~/.shannon/analytics.db)'
    )

    args = parser.parse_args()

    # Initialize database
    if args.db_path:
        db_path = args.db_path
    else:
        db_path = Path.home() / ".shannon" / "analytics_dev.db"

    print(f"Database: {db_path}")

    # Remove existing database for fresh start
    if db_path.exists():
        print(f"Removing existing database...")
        db_path.unlink()

    # Create database
    db = AnalyticsDatabase(db_path=db_path)

    # Generate sample data
    generate_sample_sessions(db, count=args.sessions)

    # Print summary
    print_summary(db)

    print(f"\n✓ Sample data generated at: {db_path}")
    print("\nYou can now test analytics features with realistic data!")


if __name__ == "__main__":
    main()
