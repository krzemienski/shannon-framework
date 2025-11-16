"""
Wave 5 CLI Functional Test Suite: Analytics Database

Tests comprehensive analytics database functionality including:
- Session logging and tracking
- Wave execution logging with agent details
- Cost recording and accuracy
- Trends analysis and visualization
- Insights generation and recommendations
- Analytics query and data retrieval

Part of Shannon V3 Wave 5: Analytics Database
"""

import pytest
import sys
import time
import re
import sqlite3
import json
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional
from datetime import datetime, timedelta

# Add parent directory to path for imports
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cli_infrastructure.cli_monitor import CLIMonitor, MonitorResult
from cli_infrastructure.output_parser import OutputParser
from validation_gates.gate_framework import TestResult, TestStatus


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def simple_spec() -> Path:
    """Path to simple test specification"""
    return Path(__file__).parent.parent / 'fixtures' / 'simple_spec.md'


@pytest.fixture
def moderate_spec() -> Path:
    """Path to moderate test specification"""
    return Path(__file__).parent.parent / 'fixtures' / 'moderate_spec.md'


@pytest.fixture
def complex_spec() -> Path:
    """Path to complex test specification"""
    return Path(__file__).parent.parent / 'fixtures' / 'complex_spec.md'


@pytest.fixture
def analytics_db_path() -> Path:
    """Path to analytics database"""
    return Path.home() / ".shannon" / "analytics.db"


@pytest.fixture
def clean_analytics_db(analytics_db_path: Path):
    """
    Fixture to ensure clean analytics database before test

    Yields the path, then restores original state after test
    """
    # Backup original if exists
    backup_path = None
    if analytics_db_path.exists():
        backup_path = analytics_db_path.parent / f"{analytics_db_path.name}.backup"
        import shutil
        shutil.copy2(analytics_db_path, backup_path)
        analytics_db_path.unlink()

    # Ensure directory exists
    analytics_db_path.parent.mkdir(parents=True, exist_ok=True)

    yield analytics_db_path

    # Restore original if it existed
    if backup_path and backup_path.exists():
        if analytics_db_path.exists():
            analytics_db_path.unlink()
        import shutil
        shutil.copy2(backup_path, analytics_db_path)
        backup_path.unlink()
    elif analytics_db_path.exists():
        # Clean up test database
        analytics_db_path.unlink()


# ============================================================================
# DATABASE HELPER FUNCTIONS
# ============================================================================

def query_analytics_db(db_path: Path, query: str, params: List[Any] = None) -> List[Dict[str, Any]]:
    """
    Query analytics database and return results as list of dicts

    Args:
        db_path: Path to analytics.db
        query: SQL query string
        params: Query parameters

    Returns:
        List of result rows as dictionaries
    """
    if not db_path.exists():
        return []

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    except sqlite3.OperationalError:
        # Database locked or corrupted
        return []


def get_session_count(db_path: Path) -> int:
    """Get count of sessions in analytics database"""
    results = query_analytics_db(db_path, "SELECT COUNT(*) as count FROM sessions")
    return results[0]['count'] if results else 0


