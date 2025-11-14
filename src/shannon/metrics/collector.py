"""Metrics Collector for Shannon CLI V3.0

Implements MessageCollector interface to extract metrics from SDK messages:
- Cost tracking (input/output tokens, pricing)
- Token usage (input/output/total)
- Duration tracking (start/end time, elapsed)
- Progress tracking (percentage, current stage)
- Stage tracking (analysis phases, dimensions completed)

Architecture:
    SDK messages → MetricsCollector.process() → Internal state → Dashboard reads

Design Decision (from SHANNON_CLI_V3_ARCHITECTURE.md):
    - Zero-latency: process() returns immediately, updates state asynchronously
    - Thread-safe: Uses asyncio locks for state updates
    - Error isolation: Never raises exceptions (logs errors internally)
"""

from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List
from datetime import datetime
import asyncio
import logging

from shannon.sdk.interceptor import MessageCollector


@dataclass
class MetricsSnapshot:
    """
    Immutable snapshot of OPERATIONAL STATE and metrics

    Used for thread-safe reads by dashboard.
    Shows WHAT is running, WHERE we are, WHAT we're waiting for.
    """
    # Cost tracking
    cost_input: float = 0.0
    cost_output: float = 0.0
    cost_total: float = 0.0

    # Token tracking
    tokens_input: int = 0
    tokens_output: int = 0
    tokens_total: int = 0

    # Timing
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0

    # Progress
    progress: float = 0.0  # 0.0 to 1.0
    current_stage: str = "Initializing"
    current_operation: str = ""

    # Stage details
    completed_stages: List[str] = field(default_factory=list)
    total_stages: int = 0

    # Message stats
    message_count: int = 0
    error_count: int = 0

    # Status
    is_complete: bool = False
    has_error: bool = False
    error_message: Optional[str] = None

    # OPERATIONAL STATE (NEW for V3 telemetry)
    waiting_for: Optional[str] = None  # "Claude API (Sequential tool)" or None
    last_activity_time: Optional[datetime] = None  # Detect stalls
    last_activity: Optional[str] = None  # "Completed Cognitive dimension"
    current_tool: Optional[str] = None  # "Sequential" or "Read" or None
    agent_status: str = "ACTIVE"  # "ACTIVE" | "WAITING" | "BLOCKED" | "COMPLETE"


