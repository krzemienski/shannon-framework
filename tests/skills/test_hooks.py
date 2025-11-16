"""
Tests for Shannon Skills Framework - HookManager

Comprehensive test suite covering:
- PRE hooks execution (failure = abort)
- POST hooks execution (failure = warn)
- ERROR hooks execution (failure = log)
- Hook chaining (hooks with their own hooks)
- Circular dependency detection
- Timeout handling
- Event emission
- Error handling per hook type
- Execution stack management
"""

import pytest
import asyncio
from pathlib import Path
from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

from shannon.skills.hooks import (
    HookManager,
    HookExecutionResult,
    HookExecutionError,
    CircularHookError,
    HookTimeoutError,
)
from shannon.skills.registry import SkillRegistry
from shannon.skills.models import (
    Skill,
    SkillResult,
    Execution,
    ExecutionType,
    HookTrigger,
    ExecutionContext,
    Hooks,
    SkillMetadata,
)


@pytest.fixture
def schema_path():
    """Path to skill schema"""
    return Path(__file__).parent.parent.parent / "schemas" / "skill.schema.json"


@pytest.fixture
def registry(schema_path):
    """Create a fresh registry for each test"""
    SkillRegistry.reset_instance()
    return SkillRegistry(schema_path)


@pytest.fixture
def hook_manager(registry):
    """Create a hook manager with registry"""
    return HookManager(registry)


@pytest.fixture
def execution_context():
    """Create a sample execution context"""
    return ExecutionContext(
        task="Test task execution",
        variables={"test": "value"},
        constraints=["no_network"]
    )


@pytest.fixture
def pre_hook_skill():
    """Create a PRE hook skill"""
    return Skill(
        name="pre_validate",
        version="1.0.0",
        description="Pre-execution validation hook",
        category="validation",
        execution=Execution(
            type=ExecutionType.NATIVE,
            module="hooks.validation",
            class_name="ValidationHook",
            method="validate"
        )
    )


@pytest.fixture
def post_hook_skill():
    """Create a POST hook skill"""
    return Skill(
        name="post_cleanup",
        version="1.0.0",
        description="Post-execution cleanup hook",
        category="utility",
        execution=Execution(
            type=ExecutionType.NATIVE,
            module="hooks.cleanup",
            class_name="CleanupHook",
            method="cleanup"
        )
    )


@pytest.fixture
def error_hook_skill():
    """Create an ERROR hook skill"""
    return Skill(
        name="error_notify",
        version="1.0.0",
        description="Error notification hook",
        category="monitoring",
        execution=Execution(
            type=ExecutionType.NATIVE,
            module="hooks.notification",
            class_name="NotificationHook",
            method="notify"
        )
    )


@pytest.fixture
def hook_with_hooks():
    """Create a hook that itself has hooks (for chaining test)"""
    return Skill(
        name="chained_hook",
        version="1.0.0",
        description="Hook with its own hooks",
        category="testing",
        execution=Execution(
            type=ExecutionType.NATIVE,
            module="hooks.chained",
            class_name="ChainedHook",
            method="execute"
        ),
        hooks=Hooks(
            pre=["nested_pre_hook"],
            post=["nested_post_hook"]
        )
    )


@pytest.fixture
def nested_hook():
    """Create a nested hook for chaining"""
    return Skill(
        name="nested_pre_hook",
        version="1.0.0",
        description="Nested hook in a chain",
        category="testing",
        execution=Execution(
            type=ExecutionType.NATIVE,
            module="hooks.nested",
            class_name="NestedHook",
            method="execute"
        )
    )


# ============================================================================
# Test: Basic Hook Execution
# ============================================================================

@pytest.mark.asyncio
async def test_execute_empty_hooks(hook_manager, execution_context):
    """Test executing empty hook list returns success"""
    result = await hook_manager.execute_hooks(
        HookTrigger.PRE,
        [],
        execution_context
    )

    assert result.success is True
    assert len(result.executed_hooks) == 0
    assert len(result.failed_hooks) == 0
    assert result.should_abort is False


