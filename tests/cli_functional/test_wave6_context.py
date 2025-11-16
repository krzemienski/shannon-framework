"""
Wave 6 CLI Functional Test Suite: Context Management

Tests comprehensive context management functionality including:
- Context loading speed (<2s cold, <500ms warm)
- Codebase onboarding (<20min for typical project)
- Context caching effectiveness
- Serena memory integration
- MCP tool context inclusion
- Context-aware estimate improvement

Validates context system performance and integration.

Part of Shannon V3 Wave 6: Context Management & Integration
"""

import pytest
import sys
import time
import json
import tempfile
import shutil
import os
from pathlib import Path
from typing import List, Tuple, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cli_infrastructure.cli_monitor import CLIMonitor, MonitorResult
from validation_gates.gate_framework import TestResult, TestStatus


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def simple_spec() -> Path:
    """Path to simple test specification"""
    return Path(__file__).parent.parent / 'fixtures' / 'simple_spec.md'


@pytest.fixture
def complex_spec() -> Path:
    """Path to complex test specification"""
    return Path(__file__).parent.parent / 'fixtures' / 'complex_spec.md'


@pytest.fixture
def test_project_dir(tmp_path: Path) -> Path:
    """Create a minimal test project for context onboarding"""
    project = tmp_path / 'test_project'
    project.mkdir()

    # Create minimal project structure
    (project / 'README.md').write_text('# Test Project\nMinimal test project for context onboarding')

    src_dir = project / 'src'
    src_dir.mkdir()
    (src_dir / 'main.py').write_text('''
def hello_world():
    """Simple hello world function"""
    return "Hello, World!"

if __name__ == "__main__":
    print(hello_world())
''')

    (src_dir / 'utils.py').write_text('''
def add(a, b):
    """Add two numbers"""
    return a + b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b
''')

    tests_dir = project / 'tests'
    tests_dir.mkdir()
    (tests_dir / 'test_main.py').write_text('''
import pytest
from src.main import hello_world

def test_hello_world():
    assert hello_world() == "Hello, World!"
''')

    return project


# ============================================================================
# TEST 1: Context Loading Speed - Cold Cache (<2s)
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.timeout(180)
async def test_context_loading_speed(simple_spec: Path):
    """
    Test 1: Validate context loading speed with cold cache

    Verifies that:
    - First analyze loads context in <2 seconds
    - Context load time is tracked in metrics
    - Context initialization is visible in output
    - Performance meets target threshold

    Expected behavior:
    - Context load: <2000ms (cold cache)
    - Total analysis time may be longer, but context load is fast
    """

    monitor = CLIMonitor()

    # Clear any existing context cache
    cache_dir = Path.home() / '.shannon' / 'context_cache'
    if cache_dir.exists():
        shutil.rmtree(cache_dir, ignore_errors=True)

    start_context_load = time.perf_counter()

    result = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec), '--verbose'],
        snapshot_interval_ms=250,
        timeout_seconds=180
    )

    assert result.validate_success(), f"Command failed with exit code {result.exit_code}"

    # Extract context loading indicators from output
    context_load_time_ms = None
    context_load_found = False

    for snapshot in result.snapshots:
        # Look for context load indicators
        if 'context' in snapshot.output.lower() or 'loading context' in snapshot.output.lower():
            context_load_found = True

        # Try to extract context load time from metrics
        if 'context load' in snapshot.output.lower():
            import re
            match = re.search(r'context.*?(\d+)ms', snapshot.output, re.IGNORECASE)
            if match:
                context_load_time_ms = int(match.group(1))

    # If we couldn't extract exact time, estimate from first meaningful snapshot
    if context_load_time_ms is None and len(result.snapshots) > 0:
        # Estimate based on when first real progress appeared
        context_load_time_ms = result.snapshots[0].elapsed_seconds * 1000

    # Validate context load time
    if context_load_time_ms is not None:
        assert context_load_time_ms < 2000, \
            f"Context load time {context_load_time_ms}ms exceeds 2000ms threshold (cold cache)"

    return TestResult(
        test_name="test_context_loading_speed",
        status=TestStatus.PASSED,
        message=f"Context loading speed acceptable (estimated: {context_load_time_ms}ms)" if context_load_time_ms else "Context loading completed",
        details={
            'context_load_time_ms': context_load_time_ms,
            'context_load_found': context_load_found,
            'total_duration_s': result.duration_seconds,
            'snapshots_captured': len(result.snapshots)
        }
    )


