"""Interactive setup wizard for Shannon CLI.

Guides users through complete Shannon CLI configuration including:
- Python version verification
- Claude Agent SDK installation
- Shannon Framework detection/installation
- Serena MCP integration (optional)
- End-to-end verification

The wizard provides multiple installation paths:
- Plugin system (recommended)
- Git clone (manual)
- Bundled snapshot (offline)
"""

import subprocess
import sys
import shutil
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.panel import Panel
from rich.table import Table
from rich import box

from shannon.setup.framework_detector import FrameworkDetector


class SetupWizard:
    """Guide user through Shannon CLI setup with interactive prompts.

    Provides step-by-step setup process with validation at each stage.
    Handles errors gracefully and provides clear guidance for manual steps.

    Attributes:
        console: Rich console for formatted output

    Example:
        >>> wizard = SetupWizard()
        >>> success = wizard.run()
        >>> if success:
        ...     print("Setup complete!")
    """

    def __init__(self):
        """Initialize setup wizard with Rich console."""
        self.console = Console()

    def run(self) -> bool:
        """Run complete setup wizard.

        Executes all setup steps in sequence:
        1. Python version check
        2. Claude Agent SDK installation
        3. Shannon Framework detection/installation
        4. Serena MCP check (optional)
        5. Integration verification

        Returns:
            True if setup completed successfully, False otherwise
        """
        self.console.print(Panel(
            "[bold cyan]Shannon CLI Setup Wizard[/bold cyan]\n\n"
            "Welcome! This wizard will help you set up Shannon CLI and verify\n"
            "that Shannon Framework is properly installed and accessible.\n\n"
            "Setup takes 2-5 minutes depending on your installation method.",
            border_style="cyan",
            box=box.DOUBLE
        ))

        # Step 1: Check Python version
        self.console.print("\n[bold]Step 1/5:[/bold] Python Version Check")
        if not self._check_python_version():
            return False

        # Step 2: Check Claude Agent SDK
        self.console.print("\n[bold]Step 2/5:[/bold] Claude Agent SDK")
        if not self._check_agent_sdk():
            if not self._install_agent_sdk():
                return False

        # Step 3: Find/Install Shannon Framework
        self.console.print("\n[bold]Step 3/5:[/bold] Shannon Framework Detection")
        framework_path = FrameworkDetector.find_framework()

        if framework_path:
            self.console.print(f"[green]✓[/green] Shannon Framework found: {framework_path}")

            # Verify it's complete
            is_valid, message = FrameworkDetector.verify_framework(framework_path)
            if is_valid:
                self.console.print(f"[green]✓[/green] {message}")
                self._save_framework_path(framework_path)
            else:
                self.console.print(f"[yellow]⚠[/yellow] Framework incomplete: {message}")
                if not self._fix_framework(framework_path):
                    return False
        else:
            self.console.print("[yellow]⚠[/yellow] Shannon Framework not found")
            if not self._install_framework():
                return False

        # Step 4: Check Serena MCP (recommended but optional)
        self.console.print("\n[bold]Step 4/5:[/bold] Serena MCP Integration (Optional)")
        self._check_serena_mcp()

        # Step 5: Verify everything works
        self.console.print("\n[bold]Step 5/5:[/bold] Final Verification")
        if not self._verify_integration():
            return False

        # Success!
        self.console.print(Panel(
            "[bold green]✅ Setup Complete![/bold green]\n\n"
            "Shannon CLI is ready to use.\n\n"
            "Try these commands:\n"
            "  [cyan]shannon analyze spec.md[/cyan]      - Analyze a specification\n"
            "  [cyan]shannon wave requirements.md[/cyan] - Plan implementation waves\n"
            "  [cyan]shannon test[/cyan]                 - Run validation tests\n\n"
            "For help: [cyan]shannon --help[/cyan]",
            border_style="green",
            box=box.DOUBLE
        ))

        return True

    def _check_python_version(self) -> bool:
        """Check Python version is 3.10 or higher.

        Returns:
            True if Python version is sufficient, False otherwise
        """
        version = sys.version_info
        if version.major >= 3 and version.minor >= 10:
            self.console.print(
                f"[green]✓[/green] Python {version.major}.{version.minor}.{version.micro} detected"
            )
            return True
        else:
            self.console.print(
                f"[red]✗[/red] Python {version.major}.{version.minor} detected (need 3.10+)\n"
                "\nPlease upgrade Python:\n"
                "  - macOS: brew install python@3.11\n"
                "  - Ubuntu: sudo apt install python3.11\n"
                "  - Windows: python.org/downloads"
            )
            return False

    def _check_agent_sdk(self) -> bool:
        """Check if claude-agent-sdk is installed.

        Returns:
            True if SDK is installed, False otherwise
        """
        try:
            import claude_agent_sdk
            version = getattr(claude_agent_sdk, '__version__', 'unknown')
            self.console.print(f"[green]✓[/green] Claude Agent SDK {version} installed")
            return True
        except ImportError:
            self.console.print("[yellow]⚠[/yellow] Claude Agent SDK not found")
            return False

    def _install_agent_sdk(self) -> bool:
        """Install Claude Agent SDK with user confirmation.

        Returns:
            True if installation succeeded, False otherwise
        """
        if Confirm.ask("Install Claude Agent SDK now?", default=True):
            try:
                self.console.print("Installing Claude Agent SDK...")
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "claude-agent-sdk"],
                    check=True,
                    capture_output=True
                )
                self.console.print("[green]✓[/green] Claude Agent SDK installed successfully")
                return True
            except subprocess.CalledProcessError as e:
                self.console.print(
                    f"[red]✗[/red] Installation failed: {e}\n"
                    "\nManual installation:\n"
                    f"  {sys.executable} -m pip install claude-agent-sdk"
                )
                return False
        else:
            self.console.print(
                "[yellow]⚠[/yellow] Skipped. Manual installation required:\n"
                f"  {sys.executable} -m pip install claude-agent-sdk"
            )
            return False

    def _install_framework(self) -> bool:
        """Guide user through Shannon Framework installation.

        Presents three installation options:
        1. Claude Code plugin system (recommended)
        2. Git clone (manual control)
        3. Bundled snapshot (offline)

        Returns:
            True if framework installed successfully, False otherwise
        """
        self.console.print("\n[bold]Shannon Framework Installation Options:[/bold]\n")

        table = Table(show_header=True, header_style="bold cyan", box=box.SIMPLE)
        table.add_column("Option", style="cyan", width=8)
        table.add_column("Method", style="white", width=30)
        table.add_column("Pros/Cons", style="dim")

        table.add_row(
            "1",
            "Claude Code Plugin System",
            "[green]Recommended[/green] - Auto-updates, integrated"
        )
        table.add_row(
            "2",
            "Git Clone (Manual)",
            "[yellow]Advanced[/yellow] - Full control, latest changes"
        )
        table.add_row(
            "3",
            "Bundled Snapshot",
            "[dim]Offline[/dim] - No updates, limited features"
        )

        self.console.print(table)
        self.console.print()

        choice = Prompt.ask(
            "Choose installation method",
            choices=["1", "2", "3"],
            default="1"
        )

        if choice == "1":
            return self._install_via_plugin_system()
        elif choice == "2":
            return self._install_via_git()
        else:
            return self._use_bundled_framework()

    def _install_via_plugin_system(self) -> bool:
        """Install Shannon Framework via Claude Code plugin system.

        Returns:
            True if installation verified, False otherwise
        """
        self.console.print("\n[bold]Installing via Claude Code Plugin System[/bold]\n")
        self.console.print("Follow these steps in Claude Code:\n")

        steps = Panel(
            "[cyan]1.[/cyan] Open Claude Code\n"
            "[cyan]2.[/cyan] Run: [bold]/plugin marketplace add shannon-framework/shannon[/bold]\n"
            "[cyan]3.[/cyan] Run: [bold]/plugin install shannon@shannon-framework[/bold]\n"
            "[cyan]4.[/cyan] Verify installation appears in plugin list\n",
            title="Installation Steps",
            border_style="cyan"
        )
        self.console.print(steps)

        if Confirm.ask("\nHave you completed these steps?", default=False):
            # Verify installation
            plugin_path = Path.home() / '.claude' / 'plugins' / 'shannon'
            if plugin_path.exists():
                is_valid, message = FrameworkDetector.verify_framework(plugin_path)
                if is_valid:
                    self.console.print(f"[green]✓[/green] {message}")
                    self._save_framework_path(plugin_path)
                    return True
                else:
                    self.console.print(f"[yellow]⚠[/yellow] Installation incomplete: {message}")
                    return False
            else:
                self.console.print(
                    f"[yellow]⚠[/yellow] Framework not found at expected location: {plugin_path}\n"
                    "Please check Claude Code plugin installation."
                )
                return False
        else:
            self.console.print("[yellow]⚠[/yellow] Installation not completed. Please try again later.")
            return False

    def _install_via_git(self) -> bool:
        """Install Shannon Framework via Git clone.

        Returns:
            True if installation succeeded, False otherwise
        """
        self.console.print("\n[bold]Installing via Git Clone[/bold]\n")

        # Check if git is available
        if not shutil.which('git'):
            self.console.print(
                "[red]✗[/red] Git not found. Please install Git:\n"
                "  - macOS: brew install git\n"
                "  - Ubuntu: sudo apt install git\n"
                "  - Windows: git-scm.com/downloads"
            )
            return False

        # Suggest installation location
        default_path = Path.home() / 'Desktop' / 'shannon-framework'
        install_path = Prompt.ask(
            "Installation directory",
            default=str(default_path)
        )
        install_path = Path(install_path)

        if install_path.exists():
            self.console.print(f"[yellow]⚠[/yellow] Directory already exists: {install_path}")
            if not Confirm.ask("Use existing directory?", default=True):
                return False
        else:
            # Clone repository
            try:
                self.console.print(f"Cloning Shannon Framework to {install_path}...")
                subprocess.run(
                    [
                        'git', 'clone',
                        'https://github.com/shannon-framework/shannon.git',
                        str(install_path)
                    ],
                    check=True,
                    capture_output=True
                )
                self.console.print("[green]✓[/green] Repository cloned successfully")
            except subprocess.CalledProcessError as e:
                self.console.print(f"[red]✗[/red] Clone failed: {e}")
                return False

        # Verify installation
        is_valid, message = FrameworkDetector.verify_framework(install_path)
        if is_valid:
            self.console.print(f"[green]✓[/green] {message}")
            self._save_framework_path(install_path)
            return True
        else:
            self.console.print(f"[red]✗[/red] Installation invalid: {message}")
            return False

    def _use_bundled_framework(self) -> bool:
        """Use bundled Shannon Framework snapshot.

        Returns:
            True if bundled framework is valid, False otherwise
        """
        self.console.print("\n[bold]Using Bundled Framework Snapshot[/bold]\n")

        bundled_path = Path(__file__).parent.parent / 'bundled' / 'shannon-framework'

        if not bundled_path.exists():
            self.console.print(
                "[red]✗[/red] Bundled framework not found.\n"
                "This installation may not include a bundled framework.\n"
                "Please choose option 1 or 2 instead."
            )
            return False

        is_valid, message = FrameworkDetector.verify_framework(bundled_path)
        if is_valid:
            self.console.print(f"[green]✓[/green] {message}")
            self.console.print(
                "[yellow]Note:[/yellow] Bundled framework won't receive automatic updates.\n"
                "Consider installing via Claude Code plugin system for latest features."
            )
            self._save_framework_path(bundled_path)
            return True
        else:
            self.console.print(f"[red]✗[/red] Bundled framework invalid: {message}")
            return False

    def _fix_framework(self, path: Path) -> bool:
        """Attempt to fix incomplete framework installation.

        Args:
            path: Path to incomplete framework

        Returns:
            True if framework fixed, False otherwise
        """
        self.console.print(f"\n[bold]Attempting to repair framework at {path}[/bold]\n")

        # Check if it's a git repo
        if (path / '.git').exists():
            if Confirm.ask("Pull latest changes from Git?", default=True):
                try:
                    subprocess.run(
                        ['git', '-C', str(path), 'pull'],
                        check=True,
                        capture_output=True
                    )
                    self.console.print("[green]✓[/green] Updated from Git")

                    # Re-verify
                    is_valid, message = FrameworkDetector.verify_framework(path)
                    if is_valid:
                        self.console.print(f"[green]✓[/green] {message}")
                        return True
                except subprocess.CalledProcessError as e:
                    self.console.print(f"[yellow]⚠[/yellow] Git pull failed: {e}")

        self.console.print(
            "[yellow]⚠[/yellow] Could not automatically repair framework.\n"
            "Recommendation: Reinstall using option 1 or 2."
        )
        return Confirm.ask("Continue with incomplete framework?", default=False)

    def _check_serena_mcp(self):
        """Check for Serena MCP integration (optional enhancement)."""
        self.console.print(
            "[dim]Serena MCP provides enhanced code analysis capabilities.[/dim]\n"
            "This is optional but recommended for advanced features.\n"
        )

        serena_path = Path.home() / '.claude' / 'mcp' / 'serena'
        if serena_path.exists():
            self.console.print(f"[green]✓[/green] Serena MCP detected at {serena_path}")
        else:
            self.console.print(
                "[yellow]⚠[/yellow] Serena MCP not detected\n"
                "\nTo install Serena MCP, see:\n"
                "  https://github.com/jamiewilson/serena-mcp"
            )

    def _verify_integration(self) -> bool:
        """Verify Shannon CLI can access framework.

        Returns:
            True if verification passed, False otherwise
        """
        framework_path = FrameworkDetector.find_framework()

        if not framework_path:
            self.console.print("[red]✗[/red] Framework not accessible")
            return False

        is_valid, message = FrameworkDetector.verify_framework(framework_path)

        if is_valid:
            self.console.print(f"[green]✓[/green] {message}")
            self.console.print(f"[green]✓[/green] Framework accessible at: {framework_path}")
            return True
        else:
            self.console.print(f"[red]✗[/red] Verification failed: {message}")
            return False

    def _save_framework_path(self, path: Path):
        """Save framework path to CLI configuration.

        Args:
            path: Path to framework installation
        """
        try:
            from shannon.config import ShannonConfig
            config = ShannonConfig()
            config.framework_path = str(path)
            config.save()
            self.console.print(f"[dim]Framework path saved to config: {path}[/dim]")
        except Exception as e:
            self.console.print(f"[yellow]⚠[/yellow] Could not save config: {e}")

    def show_diagnostics(self):
        """Show diagnostic information about all framework locations.

        Useful for troubleshooting installation issues.
        """
        self.console.print("\n[bold]Shannon Framework Diagnostics[/bold]\n")

        locations = FrameworkDetector.search_all_locations()

        table = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED)
        table.add_column("Location", style="cyan", width=30)
        table.add_column("Path", style="white", width=40)
        table.add_column("Status", style="white", width=20)

        for loc in locations:
            status = "❌ Not Found"
            if loc['exists']:
                if loc['is_valid']:
                    status = "✅ Valid"
                else:
                    status = "⚠️ Invalid"

            table.add_row(
                loc['location_name'],
                loc['path'] or "[dim]None[/dim]",
                status
            )

        self.console.print(table)
