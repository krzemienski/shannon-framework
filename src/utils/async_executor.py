"""
Async parallel execution engine for Shannon Framework.

Provides parallel task execution with resource management, progress tracking,
and comprehensive error handling.
"""

import asyncio
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Coroutine, Dict, List, Optional, Set, TypeVar


logger = logging.getLogger(__name__)

T = TypeVar("T")


class TaskStatus(Enum):
    """Status of async task execution."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskResult:
    """Result of async task execution."""
    task_id: str
    status: TaskStatus
    result: Any = None
    error: Optional[Exception] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def success(self) -> bool:
        """Check if task completed successfully."""
        return self.status == TaskStatus.COMPLETED


@dataclass
class ExecutionReport:
    """Report of parallel execution."""
    total_tasks: int
    completed: int
    failed: int
    cancelled: int
    total_duration: float
    average_duration: float
    results: List[TaskResult]
    errors: Dict[str, Exception]


class TaskMonitor:
    """
    Monitors progress of async task execution.

    Tracks task status, timing, and provides progress reporting.
    """

    def __init__(self):
        """Initialize task monitor."""
        self.tasks: Dict[str, TaskResult] = {}
        self._lock = asyncio.Lock()

    async def register_task(
        self, task_id: str, metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Register a task for monitoring.

        Args:
            task_id: Task identifier
            metadata: Additional task metadata
        """
        async with self._lock:
            self.tasks[task_id] = TaskResult(
                task_id=task_id,
                status=TaskStatus.PENDING,
                metadata=metadata or {},
            )

    async def start_task(self, task_id: str) -> None:
        """
        Mark task as started.

        Args:
            task_id: Task identifier
        """
        async with self._lock:
            if task_id in self.tasks:
                self.tasks[task_id].status = TaskStatus.RUNNING
                self.tasks[task_id].start_time = datetime.now()

    async def complete_task(
        self, task_id: str, result: Any, error: Optional[Exception] = None
    ) -> None:
        """
        Mark task as completed.

        Args:
            task_id: Task identifier
            result: Task result
            error: Task error if failed
        """
        async with self._lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                task.end_time = datetime.now()

                if error:
                    task.status = TaskStatus.FAILED
                    task.error = error
                else:
                    task.status = TaskStatus.COMPLETED
                    task.result = result

                if task.start_time:
                    task.duration = (
                        task.end_time - task.start_time
                    ).total_seconds()

    async def cancel_task(self, task_id: str) -> None:
        """
        Mark task as cancelled.

        Args:
            task_id: Task identifier
        """
        async with self._lock:
            if task_id in self.tasks:
                self.tasks[task_id].status = TaskStatus.CANCELLED
                self.tasks[task_id].end_time = datetime.now()

    async def get_progress(self) -> Dict[str, int]:
        """
        Get current progress statistics.

        Returns:
            Dict with counts by status
        """
        async with self._lock:
            stats = defaultdict(int)
            for task in self.tasks.values():
                stats[task.status.value] += 1
            return dict(stats)

    async def get_task_results(self) -> List[TaskResult]:
        """Get all task results."""
        async with self._lock:
            return list(self.tasks.values())


class ExceptionAggregator:
    """
    Aggregates exceptions from parallel execution.

    Collects and categorizes errors for comprehensive error reporting.
    """

    def __init__(self):
        """Initialize exception aggregator."""
        self.exceptions: Dict[str, Exception] = {}
        self.exception_counts: Dict[type, int] = defaultdict(int)
        self._lock = asyncio.Lock()

    async def add_exception(self, task_id: str, exception: Exception) -> None:
        """
        Add exception from task.

        Args:
            task_id: Task identifier
            exception: Exception that occurred
        """
        async with self._lock:
            self.exceptions[task_id] = exception
            self.exception_counts[type(exception)] += 1

    async def get_exceptions(self) -> Dict[str, Exception]:
        """Get all exceptions."""
        async with self._lock:
            return dict(self.exceptions)

    async def get_exception_summary(self) -> Dict[str, int]:
        """Get exception type counts."""
        async with self._lock:
            return {
                exc_type.__name__: count
                for exc_type, count in self.exception_counts.items()
            }

    async def has_exceptions(self) -> bool:
        """Check if any exceptions occurred."""
        async with self._lock:
            return bool(self.exceptions)


