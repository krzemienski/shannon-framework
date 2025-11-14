"""
Shannon ProgressUI - Real-time Terminal Progress Display

Beautiful Rich-based terminal output that shows users exactly what's happening
as Shannon Framework skills execute. Makes CLI interaction delightful.

Created for: Wave 5 - CLI Integration
Component: ProgressUI (Agent C)
"""

from typing import Any, Dict, List, Optional, Union

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table
from rich.text import Text

# Import SDK types with fallback for testing
try:
    from claude_agent_sdk import AssistantMessage, TextBlock, ToolUseBlock

    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False
    AssistantMessage = Any
    TextBlock = Any
    ToolUseBlock = Any


class ProgressUI:
    """
    Real-time progress display for Shannon operations.

    Provides beautiful terminal output using Rich library for:
    - Skill execution progress with spinners
    - Tool call tracking with checkmarks
    - 8D analysis results with color-coded tables
    - Wave execution status
    - Phase plan summaries

    Example:
        >>> ui = ProgressUI()
        >>> # Track skill execution
        >>> ui.track_skill_execution("spec-analysis", message_stream)
        >>> # Display results
        >>> ui.display_analysis_result(analysis_result)
    """

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize ProgressUI.

        Args:
            console: Optional Rich Console instance (creates new if not provided)
        """
        self.console = console or Console()
        self._last_tool: Optional[str] = None
        self._tool_count = 0

    def track_skill_execution(
        self,
        skill_name: str,
        messages: Union[List, Any],
        show_tools: bool = True,
        show_progress: bool = True,
    ) -> None:
        """
        Show real-time progress while skill executes.

        Displays:
        - Spinner: "⠋ Running spec-analysis skill..."
        - Tool calls: "✓ Read spec.md"
        - Progress steps: "Calculating structural dimension..."
        - Final: "✓ Analysis complete"

        Args:
            skill_name: Name of the skill being executed
            messages: SDK message stream (generator or list)
            show_tools: Whether to show individual tool calls
            show_progress: Whether to show progress updates

        Example:
            >>> ui.track_skill_execution("spec-analysis", sdk_messages)
            ⠋ Running spec-analysis...
            ✓ Read /Users/nick/spec.md
            Calculating structural dimension...
            Calculating cognitive dimension...
            ✓ spec-analysis complete
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(),
            console=self.console,
            transient=True,  # Clear progress after completion
        ) as progress:
            task = progress.add_task(
                f"[cyan]Running {skill_name}...[/cyan]", total=None
            )

            # Reset tracking
            self._last_tool = None
            self._tool_count = 0

            # Process message stream
            try:
                for msg in messages:
                    # Handle ToolUseBlock
                    if SDK_AVAILABLE and isinstance(msg, ToolUseBlock):
                        if show_tools:
                            tool_name = msg.name
                            tool_desc = self._format_tool_description(msg)

                            # Show checkmark for completed tool
                            if self._last_tool:
                                self.console.print(
                                    f"  [green]✓[/green] {self._last_tool}"
                                )

                            self._last_tool = tool_desc
                            self._tool_count += 1

                            progress.update(
                                task,
                                description=f"[cyan]{tool_name}[/cyan]: {tool_desc}",
                            )

                    # Handle TextBlock progress indicators
                    elif SDK_AVAILABLE and isinstance(msg, AssistantMessage):
                        for block in msg.content:
                            if isinstance(block, TextBlock):
                                text = block.text

                                # Show progress indicators
                                if show_progress and any(
                                    keyword in text
                                    for keyword in [
                                        "Calculating",
                                        "Analyzing",
                                        "Processing",
                                        "Generating",
                                        "Evaluating",
                                    ]
                                ):
                                    # Extract first line or truncate
                                    progress_text = text.strip().split("\n")[0][:60]
                                    progress.update(
                                        task,
                                        description=f"[yellow]{progress_text}[/yellow]",
                                    )

                    # Fallback for non-SDK messages (testing)
                    elif hasattr(msg, "content"):
                        if isinstance(msg.content, str):
                            if show_progress and "Calculating" in msg.content:
                                progress.update(
                                    task,
                                    description=f"[yellow]{msg.content[:60]}[/yellow]",
                                )

            except Exception as e:
                progress.update(task, description=f"[red]✗[/red] Error: {e}")
                raise

            # Show final tool completion
            if self._last_tool:
                self.console.print(f"  [green]✓[/green] {self._last_tool}")

            # Final completion message
            progress.update(task, description=f"[green]✓[/green] {skill_name} complete")

        # Show summary
        if self._tool_count > 0:
            self.console.print(
                f"\n[dim]Used {self._tool_count} tool{'s' if self._tool_count != 1 else ''}[/dim]"
            )

    def display_analysis_result(self, result: Dict[str, Any]) -> None:
        """
        Display 8D complexity analysis with Rich tables.

        Shows:
        - Complexity score with color coding
        - 8D dimension breakdown table
        - Domain distribution
        - MCP recommendations summary
        - Phase plan overview

        Args:
            result: Analysis result dict from MessageParser.extract_analysis_result()

        Example:
            >>> ui.display_analysis_result(analysis_result)
            Complexity: 0.68 (COMPLEX)

            ╭─────────────── 8D Complexity Breakdown ───────────────╮
            │ Dimension      │  Score │ Weight │ Contribution │
            ├────────────────┼────────┼────────┼──────────────┤
            │ Structural     │  0.650 │    20% │       0.1300 │
            │ Cognitive      │  0.700 │    15% │       0.1050 │
            ...
        """
        # Extract data
        complexity = result["complexity_score"]
        interpretation = result["interpretation"]
        dimension_scores = result["dimension_scores"]
        domain_percentages = result.get("domain_percentages", {})
        mcp_recommendations = result.get("mcp_recommendations", [])

        # 1. Complexity Score Header
        color = self._get_complexity_color(complexity)
        self.console.print()
        self.console.print(
            Panel(
                Text(
                    f"Complexity: {complexity:.3f} ({interpretation})",
                    style=f"bold {color}",
                    justify="center",
                ),
                border_style=color,
                padding=(0, 2),
            )
        )
        self.console.print()

        # 2. Dimension Breakdown Table
        table = Table(
            title="8D Complexity Breakdown",
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            title_style="bold white",
        )

        table.add_column("Dimension", style="cyan", no_wrap=True)
        table.add_column("Score", justify="right", style="magenta")
        table.add_column("Weight", justify="right", style="green")
        table.add_column("Contribution", justify="right", style="yellow")

        # Add rows for each dimension
        dimension_order = [
            "structural",
            "cognitive",
            "coordination",
            "temporal",
            "technical",
            "scale",
            "uncertainty",
            "dependencies",
        ]

        for dim_name in dimension_order:
            if dim_name in dimension_scores:
                dim_data = dimension_scores[dim_name]
                score = dim_data["score"]
                weight = dim_data["weight"]
                contribution = dim_data.get("contribution", score * weight)

                table.add_row(
                    dim_name.capitalize(),
                    f"{score:.3f}",
                    f"{weight:.0%}",
                    f"{contribution:.4f}",
                )

        self.console.print(table)

        # 3. Domain Breakdown
        if domain_percentages:
            self.console.print("\n[bold]Domain Breakdown:[/bold]")
            # Sort domains by percentage (highest first)
            sorted_domains = sorted(
                domain_percentages.items(), key=lambda x: x[1], reverse=True
            )
            for domain, pct in sorted_domains:
                # Create bar visualization
                bar_length = int(pct / 5)  # 5% per bar unit
                bar = "█" * bar_length
                self.console.print(f"  {domain:20s} [cyan]{bar}[/cyan] {pct}%")

        # 4. MCP Recommendations Summary
        if mcp_recommendations:
            self.console.print(
                f"\n[bold]MCP Recommendations:[/bold] {len(mcp_recommendations)} total"
            )

            # Group by tier
            tier1 = [m for m in mcp_recommendations if m.get("tier") == 1]
            tier2 = [m for m in mcp_recommendations if m.get("tier") == 2]
            tier3 = [m for m in mcp_recommendations if m.get("tier") == 3]

            if tier1:
                self.console.print(f"  [red]⚠ Tier 1 (Required):[/red] {len(tier1)}")
                for mcp in tier1[:3]:  # Show first 3
                    self.console.print(
                        f"    • [cyan]{mcp['name']}[/cyan] - {mcp['purpose']}"
                    )

            if tier2:
                self.console.print(
                    f"  [yellow]⚡ Tier 2 (Recommended):[/yellow] {len(tier2)}"
                )

            if tier3:
                self.console.print(f"  [dim]✓ Tier 3 (Optional):[/dim] {len(tier3)}")

        # 5. Execution Strategy & Timeline
        strategy = result.get("execution_strategy", "sequential")
        timeline = result.get("timeline_estimate", "See phase plan")

        self.console.print(f"\n[bold]Execution Strategy:[/bold] {strategy}")
        self.console.print(f"[bold]Timeline Estimate:[/bold] {timeline}")

        self.console.print()

    def display_wave_progress(
        self,
        wave_number: int,
        wave_name: str,
        agent_count: int,
        status: str = "starting",
    ) -> None:
        """
        Show wave execution progress.

        Args:
            wave_number: Wave number (1-5)
            wave_name: Name of the wave (e.g., "Foundation")
            agent_count: Number of agents in this wave
            status: Status message ("starting", "running", "complete")

        Example:
            >>> ui.display_wave_progress(1, "Foundation", 3, "starting")
            🌊 Wave 1: Foundation (3 agents)
            >>> ui.display_wave_progress(1, "Foundation", 3, "complete")
            ✓ Wave 1 complete
        """
        if status == "starting":
            self.console.print(
                f"\n[bold blue]🌊 Wave {wave_number}: {wave_name}[/bold blue] "
                f"({agent_count} agent{'s' if agent_count != 1 else ''})"
            )
        elif status == "complete":
            self.console.print(
                f"[green]✓[/green] [bold]Wave {wave_number} complete[/bold]\n"
            )
        else:
            self.console.print(f"[cyan]⠋[/cyan] Wave {wave_number}: {status}")

    def display_phase_plan(self, phases: List[Dict[str, Any]]) -> None:
        """
        Display 5-phase implementation plan.

        Args:
            phases: List of phase dicts from analysis result

        Example:
            >>> ui.display_phase_plan(result['phase_plan'])
            ╭────────── 5-Phase Implementation Plan ──────────╮
            │ Phase 1: Foundation (20%)                      │
            │ Phase 2: Core Systems (25%)                    │
            ...
        """
        table = Table(
            title="5-Phase Implementation Plan",
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
        )

        table.add_column("Phase", style="cyan", no_wrap=True)
        table.add_column("Name", style="white")
        table.add_column("Duration", justify="right", style="yellow")
        table.add_column("Objectives", style="dim")

        for phase in phases:
            phase_num = phase["phase_number"]
            phase_name = phase["phase_name"]
            duration_pct = phase.get("duration_percent", 20)
            objectives = phase.get("objectives", [])

            # Format objectives (show first 2)
            obj_summary = ", ".join(objectives[:2])
            if len(objectives) > 2:
                obj_summary += f" (+{len(objectives) - 2} more)"

            table.add_row(
                f"Phase {phase_num}",
                phase_name,
                f"{duration_pct}%",
                obj_summary[:50],
            )

        self.console.print()
        self.console.print(table)
        self.console.print()

    def display_session_summary(self, session_data: Dict[str, Any]) -> None:
        """
        Display session information summary.

        Args:
            session_data: Session metadata dict

        Example:
            >>> ui.display_session_summary({
            ...     "session_id": "20250113_143022",
            ...     "spec_file": "spec.md",
            ...     "complexity": 0.68
            ... })
        """
        session_id = session_data.get("session_id", "unknown")
        spec_file = session_data.get("spec_file", "unknown")

        panel = Panel(
            f"[bold]Session:[/bold] {session_id}\n" f"[bold]Spec:[/bold] {spec_file}",
            title="[bold cyan]Shannon Session[/bold cyan]",
            border_style="cyan",
        )

        self.console.print()
        self.console.print(panel)
        self.console.print()

    def show_error(self, message: str, details: Optional[str] = None) -> None:
        """
        Display error message.

        Args:
            message: Error message
            details: Optional detailed error information
        """
        error_panel = Panel(
            f"[bold red]{message}[/bold red]"
            + (f"\n\n[dim]{details}[/dim]" if details else ""),
            title="[bold red]Error[/bold red]",
            border_style="red",
        )

        self.console.print()
        self.console.print(error_panel)
        self.console.print()

    def show_success(self, message: str) -> None:
        """
        Display success message.

        Args:
            message: Success message
        """
        self.console.print(f"\n[green]✓[/green] [bold]{message}[/bold]\n")

    def success(self, message: str) -> None:
        """Alias for show_success."""
        self.show_success(message)

    def error(self, message: str, details: Optional[str] = None) -> None:
        """Alias for show_error."""
        self.show_error(message, details)

    def display_wave_result(self, result: Dict[str, Any]) -> None:
        """
        Display wave execution results.

        Args:
            result: Wave result dict from MessageParser.extract_wave_result()
        """
        wave_number = result.get("wave_number", 1)
        wave_name = result.get("wave_name", "Unknown")
        agents_deployed = result.get("agents_deployed", 0)
        execution_time = result.get("execution_time_minutes", 0.0)
        files_created = result.get("files_created", [])
        components_built = result.get("components_built", [])
        tests_created = result.get("tests_created", 0)
        no_mocks = result.get("no_mocks_confirmed", False)

        # Display header
        self.console.print()
        self.console.print(f"[bold cyan]Wave {wave_number}: {wave_name}[/bold cyan]")
        self.console.print()

        # Summary metrics
        self.console.print(f"[bold]Agents Deployed:[/bold] {agents_deployed}")
        self.console.print(f"[bold]Execution Time:[/bold] {execution_time:.1f} minutes")
        self.console.print(f"[bold]Files Created:[/bold] {len(files_created)}")
        self.console.print(f"[bold]Components Built:[/bold] {len(components_built)}")
        self.console.print(f"[bold]Tests Created:[/bold] {tests_created}")

        # NO MOCKS confirmation
        if no_mocks:
            self.console.print("[green]✓ NO MOCKS confirmed[/green]")
        else:
            self.console.print("[yellow]⚠ Mocks may have been used[/yellow]")

        # Files created
        if files_created:
            self.console.print("\n[bold]Files Created:[/bold]")
            for file_path in files_created[:10]:  # Show first 10
                self.console.print(f"  • {file_path}")
            if len(files_created) > 10:
                self.console.print(f"  [dim]... and {len(files_created) - 10} more[/dim]")

        # Components built
        if components_built:
            self.console.print("\n[bold]Components Built:[/bold]")
            for component in components_built[:5]:  # Show first 5
                self.console.print(f"  • {component}")
            if len(components_built) > 5:
                self.console.print(f"  [dim]... and {len(components_built) - 5} more[/dim]")

        self.console.print()

    def display_session_status(
        self,
        session_id: str,
        analysis: Optional[Dict[str, Any]],
        wave_count: int
    ) -> None:
        """
        Display session status information.

        Args:
            session_id: Session identifier
            analysis: Analysis result dict (if available)
            wave_count: Number of completed waves
        """
        self.console.print()
        self.console.print(f"[bold cyan]Session Status: {session_id}[/bold cyan]")
        self.console.print()

        if analysis:
            complexity = analysis.get("complexity_score", 0.0)
            interpretation = analysis.get("interpretation", "Unknown")
            color = self._get_complexity_color(complexity)

            self.console.print(f"[bold]Analysis:[/bold]")
            self.console.print(f"  Complexity: [{color}]{complexity:.3f} ({interpretation})[/{color}]")
            self.console.print(f"  Waves Completed: {wave_count}")
        else:
            self.console.print("[yellow]No analysis found[/yellow]")
            self.console.print(f"Waves Completed: {wave_count}")

        self.console.print()

    def update_wave_progress(self, progress: Dict[str, Any]) -> None:
        """
        Update wave execution progress.

        Args:
            progress: Progress indicator dict
        """
        if progress.get("type") == "progress":
            step = progress.get("step", "")
            if step:
                self.console.print(f"  [dim]{step}[/dim]")
        elif progress.get("type") == "tool":
            tool = progress.get("tool", "")
            if tool:
                self.console.print(f"  [cyan]→[/cyan] {tool}")

    def display_test_result(self, result: Dict[str, Any]) -> None:
        """
        Display test execution results.

        Args:
            result: Test result dict from MessageParser.extract_test_result()
        """
        total_tests = result.get("total_tests", 0)
        tests_passed = result.get("tests_passed", 0)
        tests_failed = result.get("tests_failed", 0)
        all_passed = result.get("all_passed", False)
        execution_time = result.get("execution_time", 0.0)
        coverage = result.get("coverage")
        no_mocks = result.get("no_mocks_confirmed", False)

        # Display header
        self.console.print()
        self.console.print("[bold cyan]Test Results[/bold cyan]")
        self.console.print()

        # Summary
        if all_passed:
            self.console.print(f"[green]✓ All tests passed ({tests_passed}/{total_tests})[/green]")
        else:
            self.console.print(f"[red]✗ {tests_failed} test(s) failed ({tests_passed}/{total_tests} passed)[/red]")

        self.console.print(f"[bold]Execution Time:[/bold] {execution_time:.1f} minutes")

        if coverage is not None:
            coverage_color = "green" if coverage >= 95 else "yellow" if coverage >= 80 else "red"
            self.console.print(f"[bold]Coverage:[/bold] [{coverage_color}]{coverage:.1f}%[/{coverage_color}]")

        # NO MOCKS confirmation
        if no_mocks:
            self.console.print("[green]✓ NO MOCKS enforcement confirmed[/green]")
        else:
            self.console.print("[yellow]⚠ Mock usage detected[/yellow]")

        # Test details
        test_details = result.get("test_details", [])
        if test_details:
            self.console.print("\n[bold]Test Details:[/bold]")
            for detail in test_details[:10]:  # Show first 10
                if "FAIL" in detail:
                    self.console.print(f"  [red]{detail}[/red]")
                else:
                    self.console.print(f"  [green]{detail}[/green]")
            if len(test_details) > 10:
                self.console.print(f"  [dim]... and {len(test_details) - 10} more[/dim]")

        self.console.print()

    # ============================================================================
    # PRIVATE HELPER METHODS
    # ============================================================================

    def _get_complexity_color(self, score: float) -> str:
        """Get Rich color based on complexity score."""
        if score < 0.40:
            return "green"
        elif score < 0.60:
            return "yellow"
        elif score < 0.75:
            return "orange1"
        else:
            return "red"

    def _format_tool_description(self, tool_block: Any) -> str:
        """Format tool use block into human-readable description."""
        if not hasattr(tool_block, "input"):
            return tool_block.name

        tool_input = tool_block.input

        # Handle common tool types
        if "path" in tool_input or "file_path" in tool_input:
            path = tool_input.get("path") or tool_input.get("file_path")
            return f"{tool_block.name} {path}"

        if "query" in tool_input:
            query = tool_input["query"]
            return f"{tool_block.name}: {query[:40]}"

        if "description" in tool_input:
            desc = tool_input["description"]
            return f"{tool_block.name}: {desc[:40]}"

        return tool_block.name


# Export
__all__ = ["ProgressUI"]
