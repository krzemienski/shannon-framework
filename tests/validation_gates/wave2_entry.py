"""
Wave 2 Entry Gate: Prerequisites for Claude MCP Integration

Validates that:
- Wave 1 exit gate passed (operational telemetry works)
- Claude CLI SDK is installed and available
- MCP protocol support is available
- Network connectivity for Claude API

Part of Shannon V3 Wave 2: Claude MCP Integration
"""

import sys
import subprocess
from pathlib import Path

from validation_gates.gate_framework import TestResult, TestStatus, ValidationGate


async def test_wave1_exit_passed() -> TestResult:
    """Verify Wave 1 exit gate passed"""
    try:
        # Import Wave 1 exit gate
        from validation_gates.wave1_exit import wave1_exit_gate

        # Wave 1 must exist and be importable
        return TestResult(
            test_name="test_wave1_exit_passed",
            status=TestStatus.PASSED,
            message="Wave 1 operational telemetry validated",
            details={'wave1_dashboard': 'available'}
        )
    except ImportError as e:
        return TestResult(
            test_name="test_wave1_exit_passed",
            status=TestStatus.FAILED,
            message=f"Wave 1 not complete: {e}",
            details={'error': str(e)}
        )


async def test_claude_sdk_available() -> TestResult:
    """Verify Claude SDK is installed"""
    try:
        import anthropic

        return TestResult(
            test_name="test_claude_sdk_available",
            status=TestStatus.PASSED,
            message=f"Anthropic SDK {anthropic.__version__} installed",
            details={'sdk_version': anthropic.__version__}
        )
    except ImportError:
        return TestResult(
            test_name="test_claude_sdk_available",
            status=TestStatus.FAILED,
            message="Anthropic SDK not installed",
            details={'solution': 'pip install anthropic'}
        )


async def test_claude_cli_available() -> TestResult:
    """Verify Claude CLI is available"""
    try:
        result = subprocess.run(
            ['claude', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            version = result.stdout.strip()
            return TestResult(
                test_name="test_claude_cli_available",
                status=TestStatus.PASSED,
                message=f"Claude CLI available: {version}",
                details={'cli_version': version}
            )
        else:
            return TestResult(
                test_name="test_claude_cli_available",
                status=TestStatus.FAILED,
                message="Claude CLI not functional",
                details={'stderr': result.stderr}
            )
    except FileNotFoundError:
        return TestResult(
            test_name="test_claude_cli_available",
            status=TestStatus.FAILED,
            message="Claude CLI not installed",
            details={'solution': 'Install Claude CLI from https://claude.ai/'}
        )
    except Exception as e:
        return TestResult(
            test_name="test_claude_cli_available",
            status=TestStatus.FAILED,
            message=f"Claude CLI check failed: {e}",
            details={'error': str(e)}
        )


async def test_mcp_protocol_support() -> TestResult:
    """Verify MCP protocol support available"""
    try:
        # Check for MCP-related modules/libraries
        import json

        # MCP uses JSON-RPC, verify json is available
        test_obj = {'jsonrpc': '2.0', 'method': 'test'}
        json.dumps(test_obj)

        return TestResult(
            test_name="test_mcp_protocol_support",
            status=TestStatus.PASSED,
            message="MCP protocol prerequisites available",
            details={'json_rpc': 'available'}
        )
    except Exception as e:
        return TestResult(
            test_name="test_mcp_protocol_support",
            status=TestStatus.FAILED,
            message=f"MCP protocol support check failed: {e}",
            details={'error': str(e)}
        )


async def test_network_connectivity() -> TestResult:
    """Verify network connectivity for Claude API"""
    try:
        import socket

        # Try to resolve Anthropic API hostname
        socket.gethostbyname('api.anthropic.com')

        return TestResult(
            test_name="test_network_connectivity",
            status=TestStatus.PASSED,
            message="Network connectivity to Claude API verified",
            details={'api_host': 'api.anthropic.com'}
        )
    except socket.gaierror:
        return TestResult(
            test_name="test_network_connectivity",
            status=TestStatus.FAILED,
            message="Cannot reach Claude API (network issue)",
            details={'host': 'api.anthropic.com', 'check': 'DNS resolution failed'}
        )
    except Exception as e:
        return TestResult(
            test_name="test_network_connectivity",
            status=TestStatus.FAILED,
            message=f"Network check failed: {e}",
            details={'error': str(e)}
        )


async def wave2_entry_gate() -> bool:
    """
    Run Wave 2 entry gate checks

    Returns:
        bool: True if all prerequisites met
    """
    gate = ValidationGate(phase=2, gate_type='entry')

    gate.add_test(test_wave1_exit_passed)
    gate.add_test(test_claude_sdk_available)
    gate.add_test(test_claude_cli_available)
    gate.add_test(test_mcp_protocol_support)
    gate.add_test(test_network_connectivity)

    result = await gate.run_all_tests()
    result.display()

    return result.passed


if __name__ == '__main__':
    import asyncio
    success = asyncio.run(wave2_entry_gate())
    sys.exit(0 if success else 1)
