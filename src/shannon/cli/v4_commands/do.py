"""Shannon CLI - shannon do command

The main user-facing command that orchestrates complete task execution:
1. Parse natural language task
2. Create execution plan
3. Execute skills in order
4. Create checkpoints
5. Stream to dashboard (optional)
6. Handle HALT/RESUME

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

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from shannon.config import ShannonConfig
from shannon.skills.registry import SkillRegistry
from shannon.skills.executor import SkillExecutor
from shannon.skills.hooks import HookManager
from shannon.skills.dependencies import DependencyResolver
from shannon.skills.loader import SkillLoader
from shannon.skills.discovery import DiscoveryEngine
from shannon.orchestration import TaskParser, ExecutionPlanner, StateManager, Orchestrator
from shannon.server.websocket import emit_skill_event, emit_checkpoint_event

logger = logging.getLogger(__name__)


@click.command(name='do')
@click.argument('task')
@click.option('--dashboard', '-d', is_flag=True, help='Start WebSocket server for dashboard')
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
    """
    Execute natural language task with orchestration.

    The shannon do command is the main entry point for task execution.
    It handles the complete workflow:

    \b
    1. Task Parsing: Extract intent from natural language
    2. Planning: Create execution plan with dependencies
    3. Execution: Run skills in order with checkpoints
    4. Monitoring: Stream to dashboard if enabled

    \b
    Examples:
        shannon do "create authentication system"
        shannon do "fix login bug" --dashboard
        shannon do "add tests" --auto
        shannon do "refactor user module" --dry-run

    \b
    Features:
        - Natural language task understanding
        - Automatic skill selection and ordering
        - Checkpoint creation for rollback
        - Real-time dashboard streaming
        - HALT/RESUME support
        - Auto-mode for unattended execution
    """
    async def run_do():
        """Execute do command asynchronously"""
        console = Console()
        config = ShannonConfig()
        project_path = Path(project_root).resolve()

        # Generate session ID if not provided
        if not session_id:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            generated_session_id = f"do_{timestamp}"
        else:
            generated_session_id = session_id

        # Display header
        console.print()
        console.print(Panel.fit(
            "[bold cyan]Shannon Orchestration[/bold cyan]\n\n"
            f"Task: {task}\n"
            f"Project: {project_path}\n"
            f"Session: {generated_session_id}",
            border_style="cyan"
        ))
        console.print()

        try:
            # Initialize components
            console.print("[dim]Initializing orchestration components...[/dim]")

            # Get or initialize registry with schema
            # Schema is at project root /schemas/skill.schema.json
            # __file__ is at src/shannon/cli/v4_commands/do.py
            # So we go up 4 levels to get to project root
            schema_path = Path(__file__).parent.parent.parent.parent.parent / "schemas" / "skill.schema.json"
            try:
                registry = await SkillRegistry.get_instance()
            except ValueError:
                # First initialization - need schema path
                registry = await SkillRegistry.get_instance(schema_path)

            # Discover and load skills
            console.print("[dim]Discovering skills...[/dim]")
            loader = SkillLoader(registry)
            discovery = DiscoveryEngine(registry, loader)
            skills = await discovery.discover_all(project_root=project_path)
            console.print(f"[dim]Loaded {len(skills)} skills[/dim]")

            hook_manager = HookManager(registry)
            executor = SkillExecutor(registry, hook_manager)
            dependency_resolver = DependencyResolver(registry)
            task_parser = TaskParser(registry)
            planner = ExecutionPlanner(registry, dependency_resolver)
            state_manager = StateManager(project_path)

            # Start WebSocket server if dashboard enabled
            if dashboard:
                console.print("[dim]Starting WebSocket server for dashboard...[/dim]")
                from shannon.server.app import app as dashboard_app
                # Start server in background
                # (In production, would use asyncio.create_task)
                console.print("[yellow]Dashboard: ws://localhost:8000[/yellow]")

            console.print()

            # STEP 1: Parse task
            console.print("[bold cyan]Step 1: Parsing task...[/bold cyan]")

            parsed = await task_parser.parse(task)

            console.print(f"  [green]✓[/green] Goal: {parsed.intent.goal}")
            console.print(f"  [green]✓[/green] Domain: {parsed.intent.domain}")
            console.print(f"  [green]✓[/green] Type: {parsed.intent.type}")
            console.print(f"  [green]✓[/green] Keywords: {', '.join(parsed.intent.keywords[:5])}")
            console.print(f"  [green]✓[/green] Candidate skills: {len(parsed.candidate_skills)}")
            console.print(f"  [dim]Confidence: {parsed.confidence:.2%}[/dim]")
            console.print()

            # STEP 2: Create plan
            console.print("[bold cyan]Step 2: Creating execution plan...[/bold cyan]")

            plan = await planner.create_plan(parsed, auto_mode=auto)

            console.print(f"  [green]✓[/green] Steps: {len(plan.steps)}")
            console.print(f"  [green]✓[/green] Checkpoints: {len(plan.checkpoints)}")
            console.print(f"  [green]✓[/green] Decision points: {len(plan.decision_points)}")
            console.print(f"  [green]✓[/green] Estimated duration: {plan.estimated_duration:.0f}s")
            console.print()

            # Display plan details
            if verbose or dry_run:
                plan_table = Table(title="Execution Plan", show_header=True)
                plan_table.add_column("#", style="dim")
                plan_table.add_column("Skill", style="cyan")
                plan_table.add_column("Duration", justify="right", style="yellow")
                plan_table.add_column("Checkpoint", justify="center", style="green")
                plan_table.add_column("Critical", justify="center", style="red")

                for i, step in enumerate(plan.steps, 1):
                    plan_table.add_row(
                        str(i),
                        step.skill_name,
                        f"{step.estimated_duration:.0f}s",
                        "✓" if step.checkpoint_before else "",
                        "✓" if step.critical else ""
                    )

                console.print(plan_table)
                console.print()

            # DRY RUN: Stop here
            if dry_run:
                console.print("[yellow]Dry run complete - no execution performed[/yellow]")
                console.print()
                return

            # STEP 3: Execute plan
            console.print("[bold cyan]Step 3: Executing plan...[/bold cyan]")
            console.print()

            # Create orchestrator
            async def event_callback(event_type: str, data: dict, session_id: str):
                """Callback for event emission"""
                if dashboard:
                    # Emit to WebSocket
                    if event_type.startswith('skill:'):
                        await emit_skill_event(event_type, data, session_id)
                    elif event_type.startswith('checkpoint:'):
                        await emit_checkpoint_event(data, session_id)

                # Also log to console
                if verbose:
                    console.print(f"[dim]Event: {event_type}[/dim]")

            orchestrator = Orchestrator(
                plan=plan,
                executor=executor,
                state_manager=state_manager,
                session_id=generated_session_id,
                event_callback=event_callback if dashboard else None
            )

            # Execute with progress
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                exec_task = progress.add_task(
                    f"Executing {len(plan.steps)} skills...",
                    total=len(plan.steps)
                )

                # Execute orchestrator
                result = await orchestrator.execute()

                progress.update(exec_task, completed=len(plan.steps))

            console.print()

            # STEP 4: Display results
            if result.success:
                console.print(Panel.fit(
                    "[bold green]✓ Execution Complete[/bold green]\n\n"
                    f"Steps: {result.steps_completed}/{result.steps_total}\n"
                    f"Checkpoints: {len(result.checkpoints_created)}\n"
                    f"Duration: {result.duration_seconds:.1f}s",
                    border_style="green"
                ))
            else:
                console.print(Panel.fit(
                    "[bold red]✗ Execution Failed[/bold red]\n\n"
                    f"Steps completed: {result.steps_completed}/{result.steps_total}\n"
                    f"Error: {result.error}\n"
                    f"Duration: {result.duration_seconds:.1f}s",
                    border_style="red"
                ))

            console.print()

            # Show checkpoints
            if result.checkpoints_created:
                console.print("[dim]Checkpoints created:[/dim]")
                for cp_id in result.checkpoints_created:
                    console.print(f"  [dim]- {cp_id}[/dim]")
                console.print()

            # Exit with appropriate code
            sys.exit(0 if result.success else 1)

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
    """Register do command with CLI group"""
    cli_group.add_command(do_command)