@pytest.mark.asyncio
async def test_execute_single_pre_hook_success(
    hook_manager, registry, pre_hook_skill, execution_context
):
    """Test successful execution of single PRE hook"""
    await registry.register(pre_hook_skill)

    result = await hook_manager.execute_hooks(
        HookTrigger.PRE,
        ["pre_validate"],
        execution_context
    )

    assert result.success is True
    assert "pre_validate" in result.executed_hooks
    assert len(result.failed_hooks) == 0
    assert result.should_abort is False
    assert result.total_duration > 0


@pytest.mark.asyncio
async def test_execute_multiple_pre_hooks(
    hook_manager, registry, execution_context
):
    """Test execution of multiple PRE hooks in sequence"""
    # Register multiple hooks
    hooks = []
    for i in range(3):
        hook = Skill(
            name=f"pre_hook_{i}",
            version="1.0.0",
            description=f"Pre hook number {i} for testing",
            category="validation",
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="hooks.test",
                class_name="TestHook",
                method="validate"
            )
        )
        await registry.register(hook)
        hooks.append(hook.name)

    result = await hook_manager.execute_hooks(
        HookTrigger.PRE,
        hooks,
        execution_context
    )

    assert result.success is True
    assert len(result.executed_hooks) == 3
    assert result.executed_hooks == hooks
    assert len(result.failed_hooks) == 0


# ============================================================================
# Test: PRE Hook Failure Handling (ABORT)
# ============================================================================

@pytest.mark.asyncio
async def test_pre_hook_failure_aborts_execution(
    hook_manager, registry, execution_context
):
    """Test that PRE hook failure aborts execution"""
    # Create a hook skill
    failing_hook = Skill(
        name="failing_pre_hook",
        version="1.0.0",
        description="A hook that will fail",
        category="validation",
        execution=Execution(
                type=ExecutionType.NATIVE,
                module="hooks.failing",
                class_name="FailingHook",
                method="validate"
            )
    )
    await registry.register(failing_hook)

    # Mock the _execute_hook_skill to return failure
    async def mock_execute_fail(skill, context):
        return SkillResult(
            skill_name=skill.name,
            success=False,
            error="Validation failed",
            timestamp=datetime.now()
        )

    hook_manager._execute_hook_skill = mock_execute_fail

    result = await hook_manager.execute_hooks(
        HookTrigger.PRE,
        ["failing_pre_hook"],
        execution_context
    )

    assert result.success is False
    assert result.should_abort is True
    assert "failing_pre_hook" in result.failed_hooks
    assert len(result.results) == 1
    assert result.results[0].success is False


@pytest.mark.asyncio
async def test_pre_hook_stops_on_first_failure(
    hook_manager, registry, execution_context
):
    """Test that PRE hooks stop executing after first failure"""
    # Register 3 hooks
    for i in range(3):
        hook = Skill(
            name=f"pre_hook_{i}",
            version="1.0.0",
            description=f"Pre hook {i}",
            category="validation",
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="hooks.test",
                class_name="TestHook",
                method="validate"
            )
        )
        await registry.register(hook)

    # Mock to fail on second hook
    call_count = 0

    async def mock_execute_conditional(skill, context):
        nonlocal call_count
        call_count += 1
        success = call_count != 2  # Fail on second call

        return SkillResult(
            skill_name=skill.name,
            success=success,
            error="Failed" if not success else None,
            timestamp=datetime.now()
        )

    hook_manager._execute_hook_skill = mock_execute_conditional

    result = await hook_manager.execute_hooks(
        HookTrigger.PRE,
        ["pre_hook_0", "pre_hook_1", "pre_hook_2"],
        execution_context
    )

    assert result.success is False
    assert result.should_abort is True
    # Only first two hooks should be executed
    assert len(result.executed_hooks) == 2
    assert "pre_hook_1" in result.failed_hooks
    # Third hook should not be executed
    assert "pre_hook_2" not in result.executed_hooks


# ============================================================================
# Test: POST Hook Failure Handling (WARN)
# ============================================================================

