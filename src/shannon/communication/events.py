"""
Shannon Event Bus System

Production-grade event bus for real-time event propagation across
Shannon components. Supports multiple subscribers, WebSocket integration,
and comprehensive event tracking.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set
from uuid import uuid4

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Event types for Shannon system events."""

    # Skill events
    SKILL_STARTED = "skill:started"
    SKILL_COMPLETED = "skill:completed"
    SKILL_FAILED = "skill:failed"
    SKILL_PROGRESS = "skill:progress"

    # File events
    FILE_MODIFIED = "file:modified"
    FILE_CREATED = "file:created"
    FILE_DELETED = "file:deleted"
    FILE_MOVED = "file:moved"

    # Decision events
    DECISION_POINT = "decision:point"
    DECISION_MADE = "decision:made"
    DECISION_REQUIRED = "decision:required"

    # Validation events
    VALIDATION_STARTED = "validation:started"
    VALIDATION_RESULT = "validation:result"
    VALIDATION_FAILED = "validation:failed"

    # Agent events
    AGENT_SPAWNED = "agent:spawned"
    AGENT_PROGRESS = "agent:progress"
    AGENT_COMPLETED = "agent:completed"
    AGENT_FAILED = "agent:failed"

    # System events
    CHECKPOINT_CREATED = "checkpoint:created"
    CHECKPOINT_RESTORED = "checkpoint:restored"
    EXECUTION_HALTED = "execution:halted"
    EXECUTION_RESUMED = "execution:resumed"
    EXECUTION_STARTED = "execution:started"
    EXECUTION_COMPLETED = "execution:completed"

    # Wave events
    WAVE_STARTED = "wave:started"
    WAVE_COMPLETED = "wave:completed"
    WAVE_FAILED = "wave:failed"

    # Error events
    ERROR_OCCURRED = "error:occurred"
    ERROR_RECOVERED = "error:recovered"


