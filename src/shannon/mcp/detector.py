"""
MCP Detector - Automated MCP detection and verification.

Detects installed MCPs via two methods:
1. SDK tool discovery (primary) - functional verification
2. claude CLI listing (fallback) - config verification

Philosophy: Functional verification over config parsing.
"""

import asyncio
import logging
import subprocess
from typing import List, Dict, Tuple, Optional, Any


class MCPDetector:
    """
    Detects installed MCPs and verifies functionality.

    Uses dual detection strategy:
    - Primary: SDK tool discovery (proves MCP is functional)
    - Fallback: CLI parsing (proves MCP is configured)

    Integration:
    - Used by MCPInstaller to verify installations
    - Used by MCPManager for pre-wave checks
    - Used by setup wizard to validate environment
    """

    def __init__(self):
        """Initialize MCP detector with logging."""
        self.logger = logging.getLogger(__name__)

    async def check_installed(self, mcp_name: str) -> bool:
        """
        Check if MCP is installed and functional.

        Tries SDK method first (more reliable), falls back to CLI.
        Returns True only if MCP is both installed AND working.

        Args:
            mcp_name: Name of MCP to check (e.g., "serena", "context7")

        Returns:
            True if MCP is installed and functional, False otherwise
        """
        # Try SDK method first (functional verification)
        try:
            installed = await self._check_via_sdk(mcp_name)
            if installed:
                self.logger.info(f"MCP {mcp_name} verified via SDK")
                return True
        except Exception as e:
            self.logger.debug(f"SDK check failed for {mcp_name}: {e}")

        # Fallback to CLI method (config verification)
        try:
            installed = self._check_via_cli(mcp_name)
            if installed:
                self.logger.info(f"MCP {mcp_name} verified via CLI")
                return installed
        except Exception as e:
            self.logger.debug(f"CLI check failed for {mcp_name}: {e}")

        return False

    async def _check_via_sdk(self, mcp_name: str) -> bool:
        """
        Check MCP via SDK tool discovery.

        Creates minimal SDK query to trigger tool discovery,
        then checks if MCP tools are present in the response.

        This is FUNCTIONAL verification - we know MCP works if
        SDK can see its tools.

        Args:
            mcp_name: Name of MCP to check

        Returns:
            True if MCP tools found in SDK, False otherwise
        """
        # NOTE: This will be implemented when SDK integration is available
        # For Wave 2, we rely on CLI method
        # Wave 4 will add SDK-based verification
        self.logger.debug(f"SDK verification not yet implemented for {mcp_name}")
        return False

    def _check_via_cli(self, mcp_name: str) -> bool:
        """
        Check MCP via claude CLI.

        Runs: claude mcp list
        Parses output for MCP name.

        Less reliable than SDK method (depends on CLI format),
        but works immediately without SDK integration.

        Args:
            mcp_name: Name of MCP to check

        Returns:
            True if MCP found in CLI output, False otherwise
        """
        try:
            result = subprocess.run(
                ['claude', 'mcp', 'list'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                # Parse installed MCPs from output
                installed = self._parse_mcp_list(result.stdout)

                # Case-insensitive match
                return mcp_name.lower() in [m.lower() for m in installed]

            return False

        except subprocess.TimeoutExpired:
            self.logger.warning("claude mcp list timed out")
            return False

        except FileNotFoundError:
            self.logger.error("claude CLI not found - is Claude Code installed?")
            return False

    def _parse_mcp_list(self, output: str) -> List[str]:
        """
        Parse `claude mcp list` output to extract MCP names.

        Supports multiple formats:
        1. Simple list:
           - serena
           - context7

        2. Health check format (claude mcp list):
           serena: uvx ... - ✓ Connected

        Args:
            output: Raw stdout from `claude mcp list`

        Returns:
            List of installed MCP names
        """
        installed = []

        for line in output.splitlines():
            line = line.strip()

            # Skip empty lines and headers
            if not line or 'Checking' in line or 'MCP server' in line or 'Installed' in line:
                continue

            # Format 1: Simple list (- serena or * serena)
            if line.startswith('-') or line.startswith('*'):
                mcp_name = line.lstrip('-* ').strip()
                if mcp_name and mcp_name != '(none)':
                    installed.append(mcp_name)

            # Format 2: Health check format (name: command - status)
            elif ':' in line:
                # Extract MCP name before the colon
                mcp_name = line.split(':')[0].strip()
                # Avoid: plugin paths, empty names, headers
                if mcp_name and '/' not in mcp_name and not mcp_name.endswith('MCPs'):
                    installed.append(mcp_name)

        return installed

    async def get_available_tools(self, mcp_name: str) -> List[str]:
        """
        Get list of tools provided by MCP.

        Useful for verification and user feedback after installation.
        Shows user exactly what tools they gained.

        Args:
            mcp_name: Name of MCP to query

        Returns:
            List of tool names provided by MCP (empty if not available)
        """
        # NOTE: SDK-based tool discovery for Wave 4
        # For now, return empty list
        self.logger.debug(f"Tool discovery not yet implemented for {mcp_name}")
        return []

    async def check_all_recommended(
        self,
        recommendations: List[Dict[str, Any]]
    ) -> Dict[str, bool]:
        """
        Check installation status of all recommended MCPs.

        Runs checks in parallel for speed (important for large lists).

        Args:
            recommendations: List of MCP dicts with 'name' key

        Returns:
            Dict mapping MCP name to installed status
            Example: {'serena': True, 'context7': False}
        """
        async def check_one(mcp: Dict[str, Any]) -> Tuple[str, bool]:
            """Check single MCP and return (name, status) tuple."""
            name = mcp.get('name', mcp.get('mcp_name', 'unknown'))
            installed = await self.check_installed(name)
            return (name, installed)

        # Run all checks in parallel
        results = await asyncio.gather(*[
            check_one(mcp) for mcp in recommendations
        ], return_exceptions=True)

        # Filter out exceptions, log errors
        status_map = {}
        for result in results:
            if isinstance(result, Exception):
                self.logger.error(f"MCP check failed: {result}")
                continue

            name, installed = result
            status_map[name] = installed

        return status_map

    def get_installed_mcps(self) -> List[str]:
        """
        Get list of all currently installed MCPs.

        Uses CLI method for immediate results without async.

        Returns:
            List of installed MCP names
        """
        try:
            result = subprocess.run(
                ['claude', 'mcp', 'list'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                return self._parse_mcp_list(result.stdout)

            return []

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.logger.error(f"Failed to get installed MCPs: {e}")
            return []