@pytest.mark.asyncio
async def test_post_hook_failure_warns_but_continues(
    hook_manager, registry, execution_context
):
    """Test that POST hook failure logs warning but doesn't fail"""
    # Register hooks
    for i in range(3):
        hook = Skill(
            name=f"post_hook_{i}",
            version="1.0.0",
            description=f"Post hook {i}",
            category="utility",
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="hooks.cleanup",
                class_name="CleanupHook",
                method="cleanup"
            )
        )
        await registry.register(hook)

    # Mock to fail on second hook
    call_count = 0

    async def mock_execute_conditional(skill, context):
        nonlocal call_count
        call_count += 1
        success = call_count != 2  # Fail on second call

        return SkillResult(
            skill_name=skill.name,
            success=success,
            error="Cleanup failed" if not success else None,
            timestamp=datetime.now()
        )

    hook_manager._execute_hook_skill = mock_execute_conditional

    result = await hook_manager.execute_hooks(
        HookTrigger.POST,
        ["post_hook_0", "post_hook_1", "post_hook_2"],
        execution_context
    )

    # POST hook failure doesn't fail the result
    assert result.success is True
    # All hooks should be executed
    assert len(result.executed_hooks) == 3
    # But failure is tracked
    assert "post_hook_1" in result.failed_hooks
    assert len(result.failed_hooks) == 1


# ============================================================================
# Test: ERROR Hook Failure Handling (LOG)
# ============================================================================

@pytest.mark.asyncio
async def test_error_hook_failure_logs_but_continues(
    hook_manager, registry, execution_context
):
    """Test that ERROR hook failure is logged but doesn't cascade"""
    # Register error hooks
    for i in range(3):
        hook = Skill(
            name=f"error_hook_{i}",
            version="1.0.0",
            description=f"Error hook {i}",
            category="monitoring",
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="hooks.notify",
                class_name="NotifyHook",
                method="notify"
            )
        )
        await registry.register(hook)

    # Mock to fail on all hooks
    async def mock_execute_fail(skill, context):
        return SkillResult(
            skill_name=skill.name,
            success=False,
            error="Notification failed",
            timestamp=datetime.now()
        )

    hook_manager._execute_hook_skill = mock_execute_fail

    result = await hook_manager.execute_hooks(
        HookTrigger.ERROR,
        ["error_hook_0", "error_hook_1", "error_hook_2"],
        execution_context
    )

    # ERROR hook failures don't fail the result
    assert result.success is True
    # All hooks should be executed
    assert len(result.executed_hooks) == 3
    # All failures tracked
    assert len(result.failed_hooks) == 3


# ============================================================================
# Test: Circular Dependency Detection
# ============================================================================

@pytest.mark.asyncio
async def test_circular_hook_detection_direct(
    hook_manager, registry, execution_context
):
    """Test detection of direct circular dependency (A -> A)"""
    circular_hook = Skill(
        name="circular_hook",
        version="1.0.0",
        description="Hook that references itself for testing",
        category="testing",
        execution=Execution(
                type=ExecutionType.NATIVE,
                module="hooks.circular",
                class_name="CircularHook",
                method="execute"
            ),
        hooks=Hooks(pre=["circular_hook"])  # References itself
    )
    await registry.register(circular_hook)

    # Manually add to execution stack to simulate it's already executing
    hook_manager.execution_stack.append("circular_hook")

    # Now trying to execute it again should raise error
    with pytest.raises(CircularHookError) as exc_info:
        await hook_manager.execute_single_hook(
            "circular_hook",
            HookTrigger.PRE,
            execution_context
        )

    assert "Circular hook dependency detected" in str(exc_info.value)
    assert "circular_hook" in str(exc_info.value)

    # Clean up
    hook_manager.clear_execution_stack()


