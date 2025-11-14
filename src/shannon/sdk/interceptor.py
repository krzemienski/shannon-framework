"""SDK Message Interceptor for Shannon CLI V3.0

Transparent async wrapper around Claude Agent SDK query() that enables:
1. Zero-latency message streaming (messages yielded immediately)
2. Parallel collector pattern for metrics, tracking, context extraction
3. Error isolation (collector failures don't break stream)
4. Non-breaking SDK API contract

Architecture:
    SDK query() → MessageInterceptor → [Collectors run in parallel] → Client receives messages

Key Design Decision (from SHANNON_CLI_V3_ARCHITECTURE.md 4.1):
- Messages yielded immediately (zero latency)
- Collectors execute via asyncio.create_task() in background
- No blocking, no race conditions
- Maintains async iterator contract
"""

from typing import AsyncIterator, List, Protocol, Any, Optional
from abc import ABC, abstractmethod
import asyncio
import logging
from datetime import datetime


class MessageCollector(ABC):
    """
    Abstract base for message collectors

    All collectors implement this interface and process messages asynchronously
    without blocking the main stream.

    Examples:
        - MetricsCollector: Extract cost, tokens, timing
        - AgentStateCollector: Track agent progress, tool calls
        - ContextCollector: Extract file references, context usage
    """

    @abstractmethod
    async def process(self, message: Any) -> None:
        """
        Process a message asynchronously

        This method is called in background via asyncio.create_task()
        and MUST NOT raise exceptions (handle internally).

        Args:
            message: SDK message (AssistantMessage, ToolUseBlock, etc.)
        """
        pass

    @abstractmethod
    async def on_stream_complete(self) -> None:
        """
        Called when message stream completes

        Use for finalization, flushing buffers, etc.
        """
        pass

    @abstractmethod
    async def on_stream_error(self, error: Exception) -> None:
        """
        Called when message stream errors

        Args:
            error: Exception that occurred
        """
        pass


class MessageInterceptor:
    """
    Transparent async wrapper for SDK query() with parallel collectors

    Core implementation of Shannon V3 message interception strategy.

    Usage:
        interceptor = MessageInterceptor()
        collectors = [MetricsCollector(), AgentStateCollector()]

        # Wrap SDK query iterator
        async for msg in interceptor.intercept(query_iterator, collectors):
            # Caller receives messages with ZERO latency
            # Collectors process in parallel
            yield msg

    Performance Characteristics:
        - Zero added latency (messages yielded immediately)
        - O(1) overhead per message (task creation)
        - Collectors run in parallel (non-blocking)
        - Error isolation (collector failures don't affect stream)
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize message interceptor

        Args:
            logger: Optional logger for debugging
        """
        self.logger = logger or self._default_logger()
        self._active_tasks: List[asyncio.Task] = []

    async def intercept(
        self,
        query_iterator: AsyncIterator[Any],
        collectors: List[MessageCollector]
    ) -> AsyncIterator[Any]:
        """
        Intercept SDK query messages while maintaining streaming behavior

        Key Insight (from architecture doc):
            Use asyncio.create_task() to process messages in parallel
            with yielding them, avoiding any blocking.

        Args:
            query_iterator: AsyncIterator from SDK query()
            collectors: List of MessageCollector instances

        Yields:
            Messages from query_iterator (unchanged, zero latency)

        Example:
            query_iter = query(prompt, options)
            collectors = [MetricsCollector(), ContextCollector()]

            async for msg in interceptor.intercept(query_iter, collectors):
                # msg received with zero latency
                # collectors processing in background
                print(msg)
        """
        message_count = 0
        error_occurred: Optional[Exception] = None

        try:
            async for msg in query_iterator:
                message_count += 1

                # Non-blocking: Fire collectors in background
                for collector in collectors:
                    # Create task for each collector
                    # Tasks run in parallel, don't block message yielding
                    task = asyncio.create_task(
                        self._safe_process(collector, msg, message_count)
                    )
                    self._active_tasks.append(task)

                # Yield immediately - zero latency added
                yield msg

            self.logger.debug(f"Stream complete: {message_count} messages processed")

        except Exception as e:
            error_occurred = e
            self.logger.error(f"Stream error after {message_count} messages: {e}")
            raise

        finally:
            # Wait for all collector tasks to complete
            await self._finalize_collectors(collectors, error_occurred)

    async def _safe_process(
        self,
        collector: MessageCollector,
        message: Any,
        message_number: int
    ) -> None:
        """
        Safely process message with error isolation

        Ensures collector errors don't affect:
        1. Message stream delivery
        2. Other collectors
        3. Overall operation

        Args:
            collector: Collector instance
            message: SDK message to process
            message_number: Sequential message number for debugging
        """
        collector_name = collector.__class__.__name__

        try:
            await collector.process(message)

        except asyncio.CancelledError:
            # Task was cancelled (normal during cleanup)
            self.logger.debug(
                f"{collector_name}: Task cancelled at message {message_number}"
            )

        except Exception as e:
            # Collector error - log but don't propagate
            self.logger.error(
                f"{collector_name}: Error processing message {message_number}: {e}",
                exc_info=True
            )

    async def _finalize_collectors(
        self,
        collectors: List[MessageCollector],
        error: Optional[Exception]
    ) -> None:
        """
        Finalize all collectors after stream completes or errors

        Args:
            collectors: List of collectors to finalize
            error: Exception if stream errored, None if completed normally
        """
        # Wait for all active tasks to complete
        if self._active_tasks:
            self.logger.debug(f"Waiting for {len(self._active_tasks)} collector tasks")

            # Give tasks reasonable time to complete
            try:
                await asyncio.wait_for(
                    asyncio.gather(*self._active_tasks, return_exceptions=True),
                    timeout=5.0
                )
            except asyncio.TimeoutError:
                self.logger.warning("Collector tasks timeout - cancelling remaining tasks")
                for task in self._active_tasks:
                    if not task.done():
                        task.cancel()

            self._active_tasks.clear()

        # Call appropriate lifecycle method on each collector
        for collector in collectors:
            collector_name = collector.__class__.__name__

            try:
                if error:
                    await collector.on_stream_error(error)
                else:
                    await collector.on_stream_complete()

            except Exception as e:
                # Collector lifecycle error - log but don't propagate
                self.logger.error(
                    f"{collector_name}: Error in finalization: {e}",
                    exc_info=True
                )

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


