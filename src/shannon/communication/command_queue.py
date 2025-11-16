"""
Shannon Command Queue System

Production-grade command queue for handling real-time commands from
external interfaces. Supports priority-based processing, command history,
and rollback capabilities.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

logger = logging.getLogger(__name__)


class CommandType(Enum):
    """Command types for Shannon system control."""

    HALT = "HALT"
    RESUME = "RESUME"
    ROLLBACK = "ROLLBACK"
    REDIRECT = "REDIRECT"
    DECISION = "DECISION"
    INJECT = "INJECT"
    CHECKPOINT = "CHECKPOINT"
    CANCEL = "CANCEL"
    PRIORITY = "PRIORITY"


class CommandStatus(Enum):
    """Status of command execution."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Command:
    """
    Command data structure for Shannon commands.

    Attributes:
        command_id: Unique command identifier
        command_type: Type of command
        priority: Priority level (1=highest, 10=lowest)
        timestamp: When command was created
        data: Command payload data
        source: Source of command
        status: Current execution status
        result: Command execution result
        error: Error message if failed
        metadata: Additional command metadata
    """
    command_id: str = field(default_factory=lambda: str(uuid4()))
    command_type: CommandType = field(default=CommandType.HALT)
    priority: int = field(default=5)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = field(default_factory=dict)
    source: str = field(default="unknown")
    status: CommandStatus = field(default=CommandStatus.PENDING)
    result: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __lt__(self, other: "Command") -> bool:
        """Compare commands by priority (lower number = higher priority)."""
        if self.priority != other.priority:
            return self.priority < other.priority
        # Secondary sort by timestamp (older first)
        return self.timestamp < other.timestamp

    def to_dict(self) -> Dict[str, Any]:
        """Convert command to dictionary for serialization."""
        return {
            "command_id": self.command_id,
            "command_type": self.command_type.value,
            "priority": self.priority,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "source": self.source,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Command":
        """Create command from dictionary."""
        return cls(
            command_id=data.get("command_id", str(uuid4())),
            command_type=CommandType(data["command_type"]),
            priority=data.get("priority", 5),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            data=data.get("data", {}),
            source=data.get("source", "unknown"),
            status=CommandStatus(data.get("status", "pending")),
            result=data.get("result"),
            error=data.get("error"),
            metadata=data.get("metadata", {}),
        )


class CommandQueue:
    """
    Production-grade command queue for Shannon system.

    Features:
    - Priority-based command processing
    - Async command handling
    - Command history and replay
    - Cancellation support
    - Statistics tracking
    """

    def __init__(
        self,
        max_history: int = 1000,
        enable_history: bool = True,
    ):
        """
        Initialize command queue.

        Args:
            max_history: Maximum commands to keep in history
            enable_history: Whether to track command history
        """
        self._queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self._history: List[Command] = []
        self._max_history = max_history
        self._enable_history = enable_history
        self._pending_commands: Dict[str, Command] = {}
        self._lock = asyncio.Lock()
        self._command_count = 0
        self._processing_task: Optional[asyncio.Task] = None

        logger.info("CommandQueue initialized")

    async def enqueue(
        self,
        command_type: CommandType,
        data: Dict[str, Any],
        priority: int = 5,
        source: str = "unknown",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Command:
        """
        Add command to queue with priority.

        Args:
            command_type: Type of command
            data: Command data payload
            priority: Priority level (1=highest, 10=lowest)
            source: Source of command
            metadata: Optional metadata

        Returns:
            Created command object
        """
        if not 1 <= priority <= 10:
            raise ValueError("Priority must be between 1 and 10")

        command = Command(
            command_type=command_type,
            priority=priority,
            data=data,
            source=source,
            metadata=metadata or {},
        )

        async with self._lock:
            self._command_count += 1
            self._pending_commands[command.command_id] = command

        await self._queue.put(command)

        logger.info(
            f"Command enqueued: {command_type.value} "
            f"(priority={priority}, id={command.command_id})"
        )

        return command

    async def enqueue_command(
        self,
        command: Command,
        priority: Optional[int] = None,
    ) -> Command:
        """
        Enqueue existing command object.

        Args:
            command: Command to enqueue
            priority: Optional priority override

        Returns:
            The enqueued command
        """
        if priority is not None:
            if not 1 <= priority <= 10:
                raise ValueError("Priority must be between 1 and 10")
            command.priority = priority

        async with self._lock:
            self._command_count += 1
            self._pending_commands[command.command_id] = command

        await self._queue.put(command)

        logger.info(
            f"Command enqueued: {command.command_type.value} "
            f"(priority={command.priority}, id={command.command_id})"
        )

        return command

    async def dequeue(self, timeout: Optional[float] = None) -> Command:
        """
        Get next command from queue.

        Args:
            timeout: Optional timeout in seconds

        Returns:
            Next command in priority order

        Raises:
            asyncio.TimeoutError: If timeout expires
        """
        while True:
            if timeout:
                command = await asyncio.wait_for(
                    self._queue.get(),
                    timeout=timeout
                )
            else:
                command = await self._queue.get()

            async with self._lock:
                # Skip cancelled commands
                if command.status == CommandStatus.CANCELLED:
                    continue

                if command.command_id in self._pending_commands:
                    del self._pending_commands[command.command_id]

            command.status = CommandStatus.PROCESSING

            logger.debug(
                f"Command dequeued: {command.command_type.value} "
                f"(id={command.command_id})"
            )

            return command

    async def complete_command(
        self,
        command: Command,
        result: Optional[Any] = None,
        error: Optional[str] = None,
    ) -> None:
        """
        Mark command as completed.

        Args:
            command: Command to complete
            result: Optional result data
            error: Optional error message
        """
        command.status = (
            CommandStatus.FAILED if error
            else CommandStatus.COMPLETED
        )
        command.result = result
        command.error = error

        async with self._lock:
            if self._enable_history:
                self._history.append(command)
                if len(self._history) > self._max_history:
                    self._history.pop(0)

        logger.info(
            f"Command completed: {command.command_type.value} "
            f"(status={command.status.value}, id={command.command_id})"
        )

    async def cancel_command(self, command_id: str) -> bool:
        """
        Cancel pending command.

        Args:
            command_id: ID of command to cancel

        Returns:
            True if cancelled, False if not found
        """
        async with self._lock:
            if command_id in self._pending_commands:
                command = self._pending_commands[command_id]
                command.status = CommandStatus.CANCELLED
                del self._pending_commands[command_id]

                if self._enable_history:
                    self._history.append(command)

                logger.info(f"Command cancelled: {command_id}")
                return True

        logger.warning(f"Command not found for cancellation: {command_id}")
        return False

    def peek_pending(self) -> List[Command]:
        """
        Peek at pending commands without removing them.

        Returns:
            List of pending commands in priority order
        """
        commands = sorted(
            self._pending_commands.values(),
            key=lambda c: (c.priority, c.timestamp)
        )
        return commands

    def peek_history(
        self,
        limit: int = 10,
        command_type: Optional[CommandType] = None,
        status: Optional[CommandStatus] = None,
    ) -> List[Command]:
        """
        Get recent commands from history.

        Args:
            limit: Maximum number of commands to return
            command_type: Optional filter by command type
            status: Optional filter by status

        Returns:
            List of recent commands
        """
        commands = self._history

        # Filter by command type
        if command_type:
            commands = [
                c for c in commands
                if c.command_type == command_type
            ]

        # Filter by status
        if status:
            commands = [
                c for c in commands
                if c.status == status
            ]

        # Return most recent first
        return commands[-limit:][::-1]

    def get_command_by_id(self, command_id: str) -> Optional[Command]:
        """
        Get command by ID from pending or history.

        Args:
            command_id: Command ID to find

        Returns:
            Command if found, None otherwise
        """
        # Check pending
        if command_id in self._pending_commands:
            return self._pending_commands[command_id]

        # Check history
        for command in reversed(self._history):
            if command.command_id == command_id:
                return command

        return None

    def get_stats(self) -> Dict[str, Any]:
        """
        Get command queue statistics.

        Returns:
            Dictionary of statistics
        """
        status_counts = {}
        for command in self._history:
            status = command.status.value
            status_counts[status] = status_counts.get(status, 0) + 1

        type_counts = {}
        for command in self._history:
            cmd_type = command.command_type.value
            type_counts[cmd_type] = type_counts.get(cmd_type, 0) + 1

        return {
            "total_commands": self._command_count,
            "pending_count": len(self._pending_commands),
            "history_size": len(self._history),
            "status_counts": status_counts,
            "type_counts": type_counts,
        }

    def clear_history(self) -> None:
        """Clear command history."""
        self._history.clear()
        logger.info("Command history cleared")

    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return self._queue.empty()

    def pending_count(self) -> int:
        """Get count of pending commands."""
        return len(self._pending_commands)


# Global command queue instance
_command_queue: Optional[CommandQueue] = None


def get_command_queue() -> CommandQueue:
    """Get or create global command queue instance."""
    global _command_queue
    if _command_queue is None:
        _command_queue = CommandQueue()
    return _command_queue


def reset_command_queue() -> None:
    """Reset global command queue (for testing)."""
    global _command_queue
    _command_queue = None
