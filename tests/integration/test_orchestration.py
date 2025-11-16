"""Integration tests for Shannon Orchestration Layer.

Tests the complete workflow:
1. Parse task
2. Create execution plan
3. Execute skills
4. Create checkpoints
5. Rollback capability

This is the CRITICAL test that validates the entire orchestration layer.
"""

import asyncio
import pytest
from pathlib import Path
from datetime import datetime

from shannon.skills.registry import SkillRegistry
from shannon.skills.executor import SkillExecutor
from shannon.skills.hooks import HookManager
from shannon.skills.dependencies import DependencyResolver
from shannon.skills.models import Skill, ExecutionType, Execution, Parameter
from shannon.orchestration import (
    TaskParser,
    ExecutionPlanner,
    StateManager,
    Orchestrator
)


@pytest.fixture
async def registry():
    """Create registry with test skills"""
    registry = SkillRegistry.get_instance()

    # Register test skills
    skills = [
        Skill(
            name="analysis",
            version="1.0.0",
            description="Analyze code for patterns",
            category="analysis",
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.fixtures.test_skills",
                class_name="AnalysisSkill",
                method="execute"
            )
        ),
        Skill(
            name="code_generation",
            version="1.0.0",
            description="Generate code from requirements",
            category="generation",
            dependencies=["analysis"],  # Depends on analysis
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.fixtures.test_skills",
                class_name="CodeGenSkill",
                method="execute"
            )
        ),
        Skill(
            name="validation",
            version="1.0.0",
            description="Validate generated code",
            category="validation",
            dependencies=["code_generation"],  # Depends on code_generation
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.fixtures.test_skills",
                class_name="ValidationSkill",
                method="execute"
            )
        ),
        Skill(
            name="git_operations",
            version="1.0.0",
            description="Commit changes to git",
            category="git",
            dependencies=["validation"],  # Depends on validation
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.fixtures.test_skills",
                class_name="GitOpsSkill",
                method="execute"
            )
        )
    ]

    for skill in skills:
        await registry.register(skill)

    yield registry

    # Cleanup
    registry._skills.clear()
    registry._by_category.clear()


@pytest.fixture
def project_root(tmp_path):
    """Create temporary project directory"""
    return tmp_path


@pytest.mark.asyncio
async def test_task_parser(registry):
    """Test task parsing extracts correct intent"""
    parser = TaskParser(registry)

    parsed = await parser.parse("create authentication system with JWT")

    assert parsed.raw_task == "create authentication system with JWT"
    assert parsed.intent.goal == "create"
    assert parsed.intent.domain == "authentication"
    assert "jwt" in parsed.intent.keywords
    assert len(parsed.candidate_skills) > 0
    assert parsed.confidence > 0.0


@pytest.mark.asyncio
async def test_execution_planner(registry):
    """Test execution planner creates valid plan"""
    parser = TaskParser(registry)
    resolver = DependencyResolver(registry)
    planner = ExecutionPlanner(registry, resolver)

    # Parse task
    parsed = await parser.parse("create new API endpoint")

    # Create plan
    plan = await planner.create_plan(parsed)

    assert plan.plan_id is not None
    assert plan.task == parsed.raw_task
    assert len(plan.steps) > 0
    assert plan.estimated_duration > 0

    # Verify skills are ordered by dependencies
    skill_names = [step.skill_name for step in plan.steps]
    if "analysis" in skill_names and "code_generation" in skill_names:
        # analysis should come before code_generation
        assert skill_names.index("analysis") < skill_names.index("code_generation")

    # Verify checkpoints are planned
    assert len(plan.checkpoints) > 0


@pytest.mark.asyncio
async def test_state_manager_checkpoint(project_root):
    """Test state manager creates and restores checkpoints"""
    manager = StateManager(project_root)

    # Create test file
    test_file = project_root / "test.txt"
    test_file.write_text("initial content")

    # Track file
    manager.add_tracked_file(test_file)

    # Create checkpoint
    checkpoint1 = await manager.create_checkpoint("initial")

    assert checkpoint1.id is not None
    assert checkpoint1.label == "initial"
    assert len(checkpoint1.file_snapshots) > 0

    # Modify file
    test_file.write_text("modified content")

    # Create another checkpoint
    checkpoint2 = await manager.create_checkpoint("modified")

    # Restore first checkpoint
    await manager.restore_checkpoint(checkpoint1.id)

    # Verify file was restored
    assert test_file.read_text() == "initial content"

    # Verify checkpoint
    is_valid = await manager.verify_checkpoint(checkpoint1.id)
    assert is_valid


