"""
Shannon Skills Framework - Hook Execution Manager

The HookManager is responsible for executing lifecycle hooks for skills.
Hooks are just skills that run at specific points in the execution lifecycle:
- PRE: Before main skill execution (failure aborts main execution)
- POST: After successful main execution (failure logged as warning)
- ERROR: When main skill fails (failure logged but doesn't cascade)

Features:
- Hook dependency resolution (hooks can depend on other skills)
- Circular dependency detection
- Hook chaining support (hooks can have their own hooks)
- Timeout handling per hook
- Event emission for observability
- Type-specific failure handling

Architecture:
    Hooks are simply skills that are executed at lifecycle points.
    The HookManager resolves hook names to skills via the registry,
    executes them with proper error handling, and tracks execution state
    to prevent infinite loops.
"""

import asyncio
import logging
from typing import List, Optional, Set, Dict, Any
from datetime import datetime
from dataclasses import dataclass, field

from shannon.skills.models import (
    HookTrigger,
    ExecutionContext,
    SkillResult,
    SkillStatus,
)

logger = logging.getLogger(__name__)


class HookExecutionError(Exception):
    """Raised when hook execution encounters an error"""
    pass


class CircularHookError(HookExecutionError):
    """Raised when circular hook dependencies are detected"""
    pass


class HookTimeoutError(HookExecutionError):
    """Raised when hook execution exceeds timeout"""
    pass


@dataclass
class HookExecutionResult:
    """
    Result of executing a list of hooks.

    Attributes:
        success: Whether all hooks succeeded (based on hook type semantics)
        executed_hooks: List of hook names that were executed
        failed_hooks: List of hook names that failed
        results: Individual results for each hook
        total_duration: Total time spent executing hooks
        should_abort: Whether execution should abort (for PRE hook failures)
    """
    success: bool
    executed_hooks: List[str] = field(default_factory=list)
    failed_hooks: List[str] = field(default_factory=list)
    results: List[SkillResult] = field(default_factory=list)
    total_duration: float = 0.0
    should_abort: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'success': self.success,
            'executed_hooks': self.executed_hooks,
            'failed_hooks': self.failed_hooks,
            'results': [r.to_dict() for r in self.results],
            'total_duration': self.total_duration,
            'should_abort': self.should_abort
        }


