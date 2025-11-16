"""
Example integration showing Event Bus and Command Queue usage with WebSocket.

This example demonstrates how the communication components integrate with
Shannon's execution system and WebSocket server.
"""

import asyncio
from typing import Dict, Any

from .events import EventBus, EventType, Event
from .command_queue import CommandQueue, CommandType, Command


class ShannonCommunicationIntegration:
    """
    Example integration of Event Bus and Command Queue.

    This demonstrates how these components would be used in Shannon v4.0
    with the WebSocket server for real-time communication.
    """

    def __init__(self):
        self.event_bus = EventBus()
        self.command_queue = CommandQueue()
        self.execution_paused = False

    async def setup_websocket_integration(self):
        """Set up WebSocket handlers for bidirectional communication."""

        async def websocket_event_handler(event: Event):
            """
            Send events to WebSocket clients.

            In real implementation, this would send JSON over WebSocket:
            await websocket.send_json(event.to_dict())
            """
            print(f"[WebSocket Out] Event: {event.event_type.value}")
            print(f"  Data: {event.data}")

        # Register WebSocket handler
        self.event_bus.register_websocket_handler(websocket_event_handler)

        # Subscribe to all events for logging
        await self.event_bus.subscribe_all(
            self._log_event,
            subscription_id="global_logger"
        )

    async def _log_event(self, event: Event):
        """Log all events."""
        print(f"[Event Log] {event.event_type.value} from {event.source}")

    async def simulate_skill_execution(self):
        """
        Simulate skill execution with event emission.

        This shows how skills would emit events during execution.
        """
        # Skill started
        await self.event_bus.emit(
            event_type=EventType.SKILL_STARTED,
            data={
                "skill_name": "test_skill",
                "args": {"param": "value"},
            },
            source="executor",
            correlation_id="exec-123",
        )

        # Simulate work
        await asyncio.sleep(0.5)

        # Emit progress
        await self.event_bus.emit(
            event_type=EventType.SKILL_PROGRESS,
            data={
                "skill_name": "test_skill",
                "progress": 50,
                "message": "Processing data...",
            },
            source="executor",
            correlation_id="exec-123",
        )

        # Simulate more work
        await asyncio.sleep(0.5)

        # Skill completed
        await self.event_bus.emit(
            event_type=EventType.SKILL_COMPLETED,
            data={
                "skill_name": "test_skill",
                "result": {"status": "success"},
            },
            source="executor",
            correlation_id="exec-123",
        )

    async def handle_incoming_command(self, command_data: Dict[str, Any]):
        """
        Handle command from WebSocket client.

        This would be called when WebSocket receives a command.
        """
        command = await self.command_queue.enqueue(
            command_type=CommandType[command_data["type"]],
            data=command_data.get("data", {}),
            priority=command_data.get("priority", 5),
            source="websocket",
        )

        print(f"[Command In] {command.command_type.value} enqueued")
        return command

    async def process_commands(self):
        """
        Process commands from queue.

        This would run continuously in Shannon's execution loop.
        """
        while True:
            try:
                # Wait for command with timeout
                command = await self.command_queue.dequeue(timeout=1.0)

                print(f"[Command Process] {command.command_type.value}")

                # Process command
                if command.command_type == CommandType.HALT:
                    await self._handle_halt(command)
                elif command.command_type == CommandType.RESUME:
                    await self._handle_resume(command)
                elif command.command_type == CommandType.DECISION:
                    await self._handle_decision(command)
                else:
                    await self._handle_generic_command(command)

            except asyncio.TimeoutError:
                # No command available, continue
                continue
            except Exception as e:
                print(f"Error processing command: {e}")

    async def _handle_halt(self, command: Command):
        """Handle HALT command."""
        self.execution_paused = True

        await self.event_bus.emit(
            event_type=EventType.EXECUTION_HALTED,
            data={
                "reason": command.data.get("reason", "User requested"),
                "command_id": command.command_id,
            },
            source="command_handler",
        )

        await self.command_queue.complete_command(
            command,
            result={"status": "halted"}
        )

    async def _handle_resume(self, command: Command):
        """Handle RESUME command."""
        self.execution_paused = False

        await self.event_bus.emit(
            event_type=EventType.EXECUTION_RESUMED,
            data={"command_id": command.command_id},
            source="command_handler",
        )

        await self.command_queue.complete_command(
            command,
            result={"status": "resumed"}
        )

    async def _handle_decision(self, command: Command):
        """Handle DECISION command (user provides decision at decision point)."""
        decision = command.data.get("decision")

        await self.event_bus.emit(
            event_type=EventType.DECISION_MADE,
            data={
                "decision": decision,
                "command_id": command.command_id,
            },
            source="command_handler",
        )

        await self.command_queue.complete_command(
            command,
            result={"decision": decision}
        )

    async def _handle_generic_command(self, command: Command):
        """Handle other commands."""
        await self.command_queue.complete_command(
            command,
            result={"status": "processed"}
        )


async def main():
    """
    Example usage demonstrating the integration.
    """
    print("=== Shannon Communication Integration Example ===\n")

    integration = ShannonCommunicationIntegration()

    # Setup WebSocket integration
    await integration.setup_websocket_integration()

    # Start command processor in background
    processor_task = asyncio.create_task(integration.process_commands())

    # Simulate skill execution
    print("\n--- Simulating Skill Execution ---\n")
    await integration.simulate_skill_execution()

    await asyncio.sleep(0.5)

    # Simulate incoming commands from WebSocket
    print("\n--- Simulating Incoming Commands ---\n")

    # HALT command
    await integration.handle_incoming_command({
        "type": "HALT",
        "data": {"reason": "User requested pause"},
        "priority": 1,
    })

    await asyncio.sleep(0.5)

    # RESUME command
    await integration.handle_incoming_command({
        "type": "RESUME",
        "data": {},
        "priority": 1,
    })

    await asyncio.sleep(0.5)

    # DECISION command
    await integration.handle_incoming_command({
        "type": "DECISION",
        "data": {"decision": "approve"},
        "priority": 2,
    })

    await asyncio.sleep(1.0)

    # Cancel processor task
    processor_task.cancel()
    try:
        await processor_task
    except asyncio.CancelledError:
        pass

    # Show statistics
    print("\n--- Statistics ---\n")
    print("Event Bus Stats:", integration.event_bus.get_stats())
    print("Command Queue Stats:", integration.command_queue.get_stats())

    print("\n=== Example Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