@pytest.mark.asyncio
async def test_orchestrator_execution(registry, project_root):
    """Test orchestrator executes plan correctly"""
    # Create components
    hook_manager = HookManager(registry)
    executor = SkillExecutor(registry, hook_manager)
    parser = TaskParser(registry)
    resolver = DependencyResolver(registry)
    planner = ExecutionPlanner(registry, resolver)
    state_manager = StateManager(project_root)

    # Parse and plan
    parsed = await parser.parse("create simple feature")
    plan = await planner.create_plan(parsed)

    # Create orchestrator
    events = []

    async def event_callback(event_type, data, session_id):
        events.append((event_type, data))

    orchestrator = Orchestrator(
        plan=plan,
        executor=executor,
        state_manager=state_manager,
        session_id="test_session",
        event_callback=event_callback
    )

    # Execute
    result = await orchestrator.execute()

    assert result.success
    assert result.steps_completed == len(plan.steps)
    assert len(result.checkpoints_created) > 0
    assert result.duration_seconds > 0

    # Verify events were emitted
    event_types = [e[0] for e in events]
    assert "execution:started" in event_types
    assert "execution:completed" in event_types


@pytest.mark.asyncio
async def test_orchestrator_halt_resume(registry, project_root):
    """Test orchestrator can halt and resume"""
    # Create components
    hook_manager = HookManager(registry)
    executor = SkillExecutor(registry, hook_manager)
    parser = TaskParser(registry)
    resolver = DependencyResolver(registry)
    planner = ExecutionPlanner(registry, resolver)
    state_manager = StateManager(project_root)

    # Parse and plan
    parsed = await parser.parse("test halt resume")
    plan = await planner.create_plan(parsed)

    # Create orchestrator
    orchestrator = Orchestrator(
        plan=plan,
        executor=executor,
        state_manager=state_manager
    )

    # Start execution in background
    exec_task = asyncio.create_task(orchestrator.execute())

    # Wait a bit
    await asyncio.sleep(0.1)

    # Halt execution
    await orchestrator.halt("Test halt")

    assert orchestrator.state == orchestrator.state.__class__.HALTED

    # Resume execution
    await orchestrator.resume()

    # Wait for completion
    result = await exec_task

    assert result.success


@pytest.mark.asyncio
async def test_end_to_end_workflow(registry, project_root):
    """Test complete end-to-end workflow"""
    # This is the CRITICAL test - validates entire orchestration layer

    # STEP 1: Parse task
    parser = TaskParser(registry)
    parsed = await parser.parse("create authentication with JWT tokens")

    assert parsed.intent.goal == "create"
    assert "authentication" in parsed.intent.domain or "auth" in parsed.intent.keywords

    # STEP 2: Create plan
    resolver = DependencyResolver(registry)
    planner = ExecutionPlanner(registry, resolver)
    plan = await planner.create_plan(parsed)

    assert len(plan.steps) > 0
    assert len(plan.checkpoints) > 0

    # STEP 3: Execute with checkpoints
    hook_manager = HookManager(registry)
    executor = SkillExecutor(registry, hook_manager)
    state_manager = StateManager(project_root)

    orchestrator = Orchestrator(
        plan=plan,
        executor=executor,
        state_manager=state_manager
    )

    result = await orchestrator.execute()

    # STEP 4: Verify results
    assert result.success
    assert result.steps_completed == len(plan.steps)
    assert len(result.checkpoints_created) > 0

    # STEP 5: Verify checkpoints can be listed
    checkpoints = await state_manager.list_checkpoints()
    assert len(checkpoints) > 0

    # STEP 6: Verify can rollback
    if checkpoints:
        first_checkpoint = checkpoints[0]
        await state_manager.restore_checkpoint(first_checkpoint.id)

        # Verify checkpoint
        is_valid = await state_manager.verify_checkpoint(first_checkpoint.id)
        assert is_valid


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
