"""
MCP Installer - Automated MCP installation with progress feedback.

Installation flow:
1. Run `claude mcp add {name}`
2. Wait for completion with timeout
3. Verify installation via detector
4. Report success/failure with Rich UI

Integrates with:
- MCPDetector for verification
- Rich for progress display
- Setup wizard for batch installation
"""

import asyncio
import logging
import subprocess
from typing import Dict, List, Optional, Any

from rich.console import Console
from rich.prompt import Confirm, Prompt


class MCPInstaller:
    """
    Handles MCP installation with progress feedback.

    Features:
    - Single MCP installation with progress
    - Batch installation with selective mode
    - Timeout handling (120s default)
    - Verification after install
    - User-friendly error messages
    """

    def __init__(self, detector):
        """
        Initialize installer with detector for verification.

        Args:
            detector: MCPDetector instance for post-install verification
        """
        self.detector = detector
        self.console = Console()
        self.logger = logging.getLogger(__name__)

    async def install_with_progress(
        self,
        mcp_name: str,
        timeout: int = 120
    ) -> bool:
        """
        Install MCP with visual progress feedback.

        Steps:
        1. Run `claude mcp add {mcp_name}`
        2. Wait for completion
        3. Give MCP time to initialize
        4. Verify installation
        5. Report results

        Args:
            mcp_name: Name of MCP to install
            timeout: Max seconds to wait for installation (default: 120)

        Returns:
            True if installed and verified, False otherwise
        """
        self.console.print(f"\n[bold cyan]Installing {mcp_name} MCP[/bold cyan]")

        # Step 1: Run installation command
        with self.console.status(
            f"[bold green]Running: claude mcp add {mcp_name}[/bold green]"
        ):
            try:
                result = subprocess.run(
                    ['claude', 'mcp', 'add', mcp_name],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )

                if result.returncode != 0:
                    self.console.print(f"[red]✗ Installation failed[/red]")
                    self.console.print(f"[dim]{result.stderr}[/dim]")
                    self.logger.error(
                        f"Installation failed for {mcp_name}: {result.stderr}"
                    )
                    return False

                self.console.print(f"[green]✓ Installation command completed[/green]")

            except subprocess.TimeoutExpired:
                self.console.print(
                    f"[red]✗ Installation timed out after {timeout}s[/red]"
                )
                self.logger.error(f"Installation timeout for {mcp_name}")
                return False

            except FileNotFoundError:
                self.console.print(
                    "[red]✗ claude CLI not found[/red]\n"
                    "[dim]Is Claude Code installed?[/dim]"
                )
                self.logger.error("claude CLI not found")
                return False

        # Step 2: Wait for MCP to initialize
        self.console.print(f"  ⠋ Waiting for {mcp_name} to initialize...")
        await asyncio.sleep(2)  # Give MCP time to start

        # Step 3: Verify installation
        self.console.print(f"  ⠋ Verifying {mcp_name}...")

        if await self.detector.check_installed(mcp_name):
            # Get available tools
            tools = await self.detector.get_available_tools(mcp_name)

            self.console.print(
                f"[green]✅ {mcp_name} installed successfully[/green]"
            )

            # Show tools if available
            if tools:
                self.console.print(
                    f"[dim]  Tools: {', '.join(tools[:5])}"
                    f"{'...' if len(tools) > 5 else ''}[/dim]"
                )
            else:
                self.console.print(
                    f"[dim]  Tool discovery not yet available[/dim]"
                )

            return True

        else:
            self.console.print(
                f"[yellow]⚠️  Installed but not responding[/yellow]\n"
                f"[dim]May need to restart Claude Code[/dim]"
            )
            self.logger.warning(
                f"MCP {mcp_name} installed but verification failed"
            )
            return False

    async def install_batch(
        self,
        mcps: List[Dict[str, Any]],
        mode: str = "all"
    ) -> Dict[str, bool]:
        """
        Install multiple MCPs with user control.

        Modes:
        - 'all': Install all MCPs automatically
        - 'selective': Prompt for each MCP
        - 'skip': Skip installation

        Args:
            mcps: List of MCP dicts with 'name', 'purpose', etc.
            mode: Installation mode ('all', 'selective', 'skip')

        Returns:
            Dict mapping MCP name to installation success
            Example: {'serena': True, 'context7': False}
        """
        if mode == "skip":
            self.console.print("[yellow]Skipping MCP installation[/yellow]")
            return {}

        results = {}

        for i, mcp in enumerate(mcps, 1):
            self.console.print(
                f"\n[bold]Installing MCP {i}/{len(mcps)}[/bold]"
            )

            # Show MCP info
            name = mcp.get('name', mcp.get('mcp_name', 'unknown'))
            purpose = mcp.get('purpose', mcp.get('justification', ''))

            if purpose:
                self.console.print(f"[dim]Purpose: {purpose}[/dim]")

            # Selective mode: ask for each MCP
            if mode == "selective":
                if not Confirm.ask(f"Install {name}?"):
                    self.console.print(f"[yellow]Skipped {name}[/yellow]")
                    results[name] = False
                    continue

            # Install
            success = await self.install_with_progress(name)
            results[name] = success

        # Summary
        self._print_summary(results)

        return results

    def _print_summary(self, results: Dict[str, bool]) -> None:
        """
        Print installation summary.

        Args:
            results: Dict mapping MCP name to success status
        """
        self.console.print("\n[bold]Installation Summary[/bold]")

        successful = [name for name, success in results.items() if success]
        failed = [name for name, success in results.items() if not success]

        self.console.print(
            f"  Installed: {len(successful)}/{len(results)}"
        )

        if successful:
            self.console.print("[green]✓ Successful:[/green]")
            for name in successful:
                self.console.print(f"    - {name}")

        if failed:
            self.console.print("[red]✗ Failed:[/red]")
            for name in failed:
                self.console.print(f"    - {name}")

    async def verify_mcp(self, mcp_name: str) -> bool:
        """
        Verify MCP is installed and functional.

        Wrapper around detector.check_installed with logging.

        Args:
            mcp_name: Name of MCP to verify

        Returns:
            True if MCP is functional, False otherwise
        """
        self.logger.info(f"Verifying MCP: {mcp_name}")
        installed = await self.detector.check_installed(mcp_name)

        if installed:
            self.logger.info(f"MCP {mcp_name} verified successfully")
        else:
            self.logger.warning(f"MCP {mcp_name} verification failed")

        return installed

    def uninstall_mcp(self, mcp_name: str) -> bool:
        """
        Uninstall MCP via claude CLI.

        Args:
            mcp_name: Name of MCP to uninstall

        Returns:
            True if uninstall succeeded, False otherwise
        """
        self.console.print(f"\n[bold cyan]Uninstalling {mcp_name} MCP[/bold cyan]")

        try:
            result = subprocess.run(
                ['claude', 'mcp', 'remove', mcp_name],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                self.console.print(f"[green]✅ {mcp_name} uninstalled[/green]")
                return True
            else:
                self.console.print(f"[red]✗ Uninstall failed[/red]")
                self.console.print(f"[dim]{result.stderr}[/dim]")
                return False

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.console.print(f"[red]✗ Uninstall error: {e}[/red]")
            return False
