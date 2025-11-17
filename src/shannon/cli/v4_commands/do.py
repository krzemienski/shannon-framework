"""Shannon CLI - shannon do command (V5 Integrated)

V5 version that uses UnifiedOrchestrator for proper V3+V4 integration.
This ensures shannon do gets all V3 features: cache, analytics, context, cost optimization.

Example:
    shannon do "create authentication system with JWT"
    shannon do "fix the login bug" --dashboard
    shannon do "add tests for user API" --auto
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime
import uuid

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from shannon.config import ShannonConfig
from shannon.unified_orchestrator import UnifiedOrchestrator
from shannon.orchestration.multi_file_parser import MultiFileParser
from shannon.executor.multi_file_executor import MultiFileExecutor

logger = logging.getLogger(__name__)


@click.command(name='do')
@click.argument('task')
@click.option('--dashboard', '-d', is_flag=True, help='Enable real-time dashboard')
@click.option('--auto', is_flag=True, help='Auto-mode: use defaults for decisions')
@click.option('--project-root', type=click.Path(exists=True), default='.',
              help='Project root directory')
@click.option('--session-id', help='Session ID for dashboard (auto-generated if not provided)')
@click.option('--dry-run', is_flag=True, help='Plan only, do not execute')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def do_command(
    task: str,
    dashboard: bool,
    auto: bool,
    project_root: str,
    session_id: Optional[str],
    dry_run: bool,
    verbose: bool
):
    """Execute natural language task with V5 unified orchestration.

    shannon do uses UnifiedOrchestrator to combine V3 intelligence
    (cache, analytics, context, cost) with V4 execution (skills, agents, dashboard).

    \b
    Workflow:
        1. Task Parsing: Extract intent from natural language
        2. Planning: Create execution plan with dependencies
        3. Execution: Run skills via UnifiedOrchestrator
        4. Monitoring: Real-time dashboard streaming
        5. V3 Features: Automatic cache, analytics, cost optimization

    \b
    Examples:
        shannon do "create authentication system"
        shannon do "fix login bug" --dashboard
        shannon do "add tests" --auto
        shannon do "refactor user module" --dry-run

    \b
    V5 Features:
        - UnifiedOrchestrator (V3+V4 integrated)
        - Intelligent caching (from V3)
        - Cost optimization (from V3)
        - Analytics recording (from V3)
        - Multi-agent execution (from V4)
        - Real-time dashboard (from V4)
    """
    async def run_do():
        """Execute do command asynchronously via UnifiedOrchestrator"""
        console = Console()
        config = ShannonConfig()
        project_path = Path(project_root).resolve()

        # Generate session ID if not provided
        if not session_id:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = uuid.uuid4().hex[:8]
            generated_session_id = f"do_{timestamp}_{unique_id}"
        else:
            generated_session_id = session_id

        console.print()
        console.print(Panel.fit(
            "[bold cyan]Shannon V5 Unified Orchestration[/bold cyan]\n\n"
            f"Task: {task}\n"
            f"Project: {project_path}\n"
            f"Session: {generated_session_id}",
            border_style="cyan"
        ))
        console.print()

        if dashboard:
            console.print(f"[dim]Dashboard: http://localhost:5173 (session: {generated_session_id})[/dim]\n")

        try:
            # V5: Initialize UnifiedOrchestrator (gets V3+V4 features)
            console.print("[dim]Initializing UnifiedOrchestrator (V3+V4 integrated)...[/dim]")
            orchestrator = UnifiedOrchestrator(config)

            # Verify V3 features available
            if verbose:
                status = orchestrator.get_status()
                v3_count = sum(status['v3_components'].values())
                v4_count = sum(status['v4_components'].values())
                shared_count = sum(status['shared_subsystems'].values())
                console.print(f"[dim]  V3 components: {v3_count}/4[/dim]")
                console.print(f"[dim]  V4 components: {v4_count}/5[/dim]")
                console.print(f"[dim]  Shared subsystems: {shared_count}/6[/dim]")

            console.print()

            # Check for multi-file request FIRST
            multi_file_parser = MultiFileParser()
            if multi_file_parser.is_multi_file(task):
                console.print("  [yellow]⚡[/yellow] Multi-file request detected")
                multi_file_request = multi_file_parser.parse(task)

                if multi_file_request:
                    console.print(f"  [green]✓[/green] Directory: {multi_file_request.directory}")
                    console.print(f"  [green]✓[/green] Files: {len(multi_file_request.files)}")
                    for file_name in multi_file_request.files:
                        console.print(f"    [dim]- {file_name}[/dim]")
                    console.print()

                    # Execute multi-file creation
                    console.print("[bold cyan]Executing multi-file creation...[/bold cyan]")
                    multi_file_executor = MultiFileExecutor(project_root=project_path)

                    result = await multi_file_executor.execute(
                        directory=multi_file_request.directory,
                        files=multi_file_request.files,
                        base_task=multi_file_request.base_task
                    )

                    console.print()

                    # Display results
                    if result.success:
                        console.print(Panel.fit(
                            f"[bold green]✓ Multi-File Creation Complete[/bold green]\n\n"
                            f"Directory: {result.directory}\n"
                            f"Files created: {len(result.files_created)}/{result.total_files}\n"
                            f"Duration: {result.duration_seconds:.1f}s\n\n"
                            f"Files:\n" + "\n".join(f"  ✓ {f}" for f in result.files_created),
                            border_style="green"
                        ))
                        console.print()
                        return
                    else:
                        console.print(Panel.fit(
                            f"[bold red]✗ Multi-File Creation Failed[/bold red]\n\n"
                            f"Files created: {len(result.files_created)}/{result.total_files}\n"
                            f"Errors: {len(result.errors)}\n\n"
                            f"Details:\n" + "\n".join(f"  ✗ {e}" for e in result.errors),
                            border_style="red"
                        ))
                        console.print()
                        sys.exit(1)

            # Create dashboard client if dashboard enabled
            dashboard_client = None
            if dashboard:
                console.print("[dim]Connecting to dashboard...[/dim]")
                from shannon.communication.dashboard_client import DashboardEventClient
                dashboard_url = 'http://localhost:8000'
                dashboard_client = DashboardEventClient(dashboard_url, generated_session_id)

                connected = await dashboard_client.connect()
                if connected:
                    console.print("[dim]✓ Dashboard connected[/dim]\n")
                else:
                    console.print("[yellow]⚠ Dashboard connection failed - continuing without real-time updates[/yellow]\n")
                    dashboard_client = None

            # STEP 1: Execute via UnifiedOrchestrator
            # This automatically gets V3 features (cache, analytics, cost) + V4 features (skills, agents)
            console.print("[bold cyan]Executing task via UnifiedOrchestrator...[/bold cyan]")
            console.print()

            # Show what's happening
            if verbose:
                console.print("[dim]V3 Features Active:[/dim]")
                console.print("[dim]  - Cache: Check before, save after[/dim]")
                console.print("[dim]  - Analytics: Record session to database[/dim]")
                console.print("[dim]  - Cost: Optimize model selection[/dim]")
                console.print("[dim]  - Context: Load project context if available[/dim]")
                console.print("[dim]V4 Features Active:[/dim]")
                console.print("[dim]  - Skills: Auto-discovery and execution[/dim]")
                console.print("[dim]  - Agents: Spawn for each skill (AgentPool)[/dim]")
                console.print("[dim]  - Checkpoints: Create for rollback[/dim]")
                console.print("[dim]  - Dashboard: Real-time event streaming[/dim]")
                console.print()

            # Execute via UnifiedOrchestrator
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                exec_task = progress.add_task("Executing task...", total=None)

                # V5: Unified execution with both V3 and V4 features
                result = await orchestrator.execute_skills(
                    task=task,
                    dashboard_client=dashboard_client,
                    session_id=generated_session_id
                )

                progress.update(exec_task, completed=True)

            console.print()

            # STEP 2: Display results
            success = result.get('success', False)

            if success:
                console.print(Panel.fit(
                    "[bold green]✓ Execution Complete[/bold green]\n\n"
                    f"Steps: {result.get('steps_completed', 0)}/{result.get('steps_total', 0)}\n"
                    f"Checkpoints: {len(result.get('checkpoints_created', []))}\n"
                    f"Duration: {result.get('duration_seconds', 0):.1f}s",
                    border_style="green"
                ))
            else:
                console.print(Panel.fit(
                    "[bold red]✗ Execution Failed[/bold red]\n\n"
                    f"Steps completed: {result.get('steps_completed', 0)}/{result.get('steps_total', 0)}\n"
                    f"Error: {result.get('error', 'Unknown')}\n"
                    f"Duration: {result.get('duration_seconds', 0):.1f}s",
                    border_style="red"
                ))

            console.print()

            # Show checkpoints
            checkpoints = result.get('checkpoints_created', [])
            if checkpoints:
                console.print("[dim]Checkpoints created:[/dim]")
                for cp_id in checkpoints:
                    console.print(f"  [dim]- {cp_id}[/dim]")
                console.print()

            # Show V3 feature usage
            if verbose and orchestrator.cache:
                console.print("[dim]V3 Features Used:[/dim]")
                # TODO: Get cache stats, analytics session ID, cost saved
                console.print()

            # Exit with appropriate code
            sys.exit(0 if success else 1)

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user[/yellow]\n")
            sys.exit(130)

        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]\n")
            if verbose:
                import traceback
                console.print("[dim]" + traceback.format_exc() + "[/dim]")
            sys.exit(1)

    # Run async workflow
    import anyio
    anyio.run(run_do)


# Register command
def register(cli_group):
    """Register V5 do command with CLI group"""
    cli_group.add_command(do_command)
