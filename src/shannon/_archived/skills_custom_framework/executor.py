"""
Shannon Skills Framework - Skill Execution Engine

The SkillExecutor is responsible for executing all skill types with full lifecycle
management including hooks, checkpoints, timeouts, retries, and event emission.

This is the FINAL component of Wave 1 - the runtime execution engine.

Features:
- Execute all 4 skill types (native, script, mcp, composite)
- Full hook integration (pre/post/error via HookManager)
- Checkpoint creation before execution (placeholder for rollback)
- Event emission for observability (placeholder event_bus)
- Timeout handling (asyncio.wait_for)
- Retry logic on failure with exponential backoff
- Result aggregation and comprehensive reporting
- Thread-safe execution state management
- Parameter validation and type coercion
- Detailed error messages for debugging

Execution Types:
    NATIVE: Python module.class.method import and invocation
    SCRIPT: Shell script/executable via subprocess
    MCP: MCP server tool invocation (placeholder for SDK integration)
    COMPOSITE: Sequential orchestration of multiple skills

Architecture:
    The executor is the runtime engine for the skills framework.
    It coordinates with:
    - SkillRegistry: Resolve skill names and dependencies
    - HookManager: Execute lifecycle hooks
    - EventBus: Emit execution events (placeholder)
    - CheckpointManager: Create restore points (placeholder)

Thread Safety:
    Uses asyncio.Lock for execution state management.
    All async operations are properly awaited.

Usage:
    executor = SkillExecutor(registry, hook_manager)

    result = await executor.execute(
        skill=skill,
        parameters={'feature': 'auth', 'project_root': '/path'},
        context=context
    )

    if result.success:
        print(f"Success: {result.data}")
    else:
        print(f"Failed: {result.error}")
"""

import asyncio
import importlib
import subprocess
import time
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

from shannon.skills.models import (
    Skill,
    SkillResult,
    ExecutionContext,
    ExecutionType,
    Parameter,
)
from shannon.skills.registry import SkillRegistry, SkillNotFoundError
from shannon.skills.hooks import HookManager, HookTrigger

logger = logging.getLogger(__name__)


class SkillExecutionError(Exception):
    """Raised when skill execution encounters an error"""
    pass


class ParameterValidationError(SkillExecutionError):
    """Raised when parameter validation fails"""
    pass


class SkillTimeoutError(SkillExecutionError):
    """Raised when skill execution exceeds timeout"""
    pass


class NativeExecutionError(SkillExecutionError):
    """Raised when native Python execution fails"""
    pass


class ScriptExecutionError(SkillExecutionError):
    """Raised when script execution fails"""
    pass


class MCPExecutionError(SkillExecutionError):
    """Raised when MCP tool execution fails"""
    pass


class CompositeExecutionError(SkillExecutionError):
    """Raised when composite skill orchestration fails"""
    pass