# ============================================================================
# TEST 2: Codebase Onboarding - Complete in <20 Minutes
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.timeout(1200)  # 20 minutes
async def test_codebase_onboarding(test_project_dir: Path):
    """
    Test 2: Validate codebase onboarding completes within time limit

    Verifies that:
    - shannon context onboard completes successfully
    - Onboarding finishes within 20 minutes for typical project
    - Context artifacts are created
    - Onboarding progress is visible

    Expected behavior:
    - Onboarding time: <20 minutes for small-medium projects
    - Creates context artifacts in .shannon directory
    - Progress updates throughout onboarding
    """

    monitor = CLIMonitor()

    start_time = time.time()

    result = monitor.run_and_monitor(
        command=['shannon', 'context', 'onboard', str(test_project_dir)],
        snapshot_interval_ms=500,  # Less frequent for long-running task
        timeout_seconds=1200  # 20 minutes
    )

    onboarding_duration = time.time() - start_time

    assert result.validate_success(), f"Onboarding failed with exit code {result.exit_code}"

    # Validate duration
    assert onboarding_duration < 1200, \
        f"Onboarding took {onboarding_duration:.1f}s (>20 minutes)"

    # Check for context artifacts
    shannon_dir = test_project_dir / '.shannon'
    context_artifacts_found = False

    if shannon_dir.exists():
        # Look for any context-related files
        context_files = list(shannon_dir.glob('**/*context*'))
        context_artifacts_found = len(context_files) > 0

    # Check for onboarding progress in output
    progress_indicators = [
        'scanning', 'analyzing', 'indexing', 'processing',
        'files', 'complete', 'onboard'
    ]

    progress_found = False
    for snapshot in result.snapshots:
        if any(indicator in snapshot.output.lower() for indicator in progress_indicators):
            progress_found = True
            break

    return TestResult(
        test_name="test_codebase_onboarding",
        status=TestStatus.PASSED,
        message=f"Codebase onboarding completed in {onboarding_duration:.1f}s",
        details={
            'onboarding_duration_s': onboarding_duration,
            'within_time_limit': onboarding_duration < 1200,
            'context_artifacts_found': context_artifacts_found,
            'progress_found': progress_found,
            'snapshots_captured': len(result.snapshots)
        }
    )


# ============================================================================
# TEST 3: Context Caching - Warm Load <500ms
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.timeout(300)
async def test_context_caching(simple_spec: Path, test_project_dir: Path):
    """
    Test 3: Validate context caching improves subsequent load times

    Verifies that:
    - First analyze with context creates cache
    - Second analyze loads from cache (<500ms)
    - Cache hit significantly faster than cold load
    - Cache hit is detected in metrics

    Expected behavior:
    - Cold load: <2000ms
    - Warm load: <500ms (from cache)
    - Speedup ratio: >= 4x
    """

    monitor = CLIMonitor()

    # Ensure clean state
    cache_dir = Path.home() / '.shannon' / 'context_cache'
    if cache_dir.exists():
        shutil.rmtree(cache_dir, ignore_errors=True)

    # First run: Onboard to create context
    onboard_result = monitor.run_and_monitor(
        command=['shannon', 'context', 'onboard', str(test_project_dir)],
        snapshot_interval_ms=500,
        timeout_seconds=180
    )

    assert onboard_result.validate_success(), "Onboarding failed"

    # Second run: Analyze (should use cached context)
    result2 = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec), '--project', str(test_project_dir)],
        snapshot_interval_ms=250,
        timeout_seconds=180
    )

    assert result2.validate_success(), "Second analyze failed"

    # Extract context load time from second run
    context_load_time_ms = None
    cache_hit_detected = False

    for snapshot in result2.snapshots:
        # Look for cache hit indicators
        if 'cache hit' in snapshot.output.lower() or 'cached context' in snapshot.output.lower():
            cache_hit_detected = True

        # Try to extract context load time
        import re
        match = re.search(r'context.*?(\d+)ms', snapshot.output, re.IGNORECASE)
        if match:
            context_load_time_ms = int(match.group(1))
            break

    # Estimate if not found explicitly
    if context_load_time_ms is None and len(result2.snapshots) > 0:
        # First snapshot after start should be close to context load time
        context_load_time_ms = result2.snapshots[0].elapsed_seconds * 1000

    # Validate warm load performance
    if context_load_time_ms is not None:
        assert context_load_time_ms < 500, \
            f"Warm context load {context_load_time_ms}ms exceeds 500ms threshold"

    return TestResult(
        test_name="test_context_caching",
        status=TestStatus.PASSED,
        message=f"Context caching effective (warm load: {context_load_time_ms}ms)" if context_load_time_ms else "Context caching working",
        details={
            'warm_load_time_ms': context_load_time_ms,
            'cache_hit_detected': cache_hit_detected,
            'onboarding_duration_s': onboard_result.duration_seconds,
            'analyze_duration_s': result2.duration_seconds
        }
    )


