#!/usr/bin/env python3
"""
Agent Control System Demonstration

Shows the agent state tracking, control, and message routing system in action.

Run:
    python demo_agent_control.py
"""

import asyncio
import time
from shannon.agents import (
    AgentStateTracker,
    AgentController,
    MessageRouter
)


async def demo_agent_lifecycle():
    """Demonstrate complete agent lifecycle."""
    print("=" * 70)
    print("SHANNON CLI V3.0 - AGENT CONTROL SYSTEM DEMONSTRATION")
    print("=" * 70)
    print()

    # Create tracker
    print("1. Creating AgentStateTracker...")
    tracker = AgentStateTracker()
    print("   ✓ Tracker created\n")

    # Register agents for Wave 2
    print("2. Registering agents for Wave 2...")
    agents = [
        ("backend-builder", "Build authentication API"),
        ("database-arch", "Design database schema"),
        ("api-designer", "Design REST API endpoints")
    ]

    for agent_type, task in agents:
        agent_id = f"wave-2-{agent_type}"
        tracker.register_agent(
            agent_id=agent_id,
            wave_number=2,
            agent_type=agent_type,
            task_description=task
        )
        print(f"   ✓ Registered: {agent_id}")

    print()

    # Start all agents
    print("3. Starting all agents...")
    for agent_type, _ in agents:
        agent_id = f"wave-2-{agent_type}"
        tracker.mark_started(agent_id)
        print(f"   ✓ Started: {agent_id}")

    print()

    # Simulate agent work
    print("4. Simulating agent work...")
    print()

    # Backend builder makes progress
    print("   Backend builder working...")
    for progress in [20, 40, 60]:
        await asyncio.sleep(0.1)
        tracker.update_progress("wave-2-backend-builder", progress)
        tracker.update_metrics(
            "wave-2-backend-builder",
            cost_delta=0.15,
            tokens_in_delta=200,
            tokens_out_delta=100
        )
        tracker.add_message("wave-2-backend-builder", {"step": progress})
        print(f"   ├─ Progress: {progress}%")

    # Database architect completes quickly
    print("\n   Database architect completing...")
    await asyncio.sleep(0.1)
    tracker.update_progress("wave-2-database-arch", 100)
    tracker.update_metrics(
        "wave-2-database-arch",
        cost_delta=0.85,
        tokens_in_delta=1500,
        tokens_out_delta=800
        )
    tracker.add_file_created("wave-2-database-arch", "src/db/schema.sql")
    tracker.mark_complete("wave-2-database-arch")
    print("   ✓ Completed: database-arch")

    # API designer makes slower progress
    print("\n   API designer working...")
    tracker.update_progress("wave-2-api-designer", 30)
    tracker.update_metrics(
        "wave-2-api-designer",
        cost_delta=0.25,
        tokens_in_delta=300,
        tokens_out_delta=150
    )

    print()

    # Show wave status
    print("5. Wave Status at mid-point:")
    print()

    active_agents = tracker.get_active_agents()
    print(f"   Active agents: {len(active_agents)}")
    for agent in active_agents:
        print(f"   ├─ {agent.agent_id}")
        print(f"   │  ├─ Progress: {agent.progress_percent:.0f}%")
        print(f"   │  ├─ Cost: ${agent.cost_usd:.2f}")
        print(f"   │  └─ Duration: {agent.duration_minutes:.1f} min")

    print()

    # Get wave summary
    summary = tracker.get_wave_summary(2)
    print("   Wave 2 Summary:")
    print(f"   ├─ Total agents: {summary['total_agents']}")
    print(f"   ├─ Active: {summary['active_agents']}")
    print(f"   ├─ Complete: {summary['complete_agents']}")
    print(f"   ├─ Failed: {summary['failed_agents']}")
    print(f"   ├─ Total cost: ${summary['total_cost']:.2f}")
    print(f"   └─ Total tokens: {summary['total_tokens']:,}")

    print()

    # Complete remaining agents
    print("6. Completing remaining agents...")

    # Backend builder completes
    tracker.update_progress("wave-2-backend-builder", 100)
    tracker.add_file_created("wave-2-backend-builder", "src/api/auth.js")
    tracker.add_file_created("wave-2-backend-builder", "src/middleware/jwt.js")
    tracker.mark_complete("wave-2-backend-builder")
    print("   ✓ Completed: backend-builder")

    # API designer completes
    tracker.update_progress("wave-2-api-designer", 100)
    tracker.add_file_created("wave-2-api-designer", "docs/api-spec.md")
    tracker.mark_complete("wave-2-api-designer")
    print("   ✓ Completed: api-designer")

    print()

    # Final wave status
    print("7. Final Wave Status:")
    print()

    summary = tracker.get_wave_summary(2)
    print("   Wave 2 Complete!")
    print(f"   ├─ Total agents: {summary['total_agents']}")
    print(f"   ├─ All complete: {summary['complete_agents']}")
    print(f"   ├─ Total cost: ${summary['total_cost']:.2f}")
    print(f"   ├─ Total tokens: {summary['total_tokens']:,}")
    print(f"   ├─ Files created: {summary['files_created']}")
    print(f"   └─ Duration: {summary['duration_minutes']:.1f} min")

    print()

    # Show created files
    print("8. Files Created:")
    for agent_type, _ in agents:
        agent_id = f"wave-2-{agent_type}"
        state = tracker.get_state(agent_id)
        if state.files_created:
            print(f"   {agent_type}:")
            for file_path in state.files_created:
                print(f"   ├─ {file_path}")

    print()
    print("=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


async def demo_controller():
    """Demonstrate controller operations."""
    print()
    print("=" * 70)
    print("CONTROLLER OPERATIONS DEMONSTRATION")
    print("=" * 70)
    print()

    tracker = AgentStateTracker()
    controller = AgentController(tracker)

    # Register test agent
    agent_id = "test-agent-1"
    tracker.register_agent(
        agent_id=agent_id,
        wave_number=1,
        agent_type="tester",
        task_description="Test controller operations"
    )

    # Test pause/resume
    print("1. Wave Pause/Resume:")
    print(f"   Wave 1 paused: {controller.is_wave_paused(1)}")

    controller.pause_wave(1)
    print(f"   After pause: {controller.is_wave_paused(1)}")

    controller.resume_wave(1)
    print(f"   After resume: {controller.is_wave_paused(1)}")

    print()

    # Test should_start_agent
    print("2. Agent Start Control:")
    print(f"   Should start: {controller.should_start_agent(agent_id)}")

    controller.pause_wave(1)
    print(f"   Should start (paused): {controller.should_start_agent(agent_id)}")

    print()

    # Test wave status
    print("3. Wave Status:")
    tracker.mark_started(agent_id)
    tracker.update_progress(agent_id, 50)
    tracker.update_metrics(agent_id, cost_delta=1.5, tokens_in_delta=1000)

    status = controller.get_wave_status(1)
    print(f"   Summary: {status['summary']}")
    print(f"   Paused: {status['paused']}")
    print(f"   Bottleneck: {status['bottleneck']['agent_id'] if status['bottleneck'] else None}")

    print()
    print("=" * 70)


async def demo_message_router():
    """Demonstrate message routing."""
    print()
    print("=" * 70)
    print("MESSAGE ROUTER DEMONSTRATION")
    print("=" * 70)
    print()

    tracker = AgentStateTracker()
    router = MessageRouter(tracker)

    # Register agents
    print("1. Registering agents with router...")
    agents = ["agent-1", "agent-2", "agent-3"]
    for agent_id in agents:
        tracker.register_agent(
            agent_id=agent_id,
            wave_number=1,
            agent_type="test",
            task_description="Test routing"
        )
        tracker.mark_started(agent_id)
        router.register_agent(agent_id)
        print(f"   ✓ {agent_id}")

    print()

    # Create unified collector
    print("2. Creating unified collector...")
    collector = router.create_collector()
    print("   ✓ Collector created")

    print()

    # Send test messages
    print("3. Routing test messages...")
    test_messages = [
        {"type": "message", "content": "Hello"},
        {"type": "tool", "tool": "read_file"},
        {"type": "message", "content": "Complete"}
    ]

    for i, msg in enumerate(test_messages, 1):
        await collector.process(msg)
        print(f"   ✓ Message {i} routed to all agents")

    print()

    # Verify all agents received messages
    print("4. Verifying message distribution:")
    for agent_id in agents:
        state = tracker.get_state(agent_id)
        print(f"   {agent_id}: {len(state.all_messages)} messages received")

    print()

    # Complete stream
    await collector.on_stream_complete()
    print("5. Stream completed successfully")

    print()
    print("=" * 70)


async def main():
    """Run all demonstrations."""
    await demo_agent_lifecycle()
    await demo_controller()
    await demo_message_router()

    print()
    print("All demonstrations completed successfully!")
    print()


if __name__ == "__main__":
    asyncio.run(main())
