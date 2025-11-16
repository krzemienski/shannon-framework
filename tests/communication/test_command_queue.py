"""
Comprehensive tests for Shannon Command Queue system.
"""

import asyncio
import pytest
from datetime import datetime

from shannon.communication.command_queue import (
    CommandQueue,
    CommandType,
    CommandStatus,
    Command,
    get_command_queue,
    reset_command_queue,
)


@pytest.fixture
def command_queue():
    """Create fresh command queue for each test."""
    reset_command_queue()
    queue = CommandQueue(max_history=100)
    yield queue
    reset_command_queue()


@pytest.fixture
def sample_command():
    """Create sample command for testing."""
    return Command(
        command_type=CommandType.HALT,
        priority=5,
        data={"reason": "test halt", "timeout": 60},
        source="test_source",
    )


class TestCommand:
    """Test Command data structure."""

    def test_command_creation(self, sample_command):
        """Test command object creation."""
        assert sample_command.command_type == CommandType.HALT
        assert sample_command.priority == 5
        assert sample_command.data["reason"] == "test halt"
        assert sample_command.source == "test_source"
        assert sample_command.status == CommandStatus.PENDING
        assert sample_command.command_id is not None
        assert isinstance(sample_command.timestamp, datetime)

    def test_command_comparison(self):
        """Test command priority comparison."""
        cmd1 = Command(command_type=CommandType.HALT, priority=1)
        cmd2 = Command(command_type=CommandType.RESUME, priority=5)
        cmd3 = Command(command_type=CommandType.HALT, priority=1)

        # Lower priority number should be less than higher
        assert cmd1 < cmd2
        assert not cmd2 < cmd1

        # Same priority should compare by timestamp
        assert cmd1 < cmd3  # cmd1 created first

    def test_command_to_dict(self, sample_command):
        """Test command serialization to dictionary."""
        cmd_dict = sample_command.to_dict()

        assert cmd_dict["command_type"] == "HALT"
        assert cmd_dict["priority"] == 5
        assert cmd_dict["data"]["reason"] == "test halt"
        assert cmd_dict["source"] == "test_source"
        assert cmd_dict["status"] == "pending"
        assert "command_id" in cmd_dict
        assert "timestamp" in cmd_dict

    def test_command_from_dict(self, sample_command):
        """Test command deserialization from dictionary."""
        cmd_dict = sample_command.to_dict()
        restored_command = Command.from_dict(cmd_dict)

        assert restored_command.command_type == sample_command.command_type
        assert restored_command.priority == sample_command.priority
        assert restored_command.data == sample_command.data
        assert restored_command.source == sample_command.source