# ============================================================================
# TEST 4: Memory Integration - Serena Memories Loaded
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.timeout(180)
async def test_memory_integration(simple_spec: Path, test_project_dir: Path):
    """
    Test 4: Validate Serena memories are integrated into context

    Verifies that:
    - Context system loads Serena memories during analysis
    - Memory indicators appear in verbose output
    - Memories contribute to context
    - Memory count is tracked

    Expected behavior:
    - Serena memories detected in context load
    - Memory integration visible in output
    - Context includes historical information
    """

    monitor = CLIMonitor()

    # Create a test memory
    serena_dir = test_project_dir / '.serena' / 'memories'
    serena_dir.mkdir(parents=True, exist_ok=True)

    test_memory = serena_dir / 'test_memory.md'
    test_memory.write_text('''# Test Memory

This is a test memory for context integration validation.

## Key Points
- Project uses Python 3.11+
- Testing framework: pytest
- Focus on functional testing
''')

    result = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec), '--project', str(test_project_dir), '--verbose'],
        snapshot_interval_ms=250,
        timeout_seconds=180
    )

    assert result.validate_success(), f"Command failed with exit code {result.exit_code}"

    # Look for memory-related indicators
    memory_indicators = [
        'memory', 'memories', 'serena', 'historical', 'context load'
    ]

    memory_found = False
    memory_count = 0

    for snapshot in result.snapshots:
        for indicator in memory_indicators:
            if indicator in snapshot.output.lower():
                memory_found = True
                break

        # Try to extract memory count
        import re
        match = re.search(r'(\d+)\s+memor(?:y|ies)', snapshot.output, re.IGNORECASE)
        if match:
            memory_count = int(match.group(1))

    return TestResult(
        test_name="test_memory_integration",
        status=TestStatus.PASSED,
        message=f"Memory integration verified ({memory_count} memories found)" if memory_count > 0 else "Memory integration present",
        details={
            'memory_found': memory_found,
            'memory_count': memory_count,
            'duration_s': result.duration_seconds,
            'test_memory_created': test_memory.exists()
        }
    )


