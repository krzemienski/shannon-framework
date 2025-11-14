"""Live Metrics Dashboard for Shannon CLI V3.0

Two-layer real-time metrics display with keyboard control:

Layer 1 (Compact): 3-line progress summary
- Progress bar with percentage
- Cost, tokens, duration
- Keyboard hint

Layer 2 (Detailed): Full-screen streaming output
- Progress bar at top
- Streaming message buffer (scrollable)
- Completed stages
- Live metrics
- Keyboard controls

Keyboard Controls:
- Enter: Expand to Layer 2
- Esc: Collapse to Layer 1
- q: Request quit
- p: Request pause

Architecture:
    MetricsCollector → LiveDashboard.render() → Rich.Live → Terminal (4 Hz)

Design Decision (from SHANNON_CLI_V3_ARCHITECTURE.md):
    - 4 Hz refresh rate (smooth without CPU waste)
    - Non-blocking keyboard input (termios)
    - Streaming buffer (last 100 messages)
    - Graceful terminal resize handling
"""

from typing import Optional, Callable
from collections import deque
from datetime import datetime
import asyncio

from rich.console import Console, RenderableType
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.live import Live
from rich.text import Text
from rich.table import Table

from shannon.metrics.collector import MetricsCollector, MetricsSnapshot
from shannon.metrics.keyboard import KeyboardHandler, Key


