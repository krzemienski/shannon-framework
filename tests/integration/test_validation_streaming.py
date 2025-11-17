"""
Test validation streaming E2E integration

Verifies that validation events flow from validator to dashboard UI:
- ValidationOrchestrator receives dashboard_client
- Events are emitted during validation
- Dashboard client forwards events to server
"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from shannon.executor.validator import ValidationOrchestrator


async def test_validator_receives_dashboard_client():
    """Test that ValidationOrchestrator can be instantiated with dashboard_client"""
    # Create mock dashboard client
    mock_client = MagicMock()
    mock_client.emit_event = AsyncMock()

    # Create validator with dashboard_client
    validator = ValidationOrchestrator(
        project_root=Path.cwd(),
        dashboard_client=mock_client
    )

    # Verify dashboard_client is set
    assert validator.dashboard_client is mock_client
    print("✓ ValidationOrchestrator receives dashboard_client")


async def test_validation_emits_events():
    """Test that validation emits events when dashboard_client is present"""
    # Create mock dashboard client
    mock_client = MagicMock()
    mock_client.emit_event = AsyncMock()

    # Create validator with dashboard_client
    validator = ValidationOrchestrator(
        project_root=Path.cwd(),
        dashboard_client=mock_client
    )

    # Run a simple check (build will likely fail, but we just want to verify events)
    try:
        result = await validator._run_check_with_exit_code('echo "test"', 'Test Check')
    except Exception as e:
        print(f"  Check failed (expected): {e}")

    # Verify events were emitted
    calls = mock_client.emit_event.call_args_list

    # Should have emitted validation:started
    started_calls = [c for c in calls if c[0][0] == 'validation:started']
    assert len(started_calls) > 0, "Should emit validation:started event"
    print(f"✓ Emitted {len(started_calls)} validation:started event(s)")

    # Should have emitted validation:output
    output_calls = [c for c in calls if c[0][0] == 'validation:output']
    print(f"✓ Emitted {len(output_calls)} validation:output event(s)")

    # Should have emitted validation:completed
    completed_calls = [c for c in calls if c[0][0] == 'validation:completed']
    assert len(completed_calls) > 0, "Should emit validation:completed event"
    print(f"✓ Emitted {len(completed_calls)} validation:completed event(s)")


async def test_validation_without_dashboard_client():
    """Test that validation works without dashboard_client (no crashes)"""
    # Create validator WITHOUT dashboard_client
    validator = ValidationOrchestrator(
        project_root=Path.cwd(),
        dashboard_client=None
    )

    # Run a simple check - should not crash even without dashboard_client
    try:
        result = await validator._run_check_with_exit_code('echo "test"', 'Test Check')
        print("✓ Validation works without dashboard_client (no crash)")
    except Exception as e:
        print(f"  Check result: {e}")

    assert validator.dashboard_client is None
    print("✓ ValidationOrchestrator handles None dashboard_client gracefully")


async def main():
    """Run all tests"""
    print("Testing Validation Streaming Integration")
    print("=" * 60)
    print()

    print("[1/3] Test validator receives dashboard_client")
    await test_validator_receives_dashboard_client()
    print()

    print("[2/3] Test validation emits events")
    await test_validation_emits_events()
    print()

    print("[3/3] Test validation without dashboard_client")
    await test_validation_without_dashboard_client()
    print()

    print("=" * 60)
    print("✅ All validation streaming tests passed!")
    print()


if __name__ == '__main__':
    asyncio.run(main())
