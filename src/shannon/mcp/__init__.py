"""
MCP (Model Context Protocol) Management System.

Provides automated MCP detection, installation, and verification:

- MCPDetector: Check if MCPs are installed via CLI and SDK
- MCPInstaller: Install MCPs with progress feedback
- MCPVerifier: Verify MCPs are functional after installation
- MCPManager: Unified interface for all MCP operations

Usage:
    from shannon.mcp import MCPManager

    manager = MCPManager()

    # Post-analysis auto-install
    await manager.post_analysis_check(analysis_result)

    # Pre-wave verification
    await manager.pre_wave_check(wave_plan)

    # Health check
    await manager.health_check()

Architecture:
    MCPManager uses:
    - MCPDetector for installation checks
    - MCPInstaller for adding new MCPs
    - MCPVerifier for post-install verification

Integration points:
    - shannon analyze: post_analysis_check()
    - shannon wave: pre_wave_check()
    - shannon setup: setup_base_mcps()
    - /shannon:check_mcps: health_check()
"""

from .detector import MCPDetector
from .installer import MCPInstaller
from .verifier import MCPVerifier, MCPHealthReport
from .manager import MCPManager

__all__ = [
    'MCPDetector',
    'MCPInstaller',
    'MCPVerifier',
    'MCPHealthReport',
    'MCPManager',
]

__version__ = '3.0.0'
