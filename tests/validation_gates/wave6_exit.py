"""
Wave 6 Exit Gate: Context-Aware Execution Validation

Runs all 6 Wave 6 functional tests to validate:
- Serena MCP connection and tool discovery
- Memory read/write operations
- Context persistence across executions
- Context-aware command optimization
- Project state tracking
- Context invalidation strategies

Requires 100% pass rate to proceed to Wave 7.

Part of Shannon V3 Wave 6: Context-Aware Execution (Serena Integration)
"""

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from validation_gates.gate_framework import ValidationGate
from cli_functional.test_wave6_context import TestWave6Context


async def wave6_exit_gate() -> bool:
    """
    Run Wave 6 exit gate - all 6 functional tests

    Returns:
        bool: True if all tests pass
    """
    gate = ValidationGate(phase=6, gate_type='exit')

    # Instantiate test class
    context_tests = TestWave6Context()

    # Add all 6 Wave 6 tests
    gate.add_test(context_tests.test_serena_mcp_connection)
    gate.add_test(context_tests.test_memory_operations)
    gate.add_test(context_tests.test_context_persistence)
    gate.add_test(context_tests.test_context_aware_optimization)
    gate.add_test(context_tests.test_project_state_tracking)
    gate.add_test(context_tests.test_context_invalidation)

    result = await gate.run_all_tests()
    result.display()

    return result.passed


if __name__ == '__main__':
    import asyncio
    success = asyncio.run(wave6_exit_gate())
    sys.exit(0 if success else 1)