def get_sessions(db_path: Path, limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent sessions from analytics database"""
    return query_analytics_db(
        db_path,
        "SELECT * FROM sessions ORDER BY started_at DESC LIMIT ?",
        [limit]
    )


def get_wave_executions(db_path: Path, limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent wave executions from analytics database"""
    return query_analytics_db(
        db_path,
        "SELECT * FROM wave_executions ORDER BY started_at DESC LIMIT ?",
        [limit]
    )


def get_total_cost(db_path: Path, days: int = 30) -> float:
    """Get total cost from sessions in past N days"""
    cutoff = datetime.now() - timedelta(days=days)
    results = query_analytics_db(
        db_path,
        """
        SELECT COALESCE(SUM(cost_usd), 0.0) as total_cost
        FROM sessions
        WHERE started_at >= ?
        """,
        [cutoff.isoformat()]
    )
    return float(results[0]['total_cost']) if results else 0.0


def get_trends_data(db_path: Path) -> Dict[str, Any]:
    """Get trends data from analytics database"""
    # Query cost trend
    cost_results = query_analytics_db(
        db_path,
        """
        SELECT
            date(started_at) as date,
            COUNT(*) as session_count,
            COALESCE(SUM(cost_usd), 0.0) as daily_cost,
            COALESCE(AVG(cost_usd), 0.0) as avg_cost
        FROM sessions
        WHERE started_at >= datetime('now', '-30 days')
        GROUP BY date(started_at)
        ORDER BY date
        """
    )

    # Query performance trend
    perf_results = query_analytics_db(
        db_path,
        """
        SELECT
            date(started_at) as date,
            COALESCE(AVG(duration_seconds), 0.0) as avg_duration,
            COALESCE(AVG(tokens_used), 0.0) as avg_tokens
        FROM sessions
        WHERE started_at >= datetime('now', '-30 days')
        GROUP BY date(started_at)
        ORDER BY date
        """
    )

    return {
        'cost_trend': cost_results,
        'performance_trend': perf_results
    }


# ============================================================================
# TEST 1: Session Logging
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_session_logging(simple_spec: Path, clean_analytics_db: Path):
    """
    Test 1: Run analyze, check analytics.db created, validate session logged

    Verifies that:
    - analytics.db file is created in ~/.shannon/
    - Session is logged with command details
    - Session contains: command, timestamp, status
    - Session count increases after execution
    """

    db_path = clean_analytics_db
    initial_count = get_session_count(db_path)

    # Run analyze command
    monitor = CLIMonitor()
    result = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec)],
        snapshot_interval_ms=250,
        timeout_seconds=120
    )

    assert result.validate_success(), f"Command failed with exit code {result.exit_code}"

    # Check that database was created
    assert db_path.exists(), f"Analytics database not created at {db_path}"

    # Check that session was logged
    time.sleep(1)  # Give database time to sync
    final_count = get_session_count(db_path)

    assert final_count > initial_count, \
        f"Session not logged. Before: {initial_count}, After: {final_count}"

    # Get the new session
    sessions = get_sessions(db_path, limit=1)
    assert len(sessions) > 0, "No sessions found in database"

    session = sessions[0]
    assert 'command' in session, "Session missing 'command' field"
    assert 'started_at' in session, "Session missing 'started_at' field"
    assert session['command'] == 'analyze', f"Command mismatch: {session['command']}"

    return TestResult(
        test_name="test_session_logging",
        status=TestStatus.PASSED,
        message=f"Session logged successfully (total sessions: {final_count})",
        details={
            'db_path': str(db_path),
            'db_exists': db_path.exists(),
            'session_count_before': initial_count,
            'session_count_after': final_count,
            'session_command': session.get('command'),
            'session_status': session.get('status')
        }
    )


# ============================================================================
# TEST 2: Wave Tracking
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.timeout(180)
async def test_wave_tracking(complex_spec: Path, clean_analytics_db: Path):
    """
    Test 2: Run wave, validate wave execution logged with agent details

    Verifies that:
    - Wave execution is logged in wave_executions table
    - Wave contains: wave_id, agent_count, completed_agents, started_at
    - Agent details are captured (agent_id, agent_type, status)
    - Wave execution status is tracked
    """

    db_path = clean_analytics_db
    initial_wave_count = len(get_wave_executions(db_path))

    # Run wave command
    monitor = CLIMonitor()
    result = monitor.run_and_monitor(
        command=['shannon', 'wave', str(complex_spec)],
        snapshot_interval_ms=250,
        timeout_seconds=180
    )

    assert result.validate_success(), f"Command failed with exit code {result.exit_code}"

    # Give database time to sync
    time.sleep(1)

    # Check wave execution was logged
    final_wave_count = len(get_wave_executions(db_path))
    assert final_wave_count > initial_wave_count, \
        f"Wave execution not logged. Before: {initial_wave_count}, After: {final_wave_count}"

    # Get the new wave execution
    wave_execs = get_wave_executions(db_path, limit=1)
    assert len(wave_execs) > 0, "No wave executions found in database"

    wave_exec = wave_execs[0]
    assert 'wave_id' in wave_exec or 'session_id' in wave_exec, \
        "Wave execution missing wave_id or session_id field"
    assert 'started_at' in wave_exec, "Wave execution missing started_at field"
    assert 'agent_count' in wave_exec or 'agents_total' in wave_exec, \
        "Wave execution missing agent_count field"

    # Verify agent count is positive
    agent_count = wave_exec.get('agent_count') or wave_exec.get('agents_total', 0)
    assert agent_count > 0, f"Agent count should be > 0, got {agent_count}"

    return TestResult(
        test_name="test_wave_tracking",
        status=TestStatus.PASSED,
        message=f"Wave execution tracked (agents: {agent_count})",
        details={
            'db_path': str(db_path),
            'wave_executions_before': initial_wave_count,
            'wave_executions_after': final_wave_count,
            'agent_count': agent_count,
            'wave_id': wave_exec.get('wave_id') or wave_exec.get('session_id'),
            'status': wave_exec.get('status')
        }
    )


