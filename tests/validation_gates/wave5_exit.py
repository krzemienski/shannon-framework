"""
Wave 5 Exit Gate: Persistent Analytics Engine Validation

Runs all 6 Wave 5 functional tests to validate:
- Analytics database schema and migrations
- Metrics collection and storage
- Time-series analysis queries
- Aggregation and reporting
- Database performance and indexing
- Data export and visualization

Requires 100% pass rate to proceed to Wave 6.

Part of Shannon V3 Wave 5: Persistent Analytics Engine
"""

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from validation_gates.gate_framework import ValidationGate
from cli_functional.test_wave5_analytics import TestWave5Analytics


async def wave5_exit_gate() -> bool:
    """
    Run Wave 5 exit gate - all 6 functional tests

    Returns:
        bool: True if all tests pass
    """
    gate = ValidationGate(phase=5, gate_type='exit')

    # Instantiate test class
    analytics_tests = TestWave5Analytics()

    # Add all 6 Wave 5 tests
    gate.add_test(analytics_tests.test_database_schema_migrations)
    gate.add_test(analytics_tests.test_metrics_collection_storage)
    gate.add_test(analytics_tests.test_timeseries_analysis)
    gate.add_test(analytics_tests.test_aggregation_reporting)
    gate.add_test(analytics_tests.test_database_performance)
    gate.add_test(analytics_tests.test_data_export_visualization)

    result = await gate.run_all_tests()
    result.display()

    return result.passed


if __name__ == '__main__':
    import asyncio
    success = asyncio.run(wave5_exit_gate())
    sys.exit(0 if success else 1)