class TransparentAsyncWrapper:
    """
    Convenience wrapper for common interceptor usage patterns

    Provides simplified API for integrating interceptor into existing code.

    Usage:
        wrapper = TransparentAsyncWrapper(collectors=[...])

        # Wrap any async iterator
        async for msg in wrapper.wrap(query_iterator):
            yield msg
    """

    def __init__(
        self,
        collectors: List[MessageCollector],
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize wrapper with collectors

        Args:
            collectors: List of collectors to use for all wrapped iterators
            logger: Optional logger
        """
        self.collectors = collectors
        self.interceptor = MessageInterceptor(logger=logger)

    async def wrap(self, query_iterator: AsyncIterator[Any]) -> AsyncIterator[Any]:
        """
        Wrap async iterator with interception

        Args:
            query_iterator: AsyncIterator to wrap

        Yields:
            Messages from iterator (with collectors running in background)
        """
        async for msg in self.interceptor.intercept(query_iterator, self.collectors):
            yield msg


# Example collector implementations (for reference/testing)

class DebugCollector(MessageCollector):
    """
    Debug collector that logs all messages

    Useful for development and testing.
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        self.message_count = 0
        self.start_time: Optional[datetime] = None

    async def process(self, message: Any) -> None:
        """Log message type and count"""
        if self.start_time is None:
            self.start_time = datetime.now()

        self.message_count += 1
        msg_type = type(message).__name__
        self.logger.debug(f"Message {self.message_count}: {msg_type}")

    async def on_stream_complete(self) -> None:
        """Log completion statistics"""
        if self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds()
            self.logger.info(
                f"Stream complete: {self.message_count} messages in {duration:.2f}s"
            )

    async def on_stream_error(self, error: Exception) -> None:
        """Log error"""
        self.logger.error(f"Stream error after {self.message_count} messages: {error}")


class BufferingCollector(MessageCollector):
    """
    Collector that buffers all messages in memory

    Useful for testing and post-processing analysis.
    """

    def __init__(self, max_messages: int = 1000):
        """
        Initialize buffering collector

        Args:
            max_messages: Maximum messages to buffer (prevents unbounded growth)
        """
        self.messages: List[Any] = []
        self.max_messages = max_messages
        self.overflow_count = 0

    async def process(self, message: Any) -> None:
        """Buffer message if space available"""
        if len(self.messages) < self.max_messages:
            self.messages.append(message)
        else:
            self.overflow_count += 1

    async def on_stream_complete(self) -> None:
        """Stream completed"""
        pass

    async def on_stream_error(self, error: Exception) -> None:
        """Stream errored"""
        pass

    def get_messages(self) -> List[Any]:
        """
        Get buffered messages

        Returns:
            List of buffered messages
        """
        return self.messages.copy()

    def clear(self) -> None:
        """Clear buffer"""
        self.messages.clear()
        self.overflow_count = 0