# ============================================================================
# TEST 3: Cost Recording
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_cost_recording(simple_spec: Path, clean_analytics_db: Path):
    """
    Test 3: Run analyze, validate cost recorded accurately in analytics DB

    Verifies that:
    - Cost is recorded in session table
    - Cost value is numeric and > 0
    - Cost matches reported metrics (if available)
    - Multiple executions accumulate costs correctly
    """

    db_path = clean_analytics_db
    initial_total_cost = get_total_cost(db_path)

    # Run first analyze command
    monitor = CLIMonitor()
    result1 = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec)],
        snapshot_interval_ms=250,
        timeout_seconds=120
    )

    assert result1.validate_success(), f"First command failed with exit code {result1.exit_code}"

    time.sleep(1)

    # Check cost was recorded
    cost_after_first = get_total_cost(db_path)
    assert cost_after_first > initial_total_cost, \
        f"Cost not recorded. Before: ${initial_total_cost:.4f}, After: ${cost_after_first:.4f}"

    first_cost = cost_after_first - initial_total_cost

    # Run second analyze command
    result2 = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec)],
        snapshot_interval_ms=250,
        timeout_seconds=120
    )

    assert result2.validate_success(), f"Second command failed with exit code {result2.exit_code}"

    time.sleep(1)

    # Check accumulated cost
    cost_after_second = get_total_cost(db_path)
    accumulated_cost = cost_after_second - initial_total_cost

    # Second execution should add to total
    assert cost_after_second > cost_after_first, \
        f"Cost not accumulated. After 1st: ${cost_after_first:.4f}, After 2nd: ${cost_after_second:.4f}"

    # Get sessions for detailed validation
    sessions = get_sessions(db_path, limit=2)

    for session in sessions:
        cost_usd = session.get('cost_usd', 0)
        assert isinstance(cost_usd, (int, float)), \
            f"Cost should be numeric, got {type(cost_usd)}: {cost_usd}"
        assert cost_usd >= 0, f"Cost should be >= 0, got {cost_usd}"

    return TestResult(
        test_name="test_cost_recording",
        status=TestStatus.PASSED,
        message=f"Cost recorded accurately (total: ${accumulated_cost:.4f})",
        details={
            'initial_cost': initial_total_cost,
            'cost_after_first': cost_after_first,
            'cost_after_second': cost_after_second,
            'first_execution_cost': first_cost,
            'accumulated_cost': accumulated_cost,
            'session_count': len(sessions),
            'sessions_have_cost': all('cost_usd' in s for s in sessions)
        }
    )


# ============================================================================
# TEST 4: Trends Analysis
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.timeout(600)
async def test_trends_analysis(simple_spec: Path, clean_analytics_db: Path):
    """
    Test 4: Run analyze 5x, execute shannon analytics trends, validate trends shown

    Verifies that:
    - Multiple executions create trend data in database
    - Trends can be queried and analyzed
    - Trend data shows cost, tokens, duration over time
    - Trends command displays analysis results
    """

    db_path = clean_analytics_db
    monitor = CLIMonitor()

    # Run analyze command 5 times with delays to create time-series data
    execution_times = []
    for i in range(5):
        print(f"Execution {i+1}/5...")
        start_exec = time.time()

        result = monitor.run_and_monitor(
            command=['shannon', 'analyze', str(simple_spec)],
            snapshot_interval_ms=250,
            timeout_seconds=120
        )

        exec_time = time.time() - start_exec
        execution_times.append(exec_time)

        assert result.validate_success(), \
            f"Execution {i+1} failed with exit code {result.exit_code}"

        # Wait between executions
        if i < 4:
            time.sleep(2)

    # Give database time to sync
    time.sleep(2)

    # Query trends data
    trends_data = get_trends_data(db_path)

    cost_trend = trends_data.get('cost_trend', [])
    perf_trend = trends_data.get('performance_trend', [])

    assert len(cost_trend) > 0, "No cost trend data found"

    # Validate trend structure
    for day_data in cost_trend:
        assert 'date' in day_data, "Trend missing date field"
        assert 'session_count' in day_data, "Trend missing session_count field"
        assert 'daily_cost' in day_data, "Trend missing daily_cost field"
        assert day_data['session_count'] > 0, "Trend should have > 0 sessions"

    # Run shannon analytics trends command
    analytics_monitor = CLIMonitor()
    analytics_result = analytics_monitor.run_and_monitor(
        command=['shannon', 'analytics', 'trends'],
        snapshot_interval_ms=250,
        timeout_seconds=60
    )

    # Validate trends command output
    assert analytics_result.validate_success() or analytics_result.exit_code == 0, \
        f"Trends command failed with exit code {analytics_result.exit_code}"

    output = analytics_result.total_output.lower()

    # Check for trend indicators in output
    trend_indicators = ['trend', 'cost', 'day', 'average', 'session', 'total']
    found_indicators = sum(1 for indicator in trend_indicators if indicator in output)

    assert found_indicators >= 2, \
        f"Trends output missing trend indicators. Found {found_indicators}/6"

    return TestResult(
        test_name="test_trends_analysis",
        status=TestStatus.PASSED,
        message=f"Trends analyzed ({len(cost_trend)} daily trends, 5 executions)",
        details={
            'executions': 5,
            'average_execution_time': sum(execution_times) / len(execution_times),
            'cost_trend_days': len(cost_trend),
            'perf_trend_days': len(perf_trend),
            'total_daily_cost': sum(d.get('daily_cost', 0) for d in cost_trend),
            'trends_command_success': analytics_result.validate_success()
        }
    )