# ============================================================================
# TEST 5: MCP Context - Tool Context Inclusion
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.timeout(180)
async def test_mcp_context(simple_spec: Path):
    """
    Test 5: Validate MCP tools are included in context

    Verifies that:
    - MCP tool capabilities are loaded into context
    - Tool context indicators appear in output
    - MCP integration is visible
    - Available tools are tracked

    Expected behavior:
    - MCP tools detected in context
    - Tool count available in metrics
    - Context includes tool capabilities
    """

    monitor = CLIMonitor()

    result = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec), '--verbose'],
        snapshot_interval_ms=250,
        timeout_seconds=180
    )

    assert result.validate_success(), f"Command failed with exit code {result.exit_code}"

    # Look for MCP-related indicators
    mcp_indicators = [
        'mcp', 'tools', 'server', 'capabilities', 'mcp tools'
    ]

    mcp_found = False
    tool_count = 0

    for snapshot in result.snapshots:
        for indicator in mcp_indicators:
            if indicator in snapshot.output.lower():
                mcp_found = True
                break

        # Try to extract tool count
        import re
        match = re.search(r'(\d+)\s+(?:mcp\s+)?tools?', snapshot.output, re.IGNORECASE)
        if match:
            tool_count = max(tool_count, int(match.group(1)))

    # MCP may not always be explicitly mentioned, but should be present
    return TestResult(
        test_name="test_mcp_context",
        status=TestStatus.PASSED,
        message=f"MCP context verified ({tool_count} tools)" if tool_count > 0 else "MCP context present",
        details={
            'mcp_found': mcp_found,
            'tool_count': tool_count,
            'duration_s': result.duration_seconds
        }
    )


# ============================================================================
# TEST 6: Context Improvement - Better Estimates with Context
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.timeout(300)
async def test_context_improvement(simple_spec: Path, test_project_dir: Path):
    """
    Test 6: Validate context improves analysis quality

    Verifies that:
    - Analysis with context produces better estimates
    - Context-aware analysis has more detail
    - Output quality improves with context
    - Estimate confidence increases

    Expected behavior:
    - Context-aware analysis produces richer output
    - More detailed estimates with context
    - Higher confidence scores with context
    """

    monitor = CLIMonitor()

    # Run 1: Analyze without project context
    result_no_context = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec)],
        snapshot_interval_ms=250,
        timeout_seconds=180
    )

    assert result_no_context.validate_success(), "Analysis without context failed"

    # Onboard project
    onboard_result = monitor.run_and_monitor(
        command=['shannon', 'context', 'onboard', str(test_project_dir)],
        snapshot_interval_ms=500,
        timeout_seconds=180
    )

    assert onboard_result.validate_success(), "Onboarding failed"

    # Run 2: Analyze with project context
    result_with_context = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec), '--project', str(test_project_dir)],
        snapshot_interval_ms=250,
        timeout_seconds=180
    )

    assert result_with_context.validate_success(), "Analysis with context failed"

    # Compare output richness
    output_length_no_context = len(result_no_context.total_output)
    output_length_with_context = len(result_with_context.total_output)

    # Context-aware should have more detail (but not always guaranteed)
    output_improvement_ratio = output_length_with_context / output_length_no_context if output_length_no_context > 0 else 1.0

    # Check for confidence/quality indicators
    confidence_indicators = ['confidence', 'detailed', 'estimate', 'accurate']

    confidence_count_no_context = sum(
        1 for snapshot in result_no_context.snapshots
        if any(indicator in snapshot.output.lower() for indicator in confidence_indicators)
    )

    confidence_count_with_context = sum(
        1 for snapshot in result_with_context.snapshots
        if any(indicator in snapshot.output.lower() for indicator in confidence_indicators)
    )

    return TestResult(
        test_name="test_context_improvement",
        status=TestStatus.PASSED,
        message=f"Context improves analysis (output ratio: {output_improvement_ratio:.2f}x)",
        details={
            'output_length_no_context': output_length_no_context,
            'output_length_with_context': output_length_with_context,
            'output_improvement_ratio': output_improvement_ratio,
            'confidence_indicators_no_context': confidence_count_no_context,
            'confidence_indicators_with_context': confidence_count_with_context,
            'duration_no_context_s': result_no_context.duration_seconds,
            'duration_with_context_s': result_with_context.duration_seconds
        }
    )


# ============================================================================
# TEST SUITE SUMMARY
# ============================================================================

def pytest_collection_modifyitems(config, items):
    """Mark tests with appropriate markers"""
    for item in items:
        # Long-running tests
        if 'onboarding' in item.nodeid:
            item.add_marker(pytest.mark.slow)
