"""
Comprehensive tests for SkillExecutor - Shannon v4.0 Skills Framework

Tests cover:
- Native Python execution (module.class.method)
- Script execution (shell scripts)
- MCP tool execution (placeholder)
- Composite skill orchestration
- Hook integration (pre/post/error)
- Timeout handling
- Retry logic with exponential backoff
- Parameter validation
- Error handling and edge cases
- Event emission
- Checkpoint creation
"""

import pytest
import asyncio
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch

from shannon.skills.executor import (
    SkillExecutor,
    SkillExecutionError,
    ParameterValidationError,
    NativeExecutionError,
    ScriptExecutionError,
    CompositeExecutionError,
)
from shannon.skills.models import (
    Skill,
    ExecutionType,
    Execution,
    Parameter,
    Hooks,
    SkillMetadata,
    ExecutionContext,
    SkillResult,
)
from shannon.skills.registry import SkillRegistry
from shannon.skills.hooks import HookManager


@pytest.fixture
def schema_path(tmp_path):
    """Create a minimal schema file for testing"""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["name", "version", "description", "execution"],
        "properties": {
            "name": {"type": "string"},
            "version": {"type": "string"},
            "description": {"type": "string"},
            "category": {"type": "string"},
            "execution": {"type": "object"}
        }
    }

    schema_file = tmp_path / "skill.schema.json"
    import json
    with open(schema_file, 'w') as f:
        json.dump(schema, f)

    return schema_file


@pytest.fixture
def registry(schema_path):
    """Create test registry"""
    registry = SkillRegistry(schema_path=schema_path)
    return registry


@pytest.fixture
def hook_manager(registry):
    """Create test hook manager"""
    return HookManager(registry=registry)


@pytest.fixture
def executor(registry, hook_manager):
    """Create test executor"""
    return SkillExecutor(
        registry=registry,
        hook_manager=hook_manager
    )


@pytest.fixture
def execution_context():
    """Create test execution context"""
    return ExecutionContext(
        task="Test task",
        variables={'test_var': 'value'}
    )


@pytest.fixture
def sample_native_skill():
    """Create a sample native skill"""
    return Skill(
        name="test_native_skill",
        version="1.0.0",
        description="Test native skill",
        category="testing",
        parameters=[
            Parameter(name="input", type="string", required=True),
            Parameter(name="count", type="integer", required=False, default=1),
        ],
        execution=Execution(
            type=ExecutionType.NATIVE,
            module="tests.skills.test_helpers",
            class_name="TestNativeClass",
            method="execute",
            timeout=30,
            retry=0
        ),
        hooks=Hooks(),
        metadata=SkillMetadata()
    )


@pytest.fixture
def sample_composite_skill():
    """Create a sample composite skill"""
    return Skill(
        name="test_composite_skill",
        version="1.0.0",
        description="Test composite skill",
        category="orchestration",
        parameters=[
            Parameter(name="input", type="string", required=True),
        ],
        execution=Execution(
            type=ExecutionType.COMPOSITE,
            skills=[
                "skill_one",
                {
                    "name": "skill_two",
                    "parameters": {"input": "modified"},
                    "on_failure": "continue"
                },
                "skill_three"
            ],
            timeout=120,
            retry=0
        ),
        hooks=Hooks(),
        metadata=SkillMetadata()
    )