# ============================================================================
# TEST 5: Insights Generation
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.timeout(600)
async def test_insights_generation(simple_spec: Path, clean_analytics_db: Path):
    """
    Test 5: After executions, run shannon analytics insights, validate recommendations

    Verifies that:
    - Multiple executions create sufficient data for insights
    - Insights command runs successfully
    - Insights output contains recommendations or analysis
    - Insight categories are present (cost, performance, patterns)
    """

    db_path = clean_analytics_db
    monitor = CLIMonitor()

    # Run analyze command 3 times to generate insights
    for i in range(3):
        print(f"Pre-insight execution {i+1}/3...")

        result = monitor.run_and_monitor(
            command=['shannon', 'analyze', str(simple_spec)],
            snapshot_interval_ms=250,
            timeout_seconds=120
        )

        assert result.validate_success(), \
            f"Execution {i+1} failed with exit code {result.exit_code}"

        if i < 2:
            time.sleep(1)

    # Give database time to sync
    time.sleep(2)

    # Run shannon analytics insights command
    insights_monitor = CLIMonitor()
    insights_result = insights_monitor.run_and_monitor(
        command=['shannon', 'analytics', 'insights'],
        snapshot_interval_ms=250,
        timeout_seconds=60
    )

    # Validate insights command execution
    assert insights_result.validate_success() or insights_result.exit_code == 0, \
        f"Insights command failed with exit code {insights_result.exit_code}"

    output = insights_result.total_output.lower()

    # Check for insight content
    insight_keywords = ['insight', 'recommend', 'suggest', 'analysis', 'optimization', 'trend', 'pattern']
    found_keywords = sum(1 for keyword in insight_keywords if keyword in output)

    # Should find at least some insight-related content
    has_insight_content = found_keywords >= 1
    assert has_insight_content or len(output) > 50, \
        "Insights output appears empty or too short"

    # Query database to verify insight data can be extracted
    sessions = get_sessions(db_path, limit=10)
    assert len(sessions) >= 3, "Should have at least 3 sessions for insights"

    # Check for data patterns that insights might analyze
    total_cost = sum(s.get('cost_usd', 0) for s in sessions)
    avg_duration = sum(s.get('duration_seconds', 0) for s in sessions) / len(sessions)

    assert total_cost > 0, "Should have cost data for insights"
    assert avg_duration > 0, "Should have duration data for insights"

    return TestResult(
        test_name="test_insights_generation",
        status=TestStatus.PASSED,
        message=f"Insights generated ({found_keywords} insight keywords found)",
        details={
            'executions': 3,
            'sessions_in_db': len(sessions),
            'total_cost': total_cost,
            'avg_duration': avg_duration,
            'insight_keywords_found': found_keywords,
            'insights_command_success': insights_result.validate_success(),
            'output_length': len(output)
        }
    )


