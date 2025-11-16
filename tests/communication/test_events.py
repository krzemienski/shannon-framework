"""
Comprehensive tests for Shannon Event Bus system.
"""

import asyncio
import pytest
from datetime import datetime
from typing import List

from shannon.communication.events import (
    EventBus,
    EventType,
    Event,
    EventSubscription,
    get_event_bus,
    reset_event_bus,
)


@pytest.fixture
def event_bus():
    """Create fresh event bus for each test."""
    reset_event_bus()
    bus = EventBus(max_history=100)
    yield bus
    reset_event_bus()


@pytest.fixture
def sample_event():
    """Create sample event for testing."""
    return Event(
        event_type=EventType.SKILL_STARTED,
        data={"skill_name": "test_skill", "args": {"param": "value"}},
        source="test_source",
        correlation_id="test-correlation-123",
    )


class TestEvent:
    """Test Event data structure."""

    def test_event_creation(self, sample_event):
        """Test event object creation."""
        assert sample_event.event_type == EventType.SKILL_STARTED
        assert sample_event.data["skill_name"] == "test_skill"
        assert sample_event.source == "test_source"
        assert sample_event.correlation_id == "test-correlation-123"
        assert sample_event.event_id is not None
        assert isinstance(sample_event.timestamp, datetime)

    def test_event_to_dict(self, sample_event):
        """Test event serialization to dictionary."""
        event_dict = sample_event.to_dict()

        assert event_dict["event_type"] == "skill:started"
        assert event_dict["data"]["skill_name"] == "test_skill"
        assert event_dict["source"] == "test_source"
        assert event_dict["correlation_id"] == "test-correlation-123"
        assert "event_id" in event_dict
        assert "timestamp" in event_dict

    def test_event_from_dict(self, sample_event):
        """Test event deserialization from dictionary."""
        event_dict = sample_event.to_dict()
        restored_event = Event.from_dict(event_dict)

        assert restored_event.event_type == sample_event.event_type
        assert restored_event.data == sample_event.data
        assert restored_event.source == sample_event.source
        assert restored_event.correlation_id == sample_event.correlation_id