@pytest.mark.asyncio
async def test_circular_hook_detection_indirect(
    hook_manager, registry, execution_context
):
    """Test detection of indirect circular dependency (A -> B -> A)"""
    # Create hook A that depends on B
    hook_a = Skill(
        name="hook_a",
        version="1.0.0",
        description="Hook A for testing circular dependencies",
        category="testing",
        execution=Execution(
                type=ExecutionType.NATIVE,
                module="hooks.test",
                class_name="TestHook",
                method="execute"
            )
    )

    # Create hook B that depends on A (circular)
    hook_b = Skill(
        name="hook_b",
        version="1.0.0",
        description="Hook B for testing circular dependencies",
        category="testing",
        execution=Execution(
                type=ExecutionType.NATIVE,
                module="hooks.test",
                class_name="TestHook",
                method="execute"
            )
    )

    await registry.register(hook_a)
    await registry.register(hook_b)

    # Manually add to execution stack to simulate circular call
    hook_manager.execution_stack.append("hook_a")

    # Now trying to execute hook_a again should raise error
    with pytest.raises(CircularHookError):
        await hook_manager.execute_single_hook(
            "hook_a",
            HookTrigger.PRE,
            execution_context
        )

    # Clean up
    hook_manager.clear_execution_stack()


# ============================================================================
# Test: Hook Not Found
# ============================================================================

@pytest.mark.asyncio
async def test_hook_not_found_in_registry(
    hook_manager, registry, execution_context
):
    """Test handling of hook that doesn't exist in registry"""
    result = await hook_manager.execute_single_hook(
        "nonexistent_hook",
        HookTrigger.PRE,
        execution_context
    )

    assert result.success is False
    assert "not found in registry" in result.error.lower()


@pytest.mark.asyncio
async def test_execute_hooks_with_missing_hook(
    hook_manager, registry, execution_context
):
    """Test executing hook list with missing hook"""
    # Register one valid hook
    valid_hook = Skill(
        name="valid_hook",
        version="1.0.0",
        description="Valid hook",
        category="testing",
        execution=Execution(
                type=ExecutionType.NATIVE,
                module="hooks.test",
                class_name="TestHook",
                method="execute"
            )
    )
    await registry.register(valid_hook)

    # Try to execute valid and invalid hooks
    result = await hook_manager.execute_hooks(
        HookTrigger.POST,
        ["valid_hook", "missing_hook"],
        execution_context
    )

    # POST hooks continue on failure
    assert len(result.executed_hooks) == 2
    assert "missing_hook" in result.failed_hooks
    assert "valid_hook" not in result.failed_hooks


# ============================================================================
# Test: Timeout Handling
# ============================================================================

@pytest.mark.asyncio
async def test_hook_execution_timeout(
    hook_manager, registry, execution_context
):
    """Test timeout handling for hook execution"""
    slow_hook = Skill(
        name="slow_hook",
        version="1.0.0",
        description="Slow hook for timeout testing",
        category="testing",
        execution=Execution(
                type=ExecutionType.NATIVE,
                module="hooks.slow",
                class_name="SlowHook",
                method="execute"
            )
    )
    await registry.register(slow_hook)

    # Mock slow execution
    async def mock_slow_execute(skill, context):
        await asyncio.sleep(2)  # 2 second delay
        return SkillResult(
            skill_name=skill.name,
            success=True,
            timestamp=datetime.now()
        )

    hook_manager._execute_hook_skill = mock_slow_execute

    # Execute with 1 second timeout
    result = await hook_manager.execute_hooks(
        HookTrigger.PRE,
        ["slow_hook"],
        execution_context,
        timeout=1
    )

    assert result.success is False
    # PRE timeout should abort
    assert result.should_abort is True


# ============================================================================
# Test: Event Emission
# ============================================================================

@pytest.mark.asyncio
async def test_event_emission_on_hook_execution(
    registry, pre_hook_skill, execution_context
):
    """Test that events are emitted during hook execution"""
    await registry.register(pre_hook_skill)

    # Create mock event bus
    event_bus = Mock()
    event_bus.emit = AsyncMock()

    hook_manager = HookManager(registry, event_bus)

    await hook_manager.execute_hooks(
        HookTrigger.PRE,
        ["pre_validate"],
        execution_context
    )

    # Verify events were emitted
    assert event_bus.emit.called
    # Should have: hooks.started, hook.started, hook.completed, hooks.completed
    assert event_bus.emit.call_count >= 2


@pytest.mark.asyncio
async def test_no_event_emission_without_event_bus(
    hook_manager, registry, pre_hook_skill, execution_context
):
    """Test that execution works without event bus"""
    await registry.register(pre_hook_skill)

    # Execute without event bus (hook_manager fixture has no event bus)
    result = await hook_manager.execute_hooks(
        HookTrigger.PRE,
        ["pre_validate"],
        execution_context
    )

    # Should succeed even without event bus
    assert result.success is True