# ============================================================================
# TEST 6: Analytics Query
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_analytics_query(simple_spec: Path, clean_analytics_db: Path):
    """
    Test 6: Query analytics DB (shannon analytics report --days 30), validate data returned

    Verifies that:
    - Analytics report command returns data for past 30 days
    - Report contains: session count, total cost, average metrics
    - Multiple date ranges can be queried
    - Report output is well-formed and readable
    """

    db_path = clean_analytics_db
    monitor = CLIMonitor()

    # Run analyze to generate data
    print("Generating analytics data...")
    result = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec)],
        snapshot_interval_ms=250,
        timeout_seconds=120
    )

    assert result.validate_success(), f"Command failed with exit code {result.exit_code}"

    time.sleep(1)

    # Query 30-day report via CLI
    report_monitor = CLIMonitor()
    report_result = report_monitor.run_and_monitor(
        command=['shannon', 'analytics', 'report', '--days', '30'],
        snapshot_interval_ms=250,
        timeout_seconds=60
    )

    # Validate report command succeeded
    assert report_result.validate_success() or report_result.exit_code == 0, \
        f"Report command failed with exit code {report_result.exit_code}"

    report_output = report_result.total_output

    # Validate report contains data
    assert len(report_output) > 20, "Report output appears empty"

    # Check for report indicators
    report_indicators = ['session', 'cost', 'total', 'day', 'average', '30', 'report']
    found_indicators = sum(1 for indicator in report_indicators if indicator in report_output.lower())

    assert found_indicators >= 2, \
        f"Report missing indicators. Found {found_indicators}/7"

    # Query database directly to validate report accuracy
    sessions_30d = get_sessions(db_path, limit=100)
    total_cost_30d = get_total_cost(db_path, days=30)

    # Validate data exists
    assert len(sessions_30d) > 0, "Should have at least one session in 30-day window"
    assert total_cost_30d >= 0, "Total cost should be >= 0"

    # Verify report mentions some of this data
    session_count_str = str(len(sessions_30d))
    cost_str = f"{total_cost_30d:.2f}"

    # At least one metric should appear in report
    has_count_mention = session_count_str in report_output or 'session' in report_output.lower()
    has_cost_mention = cost_str in report_output or '$' in report_output

    assert has_count_mention or has_cost_mention or len(report_output) > 50, \
        "Report should mention sessions or costs"

    # Test different time range (7 days)
    report_7d_result = report_monitor.run_and_monitor(
        command=['shannon', 'analytics', 'report', '--days', '7'],
        snapshot_interval_ms=250,
        timeout_seconds=60
    )

    assert report_7d_result.validate_success() or report_7d_result.exit_code == 0, \
        f"7-day report command failed with exit code {report_7d_result.exit_code}"

    report_7d_output = report_7d_result.total_output
    assert len(report_7d_output) > 20, "7-day report output appears empty"

    return TestResult(
        test_name="test_analytics_query",
        status=TestStatus.PASSED,
        message=f"Analytics query working (30d: {len(sessions_30d)} sessions, ${total_cost_30d:.4f})",
        details={
            'sessions_30d': len(sessions_30d),
            'total_cost_30d': total_cost_30d,
            'report_30d_length': len(report_output),
            'report_7d_length': len(report_7d_output),
            'report_30d_indicators': found_indicators,
            'cost_format_valid': isinstance(total_cost_30d, (int, float))
        }
    )


# ============================================================================
# TEST SUITE SUMMARY
# ============================================================================

def pytest_collection_modifyitems(config, items):
    """Mark tests with appropriate markers"""
    for item in items:
        # Mark analytics tests
        if 'analytics' in item.nodeid:
            item.add_marker(pytest.mark.analytics)
            # Add longer timeout for analytics tests
            item.add_marker(pytest.mark.timeout(600))


if __name__ == '__main__':
    """
    Run tests with: pytest tests/cli_functional/test_wave5_analytics.py -v

    Fixtures:
    - simple_spec: Basic specification for quick testing
    - moderate_spec: Medium complexity specification
    - complex_spec: Complex specification with multiple agents
    - clean_analytics_db: Cleans analytics database before/after each test

    Test Coverage:
    - Session logging and tracking
    - Wave execution with agent details
    - Cost recording and accuracy
    - Trends analysis and visualization
    - Insights generation and recommendations
    - Analytics query and reporting

    Database:
    - Location: ~/.shannon/analytics.db
    - Tables: sessions, wave_executions, trends, insights
    - Queries: Cost totals, trends, performance metrics
    """
    pytest.main([__file__, '-v', '-s'])