class LiveDashboard:
    """
    Two-layer live metrics dashboard

    Displays real-time metrics from MetricsCollector with keyboard control.

    Usage:
        collector = MetricsCollector()
        dashboard = LiveDashboard(collector)

        # Run in context manager
        with dashboard:
            # Dashboard updates at 4 Hz automatically
            # Keyboard controls work
            await long_running_operation()

    Layer 1 (default):
        ┌─ Shannon: spec-analysis ──┐
        │ ▓▓▓▓▓▓░░░░ 60% (5/8 dims) │
        │ $0.12 | 8.2K | 45s        │
        │ Press ↵ for streaming     │
        └────────────────────────────┘

    Layer 2 (expanded):
        - Full screen layout
        - Progress bar at top
        - Streaming output (last 100 messages)
        - Completed stages list
        - Live metrics table
        - Keyboard controls

    Keyboard Events:
        - Enter: toggle_expand()
        - Esc: collapse()
        - q: request_quit()
        - p: request_pause()
    """

    def __init__(
        self,
        collector: MetricsCollector,
        console: Optional[Console] = None,
        refresh_per_second: int = 4,
        buffer_size: int = 100
    ):
        """
        Initialize live dashboard with message streaming

        Args:
            collector: MetricsCollector instance to read from
            console: Rich console (creates default if None)
            refresh_per_second: UI refresh rate (default: 4 Hz)
            buffer_size: Max streaming messages to buffer
        """
        self.collector = collector
        self.console = console or Console()
        self.refresh_per_second = refresh_per_second
        self.buffer_size = buffer_size

        # UI state
        self.expanded = False
        self.streaming_buffer: deque[str] = deque(maxlen=buffer_size)

        # Keyboard handler
        self.keyboard = KeyboardHandler()

        # Control flags (read by external code)
        self.quit_requested = False
        self.pause_requested = False

        # Rich components
        self._live: Optional[Live] = None
        self._progress: Optional[Progress] = None

        # Last known snapshot (for rendering)
        self._last_snapshot: Optional[MetricsSnapshot] = None

    def __enter__(self):
        """Start dashboard in context manager"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop dashboard in context manager"""
        self.stop()
        return False

    def start(self) -> None:
        """
        Start dashboard rendering

        Sets up:
        - Keyboard handler (non-blocking input)
        - Rich Live display (4 Hz refresh)
        - Progress bar
        """
        # Setup keyboard
        self.keyboard.setup_nonblocking()

        # Create Rich Live display
        self._live = Live(
            self.render(),
            console=self.console,
            refresh_per_second=self.refresh_per_second,
            transient=False  # Keep display after exit
        )

        # Start live rendering
        self._live.start()

    def stop(self) -> None:
        """
        Stop dashboard rendering

        Cleans up:
        - Rich Live display
        - Keyboard handler (restore terminal)
        """
        if self._live:
            self._live.stop()
            self._live = None

        # Restore terminal
        self.keyboard.restore_terminal()

    def update(self, streaming_message: Optional[str] = None) -> None:
        """
        Update dashboard state

        Called externally to:
        1. Add streaming messages to buffer
        2. Check for keyboard input
        3. Trigger re-render

        Args:
            streaming_message: New message to add to buffer (optional)
        """
        # Add to streaming buffer
        if streaming_message:
            self.streaming_buffer.append(streaming_message)

        # Get latest metrics
        self._last_snapshot = self.collector.get_snapshot()

        # Check for keyboard input
        self._handle_keyboard()

        # Update live display
        if self._live:
            self._live.update(self.render())

    def render(self) -> RenderableType:
        """
        Render appropriate view based on state

        Returns:
            Panel (compact) or Layout (detailed)
        """
        # Get current snapshot
        snapshot = self._last_snapshot or self.collector.get_snapshot()

        if self.expanded:
            return self._create_detailed_layout(snapshot)
        else:
            return self._create_compact_layout(snapshot)

    def _create_compact_layout(self, snapshot: MetricsSnapshot) -> Panel:
        """
        Create compact 3-line view

        Args:
            snapshot: Current metrics

        Returns:
            Panel with compact display
        """
        # Progress bar
        progress_chars = 10
        filled = int(snapshot.progress * progress_chars)
        bar = '▓' * filled + '░' * (progress_chars - filled)

        # Format metrics
        cost_str = f"${snapshot.cost_total:.2f}"
        tokens_str = f"{snapshot.tokens_total / 1000:.1f}K"
        duration_str = f"{snapshot.duration_seconds:.0f}s"

        # Stage info
        stage_info = ""
        if snapshot.total_stages > 0:
            completed = len(snapshot.completed_stages)
            stage_info = f" ({completed}/{snapshot.total_stages} dims)"

        # Build content
        content = (
            f"{bar} {snapshot.progress:.0%}{stage_info}\n"
            f"{cost_str} | {tokens_str} | {duration_str}\n"
            f"Press ↵ for streaming"
        )

        # Determine border style based on status
        border_style = "cyan"
        if snapshot.has_error:
            border_style = "red"
        elif snapshot.is_complete:
            border_style = "green"

        return Panel(
            content,
            title=f"Shannon: {snapshot.current_operation}",
            border_style=border_style
        )

    def _create_detailed_layout(self, snapshot: MetricsSnapshot) -> Layout:
        """
        Create detailed full-screen layout

        Args:
            snapshot: Current metrics

        Returns:
            Layout with detailed display
        """
        layout = Layout()

        # Split into sections
        layout.split_column(
            Layout(name="progress", size=3),
            Layout(name="streaming", ratio=1),  # Takes most space
            Layout(name="stages", size=5),
            Layout(name="metrics", size=5),
            Layout(name="controls", size=1)
        )

        # Populate sections
        layout["progress"].update(self._render_progress(snapshot))
        layout["streaming"].update(self._render_streaming())
        layout["stages"].update(self._render_stages(snapshot))
        layout["metrics"].update(self._render_metrics(snapshot))
        layout["controls"].update(self._render_controls())

        return layout

    def _render_progress(self, snapshot: MetricsSnapshot) -> Panel:
        """
        Render progress bar panel

        Args:
            snapshot: Current metrics

        Returns:
            Panel with progress bar
        """
        # Create progress bar
        progress = Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )

        task = progress.add_task(
            snapshot.current_stage,
            total=100,
            completed=snapshot.progress * 100
        )

        return Panel(progress, border_style="cyan")

    def _render_streaming(self) -> Panel:
        """
        Render streaming output buffer

        Returns:
            Panel with buffered messages
        """
        # Get last N messages
        messages = list(self.streaming_buffer)[-20:]  # Show last 20 lines

        if not messages:
            content = Text("Waiting for output...", style="dim")
        else:
            # Join messages with newlines
            content = Text("\n".join(messages))

        return Panel(
            content,
            title="Streaming Output",
            border_style="blue"
        )

    def _render_stages(self, snapshot: MetricsSnapshot) -> Panel:
        """
        Render completed stages

        Args:
            snapshot: Current metrics

        Returns:
            Panel with stage list
        """
        if not snapshot.completed_stages:
            content = Text("No stages completed yet", style="dim")
        else:
            # Create bullet list
            lines = []
            for stage in snapshot.completed_stages:
                lines.append(f"✓ {stage}")

            content = Text("\n".join(lines), style="green")

        return Panel(
            content,
            title=f"Completed Stages ({len(snapshot.completed_stages)}/{snapshot.total_stages})",
            border_style="green"
        )

    def _render_metrics(self, snapshot: MetricsSnapshot) -> Panel:
        """
        Render live metrics table

        Args:
            snapshot: Current metrics

        Returns:
            Panel with metrics table
        """
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan", justify="right")
        table.add_column(style="white")

        # Cost
        table.add_row("Cost:", f"${snapshot.cost_total:.4f}")
        table.add_row("  Input:", f"${snapshot.cost_input:.4f}")
        table.add_row("  Output:", f"${snapshot.cost_output:.4f}")

        table.add_row("", "")  # Spacer

        # Tokens
        table.add_row("Tokens:", f"{snapshot.tokens_total:,}")
        table.add_row("  Input:", f"{snapshot.tokens_input:,}")
        table.add_row("  Output:", f"{snapshot.tokens_output:,}")

        table.add_row("", "")  # Spacer

        # Timing
        table.add_row("Duration:", f"{snapshot.duration_seconds:.1f}s")

        table.add_row("", "")  # Spacer

        # Messages
        table.add_row("Messages:", f"{snapshot.message_count}")
        if snapshot.error_count > 0:
            table.add_row("Errors:", f"{snapshot.error_count}", style="red")

        return Panel(table, title="Metrics", border_style="yellow")

    def _render_controls(self) -> Panel:
        """
        Render keyboard controls

        Returns:
            Panel with control hints
        """
        controls = "[Esc] Collapse | [q] Quit | [p] Pause"
        return Panel(controls, border_style="dim")

    def _handle_keyboard(self) -> None:
        """
        Handle keyboard input (non-blocking)

        Checks for key presses and updates state accordingly.
        """
        key = self.keyboard.read_key(timeout=0.0)

        if key is None:
            return

        if key == Key.ENTER:
            self.expanded = True

        elif key == Key.ESC:
            self.expanded = False

        elif key == Key.Q:
            self.quit_requested = True

        elif key == Key.P:
            self.pause_requested = not self.pause_requested

    def toggle_expand(self) -> None:
        """Toggle between compact and detailed views"""
        self.expanded = not self.expanded

    def collapse(self) -> None:
        """Force collapse to compact view"""
        self.expanded = False

    def expand(self) -> None:
        """Force expand to detailed view"""
        self.expanded = True


# Async helper for integration with async workflows

async def run_with_dashboard(
    collector: MetricsCollector,
    operation: Callable,
    console: Optional[Console] = None
) -> None:
    """
    Run async operation with live dashboard

    Convenience wrapper for running operations with dashboard.

    Args:
        collector: MetricsCollector instance
        operation: Async callable to run
        console: Optional Rich console

    Example:
        collector = MetricsCollector()

        async def my_operation():
            # Do work
            pass

        await run_with_dashboard(collector, my_operation)
    """
    dashboard = LiveDashboard(collector, console=console)

    try:
        dashboard.start()

        # Run operation with periodic dashboard updates
        operation_task = asyncio.create_task(operation())
        update_task = asyncio.create_task(_update_loop(dashboard))

        # Wait for operation to complete
        await operation_task

        # Stop update loop
        update_task.cancel()
        try:
            await update_task
        except asyncio.CancelledError:
            pass

    finally:
        dashboard.stop()


async def _update_loop(dashboard: LiveDashboard) -> None:
    """
    Periodic dashboard update loop

    Args:
        dashboard: Dashboard to update
    """
    while True:
        dashboard.update()
        await asyncio.sleep(0.25)  # 4 Hz
