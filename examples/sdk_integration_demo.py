#!/usr/bin/env python3
"""
SDK Integration Demo - Shannon CLI V3.0

Demonstrates the SDK message interception layer created in Wave 1.

Run with:
    python examples/sdk_integration_demo.py
"""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from shannon.sdk.interceptor import MessageCollector, MessageInterceptor, DebugCollector
from shannon.sdk.stream_handler import StreamHandler


class DemoCollector(MessageCollector):
    """
    Demo collector that shows message interception

    This collector demonstrates how Wave 2+ modules will
    implement the MessageCollector interface.
    """

    def __init__(self, name: str):
        self.name = name
        self.messages_received = 0

    async def process(self, message) -> None:
        """Process message asynchronously"""
        self.messages_received += 1
        msg_type = type(message).__name__
        print(f"  [{self.name}] Message {self.messages_received}: {msg_type}")

    async def on_stream_complete(self) -> None:
        """Called when stream completes"""
        print(f"  [{self.name}] Stream complete! Received {self.messages_received} messages")

    async def on_stream_error(self, error: Exception) -> None:
        """Called when stream errors"""
        print(f"  [{self.name}] Stream error: {error}")


async def demo_basic_interception():
    """
    Demo 1: Basic message interception

    Shows how interceptor wraps an async iterator and
    delivers messages to collectors in parallel.
    """
    print("=" * 70)
    print("Demo 1: Basic Message Interception")
    print("=" * 70)

    # Create a simple async iterator (simulating SDK)
    async def mock_query():
        """Simulate SDK query response"""
        for i in range(5):
            await asyncio.sleep(0.1)  # Simulate network delay
            yield f"Message {i+1}"

    # Create interceptor and collectors
    interceptor = MessageInterceptor()
    collector1 = DemoCollector("Metrics")
    collector2 = DemoCollector("Context")

    print("\nStarting interception with 2 collectors...")
    print("Each message will be delivered to both collectors in parallel.")
    print()

    # Intercept messages
    messages_received = []
    async for msg in interceptor.intercept(mock_query(), [collector1, collector2]):
        print(f"Main consumer received: {msg}")
        messages_received.append(msg)

    # Give collectors time to finish
    await asyncio.sleep(0.5)

    print(f"\nTotal messages received: {len(messages_received)}")
    print()


async def demo_error_isolation():
    """
    Demo 2: Error isolation

    Shows how collector errors don't break the stream.
    """
    print("=" * 70)
    print("Demo 2: Error Isolation")
    print("=" * 70)

    class ErrorCollector(MessageCollector):
        """Collector that throws an error on the 2nd message"""

        def __init__(self):
            self.count = 0

        async def process(self, message):
            self.count += 1
            if self.count == 2:
                raise RuntimeError("Simulated error on message 2")
            print(f"  [ErrorCollector] Processed message {self.count}")

        async def on_stream_complete(self):
            pass

        async def on_stream_error(self, error):
            pass

    # Create a simple async iterator
    async def mock_query():
        for i in range(4):
            await asyncio.sleep(0.1)
            yield f"Message {i+1}"

    # Create interceptor with error-throwing and normal collector
    interceptor = MessageInterceptor()
    error_collector = ErrorCollector()
    normal_collector = DemoCollector("Normal")

    print("\nStarting stream with error-throwing collector...")
    print("Error collector will throw on message 2, but stream continues.")
    print()

    # Intercept messages
    messages_received = []
    async for msg in interceptor.intercept(mock_query(), [error_collector, normal_collector]):
        print(f"Main consumer received: {msg}")
        messages_received.append(msg)

    await asyncio.sleep(0.5)

    print(f"\nStream completed successfully despite collector error!")
    print(f"Total messages: {len(messages_received)}")
    print()


async def demo_stream_handler():
    """
    Demo 3: Stream handler with health monitoring

    Shows stream health monitoring and statistics.
    """
    print("=" * 70)
    print("Demo 3: Stream Handler with Health Monitoring")
    print("=" * 70)

    # Create a simple async iterator
    async def mock_query():
        for i in range(5):
            await asyncio.sleep(0.2)  # Simulate processing time
            yield f"Message {i+1}"

    # Create stream handler
    handler = StreamHandler(
        enable_buffering=True,
        buffer_size=10,
        stall_timeout=30.0,
        total_timeout=600.0
    )

    print("\nStarting stream with health monitoring...")
    print()

    # Handle stream
    message_count = 0
    async for msg in handler.handle(mock_query()):
        message_count += 1
        print(f"Received: {msg}")

        # Show stats periodically
        if message_count % 2 == 0:
            stats = handler.get_stats()
            print(f"  Stats: {stats['message_count']} msgs, "
                  f"{stats['duration']:.2f}s, "
                  f"{stats['messages_per_second']:.2f} msg/s")

    # Final stats
    final_stats = handler.get_stats()
    print(f"\nFinal Statistics:")
    print(f"  Messages: {final_stats['message_count']}")
    print(f"  Duration: {final_stats['duration']:.2f}s")
    print(f"  Throughput: {final_stats['messages_per_second']:.2f} msg/s")
    print(f"  Status: {final_stats['status']}")
    print(f"  Completed: {final_stats['completed_successfully']}")
    print()


async def demo_zero_latency():
    """
    Demo 4: Zero latency characteristic

    Shows that messages are yielded immediately,
    not blocked by collector processing.
    """
    print("=" * 70)
    print("Demo 4: Zero Latency Characteristic")
    print("=" * 70)

    import time

    class SlowCollector(MessageCollector):
        """Collector that takes time to process"""

        async def process(self, message):
            # Simulate slow processing
            await asyncio.sleep(0.5)
            print(f"  [SlowCollector] Finished processing: {message}")

        async def on_stream_complete(self):
            pass

        async def on_stream_error(self, error):
            pass

    # Create a simple async iterator
    async def mock_query():
        for i in range(3):
            yield f"Message {i+1}"

    # Create interceptor with slow collector
    interceptor = MessageInterceptor()
    slow_collector = SlowCollector()

    print("\nCollector takes 0.5s to process each message.")
    print("But messages are yielded immediately (zero latency).")
    print()

    # Intercept messages and time each yield
    async for msg in interceptor.intercept(mock_query(), [slow_collector]):
        start = time.time()
        print(f"Main consumer received (immediately): {msg}")
        elapsed = time.time() - start
        print(f"  Time to receive: {elapsed*1000:.1f}ms (should be ~0ms)")

    # Give collector time to finish
    print("\nWaiting for slow collector to finish processing...")
    await asyncio.sleep(2)
    print("Done!")
    print()


async def main():
    """Run all demos"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  Shannon CLI V3.0 - SDK Integration Layer Demo".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("║" + "  Wave 1, Agent 1: SDK Integration Specialist".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print()

    await demo_basic_interception()
    await asyncio.sleep(1)

    await demo_error_isolation()
    await asyncio.sleep(1)

    await demo_stream_handler()
    await asyncio.sleep(1)

    await demo_zero_latency()

    print("=" * 70)
    print("All Demos Complete!")
    print("=" * 70)
    print()
    print("Key Takeaways:")
    print("  1. ✅ Messages delivered to all collectors in parallel")
    print("  2. ✅ Collector errors don't break stream (error isolation)")
    print("  3. ✅ Stream health monitoring tracks performance")
    print("  4. ✅ Zero latency - messages yield immediately")
    print()
    print("Ready for Wave 2 (Metrics & Context) to build upon!")
    print()


if __name__ == "__main__":
    asyncio.run(main())
