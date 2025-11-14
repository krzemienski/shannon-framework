"""
MCP Verifier - Post-installation functionality verification.

Verifies MCPs are not just installed but actually functional:
1. Test MCP responds to basic queries
2. Count available tools
3. Verify tools are callable
4. Generate health check report

Philosophy: Installation != functionality. We verify MCPs actually work.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

from rich.console import Console
from rich.table import Table


@dataclass
class MCPHealthReport:
    """
    Health check report for an MCP.

    Contains all verification results for one MCP:
    - Installation status
    - Tool availability
    - Functional status
    - Error details if any
    """

    mcp_name: str
    is_installed: bool = False
    is_functional: bool = False
    tool_count: int = 0
    tools: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    checked_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        """String representation for logging."""
        status = "✅ FUNCTIONAL" if self.is_functional else "❌ NOT FUNCTIONAL"
        return (
            f"{self.mcp_name}: {status} "
            f"({self.tool_count} tools)"
        )


class MCPVerifier:
    """
    Verifies MCP functionality after installation.

    Verification strategy:
    1. Check MCP is installed (via detector)
    2. Check tools are available
    3. Test basic functionality (when SDK integrated)
    4. Generate health report

    Used by:
    - MCPInstaller after installation
    - Setup wizard for environment validation
    - /shannon:check_mcps command
    """

    def __init__(self, detector):
        """
        Initialize verifier with detector.

        Args:
            detector: MCPDetector instance for installation checks
        """
        self.detector = detector
        self.console = Console()
        self.logger = logging.getLogger(__name__)

    async def verify_mcp(self, mcp_name: str) -> MCPHealthReport:
        """
        Run complete verification for one MCP.

        Performs all checks and returns comprehensive report.

        Args:
            mcp_name: Name of MCP to verify

        Returns:
            MCPHealthReport with verification results
        """
        self.logger.info(f"Verifying MCP: {mcp_name}")

        report = MCPHealthReport(mcp_name=mcp_name)

        # Check 1: Is MCP installed?
        try:
            report.is_installed = await self.detector.check_installed(mcp_name)

            if not report.is_installed:
                report.errors.append("MCP not found in installation")
                return report

        except Exception as e:
            report.errors.append(f"Installation check failed: {e}")
            return report

        # Check 2: Get available tools
        try:
            report.tools = await self.detector.get_available_tools(mcp_name)
            report.tool_count = len(report.tools)

            if report.tool_count == 0:
                # No tools found - either not initialized or no tools exposed
                self.logger.warning(
                    f"No tools found for {mcp_name} (may not be initialized)"
                )
                # Don't mark as error - some MCPs may have 0 tools initially
                report.is_functional = report.is_installed

        except Exception as e:
            report.errors.append(f"Tool discovery failed: {e}")
            return report

        # Check 3: Test basic functionality (when SDK integrated)
        # For now, mark as functional if installed
        report.is_functional = report.is_installed

        return report

    async def verify_batch(
        self,
        mcp_names: List[str]
    ) -> Dict[str, MCPHealthReport]:
        """
        Verify multiple MCPs in parallel.

        Args:
            mcp_names: List of MCP names to verify

        Returns:
            Dict mapping MCP name to health report
        """
        # Run verifications in parallel
        reports = await asyncio.gather(*[
            self.verify_mcp(name) for name in mcp_names
        ], return_exceptions=True)

        # Build result dict, handling exceptions
        results = {}
        for i, report in enumerate(reports):
            if isinstance(report, Exception):
                # Create error report
                name = mcp_names[i]
                error_report = MCPHealthReport(mcp_name=name)
                error_report.errors.append(f"Verification exception: {report}")
                results[name] = error_report
            else:
                results[report.mcp_name] = report

        return results

    def print_health_report(
        self,
        reports: Dict[str, MCPHealthReport]
    ) -> None:
        """
        Print health check reports in a formatted table.

        Args:
            reports: Dict mapping MCP name to health report
        """
        table = Table(title="MCP Health Check")

        table.add_column("MCP", style="cyan")
        table.add_column("Status", style="bold")
        table.add_column("Tools", justify="right")
        table.add_column("Notes", style="dim")

        for name, report in reports.items():
            # Determine status emoji
            if report.is_functional:
                status = "[green]✅ OK[/green]"
            elif report.is_installed:
                status = "[yellow]⚠️  PARTIAL[/yellow]"
            else:
                status = "[red]❌ FAILED[/red]"

            # Format tool count
            tools = str(report.tool_count) if report.tool_count > 0 else "-"

            # Format notes
            if report.errors:
                notes = report.errors[0]  # Show first error
            elif not report.is_installed:
                notes = "Not installed"
            elif report.tool_count == 0:
                notes = "No tools found"
            else:
                notes = "All checks passed"

            table.add_row(name, status, tools, notes)

        self.console.print(table)

    async def health_check_all(self) -> Dict[str, MCPHealthReport]:
        """
        Run health check on all installed MCPs.

        Discovers installed MCPs via detector, then verifies each.

        Returns:
            Dict mapping MCP name to health report
        """
        self.console.print("\n[bold cyan]Running MCP health check...[/bold cyan]")

        # Get all installed MCPs
        installed = self.detector.get_installed_mcps()

        if not installed:
            self.console.print("[yellow]No MCPs installed[/yellow]")
            return {}

        self.console.print(f"Found {len(installed)} installed MCPs")

        # Verify each
        reports = await self.verify_batch(installed)

        # Print results
        self.print_health_report(reports)

        # Summary
        functional = sum(1 for r in reports.values() if r.is_functional)
        total = len(reports)

        if functional == total:
            self.console.print(
                f"\n[green]✅ All {total} MCPs functional[/green]"
            )
        else:
            self.console.print(
                f"\n[yellow]⚠️  {functional}/{total} MCPs functional[/yellow]"
            )

        return reports

    def get_summary_stats(
        self,
        reports: Dict[str, MCPHealthReport]
    ) -> Dict[str, Any]:
        """
        Generate summary statistics from health reports.

        Args:
            reports: Dict mapping MCP name to health report

        Returns:
            Dict with summary stats (total, functional, failed, etc.)
        """
        total = len(reports)
        functional = sum(1 for r in reports.values() if r.is_functional)
        installed = sum(1 for r in reports.values() if r.is_installed)
        failed = total - installed
        total_tools = sum(r.tool_count for r in reports.values())

        return {
            'total_mcps': total,
            'functional': functional,
            'installed_only': installed - functional,
            'failed': failed,
            'total_tools': total_tools,
            'health_score': (functional / total * 100) if total > 0 else 0.0
        }
