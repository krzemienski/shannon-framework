"""
Shannon Communication Module

Provides event bus and command queue infrastructure for real-time
communication between Shannon components and external interfaces.
"""

from .events import EventBus, EventType, Event
from .command_queue import CommandQueue, CommandType, Command

__all__ = [
    "EventBus",
    "EventType",
    "Event",
    "CommandQueue",
    "CommandType",
    "Command",
]