@dataclass
class Event:
    """
    Event data structure for Shannon events.

    Attributes:
        event_id: Unique event identifier
        event_type: Type of event
        timestamp: When event occurred
        data: Event payload data
        source: Component that emitted the event
        correlation_id: ID for correlating related events
        metadata: Additional event metadata
    """
    event_id: str = field(default_factory=lambda: str(uuid4()))
    event_type: EventType = field(default=EventType.EXECUTION_STARTED)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = field(default_factory=dict)
    source: str = field(default="unknown")
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary for serialization."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "source": self.source,
            "correlation_id": self.correlation_id,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        """Create event from dictionary."""
        return cls(
            event_id=data.get("event_id", str(uuid4())),
            event_type=EventType(data["event_type"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            data=data.get("data", {}),
            source=data.get("source", "unknown"),
            correlation_id=data.get("correlation_id"),
            metadata=data.get("metadata", {}),
        )


class EventSubscription:
    """Subscription to an event type with handler and filters."""

    def __init__(
        self,
        event_type: EventType,
        handler: Callable[[Event], Any],
        filter_fn: Optional[Callable[[Event], bool]] = None,
        subscription_id: Optional[str] = None,
    ):
        """
        Initialize event subscription.

        Args:
            event_type: Type of event to subscribe to
            handler: Async or sync handler function
            filter_fn: Optional filter function for selective handling
            subscription_id: Optional custom subscription ID
        """
        self.subscription_id = subscription_id or str(uuid4())
        self.event_type = event_type
        self.handler = handler
        self.filter_fn = filter_fn
        self.created_at = datetime.utcnow()
        self.call_count = 0
        self.error_count = 0
        self.last_called = None

    async def handle(self, event: Event) -> bool:
        """
        Handle event with subscription handler.

        Args:
            event: Event to handle

        Returns:
            True if handled successfully, False otherwise
        """
        # Apply filter if present
        if self.filter_fn and not self.filter_fn(event):
            return True

        try:
            # Call handler (support both async and sync)
            if asyncio.iscoroutinefunction(self.handler):
                await self.handler(event)
            else:
                self.handler(event)

            self.call_count += 1
            self.last_called = datetime.utcnow()
            return True

        except Exception as e:
            self.error_count += 1
            logger.error(
                f"Error in event handler {self.subscription_id}: {e}",
                exc_info=True
            )
            return False


class EventBus:
    """
    Production-grade event bus for Shannon system.

    Features:
    - Async event emission and handling
    - Multiple subscribers per event type
    - Event filtering and correlation
    - WebSocket integration
    - Event history and replay
    - Subscription management
    """

    def __init__(
        self,
        max_history: int = 1000,
        enable_history: bool = True,
    ):
        """
        Initialize event bus.

        Args:
            max_history: Maximum events to keep in history
            enable_history: Whether to track event history
        """
        self._subscriptions: Dict[EventType, List[EventSubscription]] = {}
        self._global_subscriptions: List[EventSubscription] = []
        self._history: List[Event] = []
        self._max_history = max_history
        self._enable_history = enable_history
        self._websocket_handlers: Set[Callable[[Event], Any]] = set()
        self._event_count = 0
        self._lock = asyncio.Lock()

        logger.info("EventBus initialized")

    async def emit(
        self,
        event_type: EventType,
        data: Dict[str, Any],
        source: str = "unknown",
        correlation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Event:
        """
        Emit event to all subscribers.

        Args:
            event_type: Type of event
            data: Event data payload
            source: Source component
            correlation_id: Optional correlation ID
            metadata: Optional metadata

        Returns:
            Created event object
        """
        # Create event
        event = Event(
            event_type=event_type,
            data=data,
            source=source,
            correlation_id=correlation_id,
            metadata=metadata or {},
        )

        async with self._lock:
            self._event_count += 1

            # Add to history
            if self._enable_history:
                self._history.append(event)
                if len(self._history) > self._max_history:
                    self._history.pop(0)

        logger.debug(
            f"Event emitted: {event_type.value} from {source} "
            f"(id={event.event_id})"
        )

        # Notify subscribers (don't await to prevent blocking)
        asyncio.create_task(self._notify_subscribers(event))

        return event

    async def _notify_subscribers(self, event: Event) -> None:
        """
        Notify all subscribers of event.

        Args:
            event: Event to notify about
        """
        # Get subscribers for this event type
        subscriptions = self._subscriptions.get(event.event_type, [])
        all_subscriptions = subscriptions + self._global_subscriptions

        # Notify all subscribers concurrently
        if all_subscriptions:
            tasks = [sub.handle(event) for sub in all_subscriptions]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Log any errors
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(
                        f"Subscription handler failed: {result}",
                        exc_info=result
                    )

        # Notify WebSocket handlers (always, even if no subscriptions)
        if self._websocket_handlers:
            await self.emit_to_websocket(event)

    async def subscribe(
        self,
        event_type: EventType,
        handler: Callable[[Event], Any],
        filter_fn: Optional[Callable[[Event], bool]] = None,
        subscription_id: Optional[str] = None,
    ) -> str:
        """
        Subscribe to specific event type.

        Args:
            event_type: Event type to subscribe to
            handler: Handler function (async or sync)
            filter_fn: Optional filter function
            subscription_id: Optional custom subscription ID

        Returns:
            Subscription ID for unsubscribing
        """
        subscription = EventSubscription(
            event_type=event_type,
            handler=handler,
            filter_fn=filter_fn,
            subscription_id=subscription_id,
        )

        async with self._lock:
            if event_type not in self._subscriptions:
                self._subscriptions[event_type] = []
            self._subscriptions[event_type].append(subscription)

        logger.info(
            f"Subscribed to {event_type.value} "
            f"(id={subscription.subscription_id})"
        )

        return subscription.subscription_id

    async def subscribe_all(
        self,
        handler: Callable[[Event], Any],
        filter_fn: Optional[Callable[[Event], bool]] = None,
        subscription_id: Optional[str] = None,
    ) -> str:
        """
        Subscribe to all events.

        Args:
            handler: Handler function (async or sync)
            filter_fn: Optional filter function
            subscription_id: Optional custom subscription ID

        Returns:
            Subscription ID for unsubscribing
        """
        subscription = EventSubscription(
            event_type=EventType.EXECUTION_STARTED,  # Placeholder
            handler=handler,
            filter_fn=filter_fn,
            subscription_id=subscription_id,
        )

        async with self._lock:
            self._global_subscriptions.append(subscription)

        logger.info(
            f"Subscribed to all events (id={subscription.subscription_id})"
        )

        return subscription.subscription_id

    async def unsubscribe(self, subscription_id: str) -> bool:
        """
        Unsubscribe from events.

        Args:
            subscription_id: Subscription ID to remove

        Returns:
            True if unsubscribed, False if not found
        """
        async with self._lock:
            # Check type-specific subscriptions
            for event_type, subscriptions in self._subscriptions.items():
                for i, sub in enumerate(subscriptions):
                    if sub.subscription_id == subscription_id:
                        subscriptions.pop(i)
                        logger.info(
                            f"Unsubscribed from {event_type.value} "
                            f"(id={subscription_id})"
                        )
                        return True

            # Check global subscriptions
            for i, sub in enumerate(self._global_subscriptions):
                if sub.subscription_id == subscription_id:
                    self._global_subscriptions.pop(i)
                    logger.info(
                        f"Unsubscribed from all events (id={subscription_id})"
                    )
                    return True

        logger.warning(f"Subscription not found: {subscription_id}")
        return False

    async def emit_to_websocket(self, event: Event) -> None:
        """
        Send event to all WebSocket handlers.

        Args:
            event: Event to send
        """
        if not self._websocket_handlers:
            return

        tasks = [handler(event) for handler in self._websocket_handlers]
        await asyncio.gather(*tasks, return_exceptions=True)

    def register_websocket_handler(
        self,
        handler: Callable[[Event], Any]
    ) -> None:
        """
        Register WebSocket handler for events.

        Args:
            handler: Handler function for WebSocket events
        """
        self._websocket_handlers.add(handler)
        logger.info("WebSocket handler registered")

    def unregister_websocket_handler(
        self,
        handler: Callable[[Event], Any]
    ) -> None:
        """
        Unregister WebSocket handler.

        Args:
            handler: Handler to unregister
        """
        self._websocket_handlers.discard(handler)
        logger.info("WebSocket handler unregistered")

    def get_history(
        self,
        event_type: Optional[EventType] = None,
        limit: Optional[int] = None,
        correlation_id: Optional[str] = None,
    ) -> List[Event]:
        """
        Get event history with optional filtering.

        Args:
            event_type: Optional event type filter
            limit: Optional limit on results
            correlation_id: Optional correlation ID filter

        Returns:
            List of events matching criteria
        """
        events = self._history

        # Filter by event type
        if event_type:
            events = [e for e in events if e.event_type == event_type]

        # Filter by correlation ID
        if correlation_id:
            events = [
                e for e in events
                if e.correlation_id == correlation_id
            ]

        # Apply limit
        if limit:
            events = events[-limit:]

        return events

    def get_stats(self) -> Dict[str, Any]:
        """
        Get event bus statistics.

        Returns:
            Dictionary of statistics
        """
        subscription_counts = {
            event_type.value: len(subs)
            for event_type, subs in self._subscriptions.items()
        }

        return {
            "total_events": self._event_count,
            "history_size": len(self._history),
            "subscription_counts": subscription_counts,
            "global_subscriptions": len(self._global_subscriptions),
            "websocket_handlers": len(self._websocket_handlers),
        }

    async def clear_history(self) -> None:
        """Clear event history."""
        async with self._lock:
            self._history.clear()
        logger.info("Event history cleared")

    async def replay_events(
        self,
        events: List[Event],
        delay: float = 0.0,
    ) -> None:
        """
        Replay events to subscribers.

        Args:
            events: Events to replay
            delay: Optional delay between events
        """
        logger.info(f"Replaying {len(events)} events")

        for event in events:
            await self._notify_subscribers(event)
            if delay > 0:
                await asyncio.sleep(delay)

        logger.info("Event replay completed")


# Global event bus instance
_event_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """Get or create global event bus instance."""
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus


def reset_event_bus() -> None:
    """Reset global event bus (for testing)."""
    global _event_bus
    _event_bus = None