class SemaphorePool:
    """
    Pool of semaphores for resource management.

    Limits concurrent execution based on resource type.
    """

    def __init__(self, default_limit: int = 10):
        """
        Initialize semaphore pool.

        Args:
            default_limit: Default concurrent task limit
        """
        self.default_limit = default_limit
        self.semaphores: Dict[str, asyncio.Semaphore] = {}
        self._lock = asyncio.Lock()

    async def acquire(self, resource_type: str, limit: Optional[int] = None) -> None:
        """
        Acquire semaphore for resource type.

        Args:
            resource_type: Type of resource
            limit: Optional custom limit
        """
        async with self._lock:
            if resource_type not in self.semaphores:
                sem_limit = limit or self.default_limit
                self.semaphores[resource_type] = asyncio.Semaphore(sem_limit)

        await self.semaphores[resource_type].acquire()

    def release(self, resource_type: str) -> None:
        """
        Release semaphore for resource type.

        Args:
            resource_type: Type of resource
        """
        if resource_type in self.semaphores:
            self.semaphores[resource_type].release()


class ParallelExecutor:
    """
    Parallel execution engine with resource management.

    Executes async tasks in parallel with configurable concurrency limits,
    progress tracking, and comprehensive error handling.
    """

    def __init__(
        self,
        max_concurrent: int = 10,
        timeout: Optional[float] = None,
    ):
        """
        Initialize parallel executor.

        Args:
            max_concurrent: Maximum concurrent tasks
            timeout: Optional timeout per task in seconds
        """
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self.monitor = TaskMonitor()
        self.aggregator = ExceptionAggregator()
        self.semaphore_pool = SemaphorePool(default_limit=max_concurrent)

    async def execute(
        self,
        tasks: List[Callable[..., Coroutine[Any, Any, T]]],
        task_args: Optional[List[tuple]] = None,
        task_kwargs: Optional[List[Dict[str, Any]]] = None,
        task_ids: Optional[List[str]] = None,
        resource_type: str = "default",
    ) -> ExecutionReport:
        """
        Execute tasks in parallel.

        Args:
            tasks: List of async functions to execute
            task_args: Optional list of positional args per task
            task_kwargs: Optional list of keyword args per task
            task_ids: Optional list of task identifiers
            resource_type: Resource type for semaphore pooling

        Returns:
            Execution report with results and statistics
        """
        start_time = datetime.now()
        num_tasks = len(tasks)

        # Prepare arguments
        args_list = task_args or [() for _ in range(num_tasks)]
        kwargs_list = task_kwargs or [{} for _ in range(num_tasks)]
        ids_list = task_ids or [f"task_{i}" for i in range(num_tasks)]

        # Register all tasks
        for task_id in ids_list:
            await self.monitor.register_task(task_id)

        # Create coroutines with monitoring
        coroutines = [
            self._execute_task(
                task_id=ids_list[i],
                task=tasks[i],
                args=args_list[i],
                kwargs=kwargs_list[i],
                resource_type=resource_type,
            )
            for i in range(num_tasks)
        ]

        # Execute all tasks in parallel
        results = await asyncio.gather(*coroutines, return_exceptions=True)

        # Process results
        task_results = await self.monitor.get_task_results()
        errors = await self.aggregator.get_exceptions()

        # Calculate statistics
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()

        completed = sum(1 for r in task_results if r.status == TaskStatus.COMPLETED)
        failed = sum(1 for r in task_results if r.status == TaskStatus.FAILED)
        cancelled = sum(1 for r in task_results if r.status == TaskStatus.CANCELLED)

        completed_durations = [
            r.duration for r in task_results if r.status == TaskStatus.COMPLETED
        ]
        average_duration = (
            sum(completed_durations) / len(completed_durations)
            if completed_durations
            else 0.0
        )

        return ExecutionReport(
            total_tasks=num_tasks,
            completed=completed,
            failed=failed,
            cancelled=cancelled,
            total_duration=total_duration,
            average_duration=average_duration,
            results=task_results,
            errors=errors,
        )

    async def _execute_task(
        self,
        task_id: str,
        task: Callable[..., Coroutine[Any, Any, T]],
        args: tuple,
        kwargs: Dict[str, Any],
        resource_type: str,
    ) -> Optional[T]:
        """
        Execute individual task with monitoring and error handling.

        Args:
            task_id: Task identifier
            task: Async function to execute
            args: Positional arguments
            kwargs: Keyword arguments
            resource_type: Resource type for semaphore

        Returns:
            Task result or None if failed
        """
        result = None
        error = None

        try:
            # Acquire resource semaphore
            await self.semaphore_pool.acquire(resource_type)

            try:
                # Mark task as started
                await self.monitor.start_task(task_id)

                # Execute with optional timeout
                if self.timeout:
                    result = await asyncio.wait_for(
                        task(*args, **kwargs), timeout=self.timeout
                    )
                else:
                    result = await task(*args, **kwargs)

            finally:
                # Release resource semaphore
                self.semaphore_pool.release(resource_type)

        except asyncio.TimeoutError as e:
            error = e
            logger.error(f"Task {task_id} timed out after {self.timeout}s")
            await self.aggregator.add_exception(task_id, e)

        except asyncio.CancelledError as e:
            error = e
            logger.warning(f"Task {task_id} was cancelled")
            await self.monitor.cancel_task(task_id)

        except Exception as e:
            error = e
            logger.error(f"Task {task_id} failed: {str(e)}")
            await self.aggregator.add_exception(task_id, e)

        finally:
            # Mark task as complete
            await self.monitor.complete_task(task_id, result, error)

        return result

    async def execute_with_batching(
        self,
        tasks: List[Callable[..., Coroutine[Any, Any, T]]],
        batch_size: int,
        task_args: Optional[List[tuple]] = None,
        task_kwargs: Optional[List[Dict[str, Any]]] = None,
        resource_type: str = "default",
    ) -> List[ExecutionReport]:
        """
        Execute tasks in batches.

        Args:
            tasks: List of async functions
            batch_size: Size of each batch
            task_args: Optional positional args per task
            task_kwargs: Optional keyword args per task
            resource_type: Resource type for semaphore

        Returns:
            List of execution reports per batch
        """
        reports = []
        num_tasks = len(tasks)

        # Prepare arguments
        args_list = task_args or [() for _ in range(num_tasks)]
        kwargs_list = task_kwargs or [{} for _ in range(num_tasks)]

        # Execute in batches
        for i in range(0, num_tasks, batch_size):
            batch_end = min(i + batch_size, num_tasks)
            batch_tasks = tasks[i:batch_end]
            batch_args = args_list[i:batch_end]
            batch_kwargs = kwargs_list[i:batch_end]
            batch_ids = [f"batch_{i//batch_size}_task_{j}" for j in range(len(batch_tasks))]

            logger.info(
                f"Executing batch {i//batch_size + 1}, tasks {i}-{batch_end}"
            )

            report = await self.execute(
                tasks=batch_tasks,
                task_args=batch_args,
                task_kwargs=batch_kwargs,
                task_ids=batch_ids,
                resource_type=resource_type,
            )

            reports.append(report)

        return reports

    async def get_progress(self) -> Dict[str, int]:
        """Get current execution progress."""
        return await self.monitor.get_progress()

    async def has_errors(self) -> bool:
        """Check if any tasks failed."""
        return await self.aggregator.has_exceptions()


# Global parallel executor instance
_global_executor: Optional[ParallelExecutor] = None


def get_parallel_executor(
    max_concurrent: Optional[int] = None, timeout: Optional[float] = None
) -> ParallelExecutor:
    """
    Get or create global parallel executor.

    Args:
        max_concurrent: Override max concurrent tasks
        timeout: Override timeout

    Returns:
        Parallel executor instance
    """
    global _global_executor
    if _global_executor is None:
        _global_executor = ParallelExecutor(
            max_concurrent=max_concurrent or 10, timeout=timeout
        )
    return _global_executor