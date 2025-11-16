"""
Wave 2 Exit Gate: Claude MCP Integration Validation

Runs all 7 Wave 2 functional tests to validate:
- MCP connection establishment
- MCP tool discovery and registration
- MCP bidirectional communication
- MCP error handling and recovery
- MCP session management
- MCP protocol compliance
- Claude Code integration with MCP servers

Requires 100% pass rate to proceed to Wave 3.

Part of Shannon V3 Wave 2: Claude MCP Integration
"""

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from validation_gates.gate_framework import ValidationGate
from cli_functional.test_wave2_mcp import TestWave2MCP


async def wave2_exit_gate() -> bool:
    """
    Run Wave 2 exit gate - all 7 functional tests

    Returns:
        bool: True if all tests pass
    """
    gate = ValidationGate(phase=2, gate_type='exit')

    # Instantiate test class
    mcp_tests = TestWave2MCP()

    # Add all 7 Wave 2 tests
    gate.add_test(mcp_tests.test_mcp_connection_establishment)
    gate.add_test(mcp_tests.test_mcp_tool_discovery)
    gate.add_test(mcp_tests.test_mcp_bidirectional_communication)
    gate.add_test(mcp_tests.test_mcp_error_handling)
    gate.add_test(mcp_tests.test_mcp_session_management)
    gate.add_test(mcp_tests.test_mcp_protocol_compliance)
    gate.add_test(mcp_tests.test_claude_code_mcp_integration)

    result = await gate.run_all_tests()
    result.display()

    return result.passed


if __name__ == '__main__':
    import asyncio
    success = asyncio.run(wave2_exit_gate())
    sys.exit(0 if success else 1)