class TestEventBus:
    """Test EventBus functionality."""

    @pytest.mark.asyncio
    async def test_emit_event(self, event_bus):
        """Test emitting events."""
        event = await event_bus.emit(
            event_type=EventType.SKILL_STARTED,
            data={"skill_name": "test"},
            source="test"
        )

        assert event.event_type == EventType.SKILL_STARTED
        assert event.data["skill_name"] == "test"
        assert event.source == "test"

    @pytest.mark.asyncio
    async def test_subscribe_and_receive(self, event_bus):
        """Test subscribing to events and receiving them."""
        received_events = []

        async def handler(event: Event):
            received_events.append(event)

        # Subscribe
        sub_id = await event_bus.subscribe(
            EventType.SKILL_STARTED,
            handler
        )

        # Emit event
        event = await event_bus.emit(
            EventType.SKILL_STARTED,
            data={"test": "data"},
            source="test"
        )

        # Wait for async notification
        await asyncio.sleep(0.1)

        assert len(received_events) == 1
        assert received_events[0].event_type == EventType.SKILL_STARTED
        assert received_events[0].data["test"] == "data"

    @pytest.mark.asyncio
    async def test_multiple_subscribers(self, event_bus):
        """Test multiple subscribers receiving same event."""
        received_1 = []
        received_2 = []

        async def handler_1(event: Event):
            received_1.append(event)

        async def handler_2(event: Event):
            received_2.append(event)

        # Subscribe both handlers
        await event_bus.subscribe(EventType.SKILL_STARTED, handler_1)
        await event_bus.subscribe(EventType.SKILL_STARTED, handler_2)

        # Emit event
        await event_bus.emit(
            EventType.SKILL_STARTED,
            data={"test": "data"},
            source="test"
        )

        await asyncio.sleep(0.1)

        assert len(received_1) == 1
        assert len(received_2) == 1
        assert received_1[0].event_id == received_2[0].event_id

    @pytest.mark.asyncio
    async def test_subscribe_all(self, event_bus):
        """Test subscribing to all events."""
        received_events = []

        async def handler(event: Event):
            received_events.append(event)

        # Subscribe to all events
        await event_bus.subscribe_all(handler)

        # Emit different event types
        await event_bus.emit(
            EventType.SKILL_STARTED,
            data={},
            source="test"
        )
        await event_bus.emit(
            EventType.FILE_CREATED,
            data={},
            source="test"
        )

        await asyncio.sleep(0.1)

        assert len(received_events) == 2
        assert received_events[0].event_type == EventType.SKILL_STARTED
        assert received_events[1].event_type == EventType.FILE_CREATED

    @pytest.mark.asyncio
    async def test_unsubscribe(self, event_bus):
        """Test unsubscribing from events."""
        received_events = []

        async def handler(event: Event):
            received_events.append(event)

        # Subscribe
        sub_id = await event_bus.subscribe(
            EventType.SKILL_STARTED,
            handler
        )

        # Emit first event
        await event_bus.emit(
            EventType.SKILL_STARTED,
            data={"count": 1},
            source="test"
        )

        await asyncio.sleep(0.1)
        assert len(received_events) == 1

        # Unsubscribe
        result = await event_bus.unsubscribe(sub_id)
        assert result is True

        # Emit second event
        await event_bus.emit(
            EventType.SKILL_STARTED,
            data={"count": 2},
            source="test"
        )

        await asyncio.sleep(0.1)
        assert len(received_events) == 1  # Still 1, not 2

    @pytest.mark.asyncio
    async def test_event_filtering(self, event_bus):
        """Test event filtering in subscriptions."""
        received_events = []

        def filter_fn(event: Event) -> bool:
            return event.data.get("important", False)

        async def handler(event: Event):
            received_events.append(event)

        # Subscribe with filter
        await event_bus.subscribe(
            EventType.SKILL_STARTED,
            handler,
            filter_fn=filter_fn
        )

        # Emit important event
        await event_bus.emit(
            EventType.SKILL_STARTED,
            data={"important": True},
            source="test"
        )

        # Emit non-important event
        await event_bus.emit(
            EventType.SKILL_STARTED,
            data={"important": False},
            source="test"
        )

        await asyncio.sleep(0.1)

        # Only important event should be received
        assert len(received_events) == 1
        assert received_events[0].data["important"] is True

    @pytest.mark.asyncio
    async def test_event_history(self, event_bus):
        """Test event history tracking."""
        # Emit multiple events
        for i in range(5):
            await event_bus.emit(
                EventType.SKILL_STARTED,
                data={"count": i},
                source="test"
            )

        # Get all history
        history = event_bus.get_history()
        assert len(history) == 5

        # Get limited history
        history = event_bus.get_history(limit=3)
        assert len(history) == 3
        assert history[-1].data["count"] == 4

        # Get filtered history
        await event_bus.emit(
            EventType.FILE_CREATED,
            data={},
            source="test"
        )
        history = event_bus.get_history(
            event_type=EventType.SKILL_STARTED
        )
        assert len(history) == 5

    @pytest.mark.asyncio
    async def test_correlation_id_filtering(self, event_bus):
        """Test filtering events by correlation ID."""
        correlation_id = "test-correlation-123"

        # Emit events with and without correlation ID
        await event_bus.emit(
            EventType.SKILL_STARTED,
            data={"test": 1},
            source="test",
            correlation_id=correlation_id
        )
        await event_bus.emit(
            EventType.SKILL_STARTED,
            data={"test": 2},
            source="test",
            correlation_id=correlation_id
        )
        await event_bus.emit(
            EventType.SKILL_STARTED,
            data={"test": 3},
            source="test"
        )

        # Get events by correlation ID
        history = event_bus.get_history(correlation_id=correlation_id)
        assert len(history) == 2
        assert all(e.correlation_id == correlation_id for e in history)

    @pytest.mark.asyncio
    async def test_websocket_handler(self, event_bus):
        """Test WebSocket handler registration and notification."""
        websocket_events = []

        async def ws_handler(event: Event):
            websocket_events.append(event)

        # Register WebSocket handler
        event_bus.register_websocket_handler(ws_handler)

        # Emit event
        await event_bus.emit(
            EventType.SKILL_STARTED,
            data={},
            source="test"
        )

        await asyncio.sleep(0.1)

        assert len(websocket_events) == 1

        # Unregister handler
        event_bus.unregister_websocket_handler(ws_handler)

        # Emit another event
        await event_bus.emit(
            EventType.SKILL_STARTED,
            data={},
            source="test"
        )

        await asyncio.sleep(0.1)

        # Still 1, not 2
        assert len(websocket_events) == 1

    @pytest.mark.asyncio
    async def test_event_stats(self, event_bus):
        """Test event bus statistics."""
        # Subscribe to events
        await event_bus.subscribe(
            EventType.SKILL_STARTED,
            lambda e: None
        )
        await event_bus.subscribe(
            EventType.FILE_CREATED,
            lambda e: None
        )
        await event_bus.subscribe_all(lambda e: None)

        # Emit events
        for _ in range(3):
            await event_bus.emit(
                EventType.SKILL_STARTED,
                data={},
                source="test"
            )

        stats = event_bus.get_stats()

        assert stats["total_events"] == 3
        assert stats["history_size"] == 3
        assert stats["global_subscriptions"] == 1
        assert EventType.SKILL_STARTED.value in stats["subscription_counts"]

    @pytest.mark.asyncio
    async def test_sync_handler(self, event_bus):
        """Test that synchronous handlers work."""
        received_events = []

        def sync_handler(event: Event):
            received_events.append(event)

        await event_bus.subscribe(
            EventType.SKILL_STARTED,
            sync_handler
        )

        await event_bus.emit(
            EventType.SKILL_STARTED,
            data={},
            source="test"
        )

        await asyncio.sleep(0.1)

        assert len(received_events) == 1

    @pytest.mark.asyncio
    async def test_replay_events(self, event_bus):
        """Test event replay functionality."""
        received_events = []

        async def handler(event: Event):
            received_events.append(event)

        await event_bus.subscribe(
            EventType.SKILL_STARTED,
            handler
        )

        # Emit some events
        events = []
        for i in range(3):
            event = await event_bus.emit(
                EventType.SKILL_STARTED,
                data={"count": i},
                source="test"
            )
            events.append(event)

        await asyncio.sleep(0.1)
        assert len(received_events) == 3

        # Clear received events
        received_events.clear()

        # Replay events
        await event_bus.replay_events(events)

        await asyncio.sleep(0.1)
        assert len(received_events) == 3

    @pytest.mark.asyncio
    async def test_clear_history(self, event_bus):
        """Test clearing event history."""
        # Emit events
        for i in range(5):
            await event_bus.emit(
                EventType.SKILL_STARTED,
                data={"count": i},
                source="test"
            )

        assert len(event_bus.get_history()) == 5

        # Clear history
        await event_bus.clear_history()

        assert len(event_bus.get_history()) == 0

    @pytest.mark.asyncio
    async def test_max_history_limit(self):
        """Test that history respects max limit."""
        event_bus = EventBus(max_history=10)

        # Emit more events than max
        for i in range(15):
            await event_bus.emit(
                EventType.SKILL_STARTED,
                data={"count": i},
                source="test"
            )

        history = event_bus.get_history()
        assert len(history) == 10

        # Should have most recent events
        assert history[-1].data["count"] == 14


class TestGlobalEventBus:
    """Test global event bus singleton."""

    def test_get_event_bus(self):
        """Test getting global event bus."""
        reset_event_bus()

        bus1 = get_event_bus()
        bus2 = get_event_bus()

        assert bus1 is bus2

    def test_reset_event_bus(self):
        """Test resetting global event bus."""
        bus1 = get_event_bus()
        reset_event_bus()
        bus2 = get_event_bus()

        assert bus1 is not bus2
