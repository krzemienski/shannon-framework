"""
Shannon Framework v4 - Sub-Agent Orchestrator

Coordinates multiple sub-agents with dependency management.
"""

import time
from typing import List, Dict, Optional, Any, Callable
from datetime import datetime
from .models import (
    OrchestrationPlan, OrchestrationResult, AgentTask, AgentResult,
    AgentStatus, OrchestrationStrategy
)
from .dependency import DependencyResolver, CircularDependencyError


class OrchestrationError(Exception):
    """Exception raised during orchestration."""
    pass


class SubAgentOrchestrator:
    """
    Orchestrates multiple sub-agents with dependency management.

    Features:
    - Parallel and sequential execution
    - Dependency resolution
    - Error handling and retries
    - SITREP collection and consolidation
    - Progress tracking
    """

    def __init__(self, agent_executor: Optional[Callable] = None):
        """
        Initialize orchestrator.

        Args:
            agent_executor: Function to execute agent tasks
                           Signature: (task: AgentTask) -> AgentResult
        """
        self.agent_executor = agent_executor or self._default_executor
        self.current_plan: Optional[OrchestrationPlan] = None
        self.current_result: Optional[OrchestrationResult] = None

    def execute_plan(self, plan: OrchestrationPlan) -> OrchestrationResult:
        """
        Execute orchestration plan.

        Args:
            plan: Orchestration plan to execute

        Returns:
            OrchestrationResult with all agent results
        """
        self.current_plan = plan
        self.current_result = OrchestrationResult(
            plan_id=plan.id,
            plan_name=plan.name,
            start_time=datetime.now(),
            total_tasks=len(plan.tasks)
        )

        # Validate plan
        resolver = DependencyResolver(plan)
        errors = resolver.validate()
        if errors:
            self.current_result.errors = errors
            self.current_result.end_time = datetime.now()
            raise OrchestrationError(f"Plan validation failed: {'; '.join(errors)}")

        # Execute based on strategy
        if plan.strategy == OrchestrationStrategy.PARALLEL:
            self._execute_parallel(plan, resolver)
        elif plan.strategy == OrchestrationStrategy.SEQUENTIAL:
            self._execute_sequential(plan, resolver)
        elif plan.strategy == OrchestrationStrategy.DEPENDENCY:
            self._execute_dependency(plan, resolver)
        elif plan.strategy == OrchestrationStrategy.PRIORITY:
            self._execute_priority(plan, resolver)

        # Finalize result
        self.current_result.end_time = datetime.now()
        self.current_result.duration_seconds = (
            self.current_result.end_time - self.current_result.start_time
        ).total_seconds()

        # Calculate statistics
        self._calculate_statistics()

        return self.current_result

    def _execute_parallel(self, plan: OrchestrationPlan, resolver: DependencyResolver):
        """Execute all tasks in parallel (ignoring dependencies)."""
        # Group tasks by max_parallel limit
        groups = []
        for i in range(0, len(plan.tasks), plan.max_parallel):
            groups.append(plan.tasks[i:i + plan.max_parallel])

        for group in groups:
            self._execute_task_group(group, plan)

    def _execute_sequential(self, plan: OrchestrationPlan, resolver: DependencyResolver):
        """Execute tasks one by one in order."""
        for task in plan.tasks:
            result = self._execute_task(task, plan)
            self.current_result.agent_results[task.id] = result

            if plan.fail_fast and result.is_failure():
                self._cancel_remaining_tasks(plan, [task.id])
                break

    def _execute_dependency(self, plan: OrchestrationPlan, resolver: DependencyResolver):
        """Execute tasks respecting dependency graph."""
        # Get execution waves
        waves = resolver.get_execution_waves()

        for wave_tasks in waves:
            # Get actual task objects
            tasks = [plan.get_task(task_id) for task_id in wave_tasks]
            tasks = [t for t in tasks if t is not None]

            # Execute wave in groups
            groups = []
            for i in range(0, len(tasks), plan.max_parallel):
                groups.append(tasks[i:i + plan.max_parallel])

            for group in groups:
                self._execute_task_group(group, plan)

                # Check for failures
                if plan.fail_fast:
                    failed = any(
                        self.current_result.agent_results[t.id].is_failure()
                        for t in group
                        if t.id in self.current_result.agent_results
                    )
                    if failed:
                        completed_ids = set(self.current_result.agent_results.keys())
                        self._cancel_remaining_tasks(plan, completed_ids)
                        return

    def _execute_priority(self, plan: OrchestrationPlan, resolver: DependencyResolver):
        """Execute tasks by priority order."""
        # Sort by priority (descending)
        sorted_tasks = sorted(plan.tasks, key=lambda t: t.priority, reverse=True)

        # Execute in priority order with dependency constraints
        completed = set()

        while len(completed) < len(plan.tasks):
            # Find highest priority tasks with satisfied dependencies
            ready_tasks = []
            for task in sorted_tasks:
                if task.id not in completed:
                    if all(dep in completed for dep in task.dependencies):
                        ready_tasks.append(task)

            if not ready_tasks:
                break

            # Execute ready tasks in groups
            for i in range(0, len(ready_tasks), plan.max_parallel):
                group = ready_tasks[i:i + plan.max_parallel]
                self._execute_task_group(group, plan)
                completed.update(t.id for t in group)

                if plan.fail_fast:
                    failed = any(
                        self.current_result.agent_results[t.id].is_failure()
                        for t in group
                    )
                    if failed:
                        self._cancel_remaining_tasks(plan, completed)
                        return

    def _execute_task_group(self, tasks: List[AgentTask], plan: OrchestrationPlan):
        """
        Execute a group of tasks (simulated parallel execution).

        Args:
            tasks: List of tasks to execute
            plan: Orchestration plan
        """
        # In a real implementation, this would dispatch tasks to actual
        # Claude Code Task tool calls in parallel
        # For now, we execute sequentially but track as if parallel

        results = []
        for task in tasks:
            result = self._execute_task(task, plan)
            results.append(result)
            self.current_result.agent_results[task.id] = result

        return results

    def _execute_task(self, task: AgentTask, plan: OrchestrationPlan) -> AgentResult:
        """
        Execute a single task.

        Args:
            task: Task to execute
            plan: Orchestration plan

        Returns:
            AgentResult
        """
        result = AgentResult(
            agent_id=task.id,
            agent_name=task.name,
            status=AgentStatus.RUNNING,
            start_time=datetime.now()
        )

        # Merge shared context with task context
        context = {**plan.shared_context, **task.context}

        # Execute with retries
        for attempt in range(task.max_retries + 1):
            try:
                # Execute agent
                execution_result = self.agent_executor(task, context)

                # Update result
                result.status = execution_result.get('status', AgentStatus.COMPLETED)
                result.output = execution_result.get('output')
                result.sitrep = execution_result.get('sitrep')
                result.artifacts = execution_result.get('artifacts', {})
                result.metrics = execution_result.get('metrics', {})
                result.error = execution_result.get('error')

                # Mark as completed if no error
                if not result.error:
                    result.status = AgentStatus.COMPLETED
                    break

            except Exception as e:
                result.error = str(e)
                result.retry_count = attempt

                if attempt < task.max_retries:
                    # Retry with exponential backoff
                    time.sleep(2 ** attempt)
                else:
                    result.status = AgentStatus.FAILED

        # Finalize timing
        result.end_time = datetime.now()
        result.duration_seconds = (
            result.end_time - result.start_time
        ).total_seconds()

        # Trigger callbacks
        if task.on_complete and result.is_success():
            try:
                task.on_complete(result)
            except Exception as e:
                print(f"Warning: on_complete callback failed: {e}")

        if task.on_error and result.is_failure():
            try:
                task.on_error(result)
            except Exception as e:
                print(f"Warning: on_error callback failed: {e}")

        return result

    def _cancel_remaining_tasks(self, plan: OrchestrationPlan, completed_ids: set):
        """
        Cancel remaining tasks after failure.

        Args:
            plan: Orchestration plan
            completed_ids: Set of completed task IDs
        """
        for task in plan.tasks:
            if task.id not in completed_ids:
                result = AgentResult(
                    agent_id=task.id,
                    agent_name=task.name,
                    status=AgentStatus.CANCELLED,
                    start_time=datetime.now(),
                    end_time=datetime.now()
                )
                self.current_result.agent_results[task.id] = result
                self.current_result.cancelled_tasks += 1

    def _calculate_statistics(self):
        """Calculate final statistics for orchestration result."""
        for result in self.current_result.agent_results.values():
            if result.status == AgentStatus.COMPLETED:
                self.current_result.completed_tasks += 1
            elif result.is_failure():
                self.current_result.failed_tasks += 1

        # Calculate aggregate metrics
        self.current_result.metrics['total_duration'] = self.current_result.duration_seconds
        self.current_result.metrics['success_rate'] = self.current_result.get_success_rate()

        if self.current_result.agent_results:
            avg_duration = sum(
                r.duration_seconds for r in self.current_result.agent_results.values()
            ) / len(self.current_result.agent_results)
            self.current_result.metrics['avg_agent_duration'] = avg_duration

    def _default_executor(self, task: AgentTask, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Default agent executor (placeholder).

        This should be replaced with actual Task tool integration.

        Args:
            task: Agent task to execute
            context: Execution context

        Returns:
            Execution result dictionary
        """
        # This is a placeholder implementation
        # In real usage, this would call Claude Code's Task tool
        return {
            'status': AgentStatus.COMPLETED,
            'output': f"Executed task: {task.name}",
            'sitrep': {
                'agent_name': task.name,
                'mission': task.prompt[:100],
                'status': 'GREEN',
            },
            'artifacts': {},
            'metrics': {},
        }

    def consolidate_sitreps(self) -> Optional[Dict[str, Any]]:
        """
        Consolidate all agent SITREPs into single report.

        Returns:
            Consolidated SITREP dictionary
        """
        if not self.current_result:
            return None

        sitreps = []
        for result in self.current_result.agent_results.values():
            if result.sitrep:
                sitreps.append(result.sitrep)

        if not sitreps:
            return None

        # In real implementation, would use SITREPGenerator.merge_sitreps
        # For now, create simple consolidated report
        consolidated = {
            'header': {
                'agent_name': 'Orchestrator',
                'mission': self.current_plan.name if self.current_plan else 'Unknown',
                'report_number': 1,
            },
            'status': {
                'overall_status': 'GREEN' if self.current_result.is_success() else 'RED',
                'completion_percentage': self.current_result.get_success_rate(),
            },
            'situation': {
                'summary': f"Orchestrated {len(sitreps)} agents",
                'tasks': [],
            },
            'agent_sitreps': sitreps,
        }

        self.current_result.consolidated_sitrep = consolidated
        return consolidated

    def get_status(self) -> Optional[Dict[str, Any]]:
        """
        Get current orchestration status.

        Returns:
            Status dictionary or None if no active orchestration
        """
        if not self.current_result:
            return None

        return {
            'plan_id': self.current_result.plan_id,
            'plan_name': self.current_result.plan_name,
            'total_tasks': self.current_result.total_tasks,
            'completed': self.current_result.completed_tasks,
            'failed': self.current_result.failed_tasks,
            'cancelled': self.current_result.cancelled_tasks,
            'success_rate': self.current_result.get_success_rate(),
            'duration': self.current_result.duration_seconds,
        }