class TestCommandQueue:
    """Test CommandQueue functionality."""

    @pytest.mark.asyncio
    async def test_enqueue_command(self, command_queue):
        """Test enqueueing commands."""
        command = await command_queue.enqueue(
            command_type=CommandType.HALT,
            data={"reason": "test"},
            priority=5,
            source="test"
        )

        assert command.command_type == CommandType.HALT
        assert command.priority == 5
        assert command.status == CommandStatus.PENDING
        assert not command_queue.is_empty()

    @pytest.mark.asyncio
    async def test_dequeue_command(self, command_queue):
        """Test dequeueing commands."""
        # Enqueue command
        enqueued = await command_queue.enqueue(
            command_type=CommandType.HALT,
            data={},
            priority=5,
            source="test"
        )

        # Dequeue command
        dequeued = await command_queue.dequeue()

        assert dequeued.command_id == enqueued.command_id
        assert dequeued.status == CommandStatus.PROCESSING
        assert command_queue.is_empty()

    @pytest.mark.asyncio
    async def test_priority_ordering(self, command_queue):
        """Test that commands are dequeued in priority order."""
        # Enqueue with different priorities
        cmd_low = await command_queue.enqueue(
            CommandType.HALT, {}, priority=10, source="test"
        )
        cmd_high = await command_queue.enqueue(
            CommandType.HALT, {}, priority=1, source="test"
        )
        cmd_mid = await command_queue.enqueue(
            CommandType.HALT, {}, priority=5, source="test"
        )

        # Dequeue in priority order
        first = await command_queue.dequeue()
        second = await command_queue.dequeue()
        third = await command_queue.dequeue()

        assert first.command_id == cmd_high.command_id
        assert second.command_id == cmd_mid.command_id
        assert third.command_id == cmd_low.command_id

    @pytest.mark.asyncio
    async def test_complete_command(self, command_queue):
        """Test completing commands."""
        # Enqueue and dequeue
        command = await command_queue.enqueue(
            CommandType.HALT, {}, priority=5, source="test"
        )
        dequeued = await command_queue.dequeue()

        # Complete successfully
        await command_queue.complete_command(
            dequeued,
            result={"success": True}
        )

        assert dequeued.status == CommandStatus.COMPLETED
        assert dequeued.result == {"success": True}
        assert dequeued.error is None

    @pytest.mark.asyncio
    async def test_complete_command_with_error(self, command_queue):
        """Test completing commands with error."""
        # Enqueue and dequeue
        command = await command_queue.enqueue(
            CommandType.HALT, {}, priority=5, source="test"
        )
        dequeued = await command_queue.dequeue()

        # Complete with error
        await command_queue.complete_command(
            dequeued,
            error="Something went wrong"
        )

        assert dequeued.status == CommandStatus.FAILED
        assert dequeued.error == "Something went wrong"

    @pytest.mark.asyncio
    async def test_cancel_command(self, command_queue):
        """Test cancelling pending commands."""
        # Enqueue command
        command = await command_queue.enqueue(
            CommandType.HALT, {}, priority=5, source="test"
        )

        # Cancel it
        result = await command_queue.cancel_command(command.command_id)

        assert result is True
        assert command.status == CommandStatus.CANCELLED

        # Try to dequeue - should timeout since queue is empty
        with pytest.raises(asyncio.TimeoutError):
            await command_queue.dequeue(timeout=0.1)

    @pytest.mark.asyncio
    async def test_cancel_nonexistent_command(self, command_queue):
        """Test cancelling non-existent command."""
        result = await command_queue.cancel_command("nonexistent-id")
        assert result is False

    @pytest.mark.asyncio
    async def test_peek_pending(self, command_queue):
        """Test peeking at pending commands."""
        # Enqueue multiple commands
        cmd1 = await command_queue.enqueue(
            CommandType.HALT, {}, priority=5, source="test"
        )
        cmd2 = await command_queue.enqueue(
            CommandType.RESUME, {}, priority=3, source="test"
        )
        cmd3 = await command_queue.enqueue(
            CommandType.HALT, {}, priority=7, source="test"
        )

        # Peek at pending
        pending = command_queue.peek_pending()

        assert len(pending) == 3
        assert pending[0].command_id == cmd2.command_id  # Highest priority
        assert pending[1].command_id == cmd1.command_id
        assert pending[2].command_id == cmd3.command_id  # Lowest priority

    @pytest.mark.asyncio
    async def test_peek_history(self, command_queue):
        """Test peeking at command history."""
        # Enqueue, dequeue, and complete commands
        for i in range(5):
            cmd = await command_queue.enqueue(
                CommandType.HALT, {"count": i}, priority=5, source="test"
            )
            dequeued = await command_queue.dequeue()
            await command_queue.complete_command(dequeued)

        # Get history
        history = command_queue.peek_history(limit=3)

        assert len(history) == 3
        # Most recent first
        assert history[0].data["count"] == 4
        assert history[1].data["count"] == 3
        assert history[2].data["count"] == 2

    @pytest.mark.asyncio
    async def test_peek_history_with_filters(self, command_queue):
        """Test filtering command history."""
        # Enqueue different command types
        halt_cmd = await command_queue.enqueue(
            CommandType.HALT, {}, priority=5, source="test"
        )
        resume_cmd = await command_queue.enqueue(
            CommandType.RESUME, {}, priority=5, source="test"
        )

        # Complete them
        cmd1 = await command_queue.dequeue()
        await command_queue.complete_command(cmd1)

        cmd2 = await command_queue.dequeue()
        await command_queue.complete_command(cmd2, error="failed")

        # Filter by command type
        halt_history = command_queue.peek_history(
            command_type=CommandType.HALT
        )
        assert len(halt_history) == 1
        assert halt_history[0].command_type == CommandType.HALT

        # Filter by status
        failed_history = command_queue.peek_history(
            status=CommandStatus.FAILED
        )
        assert len(failed_history) == 1
        assert failed_history[0].status == CommandStatus.FAILED

    @pytest.mark.asyncio
    async def test_get_command_by_id(self, command_queue):
        """Test getting command by ID."""
        # Enqueue command
        command = await command_queue.enqueue(
            CommandType.HALT, {}, priority=5, source="test"
        )

        # Get from pending
        found = command_queue.get_command_by_id(command.command_id)
        assert found is not None
        assert found.command_id == command.command_id

        # Dequeue and complete
        dequeued = await command_queue.dequeue()
        await command_queue.complete_command(dequeued)

        # Get from history
        found = command_queue.get_command_by_id(command.command_id)
        assert found is not None
        assert found.command_id == command.command_id

    @pytest.mark.asyncio
    async def test_get_nonexistent_command(self, command_queue):
        """Test getting non-existent command."""
        found = command_queue.get_command_by_id("nonexistent-id")
        assert found is None

    @pytest.mark.asyncio
    async def test_command_stats(self, command_queue):
        """Test command queue statistics."""
        # Enqueue some commands
        await command_queue.enqueue(
            CommandType.HALT, {}, priority=5, source="test"
        )
        await command_queue.enqueue(
            CommandType.RESUME, {}, priority=5, source="test"
        )

        # Complete one
        cmd = await command_queue.dequeue()
        await command_queue.complete_command(cmd)

        stats = command_queue.get_stats()

        assert stats["total_commands"] == 2
        assert stats["pending_count"] == 1
        assert stats["history_size"] == 1
        assert CommandType.HALT.value in stats["type_counts"]
        assert CommandStatus.COMPLETED.value in stats["status_counts"]

    @pytest.mark.asyncio
    async def test_clear_history(self, command_queue):
        """Test clearing command history."""
        # Enqueue and complete commands
        for i in range(3):
            cmd = await command_queue.enqueue(
                CommandType.HALT, {}, priority=5, source="test"
            )
            dequeued = await command_queue.dequeue()
            await command_queue.complete_command(dequeued)

        assert len(command_queue.peek_history()) == 3

        # Clear history
        command_queue.clear_history()

        assert len(command_queue.peek_history()) == 0

    @pytest.mark.asyncio
    async def test_is_empty(self, command_queue):
        """Test checking if queue is empty."""
        assert command_queue.is_empty()

        await command_queue.enqueue(
            CommandType.HALT, {}, priority=5, source="test"
        )

        assert not command_queue.is_empty()

        await command_queue.dequeue()

        assert command_queue.is_empty()

    @pytest.mark.asyncio
    async def test_pending_count(self, command_queue):
        """Test getting count of pending commands."""
        assert command_queue.pending_count() == 0

        await command_queue.enqueue(
            CommandType.HALT, {}, priority=5, source="test"
        )
        await command_queue.enqueue(
            CommandType.RESUME, {}, priority=5, source="test"
        )

        assert command_queue.pending_count() == 2

        await command_queue.dequeue()

        assert command_queue.pending_count() == 1

    @pytest.mark.asyncio
    async def test_enqueue_existing_command(self, command_queue):
        """Test enqueueing an existing command object."""
        command = Command(
            command_type=CommandType.HALT,
            priority=5,
            data={"test": "data"},
            source="test"
        )

        enqueued = await command_queue.enqueue_command(command)

        assert enqueued.command_id == command.command_id
        assert not command_queue.is_empty()

    @pytest.mark.asyncio
    async def test_enqueue_with_priority_override(self, command_queue):
        """Test enqueueing with priority override."""
        command = Command(
            command_type=CommandType.HALT,
            priority=10,
            data={},
            source="test"
        )

        # Enqueue with different priority
        enqueued = await command_queue.enqueue_command(
            command,
            priority=1
        )

        assert enqueued.priority == 1

    @pytest.mark.asyncio
    async def test_invalid_priority(self, command_queue):
        """Test that invalid priorities are rejected."""
        with pytest.raises(ValueError):
            await command_queue.enqueue(
                CommandType.HALT,
                {},
                priority=0,
                source="test"
            )

        with pytest.raises(ValueError):
            await command_queue.enqueue(
                CommandType.HALT,
                {},
                priority=11,
                source="test"
            )

    @pytest.mark.asyncio
    async def test_dequeue_timeout(self, command_queue):
        """Test dequeue with timeout."""
        with pytest.raises(asyncio.TimeoutError):
            await command_queue.dequeue(timeout=0.1)

    @pytest.mark.asyncio
    async def test_max_history_limit(self):
        """Test that history respects max limit."""
        queue = CommandQueue(max_history=5)

        # Enqueue and complete more commands than max
        for i in range(10):
            cmd = await queue.enqueue(
                CommandType.HALT,
                {"count": i},
                priority=5,
                source="test"
            )
            dequeued = await queue.dequeue()
            await queue.complete_command(dequeued)

        history = queue.peek_history(limit=100)
        assert len(history) <= 5

    @pytest.mark.asyncio
    async def test_concurrent_operations(self, command_queue):
        """Test concurrent enqueue/dequeue operations."""
        async def enqueuer():
            for i in range(10):
                await command_queue.enqueue(
                    CommandType.HALT,
                    {"count": i},
                    priority=5,
                    source="test"
                )
                await asyncio.sleep(0.01)

        async def dequeuer():
            for i in range(10):
                await command_queue.dequeue()
                await asyncio.sleep(0.01)

        # Run concurrently
        await asyncio.gather(enqueuer(), dequeuer())

        assert command_queue.is_empty()


class TestGlobalCommandQueue:
    """Test global command queue singleton."""

    def test_get_command_queue(self):
        """Test getting global command queue."""
        reset_command_queue()

        queue1 = get_command_queue()
        queue2 = get_command_queue()

        assert queue1 is queue2

    def test_reset_command_queue(self):
        """Test resetting global command queue."""
        queue1 = get_command_queue()
        reset_command_queue()
        queue2 = get_command_queue()

        assert queue1 is not queue2