class MetricsCollector(MessageCollector):
    """
    Collects metrics from SDK message stream

    Implements MessageCollector interface for transparent integration
    with MessageInterceptor from Wave 1.

    Usage:
        collector = MetricsCollector()
        interceptor = MessageInterceptor()

        async for msg in interceptor.intercept(query_iter, [collector]):
            # Collector updates metrics in background
            snapshot = collector.get_snapshot()
            print(f"Progress: {snapshot.progress:.0%}")

    Thread Safety:
        - All public methods are async and use locks
        - get_snapshot() returns immutable copy
        - Safe for concurrent dashboard reads
    """

    def __init__(
        self,
        operation_name: str = "shannon-operation",
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize metrics collector

        Args:
            operation_name: Name of operation being tracked
            logger: Optional logger for debugging
        """
        self.operation_name = operation_name
        self.logger = logger or self._default_logger()

        # Internal state (protected by lock)
        self._lock = asyncio.Lock()
        self._metrics = MetricsSnapshot(
            current_operation=operation_name,
            start_time=datetime.now()
        )

        # Message parsing state
        self._message_buffer: List[str] = []
        self._last_progress_update: Optional[datetime] = None

    async def process(self, message: Any) -> None:
        """
        Process SDK message and extract metrics

        Called by MessageInterceptor for each SDK message.
        Must not raise exceptions (error isolation requirement).

        Args:
            message: SDK message object (type varies by SDK version)
        """
        try:
            async with self._lock:
                self._metrics.message_count += 1

                # Extract metrics based on message type
                await self._extract_from_message(message)

        except Exception as e:
            # Error isolation: log but don't propagate
            self.logger.error(f"Error processing message: {e}", exc_info=True)
            async with self._lock:
                self._metrics.error_count += 1

    async def on_stream_complete(self) -> None:
        """
        Called when message stream completes successfully

        Finalizes metrics (end time, final progress, etc.)
        """
        try:
            async with self._lock:
                self._metrics.end_time = datetime.now()
                self._metrics.is_complete = True
                self._metrics.progress = 1.0

                if self._metrics.start_time:
                    elapsed = (self._metrics.end_time - self._metrics.start_time).total_seconds()
                    self._metrics.duration_seconds = elapsed

                self.logger.info(
                    f"Stream complete: {self._metrics.message_count} messages, "
                    f"${self._metrics.cost_total:.4f}, "
                    f"{self._metrics.duration_seconds:.1f}s"
                )

        except Exception as e:
            self.logger.error(f"Error in on_stream_complete: {e}", exc_info=True)

    async def on_stream_error(self, error: Exception) -> None:
        """
        Called when message stream errors

        Args:
            error: Exception that occurred
        """
        try:
            async with self._lock:
                self._metrics.end_time = datetime.now()
                self._metrics.has_error = True
                self._metrics.error_message = str(error)

                if self._metrics.start_time:
                    elapsed = (self._metrics.end_time - self._metrics.start_time).total_seconds()
                    self._metrics.duration_seconds = elapsed

                self.logger.error(
                    f"Stream error after {self._metrics.message_count} messages: {error}"
                )

        except Exception as e:
            self.logger.error(f"Error in on_stream_error: {e}", exc_info=True)

    def get_snapshot(self) -> MetricsSnapshot:
        """
        Get immutable snapshot of OPERATIONAL STATE and metrics

        Thread-safe: Returns copy of internal state without locking.
        Dashboard can call this at any time without blocking.

        Returns:
            MetricsSnapshot with current operational state and metrics
        """
        # Calculate wait duration if waiting
        waiting_duration = None
        if self._tool_start_time:
            waiting_duration = (datetime.now() - self._tool_start_time).total_seconds()

        # Return copy with all operational state
        return MetricsSnapshot(
            cost_input=self._metrics.cost_input,
            cost_output=self._metrics.cost_output,
            cost_total=self._metrics.cost_total,
            tokens_input=self._metrics.tokens_input,
            tokens_output=self._metrics.tokens_output,
            tokens_total=self._metrics.tokens_total,
            start_time=self._metrics.start_time,
            end_time=self._metrics.end_time,
            duration_seconds=self._metrics.duration_seconds,
            progress=self._metrics.progress,
            current_stage=self._metrics.current_stage,
            current_operation=self._metrics.current_operation,
            completed_stages=self._metrics.completed_stages.copy(),
            total_stages=self._metrics.total_stages,
            message_count=self._metrics.message_count,
            error_count=self._metrics.error_count,
            is_complete=self._metrics.is_complete,
            has_error=self._metrics.has_error,
            error_message=self._metrics.error_message,
            # OPERATIONAL STATE
            waiting_for=self._metrics.waiting_for,
            last_activity_time=self._metrics.last_activity_time,
            last_activity=self._metrics.last_activity,
            current_tool=self._metrics.current_tool,
            agent_status=self._metrics.agent_status
        )

    async def _extract_from_message(self, message: Any) -> None:
        """
        Extract OPERATIONAL STATE from SDK message

        Extracts:
        - Current operation/stage from text
        - Tool calls in progress
        - Completed stages/dimensions
        - Progress percentage
        - Cost/tokens from usage blocks

        Args:
            message: SDK message to parse
        """
        # Get message type
        msg_type = type(message).__name__

        # Extract text content for operational state parsing
        text_content = None
        if hasattr(message, 'text'):
            text_content = message.text
        elif hasattr(message, 'content') and isinstance(message.content, str):
            text_content = message.content

        # Parse operational state from text
        if text_content:
            # Detect current step/stage
            if "## Step" in text_content or "### " in text_content:
                # Extract stage name
                lines = text_content.split('\n')
                for line in lines:
                    if line.startswith("## Step") or line.startswith("###"):
                        stage = line.replace("##", "").replace("###", "").strip()
                        self._metrics.current_stage = stage[:50]  # Truncate
                        break

            # Detect dimension completion (for spec analysis)
            import re
            score_pattern = r'Score:\s*\*\*(\d+\.\d+)\*\*'
            dimension_pattern = r'\*\*(\w+)\s+Complexity'

            if re.search(score_pattern, text_content):
                # Found a completed dimension
                dim_match = re.search(dimension_pattern, text_content)
                score_match = re.search(score_pattern, text_content)

                if dim_match and score_match:
                    dim_name = dim_match.group(1)
                    score = float(score_match.group(1))

                    # Add to completed stages
                    stage_entry = f"{dim_name} ({score:.2f})"
                    if stage_entry not in self._metrics.completed_stages:
                        self._metrics.completed_stages.append(stage_entry)

                        # Update progress if this is 8D analysis (8 dimensions)
                        if self._metrics.total_stages == 0:
                            self._metrics.total_stages = 8  # Spec analysis has 8 dimensions

                        completed_count = len(self._metrics.completed_stages)
                        self._metrics.progress = completed_count / self._metrics.total_stages

            # Detect current activity
            activity_keywords = {
                "Analyzing": "analyzing",
                "Calculating": "calculating",
                "Processing": "processing",
                "Generating": "generating",
                "Computing": "computing"
            }

            for keyword, state in activity_keywords.items():
                if keyword in text_content:
                    # Extract what's being analyzed
                    if "complexity" in text_content.lower():
                        for dim in ["Structural", "Cognitive", "Coordination", "Temporal", "Technical", "Scale", "Uncertainty", "Dependencies"]:
                            if dim in text_content:
                                self._metrics.current_stage = f"{state.title()} {dim} Complexity"
                                self._metrics.agent_status = "ACTIVE"
                                self._metrics.last_activity = f"{state.title()} {dim}"
                                self._metrics.last_activity_time = datetime.now()
                                break

        # Detect tool calls (WAITING state)
        if hasattr(message, 'name'):  # ToolUseBlock
            tool_name = message.name
            self._metrics.current_tool = tool_name
            self._metrics.waiting_for = f"API call ({tool_name} tool)"
            self._metrics.agent_status = "WAITING"
            self._tool_start_time = datetime.now()
            self._current_tool_name = tool_name

            # Log activity
            self._metrics.last_activity = f"Tool: {tool_name}"
            self._metrics.last_activity_time = datetime.now()

        # Detect tool completion (results returned)
        if hasattr(message, 'is_error'):  # ToolResultBlock
            if self._current_tool_name:
                self._metrics.last_activity = f"✓ {self._current_tool_name} complete"
                self._metrics.last_activity_time = datetime.now()

            # Clear waiting state
            self._metrics.waiting_for = None
            self._metrics.current_tool = None
            self._metrics.agent_status = "ACTIVE"
            self._tool_start_time = None
            self._current_tool_name = None

        # Try to extract usage info (tokens, cost)
        if hasattr(message, 'usage'):
            await self._extract_usage(message.usage)

        # Try to extract content (for progress parsing)
        if hasattr(message, 'content'):
            await self._extract_content(message.content)

        # Try to extract delta (streaming updates)
        if hasattr(message, 'delta'):
            await self._extract_delta(message.delta)

        # Update timing
        if self._metrics.start_time:
            elapsed = (datetime.now() - self._metrics.start_time).total_seconds()
            self._metrics.duration_seconds = elapsed

    async def _extract_usage(self, usage: Any) -> None:
        """
        Extract token and cost information from usage block

        Args:
            usage: Usage object from SDK message
        """
        # Extract token counts
        if hasattr(usage, 'input_tokens'):
            self._metrics.tokens_input = usage.input_tokens

        if hasattr(usage, 'output_tokens'):
            self._metrics.tokens_output = usage.output_tokens

        self._metrics.tokens_total = self._metrics.tokens_input + self._metrics.tokens_output

        # Calculate costs (using Sonnet 4.5 pricing)
        # Input: $3 per million tokens
        # Output: $15 per million tokens
        self._metrics.cost_input = (self._metrics.tokens_input / 1_000_000) * 3.0
        self._metrics.cost_output = (self._metrics.tokens_output / 1_000_000) * 15.0
        self._metrics.cost_total = self._metrics.cost_input + self._metrics.cost_output

    async def _extract_content(self, content: Any) -> None:
        """
        Extract progress information from content blocks

        Args:
            content: Content from SDK message
        """
        # Handle list of content blocks
        if isinstance(content, list):
            for block in content:
                await self._extract_content_block(block)
        else:
            await self._extract_content_block(content)

    async def _extract_content_block(self, block: Any) -> None:
        """
        Extract metrics from single content block

        Args:
            block: Content block to parse
        """
        # Try to get text content
        text = None
        if hasattr(block, 'text'):
            text = block.text
        elif hasattr(block, 'content') and isinstance(block.content, str):
            text = block.content

        if text:
            self._message_buffer.append(text)

            # Parse for progress indicators
            # Look for patterns like "Progress: 60%" or "Completed: 5/8"
            await self._parse_progress_from_text(text)

    async def _extract_delta(self, delta: Any) -> None:
        """
        Extract metrics from delta (streaming update)

        Args:
            delta: Delta object from streaming message
        """
        # Similar to content extraction
        if hasattr(delta, 'text'):
            self._message_buffer.append(delta.text)
            await self._parse_progress_from_text(delta.text)

    async def _parse_progress_from_text(self, text: str) -> None:
        """
        Parse progress indicators from text content

        Looks for patterns:
        - "Progress: 60%"
        - "Dimension 5/8"
        - "Stage: Analysis Complete"

        Args:
            text: Text to parse
        """
        import re

        # Progress percentage pattern
        progress_match = re.search(r'(?i)progress:?\s*(\d+(?:\.\d+)?)\s*%', text)
        if progress_match:
            progress = float(progress_match.group(1)) / 100.0
            self._metrics.progress = min(max(progress, 0.0), 1.0)
            self._last_progress_update = datetime.now()

        # Dimension/stage completion pattern
        stage_match = re.search(r'(?i)(?:dimension|stage)\s*(\d+)\s*/\s*(\d+)', text)
        if stage_match:
            current = int(stage_match.group(1))
            total = int(stage_match.group(2))
            self._metrics.total_stages = total
            self._metrics.progress = current / total if total > 0 else 0.0
            self._last_progress_update = datetime.now()

        # Stage name pattern
        stage_name_match = re.search(r'(?i)(?:stage|phase):\s*([A-Za-z\s]+)', text)
        if stage_name_match:
            stage_name = stage_name_match.group(1).strip()
            self._metrics.current_stage = stage_name
            if stage_name not in self._metrics.completed_stages:
                self._metrics.completed_stages.append(stage_name)

    def _default_logger(self) -> logging.Logger:
        """Create default logger if none provided"""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
