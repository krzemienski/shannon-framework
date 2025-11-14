"""
MCP Manager - Unified MCP management interface.

Coordinates detector, installer, and verifier for complete MCP lifecycle:
- Auto-install workflow (post-analysis, pre-wave)
- Health checking
- Batch operations
- Integration with cache and analytics

This is the primary interface used by Shannon CLI commands.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any

from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from .detector import MCPDetector
from .installer import MCPInstaller
from .verifier import MCPVerifier


class MCPManager:
    """
    Unified MCP management interface.

    Integrates detector, installer, and verifier into cohesive workflows.

    Integration points:
    - Post-analysis: Auto-install recommended MCPs
    - Pre-wave: Verify required MCPs
    - Setup wizard: Install base MCPs
    - Health checks: Verify all MCPs

    Used by:
    - shannon analyze (post-analysis auto-install)
    - shannon wave (pre-wave verification)
    - shannon setup (initial MCP setup)
    - /shannon:check_mcps (health check command)
    """

    def __init__(self, cache_manager=None):
        """
        Initialize MCP manager with integrated components.

        Args:
            cache_manager: Optional CacheManager for MCP recommendations
        """
        self.detector = MCPDetector()
        self.installer = MCPInstaller(self.detector)
        self.verifier = MCPVerifier(self.detector)
        self.cache_manager = cache_manager
        self.console = Console()
        self.logger = logging.getLogger(__name__)

    async def post_analysis_check(
        self,
        analysis_result: Dict[str, Any]
    ) -> Dict[str, bool]:
        """
        After analyze completes, check and install recommended MCPs.

        Workflow:
        1. Extract MCP recommendations from analysis
        2. Filter to Tier 1-2 (mandatory and primary)
        3. Check which are missing
        4. Show recommendations table
        5. Prompt user for installation
        6. Install and verify

        Called by: shannon analyze
        Timing: After analysis, before returning to user

        Args:
            analysis_result: Dict with 'mcp_recommendations' key

        Returns:
            Dict mapping MCP name to installation success
        """
        recommendations = analysis_result.get('mcp_recommendations', [])

        if not recommendations:
            self.logger.info("No MCP recommendations in analysis result")
            return {}

        # Filter to critical MCPs (Tier 1-2)
        critical = [
            mcp for mcp in recommendations
            if mcp.get('tier', 3) <= 2
        ]

        if not critical:
            self.console.print(
                "[green]✅ All recommended MCPs already installed[/green]"
            )
            return {}

        # Check installation status
        status = await self.detector.check_all_recommended(critical)
        missing = [
            mcp for mcp in critical
            if not status.get(mcp.get('name', mcp.get('mcp_name')), False)
        ]

        if not missing:
            self.console.print(
                "[green]✅ All recommended MCPs already installed[/green]"
            )
            return {}

        # Show recommendations
        self._show_recommendations_table(missing)

        # Prompt user
        choice = Prompt.ask(
            "\nInstall missing MCPs?",
            choices=["all", "selective", "skip"],
            default="all"
        )

        if choice == "skip":
            self.console.print("[yellow]Skipping MCP installation[/yellow]")
            return {}

        # Install
        results = await self.installer.install_batch(missing, mode=choice)

        # Verify installed MCPs
        if results:
            await self._verify_installed(results)

        return results

    async def pre_wave_check(
        self,
        wave_plan: Dict[str, Any]
    ) -> bool:
        """
        Before wave execution, verify required MCPs are available.

        Workflow:
        1. Extract required MCPs from wave plan
        2. Check installation status
        3. If missing, prompt for installation
        4. Verify all required MCPs functional

        Called by: shannon wave
        Timing: Before spawning agents

        Args:
            wave_plan: Dict with 'required_mcps' key

        Returns:
            True if all required MCPs available, False otherwise
        """
        required = wave_plan.get('required_mcps', [])

        if not required:
            return True  # No MCP requirements

        # Check all required MCPs
        status = await self.detector.check_all_recommended([
            {'name': mcp} for mcp in required
        ])

        missing = [
            mcp for mcp in required
            if not status.get(mcp, False)
        ]

        if not missing:
            self.console.print(
                "[green]✅ All required MCPs available[/green]"
            )
            return True

        # Some missing
        self.console.print(
            "[yellow]⚠️  Wave requires MCPs that aren't installed:[/yellow]"
        )
        for mcp in missing:
            self.console.print(f"  - {mcp}")

        if Confirm.ask("\nInstall required MCPs before starting wave?"):
            results = await self.installer.install_batch([
                {'name': mcp} for mcp in missing
            ], mode="all")

            # Verify all succeeded
            all_success = all(results.values())

            if all_success:
                self.console.print(
                    "[green]✅ All required MCPs installed[/green]"
                )
            else:
                self.console.print(
                    "[red]⚠️  Some MCPs failed to install[/red]"
                )

            return all_success
        else:
            self.console.print(
                "[red]Warning: Wave may fail without required MCPs[/red]"
            )
            return Confirm.ask("Proceed anyway?")

    async def setup_base_mcps(self) -> Dict[str, bool]:
        """
        Install base MCPs during setup wizard.

        Base MCPs:
        - serena (mandatory for Shannon Framework)
        - context7 (recommended for documentation)

        Returns:
            Dict mapping MCP name to installation success
        """
        self.console.print("\n[bold cyan]Installing base MCPs[/bold cyan]")

        base_mcps = [
            {
                'name': 'serena',
                'purpose': 'Context preservation for Shannon Framework',
                'tier': 1
            },
            {
                'name': 'context7',
                'purpose': 'Up-to-date documentation for Python/Rich/SDK',
                'tier': 2
            }
        ]

        # Check which are missing
        status = await self.detector.check_all_recommended(base_mcps)
        missing = [
            mcp for mcp in base_mcps
            if not status.get(mcp['name'], False)
        ]

        if not missing:
            self.console.print("[green]✅ Base MCPs already installed[/green]")
            return {mcp['name']: True for mcp in base_mcps}

        # Show table
        self._show_recommendations_table(missing)

        # Install (default to all)
        choice = Prompt.ask(
            "\nInstall base MCPs?",
            choices=["all", "selective", "skip"],
            default="all"
        )

        if choice == "skip":
            return {}

        results = await self.installer.install_batch(missing, mode=choice)

        # Verify
        await self._verify_installed(results)

        return results

    async def health_check(self) -> Dict[str, Any]:
        """
        Run complete health check on all installed MCPs.

        Returns:
            Dict with health reports and summary stats
        """
        reports = await self.verifier.health_check_all()
        stats = self.verifier.get_summary_stats(reports)

        return {
            'reports': reports,
            'stats': stats
        }

    def _show_recommendations_table(
        self,
        mcps: List[Dict[str, Any]]
    ) -> None:
        """
        Display recommendations in formatted table.

        Args:
            mcps: List of MCP dicts to display
        """
        table = Table(title="Recommended MCPs")

        table.add_column("MCP", style="cyan")
        table.add_column("Tier", justify="center")
        table.add_column("Purpose", style="dim")

        for mcp in mcps:
            name = mcp.get('name', mcp.get('mcp_name', 'unknown'))
            tier = mcp.get('tier', '?')
            purpose = mcp.get('purpose', mcp.get('justification', ''))

            # Tier styling
            tier_str = f"[bold]{tier}[/bold]"
            if tier == 1:
                tier_str = f"[red]{tier}[/red]"
            elif tier == 2:
                tier_str = f"[yellow]{tier}[/yellow]"

            table.add_row(name, tier_str, purpose)

        self.console.print(table)

    async def _verify_installed(
        self,
        results: Dict[str, bool]
    ) -> None:
        """
        Verify newly installed MCPs.

        Args:
            results: Dict mapping MCP name to installation success
        """
        successful = [name for name, success in results.items() if success]

        if not successful:
            return

        self.console.print("\n[bold]Verifying installations...[/bold]")

        reports = await self.verifier.verify_batch(successful)

        # Quick summary
        functional = sum(1 for r in reports.values() if r.is_functional)
        total = len(reports)

        if functional == total:
            self.console.print(
                f"[green]✅ All {total} MCPs verified[/green]"
            )
        else:
            self.console.print(
                f"[yellow]⚠️  {functional}/{total} MCPs verified[/yellow]"
            )