class TestNativeClass:
    """Mock class for native skill testing"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root

    async def execute(self, input: str, count: int = 1):
        """Mock async method"""
        return {
            'input': input,
            'count': count,
            'result': f"Processed {input} x {count}",
            'project_root': str(self.project_root) if self.project_root else None
        }

    def sync_execute(self, input: str):
        """Mock sync method"""
        return {'input': input, 'result': f"Sync processed {input}"}


@pytest.mark.asyncio
class TestSkillExecutorBasics:
    """Test basic executor functionality"""

    async def test_executor_initialization(self, registry, hook_manager):
        """Test executor initializes correctly"""
        executor = SkillExecutor(
            registry=registry,
            hook_manager=hook_manager
        )

        assert executor.registry == registry
        assert executor.hook_manager == hook_manager
        assert executor.event_bus is None
        assert executor.checkpoint_manager is None
        assert executor._execution_count == 0

    async def test_executor_with_optional_components(self, registry, hook_manager):
        """Test executor with event bus and checkpoint manager"""
        mock_event_bus = Mock()
        mock_checkpoint_manager = Mock()

        executor = SkillExecutor(
            registry=registry,
            hook_manager=hook_manager,
            event_bus=mock_event_bus,
            checkpoint_manager=mock_checkpoint_manager
        )

        assert executor.event_bus == mock_event_bus
        assert executor.checkpoint_manager == mock_checkpoint_manager

    async def test_get_statistics(self, executor):
        """Test statistics retrieval"""
        stats = executor.get_statistics()

        assert 'total_executions' in stats
        assert 'registry_skills' in stats
        assert 'has_event_bus' in stats
        assert 'has_checkpoint_manager' in stats
        assert stats['total_executions'] == 0


@pytest.mark.asyncio
class TestParameterValidation:
    """Test parameter validation"""

    async def test_required_parameter_missing(self, executor, sample_native_skill, execution_context):
        """Test error when required parameter is missing"""
        # Remove required parameter
        result = await executor.execute(
            skill=sample_native_skill,
            parameters={},  # Missing 'input'
            context=execution_context
        )

        assert result.success is False
        assert 'Required parameter missing: input' in result.error

    async def test_parameter_type_validation(self, executor, execution_context):
        """Test parameter type validation"""
        skill = Skill(
            name="type_test_skill",
            version="1.0.0",
            description="Test type validation",
            category="testing",
            parameters=[
                Parameter(name="count", type="integer", required=True),
            ],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.skills.test_helpers",
                class_name="TestNativeClass",
                method="execute",
                timeout=30,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        # Pass wrong type
        result = await executor.execute(
            skill=skill,
            parameters={'count': 'not_an_integer'},
            context=execution_context
        )

        assert result.success is False
        assert 'type validation failed' in result.error.lower()

    async def test_parameter_validation_regex(self, executor, execution_context):
        """Test parameter validation with regex"""
        skill = Skill(
            name="regex_test_skill",
            version="1.0.0",
            description="Test regex validation",
            category="testing",
            parameters=[
                Parameter(
                    name="email",
                    type="string",
                    required=True,
                    validation=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                ),
            ],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.skills.test_helpers",
                class_name="TestNativeClass",
                method="execute",
                timeout=30,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        # Invalid email
        result = await executor.execute(
            skill=skill,
            parameters={'email': 'invalid-email'},
            context=execution_context
        )

        assert result.success is False
        assert 'validation' in result.error.lower()


@pytest.mark.asyncio
class TestNativeExecution:
    """Test native Python execution"""

    async def test_native_async_execution(self, executor, registry, execution_context):
        """Test native async method execution"""
        skill = Skill(
            name="native_async_skill",
            version="1.0.0",
            description="Test native async",
            category="testing",
            parameters=[
                Parameter(name="input", type="string", required=True),
            ],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.skills.test_helpers",
                class_name="TestNativeClass",
                method="execute",
                timeout=30,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(skill)

        result = await executor.execute(
            skill=skill,
            parameters={'input': 'test_value'},
            context=execution_context
        )

        assert result.success is True
        assert result.data is not None
        assert result.data['input'] == 'test_value'
        assert 'Processed test_value' in result.data['result']
        assert result.duration > 0

    async def test_native_with_project_root(self, executor, registry, execution_context, tmp_path):
        """Test native execution with project_root parameter"""
        skill = Skill(
            name="native_project_skill",
            version="1.0.0",
            description="Test with project_root",
            category="testing",
            parameters=[
                Parameter(name="input", type="string", required=True),
                Parameter(name="project_root", type="string", required=True),
            ],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.skills.test_helpers",
                class_name="TestNativeClass",
                method="execute",
                timeout=30,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(skill)

        result = await executor.execute(
            skill=skill,
            parameters={
                'input': 'test',
                'project_root': str(tmp_path)
            },
            context=execution_context
        )

        assert result.success is True
        assert result.data['project_root'] == str(tmp_path)

    async def test_native_import_error(self, executor, registry, execution_context):
        """Test native execution with import error"""
        skill = Skill(
            name="import_error_skill",
            version="1.0.0",
            description="Test import error",
            category="testing",
            parameters=[],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="nonexistent.module",
                class_name="NonexistentClass",
                method="execute",
                timeout=30,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(skill)

        result = await executor.execute(
            skill=skill,
            parameters={},
            context=execution_context
        )

        assert result.success is False
        assert 'import' in result.error.lower()


@pytest.mark.asyncio
class TestScriptExecution:
    """Test shell script execution"""

    async def test_script_execution_success(self, executor, registry, execution_context, tmp_path):
        """Test successful script execution"""
        # Create test script
        script_path = tmp_path / "test_script.sh"
        script_path.write_text("#!/bin/bash\necho 'Hello from script'\nexit 0")
        script_path.chmod(0o755)

        skill = Skill(
            name="script_skill",
            version="1.0.0",
            description="Test script",
            category="testing",
            parameters=[],
            execution=Execution(
                type=ExecutionType.SCRIPT,
                script=str(script_path),
                timeout=30,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(skill)

        result = await executor.execute(
            skill=skill,
            parameters={},
            context=execution_context
        )

        assert result.success is True
        assert 'Hello from script' in result.data['stdout']
        assert result.data['return_code'] == 0

    async def test_script_execution_failure(self, executor, registry, execution_context, tmp_path):
        """Test script execution with non-zero exit code"""
        # Create failing script
        script_path = tmp_path / "failing_script.sh"
        script_path.write_text("#!/bin/bash\necho 'Error message' >&2\nexit 1")
        script_path.chmod(0o755)

        skill = Skill(
            name="failing_script_skill",
            version="1.0.0",
            description="Test failing script",
            category="testing",
            parameters=[],
            execution=Execution(
                type=ExecutionType.SCRIPT,
                script=str(script_path),
                timeout=30,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(skill)

        result = await executor.execute(
            skill=skill,
            parameters={},
            context=execution_context
        )

        assert result.success is False
        assert 'exited with code 1' in result.error


@pytest.mark.asyncio
class TestMCPExecution:
    """Test MCP tool execution"""

    async def test_mcp_execution_placeholder(self, executor, registry, execution_context):
        """Test MCP execution (placeholder)"""
        skill = Skill(
            name="mcp_skill",
            version="1.0.0",
            description="Test MCP",
            category="testing",
            parameters=[
                Parameter(name="query", type="string", required=True),
            ],
            execution=Execution(
                type=ExecutionType.MCP,
                mcp_server="test_server",
                mcp_tool="test_tool",
                timeout=30,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(skill)

        result = await executor.execute(
            skill=skill,
            parameters={'query': 'test query'},
            context=execution_context
        )

        # Placeholder should succeed
        assert result.success is True
        assert result.data['mcp_server'] == 'test_server'
        assert result.data['mcp_tool'] == 'test_tool'


@pytest.mark.asyncio
class TestCompositeExecution:
    """Test composite skill orchestration"""

    async def test_composite_simple_success(self, executor, registry, execution_context):
        """Test composite skill with all sub-skills succeeding"""
        # Register sub-skills
        sub_skill_1 = Skill(
            name="sub_skill_1",
            version="1.0.0",
            description="Sub skill 1",
            category="testing",
            parameters=[Parameter(name="input", type="string", required=True)],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.skills.test_helpers",
                class_name="TestNativeClass",
                method="execute",
                timeout=30,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        sub_skill_2 = Skill(
            name="sub_skill_2",
            version="1.0.0",
            description="Sub skill 2",
            category="testing",
            parameters=[Parameter(name="input", type="string", required=True)],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.skills.test_helpers",
                class_name="TestNativeClass",
                method="execute",
                timeout=30,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(sub_skill_1)
        await registry.register(sub_skill_2)

        # Create composite skill
        composite = Skill(
            name="composite_skill",
            version="1.0.0",
            description="Test composite",
            category="orchestration",
            parameters=[Parameter(name="input", type="string", required=True)],
            execution=Execution(
                type=ExecutionType.COMPOSITE,
                skills=["sub_skill_1", "sub_skill_2"],
                timeout=120,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(composite)

        result = await executor.execute(
            skill=composite,
            parameters={'input': 'test'},
            context=execution_context
        )

        assert result.success is True
        assert result.data['total_skills'] == 2
        assert result.data['successful_skills'] == 2
        assert len(result.data['results']) == 2

    async def test_composite_with_failure_halt(self, executor, registry, execution_context):
        """Test composite with failure and halt directive"""
        # Register sub-skill that will fail
        failing_skill = Skill(
            name="failing_skill",
            version="1.0.0",
            description="Failing skill",
            category="testing",
            parameters=[],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="nonexistent.module",
                class_name="Nonexistent",
                method="execute",
                timeout=30,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        success_skill = Skill(
            name="success_skill",
            version="1.0.0",
            description="Success skill",
            category="testing",
            parameters=[],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.skills.test_helpers",
                class_name="TestNativeClass",
                method="execute",
                timeout=30,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(failing_skill)
        await registry.register(success_skill)

        # Composite with halt on failure
        composite = Skill(
            name="composite_halt",
            version="1.0.0",
            description="Test halt on failure",
            category="orchestration",
            parameters=[],
            execution=Execution(
                type=ExecutionType.COMPOSITE,
                skills=[
                    {"name": "failing_skill", "on_failure": "halt"},
                    "success_skill"  # Should not execute
                ],
                timeout=120,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(composite)

        result = await executor.execute(
            skill=composite,
            parameters={},
            context=execution_context
        )

        # Should have results from only first skill
        assert len(result.data['results']) == 1
        assert result.data['failed_skills'] == ['failing_skill']


@pytest.mark.asyncio
class TestHookIntegration:
    """Test hook integration"""

    async def test_pre_hook_success(self, executor, registry, hook_manager, execution_context):
        """Test pre-hook execution"""
        # Register pre-hook skill
        pre_hook_skill = Skill(
            name="pre_hook_skill",
            version="1.0.0",
            description="Pre-hook",
            category="testing",
            parameters=[],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.skills.test_helpers",
                class_name="TestNativeClass",
                method="execute",
                timeout=30,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(pre_hook_skill)

        # Main skill with pre-hook
        main_skill = Skill(
            name="main_with_pre_hook",
            version="1.0.0",
            description="Main skill",
            category="testing",
            parameters=[Parameter(name="input", type="string", required=True)],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.skills.test_helpers",
                class_name="TestNativeClass",
                method="execute",
                timeout=30,
                retry=0
            ),
            hooks=Hooks(pre=["pre_hook_skill"]),
            metadata=SkillMetadata()
        )

        await registry.register(main_skill)

        result = await executor.execute(
            skill=main_skill,
            parameters={'input': 'test'},
            context=execution_context
        )

        assert result.success is True
        assert result.hooks_executed['pre'] is True

    async def test_pre_hook_failure_aborts(self, executor, registry, execution_context):
        """Test that pre-hook failure aborts execution"""
        # Register failing pre-hook using FailingNativeClass
        failing_hook = Skill(
            name="failing_pre_hook",
            version="1.0.0",
            description="Failing hook",
            category="testing",
            parameters=[],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.skills.test_helpers",
                class_name="FailingNativeClass",
                method="execute",
                timeout=30,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(failing_hook)

        # Main skill with failing pre-hook
        main_skill = Skill(
            name="main_with_failing_pre_hook",
            version="1.0.0",
            description="Main skill",
            category="testing",
            parameters=[Parameter(name="input", type="string", required=False)],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.skills.test_helpers",
                class_name="TestNativeClass",
                method="execute",
                timeout=30,
                retry=0
            ),
            hooks=Hooks(pre=["failing_pre_hook"]),
            metadata=SkillMetadata()
        )

        await registry.register(main_skill)

        result = await executor.execute(
            skill=main_skill,
            parameters={},
            context=execution_context
        )

        # Execution should be aborted due to pre-hook failure
        assert result.success is False
        assert 'pre-hook' in result.error.lower() or 'failed' in result.error.lower()


@pytest.mark.asyncio
class TestTimeoutHandling:
    """Test timeout handling"""

    async def test_execution_timeout(self, executor, registry, execution_context):
        """Test that execution times out correctly"""
        # Create a skill that will timeout
        skill = Skill(
            name="timeout_skill",
            version="1.0.0",
            description="Timeout test",
            category="testing",
            parameters=[],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.skills.test_helpers",
                class_name="SlowNativeClass",
                method="slow_execute",
                timeout=1,  # 1 second timeout
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(skill)

        result = await executor.execute(
            skill=skill,
            parameters={},
            context=execution_context
        )

        assert result.success is False
        assert 'timed out' in result.error.lower() or 'timeout' in result.error.lower()


@pytest.mark.asyncio
class TestRetryLogic:
    """Test retry logic"""

    async def test_retry_on_failure(self, executor, registry, execution_context):
        """Test that execution retries on failure"""
        attempt_count = 0

        async def failing_then_succeeding(*args, **kwargs):
            nonlocal attempt_count
            attempt_count += 1

            if attempt_count < 2:
                # First attempt fails
                raise Exception("Simulated failure")
            else:
                # Second attempt succeeds
                return SkillResult(
                    skill_name="retry_test",
                    success=True,
                    data={'attempt': attempt_count},
                    timestamp=datetime.now()
                )

        skill = Skill(
            name="retry_test_skill",
            version="1.0.0",
            description="Retry test",
            category="testing",
            parameters=[],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.skills.test_helpers",
                class_name="TestNativeClass",
                method="execute",
                timeout=30,
                retry=2  # 2 retries = 3 total attempts
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(skill)

        # Patch executor to use our failing function
        with patch.object(
            executor, '_execute_by_type',
            side_effect=failing_then_succeeding
        ):
            result = await executor.execute(
                skill=skill,
                parameters={},
                context=execution_context
            )

            assert result.success is True
            assert attempt_count == 2  # Should have tried twice

    async def test_all_retries_exhausted(self, executor, registry, execution_context):
        """Test behavior when all retries are exhausted"""
        attempt_count = 0

        async def always_failing(*args, **kwargs):
            nonlocal attempt_count
            attempt_count += 1
            raise Exception(f"Attempt {attempt_count} failed")

        skill = Skill(
            name="always_fail_skill",
            version="1.0.0",
            description="Always fails",
            category="testing",
            parameters=[],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.skills.test_helpers",
                class_name="TestNativeClass",
                method="execute",
                timeout=30,
                retry=2  # 3 total attempts
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(skill)

        with patch.object(
            executor, '_execute_by_type',
            side_effect=always_failing
        ):
            result = await executor.execute(
                skill=skill,
                parameters={},
                context=execution_context
            )

            assert result.success is False
            assert attempt_count == 3  # Should have tried 3 times


@pytest.mark.asyncio
class TestEventEmission:
    """Test event emission"""

    async def test_events_emitted(self, registry, hook_manager, execution_context):
        """Test that events are emitted during execution"""
        # Create mock event bus
        mock_event_bus = AsyncMock()

        executor = SkillExecutor(
            registry=registry,
            hook_manager=hook_manager,
            event_bus=mock_event_bus
        )

        skill = Skill(
            name="event_test_skill",
            version="1.0.0",
            description="Event test",
            category="testing",
            parameters=[Parameter(name="input", type="string", required=True)],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.skills.test_helpers",
                class_name="TestNativeClass",
                method="execute",
                timeout=30,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(skill)

        await executor.execute(
            skill=skill,
            parameters={'input': 'test'},
            context=execution_context
        )

        # Verify events were emitted
        assert mock_event_bus.emit.call_count > 0 or mock_event_bus.publish.call_count > 0


@pytest.mark.asyncio
class TestContextManagement:
    """Test execution context management"""

    async def test_result_added_to_context(self, executor, registry, execution_context):
        """Test that results are added to context"""
        skill = Skill(
            name="context_test_skill",
            version="1.0.0",
            description="Context test",
            category="testing",
            parameters=[Parameter(name="input", type="string", required=True)],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.skills.test_helpers",
                class_name="TestNativeClass",
                method="execute",
                timeout=30,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(skill)

        initial_results_count = len(execution_context.skill_results)

        await executor.execute(
            skill=skill,
            parameters={'input': 'test'},
            context=execution_context
        )

        # Context should have new result
        assert len(execution_context.skill_results) == initial_results_count + 1
        assert execution_context.skill_results[-1].skill_name == "context_test_skill"


@pytest.mark.asyncio
class TestEdgeCases:
    """Test edge cases and error conditions"""

    async def test_empty_parameters(self, executor, registry, execution_context):
        """Test execution with empty parameters"""
        skill = Skill(
            name="no_param_skill",
            version="1.0.0",
            description="No parameters",
            category="testing",
            parameters=[],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.skills.test_helpers",
                class_name="TestNativeClass",
                method="execute",
                timeout=30,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(skill)

        result = await executor.execute(
            skill=skill,
            parameters={},
            context=execution_context
        )

        assert result.success is True

    async def test_execution_counter_increments(self, executor, registry, execution_context):
        """Test that execution counter increments"""
        skill = Skill(
            name="counter_test_skill",
            version="1.0.0",
            description="Counter test",
            category="testing",
            parameters=[],
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="tests.skills.test_helpers",
                class_name="TestNativeClass",
                method="execute",
                timeout=30,
                retry=0
            ),
            hooks=Hooks(),
            metadata=SkillMetadata()
        )

        await registry.register(skill)

        initial_count = executor._execution_count

        await executor.execute(skill, {}, execution_context)
        await executor.execute(skill, {}, execution_context)

        assert executor._execution_count == initial_count + 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