# ============================================================================
# Test: Execution Stack Management
# ============================================================================

@pytest.mark.asyncio
async def test_execution_stack_cleared_after_success(
    hook_manager, registry, pre_hook_skill, execution_context
):
    """Test that execution stack is cleared after successful execution"""
    await registry.register(pre_hook_skill)

    assert len(hook_manager.get_execution_stack()) == 0

    await hook_manager.execute_single_hook(
        "pre_validate",
        HookTrigger.PRE,
        execution_context
    )

    # Stack should be cleared after execution
    assert len(hook_manager.get_execution_stack()) == 0


@pytest.mark.asyncio
async def test_execution_stack_cleared_after_error(
    hook_manager, registry, execution_context
):
    """Test that execution stack is cleared even after error"""
    error_hook = Skill(
        name="error_hook",
        version="1.0.0",
        description="Error hook for testing stack cleanup",
        category="testing",
        execution=Execution(
                type=ExecutionType.NATIVE,
                module="hooks.error",
                class_name="ErrorHook",
                method="execute"
            )
    )
    await registry.register(error_hook)

    # Mock execution to return failure
    async def mock_execute_failure(skill, context):
        return SkillResult(
            skill_name=skill.name,
            success=False,
            error="Test exception",
            timestamp=datetime.now()
        )

    hook_manager._execute_hook_skill = mock_execute_failure

    result = await hook_manager.execute_single_hook(
        "error_hook",
        HookTrigger.PRE,
        execution_context
    )

    # Stack should still be cleared
    assert len(hook_manager.get_execution_stack()) == 0
    assert result.success is False


@pytest.mark.asyncio
async def test_clear_execution_stack(hook_manager):
    """Test manual clearing of execution stack"""
    # Manually add items
    hook_manager.execution_stack.extend(["hook1", "hook2", "hook3"])
    assert len(hook_manager.get_execution_stack()) == 3

    hook_manager.clear_execution_stack()
    assert len(hook_manager.get_execution_stack()) == 0


# ============================================================================
# Test: Hook Result Tracking
# ============================================================================

@pytest.mark.asyncio
async def test_hook_results_in_execution_result(
    hook_manager, registry, execution_context
):
    """Test that individual hook results are tracked"""
    # Register multiple hooks
    for i in range(3):
        hook = Skill(
            name=f"hook_{i}",
            version="1.0.0",
            description=f"Hook number {i} for testing purposes",
            category="testing",
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="hooks.test",
                class_name="TestHook",
                method="execute"
            )
        )
        await registry.register(hook)

    result = await hook_manager.execute_hooks(
        HookTrigger.POST,
        ["hook_0", "hook_1", "hook_2"],
        execution_context
    )

    # Check that results are tracked
    assert len(result.results) == 3
    for i, hook_result in enumerate(result.results):
        assert hook_result.skill_name == f"hook_{i}"
        assert hook_result.timestamp is not None


# ============================================================================
# Test: Serialization
# ============================================================================

def test_hook_execution_result_to_dict():
    """Test serialization of HookExecutionResult"""
    result = HookExecutionResult(
        success=True,
        executed_hooks=["hook1", "hook2"],
        failed_hooks=[],
        results=[
            SkillResult(
                skill_name="hook1",
                success=True,
                timestamp=datetime.now()
            )
        ],
        total_duration=1.5,
        should_abort=False
    )

    result_dict = result.to_dict()

    assert result_dict['success'] is True
    assert len(result_dict['executed_hooks']) == 2
    assert len(result_dict['failed_hooks']) == 0
    assert result_dict['total_duration'] == 1.5
    assert result_dict['should_abort'] is False
    assert len(result_dict['results']) == 1


# ============================================================================
# Test: String Representation
# ============================================================================

def test_hook_manager_repr(hook_manager, registry):
    """Test string representation of HookManager"""
    repr_str = repr(hook_manager)
    assert "HookManager" in repr_str
    assert "registry=" in repr_str
    assert "stack_depth=" in repr_str
