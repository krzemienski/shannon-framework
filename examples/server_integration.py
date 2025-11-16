#!/usr/bin/env python3
"""Shannon Dashboard Server - Integration Example.

This example demonstrates how to integrate the WebSocket server
with Shannon's orchestrator for real-time dashboard updates.

Run the server:
    python run_server.py --reload

Then run this example:
    python examples/server_integration.py
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from shannon.server.websocket import (
    emit_skill_event,
    emit_file_event,
    emit_decision_event,
    emit_validation_event,
    emit_agent_event,
    emit_checkpoint_event,
    emit_execution_event
)


async def simulate_execution_flow():
    """
    Simulate a complete execution flow with real-time events.

    This demonstrates how the orchestrator would emit events
    during skill execution.
    """
    session_id = "demo_session_001"

    print("=" * 70)
    print("Shannon Dashboard Server - Integration Example")
    print("=" * 70)
    print(f"Session ID: {session_id}")
    print()
    print("Simulating execution flow with real-time events...")
    print("Connect dashboard to ws://localhost:8000?session_id=" + session_id)
    print("=" * 70)
    print()

    # 1. Skill Execution Started
    print("1. Starting skill execution...")
    await emit_skill_event('skill:started', {
        'skill_name': 'test_generation_skill',
        'parameters': {
            'test_framework': 'pytest',
            'coverage_target': 95
        }
    }, session_id=session_id)
    await asyncio.sleep(1)

    # 2. File Created
    print("2. Creating test file...")
    await emit_file_event('file:created', {
        'path': '/tests/test_example.py',
        'size': 2048,
        'type': 'test'
    }, session_id=session_id)
    await asyncio.sleep(1)

    # 3. Skill Progress
    print("3. Skill progress update...")
    await emit_skill_event('skill:progress', {
        'skill_name': 'test_generation_skill',
        'progress': 50,
        'message': 'Generated 5 test cases'
    }, session_id=session_id)
    await asyncio.sleep(1)

    # 4. Decision Point
    print("4. Reaching decision point...")
    await emit_decision_event('decision:point', {
        'decision_id': 'decision_001',
        'question': 'Should we add integration tests?',
        'options': ['Yes', 'No', 'Later'],
        'default': 'Yes',
        'timeout': 30
    }, session_id=session_id)
    await asyncio.sleep(2)

    # 5. Decision Made (simulated auto-decision)
    print("5. Decision made automatically...")
    await emit_decision_event('decision:made', {
        'decision_id': 'decision_001',
        'choice': 'Yes',
        'made_by': 'auto',
        'reason': 'Integration tests improve coverage'
    }, session_id=session_id)
    await asyncio.sleep(1)

    # 6. Agent Spawned
    print("6. Spawning validation agent...")
    await emit_agent_event('agent:spawned', {
        'agent_id': 'agent_validator_001',
        'agent_type': 'validator',
        'purpose': 'Validate generated tests'
    }, session_id=session_id)
    await asyncio.sleep(1)

    # 7. Validation Started
    print("7. Starting validation...")
    await emit_validation_event('validation:started', {
        'validation_id': 'val_001',
        'target': '/tests/test_example.py',
        'checks': ['syntax', 'coverage', 'quality']
    }, session_id=session_id)
    await asyncio.sleep(2)

    # 8. Validation Result
    print("8. Validation completed...")
    await emit_validation_event('validation:result', {
        'validation_id': 'val_001',
        'status': 'passed',
        'checks': {
            'syntax': {'passed': True, 'score': 100},
            'coverage': {'passed': True, 'score': 96},
            'quality': {'passed': True, 'score': 92}
        },
        'overall_score': 96
    }, session_id=session_id)
    await asyncio.sleep(1)

    # 9. Agent Completed
    print("9. Validation agent completed...")
    await emit_agent_event('agent:completed', {
        'agent_id': 'agent_validator_001',
        'result': 'success',
        'duration': 3.5
    }, session_id=session_id)
    await asyncio.sleep(1)

    # 10. File Modified
    print("10. Updating test file...")
    await emit_file_event('file:modified', {
        'path': '/tests/test_example.py',
        'changes': 'Added 2 integration tests',
        'lines_changed': 45
    }, session_id=session_id)
    await asyncio.sleep(1)

    # 11. Checkpoint Created
    print("11. Creating checkpoint...")
    await emit_checkpoint_event({
        'checkpoint_id': 'checkpoint_001',
        'description': 'Tests generated and validated',
        'files': ['/tests/test_example.py'],
        'can_rollback': True
    }, session_id=session_id)
    await asyncio.sleep(1)

    # 12. Skill Completed
    print("12. Skill execution completed...")
    await emit_skill_event('skill:completed', {
        'skill_name': 'test_generation_skill',
        'result': {
            'tests_generated': 7,
            'coverage': 96,
            'validation': 'passed'
        },
        'duration': 12.5
    }, session_id=session_id)

    print()
    print("=" * 70)
    print("Execution flow complete!")
    print("=" * 70)


async def simulate_halt_resume():
    """
    Simulate execution halt and resume flow.
    """
    session_id = "demo_session_002"

    print()
    print("=" * 70)
    print("Simulating HALT/RESUME flow...")
    print("=" * 70)
    print()

    # Start execution
    await emit_skill_event('skill:started', {
        'skill_name': 'long_running_skill',
        'parameters': {}
    }, session_id=session_id)
    await asyncio.sleep(1)

    # Halt execution
    print("Halting execution...")
    await emit_execution_event('execution:halted', {
        'reason': 'User requested pause',
        'can_resume': True
    }, session_id=session_id)
    await asyncio.sleep(2)

    # Resume execution
    print("Resuming execution...")
    await emit_execution_event('execution:resumed', {
        'resumed_at': 'checkpoint_001'
    }, session_id=session_id)
    await asyncio.sleep(1)

    # Complete
    await emit_skill_event('skill:completed', {
        'skill_name': 'long_running_skill',
        'result': {'status': 'success'}
    }, session_id=session_id)

    print("HALT/RESUME flow complete!")
    print("=" * 70)


async def main():
    """Run integration examples."""
    try:
        # Simulate full execution flow
        await simulate_execution_flow()

        # Simulate halt/resume
        await simulate_halt_resume()

        print()
        print("✓ All integration examples completed successfully!")
        print()
        print("To see real-time updates:")
        print("1. Start the server: python run_server.py --reload")
        print("2. Connect dashboard to: ws://localhost:8000")
        print("3. Run this example again")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(main())
