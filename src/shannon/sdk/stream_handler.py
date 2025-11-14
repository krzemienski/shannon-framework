"""Stream Handler for Shannon CLI V3.0

Async stream management with buffering and health monitoring.

Responsibilities:
1. Async stream lifecycle management
2. Message buffering for high-throughput scenarios
3. Stream health monitoring (timeouts, stalls)
4. Graceful error handling and recovery

Architecture:
    MessageInterceptor → StreamHandler → Buffered/Monitored Stream → Client
"""

from typing import AsyncIterator, Any, Optional, List
from collections import deque
from datetime import datetime, timedelta
import asyncio
import logging


class StreamHealthMonitor:
    """
    Monitor stream health for timeouts and stalls

    Tracks:
    - Time since last message
    - Total stream duration
    - Message rate
    - Stall detection
    """

    def __init__(
        self,
        stall_timeout: float = 30.0,
        total_timeout: float = 600.0,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize health monitor

        Args:
            stall_timeout: Seconds without message before considering stalled
            total_timeout: Maximum total stream duration in seconds
            logger: Optional logger
        """
        self.stall_timeout = stall_timeout
        self.total_timeout = total_timeout
        self.logger = logger or self._default_logger()

        self.start_time: Optional[datetime] = None
        self.last_message_time: Optional[datetime] = None
        self.message_count = 0

    def on_stream_start(self) -> None:
        """Called when stream starts"""
        self.start_time = datetime.now()
        self.last_message_time = datetime.now()
        self.message_count = 0
        self.logger.debug("Stream health monitoring started")

    def on_message_received(self) -> None:
        """Called when message received"""
        self.last_message_time = datetime.now()
        self.message_count += 1

    def check_health(self) -> tuple[bool, Optional[str]]:
        """
        Check if stream is healthy

        Returns:
            (is_healthy, error_message)
            - (True, None) if healthy
            - (False, "reason") if unhealthy
        """
        if not self.start_time or not self.last_message_time:
            return True, None

        now = datetime.now()

        # Check total timeout
        total_duration = (now - self.start_time).total_seconds()
        if total_duration > self.total_timeout:
            return False, f"Total timeout exceeded ({total_duration:.1f}s > {self.total_timeout}s)"

        # Check stall timeout
        stall_duration = (now - self.last_message_time).total_seconds()
        if stall_duration > self.stall_timeout:
            return False, f"Stream stalled ({stall_duration:.1f}s since last message)"

        return True, None

    def get_stats(self) -> dict[str, Any]:
        """
        Get stream statistics

        Returns:
            Dictionary with timing and throughput stats
        """
        if not self.start_time:
            return {
                "status": "not_started",
                "message_count": 0,
                "duration": 0.0,
                "messages_per_second": 0.0
            }

        now = datetime.now()
        duration = (now - self.start_time).total_seconds()
        messages_per_second = self.message_count / duration if duration > 0 else 0.0

        return {
            "status": "active",
            "message_count": self.message_count,
            "duration": duration,
            "messages_per_second": messages_per_second,
            "seconds_since_last_message": (now - self.last_message_time).total_seconds()
                if self.last_message_time else 0.0
        }

    def _default_logger(self) -> logging.Logger:
        """Create default logger"""
        return logging.getLogger(__name__)


class StreamBuffer:
    """
    Async-safe message buffer with backpressure handling

    Features:
    - Bounded buffer (prevents unbounded memory growth)
    - Backpressure signaling when full
    - Thread-safe async operations
    - Efficient deque-based storage
    """

    def __init__(self, max_size: int = 100):
        """
        Initialize stream buffer

        Args:
            max_size: Maximum buffered messages (prevents memory issues)
        """
        self.max_size = max_size
        self.buffer: deque[Any] = deque(maxlen=max_size)
        self.overflow_count = 0
        self._lock = asyncio.Lock()

    async def put(self, message: Any) -> bool:
        """
        Add message to buffer

        Args:
            message: Message to buffer

        Returns:
            True if buffered, False if buffer full (overflow)
        """
        async with self._lock:
            if len(self.buffer) >= self.max_size:
                self.overflow_count += 1
                return False

            self.buffer.append(message)
            return True

    async def get_all(self) -> List[Any]:
        """
        Get all buffered messages (consumes buffer)

        Returns:
            List of buffered messages
        """
        async with self._lock:
            messages = list(self.buffer)
            self.buffer.clear()
            return messages

    async def peek_all(self) -> List[Any]:
        """
        Get all buffered messages (non-consuming)

        Returns:
            List of buffered messages (buffer unchanged)
        """
        async with self._lock:
            return list(self.buffer)

    async def size(self) -> int:
        """Get current buffer size"""
        async with self._lock:
            return len(self.buffer)

    async def clear(self) -> None:
        """Clear buffer"""
        async with self._lock:
            self.buffer.clear()
            self.overflow_count = 0


class StreamHandler:
    """
    Async stream handler with buffering and health monitoring

    Manages stream lifecycle:
    1. Health monitoring (timeouts, stalls)
    2. Optional buffering for replay/analysis
    3. Graceful error handling
    4. Stream statistics

    Usage:
        handler = StreamHandler(enable_buffering=True)

        async for msg in handler.handle(stream_iterator):
            # Messages monitored and optionally buffered
            yield msg

        # Get statistics
        stats = handler.get_stats()
    """

    def __init__(
        self,
        enable_buffering: bool = False,
        buffer_size: int = 100,
        stall_timeout: float = 30.0,
        total_timeout: float = 600.0,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize stream handler

        Args:
            enable_buffering: Enable message buffering
            buffer_size: Maximum buffered messages
            stall_timeout: Seconds without message before stall warning
            total_timeout: Maximum total stream duration
            logger: Optional logger
        """
        self.enable_buffering = enable_buffering
        self.logger = logger or self._default_logger()

        # Components
        self.health_monitor = StreamHealthMonitor(
            stall_timeout=stall_timeout,
            total_timeout=total_timeout,
            logger=self.logger
        )

        self.buffer: Optional[StreamBuffer] = None
        if enable_buffering:
            self.buffer = StreamBuffer(max_size=buffer_size)

        # State
        self.is_active = False
        self.completed_successfully = False
        self.error: Optional[Exception] = None

    async def handle(
        self,
        stream_iterator: AsyncIterator[Any]
    ) -> AsyncIterator[Any]:
        """
        Handle stream with monitoring and optional buffering

        Args:
            stream_iterator: Async iterator to handle

        Yields:
            Messages from iterator

        Raises:
            asyncio.TimeoutError: If stream exceeds timeouts
            Exception: If stream errors
        """
        self.is_active = True
        self.completed_successfully = False
        self.error = None

        # Start monitoring
        self.health_monitor.on_stream_start()
        self.logger.debug("Stream handling started")

        try:
            async for msg in stream_iterator:
                # Update health monitor
                self.health_monitor.on_message_received()

                # Check health
                is_healthy, error_msg = self.health_monitor.check_health()
                if not is_healthy:
                    self.logger.error(f"Stream health check failed: {error_msg}")
                    raise asyncio.TimeoutError(error_msg)

                # Buffer if enabled
                if self.buffer:
                    buffered = await self.buffer.put(msg)
                    if not buffered:
                        self.logger.warning("Stream buffer full - message not buffered")

                # Yield message
                yield msg

            # Stream completed successfully
            self.completed_successfully = True
            stats = self.health_monitor.get_stats()
            self.logger.info(
                f"Stream complete: {stats['message_count']} messages "
                f"in {stats['duration']:.2f}s "
                f"({stats['messages_per_second']:.1f} msg/s)"
            )

        except Exception as e:
            self.error = e
            self.logger.error(f"Stream error: {e}")
            raise

        finally:
            self.is_active = False

    def get_stats(self) -> dict[str, Any]:
        """
        Get stream statistics

        Returns:
            Dictionary with stream stats
        """
        stats = self.health_monitor.get_stats()
        stats.update({
            "is_active": self.is_active,
            "completed_successfully": self.completed_successfully,
            "has_error": self.error is not None
        })

        if self.buffer:
            # Synchronous access to buffer size (lock-free read)
            stats["buffer_size"] = len(self.buffer.buffer)
            stats["buffer_overflow_count"] = self.buffer.overflow_count

        return stats

    async def get_buffered_messages(self) -> List[Any]:
        """
        Get all buffered messages (if buffering enabled)

        Returns:
            List of buffered messages, or empty list if buffering disabled
        """
        if not self.buffer:
            return []

        return await self.buffer.peek_all()

    async def clear_buffer(self) -> None:
        """Clear buffer (if buffering enabled)"""
        if self.buffer:
            await self.buffer.clear()

    def _default_logger(self) -> logging.Logger:
        """Create default logger"""
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