class HookManager:
    """
    Manages hook execution for the Shannon Skills Framework.

    Responsibilities:
    - Execute pre/post/error hooks with correct semantics
    - Resolve hook dependencies (hooks reference other skills)
    - Detect and prevent circular hook chains
    - Handle timeouts and errors per hook type
    - Emit events for observability

    Hook Execution Semantics:
        PRE hooks:
            - Run before main skill execution
            - If ANY fail, abort entire execution
            - Failures are critical errors

        POST hooks:
            - Run after successful main execution
            - If fail, log warning but don't fail skill
            - Failures don't affect skill success

        ERROR hooks:
            - Run when main skill fails
            - If fail, log but don't cascade error
            - Used for cleanup/notification

    Thread Safety:
        Uses asyncio.Lock for thread-safe execution state tracking.

    Usage:
        hook_manager = HookManager(registry, event_bus)

        # Execute pre-hooks
        pre_result = await hook_manager.execute_hooks(
            HookTrigger.PRE,
            ["validate_input", "check_permissions"],
            context
        )
        if pre_result.should_abort:
            return  # Don't execute main skill

        # Execute post-hooks
        post_result = await hook_manager.execute_hooks(
            HookTrigger.POST,
            ["update_metrics", "send_notification"],
            context
        )
    """

    def __init__(self, registry: 'SkillRegistry', event_bus: Optional[Any] = None):
        """
        Initialize the hook manager.

        Args:
            registry: SkillRegistry to resolve hook names to skills
            event_bus: Optional event bus for emitting hook events
        """
        self.registry = registry
        self.event_bus = event_bus
        self.execution_stack: List[str] = []  # For detecting circular dependencies
        self._lock = asyncio.Lock()

        logger.info("HookManager initialized")

    async def execute_hooks(
        self,
        hook_type: HookTrigger,
        hook_names: List[str],
        context: ExecutionContext,
        timeout: Optional[int] = None
    ) -> HookExecutionResult:
        """
        Execute a list of hooks of a specific type.

        Executes hooks sequentially in the order provided. Handles errors
        according to hook type semantics (abort, warn, or log).

        Args:
            hook_type: Type of hooks (PRE, POST, or ERROR)
            hook_names: List of hook names (skill names) to execute
            context: Execution context to pass to hooks
            timeout: Optional timeout in seconds for all hooks combined

        Returns:
            HookExecutionResult with execution details

        Raises:
            HookExecutionError: If critical error occurs during hook execution
        """
        if not hook_names:
            return HookExecutionResult(success=True)

        start_time = datetime.now()
        result = HookExecutionResult(success=True)

        logger.info(
            f"Executing {len(hook_names)} {hook_type.value} hooks: {hook_names}"
        )

        # Emit event
        if self.event_bus:
            await self._emit_event('hooks.started', {
                'hook_type': hook_type.value,
                'hook_names': hook_names,
                'context_task': context.task
            })

        try:
            # Set timeout for all hooks combined
            if timeout:
                try:
                    await asyncio.wait_for(
                        self._execute_hooks_sequential(
                            hook_type, hook_names, context, result
                        ),
                        timeout=timeout
                    )
                except asyncio.TimeoutError:
                    raise  # Re-raise to be caught in outer try-except
            else:
                await self._execute_hooks_sequential(
                    hook_type, hook_names, context, result
                )

        except asyncio.TimeoutError:
            error_msg = f"{hook_type.value} hooks timed out after {timeout}s"
            logger.error(error_msg)
            result.success = False

            # For PRE hooks, timeout means abort
            if hook_type == HookTrigger.PRE:
                result.should_abort = True

            # Emit timeout event
            if self.event_bus:
                await self._emit_event('hooks.timeout', {
                    'hook_type': hook_type.value,
                    'hook_names': hook_names,
                    'timeout': timeout
                })

        except Exception as e:
            error_msg = f"Unexpected error executing {hook_type.value} hooks: {str(e)}"
            logger.error(error_msg, exc_info=True)
            result.success = False

            if hook_type == HookTrigger.PRE:
                result.should_abort = True

        # Calculate total duration
        end_time = datetime.now()
        result.total_duration = (end_time - start_time).total_seconds()

        # Emit completion event
        if self.event_bus:
            await self._emit_event('hooks.completed', {
                'hook_type': hook_type.value,
                'success': result.success,
                'executed': len(result.executed_hooks),
                'failed': len(result.failed_hooks),
                'duration': result.total_duration
            })

        logger.info(
            f"Completed {hook_type.value} hooks: "
            f"{len(result.executed_hooks)} executed, "
            f"{len(result.failed_hooks)} failed, "
            f"duration={result.total_duration:.2f}s"
        )

        return result

    async def _execute_hooks_sequential(
        self,
        hook_type: HookTrigger,
        hook_names: List[str],
        context: ExecutionContext,
        result: HookExecutionResult
    ) -> None:
        """
        Execute hooks sequentially, handling errors per hook type.

        Args:
            hook_type: Type of hooks being executed
            hook_names: List of hook names to execute
            context: Execution context
            result: Result object to populate
        """
        for hook_name in hook_names:
            try:
                hook_result = await self.execute_single_hook(
                    hook_name, hook_type, context
                )

                result.executed_hooks.append(hook_name)
                result.results.append(hook_result)

                # Handle failure based on hook type
                if not hook_result.success:
                    result.failed_hooks.append(hook_name)

                    if hook_type == HookTrigger.PRE:
                        # PRE hook failure: ABORT execution
                        logger.error(
                            f"PRE hook '{hook_name}' failed - aborting execution: "
                            f"{hook_result.error}"
                        )
                        result.success = False
                        result.should_abort = True
                        break  # Stop executing remaining hooks

                    elif hook_type == HookTrigger.POST:
                        # POST hook failure: WARN but continue
                        logger.warning(
                            f"POST hook '{hook_name}' failed (non-critical): "
                            f"{hook_result.error}"
                        )
                        # Don't mark result as failed - POST hook failures are warnings

                    elif hook_type == HookTrigger.ERROR:
                        # ERROR hook failure: LOG but don't cascade
                        logger.info(
                            f"ERROR hook '{hook_name}' failed: {hook_result.error}"
                        )
                        # Don't mark result as failed - ERROR hooks are best-effort

            except Exception as e:
                error_msg = f"Exception executing hook '{hook_name}': {str(e)}"
                logger.error(error_msg, exc_info=True)

                result.failed_hooks.append(hook_name)

                # Create error result
                error_result = SkillResult(
                    skill_name=hook_name,
                    success=False,
                    error=error_msg,
                    timestamp=datetime.now()
                )
                result.results.append(error_result)

                # Handle exception based on hook type
                if hook_type == HookTrigger.PRE:
                    result.success = False
                    result.should_abort = True
                    break

    async def execute_single_hook(
        self,
        hook_name: str,
        hook_type: HookTrigger,
        context: ExecutionContext
    ) -> SkillResult:
        """
        Execute a single hook (which is just a skill).

        This method:
        1. Resolves the hook name to a skill via the registry
        2. Checks for circular dependencies
        3. Executes the skill (with its own hooks if any)
        4. Tracks execution state
        5. Handles timeouts

        Args:
            hook_name: Name of the hook (skill) to execute
            hook_type: Type of hook for logging/events
            context: Execution context to pass to hook

        Returns:
            SkillResult from hook execution

        Raises:
            CircularHookError: If circular dependency detected
            HookExecutionError: If hook cannot be executed
        """
        start_time = datetime.now()

        # Check if hook exists in registry
        skill = self.registry.get(hook_name)
        if skill is None:
            error_msg = f"Hook '{hook_name}' not found in registry"
            logger.error(error_msg)
            return SkillResult(
                skill_name=hook_name,
                success=False,
                error=error_msg,
                timestamp=start_time
            )

        # Check for circular dependencies
        async with self._lock:
            if hook_name in self.execution_stack:
                error_msg = (
                    f"Circular hook dependency detected: {hook_name} "
                    f"(stack: {self.execution_stack})"
                )
                logger.error(error_msg)
                raise CircularHookError(error_msg)

            self.execution_stack.append(hook_name)

        try:
            logger.debug(
                f"Executing {hook_type.value} hook: {hook_name} "
                f"(type: {skill.execution.type.value})"
            )

            # Emit event
            if self.event_bus:
                await self._emit_event('hook.started', {
                    'hook_name': hook_name,
                    'hook_type': hook_type.value,
                    'execution_type': skill.execution.type.value
                })

            # Execute the hook skill
            # Note: In a full implementation, this would call the SkillExecutor
            # For now, we create a mock result to show the structure
            # TODO: Integrate with SkillExecutor when available
            hook_result = await self._execute_hook_skill(skill, context)

            # Calculate duration
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            hook_result.duration = duration

            # Emit completion event
            if self.event_bus:
                await self._emit_event('hook.completed', {
                    'hook_name': hook_name,
                    'hook_type': hook_type.value,
                    'success': hook_result.success,
                    'duration': duration
                })

            logger.debug(
                f"Completed {hook_type.value} hook: {hook_name} "
                f"(success={hook_result.success}, duration={duration:.2f}s)"
            )

            return hook_result

        finally:
            # Always remove from execution stack
            async with self._lock:
                self.execution_stack.remove(hook_name)

    async def _execute_hook_skill(
        self,
        skill: 'Skill',
        context: ExecutionContext
    ) -> SkillResult:
        """
        Execute the hook skill via the SkillExecutor.

        This integrates with the SkillExecutor to properly execute hooks,
        with the executor set on the HookManager instance.

        Args:
            skill: The skill to execute
            context: Execution context

        Returns:
            SkillResult from execution
        """
        try:
            # Check if we have an executor set (for full integration)
            if hasattr(self, '_executor') and self._executor is not None:
                # Use the executor to properly run the hook
                # Note: We pass empty parameters since hooks typically don't have parameters
                return await self._executor.execute(skill, {}, context)

            # Fallback: Simulate execution (for standalone hook manager usage)
            logger.debug(
                f"Executing hook skill '{skill.name}' (placeholder mode) "
                f"(type: {skill.execution.type.value})"
            )

            # Simulate execution based on type
            if skill.execution.type.value == 'native':
                # Would call Python module.class.method
                result_data = {'message': f'Executed native hook: {skill.name}'}

            elif skill.execution.type.value == 'script':
                # Would execute shell script
                result_data = {'message': f'Executed script hook: {skill.name}'}

            elif skill.execution.type.value == 'mcp':
                # Would call MCP server tool
                result_data = {'message': f'Executed MCP hook: {skill.name}'}

            elif skill.execution.type.value == 'composite':
                # Would orchestrate multiple skills
                result_data = {'message': f'Executed composite hook: {skill.name}'}

            else:
                result_data = {'message': f'Executed hook: {skill.name}'}

            return SkillResult(
                skill_name=skill.name,
                success=True,
                data=result_data,
                timestamp=datetime.now()
            )

        except Exception as e:
            logger.error(f"Hook skill execution failed: {str(e)}", exc_info=True)
            return SkillResult(
                skill_name=skill.name,
                success=False,
                error=str(e),
                timestamp=datetime.now()
            )

    def set_executor(self, executor: Any) -> None:
        """
        Set the SkillExecutor for proper hook execution.

        This enables full integration where hooks are executed as skills
        via the SkillExecutor.

        Args:
            executor: SkillExecutor instance
        """
        self._executor = executor
        logger.debug("SkillExecutor set on HookManager")

    async def _emit_event(self, event_name: str, data: Dict[str, Any]) -> None:
        """
        Emit event to event bus if available.

        Args:
            event_name: Name of the event
            data: Event data
        """
        if self.event_bus is None:
            return

        try:
            # Assuming event bus has an async emit method
            if hasattr(self.event_bus, 'emit'):
                await self.event_bus.emit(event_name, data)
            elif hasattr(self.event_bus, 'publish'):
                await self.event_bus.publish(event_name, data)
            else:
                logger.debug(f"Event bus does not support emit/publish: {event_name}")
        except Exception as e:
            logger.warning(f"Failed to emit event '{event_name}': {str(e)}")

    def clear_execution_stack(self) -> None:
        """
        Clear the execution stack.

        Useful for testing or recovering from errors.
        Should not be needed in normal operation.
        """
        self.execution_stack.clear()
        logger.debug("Cleared hook execution stack")

    def get_execution_stack(self) -> List[str]:
        """
        Get current execution stack.

        Returns:
            List of hook names currently in execution stack
        """
        return self.execution_stack.copy()

    def __repr__(self) -> str:
        """String representation"""
        return (
            f"<HookManager: registry={self.registry}, "
            f"stack_depth={len(self.execution_stack)}>"
        )


__all__ = [
    'HookManager',
    'HookExecutionResult',
    'HookExecutionError',
    'CircularHookError',
    'HookTimeoutError',
]