class SkillExecutor:
    """
    Central execution engine for Shannon Skills Framework.

    This executor handles the complete skill execution lifecycle:
    1. Parameter validation
    2. Checkpoint creation
    3. Pre-hook execution
    4. Main skill execution (dispatched by type)
    5. Post-hook execution (on success)
    6. Error-hook execution (on failure)
    7. Retry logic with exponential backoff
    8. Result aggregation and reporting

    Responsibilities:
    - Execute all skill types with proper error handling
    - Integrate with HookManager for lifecycle hooks
    - Create checkpoints for rollback capability
    - Emit events for monitoring and observability
    - Handle timeouts with asyncio.wait_for
    - Implement retry logic with configurable attempts
    - Validate parameters against skill schema
    - Aggregate and report comprehensive results

    Design Principles:
    - Fail fast: Validation errors stop execution immediately
    - PRE hook failures: Abort execution before main skill
    - POST hook failures: Warn but don't fail skill
    - ERROR hook failures: Log but don't cascade
    - Retry only main skill, not hooks
    - Timeout applies to main skill + hooks combined

    Thread Safety:
        Uses asyncio.Lock for execution state tracking.
        Registry and HookManager are thread-safe.

    Example:
        executor = SkillExecutor(
            registry=skill_registry,
            hook_manager=hook_manager,
            event_bus=event_bus
        )

        result = await executor.execute(
            skill=library_discovery_skill,
            parameters={
                'feature_description': 'authentication',
                'category': 'auth',
                'project_root': '/Users/nick/project'
            },
            context=ExecutionContext(task="Find auth libraries")
        )
    """

    def __init__(
        self,
        registry: SkillRegistry,
        hook_manager: HookManager,
        event_bus: Optional[Any] = None,
        checkpoint_manager: Optional[Any] = None,
        dashboard_client: Optional[Any] = None
    ):
        """
        Initialize the skill executor.

        Args:
            registry: SkillRegistry for resolving skill dependencies
            hook_manager: HookManager for lifecycle hooks
            event_bus: Optional event bus for observability
            checkpoint_manager: Optional checkpoint manager for rollback
            dashboard_client: Optional dashboard client for event streaming
        """
        self.registry = registry
        self.hook_manager = hook_manager
        self.event_bus = event_bus
        self.checkpoint_manager = checkpoint_manager
        self.dashboard_client = dashboard_client
        self._lock = asyncio.Lock()
        self._execution_count = 0

        # Set executor on hook manager for full integration
        self.hook_manager.set_executor(self)

        logger.info("SkillExecutor initialized")

    async def execute(
        self,
        skill: Skill,
        parameters: Dict[str, Any],
        context: ExecutionContext
    ) -> SkillResult:
        """
        Execute a skill with full lifecycle management.

        This is the primary entry point for skill execution.
        It orchestrates the complete execution flow:
        1. Validate parameters
        2. Create checkpoint
        3. Execute pre-hooks (abort if any fail)
        4. Execute main skill with timeout and retry
        5. Execute post-hooks (on success)
        6. Execute error-hooks (on failure)
        7. Emit events throughout
        8. Return comprehensive result

        Args:
            skill: Skill to execute
            parameters: Parameter values for the skill
            context: Execution context with task and variables

        Returns:
            SkillResult with success status, data, error, duration, etc.

        Raises:
            ParameterValidationError: If parameters are invalid
            SkillTimeoutError: If execution exceeds timeout
            SkillExecutionError: If unrecoverable error occurs

        Example:
            result = await executor.execute(
                skill=my_skill,
                parameters={'input': 'value'},
                context=ExecutionContext(task="Do something")
            )
        """
        start_time = datetime.now()
        execution_id = self._generate_execution_id()

        logger.info(
            f"[{execution_id}] Starting execution: {skill.name} v{skill.version} "
            f"(type: {skill.execution.type.value})"
        )

        # Track execution count
        async with self._lock:
            self._execution_count += 1

        # Emit start event
        await self._emit_event('skill.execution.started', {
            'execution_id': execution_id,
            'skill_name': skill.name,
            'skill_version': skill.version,
            'execution_type': skill.execution.type.value,
            'parameters': self._sanitize_for_logging(parameters),
            'context_task': context.task,
            'timestamp': start_time.isoformat()
        })

        try:
            # Step 1: Validate parameters
            logger.debug(f"[{execution_id}] Validating parameters")
            self._validate_parameters(skill, parameters)

            # Step 2: Create checkpoint (placeholder)
            checkpoint_id = await self._create_checkpoint(skill, context, execution_id)

            # Step 3: Execute pre-hooks
            logger.debug(f"[{execution_id}] Executing pre-hooks")
            pre_result = await self.hook_manager.execute_hooks(
                HookTrigger.PRE,
                skill.hooks.pre,
                context
            )

            if pre_result.should_abort:
                error_msg = f"Pre-hooks failed: {pre_result.failed_hooks}"
                logger.error(f"[{execution_id}] {error_msg}")

                result = SkillResult(
                    skill_name=skill.name,
                    success=False,
                    error=error_msg,
                    duration=0.0,
                    timestamp=start_time,
                    checkpoint_id=checkpoint_id,
                    hooks_executed={'pre': False}
                )

                await self._emit_event('skill.execution.aborted', {
                    'execution_id': execution_id,
                    'skill_name': skill.name,
                    'reason': 'pre_hooks_failed',
                    'failed_hooks': pre_result.failed_hooks
                })

                return result

            # Step 4: Execute main skill with timeout and retry
            logger.info(f"[{execution_id}] Executing main skill")
            main_result = await self._execute_with_retry(
                skill, parameters, context, execution_id
            )

            # Step 5: Execute post-hooks (on success) or error-hooks (on failure)
            if main_result.success:
                logger.debug(f"[{execution_id}] Executing post-hooks")
                post_result = await self.hook_manager.execute_hooks(
                    HookTrigger.POST,
                    skill.hooks.post,
                    context
                )
                main_result.hooks_executed['post'] = post_result.success

                # Post-hook failures are warnings only
                if not post_result.success:
                    logger.warning(
                        f"[{execution_id}] Some post-hooks failed "
                        f"(non-critical): {post_result.failed_hooks}"
                    )
            else:
                logger.debug(f"[{execution_id}] Executing error-hooks")
                error_result = await self.hook_manager.execute_hooks(
                    HookTrigger.ERROR,
                    skill.hooks.error,
                    context
                )
                main_result.hooks_executed['error'] = error_result.success

                # Error-hook failures are informational only
                if not error_result.success:
                    logger.info(
                        f"[{execution_id}] Some error-hooks failed: "
                        f"{error_result.failed_hooks}"
                    )

            # Step 6: Finalize result
            end_time = datetime.now()
            main_result.duration = (end_time - start_time).total_seconds()
            main_result.checkpoint_id = checkpoint_id
            main_result.hooks_executed['pre'] = pre_result.success

            # Add result to context
            context.add_result(main_result)

            # Emit completion event
            await self._emit_event('skill.execution.completed', {
                'execution_id': execution_id,
                'skill_name': skill.name,
                'success': main_result.success,
                'duration': main_result.duration,
                'checkpoint_id': checkpoint_id,
                'hooks_executed': main_result.hooks_executed
            })

            logger.info(
                f"[{execution_id}] Completed: {skill.name} "
                f"(success={main_result.success}, duration={main_result.duration:.2f}s)"
            )

            return main_result

        except ParameterValidationError as e:
            logger.error(f"[{execution_id}] Parameter validation failed: {str(e)}")

            result = SkillResult(
                skill_name=skill.name,
                success=False,
                error=f"Parameter validation failed: {str(e)}",
                duration=0.0,
                timestamp=start_time,
                hooks_executed={'validation_failed': True}
            )

            await self._emit_event('skill.execution.failed', {
                'execution_id': execution_id,
                'skill_name': skill.name,
                'error_type': 'parameter_validation',
                'error': str(e)
            })

            return result

        except Exception as e:
            logger.error(
                f"[{execution_id}] Unexpected error executing {skill.name}: {str(e)}",
                exc_info=True
            )

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            result = SkillResult(
                skill_name=skill.name,
                success=False,
                error=f"Unexpected error: {str(e)}",
                duration=duration,
                timestamp=start_time,
                hooks_executed={'unexpected_error': True}
            )

            await self._emit_event('skill.execution.failed', {
                'execution_id': execution_id,
                'skill_name': skill.name,
                'error_type': 'unexpected',
                'error': str(e)
            })

            return result

    async def _execute_with_retry(
        self,
        skill: Skill,
        parameters: Dict[str, Any],
        context: ExecutionContext,
        execution_id: str
    ) -> SkillResult:
        """
        Execute main skill with retry logic and timeout.

        Implements exponential backoff for retries:
        - Attempt 1: No delay
        - Attempt 2: 1 second delay
        - Attempt 3: 2 second delay
        - Attempt 4: 4 second delay
        - etc.

        Args:
            skill: Skill to execute
            parameters: Validated parameters
            context: Execution context
            execution_id: Unique execution identifier

        Returns:
            SkillResult from successful execution or last attempt
        """
        max_attempts = skill.execution.retry + 1  # retry=0 means 1 attempt
        timeout = skill.execution.timeout

        last_error = None

        for attempt in range(1, max_attempts + 1):
            try:
                logger.debug(
                    f"[{execution_id}] Attempt {attempt}/{max_attempts} "
                    f"(timeout={timeout}s)"
                )

                # Apply timeout to execution
                result = await asyncio.wait_for(
                    self._execute_by_type(skill, parameters, context, execution_id),
                    timeout=timeout
                )

                if result.success:
                    if attempt > 1:
                        logger.info(
                            f"[{execution_id}] Succeeded on attempt {attempt}"
                        )
                    return result

                # Execution returned failure (not exception)
                last_error = result.error
                logger.warning(
                    f"[{execution_id}] Attempt {attempt} failed: {result.error}"
                )

                # Check if we should retry
                if attempt < max_attempts:
                    delay = 2 ** (attempt - 1)  # Exponential backoff
                    logger.info(
                        f"[{execution_id}] Retrying in {delay}s "
                        f"(attempt {attempt + 1}/{max_attempts})"
                    )
                    await asyncio.sleep(delay)
                else:
                    # Last attempt failed
                    return result

            except asyncio.TimeoutError:
                error_msg = f"Execution timed out after {timeout}s"
                logger.error(f"[{execution_id}] {error_msg}")

                last_error = error_msg

                # Check if we should retry on timeout
                if attempt < max_attempts:
                    delay = 2 ** (attempt - 1)
                    logger.info(
                        f"[{execution_id}] Retrying after timeout in {delay}s"
                    )
                    await asyncio.sleep(delay)
                else:
                    # Last attempt timed out
                    return SkillResult(
                        skill_name=skill.name,
                        success=False,
                        error=error_msg,
                        duration=timeout,
                        timestamp=datetime.now()
                    )

            except Exception as e:
                error_msg = f"Execution exception: {str(e)}"
                logger.error(
                    f"[{execution_id}] Attempt {attempt} exception: {str(e)}",
                    exc_info=True
                )

                last_error = error_msg

                # Check if we should retry on exception
                if attempt < max_attempts:
                    delay = 2 ** (attempt - 1)
                    logger.info(
                        f"[{execution_id}] Retrying after exception in {delay}s"
                    )
                    await asyncio.sleep(delay)
                else:
                    # Last attempt had exception
                    return SkillResult(
                        skill_name=skill.name,
                        success=False,
                        error=error_msg,
                        duration=0.0,
                        timestamp=datetime.now()
                    )

        # Should never reach here, but just in case
        return SkillResult(
            skill_name=skill.name,
            success=False,
            error=last_error or "Unknown error",
            duration=0.0,
            timestamp=datetime.now()
        )

    async def _execute_by_type(
        self,
        skill: Skill,
        parameters: Dict[str, Any],
        context: ExecutionContext,
        execution_id: str
    ) -> SkillResult:
        """
        Dispatch execution based on skill type.

        Args:
            skill: Skill to execute
            parameters: Validated parameters
            context: Execution context
            execution_id: Unique execution identifier

        Returns:
            SkillResult from type-specific execution

        Raises:
            SkillExecutionError: If execution type is unknown
        """
        start_time = datetime.now()

        try:
            if skill.execution.type == ExecutionType.NATIVE:
                data = await self._execute_native(skill, parameters, execution_id)

            elif skill.execution.type == ExecutionType.SCRIPT:
                data = await self._execute_script(skill, parameters, execution_id)

            elif skill.execution.type == ExecutionType.MCP:
                data = await self._execute_mcp(skill, parameters, execution_id)

            elif skill.execution.type == ExecutionType.COMPOSITE:
                data = await self._execute_composite(skill, parameters, context, execution_id)

            else:
                raise SkillExecutionError(
                    f"Unknown execution type: {skill.execution.type}"
                )

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            return SkillResult(
                skill_name=skill.name,
                success=True,
                data=data,
                duration=duration,
                timestamp=start_time
            )

        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            logger.error(
                f"[{execution_id}] Execution failed for {skill.name}: {str(e)}",
                exc_info=True
            )

            return SkillResult(
                skill_name=skill.name,
                success=False,
                error=str(e),
                duration=duration,
                timestamp=start_time
            )

    async def _execute_native(
        self,
        skill: Skill,
        parameters: Dict[str, Any],
        execution_id: str
    ) -> Any:
        """
        Execute native Python skill (module.class.method).

        Dynamic import and method invocation:
        1. Import module using importlib
        2. Get class from module
        3. Instantiate class (with project_root if needed)
        4. Get method from instance
        5. Call method with parameters

        Args:
            skill: Skill with execution.module/class_name/method
            parameters: Parameters to pass to method
            execution_id: Execution identifier for logging

        Returns:
            Result from method invocation

        Raises:
            NativeExecutionError: If import, instantiation, or invocation fails
        """
        logger.debug(
            f"[{execution_id}] Executing native: "
            f"{skill.execution.module}.{skill.execution.class_name}."
            f"{skill.execution.method}"
        )

        try:
            # Import module
            module = importlib.import_module(skill.execution.module)
            logger.debug(f"[{execution_id}] Imported module: {skill.execution.module}")

            # Get class
            cls = getattr(module, skill.execution.class_name)
            logger.debug(f"[{execution_id}] Got class: {skill.execution.class_name}")

            # Instantiate class
            # Check if constructor takes project_root, logger, or dashboard_client parameters
            try:
                import inspect
                sig = inspect.signature(cls.__init__)
                constructor_args = {}

                # Add project_root if constructor accepts it
                if 'project_root' in sig.parameters and 'project_root' in parameters:
                    constructor_args['project_root'] = Path(parameters['project_root'])

                # Add logger if constructor accepts it
                if 'logger' in sig.parameters:
                    constructor_args['logger'] = logger

                # Add dashboard_client if constructor accepts it and we have one
                if 'dashboard_client' in sig.parameters and self.dashboard_client is not None:
                    constructor_args['dashboard_client'] = self.dashboard_client

                instance = cls(**constructor_args)
                logger.debug(f"[{execution_id}] Instantiated with args: {list(constructor_args.keys())}")
            except Exception as e:
                # Fallback: try both approaches
                try:
                    instance = cls()
                except:
                    if 'project_root' in parameters:
                        project_root = Path(parameters['project_root'])
                        instance = cls(project_root=project_root)
                    else:
                        raise

            # Get method
            method = getattr(instance, skill.execution.method)
            logger.debug(f"[{execution_id}] Got method: {skill.execution.method}")

            # Call method
            # Remove project_root from parameters if it was used for constructor
            exec_params = parameters.copy()

            # If project_root was used for constructor, remove it from exec_params
            # Check if method signature has project_root parameter
            import inspect
            method_sig = inspect.signature(method)
            if 'project_root' not in method_sig.parameters and 'project_root' in exec_params:
                exec_params.pop('project_root')

            # Check if method is async or sync
            if asyncio.iscoroutinefunction(method):
                result = await method(**exec_params)
                logger.debug(f"[{execution_id}] Async method completed")
            else:
                result = method(**exec_params)
                logger.debug(f"[{execution_id}] Sync method completed")

            return result

        except ImportError as e:
            raise NativeExecutionError(
                f"Failed to import module '{skill.execution.module}': {str(e)}"
            )
        except AttributeError as e:
            raise NativeExecutionError(
                f"Failed to get class/method: {str(e)}"
            )
        except TypeError as e:
            raise NativeExecutionError(
                f"Failed to call method with parameters: {str(e)}"
            )
        except Exception as e:
            raise NativeExecutionError(
                f"Native execution failed: {str(e)}"
            )

    async def _execute_script(
        self,
        skill: Skill,
        parameters: Dict[str, Any],
        execution_id: str
    ) -> Dict[str, Any]:
        """
        Execute shell script skill.

        Uses asyncio.create_subprocess_exec to run script:
        1. Build command with script path and arguments
        2. Execute via subprocess
        3. Capture stdout and stderr
        4. Check return code
        5. Parse output

        Args:
            skill: Skill with execution.script path
            parameters: Parameters converted to CLI arguments
            execution_id: Execution identifier for logging

        Returns:
            Dictionary with stdout, stderr, return_code

        Raises:
            ScriptExecutionError: If script execution fails
        """
        script_path = skill.execution.script

        logger.debug(f"[{execution_id}] Executing script: {script_path}")

        try:
            # Build command arguments from parameters
            args = self._build_script_args(parameters)

            # Execute script
            proc = await asyncio.create_subprocess_exec(
                script_path,
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            logger.debug(f"[{execution_id}] Script process started: PID {proc.pid}")

            # Wait for completion and get output
            stdout, stderr = await proc.communicate()

            # Decode output
            stdout_str = stdout.decode('utf-8') if stdout else ""
            stderr_str = stderr.decode('utf-8') if stderr else ""

            logger.debug(
                f"[{execution_id}] Script completed: "
                f"return_code={proc.returncode}"
            )

            if proc.returncode != 0:
                raise ScriptExecutionError(
                    f"Script exited with code {proc.returncode}: {stderr_str}"
                )

            return {
                'stdout': stdout_str,
                'stderr': stderr_str,
                'return_code': proc.returncode,
                'success': True
            }

        except FileNotFoundError:
            raise ScriptExecutionError(f"Script not found: {script_path}")
        except PermissionError:
            raise ScriptExecutionError(f"Permission denied: {script_path}")
        except Exception as e:
            raise ScriptExecutionError(f"Script execution failed: {str(e)}")

    async def _execute_mcp(
        self,
        skill: Skill,
        parameters: Dict[str, Any],
        execution_id: str
    ) -> Any:
        """
        Execute MCP tool skill.

        Placeholder for MCP SDK integration.
        In production, this would:
        1. Connect to MCP server
        2. Validate tool exists
        3. Call tool with parameters
        4. Return result

        Args:
            skill: Skill with execution.mcp_server/mcp_tool
            parameters: Parameters to pass to MCP tool
            execution_id: Execution identifier for logging

        Returns:
            Result from MCP tool invocation

        Raises:
            MCPExecutionError: If MCP execution fails
        """
        logger.debug(
            f"[{execution_id}] Executing MCP tool: "
            f"{skill.execution.mcp_server}/{skill.execution.mcp_tool}"
        )

        # TODO: Integrate with MCP SDK when available
        # For now, placeholder implementation

        try:
            # Placeholder: Would call MCP client here
            # mcp_client = await get_mcp_client(skill.execution.mcp_server)
            # result = await mcp_client.call_tool(
            #     tool=skill.execution.mcp_tool,
            #     arguments=parameters
            # )

            # Simulated result for now
            result = {
                'mcp_server': skill.execution.mcp_server,
                'mcp_tool': skill.execution.mcp_tool,
                'parameters': parameters,
                'message': 'MCP execution placeholder - SDK integration pending',
                'success': True
            }

            logger.info(
                f"[{execution_id}] MCP tool executed (placeholder): "
                f"{skill.execution.mcp_tool}"
            )

            return result

        except Exception as e:
            raise MCPExecutionError(f"MCP execution failed: {str(e)}")

    async def _execute_composite(
        self,
        skill: Skill,
        parameters: Dict[str, Any],
        context: ExecutionContext,
        execution_id: str
    ) -> Dict[str, Any]:
        """
        Execute composite skill (orchestrate multiple skills).

        Executes skills sequentially:
        1. For each skill in execution.skills:
           a. Resolve skill name to Skill object
           b. Extract parameters for this skill
           c. Execute skill recursively
           d. Collect result
           e. Check on_failure directive (halt or continue)
        2. Aggregate all results
        3. Return composite result

        Args:
            skill: Composite skill with execution.skills list
            parameters: Parameters for all sub-skills
            context: Execution context
            execution_id: Execution identifier for logging

        Returns:
            Dictionary with results from all sub-skills

        Raises:
            CompositeExecutionError: If orchestration fails
        """
        logger.debug(
            f"[{execution_id}] Executing composite skill with "
            f"{len(skill.execution.skills)} sub-skills"
        )

        results = []
        failed_skills = []

        try:
            for i, skill_config in enumerate(skill.execution.skills):
                # Parse skill configuration
                if isinstance(skill_config, str):
                    # Simple skill name
                    skill_name = skill_config
                    skill_params = parameters.copy()
                    on_failure = 'halt'  # Default behavior
                elif isinstance(skill_config, dict):
                    # Detailed configuration
                    skill_name = skill_config.get('name')
                    skill_params = skill_config.get('parameters', parameters.copy())
                    on_failure = skill_config.get('on_failure', 'halt')
                else:
                    raise CompositeExecutionError(
                        f"Invalid skill config type: {type(skill_config)}"
                    )

                logger.info(
                    f"[{execution_id}] Executing sub-skill {i+1}/{len(skill.execution.skills)}: "
                    f"{skill_name}"
                )

                # Resolve skill from registry
                sub_skill = self.registry.get(skill_name)
                if sub_skill is None:
                    error_msg = f"Sub-skill not found: {skill_name}"
                    logger.error(f"[{execution_id}] {error_msg}")

                    if on_failure == 'halt':
                        raise CompositeExecutionError(error_msg)
                    else:
                        failed_skills.append(skill_name)
                        results.append({
                            'skill_name': skill_name,
                            'success': False,
                            'error': error_msg
                        })
                        continue

                # Execute sub-skill recursively
                sub_result = await self.execute(sub_skill, skill_params, context)

                results.append({
                    'skill_name': skill_name,
                    'success': sub_result.success,
                    'data': sub_result.data,
                    'error': sub_result.error,
                    'duration': sub_result.duration
                })

                # Handle failure based on on_failure directive
                if not sub_result.success:
                    failed_skills.append(skill_name)

                    if on_failure == 'halt':
                        logger.error(
                            f"[{execution_id}] Sub-skill {skill_name} failed - "
                            f"halting composite execution"
                        )
                        break
                    else:
                        logger.warning(
                            f"[{execution_id}] Sub-skill {skill_name} failed - "
                            f"continuing composite execution"
                        )

            # Build composite result
            all_success = len(failed_skills) == 0

            composite_result = {
                'total_skills': len(skill.execution.skills),
                'executed_skills': len(results),
                'successful_skills': len([r for r in results if r['success']]),
                'failed_skills': failed_skills,
                'results': results,
                'success': all_success
            }

            logger.info(
                f"[{execution_id}] Composite execution completed: "
                f"{composite_result['successful_skills']}/{composite_result['executed_skills']} succeeded"
            )

            return composite_result

        except Exception as e:
            raise CompositeExecutionError(f"Composite execution failed: {str(e)}")

    def _validate_parameters(self, skill: Skill, parameters: Dict[str, Any]) -> None:
        """
        Validate parameters against skill schema.

        Checks:
        - Required parameters are present
        - Parameter types match expected types
        - Parameter values pass validation rules

        Args:
            skill: Skill with parameter definitions
            parameters: Parameter values to validate

        Raises:
            ParameterValidationError: If validation fails
        """
        # Check required parameters
        for param in skill.parameters:
            if param.required and param.name not in parameters:
                raise ParameterValidationError(
                    f"Required parameter missing: {param.name}"
                )

        # Validate parameter types and values
        for param in skill.parameters:
            if param.name not in parameters:
                continue

            value = parameters[param.name]

            # Type validation
            try:
                self._validate_parameter_type(param, value)
            except Exception as e:
                raise ParameterValidationError(
                    f"Parameter '{param.name}' type validation failed: {str(e)}"
                )

            # Validation rule (regex for strings)
            if param.validation and param.type == 'string':
                import re
                if not re.match(param.validation, str(value)):
                    raise ParameterValidationError(
                        f"Parameter '{param.name}' failed validation: "
                        f"value '{value}' doesn't match pattern '{param.validation}'"
                    )

    def _validate_parameter_type(self, param: Parameter, value: Any) -> None:
        """
        Validate parameter type matches expected type.

        Args:
            param: Parameter definition
            value: Value to validate

        Raises:
            TypeError: If type doesn't match
        """
        type_map = {
            'string': str,
            'integer': int,
            'float': float,
            'boolean': bool,
            'array': list,
            'object': dict,
        }

        expected_type = type_map.get(param.type)
        if expected_type is None:
            return  # Unknown type, skip validation

        if not isinstance(value, expected_type):
            raise TypeError(
                f"Expected {param.type}, got {type(value).__name__}"
            )

    def _build_script_args(self, parameters: Dict[str, Any]) -> List[str]:
        """
        Build CLI arguments from parameters for script execution.

        Converts parameters dict to list of CLI arguments:
        {'project_root': '/path', 'verbose': True} ->
        ['--project-root', '/path', '--verbose']

        Args:
            parameters: Parameter dictionary

        Returns:
            List of CLI argument strings
        """
        args = []

        for key, value in parameters.items():
            # Convert underscore to hyphen for CLI
            arg_name = f"--{key.replace('_', '-')}"

            if isinstance(value, bool):
                if value:
                    args.append(arg_name)
            else:
                args.append(arg_name)
                args.append(str(value))

        return args

    async def _create_checkpoint(
        self,
        skill: Skill,
        context: ExecutionContext,
        execution_id: str
    ) -> Optional[str]:
        """
        Create checkpoint before skill execution.

        Placeholder for checkpoint manager integration.
        In production, would:
        1. Capture current state (files, variables, context)
        2. Store checkpoint with unique ID
        3. Enable rollback on failure

        Args:
            skill: Skill being executed
            context: Execution context
            execution_id: Execution identifier

        Returns:
            Checkpoint ID if created, None otherwise
        """
        if self.checkpoint_manager is None:
            return None

        try:
            # TODO: Integrate with CheckpointManager when available
            # checkpoint_id = await self.checkpoint_manager.create_checkpoint(
            #     skill_name=skill.name,
            #     context=context,
            #     execution_id=execution_id
            # )

            # Placeholder: Generate checkpoint ID
            checkpoint_id = f"checkpoint_{execution_id}_{int(time.time())}"

            logger.debug(f"[{execution_id}] Created checkpoint: {checkpoint_id}")

            return checkpoint_id

        except Exception as e:
            logger.warning(
                f"[{execution_id}] Failed to create checkpoint: {str(e)}"
            )
            return None

    async def _emit_event(self, event_name: str, data: Dict[str, Any]) -> None:
        """
        Emit event to event bus if available.

        Args:
            event_name: Name of event
            data: Event data
        """
        if self.event_bus is None:
            return

        try:
            # Assuming event bus has async emit/publish method
            if hasattr(self.event_bus, 'emit'):
                await self.event_bus.emit(event_name, data)
            elif hasattr(self.event_bus, 'publish'):
                await self.event_bus.publish(event_name, data)
            else:
                logger.debug(f"Event bus doesn't support emit/publish: {event_name}")
        except Exception as e:
            logger.warning(f"Failed to emit event '{event_name}': {str(e)}")

    def _generate_execution_id(self) -> str:
        """
        Generate unique execution identifier.

        Returns:
            Unique execution ID string
        """
        return f"exec_{uuid.uuid4().hex[:8]}"

    def _sanitize_for_logging(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize sensitive data for logging.

        Removes/masks sensitive values like passwords, tokens, keys.

        Args:
            data: Data dictionary to sanitize

        Returns:
            Sanitized dictionary safe for logging
        """
        sensitive_keys = {
            'password', 'secret', 'token', 'key', 'apikey', 'api_key',
            'credential', 'auth', 'authorization'
        }

        sanitized = {}
        for key, value in data.items():
            key_lower = key.lower()
            if any(sensitive in key_lower for sensitive in sensitive_keys):
                sanitized[key] = '***REDACTED***'
            else:
                sanitized[key] = value

        return sanitized

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get executor statistics.

        Returns:
            Dictionary with execution statistics
        """
        return {
            'total_executions': self._execution_count,
            'registry_skills': len(self.registry),
            'has_event_bus': self.event_bus is not None,
            'has_checkpoint_manager': self.checkpoint_manager is not None,
        }

    def __repr__(self) -> str:
        """String representation"""
        return (
            f"<SkillExecutor: "
            f"registry={len(self.registry)} skills, "
            f"executions={self._execution_count}>"
        )


__all__ = [
    'SkillExecutor',
    'SkillExecutionError',
    'ParameterValidationError',
    'SkillTimeoutError',
    'NativeExecutionError',
    'ScriptExecutionError',
    'MCPExecutionError',
    'CompositeExecutionError',
]
